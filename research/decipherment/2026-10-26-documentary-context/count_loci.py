"""Count editorial records by locus, not objects or decoded names."""
import argparse,collections,hashlib,json,re,sys
from pathlib import Path

ROW=re.compile(r'^<(?P<page>f(?:\d+[rv][1-6]?|Ros))\.(?P<number>\d+),(?P<locus>[^>]*)>\s*(?P<body>.*)$')
PAGES=('f68r1','f68r2','f68r3')
EXPECTED={'eva_zl3b.txt':'bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc','eva_it2a.txt':'7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5'}

def scan(text):
    out={p:[] for p in PAGES};unparsed=[];seen=set()
    for n,line in enumerate(text.splitlines(),1):
        m=ROW.match(line)
        if not m:
            if any(line.startswith('<'+p+'.') for p in PAGES):unparsed.append({'line':n,'raw':line})
            continue
        x=m.groupdict()
        if x['page'] not in out:continue
        identifier=x['page']+'.'+x['number']
        if identifier in seen:raise ValueError('Duplicate record')
        seen.add(identifier);locus=x['locus'].split(';')[0][1:]
        out[x['page']].append({'id':identifier,'source_line':n,'locus':locus,'body':x['body']})
    pages=[]
    for page,records in out.items():
        counts=collections.Counter(r['locus'] for r in records);labels=[r for r in records if r['locus'].startswith('L')]
        pages.append({'page':page,'records':len(records),'locus_counts':dict(sorted(counts.items())),'label_records':len(labels),
            'C28_literal_complete_bijection_count_condition':len(labels)==28,
            'Z12_literal_complete_bijection_count_condition':len(labels)==12,
            'rows':records,'labels':labels})
    return {'pages':pages,'unparsed_target_records':unparsed}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source-dir',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise SystemExit('Output exists')
    sources=[]
    for filename,expected in EXPECTED.items():
        raw=(a.source_dir/filename).read_bytes();assert hashlib.sha256(raw).hexdigest()==expected
        result=scan(raw.decode('utf-8-sig'));assert not result['unparsed_target_records']
        sources.append({'source':filename,'sha256':expected,**result})
    out={'status':'REPRODUCED','scope':'Editorial numeric records; count compatibility is not semantic identification','python':sys.version,
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'plan_sha256':hashlib.sha256(Path(__file__).with_name('PLAN.md').read_bytes()).hexdigest(),'sources':sources}
    a.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
    for s in sources:print(s['source'],[(p['page'],p['label_records'],p['locus_counts']) for p in s['pages']])
