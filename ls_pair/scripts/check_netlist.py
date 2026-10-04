#!/usr/bin/env python3
"""Netlist every cell with xschem and compare it device by device with the source netlists.
Exit status 1 on any difference.  Usage: check_netlist.py   (needs xschem, PDK_ROOT, PDK)"""
import os,re,subprocess,sys,shutil
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..'))
SIM=os.path.join(ROOT,'simulation')
# Reference netlists (terminal order D G S B).  ls_up: SAR_ADC_IHP level_shifter_1v2_to_3v3.spice;
# ls_dn: bidir-level-shifter bidir_channel MMP8/MMN9.
REF={
'ls_up_1v2_3v3':("vss vddl vddh out in","""
M1 inb in vss vss sg13_lv_nmos w=0.6u l=0.13u ng=1
M2 inb in vddl vddl sg13_lv_pmos w=1.2u l=0.13u ng=1
M3 a in vss vss sg13_hv_nmos w=2u l=0.45u ng=1 m=4
M4 b inb vss vss sg13_hv_nmos w=2u l=0.45u ng=1 m=4
M5 b a vddh vddh sg13_hv_pmos w=2u l=0.4u ng=1
M6 a b vddh vddh sg13_hv_pmos w=2u l=0.4u ng=1
M12 out a vss vss sg13_hv_nmos w=2u l=0.45u ng=1
M16 out a vddh vddh sg13_hv_pmos w=2u l=0.4u ng=1 m=2
"""),
'ls_dn_3v3_1v2':("vss vddl out in","""
MP1 out in vddl vddl sg13_hv_pmos w=1u l=0.45u ng=1
MN1 out in vss vss sg13_hv_nmos w=0.8u l=0.45u ng=1
""")}
def num(v):
    m=re.fullmatch(r'([-+0-9.eE]+)([a-zA-Z]*)',v)
    if not m: return v
    f={'':1,'u':1e-6,'n':1e-9,'p':1e-12,'m':1e-3}[m.group(2).lower()] if m.group(2).lower() in ('','u','n','p','m') else None
    return round(float(m.group(1))*f,15) if f else v
def devs(text):
    d={}
    for ln in text.strip().splitlines():
        t=ln.split()
        if not t or t[0][0] in '*.+' : continue
        name=t[0][1:] if t[0].startswith('X') else t[0]
        nets=t[1:5]; model=t[5]; par={k:num(v) for k,v in (x.split('=') for x in t[6:])}
        par.pop('mm_ok',None); par.setdefault('m',1.0); par['m']=float(par['m']); par['ng']=float(par.get('ng',1))
        d[name]=(nets,model,par)
    return d
fail=0
for cell,(ports,ref) in REF.items():
    net=os.path.join(SIM,cell+'.spice')
    if os.path.exists(net): os.remove(net)
    env=dict(os.environ,PWD=ROOT)
    p=subprocess.run(['xschem','--rcfile',os.path.join(ROOT,'xschemrc'),'-n','-s','-q','-x','-o',SIM,'-N',cell+'.spice',os.path.join(ROOT,'xschem',cell+'.sch')],cwd=ROOT,env=env,capture_output=True,text=True)
    print(f'[{cell}] xschem exit {p.returncode}',p.stderr.strip()[-300:])
    if not os.path.exists(net): print('  NO NETLIST'); fail+=1; continue
    txt=open(net).read()
    m=re.search(r'^\.subckt\s+(\S+)\s+(.*)$',txt,re.M) or re.search(r'^\*\*\.subckt\s+(\S+)\s+(.*)$',txt,re.M)
    got_ports=m.group(2).split() if m else []
    if got_ports!=ports.split(): print('  PORT ORDER MISMATCH',got_ports,ports.split()); fail+=1
    body=txt[m.end():txt.index('.ends') if '.ends' in txt else len(txt)]
    a=devs(body); b=devs(ref)
    if set(a)!=set(b): print('  device set differs',sorted(set(a)^set(b))); fail+=1
    for k in sorted(set(a)&set(b)):
        if a[k]!=b[k]: print('  MISMATCH',k,'\n   xschem',a[k],'\n   source',b[k]); fail+=1
    print(f'  {len(a)} devices, ports {got_ports}, ', 'OK' if not fail else 'see above')
sys.exit(1 if fail else 0)
