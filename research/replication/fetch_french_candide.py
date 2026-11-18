#!/usr/bin/env python3
"""Fetch an explicitly identified French-language Gutenberg edition, fail closed."""
from pathlib import Path
from urllib.request import Request, urlopen
import hashlib
import re

URLS = [
    "https://www.gutenberg.org/cache/epub/4650/pg4650.txt",
    "https://www.gutenberg.org/ebooks/4650.txt.utf-8",
]
TARGET = Path(__file__).resolve().parents[2] / "data/reference_corpora/french/voltaire_candide_4650.txt"
def main():
    errors = []
    for url in URLS:
        try:
            req = Request(url, headers={"User-Agent": "VoynichCorpusResearch/1.0 (research; public Gutenberg text)"})
            with urlopen(req, timeout=35) as response:
                data = response.read(2_000_001)
            if not 30_000 <= len(data) <= 2_000_000:
                raise ValueError(f"Unexpected file size: {len(data)}")
            text = data.decode("utf-8-sig")
            if not re.search(r"Language:\s*French\b", text[:8000], re.I):
                raise ValueError("Edition does not declare Language: French")
            if not re.search(r"(?i)\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG EBOOK", text):
                raise ValueError("No START Gutenberg marker")
            if not re.search(r"(?i)\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG EBOOK", text):
                raise ValueError("No END Gutenberg marker")
            TARGET.parent.mkdir(parents=True, exist_ok=True)
            TARGET.write_bytes(data)
            print(f"source={url}\nbytes={len(data)}\nsha256={hashlib.sha256(data).hexdigest()}\npath={TARGET}")
            return
        except Exception as exc:
            errors.append(f"{url}: {exc}")
    raise RuntimeError("Could not verify original French Gutenberg #4650:\n" + "\n".join(errors))
if __name__ == "__main__":
    main()
