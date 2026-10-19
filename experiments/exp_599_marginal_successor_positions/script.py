#!/usr/bin/env python3
"""Compare marginal +1/+2 token distributions after initial daiin/dain/saiin."""
from __future__ import annotations
import argparse, collections, hashlib, json, math, random, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b",ROOT/"data/transcriptions/eva_zl3b.txt"),
       ("ZL3a",ROOT/"data/transcriptions/zl3a.txt")]
TARGETS=("daiin","dain","saiin")
PAIRDEFS=(("daiin","dain"),("daiin","saiin"),("dain","saiin"))

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
    rows=[];folio="unknown";currier="unknown"
    for raw in path.read_text(encoding="latin-1").splitlines():
        line=raw.strip()
        if not line or line.startswith("#"):continue
        if re.match(r"^<f\w+>.*\$",line):
            m=re.match(r"^<(f\w+)>",line)
            if m:folio=m.group(1)
            m=re.search(r"\$L=([AB])",line)
            if m:currier=m.group(1)
            continue
        m=re.match(r"^<([^>]+)>\s+(.*)$",line)
        if not m or "," not in m.group(1):continue
        locus_raw=m.group(1).split(",",1)[1]
        locus=re.sub(r"^[+*@=~&!/]*","",locus_raw)
        if locus!="P0" or currier!="B":continue
        words=clean_words(m.group(2))
        # Requiring 3 tokens makes offset +1 and +2 analyses use identical lines.
        if len(words)<3:continue
        if words[0] in TARGETS:
            rows.append({"folio":folio,"starter":words[0],"words":words})
    return rows

def dist(values):
    c=collections.Counter(values);n=len(values)
    return {k:v/n for k,v in c.items()} if n else {}

def jsd_bits(a,b):
    da,db=dist(a),dist(b)
    if not a or not b:return None
    total=0.0
    for token in set(da)|set(db):
        p,q=da.get(token,0),db.get(token,0);m=(p+q)/2
        if p:total+=0.5*p*math.log2(p/m)
        if q:total+=0.5*q*math.log2(q/m)
    return total

def top_tokens(values,topn):
    c=collections.Counter(values);n=len(values)
    return [{"token":t,"count":v,"proportion":round(v/n,5)} for t,v in c.most_common(topn)]

def holm(values):
    order=sorted(values.items(),key=lambda kv:kv[1]);out={};running=0.0;m=len(order)
    for i,(key,p) in enumerate(order):
        running=max(running,min(1.0,(m-i)*p));out[key]=round(running,6)
    return out

def permutation_test(a,b,n_perm,seed):
    observed=jsd_bits(a,b)
    pooled=list(a)+list(b);na=len(a);rng=random.Random(seed)
    ge=0;total=0.0
    for _ in range(n_perm):
        shuffled=pooled[:]
        rng.shuffle(shuffled)
        value=jsd_bits(shuffled[:na],shuffled[na:])
        total+=value
        ge+=value>=observed-1e-12
    return {"n_a":len(a),"n_b":len(b),"observed_jsd_bits":round(observed,6),
            "null_mean_jsd_bits":round(total/n_perm,6),
            "p_upper_tail_plus_one":round((ge+1)/(n_perm+1),6),
            "permutations":n_perm,"seed":seed}

def analyze(path,label,n_perm,seed,topn):
    rows=parse(path)
    summaries={};tests={}
    for offset in (1,2):
        groups={w:[r["words"][offset] for r in rows if r["starter"]==w] for w in TARGETS}
        for word,values in groups.items():
            summaries[f"offset_{offset}_{word}"]={
              "offset":offset,"starter":word,"n":len(values),
              "unique_successors":len(set(values)),"entropy_bits":round(-sum(p*math.log2(p) for p in dist(values).values() if p>0),5),
              "top_successors":top_tokens(values,topn)}
        for i,(a,b) in enumerate(PAIRDEFS):
            key=f"offset_{offset}_{a}_vs_{b}"
            tests[key]=permutation_test(groups[a],groups[b],n_perm,seed+offset*100+i)
    # Holm across all six planned hypotheses in this source.
    for key,p in holm({k:v["p_upper_tail_plus_one"] for k,v in tests.items()}).items():
        tests[key]["p_holm_six_test_family"]=p
    return {"transcription":label,"source":{"path":str(path.relative_to(ROOT)),
            "bytes":path.stat().st_size,"sha256":sha256(path)},
            "filters":{"currier":"B","locus":"P0","minimum_clean_tokens_per_line":3,
                       "same_lines_for_offset_1_and_offset_2":True},
            "eligible_starter_lines":len(rows),
            "starter_counts":{w:sum(r["starter"]==w for r in rows) for w in TARGETS},
            "marginal_successor_distributions":summaries,"pairwise_tests":tests}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--permutations",type=int,default=5000)
    ap.add_argument("--seed",type=int,default=59920261019)
    ap.add_argument("--top",type=int,default=15)
    args=ap.parse_args()
    if args.permutations<999:ap.error("--permutations must be >=999")
    versions=[analyze(path,label,args.permutations,args.seed+i*1000,args.top)
              for i,(label,path) in enumerate(FILES) if path.exists()]
    comparison={}
    if len(versions)==2:
        for key in versions[0]["pairwise_tests"]:
            a,b=versions[0]["pairwise_tests"][key],versions[1]["pairwise_tests"][key]
            comparison[key]={"ZL3b_jsd":a["observed_jsd_bits"],"ZL3a_jsd":b["observed_jsd_bits"],
             "ZL3b_adjusted_p":a["p_holm_six_test_family"],"ZL3a_adjusted_p":b["p_holm_six_test_family"]}
    data={"experiment":"exp_599_marginal_successor_positions",
          "protocol_version":1,"starter_forms":list(TARGETS),
          "positions":{"offset_1":"token immediately after starter","offset_2":"second token after starter"},
          "metric":"Jensen-Shannon divergence between marginal token distributions; pooled-label permutation preserves group sizes",
          "notes":["All 6 comparisons (3 starter pairs x 2 token offsets) Holm-adjusted together within each transcription.",
                   "No joint bigram collapse; each offset is analyzed as a marginal distribution.",
                   "P-values are Monte Carlo estimates, and nonsignificance is not equivalence.",
                   "Successor strings are literal EVA tokens; no semantic interpretation.",
                   "Permutation does not stratify by folio/section; local sequence differences are descriptive statistical properties only."],
          "versions":versions,"cross_transcription_comparison":comparison}
    out=ROOT/"experiments/exp_599_marginal_successor_positions/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),"cross_transcription_comparison":comparison,
      "tests":[{"transcription":v["transcription"],"tests":v["pairwise_tests"]} for v in versions]},indent=2))

if __name__=="__main__":main()
