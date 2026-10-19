#!/usr/bin/env python3
"""Test actual IVTFF <%> paragraph-start comments for line-initial daiin."""
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
    # Remove comments/tags only after paragraph marker presence has been recorded.
    text=re.sub(r"<!.*?>"," ",text)
    text=re.sub(r"<[^>]*>"," ",text)
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
        meta=m.group(1)
        locus_raw=meta.split(",",1)[1]
        locus=re.sub(r"^[+*@]","",locus_raw)
        if locus!="P0": continue
        body=m.group(2)
        # IVTFF specifies <%> as paragraph start and <$> as paragraph end.
        # Capture only a marker attached to the current line before cleaning.
        paragraph_start="<%>" in body
        words=clean_words(body)
        if len(words)<2: continue
        rows.append({"folio":folio,"currier":currier,"paragraph_start":paragraph_start,
                     "words":words,"line_id":meta})
    return rows

def stats(rows):
    obs=sum(r["words"][0]=="daiin" for r in rows)
    exp=sum(r["words"].count("daiin")/len(r["words"]) for r in rows)
    return {"lines":len(rows),"daiin_tokens":sum(r["words"].count("daiin") for r in rows),
            "first_observed":obs,"first_expected":round(exp,6),
            "enrichment":round(obs/exp,6) if exp else None,
            "last_observed":sum(r["words"][-1]=="daiin" for r in rows)}

def perm_test(rows,n,seed,tail):
    obs=sum(r["words"][0]=="daiin" for r in rows)
    rng=random.Random(seed); extreme=0; vals=[]
    for _ in range(n):
        x=sum(r["words"][rng.randrange(len(r["words"]))]=="daiin" for r in rows)
        vals.append(x)
        extreme += x>=obs if tail=="upper" else x<=obs
    return {"tail":tail,"p_plus_one":round((extreme+1)/(n+1),6),
            "null_mean":round(sum(vals)/n,6),"permutations":n,"seed":seed}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--permutations",type=int,default=10000)
    ap.add_argument("--seed",type=int,default=59420261019)
    args=ap.parse_args()
    if args.permutations<999: ap.error("--permutations must be >=999")
    rows=parse(CORPUS)
    strata={}
    for dialect in ("A","B"):
      for opener in (True,False):
        group=[r for r in rows if r["currier"]==dialect and r["paragraph_start"]==opener]
        if len(group)>=20:
          key=f"Currier{dialect}_{'paragraph_opening' if opener else 'continuation'}"
          s=stats(group)
          s["upper_tail"]=perm_test(group,args.permutations,args.seed+(1 if dialect=="A" else 11)+(0 if opener else 100),"upper")
          s["lower_tail"]=perm_test(group,args.permutations,args.seed+(1 if dialect=="A" else 11)+(0 if opener else 100),"lower")
          strata[key]=s
    bstart=strata.get("CurrierB_paragraph_opening",{})
    bcont=strata.get("CurrierB_continuation",{})
    # Direct difference in rates is tested by shuffling paragraph labels among B/P0 lines,
    # preserving group sizes, and measuring difference in first-token indicator rates.
    b=[r for r in rows if r["currier"]=="B"]
    opens=[r for r in b if r["paragraph_start"]]
    cont=[r for r in b if not r["paragraph_start"]]
    obs_rate=(sum(r["words"][0]=="daiin" for r in opens)/len(opens) if opens else 0) - (sum(r["words"][0]=="daiin" for r in cont)/len(cont) if cont else 0)
    rng=random.Random(args.seed+594)
    pool=[r["words"][0]=="daiin" for r in b]
    ge=le=0
    for _ in range(args.permutations):
      rng.shuffle(pool)
      x=sum(pool[:len(opens)])/len(opens) - sum(pool[len(opens):])/len(cont) if opens and cont else 0
      ge+=x>=obs_rate; le+=x<=obs_rate
    data={"experiment":"exp_594_daiin_paragraph_start","protocol_version":1,
      "source":{"path":"data/transcriptions/eva_zl3b.txt","bytes":CORPUS.stat().st_size,"sha256":sha256(CORPUS)},
      "format_reference":"https://voynich.nu/software/ivtt/IVTFF_format.pdf (section 6.9; <%> starts a paragraph, <$> ends one)",
      "filters":{"locus":"P0","minimum_clean_tokens_per_line":2,"currier_classes_separate":True},
      "total_parsed_P0_lines":len(rows),"paragraph_marker_lines":sum(r["paragraph_start"] for r in rows),
      "strata":strata,
      "currier_B_direct_rate_difference":{"paragraph_opening_minus_continuation":round(obs_rate,8),
        "paragraph_opening_lines":len(opens),"continuation_lines":len(cont),
        "p_upper_plus_one":round((ge+1)/(args.permutations+1),6),
        "p_lower_plus_one":round((le+1)/(args.permutations+1),6),
        "permutations":args.permutations,"seed":args.seed+594},
      "guardrails":["Paragraph opener is assigned only by literal <%> in raw body, not @/+/* locator symbols.",
        "Within-stratum expected counts preserve line token inventory and length.",
        "Direct rate-difference permutation is descriptive conditional on observed first-token indicators; it is not a decipherment.",
        "Single transcript ZL3b; no semantic inference."]}
    out=ROOT/"experiments/exp_594_daiin_paragraph_start/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),"paragraph_marker_lines":data["paragraph_marker_lines"],"strata":strata,"B_direct":data["currier_B_direct_rate_difference"]},indent=2))

if __name__=="__main__": main()
