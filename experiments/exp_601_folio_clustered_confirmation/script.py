#!/usr/bin/env python3
"""Predeclared Currier-B/P0 daiin initial-position test with folio-cluster bootstrap."""
from __future__ import annotations
import argparse, collections, hashlib, json, random, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CORPUS=ROOT/"data/transcriptions/eva_zl3b.txt"
SEED=60120261019
FAMILY="single primary endpoint: Currier B, P0 body locus, >=2 cleaned EVA tokens; first token exactly daiin"

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""): h.update(block)
    return h.hexdigest()

def clean_words(text):
    text=re.sub(r"<!.*?>"," ",text)
    text=re.sub(r"<[^>]*>"," ",text)
    text=re.sub(r"\[([^:\]]+):[^\]]*\]",r"\1",text)
    text=re.sub(r"\{[^}]*\}"," ",text)
    text=re.sub(r"@\d+;?"," ",text)
    return [w.lower() for w in re.split(r"[.\s,]+",text) if re.fullmatch(r"[A-Za-z]+",w)]

def parse(path):
    rows=[]; folio="unknown"; currier="unknown"
    for line_no,raw in enumerate(path.read_text(encoding="latin-1").splitlines(),1):
        line=raw.strip()
        if not line or line.startswith("#"): continue
        if re.match(r"^<f\w+>.*\$",line):
            m=re.match(r"^<(f\w+)>",line)
            if m: folio=m.group(1)
            m=re.search(r"\$L=([AB])",line)
            currier=m.group(1) if m else "unknown"
            continue
        m=re.match(r"^<([^>]+)>\s+(.*)$",line)
        if not m or "," not in m.group(1): continue
        ident,body=m.groups()
        slot=ident.split(",",1)[1]
        normalized=re.sub(r"^[+*@=~&!/]+","",slot)
        if normalized!="P0" or currier!="B": continue
        words=clean_words(body)
        if len(words)<2: continue
        rows.append({"folio":folio,"line":line_no,"words":words,
                     "observed":int(words[0]=="daiin"),
                     "expected":words.count("daiin")/len(words)})
    return rows

def quantile(values,q):
    s=sorted(values)
    if not s:return None
    x=(len(s)-1)*q;lo=int(x);hi=min(lo+1,len(s)-1);w=x-lo
    return s[lo]*(1-w)+s[hi]*w

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bootstrap",type=int,default=20000)
    ap.add_argument("--permutations",type=int,default=20000)
    ap.add_argument("--seed",type=int,default=SEED)
    args=ap.parse_args()
    if args.bootstrap<1000 or args.permutations<1000: ap.error("bootstrap and permutations must each be >=1000")
    rows=parse(CORPUS)
    if not rows: raise SystemExit("No eligible Currier-B P0 rows parsed")
    folio_rows=collections.defaultdict(list)
    for r in rows: folio_rows[r["folio"]].append(r)
    folios=sorted(folio_rows)
    observed=sum(r["observed"] for r in rows)
    expected=sum(r["expected"] for r in rows)
    ratio=observed/expected if expected else None
    target=sum(r["words"].count("daiin") for r in rows)
    by_folio={}
    for f,rs in folio_rows.items():
        by_folio[f]={"lines":len(rs),"observed":sum(r["observed"] for r in rs),
                     "expected":sum(r["expected"] for r in rs),
                     "tokens":sum(r["words"].count("daiin") for r in rs)}
    rng=random.Random(args.seed)
    # Cluster bootstrap: resample folios, not individual lines. The primary statistic is
    # sum of observed initial hits / sum of line-inventory expected hits.
    boot=[]
    for _ in range(args.bootstrap):
        num=den=0.0
        for _j in range(len(folios)):
            f=folios[rng.randrange(len(folios))]
            num+=by_folio[f]["observed"]; den+=by_folio[f]["expected"]
        if den: boot.append(num/den)
    ci=[quantile(boot,.025),quantile(boot,.975)]
    # Conditional randomization null: one uniformly chosen token position per eligible
    # line; retains each line's token inventory/length and observed folio grouping.
    ge=0; null_sum=0.0
    for _ in range(args.permutations):
        count=0
        for r in rows:
            if r["words"][rng.randrange(len(r["words"]))]=="daiin": count+=1
        null_sum+=count
        ge+=count>=observed
    p=(ge+1)/(args.permutations+1)
    loo=[]
    for f in folios:
        n=observed-by_folio[f]["observed"]
        d=expected-by_folio[f]["expected"]
        loo.append({"folio":f,"observed":n,"expected":round(d,6),"enrichment":round(n/d,6) if d else None})
    loo_ratios=[x["enrichment"] for x in loo if x["enrichment"] is not None]
    data={
      "experiment":"exp_601_folio_clustered_confirmation","protocol_version":1,
      "status":"confirmatory statistical test of a pre-existing positional observation; not a decipherment test",
      "preregistered_primary_family":FAMILY,
      "source":{"path":"data/transcriptions/eva_zl3b.txt","bytes":CORPUS.stat().st_size,"sha256":digest(CORPUS)},
      "parser":{"folio Currier label read from $L=A/B header field","locus":"remove one leading IVTFF locator then require exact P0","minimum_clean_tokens":2,"target":"literal cleaned EVA token daiin"},
      "sample":{"eligible_lines":len(rows),"represented_folios":len(folios),"daiin_tokens":target,
                "observed_line_initial":observed,"line_inventory_expected":round(expected,6)},
      "primary_effect":{"enrichment_ratio":round(ratio,6),"excess_initial_hits":round(observed-expected,6),
                        "folio_cluster_bootstrap_ci95_percentile":[round(ci[0],6),round(ci[1],6)],
                        "bootstrap_replicates":len(boot),"bootstrap_seed":args.seed},
      "conditional_randomization_test":{"null":"independently choose one uniformly random token position within each eligible line; each line's inventory/length preserved",
        "observed_count":observed,"null_mean":round(null_sum/args.permutations,6),
        "p_one_sided_plus_one":round(p,7),"permutations":args.permutations,"seed":args.seed,
        "interpretation":"The p-value tests within-line positional exchangeability; the cluster bootstrap interval describes sensitivity to which folios are sampled. They answer different questions."},
      "leave_one_folio_out":{"minimum_enrichment":round(min(loo_ratios),6),"maximum_enrichment":round(max(loo_ratios),6),
                             "all_folios":loo},
      "limitations":["The bootstrap resamples folios equally as clusters; it does not assert folios are identically distributed.",
        "The randomization null conditions on each observed line's token inventory and length; it does not model all text-generating dependencies.",
        "ZL3a is a related transcription, not an independent manuscript sample.",
        "Currier labels and locus parsing are transcription metadata; the audit is not a full official IVTFF validation.",
        "A positional enrichment is not evidence of a semantic meaning or a decipherment."],
      "next_decision_rule":"Treat the positional effect as robust to folio sampling only if the 95% folio-cluster bootstrap interval excludes 1 and leave-one-folio-out ratios remain above 1; report the randomization p-value separately. If criteria disagree, mark inference mixed rather than choosing the favorable test."}
    out=ROOT/"experiments/exp_601_folio_clustered_confirmation/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),"sample":data["sample"],
      "primary_effect":data["primary_effect"],"randomization":data["conditional_randomization_test"],
      "leave_one_folio_out":{k:v for k,v in data["leave_one_folio_out"].items() if k!="all_folios"}},indent=2))

if __name__=="__main__":main()
