#!/usr/bin/env python3
"""Exact conditional distribution; same retrospective question, no new semantics."""
import collections
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from math import comb
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_daiin_dam_control import FILES, read_records, tokens, pair_count
PROTOCOL='research/maintenance/2026-10-22-precision-review/PROTOCOL.md'

@lru_cache(None)
def arrangements(a,b,o,last_a=False):
    if min(a,b,o)<0:
        raise ValueError('Negative category count')
    if a+b+o==0:
        return ((0,1),)
    counts=collections.Counter()
    for remaining,next_last,increment in (
        ((a-1,b,o),True,0),((a,b-1,o),False,int(last_a)),((a,b,o-1),False,0)):
        if min(remaining)<0:
            continue
        for k,n in arrangements(*remaining,next_last):
            counts[k+increment]+=n
    return tuple(sorted(counts.items()))

def distribution(words):
    a,b=words.count('daiin'),words.count('dam');o=len(words)-a-b
    total=comb(a+b+o,a)*comb(b+o,b)
    counts=dict(arrangements(a,b,o))
    if sum(counts.values())!=total:
        raise ValueError('Incorrect arrangement normalization')
    return {k:Fraction(n,total) for k,n in counts.items()}

def convolve(left,right):
    result=collections.defaultdict(Fraction)
    for a,p in left.items():
        for b,q in right.items():result[a+b]+=p*q
    return dict(sorted(result.items()))

def rational(value):
    return {'numerator':str(value.numerator),'denominator':str(value.denominator),'decimal':float(value)}

def audit(label,path,policy):
    raw,rows=read_records(ROOT/path)
    active=[];observed=0
    for row in rows:
        if row['locus']!='P0':continue
        words=tokens([row['payload']],uncertain_space=policy)
        if 'daiin' in words and 'dam' in words:active.append((row,words))
    full={0:Fraction(1)};mean=Fraction(0);matches=[]
    for row,words in active:
        dist=distribution(words)
        row_mean=sum((k*p for k,p in dist.items()),Fraction(0))
        formula=Fraction(words.count('daiin')*words.count('dam'),len(words))
        if row_mean!=formula:raise ValueError('Mean differs from analytic expectation')
        mean+=formula;full=convolve(full,dist)
        count=pair_count(words);observed+=count
        if count:matches.append({'id':row['id'],'count':count})
    if sum(full.values())!=1:raise ValueError('Total probability differs from one')
    if sum((k*p for k,p in full.items()),Fraction(0))!=mean:raise ValueError('Convolution mean mismatch')
    tail=sum((p for k,p in full.items() if k>=observed),Fraction(0))
    return {'transcription':label,'space_policy':policy,'source':path,
        'source_sha256':hashlib.sha256(raw).hexdigest(),'active_records':len(active),
        'observed_pairs':observed,'matches':matches,'exact_expected_count':rational(mean),
        'exact_exploratory_tail':rational(tail),
        'distribution':{str(k):rational(p) for k,p in full.items()}},tail

def main():
    views=[];tails=[]
    for label,path in FILES:
        for policy in ('split','join'):
            view,tail=audit(label,path,policy);views.append(view);tails.append(tail)
    previous=json.loads((ROOT/'research/decipherment/2026-10-22-daiin-dam-control/results.json').read_text())
    prior={(v['transcription'],v['space_policy']):v for v in previous['views']}
    for view in views:
        old=prior[(view['transcription'],view['space_policy'])]
        if view['source_sha256']!=old['source_sha256'] or view['observed_pairs']!=old['pair_count'] or view['active_records']!=old['active_records_for_randomization']:
            raise ValueError('Original source or selection drift')
        if view['matches']!=[{'id':m['id'],'count':m['count']} for m in old['matches']]:
            raise ValueError('Original pair loci drift')
    running=Fraction(0)
    for rank,index in enumerate(sorted(range(4),key=tails.__getitem__)):
        running=max(running,min(Fraction(1),(4-rank)*tails[index]))
        views[index]['exact_exploratory_Holm_four_views']=rational(running)
    print(json.dumps({'status':'EXPLORATORY_EXACT_NULL_NOT_CONFIRMATORY',
        'protocol':PROTOCOL,'protocol_sha256':hashlib.sha256((ROOT/PROTOCOL).read_bytes()).hexdigest(),
        'views':views,'limits':['Exact probability for declared conditional null only.',
        'Retrospective selection and multiplicity beyond four views remain uncontrolled.',
        'No plaintext, phonetics or independent replication.']},indent=2))
if __name__=='__main__':main()
