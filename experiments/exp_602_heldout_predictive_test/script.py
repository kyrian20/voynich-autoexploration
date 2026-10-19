import collections, hashlib, json, math, random, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CORPUS=ROOT/"data/transcriptions/eva_zl3b.txt"
SEED=60220261019
TARGETS=("daiin","dain","saiin")
def clean(s):
 s=re.sub(r"<!.*?>|<[^>]*>"," ",s)
 s=re.sub(r"\[([^:\]]+):[^\]]*\]",r"\1",s)
 s=re.sub(r"\{[^}]*\}|@\d+;?"," ",s)
 return [w.lower() for w in re.split(r"[.\s,]+",s) if re.fullmatch(r"[A-Za-z]+",w)]
def parse():
 rows=[]; folio="unknown"; dialect="unknown"
 for line in CORPUS.read_text(encoding="latin-1").splitlines():
  s=line.strip()
  if not s or s.startswith("#"): continue
  if re.match(r"^<f\w+>.*\$",s):
   m=re.match(r"^<(f\w+)>",s)
   if m: folio=m.group(1)
   m=re.search(r"\$L=([AB])",s); dialect=m.group(1) if m else "unknown"; continue
  m=re.match(r"^<([^>]+)>\s+(.*)$",s)
  if not m or "," not in m.group(1): continue
  slot=m.group(1).split(",",1)[1]
  if re.sub(r"^[+*@=~&!/]+","",slot)!="P0" or dialect!="B": continue
  words=clean(m.group(2))
  if len(words)<2: continue
  test=int(hashlib.sha256(("voynich-exp602:"+folio).encode()).hexdigest()[:8],16)%5==0
  rows.append((folio,words,test))
 return rows
def ll(y,p):
 p=min(max(p,1e-6),1-1e-6)
 return -(y*math.log(p)+(1-y)*math.log(1-p))
def main():
 rows=parse(); train=[r for r in rows if not r[2]]; test=[r for r in rows if r[2]]
 if len(train)<1000 or len(test)<100: raise SystemExit("Train/test split unexpectedly small")
 results={}
 for ix,t in enumerate(TARGETS):
  p=sum(w[0]==t for _,w,_ in train)/len(train)
  ds=[]; sm=si=bm=bi=0.; hits=0
  for f,w,_ in test:
   y=int(w[0]==t); q=w.count(t)/len(w); hits+=y
   a=ll(y,p); b=ll(y,q); sm+=a;si+=b;bm+=(y-p)**2;bi+=(y-q)**2
   ds.append((f,b-a))
  groups=collections.defaultdict(list)
  for f,d in ds:groups[f].append(d)
  fs=sorted(groups); rng=random.Random(SEED+ix); boot=[]
  for _ in range(10000):
   vals=[]
   for _ in fs: vals.extend(groups[fs[rng.randrange(len(fs))]])
   boot.append(sum(vals)/len(vals))
  boot.sort()
  results[t]={"test_lines":len(test),"test_folios":len(fs),"test_initial_hits":hits,"train_initial_probability":p,
   "mean_log_loss_model":sm/len(test),"mean_log_loss_inventory_baseline":si/len(test),"log_loss_gain":(si-sm)/len(test),
   "mean_brier_model":bm/len(test),"mean_brier_inventory_baseline":bi/len(test),"brier_gain":(bi-bm)/len(test),
   "folio_cluster_bootstrap_95_ci_gain":[boot[int(.025*(len(boot)-1))],boot[int(.975*(len(boot)-1))]],
   "bootstrap_probability_gain_positive":sum(v>0 for v in boot)/len(boot)}
 h=hashlib.sha256(CORPUS.read_bytes()).hexdigest()
 out={"experiment":"exp_602_heldout_predictive_test","protocol_version":1,"source_sha256":h,
  "source_bytes":CORPUS.stat().st_size,"split":"test iff first 8 hex digits of SHA256('voynich-exp602:'+folio), as integer, modulo 5 == 0; folios never split",
  "train_lines":len(train),"test_lines":len(test),"train_folios":len(set(f for f,_,z in rows if not z)),
  "test_folios":len(set(f for f,_,z in rows if z)),"population":"Currier B, exact P0, >=2 cleaned tokens",
  "model":"train-only global probability of target at line start",
  "baseline":"target token count / line length on each test line; conditional uniform-position null, not deployable prediction",
  "primary_target":"daiin","predeclared_controls":["dain","saiin"],"results":results,
  "decision_rule":"Primary predictive improvement is demonstrated only if daiin log-loss gain is positive and its folio-cluster 95% interval is wholly above zero.",
  "limitations":["Positional test only; no semantic inference.","Inventory baseline uses held-out line inventory intentionally.","ZL3a/ZL3b are related transcriptions, not independent samples."]}
 dest=ROOT/"experiments/exp_602_heldout_predictive_test/results.json";dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"output":str(dest.relative_to(ROOT)),"train_lines":len(train),"test_lines":len(test),"results":results},indent=2))
if __name__=="__main__":main()
