#!/usr/bin/env python3
"""Compare line-initial daiin between paragraph-opening and continuation lines."""
from __future__ import annotations
import argparse, hashlib, json, random, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CORPUS=ROOT/"data/transcriptions/eva_zl3b.txt"

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
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
        modifier=locus_raw[0] if locus_raw and locus_raw[0] in "+*@" else "none"
        locus=re.sub(r"^[+*@]","",locus_raw)
        words=clean_words(m.group(2))
        if len(words)<2: continue
        rows.append({"folio":folio,"currier":currier,"locus":locus,
                     "modifier":modifier,"words":words})
    return rows

def summary(rows):
    exp=sum(r["words"].count("daiin")/len(r["words"]) for r in rows)
    obs=sum(r["words"][0]=="daiin" for r in rows)
    return {"lines":len(rows),"daiin_tokens":sum(r["words"].count("daiin") for r in rows),
            "first_observed":obs,"first_expected":round(exp,5),
            "enrichment":round(obs/exp,5) if exp else None,
            "last_observed":sum(r["words"][-1]=="daiin" for r in rows)}

def monte_carlo(rows,n_perm,seed):
    exp=sum(r["words"].count("daiin")/len(r["words"]) for r in rows)
    obs=sum(r["words"][0]=="daiin" for r in rows)
    rng=random.Random(seed); ge=0; total=0
    for _ in range(n_perm):
        x=sum(r["words"][rng.randrange(len(r["words"]))]=="daiin" for r in rows)
        total+=x; ge+=x>=obs
    return {"p_one_sided_plus_one":round((ge+1)/(n_perm+1),6),
            "null_mean":round(total/n_perm,5),"permutations":n_perm,"seed":seed}

def holm(pvalues):
    ordered=sorted(pvalues.items(),key=lambda x:x[1]); out={}; running=0.0; m=len(ordered)
    for rank,(k,p) in enumerate(ordered):
        running=max(running,min(1.0,(m-rank)*p));out[k]=round(running,6)
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--permutations",type=int,default=5000)
    ap.add_argument("--seed",type=int,default=59320261019)
    args=ap.parse_args()
    if args.permutations<999: ap.error("--permutations must be >=999")
    rows=parse(CORPUS)
    # IVTFF prefix modifiers are operational paragraph/line flags whose precise
    # semantics can vary with the transcription conventions. Treat them as
    # explicit metadata categories, never assume one is a paragraph opener
    # without the format specification. The primary contrast tests @ vs +/*/none
    # only as a registered marker contrast; a negative/nonreplicating result is
    # just as informative.
    strata={}
    for dialect in ("A","B"):
      for mod in ("@","+","*","none"):
        group=[r for r in rows if r["currier"]==dialect and r["locus"]=="P0" and r["modifier"]==mod]
        if len(group)>=50:
          s=summary(group);s.update(monte_carlo(group,args.permutations,args.seed+len(strata)))
          strata[f"Currier{dialect}_P0_modifier_{'none' if mod=='none' else mod}"]=s
    bkeys=[k for k in strata if k.startswith("CurrierB_")]
    akeys=[k for k in strata if k.startswith("CurrierA_")]
    for k,v in holm({k:strata[k]["p_one_sided_plus_one"] for k in bkeys}).items():
      strata[k]["p_holm_B_modifier_family"]=v
    for k,v in holm({k:strata[k]["p_one_sided_plus_one"] for k in akeys}).items():
      strata[k]["p_holm_A_modifier_family"]=v
    data={"experiment":"exp_593_daiin_line_metadata_contrast","protocol_version":1,
          "source":{"path":"data/transcriptions/eva_zl3b.txt","bytes":CORPUS.stat().st_size,"sha256":sha256(CORPUS)},
          "filters":{"dialects_separate":True,"locus":"P0","minimum_tokens_per_line":2,
                     "modifier_categories":["@","+","*","none"]},
          "total_parsed_lines":len(rows),"primary_strata":strata,
          "interpretation_note":"Prefix modifiers are treated as transcription metadata categories, not definitive paragraph-opening labels. Results are exploratory and cannot be interpreted semantically.",
          "guardrails":["Within-line token-inventory/length expectation.","P-values are Monte Carlo and Holm-adjusted within A/B modifier families.","Do not infer meaning or decipherment."]}
    out=ROOT/"experiments/exp_593_daiin_line_metadata_contrast/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),"primary_strata":strata},indent=2))

if __name__=="__main__": main()
