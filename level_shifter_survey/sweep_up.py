import json,run,os
os.makedirs('tmp',exist_ok=True)
res=run.sweep(['sar_l2h','bidir_up','harness_ls','lpopamp_st'])
json.dump(res,open('up_results.json','w'))
print('done',len(res))
