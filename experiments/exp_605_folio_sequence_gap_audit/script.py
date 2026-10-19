#!/usr/bin/env python3
"""Audit folio/page-header sequence gaps across bundled Voynich transcriptions."""
import hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b","data/transcriptions/eva_zl3b.txt"),("IT2a","data/transcriptions/eva_it2a.txt")]
# Established commonly cited missing folio sides, expressed as folio numbers.
KNOWN_MISSING_FOLIOS={12,59,60,61,62,63,64,74,91,92,97,98,109,110}
def audit(label, rel):
 p=ROOT/rel
 text=p.read_text(encoding="latin-1")
 heads=[]
 for line_no,line in enumerate(text.splitlines(),1):
  m=re.match(r"^<(f\d+[rv])>.*\$",line.strip())
  if m: heads.append((m.group(1),line_no))
 nums=sorted({int(re.match(r"f(\d+)",x[0]).group(1)) for x in heads})
 sides={n:set() for n in nums}
 for name,_ in heads:
  m=re.match(r"f(\d+)([rv])",name)
  if m:sides[int(m.group(1))].add(m.group(2))
 missing_numbers=sorted(KNOWN_MISSING_FOLIOS-set(nums))
 expected_missing_not_observed=sorted(set(nums)&KNOWN_MISSING_FOLIOS)
 observed_side_gaps=[]
 for n in nums:
  if sides[n] != {"r","v"}:
   observed_side_gaps.append({"folio":n,"observed_sides":sorted(sides[n]),"missing_side_candidate":("v" if "r" in sides[n] else "r" if "v" in sides[n] else "both")})
 return {"label":label,"path":rel,"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"physical_lines":len(text.splitlines()),
 "page_headers":len(heads),"unique_folio_numbers":len(nums),"min_folio_number":min(nums) if nums else None,"max_folio_number":max(nums) if nums else None,
 "missing_numbers_from_known_14_list":missing_numbers,"known_missing_numbers_unexpectedly_present":expected_missing_not_observed,
 "folios_with_only_one_side_header":observed_side_gaps,"header_examples":heads[:8]}
def main():
 out={"experiment":"exp_605_folio_sequence_gap_audit","scope":"Compare folio-number/page-side headers in bundled transcriptions with a predeclared commonly cited list of 14 missing folios. This cannot detect leaves lost before numbering, and missing sides may have different explanations.",
 "known_list":sorted(KNOWN_MISSING_FOLIOS),"sources":[audit(*x) for x in FILES]}
 d=ROOT/"experiments/exp_605_folio_sequence_gap_audit";d.mkdir(parents=True,exist_ok=True)
 (d/"results.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 lines=["# exp_605 — Folio sequence gap audit","","This is a transcription-header audit, not physical codicology. It tests whether the bundled text files reflect the predeclared 14-folio list; it cannot establish unnumbered losses.","", "Predeclared list: "+", ".join(map(str,sorted(KNOWN_MISSING_FOLIOS)))+"."]
 for x in out["sources"]:
  lines += ["",f"## {x['label']}","",f"- Page headers: {x['page_headers']}; unique folio numbers: {x['unique_folio_numbers']}; range: {x['min_folio_number']}–{x['max_folio_number']}.",f"- Listed missing folio numbers absent as expected: {x['missing_numbers_from_known_14_list']}.",f"- Listed missing folio numbers unexpectedly present: {x['known_missing_numbers_unexpectedly_present']}.",f"- Folios with only one side header: {x['folios_with_only_one_side_header']}.",f"- Source SHA-256: {x['sha256']}."]
 lines += ["","## Interpretation","","A matching gap list verifies only that the transcription headers reflect known foliation gaps. It does not prove no other pages were lost, and text-only evidence cannot reliably infer missing leaves that disappeared before numbering. Any one-sided folio header should be checked against physical manuscript images and the transcription's editorial conventions before being classified as a missing page."]
 (d/"result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
 print(json.dumps(out,indent=2))
if __name__=="__main__":main()
