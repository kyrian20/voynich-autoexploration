#!/usr/bin/env python3
"""Independent-transcription robustness test for Currier-B/P0 initial daiin."""
import collections, hashlib, json, random, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CORPUS=ROOT/"data/transcriptions/eva_it2a.txt"
SEED=60420261019
def clean(s):
 s=re.sub(r"<!.*?>|<[^>]*>"," ",s)
 s=re.sub(r"\[([^:\]]+):[^\]]*\]",r"\1",s)
 s=re.sub(r"\{[^}]*\}|@\d+;?"," ",s)
 return [w.lower() for w in re.split(r"[.\s,]+",s) if re.fullmatch(r"[A-Za-z]+",w)]
def parse():
 rows=[];folio="unknown";dialect="unknown"
 for n,line in enumerate(CORPUS.read_text(encoding="latin-1").splitlines(),1):
  s=line.strip()
  if not s or s.startswith("#"):continue
  if re.match(r"^<f\w+>.*\$",s):
   m=re.match(r"^<(f\w+)>",s)
   if m:folio=m.group(1)
   m=re.search(r"\$L=([AB])",s);dialect=m.group(1) if m else "unknown"
   continue
  m=re.match(r"^<([^>]+)>\s+(.*)$",s)
  if not m or "," not in m.group(1):continue
  slot=m.group(1).split(",",1)[1]
  if re.sub(r"^[+*@=~&!/]+","",slot)!="P0" or dialect!="B":continue
  words=clean(m.group(2))
  if len(words)<2:continue
  rows.append({"folio":folio,"line":n,"words":words,"observed":int(words[0]=="daiin"),"expected":words.count("daiin")/len(words)})
 return rows
def quantile(v,q):
 v=sorted(v);x=(len(v)-1)*q;lo=int(x);hi=min(lo+1,len(v)-1);w=x-lo
 return v[lo]*(1-w)+v[hi]*w
def main():
 rows=parse()
 if len(rows)<100:raise SystemExit(f"Too few eligible rows: {len(rows)}")
 by=collections.defaultdict(list)
 for r in rows:by[r["folio"]].append(r)
 folios=sorted(by);obs=sum(r["observed"] for r in rows);exp=sum(r["expected"] for r in rows)
 rng=random.Random(SEED);boot=[]
 for _ in range(20000):
  n=d=0
  for _ in folios:
   f=folios[rng.randrange(len(folios))];n+=sum(x["observed"] for x in by[f]);d+=sum(x["expected"] for x in by[f])
  if d:boot.append(n/d)
 ge=0;null=[]
 for _ in range(20000):
  n=sum(r["words"][rng.randrange(len(r["words"]))]=="daiin" for r in rows)
  null.append(n);ge+=n>=obs
 loo=[]
 for f in folios:
  n=obs-sum(x["observed"] for x in by[f]);d=exp-sum(x["expected"] for x in by[f])
  if d:loo.append(n/d)
 out={"experiment":"exp_604_independent_transcription_replication","source":{"path":"data/transcriptions/eva_it2a.txt","bytes":CORPUS.stat().st_size,"sha256":hashlib.sha256(CORPUS.read_bytes()).hexdigest()},
 "protocol":{"population":"Currier B, exact P0, >=2 cleaned tokens","target":"literal cleaned EVA daiin as first token","null":"one uniformly selected token position per eligible line, preserving line inventory","bootstrap_resamples":20000,"permutations":20000,"seed":SEED},
 "sample":{"eligible_lines":len(rows),"folios":len(folios),"observed_initial_daiin":obs,"inventory_expected":exp,"total_daiin_tokens":sum(r["words"].count("daiin") for r in rows)},
 "enrichment_ratio":obs/exp,"folio_cluster_bootstrap_95pct":[quantile(boot,.025),quantile(boot,.975)],
 "permutation":{"null_mean":sum(null)/len(null),"p_one_sided_plus_one":(ge+1)/(len(null)+1),"exceedances":ge},
 "leave_one_folio_out_ratio_range":[min(loo),max(loo)],"caveat":"IT2a is a different transcription/version, but may share editorial conventions and is not a wholly independent manuscript witness. Positional replication is not decipherment."}
 d=ROOT/"experiments/exp_604_independent_transcription_replication";d.mkdir(parents=True,exist_ok=True)
 (d/"results.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 report=("# exp_604 — Independent transcription replication\n\n"
 "Source: IT2a, SHA-256 "+out["source"]["sha256"]+". Population: Currier B, exact P0, at least two cleaned tokens; target is literal EVA daiin in first position.\n\n"
 f"- Eligible lines: {len(rows)} across {len(folios)} folios.\n- Initial hits: {obs}; line-inventory expectation: {exp:.4f}.\n"
 f"- Enrichment: {obs/exp:.4f}x; folio-cluster bootstrap 95% CI [{out['folio_cluster_bootstrap_95pct'][0]:.4f}, {out['folio_cluster_bootstrap_95pct'][1]:.4f}].\n"
 f"- Conditional position-permutation p (plus-one): {out['permutation']['p_one_sided_plus_one']:.6g} (20,000 permutations).\n"
 f"- Leave-one-folio-out range: {min(loo):.4f}x–{max(loo):.4f}x.\n\n"
 "## Interpretation\n\nThis tests whether the same narrowly defined positional pattern appears in IT2a. IT2a is a different transcription/version, but not a wholly independent manuscript witness; editorial conventions may be shared. Positive results support robustness to transcription version, not semantic interpretation or decipherment. A null result should be retained without retuning the population.\n")
 (d/"result.md").write_text(report,encoding="utf-8")
 print(json.dumps(out,indent=2))
if __name__=="__main__":main()
