#!/usr/bin/env python3
"""Exploratory repair with development-only layer shrinkage; V1 preserved."""
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys
from residual_order import Model,TAU,ALPHA,shuffled,score,cluster_bootstrap
GRID=(0,.01,.025,.05,.1,.25,.5,1)

def bucket(group):return int(hashlib.sha256(group.encode()).hexdigest()[:8],16)%5

class Calibrated(Model):
 def __init__(self,train,development,cap=None):
  if {r['group'] for r in train}&{r['group'] for r in development}:raise ValueError('Development leakage')
  super().__init__(train,cap);self.weights=[0.0]*3;self.calibration=[]
  pairs=Counter((a,b) for row in development for a,b in zip(row['tokens'],row['tokens'][1:]))
  if not pairs:raise ValueError('No development transitions')
  n=sum(pairs.values())
  for layer in range(3):
   prepared=[]
   for (a,b),count in pairs.items():
    parent=self.probabilities(a,b)[layer]
    key=self.contexts(a)[layer];target=self.map(b)
    raw=(self.tables[layer].get(key,{}).get(target,0)+TAU*parent)/(self.totals[layer][key]+TAU)
    prepared.append((parent,raw,count))
   candidates=[{'weight':weight,'development_bits':-sum(count*math.log2((1-weight)*parent+weight*raw) for parent,raw,count in prepared)/n} for weight in GRID]
   best=min(candidates,key=lambda r:(r['development_bits'],r['weight']))
   self.weights[layer]=best['weight'];self.calibration.append(candidates)
 def probabilities(self,a,b):
  target=self.map(b);p=(self.uni[target]+ALPHA)/(self.n+ALPHA*len(self.events));out=[p]
  for layer,(table,total,key) in enumerate(zip(self.tables,self.totals,self.contexts(a))):
   raw=(table.get(key,{}).get(target,0)+TAU*p)/(total[key]+TAU)
   weight=self.weights[layer];p=(1-weight)*p+weight*raw;out.append(p)
  return out


def audit(source,cap):
 rows=source['records'];train=[r for r in rows if bucket(r['group'])>=2];dev=[r for r in rows if bucket(r['group'])==1];test=[r for r in rows if bucket(r['group'])==0]
 sets=[{r['group'] for r in part} for part in (train,dev,test)]
 if any(sets[i]&sets[j] for i,j in ((0,1),(0,2),(1,2))):raise ValueError('Partition overlap')
 m=Calibrated(train,dev,cap);real=score(m,test);controls=[]
 for i in range(16):
  seed=int(hashlib.sha256(f'PRIVATE_RESIDUAL_V1:{i}'.encode()).hexdigest()[:16],16)
  cm=Calibrated(shuffled(train,seed),dev,cap)
  if cm.vocab!=m.vocab:raise ValueError('Vocabulary drift under shuffle')
  result=score(cm,test)
  controls.append({'seed':seed,'weights':cm.weights,'identity_gain_over_edges_length':result['identity_gain_over_edges_length'],'loss_bits_per_transition':result['loss_bits_per_transition']})
 gains=[c['identity_gain_over_edges_length'] for c in controls]
 return {'label':source['label'],'kind':source['kind'],'vocabulary_cap':cap,'weights_E_EL_W':m.weights,
  'calibration_grid_scores':m.calibration,'train_groups':sorted(sets[0]),'development_groups':sorted(sets[1]),'test_groups':sorted(sets[2]),
  'train_records':len(train),'development_records':len(dev),'test_records':len(test),'training_transitions':m.n,'vocabulary_plus_UNK':len(m.events),
  'real':real,'bootstrap':cluster_bootstrap(real['groups']),
  'shuffled_training_controls':controls,'control_gain_mean':sum(gains)/len(gains),'control_gain_range':[min(gains),max(gains)],
  'real_minus_control_mean':real['identity_gain_over_edges_length']-sum(gains)/len(gains)}


def main():
 root=Path(__file__).resolve().parent;data=json.loads((root/'inputs.json').read_text())
 paths=['PROTOCOL_V2.md','residual_order_calibrated.py','residual_order.py','inputs.json']
 print(json.dumps({'status':'EXPLORATORY_REPAIR_NOT_NEW_CONFIRMATION','source_commit':data['source_commit'],
  'parameter_grid':GRID,'tau':TAU,'alpha':ALPHA,'sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths},
  'results':[audit(s,cap) for s in data['sources'] for cap in (None,2000)],'python':sys.version},indent=2))
if __name__=='__main__':main()
