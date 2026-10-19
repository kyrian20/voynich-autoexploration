#!/usr/bin/env python3
"""exp611: exact word-length and relative-position stratification for ch/sh."""
import hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b","data/transcriptions/eva_zl3b.txt"),("IT2a","data/transcriptions/eva_it2a.txt")]
ROW=re.compile(r"^<(f\d+[rv])\.\d+,[^>]*>\s*(.*)$")
TOK=re.compile(r"[a-z]{2,}")
V=set("aeiouy")
def load(label,rel):
 p=ROOT/rel; by=defaultdict(lambda:defaultdict(Counter))
 for line in p.read_text(encoding="latin-1").splitlines():
  m=ROW.match(line.strip())
  if not m: continue
  folio,body=m.groups()
  body=re.sub(r"<[^>]*>|\{[^}]*\}|\[[^]]*\]|\$[^ ]*|@\d+;?"," ",body.lower())
  for w in TOK.findall(body):
   L=len(w)
   for g in ("ch","sh"):
    start=0
    while True:
     i=w.find(g,start)
     if i<0: break
     if i+2<L:
      key=(L,i); c=by[key][folio][g]; c["n"]+=1;c["v"]+=int(w[i+2] in V)
     start=i+1
 rows=[]
 for (L,i),folios in by.items():
  for folio,cs in folios.items():
   rows.append({"length":L,"position":i,"folio":folio,"ch_n":cs["ch"]["n"],"ch_v":cs["ch"]["v"],"sh_n":cs["sh"]["n"],"sh_v":cs["sh"]["v"]})
 return {"label":label,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"rows":rows}
def summarize(d):
 strata=defaultdict(list)
 for r in d["rows"]:
  if r["ch_n"] and r["sh_n"]: strata[(r["length"],r["position"])].append(r)
 result=[]; pooled=Counter(); diff_num=diff_den=0
 for (L,pos),rs in sorted(strata.items()):
  chn=sum(x["ch_n"] for x in rs); chv=sum(x["ch_v"] for x in rs)
  shn=sum(x["sh_n"] for x in rs); shv=sum(x["sh_v"] for x in rs)
  diffs=[x["ch_v"]/x["ch_n"]-x["sh_v"]/x["sh_n"] for x in rs]
  result.append({"length":L,"position":pos,"paired_folios":len(rs),"ch_n":chn,"ch_rate":chv/chn,"sh_n":shn,"sh_rate":shv/shn,"mean_paired_folio_diff":sum(diffs)/len(diffs)})
  pooled["ch_n"]+=chn;pooled["ch_v"]+=chv;pooled["sh_n"]+=shn;pooled["sh_v"]+=shv
  diff_num+=sum(diffs);diff_den+=len(diffs)
 return {"matched_strata":len(result),"strata_with_5plus_paired_folios":sum(x["paired_folios"]>=5 for x in result),"total_paired_folio_strata":diff_den,"matched_contexts":{"ch_n":pooled["ch_n"],"ch_rate":pooled["ch_v"]/pooled["ch_n"] if pooled["ch_n"] else None,"sh_n":pooled["sh_n"],"sh_rate":pooled["sh_v"]/pooled["sh_n"] if pooled["sh_n"] else None},"mean_difference_across_paired_folio_strata":diff_num/diff_den if diff_den else None,"top_strata":sorted(result,key=lambda x:x["paired_folios"],reverse=True)[:25]}
def main():
 out={"experiment":"exp_611_exact_length_position_ch_sh","method":"Compare ch/sh only within same exact token length and character position of the digraph, on folios containing both contexts in that stratum. Descriptive matching; no inferential p-value; sparse strata and overlapping word types remain confounds.","datasets":[]}
 for label,rel in FILES:
  d=load(label,rel);out["datasets"].append({"label":label,"sha256":d["sha256"],"summary":summarize(d)})
 dest=ROOT/"experiments/exp_611_exact_length_position_ch_sh";dest.mkdir(parents=True,exist_ok=True)
 (dest/"results.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 lines=["# exp611 — Exact word-length and position matching","","## Method","Compare ch and sh only within the same exact token length and same character position of the digraph, and only on folios containing both contexts in that stratum. This is stricter than coarse length bins, but remains descriptive: word identity/template, section and hand are not fully controlled; sparse strata are reported transparently."]
 for d in out["datasets"]:
  s=d["summary"];m=s["matched_contexts"]
  lines += ["",f"## {d['label']}",f"- Source SHA-256: {d['sha256']}",f"- Matched length-position strata: {s['matched_strata']}; strata with at least 5 paired folios: {s['strata_with_5plus_paired_folios']}; paired folio-strata total: {s['total_paired_folio_strata']}",f"- Matched contexts: ch n={m['ch_n']}, vowel rate={m['ch_rate']}; sh n={m['sh_n']}, vowel rate={m['sh_rate']}",f"- Mean of within-folio differences across matched strata (ch−sh): {s['mean_difference_across_paired_folio_strata']}","", "Most populated matched strata:"]
  for x in s["top_strata"][:10]: lines.append(f"- Length {x['length']}, position {x['position']}: paired folios={x['paired_folios']}, ch rate={x['ch_rate']}, sh rate={x['sh_rate']}")
 lines += ["","## Interpretation","This is a stricter composition check than coarse length bands, not a Parisel replication. The matched aggregate is not causal because token identity and section are not controlled; no p-value is reported."]
 (dest/"result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 print(json.dumps(out,indent=2))
if __name__=="__main__":main()
