#!/usr/bin/env python3
"""Reproduce the formerly separate block against canonical repository sources."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
BLOCK=Path(__file__).resolve().parent
ROOT=BLOCK.parents[2]
sys.path.insert(0,str(ROOT))
from scripts.check_audit_snapshot import compare


def scientific_compare(expected,actual):
    # Interpreter strings can differ between local Python and Actions Python.
    # No counts, probabilities, seeds, hashes or model-selection fields ignored.
    a=dict(expected);b=dict(actual)
    if not isinstance(a.pop('python',None),str) or not isinstance(b.pop('python',None),str):
        raise ValueError('Missing interpreter identity')
    compare(a,b)


def reference_audit_compare(expected, actual):
    """Keep corpus facts and historical hits strict; report additive inventory."""
    def split(audit):
        facts = dict(audit)
        rows = facts.pop('static_references')
        declared = facts.pop('distinct_scripts_with_direct_reference')
        indexed = {(row['script'], row['input']): row for row in rows}
        if len(indexed) != len(rows):
            raise ValueError('Duplicate static reference')
        if declared != len({row['script'] for row in rows}):
            raise ValueError('Incorrect static-reference script count')
        return facts, indexed

    expected_facts, historical = split(expected)
    actual_facts, current = split(actual)
    compare(expected_facts, actual_facts)
    for key, row in historical.items():
        if key not in current:
            raise ValueError(f'Historical static reference missing: {key}')
        compare(row, current[key], f'$.static_references[{key!r}]')
    return [current[key] for key in sorted(current.keys() - historical.keys())]


def validate_source_reuse(root,inputs,review):
    excluded=review['excluded_from_new_language_baselines']
    names=[entry['path'] for entry in excluded]
    if len(names)!=len(set(names)):
        raise ValueError('Duplicate identity-review paths')
    root=root.resolve()
    for entry in inputs['raw_sources']:
        name=entry['path']
        if name in names:
            raise ValueError(f'Source requires identity/use adjudication: {name}')
        path=(root/name).resolve()
        if not path.is_relative_to(root/'data'):
            raise ValueError('Source outside canonical data tree')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']:
            raise ValueError(f'Corpus drift: {name}')


def run(args,out):
    inputs=json.loads((BLOCK/'inputs.json').read_text())
    review=json.loads((ROOT/'research/CORPUS_IDENTITY_REVIEW.json').read_text())
    validate_source_reuse(ROOT,inputs,review)
    log=out/'execution.log'
    commands=[]
    def command(arguments,output=None):
        argv=[sys.executable]+[str(a) for a in arguments]
        process=subprocess.run(argv,cwd=ROOT,text=True,capture_output=True)
        with log.open('a') as stream:
            stream.write(json.dumps({'command':argv,'exit_code':process.returncode})+'\n')
            stream.write(process.stderr)
            if output is None:stream.write(process.stdout)
        commands.append({'arguments':[str(a) for a in arguments],'exit_code':process.returncode})
        if process.returncode:raise RuntimeError(f'Integration step failed; inspect {log.name}')
        if output:output.write_text(process.stdout)
    command([ROOT/'scripts/check_corpus_integrity.py'])
    for name in ('test_residual_order.py','test_calibrated.py','test_integration.py'):
        command([BLOCK/name])
    command([BLOCK/'prepare_inputs.py','--repo',ROOT,'--out',out])
    compare(inputs,json.loads((out/'inputs.json').read_text()))
    command([BLOCK/'audit_reference_identity.py','--repo',ROOT],out/'reference_identity_audit.json')
    added_references = reference_audit_compare(
        json.loads((BLOCK/'reference_identity_audit.json').read_text()),
        json.loads((out/'reference_identity_audit.json').read_text()))
    (out/'static-reference-additions.json').write_text(
        json.dumps({'status':'STATIC_MENTIONS_NOT_PROOF_OF_EXECUTION',
                    'added_references':added_references},indent=2)+'\n')
    for stem in ('residual_order','residual_order_calibrated'):
        actual=out/(stem+'_results.json')
        command([BLOCK/(stem+'.py')],actual)
        scientific_compare(json.loads((BLOCK/(stem+'_results.json')).read_text()),json.loads(actual.read_text()))
    receipt={'status':'REPRODUCED_INTEGRATED_NOT_SEMANTIC_VALIDATION',
             'canonical_corpora_reused':len(inputs['raw_sources']),
             'raw_corpus_copies_added':0,'prepared_inputs_reproduced':True,
             'historical_reference_identity_audit_reproduced':True,
             'new_static_references':len(added_references),
             'V1_and_V2_results_reproduced':True,'commands':commands}
    (out/'integration-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({key:value for key,value in receipt.items() if key!='commands'},indent=2))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    out=args.out.resolve()
    # Integration never regenerates reference snapshots or canonical corpus bytes.
    if out==ROOT or out.is_relative_to(ROOT):
        raise ValueError('Output must be outside repository; snapshots are read-only')
    out.mkdir(parents=True,exist_ok=True)
    if (out/'execution.log').exists():
        raise ValueError('Use a fresh output directory to preserve earlier logs')
    run(args,out)
if __name__=='__main__':main()
