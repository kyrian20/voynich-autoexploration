#!/usr/bin/env node
// Reproduce experiments 613–615 without third-party packages.
// Usage: node experiments/exp_613_615_ch_sh_inference_sensitivity/analyze.mjs data/transcriptions/eva_zl3b.txt data/transcriptions/eva_it2a.txt
import fs from 'node:fs';

function parse(raw, vowels = 'aeiouy') {
  let folio = null, meta = {}, rows = [];
  for (const line of raw.split(/\r?\n/)) {
    const h = line.match(/^<(f\d+[rv])>\s+<!([^>]*)>/);
    if (h) { folio = h[1]; meta = {}; for (const m of h[2].matchAll(/\$([A-Z])=([^\s>]+)/g)) meta[m[1]] = m[2]; continue; }
    const m = line.match(/^<(f\d+[rv])\.\d+,[^>]*>\s*(.*)$/);
    if (!m || !folio) continue;
    const body = m[2].replace(/<[^>]*>|\{[^}]*\}|\[[^\]]*\]|\$[^ ]*|@\d+;?/g, ' ');
    for (const token of (body.toLowerCase().match(/[a-z]+/g) || [])) {
      for (let i = 0; i < token.length - 1; i++) {
        const dg = token.slice(i, i + 2);
        if (dg === 'ch' || dg === 'sh') rows.push({ folio, q: meta.Q || '?', len: token.length, pos: i, dg, vowel: vowels.includes(token[i + 2] || '') });
      }
    }
  }
  return rows;
}
function analyze(raw, name, vowels = 'aeiouy', B = 20000, P = 20000, seed = 613) {
  const rows = parse(raw, vowels).filter(r => r.q === 'T'), map = new Map();
  for (const r of rows) {
    const k = `${r.folio}|${r.len}|${r.pos}`;
    if (!map.has(k)) map.set(k, { folio: r.folio, obs: [], chN: 0, shN: 0, chV: 0, shV: 0 });
    const c = map.get(k); c.obs.push(r);
    if (r.dg === 'ch') { c.chN++; if (r.vowel) c.chV++; } else { c.shN++; if (r.vowel) c.shV++; }
  }
  const cells = [...map.values()].filter(c => c.chN && c.shN), fm = new Map();
  for (const c of cells) {
    if (!fm.has(c.folio)) fm.set(c.folio, { folio: c.folio, chN: 0, shN: 0, chV: 0, shV: 0, cells: 0 });
    const f = fm.get(c.folio); f.chN += c.chN; f.shN += c.shN; f.chV += c.chV; f.shV += c.shV; f.cells++;
  }
  const fs = [...fm.values()], t = { chN: 0, shN: 0, chV: 0, shV: 0 };
  for (const f of fs) { t.chN += f.chN; t.shN += f.shN; t.chV += f.chV; t.shV += f.shV; }
  const pooled = { ch_n: t.chN, ch_vowels: t.chV, ch_rate: t.chV/t.chN, sh_n: t.shN, sh_vowels: t.shV, sh_rate: t.shV/t.shN, difference_sh_minus_ch: t.shV/t.shN-t.chV/t.chN };
  const ds = fs.map(f => f.shV/f.shN-f.chV/f.chN), estimate = ds.reduce((a,b)=>a+b,0)/ds.length;
  let state = seed >>> 0; const rnd = () => { state = (1664525*state+1013904223)>>>0; return state/4294967296; };
  const boot = [];
  for (let b=0;b<B;b++) { let s=0; for(let j=0;j<ds.length;j++) s += ds[Math.floor(rnd()*ds.length)]; boot.push(s/ds.length); }
  boot.sort((a,b)=>a-b); const quant=p=>boot[Math.floor((B-1)*p)];
  let extreme=0;
  for(let b=0;b<P;b++) {
    let chV=0,shV=0,chN=0,shN=0;
    for(const c of cells) {
      const ys=c.obs.map(o=>o.vowel?1:0);
      for(let i=ys.length-1;i>0;i--){const j=Math.floor(rnd()*(i+1));[ys[i],ys[j]]=[ys[j],ys[i]];}
      for(let i=0;i<ys.length;i++){if(i<c.chN){chN++;chV+=ys[i];}else{shN++;shV+=ys[i];}}
    }
    if(Math.abs(shV/shN-chV/chN)>=Math.abs(pooled.difference_sh_minus_ch)) extreme++;
  }
  const loo=fs.map(f=>{const chN=t.chN-f.chN,shN=t.shN-f.shN,chV=t.chV-f.chV,shV=t.shV-f.shV;return shV/shN-chV/chN;});
  return {dataset:name,metadata_filter:'IVTFF $Q=T',vowel_inventory:vowels,matched_cells:cells.length,matched_folios:fs.length,pooled_matched_occurrences:pooled,folio_equal_weight_mean_difference:estimate,folio_bootstrap:{replicates:B,seed,ci95_percentile:[quant(.025),quant(.975)]},within_cell_label_permutation:{replicates:P,seed,two_sided_p_plus_one:(extreme+1)/(P+1),extreme},leave_one_folio_out_pooled_difference_range:[Math.min(...loo),Math.max(...loo)],folio_summary:fs.map(f=>({folio:f.folio,ch_n:f.chN,ch_vowels:f.chV,sh_n:f.shN,sh_vowels:f.shV,difference_sh_minus_ch:f.shV/f.shN-f.chV/f.chN,matched_cells:f.cells}))};
}
const [zlPath,itPath]=process.argv.slice(2);
if(!zlPath||!itPath){console.error('Pass paths to ZL3b and IT2a transcriptions');process.exit(2);}
const zl=fs.readFileSync(zlPath,'utf8'), it=fs.readFileSync(itPath,'utf8');
console.log(JSON.stringify({experiment:'exp_613_615_ch_sh_inference_sensitivity',ZL3b:{aeiouy:analyze(zl,'ZL3b','aeiouy',20000,20000,613),aeiou:analyze(zl,'ZL3b','aeiou',20000,20000,615)},IT2a:{aeiouy:analyze(it,'IT2a','aeiouy',20000,20000,613),aeiou:analyze(it,'IT2a','aeiou',20000,20000,615)}},null,2));
