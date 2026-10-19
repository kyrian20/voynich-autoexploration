#!/usr/bin/env python3
"""Post-hoc lexical controls for line-initial daiin enrichment in Currier A/B."""
import argparse,hashlib,json,random,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CORPUS=ROOT/"data/transcriptions/eva_zl3b.txt"
TARGETS=["daiin","aiin","chedy","dain","saiin","qokaiin"]

def sha(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()

def parse(path):
 rows=[];folio="unknown";dialect="unknown"
 for raw in path.read_text(encoding="latin-1").splitlines():
  line=raw.strip()
  if not line or line.startswith("#"):continue
  if re.match(r"^<f\w+>.*\$",line):
   m=re.match(r"^<(f\w+)>",line)
   if m:folio=m.group(1)
   m=re.search(r"\$L=([AB])",line)
   if m:dialect=m.group(1)
   continue
  m=re.match(r"^<([^>]+)>\s+(.*)$",line)
  if not m or "," not in m.group(1):continue
  locus=m.group(1).split(",",1)[1]
  locus=re.sub(r"^[+*@=~&!/-]+","",locus)
  if not locus.startswith("P"):continue
  body=m.group(2)
  body=re.sub(r"<!.*?>"," ",body);body=re.sub(r"<[^>]*>"," ",body)
  body=re.sub(r"\[([^:\]]+):[^\]]*\]",r"\1",body);body=re.sub(r"\{[^}]*\}"," ",body)
  body=re.sub(r"@\d+;?"," ",body)
  words=[w.lower() for w in re.split(r"[.\s,]+",body) if re.fullmatch(r"[A-Za-z]+",w)]
  if len(words)>=2:rows.append({"folio":folio,"dialect":dialect,"words":words})
 return rows

def holm(pvals):
 order=sorted(pvals,key=lambda k:pvals[k]);out={};running=0.0;m=len(order)
 for i,k in enumerate(order):
  running=max(running,min(1.0,(m-i)*pvals[k]));out[k]=round(running,6)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--permutations",type=int,default=10000);ap.add_argument("--seed",type=int,default=59720261019)
 args=ap.parse_args()
 if args.permutations<999:ap.error("--permutations must be >=999")
 rows=parse(CORPUS);results={}
 for di,dialect in enumerate(("A","B")):
  subset=[r for r in rows if r["dialect"]==dialect]
  results[dialect]={}
  pvals={}
  for wi,word in enumerate(TARGETS):
   observed=sum(r["words"][0]==word for r in subset)
   expected=sum(r["words"].count(word)/len(r["words"]) for r in subset)
   total=sum(r["words"].count(word) for r in subset)
   rng=random.Random(args.seed+di*1000+wi);ge=0;le=0;simtotal=0
   for _ in range(args.permutations):
    x=sum(r["words"][rng.randrange(len(r["words"]))]==word for r in subset)
    simtotal+=x;ge+=x>=observed;le+=x<=observed
   pu=(ge+1)/(args.permutations+1);pl=(le+1)/(args.permutations+1)
   pvals[word]=pu
   results[dialect][word]={"lines":len(subset),"token_count":total,"first_observed":observed,
    "first_expected":round(expected,5),"enrichment":round(observed/expected,5) if expected else None,
    "p_upper_plus_one":round(pu,6),"p_lower_plus_one":round(pl,6),
    "permutations":args.permutations,"seed":args.seed+di*1000+wi}
  adjusted=holm(pvals)
  for word in TARGETS:results[dialect][word]["p_holm_upper_family"]=adjusted[word]
 data={"experiment":"exp_597_daiin_frequency_control_words","protocol_version":1,
  "source":{"path":"data/transcriptions/eva_zl3b.txt","bytes":CORPUS.stat().st_size,"sha256":sha(CORPUS)},
  "target_words":TARGETS,"filters":{"generic_locus_type":"P*","minimum_clean_tokens_per_line":2,"dialects_separate":True},
  "results":results,"notes":["Exploratory post-hoc lexical control analysis; the six words are not a randomized or semantically matched control set.",
   "Expected first counts preserve each line's own token inventory and length; 10,000 Monte Carlo draws per word and dialect.",
   "Holm correction applies to six upper-tail tests separately within Currier A and Currier B. Lower-tail p-values are descriptive and not included in the primary family.",
   "Frequency differences, token morphology, and linguistic role can confound comparisons; this does not establish a semantic class or decipherment."]}
 out=ROOT/"experiments/exp_597_daiin_frequency_control_words/results.json";out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"output":str(out.relative_to(ROOT)),"results":results},indent=2))
if __name__=="__main__":main()
