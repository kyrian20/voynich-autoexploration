#!/usr/bin/env python3
"""Deterministic independent reimplementation of the Voynich line-boundary model."""
from __future__ import annotations
import collections, hashlib, json, math, re, statistics, random, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
REPO_ROOT=ROOT.parents[2]
# Use the same physical-row contract as the audited IVTFF readers.
# The script is also executable directly from its research subdirectory.
if str(REPO_ROOT) not in sys.path:
 sys.path.insert(0,str(REPO_ROOT))
from scripts.ivtff_physical_rows import checked_physical_lines
INPUTS={"ZL3b":REPO_ROOT/"data/transcriptions/eva_zl3b.txt",
        "IT2a":REPO_ROOT/"data/transcriptions/eva_it2a.txt"}
EXPECTED_SHA256={"ZL3b":"bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc",
                 "IT2a":"7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"}
ROW=re.compile(r"^<(?P<ident>[^>]+)>(?:[ \t]+(?P<body>.*))?$")
UNCERTAIN=re.compile(r"\{[^}]*\}|\?")
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()
def tokens(body,policy="primary",preserve_gaps=False):
 # IVTFF 2.0.2 §5.7.2: free-text comments have zero width in a word.
 # Do not invent a gap where the manuscript only has an annotation.
 body=re.sub(r"<![^>]*>","",body)
 # IVTFF 2.0.2 §6.7–6.9: explicit paragraph start/end tags are
 # structural boundaries, not ordinary inline whitespace. In particular,
 # a trailing <$> must not be counted as a positive line-to-line gap.
 # Preserve a sentinel on either side of a paragraph transition; remove
 # free-text comments first so marker-like text inside comments is inert.
 body=body.replace("<%>",".?.").replace("<$>",".?.")
 body=re.sub(r"<[^>]*>"," ",body)
 # Fail closed on unbalanced markup. Otherwise an unfinished IVTFF comment
 # or reading alternative is interpreted as ordinary alphabetic words and
 # can forge both within-line and cross-line candidates. Do not guess where
 # an unterminated annotation ends: quarantine the complete body row.
 # Properly closed tags and square-bracket readings were handled above or
 # are handled below; remaining angle brackets cannot be valid tokens.
 if "<" in body or ">" in body:
  return [None] if preserve_gaps else []
 if policy=="drop_uncertain_word":
  # Preserve an uncertainty sentinel until after splitting; otherwise the
  # primary-reading substitution erases the evidence needed for exclusion.
  body=re.sub(r"\[[^\]]*\]","?",body)
 else:
  body=re.sub(r"\[([^:\]]*):[^\]]*\]",r"\1",body);body=re.sub(r"\[([^\]]*)\]",r"\1",body)
 # After the selected reading policy has removed valid bracket spans,
 # any leftover bracket is malformed. A full-row barrier avoids treating
 # text after an unmatched opener (including dots) as trustworthy words.
 if "[" in body or "]" in body:
  return [None] if preserve_gaps else []
 out=[]
 for x in re.split(r"[.\s,]+",body):
  if not x:continue
  # A question mark is an unresolved glyph in either policy. Never turn
  # it into two apparent words or erase it between otherwise valid words.
  if ("?" in x or "{" in x or "}" in x or "@" in x or "/" in x
      or (policy=="drop_uncertain_word" and UNCERTAIN.search(x))):
   # IVTFF ligatures and @nnn; high-ASCII glyph codes are not word spaces.
   # Until their glyph-level representation is adjudicated, keep the entire
   # affected word as an unresolved barrier instead of forging adjacency.
   # Bare/malformed @ markers also fail closed rather than silently splitting.
   # IVTFF line-continuation slashes mark a word continued across physical
   # rows, not a word boundary. Until rows are explicitly reassembled,
   # retain a barrier rather than counting a false positive line break.
   if preserve_gaps:out.append(None)
   continue
  out.extend(w.lower() for w in re.findall(r"[A-Za-z]+",x))
 return out
def parse(path,policy="primary"):
 pages=collections.defaultdict(list)
 for lineno,raw in checked_physical_lines(path.read_text(encoding="latin-1")):
  m=ROW.match(raw.strip())
  if not m or "," not in m["ident"]:continue
  ident,locus=m["ident"].split(",",1);parts=ident.split(".")
  if len(parts)<2:continue
  page=parts[0]; pm=re.fullmatch(r"f(\d+)[rv][1-6]?",page)
  loc=re.sub(r"^[+*@=~&!/]+","",locus.strip())
  if not pm and page!="fRos":continue
  if not re.fullmatch(r"P(?:0|1|b|c|r|t)",loc):
   # A non-P locus between two P records is not a direct P-to-P
   # adjacency. Preserve its source row and locus on the preceding P row.
   # Do not insert fake body rows or change the page/calibration population.
   if page in pages and pages[page]:
    pages[page][-1].setdefault("intervening_non_p",[]).append({"line":lineno,"loc":loc})
   continue
  # Both policies must preserve unknown-glyph barriers for adjacency tests.
  ws=tokens(m["body"] or "",policy,preserve_gaps=True)
  # Preserve empty P rows as barriers: removing one would invent adjacency
  # between its predecessor and successor. Exclude entirely empty pages so
  # they cannot shift the historical every-fifth-page calibration.
  # IVTFF locus ordinals must remain available: two admitted P rows with a
  # missing numbered locus between them are not proven adjacent. Keep the
  # original row even if its identifier is malformed, but fail closed when
  # evaluating cross-row adjacency rather than guessing the missing number.
  locus_number=int(parts[-1]) if re.fullmatch(r"[0-9]+",parts[-1]) else None
  pages[page].append({"words":ws,"text":" ".join(w if w is not None else "<UNCERTAIN>" for w in ws),"line":lineno,"leaf":int(pm[1]) if pm else None,"loc":loc,"locus_number":locus_number})
 # A sentinel-only row has a nonempty list [None] but no usable word.
 # Keep it as a barrier within a populated page, never as a page of its own.
 return {page:ls for page,ls in pages.items()
         if any(any(word is not None for word in row["words"]) for row in ls)}
def feats(a,b):
 x=(a[:2],a[-2:],str(min(len(a),12)));y=(b[:2],b[-2:],str(min(len(b),12)))
 return {"start_only":(x[0],y[0]),"end_only":(x[1],y[1]),"length_only":(x[2],y[2]),
         "start_end_length_separable":x+y,"full_tuple":(x,y)}
def candidates(pages,pagenames):
 rows=[]
 for page in pagenames:
  ls=pages[page]
  for i,line in enumerate(ls):
   if not line["words"]:
    # An empty body row interrupts continuity; do not bridge across it.
    continue
   for j in range(len(line["words"])-1):
    a,b=line["words"][j:j+2]
    if a is None or b is None:continue
    rows.append({"y":0,"f":feats(a,b),"leaf":line["leaf"],"texts":(line["text"],line["text"]),"page":page})
   if i+1<len(ls) and not line.get("intervening_non_p"):
    nxt=ls[i+1]
    # Source-derived rows carry numeric locus IDs. A skipped, duplicated or
    # reversed ordinal is a discontinuity even without a visible non-P row.
    # Manually supplied legacy candidate fixtures without this field retain
    # their historical interface; real parsed rows must have valid ordinals.
    if "locus_number" in line and "locus_number" in nxt:
     a_ord,b_ord=line["locus_number"],nxt["locus_number"]
     if a_ord is None or b_ord is None or b_ord!=a_ord+1:continue
    if not nxt["words"] or line["words"][-1] is None or nxt["words"][0] is None:continue
    rows.append({"y":1,"f":feats(line["words"][-1],nxt["words"][0]),"leaf":line["leaf"],
                 "texts":(line["text"],nxt["text"]),"page":page})
 return rows
def embargo(train,test):
 # Exclude an exact line from training when that line also occurs in test;
 # also omit its test instances so identical line strings cannot drive scores.
 ttexts={t for r in test for t in r["texts"]}
 rtexts={t for r in train for t in r["texts"]}
 shared=ttexts&rtexts
 train=[r for r in train if not any(t in shared for t in r["texts"])]
 test=[r for r in test if not any(t in shared for t in r["texts"])]
 return train,test,len(shared)
def fit(train,key,alpha=.5):
 yc=collections.Counter(r["y"] for r in train); c={0:[],1:[]}; voc=[]
 nfeat=len(train[0]["f"][key])
 for y in (0,1):c[y]=[collections.Counter() for _ in range(nfeat)]
 for r in train:
  for i,v in enumerate(r["f"][key]):c[r["y"]][i][v]+=1
 for i in range(nfeat):
  voc.append(set(r["f"][key][i] for r in train))
 return yc,c,voc
def pred(train,test,key,alpha=.5):
 yc,c,v=fit(train,key,alpha);n=sum(yc.values());out=[]
 for r in test:
  scores=[]
  for y in (0,1):
   # Two classes: symmetric Dirichlet(alpha, alpha) prior.
   # Historical numerator used 2*alpha per class, yielding a different prior.
   s=math.log((yc[y]+alpha)/(n+2*alpha))
   for i,val in enumerate(r["f"][key]):
    # Reserve one explicit out-of-vocabulary bucket for unseen test values.
    # Without it, observed-category probabilities sum to 1 but an unseen
    # value receives extra positive mass, so the likelihood is not normalized.
    s+=math.log((c[y][i][val]+alpha)/(yc[y]+alpha*(len(v[i])+1)))
   scores.append(s)
  m=max(scores);a=math.exp(scores[0]-m);b=math.exp(scores[1]-m);out.append(b/(a+b))
 return out,yc
def auc(y,s):
 n1=sum(y);n0=len(y)-n1
 if n1==0 or n0==0:return float("nan")
 order=sorted(range(len(y)),key=lambda i:s[i]);rs=0;i=0
 while i<len(order):
  j=i+1
  while j<len(order) and s[order[j]]==s[order[i]]:j+=1
  rank=(i+1+j)/2;rs+=rank*sum(y[k] for k in order[i:j]);i=j
 return (rs-n1*(n1+1)/2)/(n1*n0)
def ap(y,s):
 # Average precision is a step integral over distinct score thresholds.
 # Never break equal-score ties by input order (categorical models tie often).
 n1=sum(y)
 if not n1:return float("nan")
 idx=sorted(range(len(y)),key=lambda i:s[i],reverse=True)
 seen=0;hit=0;area=0.0;i=0
 while i<len(idx):
  j=i+1
  while j<len(idx) and s[idx[j]]==s[idx[i]]:j+=1
  positive=sum(y[k] for k in idx[i:j])
  seen+=j-i;hit+=positive
  area+=(positive/n1)*(hit/seen)
  i=j
 return area
def loss(y,p):
 return -sum(v*math.log2(max(1e-15,q))+(1-v)*math.log2(max(1e-15,1-q)) for v,q in zip(y,p))/len(y)
def score(train,test,key):
 if not train or not test:return None
 p,yc=pred(train,test,key);y=[r["y"] for r in test];base=yc[1]/sum(yc.values())
 return {"n":len(y),"breaks":sum(y),"auc":auc(y,p),"ap":ap(y,p),
  "gain":loss(y,[base]*len(y))-loss(y,p),"brier":sum((q-v)**2 for q,v in zip(p,y))/len(y),
  "baseline_prevalence":base,"y":y,"p":p,"leaf":[r["leaf"] for r in test]}
def qtl(x,q):
 x=sorted(x);p=(len(x)-1)*q;i=int(p);j=min(i+1,len(x)-1);return x[i]+(p-i)*(x[j]-x[i])
def summarize(r):
 return {k:(round(v,6) if isinstance(v,float) else v) for k,v in r.items() if k not in {"y","p","leaf"}}
def run(path,label,policy):
 pages=parse(path,policy);pnames=sorted(pages);leaf={p:pages[p][0]["leaf"] for p in pnames};phys_pages=[p for p in pnames if leaf[p] is not None];leaves=sorted(set(leaf[p] for p in phys_pages))
 allc=candidates(pages,pnames);physc=candidates(pages,phys_pages);models=("start_only","end_only","length_only","start_end_length_separable","full_tuple")
 # Original fixed page split, as an implementation calibration.
 hp=set(pnames[::5]);tr=[r for r in allc if r["page"] not in hp];te=[r for r in allc if r["page"] in hp]
 tr,te,ndup=embargo(tr,te)
 page_n=len(te);page_breaks=sum(r["y"] for r in te)
 page={m:score(tr,te,m) for m in models}
 page_clean={m:summarize(v) if v else None for m,v in page.items()}
 # Physical-leaf leave-one-out; both recto/verso and all panels stay together.
 oof={m:{"y":[],"p":[],"leaf":[]} for m in models}; foldstats={m:[] for m in models}; foldinfo=[]
 for L in leaves:
  testpages={p for p in phys_pages if leaf[p]==L}
  tr=[r for r in physc if r["leaf"]!=L];te=[r for r in physc if r["leaf"]==L]
  tr,te,nd=embargo(tr,te)
  foldinfo.append({"leaf":L,"pages":len(testpages),"n":len(te),"breaks":sum(r["y"] for r in te),"duplicate_line_texts_embargoed":nd})
  for m in models:
   z=score(tr,te,m)
   if z:
    foldstats[m].append({"auc":z["auc"],"gain":z["gain"],"leaf":L})
    oof[m]["y"].extend(z["y"]);oof[m]["p"].extend(z["p"]);oof[m]["leaf"].extend(z["leaf"])
 phys={};rng=random.Random(20261028)
 for m,d in oof.items():
  y,p=d["y"],d["p"]; leaf_stats=foldstats[m]
  ba=[];bg=[]
  byleaf={x["leaf"]:x for x in leaf_stats}
  for _ in range(1999):
   sample=[rng.choice(leaves) for __ in leaves]
   aa=[byleaf[x]["auc"] for x in sample if x in byleaf and math.isfinite(byleaf[x]["auc"])]
   gg=[byleaf[x]["gain"] for x in sample if x in byleaf]
   if aa:ba.append(statistics.mean(aa))
   if gg:bg.append(statistics.mean(gg))
  phys[m]={"n":len(y),"breaks":sum(y),"auc":auc(y,p),"ap":ap(y,p),
   "gain_vs_fold_prevalence":statistics.mean(x["gain"] for x in leaf_stats),
   "brier":sum((q-v)**2 for q,v in zip(p,y))/len(y),
   "leaf_macro_auc":statistics.mean(x["auc"] for x in leaf_stats if math.isfinite(x["auc"])),
   "auc_leaf_bootstrap_ci95":[qtl(ba,.025),qtl(ba,.975)],
   "gain_leaf_bootstrap_ci95":[qtl(bg,.025),qtl(bg,.975)]}
 source={"sha256":sha(path),"bytes":path.stat().st_size,"body_pages_with_tokens":len(pnames),"numbered_pages_with_tokens":len(phys_pages),"physical_leaves_with_tokens":len(leaves),
  "unassigned_pages":sorted(set(pnames)-set(phys_pages)),"unassigned_body_lines_with_tokens":sum(len(pages[p]) for p in pnames if leaf[p] is None),
  "body_lines_with_tokens":sum(sum(any(w is not None for w in line["words"]) for line in ls) for ls in pages.values()),
  "tokens":sum(sum(w is not None for w in x["words"]) for ls in pages.values() for x in ls)}
 return {"transcription":label,"parser_policy":policy,"source":source,
  "page_split_calibration":{"heldout_pages":len(hp),"test_candidates":page_n,"test_breaks":page_breaks,
    "duplicate_line_embargo_unique_texts":ndup,"models":page_clean,
    "expected_from_article":{"pages":207,"lines":4130,"word_like_units":34963,"heldout_pages":42,"test_candidates":6190,"breaks":719,"auc":.843,"gain_bits_per_gap":.114}},
  "physical_leaf_loso":{"folds":len(leaves),"test_candidates":len(oof["full_tuple"]["y"]),"breaks":sum(oof["full_tuple"]["y"]),
    "models":{k:{a:(round(b,6) if isinstance(b,float) else [round(q,6) for q in b] if isinstance(b,list) else b) for a,b in v.items()} for k,v in phys.items()}},
  "folds":foldinfo}
def write_new_result(path,result):
 # Exclusive creation rejects existing files and symlinks; never overwrite a frozen run.
 with path.open("x",encoding="utf-8") as f:
  json.dump(result,f,indent=2,ensure_ascii=False)
  f.write("\n")

def main():
 for label,path in INPUTS.items():
  actual=sha(path)
  if actual!=EXPECTED_SHA256[label]:
   raise ValueError(f"{label}: corpus SHA-256 mismatch: {actual}")
 out={}
 for label,path in INPUTS.items():
  out[label]=[run(path,label,policy) for policy in ("primary","drop_uncertain_word")]
 result={"study":"Zenil & Uthamacumaran 2026, arXiv:2610.08861, Voynich line-boundary analysis","reimplementation":"naive categorical Bayes with alpha=0.5; page split every fifth lexicographically sorted page calibration; physical leaf LOSO; exact line string embargo; fixed seed 20261028; 1,999 bootstrap repetitions over leaves","results":out}
 write_new_result(ROOT/"line_boundary_results.json",result)
 print(json.dumps({k:[{"policy":x["parser_policy"],"source":x["source"],"page":x["page_split_calibration"],"leaf":x["physical_leaf_loso"]} for x in v] for k,v in out.items()},indent=2))
if __name__=="__main__":main()

