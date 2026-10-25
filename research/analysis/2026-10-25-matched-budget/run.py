"""Exploratory fixed-budget sensitivity of the archived V2 predictor."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

parser=argparse.ArgumentParser()
parser.add_argument('--model-dir',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
if args.output.exists(): raise SystemExit('Output already exists')
sys.path.insert(0,str(args.model_dir.resolve()))
from residual_order_calibrated import Calibrated,bucket,score

raw=(args.model_dir/'inputs.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()=='c069548868854c29d294efbc3da891a0f5cf7c62878786be78fa13ce5ba5225d'
data=json.loads(raw)
budgets=(10653,3761,3590)
seeds=range(2026102501,2026102506)

def partition(group):
    b=bucket(group)
    return 0 if b>=2 else 1 if b==1 else 2

def select(records,part,budget,seed):
    candidates=[(i,r) for i,r in enumerate(records) if partition(r['group'])==part and len(r['tokens'])>=2]
    candidates.sort(key=lambda x:hashlib.sha256(f'{seed}:{x[0]}'.encode()).digest())
    selected=[];manifest=[];remaining=budget
    for index,row in candidates:
        count=min(remaining,len(row['tokens'])-1)
        selected.append({**row,'tokens':row['tokens'][:count+1]})
        manifest.append([index,count])
        remaining-=count
        if not remaining:break
    assert remaining==0
    assert sum(len(r['tokens'])-1 for r in selected)==budget
    return selected,manifest

results=[]
for source in data['sources']:
    for seed in seeds:
        parts=[select(source['records'],p,n,seed) for p,n in enumerate(budgets)]
        groups=[{r['group'] for r in rows} for rows,_ in parts]
        assert all(not groups[a]&groups[b] for a,b in ((0,1),(0,2),(1,2)))
        model=Calibrated(parts[0][0],parts[1][0],2000)
        evaluation=score(model,parts[2][0])
        assert model.n==budgets[0] and evaluation['transitions']==budgets[2]
        results.append({'label':source['label'],'seed':seed,'weights':model.weights,
          'gain_bits':evaluation['identity_gain_over_edges_length'],'unknown_rate':evaluation['unknown_rate'],
          'loss_bits':evaluation['loss_bits_per_transition'],
          'groups':[sorted(g) for g in groups],
          'selection':[{ 'records':len(rows),'manifest':manifest,
            'sha256':hashlib.sha256(json.dumps(manifest,separators=(',',':')).encode()).hexdigest(),
            'truncated_records':sum(n<len(source['records'][i]['tokens'])-1 for i,n in manifest)} for rows,manifest in parts]})
        print(source['label'],seed,results[-1]['gain_bits'],flush=True)
out={'status':'EXPLORATORY_SIZE_SENSITIVITY_ONLY','budgets_train_dev_test':budgets,'cap':2000,
 'seeds':list(seeds),'input_sha256':hashlib.sha256(raw).hexdigest(),
 'code_sha256':{p:hashlib.sha256((args.model_dir/p).read_bytes()).hexdigest() for p in ('residual_order.py','residual_order_calibrated.py')},
 'diagnostic_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'protocol_sha256':hashlib.sha256(Path(__file__).with_name('PROTOCOL.md').read_bytes()).hexdigest(),
 'python':sys.version,'results':results}
args.output.write_text(json.dumps(out,indent=2)+'\n')
