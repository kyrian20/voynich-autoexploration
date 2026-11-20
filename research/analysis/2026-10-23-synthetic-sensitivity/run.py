"""Synthetic diagnostic. No Voynich tokens enter generated sequences."""
from pathlib import Path
import sys,json,random,hashlib,math
ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'research/analysis/2026-10-22-residual-order'
sys.path.insert(0,str(BASE))
from residual_order_calibrated import Calibrated,bucket
from residual_order import score,cluster_bootstrap,shuffled

def chains(rows,d):
 return [{**r,'tokens':r['tokens'][j::d]} for r in rows for j in range(d) if r['tokens'][j::d]]

def generate(template,v,d,p,seed,exposed):
 rng=random.Random(seed);out=[]
 def encode(i):return (chr(0x400+i) if exposed else 'a')+f'{i:03d}z'
 assert len({encode(i) for i in range(v)})==v
 for row in template:
  indices=[]
  for i in range(len(row['tokens'])):
   index=indices[i-d] if i>=d and rng.random()<p else rng.randrange(v)
   indices.append(index)
  tokens=[encode(i) for i in indices]
  assert [int(t[1:4]) for t in tokens]==indices
  out.append({'id':row['id'],'group':row['group'],'tokens':tokens})
 assert [(r['group'],len(r['tokens'])) for r in out]==[(r['group'],len(r['tokens'])) for r in template]
 return out

def analyze(rows,d):
 train=[r for r in rows if bucket(r['group'])>=2];dev=[r for r in rows if bucket(r['group'])==1];test=[r for r in rows if bucket(r['group'])==0]
 sets=[set(r['group'] for r in a) for a in (train,dev,test)]
 assert not(sets[0]&sets[1] or sets[0]&sets[2] or sets[1]&sets[2])
 model=Calibrated(chains(train,d),chains(dev,d),2000)
 cm=Calibrated(chains(shuffled(train,2026102304),d),chains(dev,d),2000)
 assert model.vocab==cm.vocab
 for a in list(sorted(model.vocab))[:2]:
  probs=[model.probabilities(a,b) for b in model.events]
  assert all(abs(sum(x[k] for x in probs)-1)<1e-9 for k in range(4))
 real=score(model,chains(test,d));control=score(cm,chains(test,d))
 return {'weights':model.weights,'real':real,'bootstrap':cluster_bootstrap(real['groups']),'shuffled_training':control,'control_weights':cm.weights,'groups':[sorted(x) for x in sets]}

def main():
 template=json.loads((BASE/'inputs.json').read_text())['sources'][0]['records'];results=[]
 for v in (32,256):
  for d in (2,3):
   for p in (0,.25,.75):
    for seed in (2026102301,2026102302,2026102303):
     original=generate(template,v,d,p,seed,False)
     for exposed in ((False,True) if p==.75 else (False,)):
      rows=generate(template,v,d,p,seed,exposed)
      assert [[t[1:] for t in r['tokens']] for r in rows]==[[t[1:] for t in r['tokens']] for r in original]
      result={'vocabulary':v,'distance':d,'copy_probability':p,'seed':seed,'edges_expose_identity':exposed,**analyze(rows,d)}
      results.append(result)
      print(v,d,p,seed,exposed,result['real']['identity_gain_over_edges_length'],file=sys.stderr,flush=True)
 paths=[BASE/'inputs.json',BASE/'residual_order.py',BASE/'residual_order_calibrated.py',Path(__file__),Path(__file__).with_name('PROTOCOL.md')]
 print(json.dumps({'status':'EXPLORATORY_SYNTHETIC_DIAGNOSTIC','python':sys.version,'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'results':results},indent=2))
if __name__=='__main__':main()
