#!/usr/bin/env python3
"""Replication of exp_594 paragraph-marker statistics in ZL3b and ZL3a."""
from __future__ import annotations
import argparse, hashlib, json, random, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b",ROOT/"data/transcriptions/eva_zl3b.txt"),
       ("ZL3a",ROOT/"data/transcriptions/zl3a.txt")]

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
        start=body.startswith("<%>")
        end=body.rstrip().endswith("<$>")
        words=clean_words(body)
        if len(words)<2: continue
        rows.append({"folio":folio,"currier":currier,"locus":locus,
                     "paragraph_start_marker":start,"paragraph_end_marker":end,
                     "words":words})
    return rows

def summary(rows):
    exp=sum(r["words"].count("daiin")/len(r["words"]) for r in rows)
    obs=sum(r["words"][0]=="daiin" for r in rows)
    return {"lines":len(rows),"daiin_tokens":sum(r["words"].count("daiin") for r in rows),
            "first_observed":obs,"first_expected":round(exp,5),
            "enrichment":round(obs/exp,5) if exp else None,
            "last_observed":sum(r["words"][-1]=="daiin" for r in rows)}

def test(rows,n_perm,seed):
    s=summary(rows);obs=s["first_observed"]
    rng=random.Random(seed);high=low=total=0
    for _ in range(n_perm):
        x=sum(r["words"][rng.randrange(len(r["words"]))]=="daiin" for r in rows)
        total+=x;high+=x>=obs;low+=x<=obs
    s.update({"null_mean":round(total/n_perm,5),
              "p_upper_tail_plus_one":round((high+1)/(n_perm+1),6),
              "p_lower_tail_plus_one":round((low+1)/(n_perm+1),6),
              "permutations":n_perm,"seed":seed})
    return s

def holm(values):
    ordered=sorted(values.items(),key=lambda x:x[1]);out={};running=0.0;m=len(ordered)
    for i,(key,p) in enumerate(ordered):
        running=max(running,min(1.0,(m-i)*p));out[key]=round(running,6)
    return out

def analyze(path,label,n_perm,seed):
    rows=parse(path)
    counts={"eligible_P_lines":len(rows),
            "start_marked_lines":sum(r["paragraph_start_marker"] for r in rows),
            "end_marked_lines":sum(r["paragraph_end_marker"] for r in rows),
            "start_and_end_same_line":sum(r["paragraph_start_marker"] and r["paragraph_end_marker"] for r in rows),
            "by_dialect":{}}
    strata={}
    for di,dialect in enumerate(("A","B")):
        group=[r for r in rows if r["currier"]==dialect]
        counts["by_dialect"][dialect]={
            "P_lines":len(group),
            "start_marked":sum(r["paragraph_start_marker"] for r in group),
            "end_marked":sum(r["paragraph_end_marker"] for r in group),
            "no_start_marker":sum(not r["paragraph_start_marker"] for r in group)}
        for si,start in enumerate((True,False)):
            subset=[r for r in group if r["paragraph_start_marker"]==start]
            if len(subset)<30: continue
            key=f"Currier{dialect}_{'explicit_start' if start else 'no_start_marker'}"
            strata[key]=test(subset,n_perm,seed+di*100+si)
        for tail in ("upper","lower"):
            field=f"p_{tail}_tail_plus_one"
            values={k:v[field] for k,v in strata.items() if k.startswith(f"Currier{dialect}_")}
            for k,p in holm(values).items(): strata[k][f"p_holm_{tail}_{dialect}_family"]=p
    return {"transcription":label,"source":{"path":str(path.relative_to(ROOT)),
            "bytes":path.stat().st_size,"sha256":sha256(path)},
            "counts":counts,"tests":strata}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--permutations",type=int,default=5000)
    ap.add_argument("--seed",type=int,default=59520261019)
    args=ap.parse_args()
    if args.permutations<999: ap.error("--permutations must be >=999")
    versions=[analyze(path,label,args.permutations,args.seed+i*1000)
              for i,(label,path) in enumerate(FILES) if path.exists()]
    comparisons={}
    if len(versions)==2:
        a,b=versions
        keys=set(a["tests"])|set(b["tests"])
        for key in sorted(keys):
            va=a["tests"].get(key);vb=b["tests"].get(key)
            comparisons[key]={
                "ZL3b_enrichment":va.get("enrichment") if va else None,
                "ZL3a_enrichment":vb.get("enrichment") if vb else None,
                "difference_ZL3a_minus_ZL3b":round(vb["enrichment"]-va["enrichment"],5) if va and vb and va.get("enrichment") is not None and vb.get("enrichment") is not None else None,
                "ZL3b_lines":va.get("lines") if va else 0,
                "ZL3a_lines":vb.get("lines") if vb else 0,
                "ZL3b_explicit_first":va.get("first_observed") if va else None,
                "ZL3a_explicit_first":vb.get("first_observed") if vb else None
            }
    data={"experiment":"exp_595_paragraph_marker_cross_transcription_replication",
          "protocol_version":1,"format_reference":"https://voynich.nu/software/ivtt/IVTFF_format.pdf §6.9",
          "filters":{"generic_locus_type":"P*","minimum_clean_tokens_per_line":2,"dialects_separate":True},
          "versions":versions,"cross_transcription_comparison":comparisons,
          "notes":["No-start-marker is not asserted to mean continuation; tagging may be incomplete.",
                   "Paragraph boundaries are transcriber decisions under IVTFF §6.9.",
                   "Comparisons are conditional on the same parser and cleaning rules.",
                   "P-values are Monte Carlo; Holm adjustment is applied to tails within dialect and transcription.",
                   "No semantic/decipherment inference."]}
    out=ROOT/"experiments/exp_595_paragraph_marker_replication/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),"versions":versions,
                      "cross_transcription_comparison":comparisons},indent=2))

if __name__=="__main__": main()
