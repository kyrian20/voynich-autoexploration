#!/usr/bin/env python3
"""EXP-593: positional scan of daiin variants with max-statistic correction."""
from __future__ import annotations
import collections, hashlib, json, random, re
from datetime import datetime, timezone
from pathlib import Path
SOURCE = Path("data/transcriptions/eva_zl3b.txt")
OUT = Path("research/experiments")
N_PERM, SEED = 5000, 20261021
VARIANTS = ("daiin", "dain", "daiiin")
HEADER = re.compile(r"^<f(\d+[rv])>\s*(.*)$")
LINE = re.compile(r"^<f(\d+[rv])\.(\d+),[^>]*>\s*(.*)$")
TOKEN = re.compile(r"[a-z]+")

def parse():
    raw = SOURCE.read_bytes()
    text = raw.decode("utf-8-sig")
    classes = {}
    for row in text.splitlines():
        m = HEADER.match(row)
        if m:
            lang = re.search(r"\$L\s*=\s*([AB])(?:\s|$)", m.group(2))
            if lang: classes[m.group(1)] = lang.group(1)
    lines = []
    for row in text.splitlines():
        m = LINE.match(row)
        if not m: continue
        folio, number, body = m.groups()
        body = re.sub(r"<[^>]*>|\{[^}]*\}|\[[^\]]*\]", " ", body)
        toks = TOKEN.findall(body.lower())
        if toks:
            lines.append({"folio":folio,"line":int(number),"currier":classes.get(folio,"unknown"),"tokens":toks})
    return raw, lines

def main():
    if not SOURCE.exists(): raise SystemExit("Missing EVA transcription")
    raw, lines = parse()
    if len(lines) < 1000: raise SystemExit(f"Input sanity check failed: {len(lines)} lines")
    obs = {}
    for w in VARIANTS:
        by = collections.defaultdict(lambda:[0,0,0])
        for row in lines:
            t=row["tokens"]; by[row["currier"]][0]+=t.count(w)
            by[row["currier"]][1]+=int(t[0]==w); by[row["currier"]][2]+=int(t[-1]==w)
        occ=sum(x[0] for x in by.values()); ini=sum(x[1] for x in by.values()); fin=sum(x[2] for x in by.values())
        obs[w]={"occurrences":occ,"line_initial":ini,"line_final":fin,
                "initial_fraction":ini/occ if occ else None,
                "by_currier":{k:{"occurrences":v[0],"line_initial":v[1],"line_final":v[2]} for k,v in sorted(by.items())}}
    rng=random.Random(SEED); null={w:[] for w in VARIANTS}; max_null=[]
    for _ in range(N_PERM):
        counts={w:0 for w in VARIANTS}
        for row in lines:
            t=row["tokens"].copy(); rng.shuffle(t)
            if t:
                for w in VARIANTS: counts[w]+=int(t[0]==w)
        for w in VARIANTS: null[w].append(counts[w])
        max_null.append(max(counts.values()))
    tests={}
    for w in VARIANTS:
        observed=obs[w]["line_initial"]
        tests[w]={"null_mean_initial":sum(null[w])/N_PERM,
                  "empirical_p":(sum(x>=observed for x in null[w])+1)/(N_PERM+1),
                  "max_stat_adjusted_p":(sum(x>=observed for x in max_null)+1)/(N_PERM+1)}
    date=datetime.now(timezone.utc).strftime("%Y-%m-%d")
    result={"experiment":"EXP-593","title":"daiiin-family variants with max-statistic correction","date_utc":date,
      "source":str(SOURCE),"source_sha256":hashlib.sha256(raw).hexdigest(),
      "lines":len(lines),"tokens":sum(len(x["tokens"]) for x in lines),
      "variants":list(VARIANTS),"permutations":N_PERM,"seed":SEED,"observed":obs,"tests":tests,
      "null_model":"Shuffle token order independently within each line; preserves each line token multiset. Family-wise adjustment uses maximum initial-line count across the three prespecified variants per permutation.",
      "limitations":["Variant family is exploratory, not exhaustive.","EVA tokenization excludes uncertain bracketed readings and punctuation.",
      "This test concerns position only, not semantics or decipherment.","Currier classes are reported only where explicitly present in folio headers."]}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/f"{date}-exp593.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    report=f"# EXP-593 — Familia de variantes de daiin y corrección por comparaciones múltiples\n\n- Fecha UTC: {date}\n- SHA-256: {result['source_sha256']}\n- Líneas: {len(lines):,}\n- Tokens: {result['tokens']:,}\n- Permutaciones: {N_PERM:,}\n- Semilla: {SEED}\n\n| Token | Ocurrencias | Inicio | Final | p empírico | p ajustado max-stat |\n|---|---:|---:|---:|---:|---:|\n"
    for w in VARIANTS:
        o=obs[w]; t=tests[w]
        report+=f"| {w} | {o['occurrences']} | {o['line_initial']} | {o['line_final']} | {t['empirical_p']:.6f} | {t['max_stat_adjusted_p']:.6f} |\n"
    report+="\n## Distribución por clase Currier\n\n"
    for w in VARIANTS:
        report+=f"### {w}\n\n| Clase | Ocurrencias | Inicio | Final |\n|---|---:|---:|---:|\n"
        for c,v in obs[w]["by_currier"].items(): report+=f"| {c} | {v['occurrences']} | {v['line_initial']} | {v['line_final']} |\n"
        report+="\n"
    report+="## Interpretación y límites\n\nUn p ajustado bajo apoyaría una preferencia posicional frente a este modelo nulo, pero no implica traducción. La prueba conserva los tokens por línea, no la estructura sintáctica; el modelo nulo puede ser demasiado simple. La clasificación Currier depende de las cabeceras disponibles. Resultados completos en el JSON asociado.\n"
    (OUT/f"{date}-exp593.md").write_text(report,encoding="utf-8")
    print(json.dumps({"experiment":"EXP-593","lines":len(lines),"tokens":result["tokens"],"tests":tests},indent=2))
if __name__=="__main__": main()
