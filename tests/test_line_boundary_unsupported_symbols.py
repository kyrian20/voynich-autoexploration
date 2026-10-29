"""Prevent unsupported IVTFF/EVA characters from forging word boundaries.

Bounded code-regression and frozen-corpus candidate audit only: no model,
holdout score, historical output, or reserved leaf is recomputed.
"""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest

SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_unsupported_symbols", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(source, policy="primary"):
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "fixture.ivtff"
        path.write_text(source, encoding="latin-1")
        return module.parse(path, policy)


def previous_tokens(body, policy):
    """Exact candidate-token path before this patch (parent 7cb3242691fd).

    This is a *conditional code counterfactual*, not a reproduction of the
    original frozen results.json, which predates other independent repairs.
    """
    body = re.sub(r"<![^>]*>", "", body)
    body = body.replace("<%>", ".?.").replace("<$>", ".?.")
    body = re.sub(r"<[^>]*>", " ", body)
    if "<" in body or ">" in body:
        return [None]
    if policy == "drop_uncertain_word":
        body = re.sub(r"\[[^\]]*\]", "?", body)
    else:
        body = re.sub(r"\[([^:\]]*):[^\]]*\]", r"\1", body)
        body = re.sub(r"\[([^\]]*)\]", r"\1", body)
    if "[" in body or "]" in body:
        return [None]
    out = []
    for x in re.split(r"[.\s,]+", body):
        if not x:
            continue
        if ("?" in x or "{" in x or "}" in x or "@" in x or "/" in x
                or (policy == "drop_uncertain_word" and module.UNCERTAIN.search(x))):
            out.append(None)
            continue
        out.extend(w.lower() for w in re.findall(r"[A-Za-z]+", x))
    return out


class UnsupportedInlineSymbols(unittest.TestCase):
    def test_apostrophe_is_not_a_word_separator(self):
        for policy in ("primary", "drop_uncertain_word"):
            with self.subTest(policy=policy):
                self.assertEqual(module.tokens("alpha.qo'ky.beta", policy, True),
                                 ["alpha", None, "beta"])
                self.assertEqual(previous_tokens("alpha.qo'ky.beta", policy),
                                 ["alpha", "qo", "ky", "beta"])
                pages = fixture("<f1r.1,@P0> alpha.qo'ky\n"
                                "<f1r.2,+P0> gamma\n", policy)
                self.assertEqual(module.candidates(pages, ["f1r"]), [])

    def test_other_unadjudicated_symbols_fail_closed(self):
        for symbol in ("'", "2", "_", ";", "#", "@123;", "{ct}", "?"):
            with self.subTest(symbol=symbol):
                self.assertEqual(module.tokens("ab" + symbol + "cd", "primary", True),
                                 [None])
        self.assertEqual(module.tokens("alpha.beta", "primary", True),
                         ["alpha", "beta"])
        self.assertEqual(module.tokens("alpha<!note>beta", "primary", True),
                         ["alphabeta"])

    def test_safe_neighbors_and_cross_row_boundary_survive(self):
        pages = fixture("<f1r.1,@P0> alpha.beta.qo'ky.gamma.delta\n"
                        "<f1r.2,+P0> epsilon\n")
        self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])],
                         [0, 0, 1])

    def test_authenticated_frozen_corpus_delta(self):
        # Exact source hashes must pass before inspection; this audit is a
        # census over candidate construction, not a predictive rerun.
        expected = {
            "ZL3b": {"primary_changed_rows": 22,
                     "drop_uncertain_word_changed_rows": 21,
                     "positive_removed": 9,
                     "primary": 55, "drop_uncertain_word": 53},
            "IT2a": {"primary_changed_rows": 0,
                     "drop_uncertain_word_changed_rows": 0,
                     "positive_removed": 0,
                     "primary": 0, "drop_uncertain_word": 0},
        }
        for label, path in module.INPUTS.items():
            self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])
            bodies = {}
            for lineno, raw in module.checked_physical_lines(
                    path.read_text(encoding="latin-1")):
                match = module.ROW.match(raw.strip())
                if match:
                    bodies[lineno] = match["body"] or ""
            for policy in ("primary", "drop_uncertain_word"):
                with self.subTest(label=label, policy=policy):
                    # Historical conditional delta predates comma quarantine.
                    # Pin the old split policy to preserve that audit's scope.
                    pages = module.parse(path, policy, uncertain_space_policy="split")
                    previous = copy.deepcopy(pages)
                    changed = 0
                    for rows in previous.values():
                        for row in rows:
                            old = previous_tokens(bodies[row["line"]], policy)
                            if old != row["words"]:
                                changed += 1
                            row["words"] = old
                    corrected = module.candidates(pages, sorted(pages))
                    prior = module.candidates(previous, sorted(previous))
                    positives = sum(r["y"] for r in prior) - sum(r["y"] for r in corrected)
                    negatives = (sum(r["y"] == 0 for r in prior)
                                 - sum(r["y"] == 0 for r in corrected))
                    self.assertEqual(changed, expected[label][policy + "_changed_rows"])
                    self.assertEqual(positives, expected[label]["positive_removed"])
                    self.assertEqual(negatives, expected[label][policy])
                    self.assertEqual(len(prior) - len(corrected), positives + negatives)
                    print(f"{label} {policy}: source SHA256 OK; affected P rows={changed}; "
                          f"candidate positives excluded={positives}; "
                          f"candidate negatives excluded={negatives}")


if __name__ == "__main__":
    unittest.main()
