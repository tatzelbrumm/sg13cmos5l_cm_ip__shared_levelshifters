#!/usr/bin/env python3
"""Netlist a testbench with xschem and run it over PVT corners with ngspice.
Usage:  run_pvt.py tb_ls_up|tb_ls_dn|tb_ls_loop [--quick]
Needs xschem, ngspice, PDK_ROOT and PDK (default ihp-sg13cmos5l), and the PSP103 OSDI at
$PDK_ROOT/$PDK/libs.tech/ngspice/osdi/psp103_nqs.osdi.
Runs the points one after the other: parallel ngspice runs stalled each other on a 2-core machine."""
import os,re,subprocess,sys,json
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..')); SIM=os.path.join(ROOT,'simulation')
tb=sys.argv[1]; quick='--quick' in sys.argv
os.environ.setdefault('PDK','ihp-sg13cmos5l')
net=os.path.join(SIM,tb+'.spice')
if os.path.exists(net): os.remove(net)
p=subprocess.run(['xschem','--rcfile',os.path.join(ROOT,'xschemrc'),'-n','-s','-q','-x','-o',SIM,'-N',tb+'.spice',os.path.join(ROOT,'tb',tb+'.sch')],cwd=ROOT,env=dict(os.environ,PWD=ROOT),capture_output=True,text=True)
if not os.path.exists(net): sys.exit('xschem produced no netlist:\n'+p.stderr)
base=open(net).read()
base=re.sub(r'^\.end\b','.end',base,flags=re.M)
corners=['tt'] if quick else ['tt','ss','ff','sf','fs']
temps=[27] if quick else [-40,27,125]
sups=[(1.2,3.3)] if quick else [(1.08,3.6),(1.2,3.3),(1.32,3.0)]
rows=[]
for c in corners:
  for T in temps:
    for vl,vh in sups:
        t=base.replace('mos_tt','mos_'+c)
        t=re.sub(r'^\.temp\s+\S+','.temp %s'%T,t,flags=re.M)
        t=re.sub(r'(\.param\s+)VDDL=\S+\s+VDDH=\S+',r'\g<1>VDDL=%s VDDH=%s'%(vl,vh),t)
        t=t.replace('.endc','quit\n.endc',1)
        f=os.path.join(SIM,'_run.cir'); open(f,'w').write(t)
        r=subprocess.run(['ngspice','-b',f],capture_output=True,text=True,env=dict(os.environ,OMP_NUM_THREADS='1'),timeout=120)
        res={k.lower():(None if v=='failed' else float(v)) for k,v in re.findall(r'^(\w+)\s*=\s*([-+0-9.eE]+|failed)',r.stdout,re.M)}
        res.update(corner=c,T=T,vddl=vl,vddh=vh); rows.append(res)
        print(' '.join(f'{k}={v:.3g}' if isinstance(v,float) else f'{k}={v}' for k,v in res.items()),flush=True)
json.dump(rows,open(os.path.join(SIM,tb+'_pvt.json'),'w'),indent=1)
