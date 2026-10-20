#!/usr/bin/env node
// EXP-592: max-T correction for line-initial EVA tokens.
// Run: node scripts/exp_592_max_t.js data/transcriptions/eva_zl3b.txt
// Standard library only. Seed and parser are fixed for reproducibility.
const fs = require("fs");
const path = process.argv[2] || "data/transcriptions/eva_zl3b.txt";
const B = 5000, SEED = 20261020, MIN_FREQ = 50;
const source = fs.readFileSync(path, "utf8");
const rows = [];
for (const raw of source.split(/\r?\n/)) {
  const m = raw.match(/^<f[0-9]+[rv]\.[^>]*>\s*(.*)$/i);
  if (!m) continue;
  const text = m[1]
    .replace(/<[^>]*>/g, " ")
    .replace(/\[[^\]]*\]/g, " ")
    .replace(/\{[^}]*\}/g, " ");
  const tokens = text.split(/[.,\s]+/)
    .map(t => t.replace(/[^a-z]/gi, "").toLowerCase())
    .filter(t => /^[a-z]+$/.test(t));
  if (tokens.length) rows.push(tokens);
}
const total = new Map(), starts = new Map(), means = new Map(), variances = new Map();
for (const row of rows) {
  for (const t of row) total.set(t, (total.get(t) || 0) + 1);
  starts.set(row[0], (starts.get(row[0]) || 0) + 1);
  const counts = new Map();
  for (const t of row) counts.set(t, (counts.get(t) || 0) + 1);
  for (const [t, c] of counts) {
    const p = c / row.length;
    means.set(t, (means.get(t) || 0) + p);
    variances.set(t, (variances.get(t) || 0) + p * (1 - p));
  }
}
const candidates = [...total.entries()]
  .filter(([, n]) => n >= MIN_FREQ)
  .map(([token]) => token)
  .map(token => {
    const mu = means.get(token) || 0, v = variances.get(token) || 0;
    const observed = starts.get(token) || 0;
    return { token, frequency: total.get(token), observed, expected: mu,
      variance: v, z: v ? (observed - mu) / Math.sqrt(v) : 0 };
  })
  .sort((a, b) => b.z - a.z);
let seed = SEED;
function rand() {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  return seed / 4294967296;
}
const daiin = candidates.find(x => x.token === "daiin");
if (!daiin) throw new Error("daiin is not in the candidate family");
let exceedDaiin = 0, exceedObservedMax = 0;
for (let b = 0; b < B; b++) {
  const simulated = new Map();
  for (const row of rows) {
    const token = row[Math.floor(rand() * row.length)];
    simulated.set(token, (simulated.get(token) || 0) + 1);
  }
  let maxZ = -Infinity;
  for (const c of candidates) {
    if (!c.variance) continue;
    const z = ((simulated.get(c.token) || 0) - c.expected) / Math.sqrt(c.variance);
    if (z > maxZ) maxZ = z;
  }
  if (maxZ >= daiin.z) exceedDaiin++;
  if (maxZ >= candidates[0].z) exceedObservedMax++;
}
const result = {
  experiment: "EXP-592",
  parser: "IVTFF text rows only; strip angle, square-bracket, and brace annotations; split on period/comma/whitespace; alphabetic tokens only",
  input: path,
  text_lines: rows.length,
  tokens: rows.reduce((n, row) => n + row.length, 0),
  vocabulary: total.size,
  candidate_min_frequency: MIN_FREQ,
  candidates: candidates.length,
  simulations: B,
  seed: SEED,
  daiin: {
    frequency: daiin.frequency,
    observed_initial: daiin.observed,
    expected_initial: Number(daiin.expected.toFixed(3)),
    z: Number(daiin.z.toFixed(4)),
    familywise_p_maxT_at_daiin_threshold: Number(((exceedDaiin + 1) / (B + 1)).toFixed(5))
  },
  top_observed: candidates.slice(0, 12).map(c => ({
    token: c.token, frequency: c.frequency, initial: c.observed,
    expected: Number(c.expected.toFixed(3)), z: Number(c.z.toFixed(3))
  })),
  max_observed_token: candidates[0].token,
  max_observed_z: Number(candidates[0].z.toFixed(3)),
  p_maxT_at_observed_max: Number(((exceedObservedMax + 1) / (B + 1)).toFixed(5))
};
console.log(JSON.stringify(result, null, 2));
