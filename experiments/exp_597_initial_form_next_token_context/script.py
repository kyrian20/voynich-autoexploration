#!/usr/bin/env python3
"""Next-token context comparison for initial daiin/dain/saiin in Currier-B P0."""
from __future__ import annotations
import argparse, collections, hashlib, json, math, random, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b",ROOT/"data/transcriptions/eva_zl3b.txt"),
       ("ZL3a",ROOT/"data/transcriptions/zl3a.txt")]
TARGETS=("daiin","dain","saiin")

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
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
        if len(words)<2:continue
        rows.append({"folio":folio,"words":words})
    return rows

def distribution(contexts):
    counts=collections.Counter(contexts);n=len(contexts)
    return {w:counts[w]/n for w in counts} if n else {}

def entropy_bits(contexts):
    d=distribution(contexts)
    return round(-sum(p*math.log2(p) for p in d.values() if p>0),5)

def jsd_bits(a,b):
    da,db=distribution(a),distribution(b)
    vocab=set(da)|set(db)
    if not a or not b:return None
    value=0.0
    for w in vocab:
        p,q=da.get(w,0.0),db.get(w,0.0);m=(p+q)/2
        if p>0:value+=0.5*p*math.log2(p/m)
        if q>0:value+=0.5*q*math.log2(q/m)
    return value

def top_counts(contexts,topn):
    c=collections.Counter(contexts);n=len(contexts)
    return [{"token":w,"count":v,"proportion":round(v/n,5)} for w,v in c.most_common(topn)]

def pair_test(a,b,n_perm,seed):
    observed=jsd_bits(a,b)
    pooled=list(a)+list(b);na=len(a)
    rng=random.Random(seed);ge=0;sumjsd=0.0
    for _ in range(n_perm):
        shuffled=pooled[:]
        rng.shuffle(shuffled)
        value=jsd_bits(shuffled[:na],shuffled[na:])
        sumjsd+=value
        ge+=value>=observed-1e-12
    return {"n_a":len(a),"n_b":len(b),"observed_jsd_bits":round(observed,6),
            "permutation_mean_jsd_bits":round(sumjsd/n_perm,6),
            "p_upper_tail_plus_one":round((ge+1)/(n_perm+1),6),
            "permutations":n_perm,"seed":seed}

def holm(values):
    ordered=sorted(values.items(),key=lambda x:x[1]);out={};running=0.0;m=len(ordered)
    for i,(k,p) in enumerate(ordered):
        running=max(running,min(1.0,(m-i)*p));out[k]=round(running,6)
    return out

def analyze(path,label,n_perm,seed,topn):
    rows=parse(path)
    groups={w:[r["words"][1] for r in rows if r["words"][0]==w] for w in TARGETS}
    context_summaries={}
    for word,ctx in groups.items():
        context_summaries[word]={"starting_lines":len(ctx),"unique_next_tokens":len(set(ctx)),
                                 "entropy_bits":entropy_bits(ctx),"top_next_tokens":top_counts(ctx,topn)}
    pairs={}
    pairdefs=[("daiin","dain"),("daiin","saiin"),("dain","saiin")]
    for i,(a,b) in enumerate(pairdefs):
        key=f"{a}_vs_{b}"
        pairs[key]=pair_test(groups[a],groups[b],n_perm,seed+i)
    adj=holm({k:v["p_upper_tail_plus_one"] for k,v in pairs.items()})
    for k,v in adj.items():pairs[k]["p_holm_three_pair_family"]=v
    # Descriptive all-other-start baseline; not included in the three primary tests.
    other=[r["words"][1] for r in rows if r["words"][0] not in TARGETS]
    each_vs_other={}
    for i,w in enumerate(TARGETS):
        each_vs_other[w]={"other_start_lines":len(other),"jsd_vs_other_start_context_bits":round(jsd_bits(groups[w],other),6),
                          "top_other_start_contexts":top_counts(other,topn)}
    return {"transcription":label,"source":{"path":str(path.relative_to(ROOT)),
            "bytes":path.stat().st_size,"sha256":sha256(path)},
            "currier_B_P0_lines":len(rows),"target_starter_counts":{w:sum(r["words"][0]==w for r in rows) for w in TARGETS},
            "successor_distributions":context_summaries,"pairwise_distribution_tests":pairs,
            "descriptive_vs_other_line_starts":each_vs_other}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--permutations",type=int,default=5000)
    ap.add_argument("--seed",type=int,default=59720261019)
    ap.add_argument("--top",type=int,default=15)
    args=ap.parse_args()
    if args.permutations<999:ap.error("--permutations must be >=999")
    versions=[analyze(path,label,args.permutations,args.seed+i*1000,args.top)
              for i,(label,path) in enumerate(FILES) if path.exists()]
    data={"experiment":"exp_597_initial_form_next_token_context","protocol_version":1,
          "primary_forms":list(TARGETS),
          "filters":{"currier":"B","locus":"P0","minimum_clean_tokens_per_line":2},
          "metric":"Jensen-Shannon divergence in bits between next-token distributions; pair-label permutation preserves group sizes",
          "notes":["The three primary pairwise comparisons are Holm-adjusted together within each transcription.",
                   "Successor words are literal EVA tokens; no semantic role is assumed.",
                   "Pairwise permutation assumes successor labels exchangeable under the null and does not stratify by folio; this limits causal/grammatical interpretation.",
                   "All-other-start comparison is descriptive and not part of the corrected primary family.",
                   "Nonsignificance does not prove equivalent distributions. No decipherment inference."],
          "versions":versions}
    out=ROOT/"experiments/exp_597_initial_form_next_token_context/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),
                      "versions":[{"transcription":v["transcription"],
                         "groups":v["successor_distributions"],"pairs":v["pairwise_distribution_tests"]} for v in versions]},indent=2))

if __name__=="__main__":main()
