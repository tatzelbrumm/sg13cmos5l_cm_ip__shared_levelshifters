import json,run,numpy as np
out=[]
cases=[('tt',27,3.3),('ss',27,3.6),('sf',27,3.6)]
vls=[round(x,3) for x in np.arange(0.60,1.33,0.04)]
for n in ['sar_l2h','bidir_up','harness_ls','lpopamp_st','hsxo_xd']:
    for (c,T,vh) in cases:
        for vl in vls+([1.5,1.8,2.0] if n=='hsxo_xd' else []):
            r,_=run.run(run.netlist_up(n,c,T,vl,vh),n)
            ok = r.get('tplh') is not None and r.get('tphl') is not None and r.get('voh',0)>0.95*vh and r.get('vol',9)<0.05*vh
            out.append(dict(name=n,corner=c,T=T,vh=vh,vl=vl,ok=bool(ok),**{k:v for k,v in r.items() if not k.startswith('_')}))
        print(n,c,'done',flush=True)
json.dump(out,open('vmin_results.json','w'))
print('ALLDONE')
