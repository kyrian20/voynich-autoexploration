#!/usr/bin/env python3
"""Opt-in Gemini methodological review, with no repository checkout or corpus access.

This command only reads the fixed public methodological prompt and writes local
review artifacts. It never prints API credentials or remote response bodies.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

# Support both `python -m scripts.request_gemini_review` and the documented
# direct entry point `python scripts/request_gemini_review.py`.
if __package__:
    from .validate_gemini_review import validate
else:
    from validate_gemini_review import validate

PROMPT_PATH = Path(__file__).resolve().parents[1] / "research/protocols/2026-10-24-gemini-ch-sh-review-prompt.md"
API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models/"
MAX_RESPONSE = 128 * 1024


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def build_request(model, key, prompt):
    if not model or not all(c.isalnum() or c in ".-_" for c in model):
        raise ValueError("invalid model identifier")
    if not key:
        raise ValueError("missing GEMINI_API_KEY")
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "maxOutputTokens": 4096},
    }
    return urllib.request.Request(
        API_ROOT + model + ":generateContent",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )


def extract_text(payload):
    candidates = payload.get("candidates", [])
    if not candidates:
        raise ValueError("no candidates")
    parts = candidates[0].get("content", {}).get("parts", [])
    text = "".join(part.get("text", "") for part in parts if not part.get("thought"))
    if not text.strip():
        raise ValueError("empty model response")
    return text


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Exact model name verified in smoke report")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--execute", action="store_true", help="Authorize exactly one API POST")
    args = parser.parse_args(argv)
    if not args.execute:
        print("DRY_RUN_ONLY: no network request; add --execute to authorize one POST")
        return 0
    if args.output_dir.exists() and any(args.output_dir.iterdir()):
        print("BLOCKED: output directory is not empty")
        return 2
    prompt = PROMPT_PATH.read_text(encoding="utf-8")
    # Refuse unexpected changes to the fixed prompt; review content before execution.
    if len(prompt.encode("utf-8")) > 16000:
        print("BLOCKED: methodological prompt too large")
        return 2
    try:
        request = build_request(args.model, os.environ.get("GEMINI_API_KEY", ""), prompt)
    except ValueError:
        print("BLOCKED: invalid model or missing API secret")
        return 2
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=90) as response:
            raw = response.read(MAX_RESPONSE + 1)
            if len(raw) > MAX_RESPONSE:
                raise ValueError("oversize API response")
            envelope = json.loads(raw)
        text = extract_text(envelope)
        review = json.loads(text)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
        print("FAILED: API or response error (details suppressed)")
        return 1
    errors = validate(review)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "review-untrusted.json").write_text(
        json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "status": "SCHEMA_VALID_ONLY" if not errors else "INVALID_SCHEMA",
        "scientific_status": "PROPOSED_UNVERIFIED",
        "model": args.model,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "response_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "schema_error_count": len(errors),
        "manuscript_corpus_sent": False,
        "api_attempts": 1,
    }
    (args.output_dir / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"REVIEW_SAVED: {receipt['status']}; scientific_status=PROPOSED_UNVERIFIED")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
