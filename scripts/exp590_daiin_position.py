#!/usr/bin/env python3
"""Reproducible, API-free positional baseline for the Voynich EVA transcription."""
from __future__ import annotations
import collections
import hashlib
import json
import math
import random
import re
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_ivtff_metadata import parse_currier_language
from scripts.audit_ivtff_ligature_views import legacy_parser_coverage

SOURCE = ROOT / "data/transcriptions/eva_zl3b.txt"
OUT = ROOT / "research/experiments"
N_PERM = 5000
SEED = 20261020
FOLIO_HEADER = re.compile(r"^<(f(?:\d+[rv][1-6]?|Ros))>\s*(.*)$")
TEXT_LINE = re.compile(r"^<(f(?:\d+[rv][1-6]?|Ros))\.(\d+),[^>]*>\s*(.*)$")
TOKEN_RE = re.compile(r"[a-z]+")
TARGET = "daiin"


def load_lines(path: Path):
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig")
    folio_currier: dict[str, str] = {}
    for row in text.splitlines():
        m = FOLIO_HEADER.match(row)
        if m:
            lang = parse_currier_language(m.group(2))
            if lang:
                folio_currier[m.group(1)] = lang
    parsed = []
    for row in text.splitlines():
        m = TEXT_LINE.match(row)
        if not m:
            continue
        folio, line_no, body = m.groups()
        body = re.sub(r"<[^>]*>|\{[^}]*\}|\[[^\]]*\]", " ", body)
        tokens = TOKEN_RE.findall(body.lower())
        if tokens:
            parsed.append({"folio": folio, "line": int(line_no),
                           "currier": folio_currier.get(folio, "unknown"),
                           "tokens": tokens})
    return raw, parsed


def measure(lines):
    target_n = first_n = last_n = 0
    by_currier = collections.defaultdict(lambda: [0, 0, 0, 0])
    for line in lines:
        toks = line["tokens"]
        n = toks.count(TARGET)
        target_n += n
        first_n += int(toks[0] == TARGET)
        last_n += int(toks[-1] == TARGET)
        row = by_currier[line["currier"]]
        row[0] += n
        row[1] += int(toks[0] == TARGET)
        row[2] += int(toks[-1] == TARGET)
        row[3] += 1
    return {
        "tokens": sum(len(x["tokens"]) for x in lines),
        "lines": len(lines),
        "target_occurrences": target_n,
        "line_initial_occurrences": first_n,
        "line_final_occurrences": last_n,
        "initial_rate_per_target_occurrence": first_n / target_n if target_n else None,
        "final_rate_per_target_occurrence": last_n / target_n if target_n else None,
        "currier": {
            k: {"target_occurrences": v[0], "line_initial_lines": v[1],
                "line_final_lines": v[2], "lines": v[3]}
            for k, v in sorted(by_currier.items())
        },
    }


def permutation_test(lines, observed, n_perm=N_PERM, seed=SEED):
    # Null: within each line, token order is exchangeable. Each permutation
    # preserves each line's exact token multiset and tests only line-initial position.
    rng = random.Random(seed)
    null = []
    for _ in range(n_perm):
        count = 0
        for line in lines:
            # Only the first token matters for this statistic. Sampling one
            # uniformly random token is exactly equivalent to shuffling the
            # line and inspecting position zero, but avoids shuffling every
            # token in every replicate.
            toks = line["tokens"]
            count += int(bool(toks) and rng.choice(toks) == TARGET)
        null.append(count)
    mean = sum(null) / n_perm
    ge = sum(x >= observed for x in null)
    return {
        "permutations": n_perm, "seed": seed,
        "null_mean_initial_lines": mean,
        "null_sd_initial_lines": (sum((x - mean) ** 2 for x in null) / n_perm) ** 0.5,
        "empirical_one_sided_p": (ge + 1) / (n_perm + 1),
        "null_ge_observed": ge,
        "interpretation": "Exploratory positional test; not a decipherment claim.",
    }



def archive_paths(date: str):
    """Use date-specific historical names without ever overwriting an archive."""
    return (OUT / f"{date}-exp590-corrected-L-metadata.json",
            OUT / f"{date}-exp590-corrected-L-metadata.md")


def _unique_json_pairs(pairs):
    """Reject ambiguous JSON even if the duplicate would otherwise be ignored."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def archive_status(paths, date: str, source_sha: str):
    """Return new/existing, rejecting incomplete or inconsistent frozen outputs.

    This checks the archive's structure and internal consistency, NOT independent
    regeneration of its permutation distribution or scientific validity.
    """
    if any(path.is_symlink() for path in paths):
        raise RuntimeError("EXP-590 archive destination is a symlink")
    present = [path.exists() for path in paths]
    if not any(present):
        return "new"
    if not all(present) or not all(path.is_file() for path in paths):
        raise RuntimeError("EXP-590 archive is partial or not a regular file; manual adjudication required")
    try:
        saved = json.loads(paths[0].read_text(encoding="utf-8"),
                           object_pairs_hook=_unique_json_pairs)
        report = paths[1].read_text(encoding="utf-8")
    except (OSError, UnicodeError, ValueError) as exc:
        raise RuntimeError("EXP-590 archive is unreadable or ambiguous; refusing replacement") from exc
    expected = {"experiment": "EXP-590", "date_utc": date,
                "source": "data/transcriptions/eva_zl3b.txt",
                "source_sha256": source_sha, "target": TARGET}
    if not isinstance(saved, dict) or any(saved.get(k) != value for k, value in expected.items()):
        raise RuntimeError("EXP-590 archived provenance differs; refusing replacement")
    metrics, perm = saved.get("metrics"), saved.get("permutation_test")
    if not isinstance(metrics, dict) or not isinstance(perm, dict):
        raise RuntimeError("EXP-590 archive missing metrics or permutation metadata")
    if perm.get("seed") != SEED or perm.get("permutations") != N_PERM:
        raise RuntimeError("EXP-590 archived permutation settings differ")
    def nonnegative_int(value):
        return type(value) is int and value >= 0
    keys = ("tokens", "lines", "target_occurrences",
            "line_initial_occurrences", "line_final_occurrences")
    if not all(nonnegative_int(metrics.get(k)) for k in keys):
        raise RuntimeError("EXP-590 archive has invalid count fields")
    if metrics["lines"] < 100 or metrics["target_occurrences"] < 20 or metrics["tokens"] < metrics["lines"]:
        raise RuntimeError("EXP-590 archived population fails sanity checks")
    occurrences = metrics["target_occurrences"]
    first, last = metrics["line_initial_occurrences"], metrics["line_final_occurrences"]
    if first > occurrences or last > occurrences or first > metrics["lines"] or last > metrics["lines"]:
        raise RuntimeError("EXP-590 archive has impossible positional counts")
    for key, numerator in (("initial_rate_per_target_occurrence", first),
                           ("final_rate_per_target_occurrence", last)):
        value = metrics.get(key)
        if type(value) not in (int, float) or not math.isfinite(value) or not math.isclose(
                value, numerator / occurrences, rel_tol=0, abs_tol=1e-12):
            raise RuntimeError("EXP-590 archived fraction is inconsistent")
    classes = metrics.get("currier")
    if not isinstance(classes, dict) or not classes or not set(classes) <= {"A", "B", "unknown"}:
        raise RuntimeError("EXP-590 archive has invalid Currier classes")
    totals = [0, 0, 0, 0]
    table_rows = []
    for name, row in sorted(classes.items()):
        if not isinstance(row, dict):
            raise RuntimeError("EXP-590 archive has invalid Currier row")
        fields = ("target_occurrences", "line_initial_lines", "line_final_lines", "lines")
        if not all(nonnegative_int(row.get(k)) for k in fields):
            raise RuntimeError("EXP-590 archive has invalid Currier counts")
        n, i, f, line_count = (row[k] for k in fields)
        if i > n or f > n or i > line_count or f > line_count:
            raise RuntimeError("EXP-590 archive has impossible Currier positions")
        for idx, val in enumerate((n, i, f, line_count)):
            totals[idx] += val
        table_rows.append(f"| {name} | {n} | {i} | {f} | {line_count} |")
    if totals != [occurrences, first, last, metrics["lines"]]:
        raise RuntimeError("EXP-590 Currier totals do not match the archive")
    p = perm.get("empirical_one_sided_p")
    mean = perm.get("null_mean_initial_lines")
    sd = perm.get("null_sd_initial_lines")
    ge = perm.get("null_ge_observed")
    if (not all(type(x) in (int, float) and math.isfinite(x) for x in (p, mean, sd))
            or not nonnegative_int(ge) or ge > N_PERM or sd < 0 or mean < 0
            or not math.isclose(p, (ge + 1) / (N_PERM + 1), rel_tol=0, abs_tol=1e-12)):
        raise RuntimeError("EXP-590 archive has inconsistent null statistics")
    markers = [
        f"- Fecha UTC: {date}",
        f"- SHA-256 de la transcripción: {source_sha}",
        f"- Líneas EVA parseadas: {metrics['lines']:,}",
        f"- Tokens parseados: {metrics['tokens']:,}",
        f"- Ocurrencias exactas de daiin: {occurrences:,}",
        f"- Ocurrencias en primera posición de línea: {first:,}",
        f"- Ocurrencias en última posición de línea: {last:,}",
        f"- Permutaciones: {N_PERM:,}",
        f"- Semilla fija: {SEED}",
        f"- p empírico unilateral con corrección +1: {p:.6f}",
        *table_rows,
    ]
    if any(report.splitlines().count(marker) != 1 for marker in markers):
        raise RuntimeError("EXP-590 report disagrees with its JSON or is truncated")
    return "existing"


def write_archive_pair(paths, json_text: str, report: str):
    """Exclusive create: no existing result may be silently replaced.

    A crash between writes leaves a partial pair requiring human adjudication.
    """
    OUT.mkdir(parents=True, exist_ok=True)
    with paths[0].open("x", encoding="utf-8") as handle:
        handle.write(json_text)
    with paths[1].open("x", encoding="utf-8") as handle:
        handle.write(report)


def main():
    if not SOURCE.exists():
        raise SystemExit(f"Missing transcription: {SOURCE}")
    raw, lines = load_lines(SOURCE)
    if len(lines) < 100:
        raise SystemExit(f"Refusing to report: only {len(lines)} parsed text lines.")
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    digest = hashlib.sha256(raw).hexdigest()
    paths = archive_paths(date)
    if archive_status(paths, date, digest) == "existing":
        print(json.dumps({"experiment": "EXP-590", "status": "skipped_existing",
                          "date_utc": date, "note": "No permutation rerun; no files replaced."}))
        return
    metrics = measure(lines)
    if metrics["target_occurrences"] < 20:
        raise SystemExit("Refusing to report: too few exact daiin occurrences.")
    perm = permutation_test(lines, metrics["line_initial_occurrences"])
    result = {
        "experiment": "EXP-590",
        "title": "daiin line-initial positional baseline",
        "date_utc": date, "source": str(SOURCE.relative_to(ROOT)), "source_sha256": digest,
        "tokenization": "lowercase ASCII alphabetic runs after removing IVTFF tags, braces and square-bracket annotations",
        "target": TARGET, "metrics": metrics, "permutation_test": perm,
        "coverage_comparison": {
            "legacy_restricted_pattern": legacy_parser_coverage(raw.decode("utf-8-sig")),
            "current_nonempty_token_lines": metrics["lines"],
            "scope": "Different page-ID coverage; these are not identical populations.",
        },
        "limitations": [
            "EVA transcription and tokenization choices affect counts.",
            "Only exact token daiin is tested; variants such as dain are excluded.",
            "Line-initial permutation test conditions on each line's token multiset.",
            "Currier classification is read only from the IVTFF $L page variable; unknowns remain unknown.",
            "This is descriptive statistical analysis, not a translation or decipherment.",
            "The empirical p-value is not adjusted for prior selection of daiin among other candidate words or for other exploratory analyses of the same transcription; interpret it as exploratory rather than confirmatory.",
            "The ASCII-letter token filter does not decode extended glyph codes such as @140; raw source records remain preserved."
        ],
    }
    p = perm["empirical_one_sided_p"]
    report = f"""# EXP-590 — Posición inicial de daiin

- Fecha UTC: {date}
- Fuente: {SOURCE.relative_to(ROOT)}
- SHA-256 de la transcripción: {digest}
- Líneas EVA parseadas: {metrics['lines']:,}
- Tokens parseados: {metrics['tokens']:,}
- Ocurrencias exactas de daiin: {metrics['target_occurrences']:,}
- Ocurrencias en primera posición de línea: {metrics['line_initial_occurrences']:,}
- Ocurrencias en última posición de línea: {metrics['line_final_occurrences']:,}
- Fracción de ocurrencias en primera posición: {metrics['initial_rate_per_target_occurrence']:.4f}
- Fracción de ocurrencias en última posición: {metrics['final_rate_per_target_occurrence']:.4f}

## Contraste de permutación

- Permutaciones: {perm['permutations']:,}
- Semilla fija: {perm['seed']}
- Media nula de líneas que empiezan por daiin: {perm['null_mean_initial_lines']:.3f}
- Desviación típica nula: {perm['null_sd_initial_lines']:.3f}
- p empírico unilateral con corrección +1: {p:.6f}

La hipótesis nula permuta el orden de los tokens dentro de cada línea, conservando su multiconjunto exacto. El contraste evalúa si daiin aparece al principio de línea más de lo esperable bajo ese modelo; no prueba significado lingüístico. No se han explorado múltiples palabras en este experimento, pero cualquier búsqueda posterior deberá corregir comparaciones múltiples.

**Precaución inferencial:** el valor p no corrige la selección histórica de daiin entre otras palabras ni otros análisis de esta transcripción. Es un contraste exploratorio bajo el nulo elegido, no una prueba confirmatoria independiente.

## Distribución por clase de Currier

| Clase | Ocurrencias exactas | Líneas iniciales | Líneas finales | Líneas parseadas |
|---|---:|---:|---:|---:|
"""
    for key, val in sorted(metrics["currier"].items()):
        report += f"| {key} | {val['target_occurrences']} | {val['line_initial_lines']} | {val['line_final_lines']} | {val['lines']} |\n"
    report += """
## Limitaciones y reproducibilidad

- Solo se cuenta el token exacto daiin; no se mezclan variantes como dain.
- La tokenización elimina etiquetas IVTFF y material entre llaves/corchetes; los resultados dependen de esa decisión.
- La clasificación Currier se lee de cabeceras de folio cuando está disponible; los casos sin clasificación quedan como unknown.
- Esto es una línea base exploratoria reproducible, no una traducción ni una afirmación de desciframiento.
- Datos completos y hash de entrada están en el JSON de este experimento.
"""
    legacy = result["coverage_comparison"]["legacy_restricted_pattern"]
    report += "\n## Cobertura histórica y actual\n\n| Métrica | Patrón restringido histórico | Patrón actual |\n|---|---:|---:|\n"
    for label, old_key, new_key in [("Líneas con tokens", "nonempty_token_lines", "lines"), ("Tokens", "tokens", "tokens"), ("daiin exactos", "exact_daiin_occurrences", "target_occurrences"), ("Inicios daiin", "line_initial_daiin_lines", "line_initial_occurrences")]:
        report += f"| {label} | {legacy[old_key]} | {metrics[new_key]} |\n"
    report += "\nLas columnas usan distinta cobertura de identificadores; no describen idéntica población. El filtro ASCII no decodifica los códigos de caracteres extendidos @…;. Se conserva la transcripción bruta. Véase la auditoría operativa para el cotejo exacto de registros excluidos.\n"
    write_archive_pair(paths, json.dumps(result, indent=2, ensure_ascii=False) + "\n", report)
    print(json.dumps({"experiment": "EXP-590", "date_utc": date, "lines": metrics["lines"],
                      "tokens": metrics["tokens"], "daiin": metrics["target_occurrences"],
                      "initial": metrics["line_initial_occurrences"], "p": p,
                      "source_sha256": digest}, indent=2))


if __name__ == "__main__":
    main()
