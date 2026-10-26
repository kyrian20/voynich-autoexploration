"""Limited exact-token anchor inventory; no sound or meaning assigned."""
import argparse,collections,hashlib,json,re,sys
from pathlib import Path

TARGETS=('doary','doaro','dary')
# Pattern copied, unmodified, from scripts/audit_research_readiness.py.
ROW=re.compile(r'^<(?P<page>f(?:[0-9]+[rv][1-6]?|Ros))\.(?P<number>[0-9]+),(?P<locus>[^>]*)>\s*(?P<body>.*)$')
EXPECTED={'eva_zl3b.txt':'bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc','eva_it2a.txt':'7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5'}
def sha(b):return hashlib.sha256(b).hexdigest()

def inventory(path,lex,tokens):
    raw=path.read_bytes()
    if sha(raw)!=EXPECTED[path.name]:raise ValueError('Unexpected source hash')
    views={p:{t:[] for t in TARGETS} for p in ('split','join')};skipped=[];counts={'numeric':0,'named':0};seen=set();target_locus=[]
    for n,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        match=ROW.match(line)
        if not match:
            # Do not silently discard a numeric tag that Python's Unicode \\d
            # would have accepted. The source is frozen, but derived readers
            # must also reject malformed future inputs instead of undercounting.
            if line.startswith('<f') and any(
                ch.isdecimal() and not ch.isascii()
                for ch in line.partition('>')[0]
            ):
                raise ValueError(f'Non-ASCII decimal digit in IVTFF identifier at source line {n}')
            if any(t in line for t in TARGETS):skipped.append({'source_line':n,'raw':line})
            continue
        r=match.groupdict();identifier=r['page']+'.'+r['number']
        if identifier in seen:raise ValueError('Duplicate locus')
        seen.add(identifier)
        counts['named' if r['page']=='fRos' else 'numeric']+=1
        p=lex(r['body'])
        if p.diagnostics:raise ValueError('Unresolved lexical diagnostics')
        if identifier=='f68r3.11':target_locus.append({'id':identifier,'source_line':n,'locus':r['locus'],'raw':line,'payload_spans':[{'kind':s.kind,'raw':s.raw,'start':s.start,'end':s.end} for s in p.spans]})
        for policy in views:
            words=tokens([p],uncertain_space=policy)
            for i,w in enumerate(words):
                if w in TARGETS:views[policy][w].append({'id':identifier,'page':r['page'],'locus':r['locus'],'source_line':n,'token_index0':i,'body':r['body'],'context':words[max(0,i-2):i+3]})
    if len(target_locus)!=1:raise ValueError('Expected exactly one target locus')
    return {'file':path.name,'sha256':sha(raw),'parsed_records':sum(counts.values()),
        'numeric_records':counts['numeric'],'named_records':counts['named'],'target_locus':target_locus[0],
        'unparsed_target_bearing_lines':skipped,'views':{p:{t:{'count':len(v),'matches':v} for t,v in ts.items()} for p,ts in views.items()}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo-root',required=True,type=Path);p.add_argument('--source-dir',type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    if a.output.exists():raise SystemExit('Output exists')
    sys.path.insert(0,str(a.repo_root.resolve()));from scripts.ivtff_lossless import lex,tokens
    directory=a.source_dir or a.repo_root/'data/transcriptions'
    results=[inventory(directory/name,lex,tokens) for name in EXPECTED]
    out={'schema_version':2,'status':'GENERATED','scope':'Exact-token inventory of numeric locus identifiers on numeric pages and fRos; not semantic evidence','targets':TARGETS,
        'lexer_sha256':sha((a.repo_root/'scripts/ivtff_lossless.py').read_bytes()),'script_sha256':sha(Path(__file__).read_bytes()),
        'protocol_sha256':sha(Path(__file__).with_name('PROTOCOL.md').read_bytes()),'python':sys.version,'sources':results}
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    for s in results:print(s['file'],'parsed',s['parsed_records'],'numeric',s['numeric_records'],'named',s['named_records'],{p:{t:v['count'] for t,v in ts.items()} for p,ts in s['views'].items()},'unparsed',len(s['unparsed_target_bearing_lines']))
)
EXPECTED={'eva_zl3b.txt':'bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc','eva_it2a.txt':'7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5'}
def sha(b):return hashlib.sha256(b).hexdigest()

def inventory(path,lex,tokens):
    raw=path.read_bytes()
    if sha(raw)!=EXPECTED[path.name]:raise ValueError('Unexpected source hash')
    views={p:{t:[] for t in TARGETS} for p in ('split','join')};skipped=[];counts={'numeric':0,'named':0};seen=set();target_locus=[]
    for n,line in enumerate(raw.decode('utf-8-sig').splitlines(),1):
        match=ROW.match(line)
        if not match:
            if any(t in line for t in TARGETS):skipped.append({'source_line':n,'raw':line})
            continue
        r=match.groupdict();identifier=r['page']+'.'+r['number']
        if identifier in seen:raise ValueError('Duplicate locus')
        seen.add(identifier)
        counts['named' if r['page']=='fRos' else 'numeric']+=1
        p=lex(r['body'])
        if p.diagnostics:raise ValueError('Unresolved lexical diagnostics')
        if identifier=='f68r3.11':target_locus.append({'id':identifier,'source_line':n,'locus':r['locus'],'raw':line,'payload_spans':[{'kind':s.kind,'raw':s.raw,'start':s.start,'end':s.end} for s in p.spans]})
        for policy in views:
            words=tokens([p],uncertain_space=policy)
            for i,w in enumerate(words):
                if w in TARGETS:views[policy][w].append({'id':identifier,'page':r['page'],'locus':r['locus'],'source_line':n,'token_index0':i,'body':r['body'],'context':words[max(0,i-2):i+3]})
    if len(target_locus)!=1:raise ValueError('Expected exactly one target locus')
    return {'file':path.name,'sha256':sha(raw),'parsed_records':sum(counts.values()),
        'numeric_records':counts['numeric'],'named_records':counts['named'],'target_locus':target_locus[0],
        'unparsed_target_bearing_lines':skipped,'views':{p:{t:{'count':len(v),'matches':v} for t,v in ts.items()} for p,ts in views.items()}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo-root',required=True,type=Path);p.add_argument('--source-dir',type=Path);p.add_argument('--output',required=True,type=Path);a=p.parse_args()
    if a.output.exists():raise SystemExit('Output exists')
    sys.path.insert(0,str(a.repo_root.resolve()));from scripts.ivtff_lossless import lex,tokens
    directory=a.source_dir or a.repo_root/'data/transcriptions'
    results=[inventory(directory/name,lex,tokens) for name in EXPECTED]
    out={'schema_version':2,'status':'GENERATED','scope':'Exact-token inventory of numeric locus identifiers on numeric pages and fRos; not semantic evidence','targets':TARGETS,
        'lexer_sha256':sha((a.repo_root/'scripts/ivtff_lossless.py').read_bytes()),'script_sha256':sha(Path(__file__).read_bytes()),
        'protocol_sha256':sha(Path(__file__).with_name('PROTOCOL.md').read_bytes()),'python':sys.version,'sources':results}
    a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    for s in results:print(s['file'],'parsed',s['parsed_records'],'numeric',s['numeric_records'],'named',s['named_records'],{p:{t:v['count'] for t,v in ts.items()} for p,ts in s['views'].items()},'unparsed',len(s['unparsed_target_bearing_lines']))
