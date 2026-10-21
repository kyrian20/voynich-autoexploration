#!/usr/bin/env python3
"""Descriptive lexical boundary audit around known Voynich foliation gaps."""
import hashlib, json, math, re
from collections import Counter
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.audit_ivtff_metadata import parse_currier_language
FILES = [("ZL3b", "data/transcriptions/eva_zl3b.txt"),
         ("IT2a", "data/transcriptions/eva_it2a.txt")]
# Candidate adjacent surviving sides around the predeclared gaps.
EDGES = [("f11v","f13r"),("f58v","f65r"),("f73v","f75r"),
         ("f90v","f93r"),("f96v","f99r"),("f108v","f111r")]
TOKEN = re.compile(r"(?<![A-Za-z])[A-Za-z]{2,}(?![A-Za-z])")

def jsd(a, b):
    ca, cb = Counter(a), Counter(b)
    vocab = set(ca) | set(cb)
    if not vocab: return None
    na, nb = max(1, len(a)), max(1, len(b))
    p = {w: ca[w]/na for w in vocab}
    q = {w: cb[w]/nb for w in vocab}
    m = {w: (p[w]+q[w])/2 for w in vocab}
    def kl(x, y):
        return sum(v*math.log2(v/y[k]) for k,v in x.items() if v > 0 and y[k] > 0)
    return (kl(p,m)+kl(q,m))/2

def parse(label, rel):
    path = ROOT / rel
    pages = {}
    current = None
    for line in path.read_text(encoding="latin-1").splitlines():
        h = re.match(r"^<(f\d+[rv])>.*$", line.strip())
        if h:
            current = h.group(1)
            metadata = line.strip()
            quire_match = re.search(r"\$Q\s*=\s*([^ ]+)", metadata)
            pages.setdefault(current, {
                "tokens": [],
                "currier": parse_currier_language(metadata),
                "quire": quire_match.group(1) if quire_match else None,
            })
            continue
        row = re.match(r"^<(f\d+[rv])\.\d+,[^>]*>\s*(.*)$", line.strip())
        if row:
            folio, body = row.groups()
            pages.setdefault(folio, {"tokens": [], "currier": None, "quire": None})
            # Drop IVTFF annotations, then retain EVA-like alphabetic tokens.
            body = re.sub(r"<[^>]*>|\{[^}]*\}|\[[^]]*\]|<->|\$[^ ]*", " ", body)
            pages[folio]["tokens"].extend(TOKEN.findall(body.lower()))
    return {"label":label,"path":rel,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"pages":pages}

def main():
    outputs=[]
    for label, rel in FILES:
        data=parse(label,rel); pages=data.pop("pages")
        gap=[]
        for left,right in EDGES:
            a,b=pages.get(left),pages.get(right)
            if not a or not b:
                gap.append({"edge":f"{left}->{right}","available":False}); continue
            gap.append({"edge":f"{left}->{right}","available":True,
                "left_tokens":len(a["tokens"]),"right_tokens":len(b["tokens"]),
                "left_currier":a["currier"],"right_currier":b["currier"],
                "same_currier_label":a["currier"] is not None and a["currier"]==b["currier"],
                "jensen_shannon_bits":jsd(a["tokens"],b["tokens"]),
                "vocabulary_jaccard":len(set(a["tokens"])&set(b["tokens"]))/max(1,len(set(a["tokens"])|set(b["tokens"])))})
        controls=[]
        ordered=list(pages.items())
        for (fa,a),(fb,b) in zip(ordered,ordered[1:]):
            if a["currier"] is not None and a["currier"]==b["currier"] and len(a["tokens"])>=10 and len(b["tokens"])>=10:
                d=jsd(a["tokens"],b["tokens"])
                if d is not None: controls.append({"edge":f"{fa}->{fb}","jensen_shannon_bits":d,
                    "vocabulary_jaccard":len(set(a["tokens"])&set(b["tokens"]))/max(1,len(set(a["tokens"])|set(b["tokens"])))})
        vals=[x["jensen_shannon_bits"] for x in gap if x.get("available") and x.get("same_currier_label") and x["jensen_shannon_bits"] is not None]
        cv=[x["jensen_shannon_bits"] for x in controls]
        data.update({"gap_edges":gap,"same_currier_gap_count":len(vals),"same_currier_adjacent_control_count":len(cv),
          "gap_jsd_mean":sum(vals)/len(vals) if vals else None,
          "control_jsd_mean":sum(cv)/len(cv) if cv else None,
          "gap_jsd_percentile_vs_controls":[sum(v<=x for v in cv)/len(cv) for x in vals] if cv else []})
        outputs.append(data)
    out={"experiment":"exp_606_gap_boundary_lexical_audit",
      "scope":"Exploratory descriptive comparison only. Surviving-side lexical distributions around six predeclared foliation gaps are compared with adjacent same-Currier-labelled pages. A high boundary distance cannot distinguish missing text from illustration/section/topic changes; transcription annotations and folio ordering are potential confounders.",
      "gap_edges":[f"{a}->{b}" for a,b in EDGES],"sources":outputs}
    d=ROOT/"experiments/exp_606_gap_boundary_lexical_audit"; d.mkdir(parents=True,exist_ok=True)
    (d/"results.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    lines=["# exp_606 — Lexical boundary audit around known foliation gaps","","Exploratory descriptive test; not physical codicology and not a test for unnumbered missing leaves.","",
      "Method: compare cleaned token distributions on six predeclared surviving-page transitions with adjacent page transitions sharing the same Currier label. Report Jensen–Shannon divergence (bits; higher means more different) and vocabulary Jaccard overlap (higher means more overlap). Token extraction is deliberately simple and must not be treated as a validated EVA linguistic parser."]
    for x in outputs:
      lines += ["",f"## {x['label']}","",f"- Source SHA-256: {x['sha256']}",f"- Mean gap-edge JSD (only same non-null Currier label; {x['same_currier_gap_count']} eligible edges): {x['gap_jsd_mean']}",f"- Mean same-label adjacent control JSD ({x['same_currier_adjacent_control_count']} transitions): {x['control_jsd_mean']}"]
      for e in x["gap_edges"]:
        lines.append(f"- {e['edge']}: "+(f"JSD={e['jensen_shannon_bits']:.4f}; Jaccard={e['vocabulary_jaccard']:.4f}; Currier labels {e['left_currier']} → {e['right_currier']}" if e.get("available") else "not available in this transcription"))
      if x["gap_jsd_percentile_vs_controls"]:
        lines.append("- Gap-edge JSD control percentiles: "+", ".join(f"{v:.3f}" for v in x["gap_jsd_percentile_vs_controls"]))
    lines += ["","## Interpretation limits","","Six transitions are a tiny, selected sample. Only gap edges whose two sides both have the same non-null Currier $L label enter the mean and control-percentile comparison; edges with missing/different labels remain descriptive only. Controls are adjacent surviving pages with matching Currier labels, not matched for illustration type, scribal hand, text length, or exact section. Missing leaves may interrupt content, but lexical distance cannot establish that additional pages were lost. The simple token cleanup may include annotation artefacts. No p-value or causal claim is made."]
    (d/"result.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2))
if __name__=="__main__": main()
