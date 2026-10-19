import collections, hashlib, json, math, random, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "data/transcriptions/eva_zl3b.txt"
SEED = 60320261019
TARGETS = ("daiin", "dain", "saiin")
BINS = ((2, 5, "2-4"), (5, 8, "5-7"), (8, 10**9, "8+"))
ALPHA = 1.0  # Beta(1,1) smoothing, fixed before evaluation

def clean(s):
    s = re.sub(r"<!.*?>|<[^>]*>", " ", s)
    s = re.sub(r"\[([^:\]]+):[^\]]*\]", r"\1", s)
    s = re.sub(r"\{[^}]*\}|@\d+;?", " ", s)
    return [w.lower() for w in re.split(r"[.\s,]+", s) if re.fullmatch(r"[A-Za-z]+", w)]

def parse():
    rows, folio, dialect = [], "unknown", "unknown"
    for line in CORPUS.read_text(encoding="latin-1").splitlines():
        s = line.strip()
        if not s or s.startswith("#"): continue
        if re.match(r"^<f\w+>.*\$", s):
            m = re.match(r"^<(f\w+)>", s)
            if m: folio = m.group(1)
            m = re.search(r"\$L=([AB])", s)
            dialect = m.group(1) if m else "unknown"
            continue
        m = re.match(r"^<([^>]+)>\s+(.*)$", s)
        if not m or "," not in m.group(1): continue
        slot = m.group(1).split(",", 1)[1]
        if re.sub(r"^[+*@=~&!/]+", "", slot) != "P0" or dialect not in ("A", "B"): continue
        words = clean(m.group(2))
        if len(words) < 2: continue
        held = int(hashlib.sha256(("voynich-exp602:" + folio).encode()).hexdigest()[:8], 16) % 5 == 0
        rows.append({"folio":folio,"dialect":dialect,"words":words,"held":bool(held)})
    return rows

def logloss(y,p):
    p = min(max(p, 1e-6), 1-1e-6)
    return -(y*math.log(p)+(1-y)*math.log(1-p))

def bin_name(n):
    return next(name for lo,hi,name in BINS if lo <= n < hi)

def main():
    rows = parse()
    train, test = [r for r in rows if not r["held"]], [r for r in rows if r["held"]]
    if len(train) < 1000 or len(test) < 100: raise SystemExit("Unexpected train/test size")
    out = {"experiment":"exp_603","seed_split":"same folio hash rule as exp_602","bins":[{"min":a,"max_exclusive":b,"name":n} for a,b,n in BINS],
           "smoothing":"Beta(1,1), applied to each training stratum", "train_lines":len(train),"test_lines":len(test),
           "train_folios":len(set(r["folio"] for r in train)),"test_folios":len(set(r["folio"] for r in test)),"targets":{}}
    for target in TARGETS:
        global_p = (sum(r["words"][0] == target for r in train)+ALPHA)/(len(train)+2*ALPHA)
        strata = collections.defaultdict(list)
        for r in train: strata[(r["dialect"],bin_name(len(r["words"])))].append(r)
        probs = {k:(sum(r["words"][0] == target for r in v)+ALPHA)/(len(v)+2*ALPHA) for k,v in strata.items()}
        records=[]
        for r in test:
            y=int(r["words"][0] == target)
            key=(r["dialect"],bin_name(len(r["words"])))
            p=probs.get(key,global_p)
            records.append((r["folio"],y,logloss(y,global_p),logloss(y,p),(y-global_p)**2,(y-p)**2,key))
        gain=sum(a-b for _,_,a,b,_,_,_ in records)/len(records) # positive favors stratified model
        brier_gain=sum(a-b for _,_,_,_,a,b,_ in records)/len(records)
        by_stratum={}
        for key in sorted(set(x[6] for x in records)):
            rs=[x for x in records if x[6]==key]
            by_stratum[f"{key[0]}:{key[1]}"]={"n":len(rs),"hits":sum(x[1] for x in rs),
                "global_log_loss":sum(x[2] for x in rs)/len(rs),"stratified_log_loss":sum(x[3] for x in rs)/len(rs)}
        # Paired folio-cluster bootstrap, resampling whole held-out folios
        grouped=collections.defaultdict(list)
        for x in records: grouped[x[0]].append(x[2]-x[3])
        folios=sorted(grouped); rng=random.Random(SEED+TARGETS.index(target)); boots=[]
        for _ in range(10000):
            vals=[]
            for _ in folios: vals.extend(grouped[folios[rng.randrange(len(folios))]])
            boots.append(sum(vals)/len(vals))
        boots.sort()
        out["targets"][target]={"train_global_probability":global_p,"test_initial_hits":sum(x[1] for x in records),
            "test_folios":len(folios),"global_log_loss":sum(x[2] for x in records)/len(records),
            "stratified_log_loss":sum(x[3] for x in records)/len(records),"log_loss_gain_global_minus_stratified":gain,
            "folio_cluster_bootstrap_95pct":[boots[int(.025*len(boots))],boots[int(.975*len(boots))]],
            "brier_gain_global_minus_stratified":brier_gain,"strata":by_stratum}
    (ROOT/"experiments/exp_603_stratified_heldout_prediction").mkdir(parents=True,exist_ok=True)
    p=ROOT/"experiments/exp_603_stratified_heldout_prediction/results.json"
    p.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    md=["# exp_603 — Stratified held-out prediction","",
        "Frozen split: same deterministic folio-hash rule as exp_602. Population: ZL3b, Currier A/B, P0, at least two clean tokens. Features at prediction time: Currier class and line-length bin only. Fixed bins: 2–4, 5–7, 8+ tokens. Each training stratum uses Beta(1,1) smoothing. No held-out target counts are used to estimate probabilities.","",
        f"Train: {len(train)} lines / {out['train_folios']} folios. Test: {len(test)} lines / {out['test_folios']} folios.","",
        "Positive log-loss gain means stratified model beats global train-only model. Positive Brier gain also favors stratified model.",""]
    for t,v in out["targets"].items():
        md += [f"## {t}","",f"- Held-out initial hits: {v['test_initial_hits']}",
               f"- Global log loss: {v['global_log_loss']:.6f}; stratified: {v['stratified_log_loss']:.6f}",
               f"- Log-loss gain: {v['log_loss_gain_global_minus_stratified']:.6f}; folio-bootstrap 95% CI [{v['folio_cluster_bootstrap_95pct'][0]:.6f}, {v['folio_cluster_bootstrap_95pct'][1]:.6f}]",
               f"- Brier gain: {v['brier_gain_global_minus_stratified']:.6f}",""]
    md += ["## Interpretation","", "This tests out-of-sample prediction, not decipherment. Controls are descriptive and should not be treated as independent confirmatory tests. The split and bins were fixed before evaluation. Missing train strata back off to the global rate.",""]
    (p.parent/"result.md").write_text("\n".join(md),encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__ == "__main__": main()
