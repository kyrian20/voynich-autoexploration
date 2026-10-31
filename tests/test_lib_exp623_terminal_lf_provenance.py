"""Pin the narrow byte difference between two Library originals and GitHub copies.

The Library files themselves are not bundled here; their SHA-256 and lengths
were independently checked on 2026-11-01. This is not a historical execution
reproduction or a scientific test of the Voynich manuscript.
"""
import hashlib
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

# (GitHub size, GitHub SHA-256, Library size, Library SHA-256)
PAIRS = {
    "exp623_order_null.py": (
        11136, "28925cddaa94a8a9236ad67f6f92ae83459561414cea8ba3d5d4febfac90e9c7",
        11137, "ea51e67e6f36b8c651231262cb22ebbb5ef9f98cd31c4673924e33d6a3627010",
    ),
    "exp623_shuffle_holdout.py": (
        8562, "0be5b31be711e5f6e9b216f370d786a6a247120f4539f07719dc65e624e0c28b",
        8563, "c4bb8e7fb44632b93979a26bb88c49264c3fb7c4c2d3685a59d72958f902b070",
    ),
}


class LibraryExp623ScriptProvenanceTests(unittest.TestCase):
    def test_only_missing_terminal_lf_separates_repository_copy(self):
        for name, (repo_size, repo_sha, library_size, library_sha) in PAIRS.items():
            with self.subTest(script=name):
                raw = (ROOT / "research/reproduction" / name).read_bytes()
                self.assertEqual(len(raw), repo_size)
                self.assertEqual(hashlib.sha256(raw).hexdigest(), repo_sha)
                self.assertFalse(raw.endswith(b"\n"))
                self.assertEqual(len(raw + b"\n"), library_size)
                self.assertEqual(hashlib.sha256(raw + b"\n").hexdigest(), library_sha)


if __name__ == "__main__":
    unittest.main()
