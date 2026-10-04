import json,collections
R=json.load(open('up_results.json'))
by=collections.defaultdict(list)
for r in R: by[r['name']].append(r)
for n,rs in by.items():
    ok=[r for r in rs if r.get('tplh') is not None and r.get('tphl') is not None and r['voh']>0.95*r['vh'] and r['vol']<0.05*r['vh']]
    bad=[r for r in rs if r not in ok]
    print(f"== {n}: {len(ok)}/{len(rs)} PVT points functional")
    for b in bad[:6]: print('   FAIL',b['corner'],b['T'],b['vl'],b['vh'],b.get('voh'),b.get('vol'))
    if ok:
        print('   tplh ns',round(min(r['tplh'] for r in ok)*1e9,2),'-',round(max(r['tplh'] for r in ok)*1e9,2),' tphl',round(min(r['tphl'] for r in ok)*1e9,2),'-',round(max(r['tphl'] for r in ok)*1e9,2))
        for k in('ih_lo','ih_hi','il_lo','il_hi'):
            nom=[f"{abs(r[k]):.1e}" for r in ok if r['corner']=='tt' and r['T']==27 and r['vl']==1.2]
            print('   ',k,'max',f"{max(abs(r[k]) for r in ok):.1e}",'tt27 nominal',nom)
        w=max(ok,key=lambda r:max(r['tplh'],r['tphl'])); print('   slowest',w['corner'],w['T'],w['vl'],w['vh'],round(w['tplh']*1e9,2),round(w['tphl']*1e9,2))
