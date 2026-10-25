"""Exact position support for this artificial, line-reset periodic family."""
import argparse,hashlib,json
from pathlib import Path

INPUT_SHA='c069548868854c29d294efbc3da891a0f5cf7c62878786be78fa13ce5ba5225d'
def bucket(group):return int(hashlib.sha256(group.encode()).hexdigest()[:8],16)%5

def support(rows,p,q):
    records_count=0;tokens=0;positions=set();groups=set()
    for r in rows:
        differing=[j for j in range(len(r['tokens'])) if ((j%p)-(j%q))%26]
        if differing:
            records_count+=1;groups.add(r['group']);tokens+=len(differing);positions.update(differing)
    return {'p':p,'q':q,'records_with_distinguishing_positions':records_count,
        'groups_with_distinguishing_positions':sorted(groups),'tokens_at_distinguishing_positions':tokens,
        'positions0':sorted(positions),'mapping_identical_on_all_observed_tokens':tokens==0}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--inputs',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);a=parser.parse_args()
    if a.output.exists():raise SystemExit('Output exists')
    raw=a.inputs.read_bytes();assert hashlib.sha256(raw).hexdigest()==INPUT_SHA
    results=[]
    for s in json.loads(raw)['sources']:
        if s['kind']!='natural_language_control':continue
        maximum=max(len(r['tokens']) for r in s['records']);entry={'label':s['label'],'maximum_line_tokens':maximum,
            'global_alias_pair':support(s['records'],maximum,maximum+1),'partition_support':{}}
        for part,predicate in [('train',lambda b:b>=2),('development',lambda b:b==1),('test',lambda b:b==0)]:
            rows=[r for r in s['records'] if predicate(bucket(r['group']))]
            entry['partition_support'][part]=support(rows,12,13)
        assert entry['global_alias_pair']['mapping_identical_on_all_observed_tokens']
        results.append(entry)
    a.output.write_text(json.dumps({'status':'REPRODUCED','scope':'Deterministic mapping support, not a statistical power estimate','input_sha256':INPUT_SHA,'results':results},indent=2)+'\n')
