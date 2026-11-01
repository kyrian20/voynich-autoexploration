"""Regression for panel-aware holdout v2; no manuscript text or EXP ID."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import prepare_prospective_leaf_holdout as v1
import prepare_prospective_leaf_holdout_v2 as v2

V1_MANIFEST = (ROOT / "research/decipherment/"
               "2026-10-23-prospective-leaf-holdout/manifest.json")
MISSING_V1 = {67, 68, 70, 72, 85, 86, 89, 90, 95, 102}


class PanelAwareHoldout(unittest.TestCase):
    def test_multi_panel_folio_identifiers(self):
        raw = (b"<f67r1> metadata\n<f67r1.1,@P0> abc\n"
               b"<f67v2> metadata\n<f67v2.2,+P0> def\n"
               b"<f68r2> metadata\n<f68r2.1> ghi\n"
               b"<f69r> metadata\n<f69r.1> jkl\n")
        self.assertEqual(v1.leaves_from_bytes(raw), {69})
        self.assertEqual(v2.leaves_from_bytes(raw), {67, 68, 69})

    def test_only_page_headers_qualify(self):
        # The previous broad pattern admitted record IDs, damaged page
        # boundaries and impossible panels as if they were valid headers.
        raw = (b"<f1r.1,@P0> orphan locus\n"
               b"<f2r7> invalid panel\n"
               b"<f3r,> damaged page\n"
               b"<f4r> real page\n"
               b"<f4r.1,@P0> record\n"
               b"<fRos> named page excluded\n")
        self.assertEqual(v2.leaves_from_bytes(raw), {4})

    def test_page_tag_requires_boundary_after_closing_bracket(self):
        # Prefix matching previously admitted malformed glued suffixes as
        # valid page headers, creating phantom eligible leaves.
        raw = (b"<f67r1>garbage\n"
               b"<f68r><! $L=B>\n"
               b"<f69r> <! $L=A>\n"
               b"<f70r>\n"
               b"<f71r.1,@P0> orphan locus\n")
        self.assertEqual(v2.leaves_from_bytes(raw), {69, 70})
        with self.assertRaisesRegex(ValueError, "No folio headers"):
            v2.leaves_from_bytes(b"<f67r>garbage\n<f68r><!comment>\n")

    def test_orphan_loci_cannot_create_holdout_leaf(self):
        with self.assertRaisesRegex(ValueError, "No folio headers"):
            v2.leaves_from_bytes(b"<f67r1.1,@P0> orphan\n<f69r.2,@P0> orphan\n")

    def test_unicode_digit_page_cannot_create_leaf(self):
        raw = "<f١r> invalid\n<f4r> valid\n".encode("utf-8")
        self.assertEqual(v2.leaves_from_bytes(raw), {4})

    def test_nonphysical_separator_cannot_forge_page_header(self):
        # splitlines() treats these as record breaks although IVTFF only
        # uses CR, LF and CRLF. A forged folio could enter a held-out split.
        for separator in ("\v", "\f", "\x1c", "\x1d", "\x1e",
                          "\x85", "\u2028", "\u2029"):
            with self.subTest(separator=repr(separator)):
                source = (
                    "<f1r> valid\n"
                    "<!editor" + separator + "<f2r> forged\n"
                ).encode("utf-8")
                with self.assertRaisesRegex(
                    ValueError, r"Non-physical IVTFF line separator at line 2"
                ):
                    v2.leaves_from_bytes(source)

    def test_cr_lf_crlf_remain_physical_page_boundaries(self):
        raw = b"<f1r> first\r\n<f2v1> second\r<f3r> third\n"
        self.assertEqual(v2.leaves_from_bytes(raw), {1, 2, 3})

    def test_no_reassignment_of_v1_folios(self):
        old = json.loads(V1_MANIFEST.read_text(encoding="utf-8"))
        old_leaves = set().union(*(set(x) for x in old["partitions"].values()))
        self.assertEqual(len(old_leaves), 92)
        regular = [f"<f{n}r> sample" for n in sorted(old_leaves)]
        panels = [f"<f{n}r1> sample" for n in sorted(MISSING_V1)]
        raw = ("\n".join(regular + panels) + "\n").encode()
        new = v2.build_manifest({name: raw for name in v2.SOURCE_NAMES})
        self.assertEqual(new["eligible_count"], 102)
        for group, old_members in old["partitions"].items():
            self.assertEqual(set(old_members) & set(new["partitions"][group]),
                             set(old_members))
        all_new = set().union(*(set(x) for x in new["partitions"].values()))
        self.assertEqual(all_new - old_leaves, MISSING_V1)
        self.assertEqual(sum(new["counts"].values()), 102)
        self.assertEqual(new["salt"], old["salt"])

    def test_cli_creates_new_output_identical_to_frozen_manifest(self):
        # Existing v2 partition membership must not change.
        frozen = (V1_MANIFEST.parent / "manifest-v2.json").read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "new" / "manifest.json"
            run = subprocess.run(
                [sys.executable, str(ROOT / "scripts/prepare_prospective_leaf_holdout_v2.py"),
                 "--out", str(output)],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(output.read_bytes(), frozen)

    def test_cli_refuses_existing_file_and_symlink_without_changing_bytes(self):
        # Regression: Path.write_text used to overwrite any --out destination,
        # including an archived manifest or a symlink to one.
        with tempfile.TemporaryDirectory() as tmp:
            protected = Path(tmp) / "frozen-manifest.json"
            original = b"ARCHIVED ORIGINAL -- MUST NOT CHANGE\\n"
            protected.write_bytes(original)
            targets = [protected]
            link = Path(tmp) / "link-to-archive.json"
            try:
                link.symlink_to(protected)
            except (NotImplementedError, OSError):
                pass
            else:
                targets.append(link)
            for output in targets:
                with self.subTest(path=str(output)):
                    run = subprocess.run(
                        [sys.executable,
                         str(ROOT / "scripts/prepare_prospective_leaf_holdout_v2.py"),
                         "--out", str(output)],
                        cwd=ROOT, capture_output=True, text=True, check=False,
                    )
                    self.assertNotEqual(run.returncode, 0)
                    self.assertIn("FileExistsError", run.stderr)
                    self.assertEqual(protected.read_bytes(), original)

    def test_reject_missing_source(self):
        with self.assertRaises(ValueError):
            v2.build_manifest({"eva_zl3b.txt": b"<f67r1.1> abc\n"})


    def test_manifest_generator_rejects_damaged_structural_rows(self):
        # A large, valid source is necessary: the legacy leaf extractor
        # silently ignores many malformed rows and would still allocate
        # 120 apparently eligible leaves. The generator must fail closed.
        good = "".join(f"<f{n}r> header\n" for n in range(1, 121)).encode()
        sources = {name: good for name in v2.SOURCE_NAMES}
        self.assertEqual(v2.build_manifest(sources)["eligible_count"], 120)
        bad_cases = (
            (b"<f121r7> invalid panel\n", "Unparsed numeric folio header"),
            (b"<f001r> duplicated physical f1r\n", "Duplicate physical folio header"),
            (b"<f1r.1,@P0> orphan after f120r\n", "Orphan or mismatched locus"),
            (b"<f120r.161,@P0> out of range\n", "Locus number outside"),
            (b"<f0r> nonpositive leaf\n", "Nonpositive physical leaf"),
        )
        for damaged, error in bad_cases:
            with self.subTest(damaged=damaged):
                altered = good + damaged
                with self.assertRaisesRegex(ValueError, error):
                    v2.build_manifest({name: altered for name in v2.SOURCE_NAMES})
                self.assertEqual(good + damaged, altered)


if __name__ == "__main__":
    unittest.main()
