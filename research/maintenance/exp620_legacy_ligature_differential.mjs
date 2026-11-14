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
// Independent fail-closed preflight for the fixtures consumed by this runner.
// It is deliberately narrower than a complete IVTFF validator: unknown record
// shapes are rejected rather than silently admitted to folio-stratified analysis.
function assertFolioAgreement(text) {
  let active = null;
  for (const raw of text.split(/\r?\n/)) {
    if (!raw.trim()) continue;
    const header = raw.match(/^<([A-Za-z0-9]+[rv])>\s+<!.*>\s*$/);
    if (header) { active = header[1]; continue; }
    const line = raw.match(/^<([A-Za-z0-9]+[rv])\.[^>]+>\s+.+$/);
    if (!line || !active || line[1] !== active) {
      throw new Error('IVTFF_FOLIO_PREFLIGHT_REJECTED: ' + raw);
    }
  }
  if (!active) throw new Error('IVTFF_FOLIO_PREFLIGHT_REJECTED: no header');
}
for (const key of ['ligature', 'expanded', 'terminal']) assert.doesNotThrow(() => assertFolioAgreement(fixtures[key]));
assert.throws(() => assertFolioAgreement(fixtures.mismatched_folio), /IVTFF_FOLIO_PREFLIGHT_REJECTED/);
assert.throws(() => assertFolioAgreement('<f1r.1,P0> chay\\n'), /IVTFF_FOLIO_PREFLIGHT_REJECTED/);
assert.throws(() => assertFolioAgreement('<f1r> <! $Q=T>\\nUNRECOGNIZED\\n'), /IVTFF_FOLIO_PREFLIGHT_REJECTED/);
assert.doesNotThrow(() => assertFolioAgreement('<f1r> <! $Q=T>\\n<f1r.1,P0> chay\\n<f2r> <! $Q=T>\\n<f2r.1,P0> shay\\n'));
const output = [];
for (const path of paths) {
  const source = fs.readFileSync(path, 'utf8');
  const start = source.indexOf('function parse(');
  const end = source.indexOf(path.includes('613_615') ? '\nfunction analyze(' : 'function run(', start);
  assert.ok(start >= 0 && end > start, `Cannot isolate parse() in ${path}`);
  const context = vm.createContext(Object.create(null));
  const parse = vm.runInContext(source.slice(start, end) + '\nparse', context, {timeout:1000});
  assertFolioAgreement(fixtures.ligature);
  const ligature = parse(fixtures.ligature);
  assertFolioAgreement(fixtures.expanded);
  const expanded = parse(fixtures.expanded);
  assertFolioAgreement(fixtures.terminal);
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
  preflight:'FAIL_CLOSED_FOR_TESTED_FOLIO_MISMATCH_AND_UNKNOWN_RECORDS; not integrated into frozen historical scripts',
  limitation:'Synthetic fixtures only; mismatched folio line deliberately invalid and demonstrates fail-open historical attribution. Do not treat this as a corpus-level defect frequency, IVTFF normative adjudication, corpus reproduction, or linguistic inference.'},null,2));
