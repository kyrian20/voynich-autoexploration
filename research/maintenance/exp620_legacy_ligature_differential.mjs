#!/usr/bin/env node
// EXP-620: exercise the actual historical parse functions, without changing them.
// Synthetic diagnostic of ligature deletion, not an IVTFF conformance certificate.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';

const paths = [
  'experiments/exp_613_615_ch_sh_inference_sensitivity/analyze.mjs',
  'experiments/exp_617_ch_sh_high_support/analyze.mjs',
];
const fixtures = {
  ligature: '<f1r> <! $Q=T>\n<f1r.1,P0> ch{a}y.sh{a}y\n',
  expanded: '<f1r> <! $Q=T>\n<f1r.1,P0> chay.shay\n',
  terminal: '<f1r> <! $Q=T>\n<f1r.1,P0> ch.sh\n',
  // Deliberately inconsistent header/line folio to expose metadata bleed.
  mismatched_folio: '<f1r> <! $Q=T>\n<f2r.1,P0> chay\n',
};
const output = [];
for (const path of paths) {
  const source = fs.readFileSync(path, 'utf8');
  const start = source.indexOf('function parse(');
  const end = source.indexOf(path.includes('613_615') ? '\nfunction analyze(' : 'function run(', start);
  assert.ok(start >= 0 && end > start, `Cannot isolate parse() in ${path}`);
  const context = vm.createContext(Object.create(null));
  const parse = vm.runInContext(source.slice(start, end) + '\nparse', context, {timeout:1000});
  const ligature = parse(fixtures.ligature);
  const expanded = parse(fixtures.expanded);
  const terminal = parse(fixtures.terminal);
  const mismatched = parse(fixtures.mismatched_folio);
  assert.equal(ligature.length, 0, `${path}: unexpected historical ligature policy`);
  assert.equal(expanded.length, 2, `${path}: expanded fixture should expose two events`);
  assert.equal(terminal.length, 0, `${path}: terminal digraph must not be counted`);
  assert.equal(expanded.filter(x => x.vowel).length, 2);
  // The frozen parser incorrectly assigns a f2r line to the preceding f1r header.
  // This is a characterization test, NOT acceptance of that attribution as valid.
  assert.equal(mismatched.length, 1, `${path}: historical folio-mismatch behavior changed`);
  assert.equal(mismatched[0].folio, 'f1r', `${path}: expected historical misattribution`);
  assert.equal(mismatched[0].dg, 'ch');
  output.push({path, sha256:crypto.createHash('sha256').update(source).digest('hex'),
    counts:{historical_ligature:ligature.length, explicit_expansion:expanded.length,terminal:terminal.length, mismatched_line_events:mismatched.length,
      mismatched_line_attributed_to:mismatched[0].folio},
    status:'KNOWN_LOSS_AND_FOLIO_MISATTRIBUTION_CHARACTERIZED'});
}
console.log(JSON.stringify({status:'PASS_DIAGNOSTIC_ONLY', fixtures, scripts:output,
  limitation:'Synthetic fixtures only; mismatched folio line deliberately invalid and demonstrates fail-open historical attribution. Do not treat this as a corpus-level defect frequency, IVTFF normative adjudication, corpus reproduction, or linguistic inference.'},null,2));
