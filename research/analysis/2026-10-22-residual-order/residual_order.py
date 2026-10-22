#!/usr/bin/env python3
"""Frozen exploratory comparison of normalized hierarchical predictors."""
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path
import random
import sys
TAU=20.0
ALPHA=.1
BOOTSTRAPS=2000
BOOT_SEED=2026102203
UNK='<UNK>'
NAMES=('U','E','EL','W')


def is_test(group):
 return int(hashlib.sha256(group.encode()).hexdigest()[:8],16)%5==0


def shuffled(rows,seed):
 rng=random.Random(seed);out=[]
 for row in rows:
  words=list(row['tokens']);rng.shuffle(words);out.append({**row,'tokens':words})
 return out


class Model:
 def __init__(self,rows,cap=None):
  vocabulary=Counter(w for r in rows for w in r['tokens'])
  if UNK in vocabulary:raise ValueError('Reserved token in input')
  ordered=sorted(vocabulary,key=lambda w:(-vocabulary[w],w))
  self.vocab=set(ordered if cap is None else ordered[:cap]);self.events=sorted(self.vocab)+[UNK]
  self.uni=Counter();self.tables=[defaultdict(Counter) for _ in range(3)];self.totals=[Counter() for _ in range(3)]
  self.n=0
  for row in rows:
   for a,b in zip(row['tokens'],row['tokens'][1:]):
    target=self.map(b);self.uni[target]+=1;self.n+=1
    for table,total,key in zip(self.tables,self.totals,self.contexts(a)):
     table[key][target]+=1;total[key]+=1
  if not self.n:raise ValueError('No training transitions')
 def map(self,w):return w if w in self.vocab else UNK
 def contexts(self,a):
  edge=(a[0],a[-1]);el=(edge,len(a))
  # UNK previous identities pool only within the same edge/length stratum.
  return edge,el,(self.map(a),el)
 def probabilities(self,a,b):
  target=self.map(b)
  p=(self.uni[target]+ALPHA)/(self.n+ALPHA*len(self.events));out=[p]
  for table,total,key in zip(self.tables,self.totals,self.contexts(a)):
   p=(table.get(key,{}).get(target,0)+TAU*p)/(total[key]+TAU);out.append(p)
  return out


def score(model,rows):
 groups={};unknown=0
 for row in rows:
  state=groups.setdefault(row['group'],{'n':0,'losses':[0.0]*4})
  for a,b in zip(row['tokens'],row['tokens'][1:]):
   probabilities=model.probabilities(a,b)
   if any(not (0<p<=1) for p in probabilities):raise ValueError('Invalid probability')
   for i,p in enumerate(probabilities):state['losses'][i]-=math.log2(p)
   state['n']+=1;unknown+=b not in model.vocab
 n=sum(r['n'] for r in groups.values())
 if not n:raise ValueError('No evaluation transitions')
 losses=[sum(r['losses'][i] for r in groups.values())/n for i in range(4)]
 return {'transitions':n,'unknown_targets':unknown,'unknown_rate':unknown/n,
  'loss_bits_per_transition':dict(zip(NAMES,losses)),
  'identity_gain_over_edges_length':losses[2]-losses[3],
  'identity_gain_over_unigram':losses[0]-losses[3],
  'groups':groups}


def quantile(values,q):
 values=sorted(values);x=(len(values)-1)*q;lo=int(x);hi=min(lo+1,len(values)-1)
 return values[lo]+(x-lo)*(values[hi]-values[lo])


def cluster_bootstrap(groups):
 values=list(groups.values());rng=random.Random(BOOT_SEED);gains=[]
 for _ in range(BOOTSTRAPS):
  sampled=[rng.choice(values) for _ in values]
  n=sum(g['n'] for g in sampled)
  gains.append(sum(g['losses'][2]-g['losses'][3] for g in sampled)/n)
 return {'resamples':BOOTSTRAPS,'seed':BOOT_SEED,'groups':len(values),
  'paired_group_percentile_95':[quantile(gains,.025),quantile(gains,.975)],
  'scope':'Exploratory group bootstrap, not a preregistered population confidence claim.'}


def audit(source,cap):
 rows=source['records'];train=[r for r in rows if not is_test(r['group'])];test=[r for r in rows if is_test(r['group'])]
 train_groups={r['group'] for r in train};test_groups={r['group'] for r in test}
 if train_groups & test_groups:raise ValueError('Group leakage')
 model=Model(train,cap);real=score(model,test);controls=[]
 for i in range(16):
  seed=int(hashlib.sha256(f'PRIVATE_RESIDUAL_V1:{i}'.encode()).hexdigest()[:16],16)
  control_model=Model(shuffled(train,seed),cap)
  if control_model.vocab!=model.vocab:raise ValueError('Vocabulary changed under count-preserving shuffle')
  result=score(control_model,test)
  controls.append({'seed':seed,'identity_gain_over_edges_length':result['identity_gain_over_edges_length'],
    'loss_bits_per_transition':result['loss_bits_per_transition']})
 gains=[r['identity_gain_over_edges_length'] for r in controls]
 train_lines={tuple(r['tokens']) for r in train}
 return {'label':source['label'],'kind':source['kind'],'vocabulary_cap':cap,'actual_vocabulary_plus_UNK':len(model.events),
  'train_groups':sorted(train_groups),'test_groups':sorted(test_groups),
  'train_records':len(train),'test_records':len(test),
  'train_transitions':model.n,'test_exact_lines_also_in_train':sum(tuple(r['tokens']) in train_lines for r in test),
  'real':real,'bootstrap':cluster_bootstrap(real['groups']),
  'shuffled_training_controls':controls,'control_gain_mean':sum(gains)/len(gains),
  'control_gain_range':[min(gains),max(gains)],
  'real_minus_control_mean':real['identity_gain_over_edges_length']-sum(gains)/len(gains)}


def main():
 root=Path(__file__).resolve().parent
 data=json.loads((root/'inputs.json').read_text())
 results=[audit(source,cap) for source in data['sources'] for cap in (None,2000)]
 paths=['PROTOCOL.md','prepare_inputs.py','residual_order.py','inputs.json']
 print(json.dumps({'status':'EXPLORATORY_NO_SEMANTIC_ASSIGNMENTS','parameters':{'tau':TAU,'alpha':ALPHA,'caps':[None,2000]},
  'source_commit':data['source_commit'],'sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths},
  'results':results,'python':sys.version,'limits':['Already explored manuscript, not new confirmatory folios.',
  'Paired group resampling does not remove section, hand or historical model-selection confounds.',
  'Reference controls differ in genre and sample size; compare model increments, not absolute losses.',
  'One preceding token only; no translations or universal exclusions.']},indent=2))
if __name__=='__main__':main()
