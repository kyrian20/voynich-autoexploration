#!/usr/bin/env python3
"""Exploratory partial reconstruction of Zhang & Sheng's word-pair metric.

Uses repository-pinned EVA transcriptions and the repository's lossless IVTFF
lexer. The paper does not publish the exact per-word residualization rule or
code as of 2026-11-01, so this script reports an explicit additive-effect
residualization and a raw-score sensitivity, not an exact paper replication.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import hashlib
import json
import math
import random
import re
from pathlib import Path
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = next((parent for parent in (SCRIPT_DIR, *SCRIPT_DIR.parents)
             if (parent / "data/transcriptions/eva_zl3b.txt").exists()), SCRIPT_DIR)
TRANSCRIPTION_DIR = ROOT / "data/transcriptions" if (ROOT / "data/transcriptions").is_dir() else ROOT
sys.path.insert(0, str(ROOT))

from scripts.ivtff_lossless import lex
from scripts.ivtff_rows import tokens_rows
HEADER = re.compile(r"^<(f[^>]+)>\s*(.*)$")
PAGE_ID = re.compile(r"^(f(?:[0-9]+[rv][1-6]?|Ros))")
PAGE_NO = re.compile(r"^(?:f)(\d+)[rv]")
LEGACY_TEXT_LINE = re.compile(r"^<(f(?:\d+[rv][1-6]?|Ros))\.(\d+),([^>]*)>\s*(.*)$")
LEGACY_TOKEN = re.compile(r"[a-z]+")
# Fixed input identity of the published partial audit (2026-11-01).
# Git SHA-1 is Git's blob identity; SHA-256 is the independent byte lock.
SOURCE_LOCK = {
    "eva_zl3b.txt": (
        "bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
        "2a4533ab9bdfa85db9bad602d590978953055df1",
    ),
    "eva_it2a.txt": (
        "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5",
        "4d6d3f2537b1f507a257529b49c94af7d6e03446",
    ),
}


def load_verified_source(path: Path):
    """Return one immutable text snapshot and its verified source receipt.

    Fail closed before any metric calculation on unknown, redirected or
    modified inputs. The returned snapshot is used by both reader policies,
    avoiding a second file read after hashing.
    """
    if path.name not in SOURCE_LOCK:
        raise ValueError(f"Unregistered word-pair source: {path.name}")
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError(f"Symlinked word-pair source forbidden: {path}")
    raw = path.read_bytes()
    sha256 = hashlib.sha256(raw).hexdigest()
    blob_sha = hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()
    expected_sha256, expected_blob_sha = SOURCE_LOCK[path.name]
    if (sha256, blob_sha) != (expected_sha256, expected_blob_sha):
        raise ValueError(
            f"Frozen word-pair source mismatch: {path.name}; "
            f"sha256={sha256} git_blob_sha={blob_sha}"
        )
    return raw.decode("utf-8"), {"git_blob_sha": blob_sha, "sha256": sha256}


def read_pages_legacy(path: Path, *, categories=None, keep_empty=False, source_text=None):
    """Recreate the project's EXP-590 ASCII token projection for comparison."""
    pages, current = [], None
    for rawline in (source_text if source_text is not None else path.read_text(encoding="utf-8-sig")).splitlines():
        match = HEADER.match(rawline)
        if match and "." not in match.group(1):
            locus, body = match.groups()
            page_match = PAGE_ID.match(locus)
            if not page_match:
                current = None
                continue
            meta = re.search(r"\$L=([AB])", body)
            current = {"id": page_match.group(1), "currier": meta.group(1) if meta else None,
                       "rows": []}
            pages.append(current)
            continue
        match = LEGACY_TEXT_LINE.match(rawline)
        if not match or current is None:
            continue
        folio, _, tag, body = match.groups()
        if folio != current["id"]:
            raise ValueError(f"Page/locus mismatch: page={current['id']} locus={folio}")
        category_match = re.search(r"[A-Z]", tag)
        category = category_match.group(0) if category_match else None
        if categories is not None and category not in categories:
            continue
        body = re.sub(r"<[^>]*>|\{[^}]*\}|\[[^\]]*\]", " ", body)
        words = LEGACY_TOKEN.findall(body.lower())
        if words:
            current["rows"].append(words)
    for page in pages:
        page["lines"] = page.pop("rows")
    return pages if keep_empty else [p for p in pages if p["lines"]]


def eva_glyphs(word: str) -> list[str]:
    """Split EVA words into glyphs, keeping the six documented digraphs atomic."""
    glyphs = []
    i = 0
    digraphs = ("cth", "ckh", "cph", "cfh", "ch", "sh")
    while i < len(word):
        if word[i] == "@":
            match = re.match(r"@[0-9]{3};", word[i:])
            if match:
                glyphs.append(match.group(0))
                i += len(match.group(0))
                continue
        matched = next((g for g in digraphs if word.startswith(g, i)), None)
        if matched:
            glyphs.append(matched)
            i += len(matched)
        else:
            glyphs.append(word[i])
            i += 1
    return glyphs


def levenshtein_at_most_one(a: str, b: str) -> bool:
    a, b = eva_glyphs(a), eva_glyphs(b)
    if a == b:
        return True
    if abs(len(a) - len(b)) > 1:
        return False
    i = j = edits = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
            j += 1
            continue
        edits += 1
        if edits > 1:
            return False
        if len(a) > len(b):
            i += 1
        elif len(b) > len(a):
            j += 1
        else:
            i += 1
            j += 1
    if i < len(a) or j < len(b):
        edits += 1
    return edits == 1


def read_pages(path: Path, *, uncertain_space="split", categories=None, keep_empty=False, source_text=None):
    pages = []
    current = None
    for rawline in (source_text if source_text is not None else path.read_text(encoding="utf-8")).splitlines():
        match = HEADER.match(rawline)
        if not match:
            continue
        locus, payload_text = match.groups()
        if "." not in locus:
            page_match = PAGE_ID.match(locus)
            if not page_match:
                continue
            meta = re.search(r"\$L=([AB])", payload_text)
            current = {"id": page_match.group(1), "currier": meta.group(1) if meta else None,
                       "rows": []}
            pages.append(current)
            continue
        if current is None:
            raise ValueError(f"Text line before page header: {locus}")
        if not locus.startswith(current["id"] + "."):
            raise ValueError(f"Page/locus mismatch: page={current['id']} locus={locus}")
        tag = locus.split(",", 1)[1] if "," in locus else ""
        category_match = re.search(r"[A-Z]", tag)
        category = category_match.group(0) if category_match else None
        if categories is not None and category not in categories:
            continue
        payload = lex(payload_text)
        if payload.diagnostics:
            raise ValueError(f"IVTFF diagnostics at {locus}: {payload.diagnostics}")
        current["rows"].append((locus, payload))

    # Project each continuous slash-continuation chain as one logical line.
    for page in pages:
        lines = []
        chain_loci, chain = [], []
        for locus, payload in page["rows"]:
            chain_loci.append(locus)
            chain.append(payload)
            trailing = bool(payload.spans and payload.spans[-1].kind == "continuation")
            if not trailing:
                lines.append({"loci": chain_loci[:], "tokens": tokens_rows(chain, uncertain_space=uncertain_space)})
                chain_loci, chain = [], []
        if chain:
            raise ValueError(f"Incomplete continuation at {chain_loci[-1]}")
        page["lines"] = [line["tokens"] for line in lines if line["tokens"]]
        page["line_loci"] = [line["loci"] for line in lines if line["tokens"]]
    return pages if keep_empty else [p for p in pages if p["lines"]]


def increment_pairs(lines, type_ids, allowed, into):
    for line in lines:
        ids = sorted({type_ids[w] for w in line if w in type_ids})
        for i, j in combinations(ids, 2):
            if allowed[i][j]:
                into[i][j] += 1


def ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i + 1
        while j < len(order) and values[order[j]] == values[order[i]]:
            j += 1
        rank = ((i + 1) + j) / 2.0
        for k in range(i, j):
            out[order[k]] = rank
        i = j
    return out


def pearson(a, b):
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    da, db = [x - ma for x in a], [x - mb for x in b]
    den = math.sqrt(sum(x*x for x in da) * sum(y*y for y in db))
    return sum(x*y for x, y in zip(da, db)) / den if den else float("nan")


def spearman(a, b):
    return pearson(ranks(a), ranks(b))


def additive_residual(matrix, n, pair_idx):
    import numpy as np  # Only needed for full metrics; source-lock tests use stdlib.
    # OLS fit of z_ij = alpha_i + alpha_j only over eligible pairs.
    design = np.zeros((n, n), dtype=float)
    rhs = np.zeros(n, dtype=float)
    for i, j in pair_idx:
        design[i, i] += 1.0
        design[j, j] += 1.0
        design[i, j] += 1.0
        design[j, i] += 1.0
        rhs[i] += matrix[i][j]
        rhs[j] += matrix[i][j]
    alpha = np.linalg.solve(design, rhs)
    out = [[0.0] * n for _ in range(n)]
    for i, j in pair_idx:
        out[i][j] = out[j][i] = matrix[i][j] - alpha[i] - alpha[j]
    return out


def metric(pages, *, seed=20261101, shuffles=20, top_k=300):
    all_lines = [line for page in pages for line in page["lines"]]
    freq = Counter(w for line in all_lines for w in line)
    vocab = sorted(freq, key=lambda w: (-freq[w], w))[:top_k]
    n = len(vocab)
    type_ids = {w: i for i, w in enumerate(vocab)}
    allowed = [[False] * n for _ in range(n)]
    pair_idx = []
    for i, j in combinations(range(n), 2):
        if not levenshtein_at_most_one(vocab[i], vocab[j]):
            allowed[i][j] = True
            allowed[j][i] = True
            pair_idx.append((i, j))

    halves = [[], []]
    for page_index, page in enumerate(pages):
        half = (page_index // 10) % 2
        halves[half].append((page_index, page))
    observed = [[[0] * n for _ in range(n)] for _ in range(2)]
    for h in range(2):
        for _, page in halves[h]:
            increment_pairs(page["lines"], type_ids, allowed, observed[h])

    expected = [[[0.0] * n for _ in range(n)] for _ in range(2)]
    rng = random.Random(seed)
    for _ in range(shuffles):
        shuffled_counts = [[[0] * n for _ in range(n)] for _ in range(2)]
        for page_index, page in enumerate(pages):
            lines = page["lines"]
            movable = [w for line in lines for w in line[1:-1]]
            rng.shuffle(movable)
            k = 0
            shuffled_lines = []
            for line in lines:
                middle = len(line[1:-1])
                shuffled_lines.append(line[:1] + movable[k:k+middle] + (line[-1:] if len(line) > 1 else []))
                k += middle
            half = (page_index // 10) % 2
            increment_pairs(shuffled_lines, type_ids, allowed, shuffled_counts[half])
        for h in range(2):
            for i, j in pair_idx:
                expected[h][i][j] += shuffled_counts[h][i][j] / shuffles
                expected[h][j][i] += shuffled_counts[h][j][i] / shuffles

    z = []
    for h in range(2):
        mat = [[0.0] * n for _ in range(n)]
        for i, j in pair_idx:
            e = expected[h][i][j]
            v = (observed[h][i][j] - e) / math.sqrt(e + 0.5)
            mat[i][j] = mat[j][i] = v
        z.append(mat)
    residual = [additive_residual(z[h], n, pair_idx) for h in range(2)]
    raw_a = [z[0][i][j] for i, j in pair_idx]
    raw_b = [z[1][i][j] for i, j in pair_idx]
    res_a = [residual[0][i][j] for i, j in pair_idx]
    res_b = [residual[1][i][j] for i, j in pair_idx]
    return {
        "n_pages": len(pages), "n_lines": len(all_lines), "n_tokens": sum(map(len, all_lines)),
        "n_types": n, "n_eligible_pairs": len(pair_idx), "shuffles": shuffles, "seed": seed,
        "split": "alternating blocks of 10 pages in source order",
        "score_raw_spearman": spearman(raw_a, raw_b),
        "score_additive_propensity_residual_spearman": spearman(res_a, res_b),
        "score_pearson_residuals": pearson(res_a, res_b),
        "implementation_choices": {
            "top_k_tie_break": "frequency descending, EVA token ascending",
            "near_copy_exclusion": "EVA glyph-level word-type Levenshtein distance <= 1",
            "word_view": "uncertain spaces split; primary alternatives; expand ligatures",
            "shuffle": "uniform permutation of interior tokens across all lines within each page; line endpoints fixed",
            "propensity_removal": "OLS additive word effects alpha_i + alpha_j fitted separately per half",
            "shuffled_expected": "mean co-line counts across 20 randomizations; same fixed global vocabulary",
        },
    }



def flatten_run_records(results):
    """Serialize computed metrics to the *existing* frozen results.json schema.

    The first version of main() emitted a nested "results" object although
    the archived artifact stores 54 flat "run_records". This projection
    changes only the receipt format, never the underlying metric values.
    """
    records = []
    for source, views in results.items():
        for view, grids in views.items():
            for top_k, runs in grids.items():
                for run in runs:
                    records.append({
                        "source": source,
                        "view": view,
                        "top_k": int(top_k),
                        "seed": run["seed"],
                        "shuffles": run["shuffles"],
                        "pages": run["n_pages"],
                        "lines": run["n_lines"],
                        "tokens": run["n_tokens"],
                        "eligible_pairs": run["n_eligible_pairs"],
                        "raw_spearman": run["score_raw_spearman"],
                        "additive_residual_spearman": run["score_additive_propensity_residual_spearman"],
                        "residual_pearson": run["score_pearson_residuals"],
                    })
    return records

def main():
    results = {}
    source_metadata = {}
    for name in ("eva_zl3b.txt", "eva_it2a.txt"):
        results[name] = {}
        source = TRANSCRIPTION_DIR / name
        source_text, source_metadata[name] = load_verified_source(source)
        for policy in ("split", "join"):
            pages = read_pages(source, uncertain_space=policy, categories={"P", "C", "R"}, keep_empty=True, source_text=source_text)
            pages = [page for page in pages if page["id"] not in {"f116v", "fRos"}]
            results[name][policy] = {
                str(k): [metric(pages, seed=20261101 + seed_offset, shuffles=20, top_k=k)
                         for seed_offset in (0, 1, 2)]
                for k in (150, 300, 600)
            }
        legacy_pages = read_pages_legacy(source, categories={"P", "C", "R"}, keep_empty=True, source_text=source_text)
        legacy_pages = [page for page in legacy_pages if page["id"] not in {"f116v", "fRos"}]
        results[name]["legacy_ascii"] = {
            str(k): [metric(legacy_pages, seed=20261101 + seed_offset, shuffles=20, top_k=k)
                     for seed_offset in (0, 1, 2)]
            for k in (150, 300, 600)
        }
    print(json.dumps({"status": "EXPLORATORY_PARTIAL_REIMPLEMENTATION",
                      "sources": source_metadata,
                      "run_records": flatten_run_records(results)}, indent=2))


if __name__ == "__main__":
    main()
