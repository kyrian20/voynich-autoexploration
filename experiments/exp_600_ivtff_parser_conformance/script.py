#!/usr/bin/env python3
"""Independent structural audit of IVTFF headers and locus identifiers."""
from __future__ import annotations
import collections, hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b",ROOT/"data/transcriptions/eva_zl3b.txt"),
       ("ZL3a",ROOT/"data/transcriptions/zl3a.txt"),
       ("IT2a",ROOT/"data/transcriptions/eva_it2a.txt")]
PAGE_RE=re.compile(r"^<(f[^.>]+)>\\s*(.*)$")
LOCUS_RE=re.compile(r"^<(?P<page>f[^.>]+)\\.(?P<number>\\d+),(?P<slot>[^>]+)>\\s*(?P<body>.*)$")
PAGE_VALID=re.compile(r"^f(?:\\d+[rv](?:[a-z])?|\\d+[rv]\\d*|[a-z0-9]+)$",re.I)
MARKERS="@+*=~&!/"
KINDS=set("PLCR")

def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def inspect(path,label):
    lines=path.read_text(encoding="latin-1").splitlines()
    page=None; header_count=0; locus_count=0; comments=0; slash_continuations=0
    missing_page=[]; malformed_locus=[]; page_mismatch=[]; bad_number=[]; bad_slot=[]
    first_char=collections.Counter(); locus_types=collections.Counter(); markers=collections.Counter()
    pages=set(); locus_keys=collections.Counter(); body_empty=0
    for i,raw in enumerate(lines,1):
        if not raw: continue
        first_char[raw[0]]+=1
        if raw.startswith("#"):
            comments+=1
            if raw.startswith("#=IVTFF") and i==1: pass
            continue
        if raw.startswith("/"):
            slash_continuations+=1
            continue
        pm=PAGE_RE.match(raw.strip())
        if pm and "." not in pm.group(1):
            page=pm.group(1); pages.add(page); header_count+=1
            continue
        lm=LOCUS_RE.match(raw.strip())
        if lm:
            locus_count+=1
            p,num,slot,body=lm.group("page","number","slot","body")
            if page is None: missing_page.append(i)
            elif p!=page: page_mismatch.append({"line":i,"current_page":page,"locus_page":p})
            if not 1<=int(num)<=999: bad_number.append({"line":i,"number":num})
            marker=slot[0] if slot and slot[0] in MARKERS else ""
            rest=slot[1:] if marker else slot
            kind=rest[:1]
            if kind not in KINDS: bad_slot.append({"line":i,"slot":slot})
            else: locus_types[kind]+=1
            markers[marker or "(none)"]+=1
            locus_keys[(p,num,slot)]+=1
            if not body.strip(): body_empty+=1
            continue
        # Lines beginning with '<' should be a page header or locus; other characters may be continuation/data.
        if raw.startswith("<"):
            malformed_locus.append({"line":i,"sample":raw[:120]})
    duplicate_keys=[{"page":k[0],"number":k[1],"slot":k[2],"count":v}
                    for k,v in locus_keys.items() if v>1]
    return {
      "label":label,"source":{"path":str(path.relative_to(ROOT)),"bytes":path.stat().st_size,"sha256":sha(path)},
      "physical_lines":len(lines),"comments":comments,"page_headers":header_count,"unique_pages":len(pages),
      "locus_lines":locus_count,"slash_continuation_lines":slash_continuations,"empty_locus_bodies":body_empty,
      "first_character_counts":dict(first_char),"locus_kind_counts":dict(locus_types),"slot_marker_counts":dict(markers),
      "missing_page_before_locus_line_numbers":missing_page[:100],"missing_page_count":len(missing_page),
      "page_mismatch_examples":page_mismatch[:20],"page_mismatch_count":len(page_mismatch),
      "invalid_locus_number_examples":bad_number[:20],"invalid_locus_number_count":len(bad_number),
      "invalid_slot_examples":bad_slot[:30],"invalid_slot_count":len(bad_slot),
      "unparsed_angle_line_examples":malformed_locus[:30],"unparsed_angle_line_count":len(malformed_locus),
      "duplicate_locus_key_examples":duplicate_keys[:30],"duplicate_locus_key_count":len(duplicate_keys)
    }

def main():
    results=[]
    for label,path in FILES:
        if path.exists(): results.append(inspect(path,label))
    out={"experiment":"exp_600_ivtff_parser_conformance","protocol_version":1,
      "reference":"IVTFF format version 2.0.2, René Zandbergen, 2025-07-08; https://www.voynich.nu/software/ivtt/IVTFF_format.pdf",
      "purpose":"Check the raw structural assumptions used by earlier token-position experiments before adding further hypotheses.",
      "caveats":["This is an independent lightweight audit, not a full official IVTT validator.",
      "The parser deliberately reports unparsed constructs instead of silently interpreting them.",
      "Some IVTFF inline constructs are valid and require format-aware treatment; an anomaly is a review item, not automatically a corrupt file.",
      "No semantic or decipherment claim is tested."],"files":results}
    dest=ROOT/"experiments/exp_600_ivtff_parser_conformance/results.json"
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\\n",encoding="utf-8")
    print(json.dumps({"output":str(dest.relative_to(ROOT)),"files":[{"label":r["label"],"lines":r["physical_lines"],"pages":r["unique_pages"],"loci":r["locus_lines"],"page_mismatch":r["page_mismatch_count"],"bad_slots":r["invalid_slot_count"],"unparsed_angle":r["unparsed_angle_line_count"],"duplicates":r["duplicate_locus_key_count"]} for r in results]},indent=2))
if __name__=="__main__": main()
