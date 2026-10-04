import json,run
out=[]
for n in ['hvinv_dn','sar_h2l']:
  for c in ('tt','ss','ff','sf','fs'):
    for T in (-40,27,125):
      for vl,vh in ((1.08,3.6),(1.2,3.3),(1.32,3.0)):
        r,_=run.run(run.netlist_dn(n,c,T,vl,vh),n)
        out.append(dict(name=n,corner=c,T=T,vl=vl,vh=vh,**{k:v for k,v in r.items() if not k.startswith('_')}))
  print(n,'done',flush=True)
json.dump(out,open('dn_results.json','w')); print('ALLDONE')
