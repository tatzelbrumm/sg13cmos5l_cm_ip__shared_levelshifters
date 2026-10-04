#!/usr/bin/env python3
"""Supply / input current and charge characterization of the level shifters.

Usage:  run_iq.py tb_ls_up|tb_ls_dn  MODE  [--gmin G]
  MODE  tr     input transition time sweep, tt / 27 C / nominal supplies
        cload  load capacitance sweep (separates load charge from intrinsic charge)
        pvt    5 corners x 3 temperatures x 3 supplies, TR = 100 ps
        gmin   quiescent current vs simulator gmin (tt / 27 C), to see what is model and what is simulator
Writes simulation/iq_<tb>_<mode>.json.  Needs xschem, ngspice, PDK_ROOT, PDK (default ihp-sg13cmos5l).

For every run: one rising and one falling input edge, input transition time TR (0 -> full swing),
  td = 10 ns delay, PW = 60 ns high.  Per edge (window = edge start .. 10 ns after the input is done):
    q_<s>_<e>      integral of the source current i(<s>) over the window (A s), as ngspice measures it
    ib_<s>_<e>     the same source's current just before the edge (baseline, A)
    ipmin/ipmax    most negative / most positive source current in the window (A)
  <s> = h (VH = vddh), l (VL = vddl), i (VIN = input source);  <e> = r (input rises), f (input falls).
  Quiescent currents: iq_<s>_lo (input low) and iq_<s>_hi (input high), averaged over 3.5 ns.
Sign convention of ngspice: a source that delivers current has a NEGATIVE i(V...).  The postprocessing
turns this around: a positive current or charge below is delivered BY the source.
"""
import os,re,subprocess,sys,json,time
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..')); SIM=os.path.join(ROOT,'simulation')
os.environ.setdefault('PDK','ihp-sg13cmos5l')
TD=10e-9; PW=60e-9; TSET=10e-9
def ns(x): return '%.6g'%x

def base_deck(tb):
    net=os.path.join(SIM,tb+'.spice')
    if os.path.exists(net): os.remove(net)
    subprocess.run(['xschem','--rcfile',os.path.join(ROOT,'xschemrc'),'-n','-s','-q','-x','-o',SIM,'-N',tb+'.spice',os.path.join(ROOT,'tb',tb+'.sch')],
                   cwd=ROOT,env=dict(os.environ,PWD=ROOT),capture_output=True,text=True)
    if not os.path.exists(net): sys.exit('xschem produced no netlist')
    t=open(net).read()
    t=re.sub(r'^\.(meas|tran|param|temp|options)\b.*\n','',t,flags=re.M)      # our own analysis replaces the tb's
    t=re.sub(r'^\.control\b[\s\S]*?^\.endc\b.*\n','',t,flags=re.M)
    return t

def deck(base,tb,corner,T,vl,vh,tr,cload,gmin):
    vin_hi = vh if tb=='tb_ls_dn' else vl
    t=re.sub(r'^VIN .*$',f'VIN in GND PULSE(0 {vin_hi} {ns(TD)} {ns(tr)} {ns(tr)} {ns(PW)} 1)',base,flags=re.M)
    t=t.replace('mos_tt','mos_'+corner)
    tr_end=TD+tr; tf0=TD+tr+PW; tf_end=tf0+tr; tstop=tf_end+TSET+5e-9
    L=[f'.temp {T}',f'.param VDDL={vl} VDDH={vh} CLOAD={ns(cload)} TR={ns(tr)}',
       f'.options gmin={gmin} abstol=1e-15 reltol=1e-4',
       f'.tran 20p {ns(tstop)}']
    for e,t0,t1 in (('r',TD,tr_end+TSET),('f',tf0,tf_end+TSET)):
        for s,src in (('h','VH'),('l','VL'),('i','VIN')):
            L.append(f'.meas tran q_{s}_{e} integ i({src}) from={ns(t0)} to={ns(t1)}')
            L.append(f'.meas tran ib_{s}_{e} avg i({src}) from={ns(t0-4e-9)} to={ns(t0-0.5e-9)}')
            L.append(f'.meas tran ipmin_{s}_{e} min i({src}) from={ns(t0)} to={ns(t1)}')
            L.append(f'.meas tran ipmax_{s}_{e} max i({src}) from={ns(t0)} to={ns(t1)}')
    for s,src in (('h','VH'),('l','VL'),('i','VIN')):
        L.append(f'.meas tran iq_{s}_lo avg i({src}) from={ns(TD-4e-9)} to={ns(TD-0.5e-9)}')
        L.append(f'.meas tran iq_{s}_hi avg i({src}) from={ns(tf0-4e-9)} to={ns(tf0-0.5e-9)}')
    L.append('.meas tran vout_lo avg v(out) from=%s to=%s'%(ns(TD-4e-9),ns(TD-0.5e-9)))
    L.append('.meas tran vout_hi avg v(out) from=%s to=%s'%(ns(tf0-4e-9),ns(tf0-0.5e-9)))
    L.append('.control\npre_osdi %s/%s/libs.tech/ngspice/osdi/psp103_nqs.osdi\nrun\nquit\n.endc'%(os.environ['PDK_ROOT'],os.environ['PDK']))
    # lib lines of the tb carry the corner; insert our block before .end
    return t.replace('\n.end\n','\n'+'\n'.join(L)+'\n.end\n')

def run(base,tb,corner='tt',T=27,vl=1.2,vh=3.3,tr=100e-12,cload=20e-15,gmin=1e-15):
    f=os.path.join(SIM,'_iq.cir'); open(f,'w').write(deck(base,tb,corner,T,vl,vh,tr,cload,gmin))
    r=subprocess.run(['ngspice','-b',f],capture_output=True,text=True,env=dict(os.environ,OMP_NUM_THREADS='1'),timeout=60)
    res={k.lower():(None if v=='failed' else float(v)) for k,v in re.findall(r'^(\w+)\s*=\s*([-+0-9.eE]+|failed)',r.stdout,re.M)}
    res.update(corner=corner,T=T,vddl=vl,vddh=vh,tr=tr,cload=cload,gmin=gmin)
    return res

if __name__=='__main__':
    tb=sys.argv[1]; mode=sys.argv[2]
    base=base_deck(tb); rows=[]; t0=time.time()
    def add(**kw):
        r=run(base,tb,**kw); rows.append(r)
        print(' '.join(f'{k}={r[k]}' for k in ('corner','T','vddl','vddh','tr','cload','gmin')),
              ' ok' if r.get('q_h_r') is not None else ' FAILED',flush=True)
    if mode=='tr':
        for tr in (20e-12,50e-12,100e-12,300e-12,1e-9,3e-9,10e-9): add(tr=tr)
    elif mode=='cload':
        for c in (1e-15,20e-15,50e-15,100e-15): add(cload=c)
    elif mode=='gmin':
        for T in (27,125):
            for g in (1e-12,1e-15,1e-18): add(T=T,gmin=g)
    elif mode=='pvt':
        for c in ('tt','ss','ff','sf','fs'):
            for T in (-40,27,125):
                for vl,vh in ((1.08,3.6),(1.2,3.3),(1.32,3.0)): add(corner=c,T=T,vl=vl,vh=vh)
    json.dump(rows,open(os.path.join(SIM,f'iq_{tb}_{mode}.json'),'w'),indent=1)
    print('done %d runs in %.0f s'%(len(rows),time.time()-t0))
