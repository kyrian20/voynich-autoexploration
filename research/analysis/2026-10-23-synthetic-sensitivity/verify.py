"""Check extraction and explain redundant-context shrinkage."""
from collections import Counter
import json
from pathlib import Path
from run import chains,generate,Calibrated,bucket,BASE
checks=0
for n in range(20):
 for d in range(1,6):
  t=list(map(str,range(n)));rows=chains([{'tokens':t,'group':'g'}],d)
  assert Counter((a,b) for r in rows for a,b in zip(r['tokens'],r['tokens'][1:]))==Counter(zip(t,t[d:]))
  checks+=1
template=json.loads((BASE/'inputs.json').read_text())['sources'][0]['records']
rows=generate(template,256,3,.75,2026102303,True)
tr=chains([r for r in rows if bucket(r['group'])>=2],3);dv=chains([r for r in rows if bucket(r['group'])==1],3)
m=Calibrated(tr,dv,2000)
for a in m.vocab:
 keys=m.contexts(a)
 assert m.tables[0][keys[0]]==m.tables[1][keys[1]]==m.tables[2][keys[2]]
 assert m.totals[0][keys[0]]==m.totals[1][keys[1]]==m.totals[2][keys[2]]
# Equal context partitions do not imply equal fitted probabilities:
# each layer mixes the same empirical distribution with its current parent.
a=sorted(m.vocab)[0];b=a
probs=m.probabilities(a,b)
assert probs[2]!=probs[3]
print(json.dumps({'pair_checks':checks,'redundant_contexts_checked':len(m.vocab),'weights':m.weights,'example_probabilities':probs,'explanation':'Identical sufficient counts, different hierarchical shrinkage; tiny W-EL need not represent additional contextual information.'},indent=2))
