#!/usr/bin/env python3
"""Independent IVTFF parser cross-check for line IDs, loci, Currier labels, and tokens.

Parser A follows the regex extraction used by exp_600. Parser B uses delimiter/state
parsing with an independent token scanner. Every discrepancy is retained.
"""
from __future__ import annotations
import collections, hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
FILES=[("ZL3b",ROOT/"data/transcriptions/eva_zl3b.txt"),
       ("ZL3a",ROOT/"data/transcriptions/zl3a.txt")]
TARGETS=("daiin","aiin","chedy","dain","saiin","qokaiin")

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):h.update(block)
    return h.hexdigest()

# Parser A: regex-based extraction, independently restated from exp_600.
def tokens_regex(body):
    text=re.sub(r"<!.*?>"," ",body)
    text=re.sub(r"<[^>]*>"," ",text).replace("<$>"," ").replace("<%>"," ")
    text=re.sub(r"\[([^:\]]*):[^\]]*\]",r"\1",text)
    text=re.sub(r"\{[^}]*\}"," ",text)
    text=re.sub(r"@\d+;?"," ",text)
    return [x.lower() for x in re.split(r"[.\s,]+",text) if re.fullmatch(r"[A-Za-z]+",x)]

def parser_a(path):
    out=[];folio="unknown";currier="unknown";headers=0;unparsed=[]
    for n,raw in enumerate(path.read_text(encoding="latin-1").splitlines(),1):
        s=raw.strip()
        if not s or s.startswith("#"):continue
        h=re.match(r"^<(f[^>]+)>\s*(.*)$",s)
        if h and "," not in h.group(1):
            folio=h.group(1);m=re.search(r"\$L=([AB])",h.group(2))
            currier=m.group(1) if m else "unknown";headers+=1;continue
        m=re.match(r"^<([^>]+)>\s+(.*)$",s)
        if not m or "," not in m.group(1):continue
        ident,locus=m.group(1).split(",",1);ident=ident.strip();locus=locus.strip()
        if not re.match(r"^f[^.]+\..+$",ident):
            unparsed.append({"line":n,"identifier":ident});continue
        norm=re.sub(r"^[+*@=~&!/]+","",locus)
        out.append({"id":ident,"folio":folio,"currier":currier,"raw_locus":locus,
                    "locus":norm,"body":m.group(2).strip(),"tokens":tokens_regex(m.group(2)),
                    "start":m.group(2).startswith("<%>"),"end":m.group(2).rstrip().endswith("<$>"),"line":n})
    return {"records":out,"headers":headers,"unparsed":unparsed}

# Parser B: stateful line scanner. It locates delimiters directly, then tokenizes
# by consuming markup/alternatives with a different implementation.
def tokens_scanner(body):
    """Tokenize after inline normalization; bracket alternatives splice into the word."""
    i = 0
    n = len(body)
    word = []
    kept = []

    def flush_word():
        if not word:
            return
        token = "".join(word)
        if token.isascii() and token.isalpha():
            kept.append(token.lower())
        word.clear()

    while i < n:
        ch = body[i]
        if ch.isspace() or ch in ".,": 
            flush_word()
            i += 1
            continue
        if body.startswith("<!", i):
            # IVTFF free-text comments terminate at the next closing angle bracket.
            flush_word()
            j = body.find(">", i + 2)
            i = n if j < 0 else j + 1
            continue
        if ch == "<":
            flush_word()
            j = body.find(">", i + 1)
            i = n if j < 0 else j + 1
            continue
        if ch == "[":
            j = body.find("]", i + 1)
            if j < 0:
                # Malformed uncertain reading: invalidate the current lexical unit.
                word.append("?")
                i += 1
                continue
            inner = body[i + 1:j]
            # Primary policy: use the first alternative in place, not as a new token.
            # Apply the same later normalization steps as Parser A to annotations
            # inside that alternative: brace spans and @number markers become spaces.
            alternative = inner.split(":", 1)[0]
            alternative = re.sub(r"\{[^}]*\}", " ", alternative)
            alternative = re.sub(r"@\d+;?", " ", alternative)
            for alt_char in alternative:
                if alt_char.isspace() or alt_char in ".,": 
                    flush_word()
                else:
                    word.append(alt_char)
            i = j + 1
            continue
        if ch == "{":
            # Match the declared primary parser policy: omit brace-delimited material.
            flush_word()
            j = body.find("}", i + 1)
            i = n if j < 0 else j + 1
            continue
        if ch == "@":
            flush_word()
            j = i + 1
            while j < n and body[j].isdigit():
                j += 1
            if j > i + 1:
                if j < n and body[j] == ";":
                    j += 1
                i = j
                continue
        if ch.isalpha() and ch.isascii():
            word.append(ch)
            i += 1
            continue
        # Any other character makes the current lexical unit non-EVA; keep it
        # in the buffer so the whole unit is conservatively excluded at flush.
        word.append(ch)
        i += 1

    flush_word()
    return kept

def parser_b(path):
    out=[];folio="unknown";currier="unknown";headers=0;unparsed=[]
    for n,raw in enumerate(path.read_text(encoding="latin-1").splitlines(),1):
        s=raw.strip()
        if not s or s.startswith("#"):continue
        # Parse tags by first closing delimiter; no regex expression for header.
        if s.startswith("<f") and ">" in s:
            j=s.find(">")
            tag=s[1:j]
            tail=s[j+1:].strip()
            if "," not in tag:
                folio=tag;headers+=1
                lm=re.search(r"\$L=([AB])",tail)
                currier=lm.group(1) if lm else "unknown"
                continue
        if not s.startswith("<") or ">" not in s:continue
        j=s.find(">")
        tag=s[1:j];body=s[j+1:].strip()
        if "," not in tag or not body:continue
        ident,raw_locus=tag.split(",",1);ident=ident.strip();raw_locus=raw_locus.strip()
        if not ident.startswith("f") or "." not in ident:
            unparsed.append({"line":n,"identifier":ident});continue
        norm=raw_locus
        while norm and norm[0] in "+*@=~&!/":norm=norm[1:]
        out.append({"id":ident,"folio":folio,"currier":currier,"raw_locus":raw_locus,
                    "locus":norm,"body":body,"tokens":tokens_scanner(body),
                    "start":body.startswith("<%>"),"end":body.endswith("<$>"),"line":n})
    return {"records":out,"headers":headers,"unparsed":unparsed}

def summarize(rows):
    eligible=[r for r in rows if r["currier"]=="B" and r["locus"]=="P0" and len(r["tokens"])>=2]
    stats={}
    for word in TARGETS:
        total=sum(r["tokens"].count(word) for r in eligible)
        first=sum(bool(r["tokens"]) and r["tokens"][0]==word for r in eligible)
        expected=sum(r["tokens"].count(word)/len(r["tokens"]) for r in eligible)
        stats[word]={"lines":len(eligible),"tokens":total,"first":first,
                     "expected_first":round(expected,6),
                     "enrichment":round(first/expected,6) if expected else None}
    return {"body_lines":len(eligible),"stats":stats}

def compare(path,label):
    a=parser_a(path);b=parser_b(path)
    ar={r["id"]:r for r in a["records"]};br={r["id"]:r for r in b["records"]}
    only_a=sorted(set(ar)-set(br));only_b=sorted(set(br)-set(ar))
    mismatch=collections.Counter();examples=[]
    for key in sorted(set(ar)&set(br)):
        x,y=ar[key],br[key]
        for field in ("folio","currier","raw_locus","locus","body","tokens","start","end"):
            if x[field]!=y[field]:
                mismatch[field]+=1
                if len(examples)<100:
                    examples.append({"id":key,"field":field,"parser_A":x[field],"parser_B":y[field],
                                     "line_A":x["line"],"line_B":y["line"]})
    aa=summarize(a["records"]);bb=summarize(b["records"])
    stats_equal=aa==bb
    return {"transcription":label,"source":{"path":str(path.relative_to(ROOT)),
        "bytes":path.stat().st_size,"sha256":sha256(path)},
        "parser_A":{"record_count":len(a["records"]),"folio_headers":a["headers"],"unparsed":a["unparsed"][:100]},
        "parser_B":{"record_count":len(b["records"]),"folio_headers":b["headers"],"unparsed":b["unparsed"][:100]},
        "only_parser_A_ids":only_a[:100],"only_parser_B_ids":only_b[:100],
        "record_key_counts":{"only_A":len(only_a),"only_B":len(only_b),"common":len(set(ar)&set(br))},
        "mismatch_count_by_field":dict(mismatch),"mismatch_examples":examples,
        "primary_stat_summary_regex":aa,"primary_stat_summary_scanner":bb,
        "primary_stats_identical":stats_equal}

def main():
    versions=[compare(path,label) for label,path in FILES if path.exists()]
    data={"experiment":"exp_602_independent_ivtff_parser_audit","protocol_version":6,
      "parser_A":"regex extraction patterned after exp_600 + regex token cleanup",
      "parser_B":"stateful delimiter parser with inline first-alternative splicing; IVTFF <!…> comments end at >",
      "filters":{"Currier":"B","normalized_locus":"P0","minimum_clean_tokens_per_line":2,
                 "predeclared_tokens":list(TARGETS)},
      "versions":versions,
      "notes":["Parser agreement establishes implementation consistency only; not an authoritative transcription validation.",
               "The two implementations intentionally use different parsing approaches.",
               "Any disagreement should be fixed or adjudicated before additional hypotheses.",
               "Protocol v2 fixed Parser B incorrectly searching for ?> rather than the IVTFF comment terminator >. Protocol v3 spliced the primary bracket alternative into the surrounding lexical unit. Protocol v4 attempted to normalize brace spans and @number markers inside alternatives, but an escaping error prevented the regexes from matching. Protocol v5 fixes the regex escaping. Protocol v6 allows an empty first bracket alternative, matching the documented primary-alternative policy for forms such as [:y]; earlier result files remain preserved.",
               "No semantic or decipherment claims."]}
    out=ROOT/"experiments/exp_602_independent_ivtff_parser_audit/results_v6.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(out.relative_to(ROOT)),"versions":[{"transcription":v["transcription"],
      "A_records":v["parser_A"]["record_count"],"B_records":v["parser_B"]["record_count"],
      "mismatches":v["mismatch_count_by_field"],"primary_equal":v["primary_stats_identical"],
      "primary_A":v["primary_stat_summary_regex"],"primary_B":v["primary_stat_summary_scanner"]}
      for v in versions]},indent=2))

if __name__=="__main__":main()
