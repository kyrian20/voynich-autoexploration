"""Exploratory lag screen, reusing frozen V2 predictors."""
import sys,json,hashlib,subprocess
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'research/analysis/2026-10-22-residual-order'
sys.path.insert(0,str(BASE))
import residual_order_calibrated as v2

def chains(rows,d):
 return [{**r,'tokens':r['tokens'][offset::d]} for r in rows for offset in range(d) if r['tokens'][offset::d]]

def verify():
 for n in range(20):
  t=list(map(str,range(n)))
  for d in range(1,6):
   rows=chains([{'tokens':t,'group':'g'}],d)
   actual=Counter((a,b) for r in rows for a,b in zip(r['tokens'],r['tokens'][1:]))
   assert actual==Counter(zip(t,t[d:]))
verify()
original_shuffle=v2.shuffled
original_score=v2.score
original_model=v2.Calibrated
class LagModel(original_model):
 def __init__(self,train,development,cap=None):
  super().__init__(chains(train,DISTANCE),chains(development,DISTANCE),cap)
# audit() keeps original rows; transformation is applied exactly once at model/score boundaries.
v2.Calibrated=LagModel
v2.score=lambda model,rows: original_score(model,chains(rows,DISTANCE))
data=json.loads((BASE/'inputs.json').read_text())
results=[]
for DISTANCE in (2,3):
 for source in data['sources']:
  result=v2.audit(source,2000)
  result['distance']=DISTANCE
  results.append(result)
  print(source['label'],DISTANCE,result['real']['identity_gain_over_edges_length'],file=sys.stderr,flush=True)
paths=[BASE/'inputs.json',BASE/'residual_order.py',BASE/'residual_order_calibrated.py',Path(__file__),Path(__file__).with_name('PROTOCOL.md')]
print(json.dumps({'status':'EXPLORATORY_NOT_CONFIRMATORY','base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'pair_construction_checks':100,'python':sys.version,'results':results},indent=2))
