"""Known-content calibration, not a Voynich decipherment."""
from collections import Counter
import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import sys

INPUT_SHA='c069548868854c29d294efbc3da891a0f5cf7c62878786be78fa13ce5ba5225d'

def digest(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,separators=(',',':'),sort_keys=True).encode()).hexdigest()

def rotate(word,amount):
    return ''.join(chr((ord(c)-97+amount)%26+97) if 'a'<=c<='z' else c for c in word)

def transform(rows,period,offset,inverse=False):
    if not 1<=period<=12 or not 0<=offset<26:raise ValueError('Key outside fixed family')
    direction=-1 if inverse else 1
    return [{**r,'tokens':[rotate(w,direction*(offset+i%period)) for i,w in enumerate(r['tokens'])]} for r in rows]

def unigram(rows):
    counts=Counter(c for r in rows for w in r['tokens'] for c in w if 'a'<=c<='z')
    total=sum(counts.values())
    if not total:raise ValueError('No ASCII training characters')
    return {chr(i+97):-math.log2((counts[chr(i+97)]+.5)/(total+13)) for i in range(26)}

def plain_loss(rows,cost):
    counts=Counter(c for r in rows for w in r['tokens'] for c in w if 'a'<=c<='z')
    return sum(counts[c]*cost[c] for c in sorted(counts))/sum(counts.values())

def recover(ciphertext,cost):
    """Select a key without plaintext, ground-truth key, or test observations."""
    candidates=[]
    for period in range(1,13):
        counts=Counter((i%period,c) for r in ciphertext for i,w in enumerate(r['tokens']) for c in w if 'a'<=c<='z')
        total=sum(counts.values())
        if not total:raise ValueError('No ASCII ciphertext characters')
        for offset in range(26):
            loss=sum(n*cost[rotate(c,-offset-phase)] for (phase,c),n in sorted(counts.items()))/total
            candidates.append({'period':period,'offset':offset,'development_bits':loss})
    candidates.sort(key=lambda x:(x['development_bits'],x['period'],x['offset']))
    return {'selected':candidates[0],'top5':candidates[:5],
        'margin_bits':candidates[1]['development_bits']-candidates[0]['development_bits'],'candidate_count':len(candidates)}

def accuracy(decoded,truth):
    assert len(decoded)==len(truth)
    exact=tokens=chars=char_exact=0
    for a,b in zip(decoded,truth):
        assert a['group']==b['group'] and len(a['tokens'])==len(b['tokens'])
        for x,y in zip(a['tokens'],b['tokens']):
            assert len(x)==len(y)
            tokens+=1;exact+=x==y;chars+=len(y);char_exact+=sum(c==d for c,d in zip(x,y))
    return {'exact_tokens':exact,'tokens':tokens,'token_accuracy':exact/tokens,
        'exact_characters':char_exact,'characters':chars,'character_accuracy':char_exact/chars}

def permuted(rows,seed):
    rng=random.Random(seed);out=[]
    for r in rows:
        words=list(r['tokens']);rng.shuffle(words);out.append({**r,'tokens':words})
    return out

def recovery_case(dev,test,cost,period,offset):
    enc_dev=transform(dev,period,offset);enc_test=transform(test,period,offset)
    assert transform(enc_dev,period,offset,True)==dev
    assert transform(enc_test,period,offset,True)==test
    chosen=recover(enc_dev,cost);k=chosen['selected']
    decoded=transform(enc_test,k['period'],k['offset'],True)
    return {**chosen,'generating_key':{'period':period,'offset':offset},
        'key_exact':(k['period'],k['offset'])==(period,offset),'test':accuracy(decoded,test),
        'identity_decoder_test':accuracy(enc_test,test),
        'ciphertext_dev_sha256':digest(enc_dev),'ciphertext_test_sha256':digest(enc_test),
        'decoded_test_sha256':digest(decoded),'truth_test_sha256':digest(test)}

def run(model_dir):
    sys.path.insert(0,str(model_dir.resolve()))
    from residual_order_calibrated import Calibrated,bucket,score
    raw=(model_dir/'inputs.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=INPUT_SHA:raise ValueError('Input hash mismatch')
    results=[]
    for source in json.loads(raw)['sources']:
        if source['kind']!='natural_language_control':continue
        rows=source['records']
        train=[r for r in rows if bucket(r['group'])>=2]
        dev=[r for r in rows if bucket(r['group'])==1]
        test=[r for r in rows if bucket(r['group'])==0]
        groups=[{r['group'] for r in p} for p in (train,dev,test)]
        assert all(not groups[i]&groups[j] for i,j in ((0,1),(0,2),(1,2)))
        cost=unigram(train);recovery={};metrics={}
        for name,period,offset in [('plain',1,0),('mono',1,13),('periodic',7,11)]:
            parts=[transform(p,period,offset) for p in (train,dev,test)]
            assert all(transform(q,period,offset,True)==p for p,q in zip((train,dev,test),parts))
            model=Calibrated(parts[0],parts[1],None);s=score(model,parts[2])
            metrics[name]={'gain_bits':s['identity_gain_over_edges_length'],'weights':model.weights,
                'unknown_rate':s['unknown_rate'],'loss_bits':s['loss_bits_per_transition'],
                'training_transitions':model.n,'test_transitions':s['transitions']}
            if name!='plain':recovery[name]=recovery_case(dev,test,cost,period,offset)
        shuffled_dev=permuted(dev,2026102601);shuffled_test=permuted(test,2026102601)
        adversarial=recovery_case(shuffled_dev,shuffled_test,cost,7,11)
        original_loss=plain_loss(dev,cost);shuffled_loss=plain_loss(shuffled_dev,cost)
        invariant=abs(metrics['plain']['gain_bits']-metrics['mono']['gain_bits'])<1e-10
        gates={'all_roundtrips_exact':True,'group_partitions_disjoint':True,'mono_metric_invariant':invariant,
            'positive_recovery':all(r['key_exact'] and r['test']['token_accuracy']==1 for r in recovery.values()),
            'adversarial_score_invariant':abs(original_loss-shuffled_loss)<1e-12}
        results.append({'label':source['label'],'groups':[sorted(g) for g in groups],
            'recovery':recovery,'residual_metrics':metrics,'adversarial':adversarial,
            'adversarial_cleartext_dev_losses':[original_loss,shuffled_loss],'gates':gates})
        print(source['label'],json.dumps(gates),flush=True)
    assert len(results)==2
    root=Path(__file__).parent
    return {'status':'REPRODUCED' if all(all(r['gates'].values()) for r in results) else 'BLOCKED',
        'scope':'Known-family, known-language artificial cipher calibration only; no manuscript evaluated.',
        'input_sha256':INPUT_SHA,'python':sys.version,
        'sha256':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ('run.py','PROTOCOL.md')},
        'model_sha256':{p:hashlib.sha256((model_dir/p).read_bytes()).hexdigest() for p in ('residual_order.py','residual_order_calibrated.py')},
        'results':results}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--model-dir',required=True,type=Path);parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    if args.output.exists():raise SystemExit('Output already exists')
    out=run(args.model_dir);args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
