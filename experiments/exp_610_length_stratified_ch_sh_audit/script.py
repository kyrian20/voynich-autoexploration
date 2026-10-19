#!/usr/bin/env python3
"""exp610: length-stratified ch/sh following-vowel audit."""
import hashlib,json,re,random,math
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b","data/transcriptions/eva_zl3b.txt"),("IT2a","data/transcriptions/eva_it2a.txt")]
ROW=re.compile(r"^<(f\d+[rv])\.\d+,[^>]*>\s*(.*)$")
TOK=re.compile(r"[a-z]{2,}")
V=set("aeiouy"); SEED=6102026; B=20000; P=20000
def binlen(n): return "2-4" if n<=4 else ("5-7" if n<=7 else "8+")
def load(label,rel):
 p=ROOT/rel; agg=defaultdict(lambda:defaultdict(lambda:defaultdict(Counter)))
 for line in p.read_text(encoding="latin-1").splitlines():
  m=ROW.match(line.strip())
  if not m: continue
  folio,body=m.groups()
  body=re.sub(r"<[^>]*>|\{[^}]*\}|\[[^]]*\]|\$[^ ]*|@\d+;?"," ",body.lower())
  for word in TOK.findall(body):
   lb=binlen(len(word))
   for g in ("ch","sh"):
    i=0
    while True:
     i=word.find(g,i)
     if i<0: break
     if i+2<len(word):
      nxt=word[i+2]; c=agg[folio][lb][g]
      c["n"]+=1;c["v"]+=int(nxt in V);c["e"]+=int(nxt=="e")
     i+=1
 rows=[]
 for f,bins in agg.items():
  row={"folio":f}
  for lb in ("2-4","5-7","8+"):
   for g in ("ch","sh"):
    c=bins[lb][g];row[f"{lb}_{g}_n"]=c["n"];row[f"{lb}_{g}_v"]=c["v"]
  rows.append(row)
 return {"label":label,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"rows":rows}
def stats(ds):
 # aggregate by length bin, compare rates and counts; paired folio difference only within bins with >=1 each
 out={}
 for lb in ("2-4","5-7","8+"):
  counts={g:Counter() for g in ("ch","sh")}
  diffs=[]
  for r in ds["rows"]:
   for g in ("ch","sh"):
    counts[g]["n"]+=r[f"{lb}_{g}_n"];counts[g]["v"]+=r[f"{lb}_{g}_v"]
   if r[f"{lb}_ch_n"] and r[f"{lb}_sh_n"]:
    diffs.append(r[f"{lb}_ch_v"]/r[f"{lb}_ch_n"]-r[f"{lb}_sh_v"]/r[f"{lb}_sh_n"])
  out[lb]={"ch_n":counts["ch"]["n"],"ch_vowel_rate":counts["ch"]["v"]/counts["ch"]["n"] if counts["ch"]["n"] else None,
   "sh_n":counts["sh"]["n"],"sh_vowel_rate":counts["sh"]["v"]/counts["sh"]["n"] if counts["sh"]["n"] else None,
   "paired_folios":len(diffs),"mean_paired_difference":sum(diffs)/len(diffs) if diffs else None}
 return out
def main():
 res={"experiment":"exp_610_length_stratified_ch_sh_audit","method":{"length_bins":"2-4, 5-7, 8+ EVA letters","outcome":"vowel among next characters after ch/sh inside a token","limitations":"Descriptive stratification only; no template-conditioned model, no Currier/hand adjustment, and transcriptions are related."},"datasets":[]}
 for label,rel in FILES:
  d=load(label,rel);d["summary_by_length"]=stats(d);d.pop("rows");res["datasets"].append(d)
 dest=ROOT/"experiments/exp_610_length_stratified_ch_sh_audit";dest.mkdir(parents=True,exist_ok=True)
 (dest/"results.json").write_text(json.dumps(res,indent=2)+"\n",encoding="utf-8")
 lines=["# exp610 — Length-stratified ch/sh audit","","## Method","Tokens grouped by EVA token length (2–4, 5–7, 8+). For each length band, report pooled next-vowel rates and mean paired folio difference only for folios with both ch and sh contexts. This is a composition check, not a replication of Parisel's template-conditioned model."]
 for d in res["datasets"]:
  lines+=["",f"## {d['label']}",f"- Source SHA-256: {d['sha256']}"]
  for lb,s in d["summary_by_length"].items():
   lines += [f"- **{lb} letters**: ch n={s['ch_n']}, vowel rate={s['ch_vowel_rate']}; sh n={s['sh_n']}, vowel rate={s['sh_vowel_rate']}; paired folios={s['paired_folios']}, mean within-folio difference={s['mean_paired_difference']}"]
 lines += ["","## Interpretation","If the ch/sh contrast shrinks within length bands, overall word-length composition may explain part of it. Persistence is still not enough: template identity, section, hand and exact paper rules must be controlled before claiming replication."]
 (dest/"result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 print(json.dumps(res,indent=2))
if __name__=="__main__":main()
