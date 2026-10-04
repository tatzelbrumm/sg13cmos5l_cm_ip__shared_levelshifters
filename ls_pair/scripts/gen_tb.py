#!/usr/bin/env python3
"""Generate the xschem testbenches (tb/*.sch).  Pin offsets of the cell symbols: see gen_cells.py."""
import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','tb')
HDR=["v {xschem version=3.4.4 file_version=1.2}","G {}","K {}","V {}","S {}","E {}"]
class TB:
    def __init__(s): s.o=[]; s.n=0
    def wire(s,x1,y1,x2,y2,lab=''): s.o.append(f"N {x1} {y1} {x2} {y2} {{lab={lab}}}" if lab else f"N {x1} {y1} {x2} {y2} {{}}")
    def lab(s,x,y,l,rot=0): s.n+=1; s.o.append(f"C {{lab_pin.sym}} {x} {y} {rot} 0 {{name=p{s.n} sig_type=std_logic lab={l}}}")
    def gnd(s,x,y): s.n+=1; s.o.append(f"C {{gnd.sym}} {x} {y} 0 0 {{name=g{s.n} lab=GND}}")
    def vsrc(s,x,y,name,val,node):
        s.o.append(f"C {{vsource.sym}} {x} {y} 0 0 {{name={name} value=\"{val}\" savecurrent=false}}")
        s.wire(x,y-30,x,y-50); s.lab(x,y-50,node); s.gnd(x,y+30)
    def cap(s,x,y,name,val,node):
        s.o.append(f"C {{capa.sym}} {x} {y} 0 0 {{name={name} m=1 value={val}}}")
        s.wire(x,y-30,x,y-50); s.lab(x,y-50,node); s.gnd(x,y+30)
    def text(s,x,y,t,size=0.4): s.o.append(f"T {{{t}}} {x} {y} 0 0 {size} {size} {{}}")
    def code(s,x,y,name,val,tcl=True):
        f=' format="tcleval( @value )"' if tcl else ''
        s.o.append(f"C {{code_shown.sym}} {x} {y} 0 0 {{name={name} only_toplevel=false{f} value=\"{val}\"}}")
    def dump(s,p): open(p,'w').write("\n".join(HDR+s.o)+"\n")
MODELS=""".lib $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/models/cornerMOSlv.lib mos_tt
.lib $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/models/cornerMOShv.lib mos_tt
.temp 27"""
OSDI=""".control
pre_osdi $::env(PDK_ROOT)/$::env(PDK)/libs.tech/ngspice/osdi/psp103_nqs.osdi
run
.endc"""
def dut(t,sym,x,y,pins):
    t.o.append(f"C {{{sym}}} {x} {y} 0 0 {{name=x1}}")
    for (px,py,node,rot,dx,dy) in pins:
        if node=='GND': t.gnd(x+px,y+py); continue
        t.wire(x+px,y+py,x+px+dx,y+py+dy); t.lab(x+px+dx,y+py+dy,node,rot)
# ---------------------------------------------------------------- tb_ls_up
t=TB()
t.text(-300,-480,'tb_ls_up: ls_up_1v2_3v3, 1.2 V -> 3.3 V.  PVT sweep: scripts/run_pvt.py tb_ls_up',0.5)
dut(t,'ls_up_1v2_3v3.sym',420,-300,[(0,70,'GND',0,0,0),(-60,-70,'vddl',0,0,-20),(60,-70,'vddh',0,0,-20),(150,0,'out',2,30,0),(-150,0,'in',0,-20,0)])
t.vsrc(-200,-300,'VL','dc \\{VDDL\\}','vddl'); t.vsrc(-100,-300,'VH','dc \\{VDDH\\}','vddh')
t.vsrc(0,-300,'VIN','PULSE(0 \\{VDDL\\} 10n \\{TR\\} \\{TR\\} 20n 50n)','in'); t.cap(740,-300,'CL','\\{CLOAD\\}','out')
t.code(-300,-120,'CODE',MODELS+"""
.param VDDL=1.2 VDDH=3.3 CLOAD=50f TR=100p
.tran 20p 48n
.meas tran tplh trig v(in) val='VDDL/2' rise=1 targ v(out) val='VDDH/2' rise=1
.meas tran tphl trig v(in) val='VDDL/2' fall=1 targ v(out) val='VDDH/2' fall=1
.meas tran voh avg v(out) from=26n to=29n
.meas tran vol avg v(out) from=6n to=9n
.meas tran ih_lo avg i(VH) from=6n to=9n
.meas tran ih_hi avg i(VH) from=26n to=29n
.meas tran il_lo avg i(VL) from=6n to=9n
.meas tran il_hi avg i(VL) from=26n to=29n
"""+OSDI)
t.dump(os.path.join(D,'tb_ls_up.sch'))
# ---------------------------------------------------------------- tb_ls_dn
t=TB()
t.text(-300,-480,'tb_ls_dn: ls_dn_3v3_1v2, 3.3 V -> 1.2 V (inverting).  PVT sweep: scripts/run_pvt.py tb_ls_dn',0.5)
dut(t,'ls_dn_3v3_1v2.sym',420,-300,[(0,70,'GND',0,0,0),(0,-70,'vddl',0,0,-20),(150,0,'out',2,30,0),(-150,0,'in',0,-20,0)])
t.vsrc(-200,-300,'VL','dc \\{VDDL\\}','vddl'); t.vsrc(-100,-300,'VH','dc \\{VDDH\\}','vddh')
t.vsrc(0,-300,'VIN','PULSE(0 \\{VDDH\\} 10n \\{TR\\} \\{TR\\} 20n 50n)','in'); t.cap(740,-300,'CL','\\{CLOAD\\}','out')
t.code(-300,-120,'CODE',MODELS+"""
.param VDDL=1.2 VDDH=3.3 CLOAD=20f TR=500p
.tran 20p 48n
.meas tran t_rf trig v(in) val='VDDH/2' rise=1 targ v(out) val='VDDL/2' fall=1
.meas tran t_fr trig v(in) val='VDDH/2' fall=1 targ v(out) val='VDDL/2' rise=1
.meas tran voh avg v(out) from=6n to=9n
.meas tran vol avg v(out) from=26n to=29n
.meas tran ih_lo avg i(VH) from=6n to=9n
.meas tran ih_hi avg i(VH) from=26n to=29n
.meas tran il_lo avg i(VL) from=6n to=9n
.meas tran il_hi avg i(VL) from=26n to=29n
"""+OSDI)
t.dump(os.path.join(D,'tb_ls_dn.sch'))
# ---------------------------------------------------------------- tb_ls_loop
t=TB()
t.text(-300,-480,'tb_ls_loop: 1.2 V -> ls_up -> 3.3 V node h -> ls_dn -> 1.2 V (net inversion)',0.5)
t.o.append("C {ls_up_1v2_3v3.sym} 420 -300 0 0 {name=x1}")
for (px,py,node,rot,dx,dy) in [(0,70,'GND',0,0,0),(-60,-70,'vddl',0,0,-20),(60,-70,'vddh',0,0,-20),(150,0,'h',2,30,0),(-150,0,'in',0,-20,0)]:
    t.wire(420+px,-300+py,420+px+dx,-300+py+dy) if (dx or dy) else None
    t.lab(420+px+dx,-300+py+dy,node,rot) if node!='GND' else t.gnd(420+px,-300+py)
t.o.append("C {ls_dn_3v3_1v2.sym} 900 -300 0 0 {name=x2}")
for (px,py,node,rot,dx,dy) in [(0,70,'GND',0,0,0),(0,-70,'vddl',0,0,-20),(150,0,'out',2,30,0),(-150,0,'h',0,-20,0)]:
    t.wire(900+px,-300+py,900+px+dx,-300+py+dy) if (dx or dy) else None
    t.lab(900+px+dx,-300+py+dy,node,rot) if node!='GND' else t.gnd(900+px,-300+py)
t.vsrc(-200,-300,'VL','dc \\{VDDL\\}','vddl'); t.vsrc(-100,-300,'VH','dc \\{VDDH\\}','vddh')
t.vsrc(0,-300,'VIN','PULSE(0 \\{VDDL\\} 10n \\{TR\\} \\{TR\\} 20n 50n)','in')
t.cap(600,-300,'CH','\\{CHIGH\\}','h'); t.cap(1220,-300,'CL','\\{CLOAD\\}','out')
t.code(-300,-120,'CODE',MODELS+"""
.param VDDL=1.2 VDDH=3.3 CHIGH=50f CLOAD=20f TR=100p
.tran 20p 48n
.meas tran t_up_rise trig v(in) val='VDDL/2' rise=1 targ v(h) val='VDDH/2' rise=1
.meas tran t_up_fall trig v(in) val='VDDL/2' fall=1 targ v(h) val='VDDH/2' fall=1
.meas tran t_rf trig v(in) val='VDDL/2' rise=1 targ v(out) val='VDDL/2' fall=1
.meas tran t_fr trig v(in) val='VDDL/2' fall=1 targ v(out) val='VDDL/2' rise=1
.meas tran vh_hi avg v(h) from=26n to=29n
.meas tran vout_lo avg v(out) from=26n to=29n
.meas tran vout_hi avg v(out) from=6n to=9n
.meas tran ih_lo avg i(VH) from=6n to=9n
.meas tran ih_hi avg i(VH) from=26n to=29n
"""+OSDI)
t.dump(os.path.join(D,'tb_ls_loop.sch'))
print('tb written')
