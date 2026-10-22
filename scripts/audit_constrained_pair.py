#!/usr/bin/env python3
"""Exact conditional pair tests preserving declared position/edge strata."""
import collections
from fractions import Fraction
from itertools import combinations
import hashlib
import json
from math import comb, prod
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_daiin_dam_control import FILES, read_records, tokens, pair_count
from scripts.audit_daiin_dam_exact import convolve, rational
PROTOCOL='research/decipherment/2026-10-22-constrained-pair/PROTOCOL.md'
CONTROLS=('fixed_endpoints','same_initial','same_edges','same_edges_position')
MAX_ASSIGNMENTS=1_000_000


def stratum(word,index,length,control):
    if not word: raise ValueError('Empty token')
    position='first' if index==0 else 'last' if index==length-1 else 'interior'
    if control=='fixed_endpoints':return (position,)
    if control=='same_initial':return (word[0],)
    if control=='same_edges':return (word[0],word[-1])
    if control=='same_edges_position':return (word[0],word[-1],position)
    raise ValueError('Unknown control')


def row_distribution(words,control):
    groups=collections.defaultdict(list)
    for i,w in enumerate(words):groups[stratum(w,i,len(words),control)].append(i)
    active=[]
    for slots in groups.values():
        a=sum(words[i]=='daiin' for i in slots)
        b=sum(words[i]=='dam' for i in slots)
        if a+b:active.append((slots,a,b))
    total=prod(comb(len(slots),a)*comb(len(slots)-a,b) for slots,a,b in active)
    if total>MAX_ASSIGNMENTS:raise ValueError(f'Exact enumeration blocked: {total} assignments')
    state=['O']*len(words);counts=collections.Counter()
    def visit(group):
        if group==len(active):
            counts[sum(a=='A' and b=='B' for a,b in zip(state,state[1:]))]+=1
            return
        slots,a,b=active[group]
        for aset in combinations(slots,a):
            aset=set(aset)
            for bset in combinations([i for i in slots if i not in aset],b):
                for i in aset:state[i]='A'
                for i in bset:state[i]='B'
                visit(group+1)
                for i in slots:state[i]='O'
    visit(0)
    if sum(counts.values())!=total:raise ValueError('Assignment count mismatch')
    dist={k:Fraction(n,total) for k,n in sorted(counts.items())}
    if sum(dist.values())!=1:raise ValueError('Normalization failed')
    if pair_count(words) not in dist:raise ValueError('Observed count outside null support')
    return dist,total


def moments(dist):
    mean=sum((k*p for k,p in dist.items()),Fraction(0))
    variance=sum(((k-mean)**2*p for k,p in dist.items()),Fraction(0))
    return mean,variance


def audit(label,path,policy,prior):
    raw,rows=read_records(ROOT/path)
    if hashlib.sha256(raw).hexdigest()!=prior['source_sha256']:raise ValueError('Corpus drift')
    active=[]
    for row in rows:
        if row['locus']=='P0':
            words=tokens([row['payload']],uncertain_space=policy)
            if 'daiin' in words and 'dam' in words:active.append((row,words))
    observed=sum(pair_count(ws) for _,ws in active)
    matches=[{'id':r['id'],'count':pair_count(ws)} for r,ws in active if pair_count(ws)]
    if observed!=prior['observed_pairs'] or matches!=prior['matches']:raise ValueError('Selection drift')
    results={};tails=[]
    for control in CONTROLS:
        full={0:Fraction(1)};details=[]
        for row,words in active:
            dist,assignments=row_distribution(words,control)
            mean,var=moments(dist)
            full=convolve(full,dist)
            details.append({'id':row['id'],'folio':row['folio'],'observed_pairs':pair_count(words),
                'tokens':words,'assignments':assignments,'support':sorted(dist),
                'expected':rational(mean),'variance':rational(var)})
        mean,var=moments(full)
        tail=sum((p for k,p in full.items() if k>=observed),Fraction(0))
        tails.append(tail)
        results[control]={'observed_pairs':observed,'expected':rational(mean),'variance':rational(var),
            'exact_exploratory_tail':rational(tail),'can_vary_pair_count':bool(var),
            'variable_records':sum(d['variance']['numerator']!='0' for d in details),
            'distribution':{str(k):rational(p) for k,p in full.items()},'records':details}
    return {'transcription':label,'source':path,'source_sha256':hashlib.sha256(raw).hexdigest(),
        'space_policy':policy,'active_records':len(active),'matches':matches,'controls':results},tails


def main():
    old=json.loads((ROOT/'research/maintenance/2026-10-22-precision-review/exact-results.json').read_text())
    prior={(v['transcription'],v['space_policy']):v for v in old['views']}
    views=[];all_tails=[];refs=[]
    for label,path in FILES:
        for policy in ('split','join'):
            view,tails=audit(label,path,policy,prior[label,policy]);views.append(view)
            all_tails.extend(tails);refs.extend(view['controls'][c] for c in CONTROLS)
    running=Fraction(0)
    for rank,i in enumerate(sorted(range(len(all_tails)),key=all_tails.__getitem__)):
        running=max(running,min(Fraction(1),(len(all_tails)-rank)*all_tails[i]))
        refs[i]['Holm_16_exploratory']=rational(running)
    tracked=['scripts/audit_constrained_pair.py','scripts/ivtff_lossless.py','scripts/audit_token_policy_sensitivity.py','scripts/audit_daiin_dam_exact.py']
    print(json.dumps({'status':'EXPLORATORY_CONDITIONAL_NOT_SEMANTIC',
        'protocol':PROTOCOL,'protocol_sha256':hashlib.sha256((ROOT/PROTOCOL).read_bytes()).hexdigest(),
        'implementation_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in tracked},
        'controls':CONTROLS,'max_assignments_per_record':MAX_ASSIGNMENTS,'family_size':len(refs),'views':views,
        'limits':['Retrospective pair; Holm only covers 16 new conditional views.',
        'EVA edge characters are proxies, not adjudicated glyphs.',
        'Zero variance is lack of discrimination, not evidence against meaning.',
        'Related transcriptions and policies are dependent views.']},indent=2))
if __name__=='__main__':main()
