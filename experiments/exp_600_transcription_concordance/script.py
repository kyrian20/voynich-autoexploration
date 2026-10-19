#!/usr/bin/env python3
"""Independent line-key alignment and token concordance audit for ZL3b/ZL3a."""
from __future__ import annotations
import argparse, collections, difflib, hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b",ROOT/"data/transcriptions/eva_zl3b.txt"),
       ("ZL3a",ROOT/"data/transcriptions/zl3a.txt")]

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):h.update(block)
    return h.hexdigest()

def clean_words(text):
    # This is a declared comparison tokenizer, not an authoritative parser
    # for every IVTFF apparatus convention. Preserve the first alternative.
    text=re.sub(r"<!.*?>"," ",text)
    text=re.sub(r"<[^>]*>"," ",text)
    text=text.replace("<$>"," ").replace("<%>"," ")
    text=re.sub(r"\[([^:\]]+):[^\]]*\]",r"\1",text)
    text=re.sub(r"\{[^}]*\}"," ",text)
    text=re.sub(r"@\d+;?"," ",text)
    return [w.lower() for w in re.split(r"[.\s,]+",text) if re.fullmatch(r"[A-Za-z]+",w)]

def parse(path,label):
    records={};duplicates=[];invalid_identifiers=[];header_count=0;folio="unknown";currier="unknown"
    marker_counts=collections.Counter();locus_counts=collections.Counter()
    line_count=0
    for line_no,raw in enumerate(path.read_text(encoding="latin-1").splitlines(),1):
        line=raw.strip()
        if not line or line.startswith("#"):continue
        # Folio headers can carry compound identifiers such as <f67r1>, not
        # only simple <f1r>/<f1v> identifiers.
        hm=re.match(r"^<(f[^>]+)>\s*(.*)$",line)
        if hm and "," not in hm.group(1):
            folio=hm.group(1);header_count+=1
            lm=re.search(r"\$L=([AB])",hm.group(2))
            if lm:currier=lm.group(1)
            else:currier="unknown"
            continue
        m=re.match(r"^<([^>]+)>\s+(.*)$",line)
        if not m or "," not in m.group(1):continue
        meta=m.group(1);body=m.group(2)
        ident,raw_locus=meta.split(",",1)
        ident=ident.strip();raw_locus=raw_locus.strip()
        # Identifier (folio + line ordinal) is the cross-version alignment key.
        # IVTFF line identifiers can include suffixes beyond a simple ordinal.
        # Accept any non-empty text suffix after the folio + dot; record exceptions.
        if not re.match(r"^f[^.]+\..+$",ident):
            invalid_identifiers.append({"identifier":ident,"source_line_number":line_no})
            continue
        line_count+=1
        locus=re.sub(r"^[+*@=~&!/]+","",raw_locus)
        prefix=raw_locus[0] if raw_locus and raw_locus[0] in "+*@=~&!/" else "none"
        words=clean_words(body)
        start_marker=body.startswith("<%>")
        end_marker=body.rstrip().endswith("<$>")
        rec={"key":ident,"folio":folio,"currier":currier,"raw_locus":raw_locus,
             "locus":locus,"locator":prefix,"body":body.strip(),"tokens":words,
             "paragraph_start_marker":start_marker,"paragraph_end_marker":end_marker,
             "source_line_number":line_no}
        locus_counts[(currier,locus,prefix)]+=1
        marker_counts[(currier,start_marker,end_marker)]+=1
        if ident in records:
            duplicates.append({"key":ident,"source_line_number":line_no})
            # Keep all occurrences separately to avoid silently choosing one.
            records[ident].setdefault("duplicates",[]).append(rec)
        else:records[ident]=rec
    return {"label":label,"path":str(path.relative_to(ROOT)),"bytes":path.stat().st_size,
            "sha256":sha256(path),"folio_headers":header_count,"line_records":line_count,
            "unique_line_keys":len(records),"records":records,"duplicates":duplicates,
            "invalid_identifiers":invalid_identifiers,
            "locus_counts":[{"currier":k[0],"locus":k[1],"locator":k[2],"count":v}
                            for k,v in sorted(locus_counts.items())],
            "marker_counts":[{"currier":k[0],"start":k[1],"end":k[2],"count":v}
                             for k,v in sorted(marker_counts.items())]}

def diff_token_sequences(a,b):
    matcher=difflib.SequenceMatcher(a=a,b=b,autojunk=False)
    substitutions=insertions=deletions=0
    for tag,i1,i2,j1,j2 in matcher.get_opcodes():
        if tag=="replace":
            substitutions+=max(i2-i1,j2-j1)
        elif tag=="insert":insertions+=j2-j1
        elif tag=="delete":deletions+=i2-i1
    return {"substitutions_min_count":substitutions,"insertions":insertions,"deletions":deletions}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--examples",type=int,default=40)
    args=ap.parse_args()
    parsed=[parse(path,label) for label,path in FILES if path.exists()]
    if len(parsed)!=2:raise SystemExit("Both ZL3b and ZL3a transcription files are required")
    a,b=parsed
    ar,br=a["records"],b["records"]
    akeys,bkeys=set(ar),set(br);common=sorted(akeys&bkeys)
    only_a=sorted(akeys-bkeys);only_b=sorted(bkeys-akeys)
    summary=collections.Counter();by_currier=collections.Counter()
    by_locus=collections.Counter();by_currier_locus=collections.Counter()
    examples=[];token_edits=collections.Counter();token_diff_lines=[]
    marker_diffs=collections.Counter();locus_diffs=collections.Counter()
    for key in common:
        x,y=ar[key],br[key]
        summary["aligned_keys"]+=1
        if x["raw_locus"]!=y["raw_locus"]:
            locus_diffs[(x["raw_locus"],y["raw_locus"])]+=1
        if x["locus"]==y["locus"]:summary["normalized_locus_equal"]+=1
        else:summary["normalized_locus_different"]+=1
        if x["currier"]==y["currier"]:summary["currier_equal"]+=1
        else:summary["currier_different"]+=1
        if x["paragraph_start_marker"]!=y["paragraph_start_marker"]:
            marker_diffs["paragraph_start_annotation_diff"]+=1
        if x["paragraph_end_marker"]!=y["paragraph_end_marker"]:
            marker_diffs["paragraph_end_annotation_diff"]+=1
        raw_equal=x["body"]==y["body"]
        tokens_equal=x["tokens"]==y["tokens"]
        summary["raw_payload_equal" if raw_equal else "raw_payload_different"]+=1
        summary["clean_token_sequence_equal" if tokens_equal else "clean_token_sequence_different"]+=1
        cur=x["currier"] if x["currier"]==y["currier"] else "mismatch"
        locus=x["locus"] if x["locus"]==y["locus"] else "locus_mismatch"
        by_currier[(cur,"equal" if tokens_equal else "different")]+=1
        by_locus[(locus,"equal" if tokens_equal else "different")]+=1
        by_currier_locus[(cur,locus,"equal" if tokens_equal else "different")]+=1
        if not tokens_equal:
            edits=diff_token_sequences(x["tokens"],y["tokens"])
            for k,v in edits.items():token_edits[k]+=v
            token_diff_lines.append(key)
            if len(examples)<args.examples:
                examples.append({"key":key,"currier":x["currier"],"locus_ZL3b":x["raw_locus"],
                  "locus_ZL3a":y["raw_locus"],"locator_ZL3b":x["locator"],"locator_ZL3a":y["locator"],
                  "ZL3b_tokens":x["tokens"],"ZL3a_tokens":y["tokens"],
                  "token_edit_summary":edits,
                  "paragraph_start_ZL3b":x["paragraph_start_marker"],
                  "paragraph_start_ZL3a":y["paragraph_start_marker"]})
    data={
      "experiment":"exp_600_transcription_concordance_audit","protocol_version":1,
      "alignment_rule":"match IVTFF text records by exact folio.line identifier before comma; keep locus and locator differences as comparison outcomes",
      "tokenization_rule":"strip transcriber comments/markup, keep the first [a:b] alternative, remove {uncertain} spans, split on period/comma/whitespace, retain ASCII-letter tokens only",
      "sources":[{k:v for k,v in p.items() if k not in ("records","duplicates","locus_counts","marker_counts","invalid_identifiers")} for p in parsed],
      "coverage":{
        "ZL3b_unique_line_keys":len(akeys),"ZL3a_unique_line_keys":len(bkeys),
        "aligned_keys":len(common),"only_in_ZL3b_count":len(only_a),"only_in_ZL3a_count":len(only_b),
        "only_in_ZL3b_examples":only_a[:args.examples],"only_in_ZL3a_examples":only_b[:args.examples],
        "duplicate_keys_ZL3b":a["duplicates"],"duplicate_keys_ZL3a":b["duplicates"],
        "invalid_identifier_count_ZL3b":len(a["invalid_identifiers"]),
        "invalid_identifier_count_ZL3a":len(b["invalid_identifiers"]),
        "invalid_identifier_examples_ZL3b":a["invalid_identifiers"][:args.examples],
        "invalid_identifier_examples_ZL3a":b["invalid_identifiers"][:args.examples]},
      "alignment_summary":dict(summary),
      "token_edit_totals_on_differing_lines":dict(token_edits),
      "token_different_line_keys":token_diff_lines,
      "by_currier_token_sequence_equal_vs_different":[{"currier":k[0],"status":k[1],"count":v} for k,v in sorted(by_currier.items())],
      "by_normalized_locus_token_sequence_equal_vs_different":[{"locus":k[0],"status":k[1],"count":v} for k,v in sorted(by_locus.items())],
      "by_currier_and_locus":[{"currier":k[0],"locus":k[1],"status":k[2],"count":v} for k,v in sorted(by_currier_locus.items())],
      "raw_locus_disagreements":[{"ZL3b":k[0],"ZL3a":k[1],"count":v} for k,v in locus_diffs.most_common(50)],
      "paragraph_marker_disagreements":dict(marker_diffs),
      "examples_token_differences":examples,
      "per_file_locus_counts":{p["label"]:p["locus_counts"] for p in parsed},
      "per_file_marker_counts":{p["label"]:p["marker_counts"] for p in parsed},
      "notes":[
        "This is a provenance/concordance audit, not an independent decipherment test.",
        "Exact source-line equality is stricter than cleaned-token equality; comments and alternate-reading notation can differ while cleaned tokens agree.",
        "Tokenization is intentionally conservative and must be treated as an operational comparison rule, not the definitive interpretation of every IVTFF convention.",
        "ZL3a and ZL3b are alternative transcriptions of the same manuscript, not independent samples.",
        "All unmatched/duplicate keys and disagreements are reported; no silent pooling is performed."
      ]}
    out=ROOT/"experiments/exp_600_transcription_concordance/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),"coverage":data["coverage"],
      "alignment_summary":data["alignment_summary"],
      "by_currier":data["by_currier_token_sequence_equal_vs_different"],
      "examples":examples[:10]},indent=2))

if __name__=="__main__":main()
