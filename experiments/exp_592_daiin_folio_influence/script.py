#!/usr/bin/env python3
"""Leave-one-folio-out influence diagnostics for Currier-B P0 daiin position."""
from __future__ import annotations
import argparse, collections, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data/transcriptions/eva_zl3b.txt"

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""): h.update(block)
    return h.hexdigest()

def clean_words(text):
    text=re.sub(r"<!.*?>"," ",text)
    text=re.sub(r"<[^>]*>"," ",text).replace("<$>"," ").replace("<%>"," ")
    text=re.sub(r"\[([^:\]]+):[^\]]*\]",r"\1",text)
    text=re.sub(r"\{[^}]*\}"," ",text)
    text=re.sub(r"@\d+;?"," ",text)
    return [w.lower() for w in re.split(r"[.\s,]+",text) if re.fullmatch(r"[A-Za-z]+",w)]

def parse(path):
    rows=[]; folio="unknown"; currier="unknown"
    for raw in path.read_text(encoding="latin-1").splitlines():
        line=raw.strip()
        if not line or line.startswith("#"): continue
        if re.match(r"^<f\w+>.*\$",line):
            m=re.match(r"^<(f\w+)>",line)
            if m: folio=m.group(1)
            m=re.search(r"\$L=([AB])",line)
            if m: currier=m.group(1)
            continue
        m=re.match(r"^<([^>]+)>\s+(.*)$",line)
        if not m or "," not in m.group(1): continue
        locus_raw=m.group(1).split(",",1)[1]
        if not re.match(r"^[+*@]?P",locus_raw): continue
        locus=re.sub(r"^[+*@]","",locus_raw)
        if locus!="P0" or currier!="B": continue
        words=clean_words(m.group(2))
        if len(words)<2: continue
        rows.append({"folio":folio,"words":words})
    return rows

def counts(rows):
    obs=sum(r["words"][0]=="daiin" for r in rows)
    exp=sum(r["words"].count("daiin")/len(r["words"]) for r in rows)
    tokens=sum(r["words"].count("daiin") for r in rows)
    return {"lines":len(rows),"daiin_tokens":tokens,"first_observed":obs,
            "first_expected":round(exp,6),"enrichment":round(obs/exp,6) if exp else None,
            "excess_first_over_expected":round(obs-exp,6)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--top",type=int,default=20)
    args=ap.parse_args()
    rows=parse(CORPUS)
    folios=sorted({r["folio"] for r in rows})
    overall=counts(rows)
    per_folio=[]
    for folio in folios:
        sub=[r for r in rows if r["folio"]==folio]
        st=counts(sub)
        per_folio.append({"folio":folio,**st,
                          "share_of_observed_initial_daiin":round(st["first_observed"]/overall["first_observed"],6) if overall["first_observed"] else None,
                          "share_of_expected_daiin_initial":round(st["first_expected"]/overall["first_expected"],6) if overall["first_expected"] else None})
    leave=[]
    for folio in folios:
        remaining=[r for r in rows if r["folio"]!=folio]
        st=counts(remaining)
        leave.append({"omitted_folio":folio,**st,
                      "delta_enrichment_vs_full":round(st["enrichment"]-overall["enrichment"],6)})
    by_influence=sorted(leave,key=lambda x: abs(x["delta_enrichment_vs_full"]),reverse=True)
    top_observed=sorted(per_folio,key=lambda x:(x["first_observed"],x["excess_first_over_expected"]),reverse=True)
    top_excess=sorted(per_folio,key=lambda x:x["excess_first_over_expected"],reverse=True)
    top_share=sorted(per_folio,key=lambda x:x["share_of_observed_initial_daiin"] or 0,reverse=True)
    out_data={
      "experiment":"exp_592_daiin_folio_influence",
      "protocol_version":1,
      "source":{"path":"data/transcriptions/eva_zl3b.txt","bytes":CORPUS.stat().st_size,"sha256":sha256(CORPUS)},
      "filters":{"currier":"B","locus":"P0","minimum_clean_tokens_per_line":2,
                 "body_locus_regex":"^[+*@]?P","token_cleaning":"same conservative cleanup as exp_589–591"},
      "overall":overall,"folio_count":len(folios),
      "most_influential_leave_one_folio_out":by_influence[:args.top],
      "top_folios_by_initial_count":top_observed[:args.top],
      "top_folios_by_initial_excess":top_excess[:args.top],
      "top_folios_by_share_of_initial_count":top_share[:args.top],
      "all_folios":per_folio,
      "all_leave_one_folio_out":leave,
      "interpretation_guardrails":[
        "Leave-one-folio-out changes are influence diagnostics, not independent significance tests.",
        "Per-folio rankings are post hoc descriptive statistics; do not interpret their rank as evidence of meaning.",
        "The conditional expectation preserves each line's token inventory and length.",
        "This is a position-only test, not a decipherment."
      ]
    }
    out=ROOT/"experiments/exp_592_daiin_folio_influence/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(out_data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),"overall":overall,
       "most_influential_leave_one_folio_out":by_influence[:args.top],
       "top_folios_by_initial_count":top_observed[:args.top],
       "top_folios_by_initial_excess":top_excess[:args.top]},indent=2))

if __name__=="__main__": main()
