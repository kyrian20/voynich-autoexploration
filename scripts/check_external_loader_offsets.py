#!/usr/bin/env python3
"""Read-only audit of the pinned external Gutenberg loader; no corpus replacement."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
PIN='66f8adaadc120f93e8a4c906685ba66a9d3ab847'
FILES=['herbal/culpeper_en.txt','italian/27608.txt','italian/26166.txt']

def words(text):
    return [w.lower() for w in re.sub(r'[^A-Za-zÀ-ÿ ]',' ',text).split() if w.isalpha()]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True)
    root=parser.parse_args().repo
    if subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()!=PIN:
        raise ValueError('Wrong external revision')
    rows=[];old={};new={}
    for name in FILES:
        raw=(root/name).read_text(encoding='utf-8',errors='replace')
        if (root/name).read_bytes()!=subprocess.check_output(['git','show',f'{PIN}:{name}'],cwd=root):
            raise ValueError('External input drift')
        i,j=raw.find('*** START'),raw.find('*** END')
        legacy=raw
        if i>0:legacy=legacy[legacy.find('\n',i):]
        if j>0:legacy=legacy[:j]
        corrected=raw
        if i>=0:corrected=corrected[corrected.find('\n',i)+1:]
        end=corrected.find('*** END')
        if end>=0:corrected=corrected[:end]
        old[name]=words(legacy);new[name]=words(corrected)
        rows.append({'path':name,'start_marker_offset':i,'end_marker_offset':j,
            'legacy_retains_end_marker':'*** END' in legacy,'legacy_token_count':len(old[name]),
            'recomputed_offset_token_count':len(new[name])})
    # The inspected driver takes only 33,582 tokens in this pinned run.
    n=33582
    prefixes={
        'Culpeper':old[FILES[0]][:n]==new[FILES[0]][:n],
        'Italian_combined':(old[FILES[1]]+old[FILES[2]])[:n]==(new[FILES[1]]+new[FILES[2]])[:n]}
    print(json.dumps({'revision':PIN,'records':rows,'analysis_prefix_tokens':n,
        'analyzed_prefix_unchanged_by_offset_fix':prefixes,
        'scope':'Observed loader defect in full streams; no effect on these two selected prefixes. No revised external headline asserted.'},indent=2))
if __name__=='__main__':main()
