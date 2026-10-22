#!/usr/bin/env python3
"""Freeze declared analytical views; originals copied intact with their notices."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def pg_body(raw,start_literal):
 text=raw.decode('utf-8-sig',errors='replace')
 start=text.find(start_literal)
 if start<0:raise ValueError('Missing declared content anchor')
 body=text[start:]
 end=re.search(r'(?im)^(?:\*\*\* END OF|End of Project Gutenberg)',body)
 if not end:raise ValueError('Missing end marker')
 return body[:end.start()]


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
 args=parser.parse_args();root=args.repo.resolve();dest=args.out;dest.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(root))
 from scripts.audit_token_policy_sensitivity import read_records
 from scripts.ivtff_lossless import tokens
 specs=[('ZL3b','data/transcriptions/eva_zl3b.txt'),('IT2a','data/transcriptions/eva_it2a.txt')]
 sources=[];ids=None;receipts=[]
 for label,relative in specs:
  raw,rows=read_records(root/relative)
  receipts.append({'path':relative,'sha256':hashlib.sha256(raw).hexdigest()})
  for policy in ('split','join'):
   selected=[]
   for row in rows:
    if row['locus']!='P0':continue
    words=tokens([row['payload']],uncertain_space=policy)
    if len(words)<2:continue
    group=re.match(r'f\d+',row['folio'])
    if not group:raise ValueError('Unadjudicated physical leaf')
    selected.append({'id':row['id'],'page':row['folio'],'group':group[0],'tokens':words})
   ids=set(r['id'] for r in selected) if ids is None else ids & {r['id'] for r in selected}
   sources.append({'label':label+'_'+policy,'kind':'manuscript_view','records':selected})
 for source in sources:source['records']=[r for r in source['records'] if r['id'] in ids]
 skeleton=[len(r['tokens']) for r in sources[0]['records']]
 controls=[('Latin_Caesar_218','data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt','C. IULI CAESARIS DE BELLO GALLICO COMMENTARIUS PRIMUS'),
           ('Italian_Dante_1012','data/reference_corpora/italian/dante_divina_commedia.txt','Nel mezzo del cammin di nostra vita')]
 for label,relative,anchor in controls:
  raw=(root/relative).read_bytes()
  receipts.append({'path':relative,'sha256':hashlib.sha256(raw).hexdigest(),'body_anchor':anchor})
  words=re.findall(r'[^\W\d_]+',pg_body(raw,anchor).lower(),flags=re.UNICODE)
  rows=[];offset=0
  for i,size in enumerate(skeleton):
   if offset+size>len(words):break
   rows.append({'id':f'line{i}','page':None,'group':f'block{i//25:04d}','tokens':words[offset:offset+size]});offset+=size
  sources.append({'label':label,'kind':'natural_language_control','records':rows,'body_tokens_available':len(words),'unused_body_tokens':len(words)-offset})
 out={'source_commit':'b566b6fa461f3a4e6fd8bb3a1aaa6e71f035f190','common_physical_records':len(ids),'raw_sources':receipts,'sources':sources,
      'parser_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in ['scripts/ivtff_lossless.py','scripts/audit_token_policy_sensitivity.py']}}
 (dest/'inputs.json').write_text(json.dumps(out,ensure_ascii=False,separators=(',',':'))+'\n')
 print(json.dumps({'sources':[(s['label'],len(s['records']),sum(len(r['tokens']) for r in s['records'])) for s in sources],'common_ids':len(ids)}))
if __name__=='__main__':main()
