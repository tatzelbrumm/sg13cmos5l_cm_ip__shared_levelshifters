#!/usr/bin/env python3
"""Generate the xschem schematics/symbols of the level-shifter pair.
Pin offsets are those of sg13cmos5l_pr/sg13_{lv,hv}_{nmos,pmos}.sym (read from the PDK):
  nmos: D (20,-30) G (-20,0) S (20,30) B (20,0)
  pmos: D (20,30)  G (-20,0) S (20,-30) B (20,0)   (source on top)
flip=1 negates x of the pin offsets.  All coordinates are on the 10-unit grid."""
import os
OFF={'nmos':{'D':(20,-30),'G':(-20,0),'S':(20,30),'B':(20,0)},
     'pmos':{'D':(20,30),'G':(-20,0),'S':(20,-30),'B':(20,0)}}
class Sch:
    def __init__(s): s.w=[]; s.c=[]; s.devs={}
    def wire(s,x1,y1,x2,y2,lab=None):
        assert all(v%10==0 for v in (x1,y1,x2,y2)),(x1,y1,x2,y2)
        assert x1==x2 or y1==y2,'diagonal wire'
        s.w.append((x1,y1,x2,y2,lab))
    def path(s,*pts,lab=None):
        for a,b in zip(pts,pts[1:]): s.wire(*a,*b,lab=lab)
    def mos(s,name,kind,volt,x,y,flip,w,l,m=1,ng=1):
        model=f'sg13_{volt}_{kind}'
        props=f"name={name}\nl={l}\nw={w}\nng={ng}\nm={m}\nmm_ok=1\nmodel={model}\nspiceprefix=X"
        s.c.append(f"C {{sg13cmos5l_pr/{model}.sym}} {x} {y} 0 {flip} {{{props}\n}}")
        s.devs[name]=(kind,x,y,flip)
    def pin(s,name,p):
        kind,x,y,flip=s.devs[name]; ox,oy=OFF[kind][p]
        if flip: ox=-ox
        return (x+ox,y+oy)
    def bulk_to_source(s,name,lab=None):
        kind,x,y,flip=s.devs[name]
        b=s.pin(name,'B'); sp=s.pin(name,'S'); xo=x+(-40 if flip else 40)
        s.path(b,(xo,b[1]),(xo,sp[1]),sp,lab=lab)
    def lab_pin(s,x,y,lab,rot=0):
        s.c.append(f"C {{lab_pin.sym}} {x} {y} {rot} 0 {{name=l{len(s.c)} sig_type=std_logic lab={lab}}}")
    def port(s,kind,x,y,lab,flip=0):
        s.c.append(f"C {{{kind}.sym}} {x} {y} 0 {flip} {{name=p{len(s.c)} lab={lab}}}")
    def text(s,x,y,t,size=0.4):
        s.c.append(f"T {{{t}}} {x} {y} 0 0 {size} {size} {{}}")
    def dump(s,path):
        out=["v {xschem version=3.4.4 file_version=1.2}","G {}","K {}","V {}","S {}","E {}"]
        for x1,y1,x2,y2,lab in s.w:
            out.append(f"N {x1} {y1} {x2} {y2} {{lab={lab}}}" if lab else f"N {x1} {y1} {x2} {y2} {{}}")
        out+=s.c
        open(path,'w').write("\n".join(out)+"\n")
def sym(path,desc,pins,w=150,h=70):
    """pins: list of (name, side) side in L,R,T,B ; order = subckt port order"""
    cnt={'L':0,'R':0,'T':0,'B':0}; lines=[]; texts=[]
    n={'L':sum(1 for p in pins if p[1]=='L'),'R':sum(1 for p in pins if p[1]=='R'),'T':sum(1 for p in pins if p[1]=='T'),'B':sum(1 for p in pins if p[1]=='B')}
    pos={}
    for name,side in pins:
        i=cnt[side]; cnt[side]+=1
        if side=='L': pos[name]=(-w,0)
        if side=='R': pos[name]=(w,0)
        if side=='T': pos[name]=(-60+i*120 if n['T']>1 else 0,-h)
        if side=='B': pos[name]=(0,h)
    out=['v {xschem version=3.4.4 file_version=1.2}','G {}',
         'K {type=subcircuit\nformat="@name @pinlist @symname"\ntemplate="name=x1"\ndescription="'+desc+'"\n}','V {}','S {}','E {}',
         f'P 4 5 {-w+20} {-h+20} {w-20} {-h+20} {w-20} {h-20} {-w+20} {h-20} {-w+20} {-h+20} {{}}']
    for name,side in pins:
        x,y=pos[name]; dirn='in' if name=='in' else 'out' if name=='out' else 'inout'
        if side=='L': out.append(f'L 7 {x} {y} {x+20} {y} {{}}'); tx,ty=x+25,y-8
        if side=='R': out.append(f'L 7 {x-20} {y} {x} {y} {{}}'); tx,ty=x-25-len(name)*10,y-8
        if side=='T': out.append(f'L 7 {x} {y} {x} {y+20} {{}}'); tx,ty=x-len(name)*5,y+25
        if side=='B': out.append(f'L 7 {x} {y-20} {x} {y} {{}}'); tx,ty=x-len(name)*5,y-45
        out.append(f'B 5 {x-2.5} {y-2.5} {x+2.5} {y+2.5} {{name={name} dir={dirn}}}')
        out.append(f'T {{{name}}} {tx} {ty} 0 0 0.2 0.2 {{}}')
    return out
def write_sym(path,desc,pins,title,w=150,h=70):
    o=sym(path,desc,pins,w,h); o.append(f'T {{{title}}} {-w+30} -10 0 0 0.3 0.3 {{}}')
    open(path,'w').write("\n".join(o)+"\n")

D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','xschem')
# ------------------------------------------------------------------ ls_up
s=Sch()
s.mos('M2','pmos','lv',200,-200,0,'1.2u','0.13u')
s.mos('M1','nmos','lv',200,-100,0,'0.6u','0.13u')
s.mos('M3','nmos','hv',410,-100,0,'2u','0.45u',m=4)
s.mos('M6','pmos','hv',450,-200,1,'2u','0.4u')
s.mos('M5','pmos','hv',590,-200,0,'2u','0.4u')
s.mos('M4','nmos','hv',630,-100,1,'2u','0.45u',m=4)
s.mos('M16','pmos','hv',840,-200,0,'2u','0.4u',m=2)
s.mos('M12','nmos','hv',840,-100,0,'2u','0.45u')
for n in s.devs: s.bulk_to_source(n)
# rails (wires): vddh bus top, vss bus bottom, vddl for the LV inverter
s.path((60,-340),(430,-340),(430,-300),lab='vddh'); s.wire(430,-300,860,-300,'vddh')
for n in ('M6','M5','M16'): p=s.pin(n,'S'); s.wire(p[0],p[1],p[0],-300,'vddh')
s.wire(60,-300,220,-300,'vddl'); s.wire(220,-230,220,-300,'vddl')
s.wire(60,-30,860,-30,'vss')
for n in ('M1','M3','M4','M12'): p=s.pin(n,'S'); s.wire(p[0],p[1],p[0],-30,'vss')
# LV inverter  (in -> inb)
s.path((180,-200),(160,-200),(160,-100),(180,-100),lab='in'); s.wire(60,-150,160,-150,'in')
s.wire(220,-170,220,-130,'inb'); s.wire(220,-150,260,-150,'inb'); s.lab_pin(260,-150,'inb',2)
# cross-coupled latch
s.wire(430,-170,430,-130,'a'); s.wire(430,-150,410,-150,'a'); s.lab_pin(410,-150,'a',0); s.path((430,-160),(550,-160),(550,-200),(570,-200),lab='a')
s.wire(610,-170,610,-130,'b'); s.wire(610,-150,630,-150,'b'); s.lab_pin(630,-150,'b',2); s.path((610,-140),(490,-140),(490,-200),(470,-200),lab='b')
s.wire(390,-100,370,-100,'in'); s.lab_pin(370,-100,'in',0)
s.wire(650,-100,670,-100,'inb'); s.lab_pin(670,-100,'inb',2)
# output buffer
s.path((820,-200),(800,-200),(800,-100),(820,-100),lab='a'); s.wire(800,-150,780,-150,'a'); s.lab_pin(780,-150,'a',0)
s.wire(860,-170,860,-130,'out'); s.wire(860,-150,1000,-150,'out')
s.port('iopin',60,-30,'vss',1); s.port('iopin',60,-300,'vddl',1); s.port('iopin',60,-340,'vddh',1)
s.port('opin',1000,-150,'out',0); s.port('ipin',60,-150,'in')
s.text(60,-420,'ls_up_1v2_3v3: 1.2 V -> 3.3 V level shifter, non-inverting',0.5)
s.text(60,-390,'Netlist identical to SAR_ADC_IHP level_shifter_1v2_to_3v3 (Apache-2.0, Arjun Ananth et al.)',0.3)
s.text(60,40,'in: 0..VDDL   out: 0..VDDH   vddl 1.08-1.32 V, vddh 3.0-3.6 V.  Needs VDDL >= 1.08 V (tt: 1.0 V).',0.3)
s.dump(os.path.join(D,'ls_up_1v2_3v3.sch'))
write_sym(os.path.join(D,'ls_up_1v2_3v3.sym'),'1.2V to 3.3V level shifter (non-inverting), IHP SG13CMOS5L',
          [('vss','B'),('vddl','T'),('vddh','T'),('out','R'),('in','L')],'1.2V -> 3.3V')
# ------------------------------------------------------------------ ls_dn
d=Sch()
d.mos('MP1','pmos','hv',300,-200,0,'1u','0.45u')
d.mos('MN1','nmos','hv',300,-100,0,'0.8u','0.45u')
d.bulk_to_source('MP1'); d.bulk_to_source('MN1')
d.path((60,-300),(320,-300),lab='vddl'); d.wire(320,-230,320,-300,'vddl')
d.wire(60,-30,320,-30,'vss'); d.wire(320,-70,320,-30,'vss')
d.path((280,-200),(260,-200),(260,-100),(280,-100),lab='in'); d.wire(60,-150,260,-150,'in')
d.wire(320,-170,320,-130,'out'); d.wire(320,-150,500,-150,'out')
d.port('iopin',60,-30,'vss',1); d.port('iopin',60,-300,'vddl',1); d.port('opin',500,-150,'out',0); d.port('ipin',60,-150,'in')
d.text(60,-420,'ls_dn_3v3_1v2: 3.3 V -> 1.2 V level shifter, INVERTING',0.5)
d.text(60,-390,'HV inverter powered from VDDL (pattern of bidir-level-shifter bidir_channel MMP8/MMN9)',0.3)
d.text(60,40,'in: 0..VDDH (3.0-3.6 V)   out: 0..VDDL.  Low switching threshold (~0.6 V): rise/fall delays differ by 1-2.5 ns.',0.3)
d.dump(os.path.join(D,'ls_dn_3v3_1v2.sch'))
write_sym(os.path.join(D,'ls_dn_3v3_1v2.sym'),'3.3V to 1.2V level shifter (inverting), IHP SG13CMOS5L',
          [('vss','B'),('vddl','T'),('out','R'),('in','L')],'3.3V -> 1.2V (inv)',w=150,h=70)
print('written')
