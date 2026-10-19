#!/usr/bin/env python3
"""exp609: paired per-folio test of vowels following EVA ch vs sh."""
import hashlib, json, math, random, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b","data/transcriptions/eva_zl3b.txt"),("IT2a","data/transcriptions/eva_it2a.txt")]
ROW_RE=re.compile(r"^<(f\d+[rv])\.\d+,[^>]*>\s*(.*)$")
TOKEN_RE=re.compile(r"[a-z]{2,}")
VOWELS=set("aeiouy")
SEED=6092026
BOOT=20000
PERM=20000

def load(label,rel):
 p=ROOT/rel
 d=defaultdict(lambda: {g:Counter() for g in ("ch","sh")})
 for raw in p.read_text(encoding="latin-1").splitlines():
  m=ROW_RE.match(raw.strip())
  if not m: continue
  folio,body=m.groups()
  body=re.sub(r"<[^>]*>|\{[^}]*\}|\[[^]]*\]|\$[^ ]*|@\d+;?"," ",body.lower())
  for word in TOKEN_RE.findall(body):
   for g in ("ch","sh"):
    start=0
    while True:
     i=word.find(g,start)
     if i<0: break
     j=i+2
     if j<len(word):
      nxt=word[j]
      d[folio][g]["n"]+=1
      d[folio][g]["vowel"]+=int(nxt in VOWELS)
      d[folio][g]["e"]+=int(nxt=="e")
      d[folio][g]["a"]+=int(nxt=="a")
     start=i+1
 rows=[]
 for f,x in sorted(d.items()):
  if x["ch"]["n"] and x["sh"]["n"]:
   rows.append({"folio":f,"ch_n":x["ch"]["n"],"sh_n":x["sh"]["n"],
    "ch_vowel":x["ch"]["vowel"]/x["ch"]["n"],"sh_vowel":x["sh"]["vowel"]/x["sh"]["n"],
    "ch_e":x["ch"]["e"]/x["ch"]["n"],"sh_e":x["sh"]["e"]/x["sh"]["n"],
    "ch_a":x["ch"]["a"]/x["ch"]["n"],"sh_a":x["sh"]["a"]/x["sh"]["n"]})
 allc={g:Counter() for g in ("ch","sh")}
 for x in d.values():
  for g in ("ch","sh"): allc[g].update(x[g])
 return {"label":label,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"rows":rows,
  "totals":{g:dict(allc[g]) for g in ("ch","sh")}}

def mean(xs): return sum(xs)/len(xs) if xs else None
def analyze(ds):
 rows=ds["rows"]
 diffs=[r["ch_vowel"]-r["sh_vowel"] for r in rows]
 corr=None
 if len(rows)>2:
  a=[r["ch_vowel"] for r in rows]; b=[r["sh_vowel"] for r in rows]
  ma,mb=mean(a),mean(b)
  den=math.sqrt(sum((x-ma)**2 for x in a)*sum((x-mb)**2 for x in b))
  corr=sum((x-ma)*(y-mb) for x,y in zip(a,b))/den if den else None
 rng=random.Random(SEED)
 boots=[]
 for _ in range(BOOT):
  boots.append(mean([diffs[rng.randrange(len(diffs))] for _ in diffs]))
 lo,hi=sorted(boots)[int(.025*BOOT)],sorted(boots)[int(.975*BOOT)]
 obs=abs(mean(diffs)); extreme=0
 for _ in range(PERM):
  v=[x*(1 if rng.random()<.5 else -1) for x in diffs]
  if abs(mean(v))>=obs: extreme+=1
 return {"folios_paired":len(rows),"mean_folio_ch_vowel_rate":mean([r["ch_vowel"] for r in rows]),
  "mean_folio_sh_vowel_rate":mean([r["sh_vowel"] for r in rows]),"mean_paired_difference_ch_minus_sh":mean(diffs),
  "bootstrap_folio_resample_95pct_ci":[lo,hi],"paired_sign_flip_permutation_p_two_sided":(extreme+1)/(PERM+1),
  "pearson_correlation_folio_ch_sh_vowel_rates":corr,
  "warning":"Unweighted folio-level descriptive analysis; not Parisel's template-conditioned model. Shared template/section effects and transcription dependence remain."}

def main():
 out={"experiment":"exp_609_paired_ch_sh_vowel_test","question":"Do per-folio vowel rates after ch and sh differ, and do they co-vary, in the two available EVA transcriptions?",
 "method":{"vowels":sorted(VOWELS),"count":"within-word ch/sh occurrences with a following character","paired":"only folios with at least one context for both digraphs","bootstrap_replicates":BOOT,"sign_flip_permutations":PERM,"seed":SEED,"unit":"folio","transcription_caveat":"ZL3b and IT2a are related transcriptions, not independent manuscript witnesses."},"datasets":[]}
 for label,rel in FILES:
  d=load(label,rel); stats=analyze(d); d.pop("rows")
  d["summary"]=stats; out["datasets"].append(d)
 dest=ROOT/"experiments/exp_609_paired_ch_sh_vowel_test"; dest.mkdir(parents=True,exist_ok=True)
 (dest/"results.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 lines=["# exp609 — Paired per-folio ch/sh vowel test","","## Question","Do folio-level vowel rates after ch and sh differ, and do they co-vary?","","## Method and caveats","- Count the next character after each within-word ch/sh occurrence, if one exists; vowels are a/e/i/o/u/y.","- Compare folio-level rates only for folios with both contexts; bootstrap folios and perform a paired sign-flip test on ch-minus-sh vowel-rate differences.","- This is not a reproduction of Parisel's template-conditioned Beta-Binomial mixture. Equal folio weighting, tokenization, word-template composition and section effects limit interpretation."]
 for d in out["datasets"]:
  s=d["summary"]
  lines += ["",f"## {d['label']}",f"- Source SHA-256: {d['sha256']}",f"- Overall raw counts: {json.dumps(d['totals'],sort_keys=True)}",
  f"- Folios paired: {s['folios_paired']}",f"- Mean folio vowel rate after ch: {s['mean_folio_ch_vowel_rate']:.5f}; after sh: {s['mean_folio_sh_vowel_rate']:.5f}",
  f"- Mean paired difference (ch−sh): {s['mean_paired_difference_ch_minus_sh']:.5f}; folio bootstrap 95% CI {s['bootstrap_folio_resample_95pct_ci']}",
  f"- Paired sign-flip two-sided p: {s['paired_sign_flip_permutation_p_two_sided']:.5f}",
  f"- Correlation of folio rates (ch, sh): {s['pearson_correlation_folio_ch_sh_vowel_rates']:.4f}"]
 lines += ["","## Interpretation","A difference or correlation is descriptive, not proof of a discrete folio switch or a decipherment. Proper replication requires the paper's exact template-conditioned extraction and held-out comparison against composition-matched controls."]
 (dest/"result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 print(json.dumps(out,indent=2))
if __name__=="__main__": main()
