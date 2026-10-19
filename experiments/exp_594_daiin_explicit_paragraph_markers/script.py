#!/usr/bin/env python3
"""Audit explicit IVTFF paragraph markers against first-token daiin positioning."""
from __future__ import annotations
import argparse, hashlib, json, random, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CORPUS=ROOT/"data/transcriptions/eva_zl3b.txt"

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
        locus=re.sub(r"^[+*@=~&!/]*","",locus_raw)
        if not locus.startswith("P"): continue
        body=m.group(2)
        # Official IVTFF §6.9 says the paragraph-open marker must appear
        # at the beginning of the transliterated line; end marker at its end.
        start=body.startswith("<%>")
        end=body.rstrip().endswith("<$>")
        words=clean_words(body)
        if len(words)<2: continue
        rows.append({"folio":folio,"currier":currier,"locus":locus,
                     "locator":locus_raw[0] if locus_raw and locus_raw[0] in "@+*=~&!/" else "none",
                     "paragraph_start_marker":start,"paragraph_end_marker":end,"words":words})
    return rows

def stat(rows):
    expected=sum(r["words"].count("daiin")/len(r["words"]) for r in rows)
    observed=sum(r["words"][0]=="daiin" for r in rows)
    total=sum(r["words"].count("daiin") for r in rows)
    return {"lines":len(rows),"daiin_tokens":total,"first_observed":observed,
            "first_expected":round(expected,5),
            "enrichment":round(observed/expected,5) if expected else None,
            "last_observed":sum(r["words"][-1]=="daiin" for r in rows)}

def test(rows,n_perm,seed):
    result=stat(rows)
    if not rows or result["first_expected"] is None:
        result.update({"p_upper_tail_plus_one":None,"p_lower_tail_plus_one":None})
        return result
    observed=result["first_observed"]
    rng=random.Random(seed); high=low=total=0
    for _ in range(n_perm):
        x=sum(r["words"][rng.randrange(len(r["words"]))]=="daiin" for r in rows)
        total+=x; high+=x>=observed; low+=x<=observed
    result.update({"null_mean":round(total/n_perm,5),
                   "p_upper_tail_plus_one":round((high+1)/(n_perm+1),6),
                   "p_lower_tail_plus_one":round((low+1)/(n_perm+1),6),
                   "permutations":n_perm,"seed":seed})
    return result

def holm(values):
    items=sorted(values.items(),key=lambda item:item[1]); out={}; run=0.0; m=len(items)
    for i,(key,p) in enumerate(items):
        run=max(run,min(1.0,(m-i)*p));out[key]=round(run,6)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--permutations",type=int,default=5000)
    ap.add_argument("--seed",type=int,default=59420261019)
    args=ap.parse_args()
    if args.permutations<999: ap.error("--permutations must be >=999")
    rows=parse(CORPUS)
    markers={}
    for di,dialect in enumerate(("A","B")):
        for si,start in enumerate((True,False)):
            group=[r for r in rows if r["currier"]==dialect and r["paragraph_start_marker"]==start]
            if len(group)>=30:
                key=f"Currier{dialect}_{'explicit_paragraph_start' if start else 'no_start_marker'}"
                markers[key]=test(group,args.permutations,args.seed+di*100+si)
    # Adjust directional tails separately within each dialect and marker status.
    for dialect in ("A","B"):
        keys=[k for k in markers if k.startswith(f"Currier{dialect}_")]
        for tail in ("upper","lower"):
            pfield=f"p_{tail}_tail_plus_one"
            for k,p in holm({k:markers[k][pfield] for k in keys if markers[k].get(pfield) is not None}).items():
                markers[k][f"p_holm_{tail}_{dialect}_family"]=p
    all_counts={"body_lines":len(rows),
                "paragraph_start_marked_lines":sum(r["paragraph_start_marker"] for r in rows),
                "paragraph_end_marked_lines":sum(r["paragraph_end_marker"] for r in rows),
                "both_markers_same_line":sum(r["paragraph_start_marker"] and r["paragraph_end_marker"] for r in rows),
                "by_dialect_and_marker":{}}
    for dialect in ("A","B"):
        group=[r for r in rows if r["currier"]==dialect]
        all_counts["by_dialect_and_marker"][dialect]={
            "P_locus_lines":len(group),
            "explicit_start":sum(r["paragraph_start_marker"] for r in group),
            "explicit_end":sum(r["paragraph_end_marker"] for r in group),
            "no_start_marker":sum(not r["paragraph_start_marker"] for r in group)}
    data={"experiment":"exp_594_daiin_explicit_paragraph_markers","protocol_version":1,
          "source":{"path":"data/transcriptions/eva_zl3b.txt","bytes":CORPUS.stat().st_size,"sha256":sha256(CORPUS)},
          "format_reference":"https://voynich.nu/software/ivtt/IVTFF_format.pdf, §6.9; paragraph starts use <%> at beginning of line, ends use <$> at end.",
          "filters":{"generic_locus_type":"P*","minimum_clean_tokens_per_line":2,"dialects_separate":True},
          "counts":all_counts,"tests":markers,
          "notes":["A line without <%> is called no_start_marker, not definitively a continuation: paragraph segmentation is a transcriber decision and tagging may be incomplete.",
                   "Expected first count preserves each eligible line's token inventory and length.",
                   "P-values are Monte Carlo with separately Holm-adjusted upper/lower tails within dialect.",
                   "This tests explicit transcription markers, not manuscript semantics."]}
    out=ROOT/"experiments/exp_594_daiin_explicit_paragraph_markers/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),"counts":all_counts,"tests":markers},indent=2))

if __name__=="__main__": main()
