#!/usr/bin/env python3
"""Summarize simulation/iq_<tb>_<mode>.json written by run_iq.py.
Sign convention here: positive = delivered BY the source (ngspice reports the opposite sign).
Charges are net of the pre-edge baseline current over the measurement window (edge start .. 10 ns after the input is done).
Usage: analyze_iq.py [tb_ls_up tb_ls_dn]"""
import json,os,sys
HERE=os.path.dirname(os.path.abspath(__file__)); SIM=os.path.join(HERE,'..','simulation')
TSET=10e-9
def load(tb,mode):
    p=os.path.join(SIM,f'iq_{tb}_{mode}.json')
    return json.load(open(p)) if os.path.exists(p) else []
def Q(r,s,e):           # net charge delivered by source s during edge e, fC
    q=r.get(f'q_{s}_{e}'); ib=r.get(f'ib_{s}_{e}')
    if q is None or ib is None: return None
    return -(q-ib*(r['tr']+TSET))*1e15
def IP(r,s,e):          # peak delivered / absorbed current, uA
    a=r.get(f'ipmin_{s}_{e}'); b=r.get(f'ipmax_{s}_{e}')
    if a is None: return None
    return -a*1e6, b*1e6
def IQ(r,s,st):
    v=r.get(f'iq_{s}_{st}'); return None if v is None else -v
def f(x,fmt='%.3g'): return 'NA' if x is None else fmt%x
def row(r): return '%s %4dC %.2f/%.1fV'%(r['corner'],r['T'],r['vddl'],r['vddh'])

def tr_table(tb):
    rows=load(tb,'tr')
    print(f'--- {tb}: input transition time TR (tt, 27 C, VDDL 1.2 V, VDDH 3.3 V, CL 20 fF); charge in fC, peak in uA')
    print('   TR     | Qh_r   Qh_f  | Ql_r   Ql_f  | Qin_r  Qin_f | pk_h_r pk_h_f | pk_l_r pk_l_f | pk_in_r pk_in_f')
    for r in rows:
        pk=lambda s,e: f(IP(r,s,e)[0]) if IP(r,s,e) else 'NA'
        print('%8.3g | %6s %6s | %6s %6s | %6s %6s | %6s %6s | %6s %6s | %6s %6s'%(r['tr'],
            f(Q(r,'h','r')),f(Q(r,'h','f')),f(Q(r,'l','r')),f(Q(r,'l','f')),f(Q(r,'i','r')),f(Q(r,'i','f')),
            pk('h','r'),pk('h','f'),pk('l','r'),pk('l','f'),pk('i','r'),pk('i','f')))
def cl_table(tb):
    rows=load(tb,'cload')
    print(f'--- {tb}: load capacitance (tt, 27 C, nominal, TR 100 ps); fC.  Last row: linear fit Q = Q0 + k*CL')
    for r in rows: print('CL=%6.3g | Qh_r %7s Qh_f %7s | Ql_r %7s Ql_f %7s'%(r['cload'],f(Q(r,'h','r')),f(Q(r,'h','f')),f(Q(r,'l','r')),f(Q(r,'l','f'))))
    import numpy as np
    for s in 'hl':
        for e in 'rf':
            y=[Q(r,s,e) for r in rows]; x=[r['cload']*1e15 for r in rows]
            if None in y or max(abs(v) for v in y)<0.05: continue
            k,q0=np.polyfit(x,y,1); print(f'   fit Q{s}_{e}: Q0 = {q0:.3g} fC, k = {k:.3g} V')
def iq_table(tb):
    rows=load(tb,'pvt')
    print(f'--- {tb}: quiescent current, PVT (A, delivered by the source; | = min .. max over the 45 points, worst case in brackets)')
    for s,name in (('h','VDDH'),('l','VDDL'),('i','input')):
        for st in ('lo','hi'):
            v=[(IQ(r,s,st),r) for r in rows if IQ(r,s,st) is not None]
            if not v: continue
            lo=min(v,key=lambda t:t[0]); hi=max(v,key=lambda t:t[0])
            tt=[x for x in v if x[1]['corner']=='tt' and x[1]['T']==27 and x[1]['vddl']==1.2][0][0]
            print(f'  {name:5s} input {st}: tt/27/nom {tt:9.2e} | {lo[0]:9.2e} [{row(lo[1])}] .. {hi[0]:9.2e} [{row(hi[1])}]')
def pvt_table(tb):
    rows=load(tb,'pvt'); print(f'--- {tb}: charge / peak current over PVT, TR 100 ps, CL 20 fF (fC / uA); min .. max [worst corner]')
    for name,fn in (('Qh_r',lambda r:Q(r,'h','r')),('Qh_f',lambda r:Q(r,'h','f')),('Ql_r',lambda r:Q(r,'l','r')),('Ql_f',lambda r:Q(r,'l','f')),
                    ('Qin_r',lambda r:Q(r,'i','r')),('Qin_f',lambda r:Q(r,'i','f')),
                    ('pk_h_r',lambda r:IP(r,'h','r')[0]),('pk_h_f',lambda r:IP(r,'h','f')[0]),('pk_l_r',lambda r:IP(r,'l','r')[0]),('pk_l_f',lambda r:IP(r,'l','f')[0]),
                    ('pk_in_r',lambda r:IP(r,'i','r')[0]),('pk_in_f',lambda r:IP(r,'i','f')[0])):
        v=[(fn(r),r) for r in rows if fn(r) is not None]
        if not v or max(abs(x[0]) for x in v)<1e-3: continue
        lo=min(v,key=lambda t:t[0]); hi=max(v,key=lambda t:t[0])
        tt=[x for x in v if x[1]['corner']=='tt' and x[1]['T']==27 and x[1]['vddl']==1.2][0][0]
        print(f'  {name:8s} tt/27/nom {tt:8.3g} | {lo[0]:8.3g} [{row(lo[1])}] .. {hi[0]:8.3g} [{row(hi[1])}]')
def gmin_table(tb):
    rows=load(tb,'gmin'); print(f'--- {tb}: quiescent current vs simulator gmin (tt, nominal supplies), A delivered')
    for r in rows: print('  T=%3d gmin=%g | iq_h lo/hi %9s %9s | iq_l lo/hi %9s %9s | iq_in lo/hi %9s %9s'%(r['T'],r['gmin'],
        f(IQ(r,'h','lo'),'%.2e'),f(IQ(r,'h','hi'),'%.2e'),f(IQ(r,'l','lo'),'%.2e'),f(IQ(r,'l','hi'),'%.2e'),f(IQ(r,'i','lo'),'%.2e'),f(IQ(r,'i','hi'),'%.2e')))
if __name__=='__main__':
    for tb in (sys.argv[1:] or ['tb_ls_up','tb_ls_dn']):
        gmin_table(tb); print(); iq_table(tb); print(); tr_table(tb); print(); cl_table(tb); print(); pvt_table(tb); print('\n')
