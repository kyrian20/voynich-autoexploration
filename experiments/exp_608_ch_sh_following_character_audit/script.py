#!/usr/bin/env python3
"""exp608: exploratory audit of the ch/sh-following-character claim."""
import hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = [("ZL3b","data/transcriptions/eva_zl3b.txt"),("IT2a","data/transcriptions/eva_it2a.txt")]
ROW_RE = re.compile(r"^<(f\d+[rv])\.\d+,[^>]*>\s*(.*)$")
TOKEN_RE = re.compile(r"[a-z]{2,}")
VOWELS = set("aeiouy")

def load(label, rel):
    path = ROOT / rel
    per_folio = defaultdict(lambda: {"currier": None, "n": 0, "next": Counter(), "ch": Counter(), "sh": Counter(), "words": 0})
    for raw in path.read_text(encoding="latin-1").splitlines():
        m = ROW_RE.match(raw.strip())
        if not m: continue
        folio, body = m.groups()
        # Currier labels intentionally omitted: no validated header parser in this proxy.\n        body = re.sub(r"<[^>]*>|\{[^}]*\}|\[[^]]*\]|\$[^ ]*|@\d+;?", " ", body.lower())
        for word in TOKEN_RE.findall(body):
            per_folio[folio]["words"] += 1
            for digraph in ("ch", "sh"):
                start = 0
                while True:
                    i = word.find(digraph, start)
                    if i < 0: break
                    j = i + 2
                    if j < len(word):
                        nxt = word[j]; d = per_folio[folio]
                        d["n"] += 1; d["next"][nxt] += 1; d[digraph][nxt] += 1
                    start = i + 1
    out = []
    for folio, d in sorted(per_folio.items()):
        if not d["n"]: continue
        n=d["n"]; vowel_n=sum(d["next"][x] for x in VOWELS)
        out.append({"folio":folio,"currier":None,"word_count":d["words"],"n":n,
          "next_counts":dict(sorted(d["next"].items())),"vowel_rate":vowel_n/n,
          "e_rate":d["next"]["e"]/n,"a_rate":d["next"]["a"]/n,
          "ch_counts":dict(sorted(d["ch"].items())),"sh_counts":dict(sorted(d["sh"].items()))})
    allc=Counter()
    for d in per_folio.values(): allc.update(d["next"])
    return {"label":label,"source":rel,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
            "folios":out,"overall_next_counts":dict(sorted(allc.items()))}

def aggregate(items):
    c=Counter()
    for f in items: c.update(f["next_counts"])
    n=sum(c.values())
    return {"folios":len(items),"occurrences":n,"next_counts":dict(sorted(c.items())),
            "vowel_rate":sum(c[x] for x in VOWELS)/n if n else None,
            "e_rate":c["e"]/n if n else None,"a_rate":c["a"]/n if n else None}

def main():
    datasets=[]; summaries=[]
    for label,rel in FILES:
        ds=load(label,rel); datasets.append(ds); fs=ds["folios"]
        rates=[f["e_rate"] for f in fs if f["n"]>=5]
        summaries.append({"label":label,"source_sha256":ds["sha256"],"folios_with_context":len(fs),
          "aggregate":aggregate(fs),"currier_breakdown":"omitted; no validated label parser",
          "folios_n_ge_5":len(rates),"e_rate_range_n_ge_5":[min(rates),max(rates)] if rates else None})
    result={"experiment":"exp_608_ch_sh_following_character_audit",
      "question":"Do cleaned EVA tokens show folio-level variation in the character following ch/sh, as suggested by Parisel (2026)?",
      "method":{"token_pattern":"[a-z]{2,}","contexts":"each within-token ch/sh occurrence with a following character; overlapping occurrences counted",
      "vowels":sorted(VOWELS),"folio_range_min_n":5,"analysis":"descriptive; no tuned classifier or significance claim",
      "limitation":"Simple proxy, not a reproduction of Parisel's template-conditioned Beta-Binomial mixture. Transcriptions are related; Currier labels are intentionally not inferred; token cleanup may be imperfect."},
      "datasets":datasets,"summaries":summaries}
    dest=ROOT/"experiments/exp_608_ch_sh_following_character_audit"; dest.mkdir(parents=True,exist_ok=True)
    (dest/"results.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    lines=["# exp608 — ch/sh following-character audit","","## Question","Do cleaned EVA tokens show folio-level variation in the character following ch/sh, as suggested by Parisel (2026)?","","## Method and limitations",
      "- Count each within-word occurrence of ch or sh with a following character; summarize by folio and transcription.",
      "- Report next-character frequencies and vowel/e/a rates overall; omit Currier breakdown because labels are not parsed authoritatively.",
      "- Folio e-rate range uses folios with at least five contexts.",
      "- This is a descriptive proxy, not a replication of Parisel's template-conditioned Beta-Binomial mixture. No significance or decipherment claim follows.",
      "- ZL3b and IT2a are related transcriptions, not independent physical witnesses."]
    for s in summaries:
        a=s["aggregate"]
        lines += ["",f"## {s['label']}",f"- Source SHA-256: {s['source_sha256']}",
          f"- Folios with contexts: {s['folios_with_context']}; occurrences: {a['occurrences']}",
          f"- Next-character counts: {json.dumps(a['next_counts'],sort_keys=True)}",
          f"- Vowel rate: {a['vowel_rate']:.4f}; e rate: {a['e_rate']:.4f}; a rate: {a['a_rate']:.4f}",
          f"- Folio e-rate range (n≥5): {s['e_rate_range_n_ge_5']}"]
    lines += ["","## Interpretation guardrail","Folio variation would be compatible with the published claim but would not establish a discrete switch: word templates, section composition, transcription conventions and small counts can create apparent differences. Proper replication requires exact extraction rules, template-conditioned modeling and held-out validation."]
    (dest/"result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"experiment":result["experiment"],"summaries":summaries},indent=2))
if __name__=="__main__": main()
