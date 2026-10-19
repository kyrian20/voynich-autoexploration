#!/usr/bin/env python3
"""Two-token successor-context test for Currier-B P0 daiin/dain/saiin starters."""
from __future__ import annotations
import argparse, collections, hashlib, json, math, random, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b",ROOT/"data/transcriptions/eva_zl3b.txt"),
       ("ZL3a",ROOT/"data/transcriptions/zl3a.txt")]
TARGETS=("daiin","dain","saiin")
RARE_PAIR_THRESHOLD=2

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
        if len(words)<3:continue
        if words[0] in TARGETS:
            rows.append({"folio":folio,"starter":words[0],"pair":(words[1],words[2])})
    return rows

def distribution(values):
    counts=collections.Counter(values);n=len(values)
    return {k:v/n for k,v in counts.items()} if n else {}

def jsd_bits(a,b):
    da,db=distribution(a),distribution(b)
    if not a or not b:return None
    value=0.0
    for token in set(da)|set(db):
        p,q=da.get(token,0.0),db.get(token,0.0);m=(p+q)/2
        if p>0:value+=0.5*p*math.log2(p/m)
        if q>0:value+=0.5*q*math.log2(q/m)
    return value

def top_contexts(contexts,topn):
    counts=collections.Counter(contexts);n=len(contexts)
    return [{"pair":list(pair) if isinstance(pair,tuple) else pair,
             "count":count,"proportion":round(count/n,5)}
            for pair,count in counts.most_common(topn)]

def holm(values):
    ordered=sorted(values.items(),key=lambda item:item[1]);out={};running=0.0;m=len(ordered)
    for i,(key,p) in enumerate(ordered):
        running=max(running,min(1.0,(m-i)*p));out[key]=round(running,6)
    return out

def permutation_test(a,b,n_perm,seed):
    observed=jsd_bits(a,b)
    pooled=list(a)+list(b);na=len(a);rng=random.Random(seed)
    ge=0;sum_null=0.0
    for _ in range(n_perm):
        shuffled=pooled[:]
        rng.shuffle(shuffled)
        value=jsd_bits(shuffled[:na],shuffled[na:])
        sum_null+=value
        ge+=value>=observed-1e-12
    return {"n_a":len(a),"n_b":len(b),"observed_jsd_bits":round(observed,6),
            "null_mean_jsd_bits":round(sum_null/n_perm,6),
            "p_upper_tail_plus_one":round((ge+1)/(n_perm+1),6),
            "permutations":n_perm,"seed":seed}

def analyze(path,label,n_perm,seed,topn):
    rows=parse(path)
    raw_groups={word:[r["pair"] for r in rows if r["starter"]==word] for word in TARGETS}
    pooled_counts=collections.Counter(pair for values in raw_groups.values() for pair in values)
    # Frozen, pooled support threshold: a pair observed only once in this combined
    # three-group sample is placed in one explicit rare-context category.
    groups={word:[pair if pooled_counts[pair]>=RARE_PAIR_THRESHOLD else ("<RARE_PAIR>","<RARE_PAIR>")
                  for pair in values] for word,values in raw_groups.items()}
    context_summary={}
    for word in TARGETS:
        values=groups[word]
        raw=raw_groups[word]
        rare=sum(pooled_counts[pair]<RARE_PAIR_THRESHOLD for pair in raw)
        context_summary[word]={
          "starter_lines":len(values),"unique_raw_pairs":len(set(raw)),
          "unique_after_rare_pair_collapse":len(set(values)),
          "rare_pairs_collapsed_lines":rare,"rare_pair_line_fraction":round(rare/len(raw),5) if raw else None,
          "top_raw_two_token_contexts":top_contexts(raw,topn),
          "top_collapsed_contexts":top_contexts(values,topn),
          "entropy_collapsed_bits":round(-sum(p*math.log2(p) for p in distribution(values).values() if p>0),5)}
    pairs={}
    pairdefs=[("daiin","dain"),("daiin","saiin"),("dain","saiin")]
    for i,(a,b) in enumerate(pairdefs):
        pairs[f"{a}_vs_{b}"]=permutation_test(groups[a],groups[b],n_perm,seed+i)
    for key,p in holm({k:v["p_upper_tail_plus_one"] for k,v in pairs.items()}).items():
        pairs[key]["p_holm_three_pair_family"]=p
    return {"transcription":label,
      "source":{"path":str(path.relative_to(ROOT)),"bytes":path.stat().st_size,"sha256":sha256(path)},
      "filter":{"currier":"B","locus":"P0","minimum_clean_tokens_per_line":3},
      "eligible_starter_lines":len(rows),"starter_counts":{w:len(raw_groups[w]) for w in TARGETS},
      "rare_pair_rule":{"minimum pooled frequency to retain pair":RARE_PAIR_THRESHOLD,
                        "otherwise":"collapse to <RARE_PAIR> + <RARE_PAIR> across all three starter groups"},
      "two_token_context_summary":context_summary,"pairwise_tests":pairs}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--permutations",type=int,default=5000)
    ap.add_argument("--seed",type=int,default=59820261019)
    ap.add_argument("--top",type=int,default=15)
    args=ap.parse_args()
    if args.permutations<999:ap.error("--permutations must be >=999")
    versions=[analyze(path,label,args.permutations,args.seed+i*1000,args.top)
              for i,(label,path) in enumerate(FILES) if path.exists()]
    comparison={}
    if len(versions)==2:
        for word in TARGETS:
            a=versions[0]["two_token_context_summary"][word]
            b=versions[1]["two_token_context_summary"][word]
            comparison[word]={
              "ZL3b_lines":a["starter_lines"],"ZL3a_lines":b["starter_lines"],
              "ZL3b_rare_pair_fraction":a["rare_pair_line_fraction"],
              "ZL3a_rare_pair_fraction":b["rare_pair_line_fraction"],
              "ZL3b_unique_raw_pairs":a["unique_raw_pairs"],"ZL3a_unique_raw_pairs":b["unique_raw_pairs"]}
        for key in versions[0]["pairwise_tests"]:
            comparison[key]={
              "ZL3b_jsd":versions[0]["pairwise_tests"][key]["observed_jsd_bits"],
              "ZL3a_jsd":versions[1]["pairwise_tests"][key]["observed_jsd_bits"],
              "ZL3b_adjusted_p":versions[0]["pairwise_tests"][key]["p_holm_three_pair_family"],
              "ZL3a_adjusted_p":versions[1]["pairwise_tests"][key]["p_holm_three_pair_family"]}
    data={"experiment":"exp_598_two_token_successor_context","protocol_version":1,
      "primary_forms":list(TARGETS),"rare_pair_threshold":RARE_PAIR_THRESHOLD,
      "metric":"Jensen-Shannon divergence between two-token successor-pair distributions; pooled-label permutation preserves group sizes",
      "notes":["Rare-pair collapse threshold (pooled frequency <2) predeclared before result inspection.",
               "Three pairwise tests Holm-adjusted within each transcription.",
               "ZL3a and ZL3b have similar underlying transcription rows, so agreement is version robustness not independent-sample replication.",
               "Position/context distribution only; no semantic interpretation.",
               "Permutation does not stratify by folio and cannot rule out folio/section confounding."],
      "versions":versions,"cross_transcription_comparison":comparison}
    out=ROOT/"experiments/exp_598_two_token_successor_context/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),"comparison":comparison,
      "pairwise_tests":[{"transcription":v["transcription"],"pairs":v["pairwise_tests"]} for v in versions]},indent=2))

if __name__=="__main__":main()
