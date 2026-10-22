#!/usr/bin/env python3
"""Exploratory conditional randomization of a previously observed EVA pair."""
import collections
import hashlib
import json
from pathlib import Path
import random
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_token_policy_sensitivity import read_records
from scripts.audit_decipherment_anchor_concordances import FILES
from scripts.ivtff_lossless import tokens
PROTOCOL='research/decipherment/2026-10-22-daiin-dam-control/PROTOCOL.md'
N=9999
SEED=2026102201

def pair_count(words):
    return sum(a=='daiin' and b=='dam' for a,b in zip(words,words[1:]))

def expected(words):
    return words.count('daiin')*words.count('dam')/len(words) if words else 0.0

def holm(values):
    order=sorted(range(len(values)),key=values.__getitem__)
    out=[0.0]*len(values); running=0.0
    for rank,index in enumerate(order):
        running=max(running,min(1.0,(len(values)-rank)*values[index]))
        out[index]=running
    return out

def audit(label,path,policy):
    raw,rows=read_records(ROOT/path)
    selected=[]
    for row in rows:
        if row['locus']=='P0':
            ws=tokens([row['payload']],uncertain_space=policy)
            selected.append((row,ws))
    transitions=sum(max(0,len(ws)-1) for _,ws in selected)
    starts=sum(ws[:-1].count('daiin') for _,ws in selected)
    ends=sum(ws[1:].count('dam') for _,ws in selected)
    active=[(row,ws) for row,ws in selected if 'daiin' in ws and 'dam' in ws]
    observed=sum(pair_count(ws) for _,ws in active)
    expectation=sum(expected(ws) for _,ws in active)
    rng=random.Random(SEED); null=[]
    for _ in range(N):
        count=0
        for _,ws in active:
            shuffled=list(ws);rng.shuffle(shuffled);count+=pair_count(shuffled)
        null.append(count)
    matches=[{'id':r['id'],'folio':r['folio'],'count':pair_count(ws)} for r,ws in active if pair_count(ws)]
    return {'transcription':label,'source':path,'source_sha256':hashlib.sha256(raw).hexdigest(),
        'space_policy':policy,'P0_records':len(selected),'transitions':transitions,
        'daiin_with_successor':starts,'dam_with_predecessor':ends,'pair_count':observed,
        'conditional_rate':observed/starts if starts else None,
        'marginal_rate':ends/transitions if transitions else None,
        'null_exact_expected_count':expectation,'observed_over_expected':observed/expectation if expectation else None,
        'null_mean':sum(null)/N,'null_histogram':dict(sorted(collections.Counter(null).items())),
        'exploratory_tail_plus_one':(1+sum(x>=observed for x in null))/(N+1),
        'matches':matches,'active_records_for_randomization':len(active)}

def main():
    views=[audit(label,path,policy) for label,path in FILES for policy in ('split','join')]
    for view,adjusted in zip(views,holm([v['exploratory_tail_plus_one'] for v in views])):
        view['exploratory_Holm_four_views']=adjusted
    print(json.dumps({'audit':'daiin_dam_P0_local_randomization','status':'EXPLORATORY_NOT_CONFIRMATORY',
        'protocol':PROTOCOL,'protocol_sha256':hashlib.sha256((ROOT/PROTOCOL).read_bytes()).hexdigest(),
        'permutations':N,'seed':SEED,'views':views,
        'limits':['Pair selected after seeing the corpus; multiplicity outside four views is uncontrolled.',
                  'Null conditions on each line multiset; not an independent-token population test.',
                  'No semantics, pronunciation or language assignment.']},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
