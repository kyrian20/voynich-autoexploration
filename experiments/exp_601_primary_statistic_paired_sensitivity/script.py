#!/usr/bin/env python3
"""Paired transcription-version sensitivity for Currier-B P0 position statistics."""
from __future__ import annotations
import argparse, collections, hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b",ROOT/"data/transcriptions/eva_zl3b.txt"),
       ("ZL3a",ROOT/"data/transcriptions/zl3a.txt")]
TARGETS=("daiin","aiin","chedy","dain","saiin","qokaiin")

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):h.update(block)
    return h.hexdigest()

def clean_words(text):
    text=re.sub(r"<!.*?>"," ",text)
    text=re.sub(r"<[^>]*>"," ",text).replace("<$>"," ").replace("<%>"," ")
    text=re.sub(r"\[([^:\]]+):[^\]]*\]",r"\1",text)
    text=re.sub(r"\{[^}]*\}"," ",text)
    text=re.sub(r"@\d+;?"," ",text)
    return [w.lower() for w in re.split(r"[.\s,]+",text) if re.fullmatch(r"[A-Za-z]+",w)]

def parse(path):
    records={};folio="unknown";currier="unknown";duplicates=[]
    for line_no,raw in enumerate(path.read_text(encoding="latin-1").splitlines(),1):
        line=raw.strip()
        if not line or line.startswith("#"):continue
        hm=re.match(r"^<(f[^>]+)>\s*(.*)$",line)
        if hm and "," not in hm.group(1):
            folio=hm.group(1)
            lm=re.search(r"\$L=([AB])",hm.group(2))
            currier=lm.group(1) if lm else "unknown"
            continue
        m=re.match(r"^<([^>]+)>\s+(.*)$",line)
        if not m or "," not in m.group(1):continue
        ident,raw_locus=m.group(1).split(",",1)
        ident=ident.strip();raw_locus=raw_locus.strip()
        if not re.match(r"^f[^.]+\..+$",ident):continue
        locus=re.sub(r"^[+*@=~&!/]+","",raw_locus)
        rec={"key":ident,"folio":folio,"currier":currier,"raw_locus":raw_locus,
             "locus":locus,"words":clean_words(m.group(2)),"source_line_number":line_no}
        if ident in records:duplicates.append(ident)
        else:records[ident]=rec
    return {"path":str(path.relative_to(ROOT)),"bytes":path.stat().st_size,
            "sha256":sha256(path),"records":records,"duplicates":duplicates}

def eligible(rec,dialect="B"):
    return rec["currier"]==dialect and rec["locus"]=="P0" and len(rec["words"])>=2

def summarize(records,dialect="B"):
    rows=[r for r in records.values() if eligible(r,dialect)]
    out={"eligible_lines":len(rows),"targets":{}}
    for w in TARGETS:
        total=sum(r["words"].count(w) for r in rows)
        first=sum(r["words"][0]==w for r in rows)
        expected=sum(r["words"].count(w)/len(r["words"]) for r in rows)
        out["targets"][w]={"token_count":total,"first_observed":first,
          "first_expected":round(expected,6),
          "enrichment":round(first/expected,6) if expected else None}
    return out

def paired_compare(a,b):
    ar,br=a["records"],b["records"]
    common=sorted(set(ar)&set(br))
    common_eligible=[key for key in common if eligible(ar[key]) and eligible(br[key])]
    by_target={}
    for w in TARGETS:
        a_count=b_count=0;a_first=b_first=0
        a_expected=b_expected=0.0
        occurrence_diff_lines=first_flag_changes=0
        zl3b_only_first=zl3a_only_first=0
        examples=[]
        for key in common_eligible:
            wa,wb=ar[key]["words"],br[key]["words"]
            ca,cb=wa.count(w),wb.count(w)
            a_count+=ca;b_count+=cb
            a_expected+=ca/len(wa);b_expected+=cb/len(wb)
            fa,fb=wa[0]==w,wb[0]==w
            a_first+=fa;b_first+=fb
            if ca!=cb:occurrence_diff_lines+=1
            if fa!=fb:
                first_flag_changes+=1
                if fa:zl3b_only_first+=1
                if fb:zl3a_only_first+=1
                if len(examples)<20:
                    examples.append({"key":key,"ZL3b_first_token":wa[0],"ZL3a_first_token":wb[0],
                                     "ZL3b_target_count":ca,"ZL3a_target_count":cb})
        by_target[w]={
          "matched_eligible_lines":len(common_eligible),
          "ZL3b_token_count":a_count,"ZL3a_token_count":b_count,
          "token_count_delta_ZL3a_minus_ZL3b":b_count-a_count,
          "matched_lines_with_token_count_difference":occurrence_diff_lines,
          "ZL3b_first_observed":a_first,"ZL3a_first_observed":b_first,
          "first_count_delta_ZL3a_minus_ZL3b":b_first-a_first,
          "ZL3b_first_expected":round(a_expected,6),"ZL3a_first_expected":round(b_expected,6),
          "expected_delta_ZL3a_minus_ZL3b":round(b_expected-a_expected,6),
          "ZL3b_enrichment":round(a_first/a_expected,6) if a_expected else None,
          "ZL3a_enrichment":round(b_first/b_expected,6) if b_expected else None,
          "matched_lines_where_first_position_status_changed":first_flag_changes,
          "ZL3b_only_first":zl3b_only_first,"ZL3a_only_first":zl3a_only_first,
          "examples_first_status_changes":examples}
    # Inspect unpaired line identifiers: they can affect full-file totals, but not the matched analysis.
    only_a=sorted(set(ar)-set(br));only_b=sorted(set(br)-set(ar))
    unmatched={}
    for label,keys,records in (("ZL3b",only_a,ar),("ZL3a",only_b,br)):
        chosen=[]
        for key in keys:
            r=records[key]
            if eligible(r):chosen.append({"key":key,"folio":r["folio"],"locus":r["raw_locus"],
                                         "first_token":r["words"][0],"daiin_count":r["words"].count("daiin")})
        unmatched[label]={"line_ids":keys,"eligible_B_P0_records":chosen}
    changed_keys=[key for key in common_eligible if ar[key]["words"]!=br[key]["words"]]
    changed_first_keys=[key for key in common_eligible if ar[key]["words"][0]!=br[key]["words"][0]]
    return {"common_identifiers":len(common),"matched_eligible_B_P0_lines":len(common_eligible),
      "aligned_B_P0_lines_with_any_clean_token_change":len(changed_keys),
      "aligned_B_P0_lines_with_changed_first_token":len(changed_first_keys),
      "changed_B_P0_line_keys":changed_keys,
      "changed_first_token_line_keys":changed_first_keys,
      "by_target":by_target,"unmatched_records":unmatched}

def main():
    a=parse(FILES[0][1]);b=parse(FILES[1][1])
    data={"experiment":"exp_601_primary_statistic_paired_sensitivity",
      "protocol_version":1,
      "source_files":[{k:v for k,v in f.items() if k not in ("records","duplicates")} | {"duplicate_keys":len(f["duplicates"])} for f in (a,b)],
      "filter":{"Currier":"B","normalized_locus":"P0","minimum_clean_tokens_per_line":2},
      "full_version_summaries":{"ZL3b":summarize(a["records"]),"ZL3a":summarize(b["records"])},
      "paired_alignment":paired_compare(a,b),
      "notes":["This is a paired sensitivity comparison of two transcriptions of the same manuscript, not independent-sample inference.",
        "The expected first count sums per-line target frequency (target occurrences / line length).",
        "A line-first status change counts only if the target is first in one version but not the other.",
        "No significance test is applied to differences between transcription versions.",
        "Tokenizer/locator parser is the declared operational rule used for this family; independent parser review remains a follow-up.",
        "No semantic or decipherment claim."]}
    out=ROOT/"experiments/exp_601_primary_statistic_paired_sensitivity/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),
      "full_version_summaries":data["full_version_summaries"],
      "paired_summary":{"matched":data["paired_alignment"]["matched_eligible_B_P0_lines"],
        "token_changed":data["paired_alignment"]["aligned_B_P0_lines_with_any_clean_token_change"],
        "first_changed":data["paired_alignment"]["aligned_B_P0_lines_with_changed_first_token"]},
      "targets":data["paired_alignment"]["by_target"]},indent=2))

if __name__=="__main__":main()
