#!/usr/bin/env python3
"""Test whether daiin's initial-position affinity is exceptional vs common-word controls."""
from __future__ import annotations
import argparse, hashlib, json, random, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b",ROOT/"data/transcriptions/eva_zl3b.txt"),
       ("ZL3a",ROOT/"data/transcriptions/zl3a.txt")]
TARGETS=("daiin","aiin","chedy","dain","saiin","qokaiin")

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
        if locus!="P0":continue
        words=clean_words(m.group(2))
        if len(words)<2:continue
        rows.append({"folio":folio,"currier":currier,"words":words})
    return rows

def holm(values):
    ordered=sorted(values.items(),key=lambda kv:kv[1]);out={};running=0.0;m=len(ordered)
    for i,(k,p) in enumerate(ordered):
        running=max(running,min(1.0,(m-i)*p));out[k]=round(running,6)
    return out

def analyze(path,label,n_perm,seed):
    rows=parse(path);out={}
    for di,dialect in enumerate(("A","B")):
        group=[r for r in rows if r["currier"]==dialect]
        if not group:continue
        obs={w:sum(r["words"][0]==w for r in group) for w in TARGETS}
        expected={w:sum(r["words"].count(w)/len(r["words"]) for r in group) for w in TARGETS}
        token_count={w:sum(r["words"].count(w) for r in group) for w in TARGETS}
        totals={w:0 for w in TARGETS};upper={w:0 for w in TARGETS};lower={w:0 for w in TARGETS}
        rng=random.Random(seed+di*100)
        for _ in range(n_perm):
            drawn={w:0 for w in TARGETS}
            for r in group:
                chosen=r["words"][rng.randrange(len(r["words"]))]
                if chosen in drawn:drawn[chosen]+=1
            for w in TARGETS:
                totals[w]+=drawn[w]
                upper[w]+=drawn[w]>=obs[w]
                lower[w]+=drawn[w]<=obs[w]
        dialect_results={}
        for w in TARGETS:
            dialect_results[w]={
                "lines":len(group),"token_count":token_count[w],
                "first_observed":obs[w],"first_expected":round(expected[w],5),
                "enrichment":round(obs[w]/expected[w],5) if expected[w] else None,
                "null_mean":round(totals[w]/n_perm,5),
                "p_upper_tail_plus_one":round((upper[w]+1)/(n_perm+1),6),
                "p_lower_tail_plus_one":round((lower[w]+1)/(n_perm+1),6),
                "permutations":n_perm,"seed":seed+di*100}
        for tail in ("upper","lower"):
            pfield=f"p_{tail}_tail_plus_one"
            adj=holm({w:dialect_results[w][pfield] for w in TARGETS})
            for w,val in adj.items():dialect_results[w][f"p_holm_{tail}_family"]=val
        out[dialect]=dialect_results
    return {"transcription":label,"source":{"path":str(path.relative_to(ROOT)),
            "bytes":path.stat().st_size,"sha256":sha256(path)},
            "eligible_P0_lines":len(rows),"by_dialect":out}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--permutations",type=int,default=5000)
    ap.add_argument("--seed",type=int,default=59620261019)
    args=ap.parse_args()
    if args.permutations<999:ap.error("--permutations must be >=999")
    versions=[analyze(path,label,args.permutations,args.seed+i*1000)
              for i,(label,path) in enumerate(FILES) if path.exists()]
    comparison={}
    if len(versions)==2:
        for dialect in ("A","B"):
            for word in TARGETS:
                a=versions[0]["by_dialect"].get(dialect,{}).get(word)
                b=versions[1]["by_dialect"].get(dialect,{}).get(word)
                if a and b:
                    comparison[f"{dialect}_{word}"]={
                      "ZL3b_enrichment":a["enrichment"],"ZL3a_enrichment":b["enrichment"],
                      "difference":round(b["enrichment"]-a["enrichment"],5),
                      "ZL3b_first":a["first_observed"],"ZL3a_first":b["first_observed"],
                      "ZL3b_holm_upper":a["p_holm_upper_family"],"ZL3a_holm_upper":b["p_holm_upper_family"]}
    data={"experiment":"exp_596_daiin_vs_common_word_position_controls","protocol_version":1,
          "targets":list(TARGETS),"primary_target":"daiin",
          "filters":{"locus":"P0","Currier_A_B_separate":True,"minimum_clean_tokens_per_line":2},
          "null":"Choose one uniformly random token position independently in every line, preserving each line's token inventory and length.",
          "versions":versions,"cross_transcription_comparison":comparison,
          "notes":["Control list frozen from prior exp_589 script; not selected after seeing results.",
                   "Holm correction applied across six targets separately for each transcription/dialect/tail family.",
                   "This test concerns word placement, not semantic identity or decipherment."]}
    out=ROOT/"experiments/exp_596_daiin_position_controls/results.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),"comparison":comparison,
                      "versions":versions},indent=2))

if __name__=="__main__":main()
