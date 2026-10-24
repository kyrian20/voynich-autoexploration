#!/usr/bin/env python3
"""Validate an offline, untrusted Gemini methodological review JSON.

No API calls, no corpus access, no modification of scientific state.
"""
import argparse
import json
from pathlib import Path
import sys

FIELDS = {
    "limitations": list,
    "competing_hypotheses": list,
    "proposed_design": dict,
    "pre_registration": dict,
    "required_inputs": list,
    "unresolved_questions": list,
}
DESIGN_FIELDS = (
    "unit_of_analysis", "sampling_frame", "strata", "holdout",
    "test_statistic", "negative_controls", "parser_validation",
    "multiple_testing", "stopping_rule",
)
PREREG_FIELDS = ("primary_outcome", "decision_rule", "failure_conditions")
HYP_FIELDS = ("name", "prediction", "falsifier")


def validate(document):
    errors = []
    if not isinstance(document, dict):
        return ["root must be an object"]
    if set(document) != set(FIELDS):
        errors.append("top-level fields do not match required schema")
    for field, expected in FIELDS.items():
        if not isinstance(document.get(field), expected):
            errors.append(f"{field}: wrong or missing type")
    for field, minimum in (("limitations", 5), ("competing_hypotheses", 3),
                           ("required_inputs", 1), ("unresolved_questions", 1)):
        value = document.get(field)
        if isinstance(value, list) and len(value) < minimum:
            errors.append(f"{field}: too few entries")
    for field in ("limitations", "required_inputs", "unresolved_questions"):
        value = document.get(field)
        if isinstance(value, list) and any(not isinstance(x, str) or not x.strip() for x in value):
            errors.append(f"{field}: entries must be nonempty strings")
    hypotheses = document.get("competing_hypotheses")
    if isinstance(hypotheses, list):
        for index, hypothesis in enumerate(hypotheses):
            if not isinstance(hypothesis, dict) or set(hypothesis) != set(HYP_FIELDS):
                errors.append(f"hypothesis {index}: incorrect fields")
            elif any(not isinstance(hypothesis[k], str) or not hypothesis[k].strip() for k in HYP_FIELDS):
                errors.append(f"hypothesis {index}: missing content")
    for field, required in (("proposed_design", DESIGN_FIELDS), ("pre_registration", PREREG_FIELDS)):
        value = document.get(field)
        if isinstance(value, dict):
            if set(value) != set(required):
                errors.append(f"{field}: incorrect fields")
            elif any(not isinstance(value[k], (str, list)) or not value[k] for k in required):
                errors.append(f"{field}: missing content")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("response", type=Path, help="Local JSON file; never uploaded")
    args = parser.parse_args(argv)
    try:
        if args.response.stat().st_size > 128 * 1024:
            print("INVALID: response exceeds size limit")
            return 2
        document = json.loads(args.response.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        print("INVALID: unreadable JSON")
        return 2
    errors = validate(document)
    if errors:
        for error in errors:
            print("INVALID:", error)
        return 1
    print("SCHEMA_VALID_ONLY: untrusted proposal; scientific review still required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
