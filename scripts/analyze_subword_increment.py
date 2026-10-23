#!/usr/bin/env python3
"""Matched-target exploratory comparison; see the frozen protocol."""
from collections import Counter, defaultdict
import argparse
import hashlib
import json
import random
from pathlib import Path
from analyze_subword_boundary import BPE, Predictor, pairs, score, synthetic_checks, bucket, quantile, INPUT, ROOT

PACKAGE = ROOT/'research/analysis/2026-10-23-subword-increment'

class CharacterContext:
    def __init__(self, bpe):
        self.bpe = bpe
        self.units = bpe.units

    def encode(self, word):
        units = self.bpe.encode(word)
        # Coarsen the learned boundary unit; preserve the entire target unit.
        last = units[-1][-1] if units[-1] != '<UNKNOWN_CHAR>' else units[-1]
        return units[0], last

def signature(word):
    return word[0], word[-1], len(word)

def constrained(rows, seed):
    rng = random.Random(seed)
    out = []
    eligible = changed = total = 0
    for row in rows:
        original = row['tokens']
        words = list(original)
        classes = defaultdict(list)
        for i in range(1, len(words)-1):
            classes[signature(words[i])].append(i)
            total += 1
        for positions in classes.values():
            values = [words[i] for i in positions]
            eligible += len(positions) if len(set(values)) > 1 else 0
            rng.shuffle(values)
            for i, value in zip(positions, values):
                words[i] = value
        assert Counter(words) == Counter(original)
        assert [signature(w) for w in words] == [signature(w) for w in original]
        assert not words or (words[0] == original[0] and words[-1] == original[-1])
        changed += sum(a != b for a,b in zip(words,original))
        out.append({**row, 'tokens': words})
    return out, {'interior_positions':total, 'eligible_positions':eligible, 'changed_positions':changed}

def compare_models(train, dev, test):
    bpe = BPE(train)
    full = Predictor(train, dev, bpe)
    coarse = Predictor(train, dev, CharacterContext(bpe), full.base)
    for rows in (train,dev,test):
        assert [(g,b) for g,_,b in pairs(rows,bpe)] == [(g,b) for g,_,b in pairs(rows,coarse.bpe)]
    fine_score, coarse_score = score(full,test), score(coarse,test)
    return bpe, full, coarse, fine_score, coarse_score

def checks():
    prior = synthetic_checks()
    results = {}
    for positive in (True,False):
        choices = [('aba','xx'),('aca','yy')] if positive else [('aba','xx'),('aba','yy'),('aca','xx'),('aca','yy')]
        parts = [[{'group':name,'tokens':['edge',a,b,'edge']} for a,b in choices for _ in range(n)]
                 for name,n in [('train',50),('dev',10),('test',10)]]
        _,_,_,fine,coarse = compare_models(*parts)
        delta = coarse['model_bits']-fine['model_bits']
        assert delta > .5 if positive else abs(delta) < 1e-10
        constrained(parts[0],17)
        results['positive' if positive else 'negative'] = delta
    return {'prior':prior,'increment':results}

def interval(groups):
    rng = random.Random(2026102303)
    values = list(groups.values())
    samples = []
    for _ in range(2000):
        sample = [rng.choice(values) for _ in values]
        samples.append(sum(g['coarse_loss']-g['full_loss'] for g in sample)/sum(g['n'] for g in sample))
    return [quantile(samples,.025),quantile(samples,.975)]

def audit(source):
    rows = source['records']
    train = [r for r in rows if bucket(r['group']) >= 2]
    dev = [r for r in rows if bucket(r['group']) == 1]
    test = [r for r in rows if bucket(r['group']) == 0]
    bpe,full,coarse,fine_score,coarse_score = compare_models(train,dev,test)
    groups = {}
    for g,f in fine_score['groups'].items():
        c = coarse_score['groups'][g]
        assert f['n'] == c['n']
        groups[g] = {'n':f['n'],'full_loss':f['model_loss'],'coarse_loss':c['model_loss']}
    controls = []
    for seed in range(2026102340,2026102356):
        shuffled,support = constrained(train,seed)
        model = Predictor(shuffled,dev,bpe,full.base)
        measurement = score(model,test)
        controls.append({'seed':seed,'support':support,'weight':model.weight,'gain_bits':measurement['gain_bits']})
    return {'label':source['label'],'full':fine_score,'character':coarse_score,
            'increment_bits':coarse_score['model_bits']-fine_score['model_bits'],
            'paired_interval_95':interval(groups),'groups':groups,
            'full_weight':full.weight,'character_weight':coarse.weight,
            'full_calibration':full.calibration,'character_calibration':coarse.calibration,
            'constrained_training_controls':controls}

def run():
    synthetic = checks()  # Stop before loading real corpora on failure.
    results = []
    for source in json.loads(INPUT.read_text())['sources']:
        results.append(audit(source))
        r = results[-1]
        print(r['label'],r['increment_bits'],r['paired_interval_95'],flush=True)
    paths = [INPUT,Path(__file__),PACKAGE/'PROTOCOL.md',ROOT/'scripts/analyze_subword_boundary.py',
             INPUT.parent/'residual_order.py',INPUT.parent/'residual_order_calibrated.py']
    return {'status':'EXPLORATORY','synthetic_checks':synthetic,'results':results,
            'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args = parser.parse_args()
    result = run()
    path = PACKAGE/'results.json'
    if args.check:
        from check_audit_snapshot import compare
        compare(json.loads(path.read_text()),result)
        print('Matched-target subword increment snapshot verified')
    else:
        path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
