import subprocess, os, re, sys, itertools, json, tempfile
from concurrent.futures import ThreadPoolExecutor
HERE=os.path.dirname(os.path.abspath(__file__))
UP={ # name: (dut lines, polarity note)
 'sar_l2h':   "Xd vss vddl vddh out in sar_l2h",
 'bidir_up':  "Xd in out outb vddl vddh vss bidir_up\nCoutb outb vss {CL}",
 'harness_ls':"Xd vss vddl vddh out in harn_ls_w",
 'hsxo_xd':   "Xd vss vddl vddh out in hsxo_ls",
 'lpopamp_st':"Xd vss vddl vddh out in lpop_ls",
}
def netlist_up(name,corner,T,vl,vh,cl='50f',tr='100p'):
    dut=UP[name].replace('{CL}',cl)
    return f"""* up {name}
.lib {HERE}/models/cornerMOSlv.lib mos_{corner}
.lib {HERE}/models/cornerMOShv.lib mos_{corner}
.include {HERE}/cells.spice
.temp {T}
Vss vss 0 0
Vl vddl 0 {vl}
Vh vddh 0 {vh}
Vin in 0 PULSE(0 {vl} 10n {tr} {tr} 20n 50n)
{dut}
Cout out 0 {cl}
.tran 20p 48n
.meas tran tplh trig v(in) val={vl/2} rise=1 targ v(out) val={vh/2} rise=1
.meas tran tphl trig v(in) val={vl/2} fall=1 targ v(out) val={vh/2} fall=1
.meas tran voh avg v(out) from=26n to=29n
.meas tran vol avg v(out) from=6n to=9n
.meas tran ih_lo avg i(Vh) from=6n to=9n
.meas tran ih_hi avg i(Vh) from=26n to=29n
.meas tran il_lo avg i(Vl) from=6n to=9n
.meas tran il_hi avg i(Vl) from=26n to=29n
.control
pre_osdi {HERE}/models/psp103_nqs.osdi
run
quit
.endc
.end
"""
def run(nl,tag):
    d=tempfile.mkdtemp(dir=os.path.join(HERE,'tmp')) if os.path.isdir(os.path.join(HERE,'tmp')) else tempfile.mkdtemp()
    f=os.path.join(d,'t.cir'); open(f,'w').write(nl)
    try:
        p=subprocess.run(['ngspice','-b',f],capture_output=True,text=True,timeout=25)
        out=p.stdout+p.stderr
    except subprocess.TimeoutExpired:
        return {'_timeout':1},''
    res={}
    for m in re.finditer(r'^(\w+)\s*=\s*([-+0-9.eE]+|failed)',out,re.M):
        k,v=m.group(1).lower(),m.group(2)
        res[k]=None if v=='failed' else float(v)
    res['_err']= ('Error' in out or 'error' in out) and not res
    return res,out
if __name__=='__main__':
    os.makedirs(os.path.join(HERE,'tmp'),exist_ok=True)
    name=sys.argv[1]
    r,o=run(netlist_up(name,'tt',27,1.2,3.3),name)
    print(r); 
    if not r: print(o[-3000:])

def sweep(names,corners=('tt','ss','ff','sf','fs'),temps=(-40,27,125),sups=((1.08,3.6),(1.2,3.3),(1.32,3.0)),**kw):
    jobs=[(n,c,T,vl,vh) for n in names for c in corners for T in temps for (vl,vh) in sups]
    def f(j):
        n,c,T,vl,vh=j
        r,_=run(netlist_up(n,c,T,vl,vh,**kw),n)
        print(n,c,T,vl,vh,'TIMEOUT' if r.get('_timeout') else 'ok',flush=True)
        return dict(name=n,corner=c,T=T,vl=vl,vh=vh,**r)
    with ThreadPoolExecutor(1) as ex: return list(ex.map(f,jobs))

DN={
 'hvinv_dn':"Xd vss vddl vddh out in hvinv_dn",
 'sar_h2l':"Ven en 0 {vh}\nXi in inn vddh vss HVINV\nXd vss vddl vddh out in inn en sar_h2l",
}
def netlist_dn(name,corner,T,vl,vh,cl='20f',tr='500p'):
    dut=DN[name].replace('{vh}',str(vh))
    return f"""* dn {name}
.lib {HERE}/models/cornerMOSlv.lib mos_{corner}
.lib {HERE}/models/cornerMOShv.lib mos_{corner}
.include {HERE}/cells.spice
.temp {T}
Vss vss 0 0
Vl vddl 0 {vl}
Vh vddh 0 {vh}
Vin in 0 PULSE(0 {vh} 10n {tr} {tr} 20n 50n)
{dut}
Cout out 0 {cl}
.tran 20p 48n
.meas tran t_rr trig v(in) val={vh/2} rise=1 targ v(out) val={vl/2} rise=1
.meas tran t_rf trig v(in) val={vh/2} rise=1 targ v(out) val={vl/2} fall=1
.meas tran t_fr trig v(in) val={vh/2} fall=1 targ v(out) val={vl/2} rise=1
.meas tran t_ff trig v(in) val={vh/2} fall=1 targ v(out) val={vl/2} fall=1
.meas tran voh_in_hi avg v(out) from=26n to=29n
.meas tran vo_in_lo avg v(out) from=6n to=9n
.meas tran ih_lo avg i(Vh) from=6n to=9n
.meas tran ih_hi avg i(Vh) from=26n to=29n
.meas tran il_lo avg i(Vl) from=6n to=9n
.meas tran il_hi avg i(Vl) from=26n to=29n
.control
pre_osdi {HERE}/models/psp103_nqs.osdi
run
quit
.endc
.end
"""
