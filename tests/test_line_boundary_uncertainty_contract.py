"""Regression: bracketed IVTFF uncertainty must not survive exclusion policy."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


SCRIPT = (Path(__file__).resolve().parents[1] / "research" / "analysis" /
          "2026-10-28-line-boundary-reproduction" / "line_boundary_replication.py")
spec = importlib.util.spec_from_file_location("line_boundary_replication", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class UncertaintyPolicyContract(unittest.TestCase):
    def test_primary_reading_unchanged(self):
        self.assertEqual(module.tokens("ab[cd:ef]gh", "primary"), ["abcdgh"])

    def test_bracket_alternative_embedded_word_excluded(self):
        self.assertEqual(module.tokens("ab[cd:ef]gh", "drop_uncertain_word"), [])

    def test_bracket_only_word_excluded(self):
        self.assertEqual(module.tokens("[cd:ef]", "drop_uncertain_word"), [])

    def test_bracket_without_alternative_excluded(self):
        self.assertEqual(module.tokens("ab[cd]gh", "drop_uncertain_word"), [])

    def test_neighbouring_certain_words_preserved(self):
        self.assertEqual(module.tokens("safe.ab[cd:ef]gh.clean", "drop_uncertain_word"),
                         ["safe", "clean"])

    def test_ligature_and_question_mark_still_excluded(self):
        self.assertEqual(module.tokens("ab{cd}gh", "drop_uncertain_word"), [])
        self.assertEqual(module.tokens("ab?gh", "drop_uncertain_word"), [])

    def test_certain_words_unchanged(self):
        self.assertEqual(module.tokens("safe.clean", "drop_uncertain_word"),
                         ["safe", "clean"])

    def test_uncertain_word_is_a_barrier_not_a_new_adjacent_pair(self):
        words = module.tokens("safe.ab[cd:ef]gh.clean", "drop_uncertain_word",
                              preserve_gaps=True)
        self.assertEqual(words, ["safe", None, "clean"])
        pages = {"f1r": [{"words": words, "text": "safe <UNCERTAIN> clean",
                          "leaf": 1}]}
        self.assertEqual(module.candidates(pages, ["f1r"]), [])

    def test_uncertain_line_blocks_false_line_boundary(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "test.ivtff"
            source.write_text("<f1r.P.1,P0> safe\n"
                              "<f1r.P.2,P0> [cd:ef]\n"
                              "<f1r.P.3,P0> clean\n", encoding="latin-1")
            pages = module.parse(source, "drop_uncertain_word")
        self.assertEqual([x["words"] for x in pages["f1r"]],
                         [["safe"], [None], ["clean"]])
        self.assertEqual(module.candidates(pages, ["f1r"]), [])

    def test_certain_neighbours_still_generate_candidates(self):
        pages = {"f1r": [
            {"words": ["safe", "other"], "text": "safe other", "leaf": 1},
            {"words": ["clean"], "text": "clean", "leaf": 1}]}
        self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])],
                         [0, 1])

    def test_nonphysical_separator_cannot_forge_locus_row(self):
        import tempfile
        # Latin-1 inputs can contain six of the eight forbidden separators.
        for separator in "\v\f\x1c\x1d\x1e\x85":
            with self.subTest(separator=ord(separator)):
                with tempfile.TemporaryDirectory() as directory:
                    source = Path(directory) / "test.ivtff"
                    source.write_bytes(("<f1r.P.1,P0> safe" + separator +
                                        "<f2r.P.1,P0> forged\n" +
                                        "<f1r.P.2,P0> clean\n").encode("latin-1"))
                    with self.assertRaisesRegex(ValueError, "Non-physical IVTFF line separator"):
                        module.parse(source)

    def test_cr_lf_crlf_remain_valid_physical_rows(self):
        import tempfile
        for separator in ("\n", "\r", "\r\n"):
            with self.subTest(separator=repr(separator)):
                with tempfile.TemporaryDirectory() as directory:
                    source = Path(directory) / "test.ivtff"
                    source.write_bytes(("<f1r.P.1,P0> safe.other" + separator +
                                        "<f1r.P.2,P0> clean" + separator).encode("latin-1"))
                    pages = module.parse(source)
                    self.assertEqual(len(pages["f1r"]), 2)
                    self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])],
                                     [0, 1])

    def test_source_paths_and_hashes_match_frozen_corpora(self):
        for label, path in module.INPUTS.items():
            self.assertEqual(path.parent, module.REPO_ROOT / "data" / "transcriptions")
            self.assertTrue(path.is_file(), label)
            self.assertEqual(module.sha(path), module.EXPECTED_SHA256[label])

    def test_new_result_never_overwrites_existing_file(self):
        import json
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "result.json"
            module.write_new_result(path, {"test": 1})
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")),
                             {"test": 1})
            with self.assertRaises(FileExistsError):
                module.write_new_result(path, {"test": 2})
            self.assertEqual(json.loads(path.read_text(encoding="utf-8")),
                             {"test": 1})

    def test_new_result_rejects_symlink(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "frozen.json"
            target.write_text("frozen", encoding="utf-8")
            link = Path(directory) / "result.json"
            link.symlink_to(target)
            with self.assertRaises(FileExistsError):
                module.write_new_result(link, {"test": 2})
            self.assertEqual(target.read_text(encoding="utf-8"), "frozen")


    def test_empty_body_row_does_not_create_false_positive(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "test.ivtff"
            source.write_text("<f1r.P.1,P0> alpha.beta\n"
                              "<f1r.P.2,P0> ???\n"
                              "<f1r.P.3,P0> gamma.delta\n",
                              encoding="latin-1")
            pages = module.parse(source, "primary")
        self.assertEqual([r["words"] for r in pages["f1r"]],
                         [["alpha", "beta"], [], ["gamma", "delta"]])
        # The two within-line gaps survive; no invented inter-line gap.
        self.assertEqual([r["y"] for r in module.candidates(pages, ["f1r"])],
                         [0, 0])

    def test_zero_payload_body_row_is_not_silently_skipped(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "test.ivtff"
            source.write_text("<f1r.P.1,P0> alpha\n"
                              "<f1r.P.2,P0>\n"
                              "<f1r.P.3,P0> beta\n",
                              encoding="latin-1")
            pages = module.parse(source, "primary")
        self.assertEqual([r["words"] for r in pages["f1r"]],
                         [["alpha"], [], ["beta"]])
        self.assertEqual(module.candidates(pages, ["f1r"]), [])

    def test_uncertain_only_page_does_not_shift_calibration_population(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "test.ivtff"
            source.write_text("<f1r.P.1,P0> alpha\\n"
                              "<f2r.P.1,P0> [cd:ef]\\n"
                              "<f3r.P.1,P0> ?\\n"
                              "<f4r.P.1,P0> beta\\n",
                              encoding="latin-1")
            primary = module.parse(source, "primary")
            dropped = module.parse(source, "drop_uncertain_word")
        # f2r is populated in the primary reading, but only [None] in
        # the sensitivity policy. f3r has no words in either policy.
        self.assertEqual(list(primary), ["f1r", "f2r", "f4r"])
        self.assertEqual(list(dropped), ["f1r", "f4r"])
        self.assertEqual([r["words"] for r in dropped["f1r"]], [["alpha"]])
        self.assertEqual([r["words"] for r in dropped["f4r"]], [["beta"]])

    def test_empty_only_page_does_not_shift_calibration_population(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "test.ivtff"
            source.write_text("<f1r.P.1,P0> alpha\n"
                              "<f2r.P.1,P0> ???\n",
                              encoding="latin-1")
            pages = module.parse(source, "primary")
        self.assertEqual(list(pages), ["f1r"])

    def test_candidate_builder_handles_explicit_empty_row(self):
        pages = {"f1r": [
            {"words": ["alpha"], "text": "alpha", "leaf": 1},
            {"words": [], "text": "", "leaf": 1},
            {"words": ["beta"], "text": "beta", "leaf": 1}]}
        self.assertEqual(module.candidates(pages, ["f1r"]), [])



if __name__ == "__main__":
    unittest.main()
