#!/usr/bin/env python3
"""Reference-only diagnostic of EXP259; historical module bodies never execute."""
import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BLOCK = ROOT/'research/maintenance/2026-10-22-reference-sensitivity'

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def direct_profile(words, limit=12):
    result = []
    for i in range(limit):
        chars = Counter(w[i] for w in words if len(w)>i)
        n = sum(chars.values())
        entropy = -sum(c/n*math.log2(c/n) for c in chars.values()) if n else 0.0
        conditional = None
        if i and n:
            pairs = Counter((w[i-1], w[i]) for w in words if len(w)>i)
            previous = Counter()
            for (x,y), count in pairs.items():
                previous[x] += count
            conditional = -sum(count/n*math.log2(count/previous[x]) for (x,y),count in pairs.items())
        result.append({'position':i, 'n':n, 'marginal_bits':entropy, 'conditional_bits':conditional})
    return result

def isolated_historical():
    path = ROOT/'experiments/exp_259_char_positional_entropy/script.py'
    tree = ast.parse(path.read_text())
    names = {'entropy','positional_entropy_latin'}
    nodes = [n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
    if len(nodes)!=2:
        raise ValueError('Historical function selection changed')
    namespace = {'math':math, 'Counter':Counter, 'defaultdict':defaultdict}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),namespace)
    return namespace['positional_entropy_latin'], sha(path.read_bytes())

def verified_profile(words, historical):
    independent = direct_profile(words)
    original = historical(words,12)
    for row, (position,h,n,hc) in zip(independent,original,strict=True):
        if (position,n)!=(row['position'],row['n']) or abs(h-row['marginal_bits'])>1e-12:
            raise ValueError('Marginal implementation mismatch')
        if position and row['conditional_bits'] is not None and abs(hc-row['conditional_bits'])>1e-12:
            raise ValueError('Conditional implementation mismatch')
    return independent

def compute():
    review = json.loads((ROOT/'research/CORPUS_IDENTITY_REVIEW.json').read_text())
    mixed = next(r for r in review['excluded_from_new_language_baselines'] if r['issue']=='BILINGUAL_REQUIRES_FILTER_AUDIT')
    inputs = json.loads((ROOT/'research/analysis/2026-10-22-residual-order/inputs.json').read_text())
    latin = next(r for r in inputs['raw_sources'] if r.get('body_anchor','').startswith('C. IULI CAESARIS'))
    sources = []
    for label, metadata in [('historical_bilingual_diagnostic',mixed),('latin_caesar_full_file',latin),('latin_caesar_declared_body',latin)]:
        path = ROOT/metadata['path']
        raw = path.read_bytes()
        if sha(raw)!=metadata['sha256']:
            raise ValueError('Frozen input changed')
        text = raw.decode('utf-8-sig',errors='replace')
        if label.endswith('declared_body'):
            anchor = metadata['body_anchor']
            start = text.find(anchor)
            if start<0: raise ValueError('Missing anchor')
            end = re.search(r'(?im)^(?:\*\*\* END OF|End of Project Gutenberg)',text[start:])
            if not end: raise ValueError('Missing end marker')
            text = text[start:start+end.start()]
        words = re.findall(r'[a-zA-Z]+',text.lower())
        sources.append({'label':label,'path':metadata['path'],'sha256':sha(raw),
                        'selected_text_sha256':sha(text.encode()),'token_count':len(words),
                        'token_sequence_sha256':sha(json.dumps(words,separators=(',',':')).encode()),
                        'alphabet':''.join(sorted(set(''.join(words)))), 'words':words})
    historical,script_hash = isolated_historical()
    for source in sources:
        source['profile'] = verified_profile(source.pop('words'),historical)
    archived = ROOT/'experiments/exp_259_char_positional_entropy/result.md'
    table = archived.read_text().split('## Marginal Entropy')[1].split('## Conditional Entropy')[0]
    rows = []
    for line in table.splitlines():
        cells = [x.strip() for x in line.split('|')[1:-1]]
        if len(cells)==7 and cells[0].isdigit():
            rows.append((int(cells[0]),float(cells[5]),int(cells[6])))
    if len(rows)!=12: raise ValueError('Archive table shape changed')
    discrepancies = []
    for position,printed,n in rows:
        actual = sources[0]['profile'][position]
        if abs(actual['marginal_bits']-printed)>.000500000001 or actual['n']!=n:
            discrepancies.append({'position':position,'archived_h':printed,'archived_n':n,'replayed':actual})
    conditional_table = archived.read_text().split('## Conditional Entropy')[1].split('## Suffix Zone')[0]
    conditional_discrepancies = []
    conditional_rows = []
    for line in conditional_table.splitlines():
        cells = [x.strip() for x in line.split('|')[1:-1]]
        if len(cells)==4 and cells[0].isdigit():
            conditional_rows.append((int(cells[0]),float(cells[3])))
    if len(conditional_rows)!=11: raise ValueError('Archive conditional table shape changed')
    for position, printed in conditional_rows:
        actual = sources[0]['profile'][position]['conditional_bits']
        if abs(actual-printed)>.000500000001:
            conditional_discrepancies.append({'position':position,'archived':printed,'replayed':actual})
    contrasts = []
    for source in sources[1:]:
        contrasts.append({'comparison':source['label']+' minus historical_bilingual_diagnostic',
                          'marginal_bits':[b['marginal_bits']-a['marginal_bits'] for a,b in zip(sources[0]['profile'],source['profile'],strict=True)]})
    return {'source_commit':'96609813191caff5478ced3f5f7d4a90ed701fe7','historical_script_sha256':script_hash,
            'archived_report_sha256':sha(archived.read_bytes()), 'archive_marginal_discrepancies':discrepancies, 'archive_conditional_discrepancies':conditional_discrepancies,
            'tokenization':'EXP259 ASCII [a-zA-Z]+ lowercase, token weighted, 12 absolute character positions',
            'implementation_agreement_tolerance_bits':1e-12,'sources':sources,'contrasts':contrasts,
            'scope':'Reference sensitivity only. Bilingual input is diagnostic, excluded from new monolingual baselines. No manuscript parser, simulation or semantic validation.'}

def main():
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--out',type=Path)
    group.add_argument('--check',type=Path)
    args=parser.parse_args()
    result=compute()
    if args.check:
        if result!=json.loads(args.check.read_text()): raise SystemExit('Sensitivity replay differs')
    else:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'sources':[(s['label'],s['token_count']) for s in result['sources']],
                      'archive_marginal_discrepancies':len(result['archive_marginal_discrepancies'])}))

if __name__=='__main__': main()
