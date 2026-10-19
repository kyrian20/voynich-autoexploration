#!/usr/bin/env python3
"""exp607: held-out next-token prediction with a preregistered bigram model."""
import hashlib, json, math, random, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = [("ZL3b","data/transcriptions/eva_zl3b.txt"),("IT2a","data/transcriptions/eva_it2a.txt")]
ALPHA = 0.1
BIGRAM_WEIGHT = 0.5
TEST_MOD = 5
TOKEN_RE = re.compile(r"[a-z]{2,}")
ROW_RE = re.compile(r"^<(f\d+[rv])\.\d+,[^>]*>\s*(.*)$")
FOLIO_RE = re.compile(r"^<(f\d+[rv])>")

def load(label, rel):
    path=ROOT/rel
    pages={}
    for line in path.read_text(encoding="latin-1").splitlines():
        # Do not include page headers, comments, labels or cross-line transitions.
        m=ROW_RE.match(line.strip())
        if not m: continue
        folio, body=m.groups()
        # Remove common IVTFF editorial annotation forms before tokenization.
        body=re.sub(r"<[^>]*>|\{[^}]*\}|\[[^]]*\]|\$[^ ]*|@\d+;?", " ", body)
        toks=TOKEN_RE.findall(body.lower())
        if len(toks)>=2: pages.setdefault(folio,[]).append(toks)
    train=[]; test=[]
    for folio, lines in sorted(pages.items()):
        bucket=int(hashlib.sha256(folio.encode()).hexdigest()[:8],16)%TEST_MOD
        (test if bucket==0 else train).append((folio,lines))
    return {"label":label,"path":rel,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
            "train":train,"test":test}

def counts(groups):
    uni=Counter(); bi=Counter(); prev=Counter(); total=0; vocab=set()
    for _,lines in groups:
        for line in lines:
            uni.update(line); vocab.update(line); total+=len(line)
            for a,b in zip(line,line[1:]):
                bi[(a,b)]+=1; prev[a]+=1
    return uni,bi,prev,total,vocab

def score(train_groups, test_groups, shuffled=False):
    if shuffled:
        rng=random.Random(6072026)
        altered=[]
        for folio,lines in train_groups:
            new=[]
            for line in lines:
                x=line[:]; rng.shuffle(x); new.append(x)
            altered.append((folio,new))
        train_groups=altered
    uni,bi,prev,total,vocab=counts(train_groups)
    V=max(1,len(vocab))
    # Unknown test tokens get a single UNK bucket with additive smoothing.
    def p_uni(w):
        return (uni[w]+ALPHA)/(total+ALPHA*(V+1))
    def p_bigram(a,w):
        denom=prev[a]+ALPHA*(V+1)
        return (bi[(a,w)]+ALPHA)/denom
    loss_u=loss_mix=loss_bg=0.0; n=0
    for _,lines in test_groups:
        for line in lines:
            for i in range(1,len(line)):
                a,w=line[i-1],line[i]
                pu=p_uni(w)
                pb=p_bigram(a,w)
                pm=(1-BIGRAM_WEIGHT)*pu+BIGRAM_WEIGHT*pb
                loss_u-=math.log2(pu); loss_bg-=math.log2(pb); loss_mix-=math.log2(pm); n+=1
    return {"tokens_scored":n,"unigram_bits_per_token":loss_u/max(1,n),
            "bigram_only_bits_per_token":loss_bg/max(1,n),
            "interpolated_bits_per_token":loss_mix/max(1,n),
            "gain_vs_unigram_bits_per_token":(loss_u-loss_mix)/max(1,n),
            "train_vocabulary":V,"train_tokens":total}

def main():
    results=[]
    for label,rel in FILES:
        d=load(label,rel)
        train,test=d.pop("train"),d.pop("test")
        real=score(train,test)
        shuffled=score(train,test,shuffled=True)
        d.update({"split":"deterministic folio SHA256 first-32-bit modulo 5; bucket 0 held out",
          "train_folios":len(train),"test_folios":len(test),
          "train_lines":sum(len(x[1]) for x in train),"test_lines":sum(len(x[1]) for x in test),
          "real_sequence":real,"shuffled_train_control":shuffled,
          "control_gain_vs_unigram":shuffled["gain_vs_unigram_bits_per_token"],
          "real_minus_shuffled_gain":real["gain_vs_unigram_bits_per_token"]-shuffled["gain_vs_unigram_bits_per_token"]})
        results.append(d)
    out={"experiment":"exp_607_heldout_bigram_prediction","preregistered_parameters":{"test_modulo":TEST_MOD,"alpha":ALPHA,"bigram_interpolation_weight":BIGRAM_WEIGHT,"token_pattern":"[a-z]{2,}","score":"bits per next token, transitions never cross line boundaries"},
      "scope":"Tests whether previous-token context improves next-token prediction on unseen folios beyond a unigram baseline. Transcriptions are not independent witnesses; this is a structural-language test, not a decipherment.",
      "sources":results}
    dest=ROOT/"experiments/exp_607_heldout_bigram_prediction"; dest.mkdir(parents=True,exist_ok=True)
    (dest/"results.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    lines=["# exp_607 — Held-out next-token prediction","","## Question","Does the immediately previous token improve next-token prediction on unseen folios beyond unigram frequencies? This is a modest test of local sequential structure, not an attempt to assign meanings.","","## Preregistered method","- Split by folio using SHA-256 of folio label, modulo 5; bucket 0 is test. The same split rule is applied independently within each transcription.","- Train a unigram baseline and an interpolated bigram model (50% unigram + 50% smoothed bigram; additive alpha=0.1). Score only within-line transitions, never across line boundaries.","- Negative control: shuffle token order within every training line using a fixed random seed, preserving each training line's token inventory but destroying its original order.","- Metric: held-out bits per next token. Positive gain versus unigram means lower log loss. Compare real-order gain with shuffled-control gain.","- Limitations: simple regex tokenization may include transliteration artefacts; repeated/related transcriptions are not independent witnesses; no semantic interpretation is tested."]
    for d in results:
        r=d["real_sequence"]; s=d["shuffled_train_control"]
        lines += ["",f"## {d['label']}","",f"- Source SHA-256: {d['sha256']}",f"- Train/test folios: {d['train_folios']} / {d['test_folios']}; lines: {d['train_lines']} / {d['test_lines']}; scored transitions: {r['tokens_scored']}.",
          f"- Real order: unigram {r['unigram_bits_per_token']:.5f} bits/token; interpolated bigram {r['interpolated_bits_per_token']:.5f}; gain {r['gain_vs_unigram_bits_per_token']:.5f}.",
          f"- Shuffled-training control: interpolated {s['interpolated_bits_per_token']:.5f}; gain vs unigram {s['gain_vs_unigram_bits_per_token']:.5f}.",
          f"- Real-minus-shuffled gain: {d['real_minus_shuffled_gain']:.5f} bits/token."]
    lines += ["","## Interpretation rule","","A positive gain indicates local token order helps prediction on held-out folios under this tokenizer/model; it does not establish that the text is natural language or that any token has a known meaning. A gain similar to the shuffled control is weak evidence because token inventories and model smoothing can produce apparent improvements. A negative gain means this fixed bigram model did not beat the unigram baseline. Do not tune on the held-out folios; any follow-up must be a new preregistered test."]
    (dest/"result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__": main()
