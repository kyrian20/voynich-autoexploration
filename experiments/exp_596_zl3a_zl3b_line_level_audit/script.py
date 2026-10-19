#!/usr/bin/env python3
"""Pairwise audit of ZL3a/ZL3b body lines, tokens, and IVTFF paragraph markers."""
from __future__ import annotations
import hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FILES={"ZL3a":ROOT/"data/transcriptions/zl3a.txt","ZL3b":ROOT/"data/transcriptions/eva_zl3b.txt"}

def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()

def words(text):
 text=re.sub(r"<!.*?>"," ",text)
 text=re.sub(r"<[^>]*>"," ",text)
 text=re.sub(r"\[([^:\]]+):[^\]]*\]",r"\1",text)
 text=re.sub(r"\{[^}]*\}"," ",text)
 text=re.sub(r"@\d+;?"," ",text)
 return [w.lower() for w in re.split(r"[.\s,]+",text) if re.fullmatch(r"[A-Za-z]+",w)]

def parse(path):
 rows={};duplicates=[];folio="unknown";dialect="unknown";all_rows=[]
 for n,raw in enumerate(path.read_text(encoding="latin-1").splitlines(),1):
  line=raw.strip()
  if not line or line.startswith("#"):continue
  if re.match(r"^<f\w+>.*\$",line):
   m=re.match(r"^<(f\w+)>",line)
   if m:folio=m.group(1)
   m=re.search(r"\$L=([AB])",line)
   if m:dialect=m.group(1)
   continue
  m=re.match(r"^<([^>]+)>\s+(.*)$",line)
  if not m or "," not in m.group(1):continue
  locid=m.group(1);body=m.group(2)
  locus=locid.split(",",1)[1]
  generic=re.sub(r"^[+*@=~&!/-]+","",locus)
  if not generic.startswith("P"):continue
  key=(folio,locid)
  rec={"folio":folio,"locus_id":locid,"generic_locus":generic,"dialect":dialect,
       "start":body.startswith("<%>"),"end":body.rstrip().endswith("<$>"),
       "tokens":words(body),"raw_body":body,"source_line":n}
  all_rows.append(rec)
  if key in rows:duplicates.append({"key":key,"line":n})
  rows[key]=rec
 return rows,duplicates,all_rows

def main():
 parsed={k:parse(p) for k,p in FILES.items() if p.exists()}
 if len(parsed)!=2:raise SystemExit("Both ZL3a and ZL3b source files are required")
 a,ad,ar=parsed["ZL3a"];b,bd,br=parsed["ZL3b"]
 ka,kb=set(a),set(b);common=ka&kb
 token_diffs=[];marker_diffs=[];dialect_diffs=[];position_diffs=[]
 for key in sorted(common):
  x,y=a[key],b[key]
  if x["tokens"]!=y["tokens"]:
   token_diffs.append({"key":key,"ZL3a_tokens":x["tokens"],"ZL3b_tokens":y["tokens"],
                       "ZL3a_line_initial_daiin":bool(x["tokens"] and x["tokens"][0]=="daiin"),
                       "ZL3b_line_initial_daiin":bool(y["tokens"] and y["tokens"][0]=="daiin")})
  if (x["start"],x["end"])!=(y["start"],y["end"]):
   marker_diffs.append({"key":key,"ZL3a_start_end":[x["start"],x["end"]],"ZL3b_start_end":[y["start"],y["end"]]})
  if x["dialect"]!=y["dialect"]:dialect_diffs.append({"key":key,"ZL3a":x["dialect"],"ZL3b":y["dialect"]})
  if bool(x["tokens"] and x["tokens"][0]=="daiin")!=bool(y["tokens"] and y["tokens"][0]=="daiin"):
   position_diffs.append({"key":key,"ZL3a_first":x["tokens"][0] if x["tokens"] else None,
                           "ZL3b_first":y["tokens"][0] if y["tokens"] else None})
 def marker_counts(rows):
  return {"rows":len(rows),"start":sum(x["start"] for x in rows),"end":sum(x["end"] for x in rows),
          "dialect_start":dict(Counter(x["dialect"] for x in rows if x["start"])),
          "dialect_end":dict(Counter(x["dialect"] for x in rows if x["end"]))}
 def word_stats(rows):
  eligible=[x for x in rows if len(x["tokens"])>=2]
  out={}
  for d in ("A","B"):
   g=[x for x in eligible if x["dialect"]==d]
   for marker in ("start","no_start"):
    s=[x for x in g if x["start"]==(marker=="start")]
    exp=sum(x["tokens"].count("daiin")/len(x["tokens"]) for x in s)
    obs=sum(x["tokens"][0]=="daiin" for x in s)
    out[f"{d}_{marker}"]={"lines":len(s),"daiin_tokens":sum(x["tokens"].count("daiin") for x in s),
      "first_observed":obs,"first_expected":round(exp,5),
      "enrichment":round(obs/exp,5) if exp else None}
  return out
 out={"experiment":"exp_596_zl3a_zl3b_line_level_annotation_audit","protocol_version":1,
  "sources":{label:{"path":str(path.relative_to(ROOT)),"bytes":path.stat().st_size,"sha256":sha(path)}
             for label,path in FILES.items() if path.exists()},
  "matching":{"key":"(folio header, complete IVTFF locus identifier)","ZL3a_rows":len(a),"ZL3b_rows":len(b),
   "common_keys":len(common),"only_ZL3a":len(ka-kb),"only_ZL3b":len(kb-ka),
   "duplicate_keys_ZL3a":len(ad),"duplicate_keys_ZL3b":len(bd),
   "dialect_disagreements":len(dialect_diffs),"token_sequence_disagreements":len(token_diffs),
   "paragraph_marker_disagreements":len(marker_diffs),"line_initial_daiin_status_disagreements":len(position_diffs)},
  "summary":{"ZL3a_markers":marker_counts(ar),"ZL3b_markers":marker_counts(br),
             "ZL3a_daiin":word_stats(ar),"ZL3b_daiin":word_stats(br)},
  "examples":{"token_sequence_disagreements":token_diffs[:100],"paragraph_marker_disagreements":marker_diffs[:100],
              "line_initial_daiin_status_disagreements":position_diffs[:100],
              "dialect_disagreements":dialect_diffs[:100]},
  "interpretation":["This is a file-to-file audit, not independent external replication: ZL3a and ZL3b are closely related versions.",
   "Line keys are matched by folio header and complete IVTFF locus ID; unmatched/duplicate keys are reported, not silently merged.",
   "Tokenizer strips markup and is intended for comparative auditing; source text and hashes are preserved.",
   "Differences in cleaned tokens do not necessarily mean a substantive manuscript reading differs; punctuation and transcription conventions can contribute."]}
 outpath=ROOT/"experiments/exp_596_zl3a_zl3b_line_level_audit/results.json"
 outpath.parent.mkdir(parents=True,exist_ok=True);outpath.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
 print(json.dumps({"output":str(outpath.relative_to(ROOT)),"matching":out["matching"],"summary":out["summary"],
                   "examples":{k:v[:8] for k,v in out["examples"].items()}},indent=2,ensure_ascii=False))
if __name__=="__main__":main()
