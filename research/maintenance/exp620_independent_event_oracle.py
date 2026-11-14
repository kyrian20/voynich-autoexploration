"""Independent token-level digraph event oracle for EXP-620 (synthetic fixtures only).

This does NOT parse IVTFF or reproduce EXP-612. It isolates one previously
observed failure mode: terminal ch/sh must not enter a following-character
denominator. No manuscript corpora are read or modified.
"""
from __future__ import annotations

import argparse
import json
import unittest

DIGRAPHS = ("ch", "sh")
VOWELS = frozenset("aeiouy")
CONSONANTS = frozenset("bcdfghjklmnpqrstvwxz")


def events(token: str) -> list[tuple[str, int, str, bool | None]]:
    """Return (digraph, zero-based offset, next char, vowel/unknown) for valid followers.

    Unknown/non-letter followers are not silently counted as consonants.\n    Independent reference implementation: scan each character offset directly,
    rather than splitting on a regex or padding a terminal follower.
    """
    if not isinstance(token, str):
        raise TypeError("token must be a string")
    out = []
    for offset in range(max(0, len(token) - 2)):
        pair = token[offset:offset + 2]
        if pair in DIGRAPHS:
            follower = token[offset + 2]
            classification = (True if follower in VOWELS else
                              False if follower in CONSONANTS else None)
            out.append((pair, offset, follower, classification))
    return out


class IndependentEventFixtures(unittest.TestCase):
    def test_terminal_events_excluded(self):
        for token in ("ch", "sh", "ach", "ash", ""):
            with self.subTest(token=token):
                self.assertEqual(events(token), [])

    def test_followers_and_positions(self):
        self.assertEqual(events("che"), [("ch", 0, "e", True)])
        self.assertEqual(events("shk"), [("sh", 0, "k", False)])
        self.assertEqual(events("achyshk"), [
            ("ch", 1, "y", True), ("sh", 4, "k", False)
        ])
        self.assertEqual(events("chshy"), [("ch", 0, "s", False),
                                           ("sh", 2, "y", True)])

    def test_case_and_ambiguity_are_not_silently_normalized(self):
        self.assertEqual(events("CHa"), [])
        self.assertEqual(events("ch?"), [("ch", 0, "?", None)])
        self.assertEqual(events("sh@"), [("sh", 0, "@", None)])
        self.assertEqual(events("ch1"), [("ch", 0, "1", None)])
        self.assertEqual(events("chY"), [("ch", 0, "Y", None)])
        # These are synthetic lexical strings, not IVTFF-validity judgments.

    def test_no_implicit_cross_token_join(self):
        self.assertEqual(events("c") + events("ha"), [])
        self.assertEqual(events("sh") + events("e"), [])

    def test_non_string_rejected(self):
        with self.assertRaises(TypeError):
            events(None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", help="Inspect one synthetic token")
    args = parser.parse_args()
    if args.token is None:
        unittest.main(argv=["exp620-oracle"], verbosity=2)
    else:
        print(json.dumps(events(args.token), ensure_ascii=True))
