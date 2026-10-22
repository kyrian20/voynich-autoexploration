#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import re
ISSUES={
'latin/vulgate.txt':('WRONG_LANGUAGE_FOR_LATIN','English','The Bible, Douay-Rheims, Complete'),
'latin/caesar_gallic_wars.txt':('WRONG_LANGUAGE_FOR_LATIN','English','De Bello Gallico and Other Commentaries, English translation'),
'latin/cicero_de_officiis_latin.txt':('BILINGUAL_REQUIRES_FILTER_AUDIT','Latin and English','De Officiis #47001'),
'arabic/quran_arabic.txt':('WRONG_LANGUAGE_AND_WORK','English','Drum-Taps #8801'),
'english/kjv_bible.txt':('WRONG_WORK_SAME_LANGUAGE','English','The Book of Mormon #17'),
'latin/cicero_caesar_latin.txt':('BLOCKED_EMPTY','none','empty')}

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);root=p.parse_args().repo.resolve()
 files=[];references=[]
 for path in sorted((root/'data/reference_corpora').rglob('*.txt')):
  relative=path.relative_to(root/'data/reference_corpora').as_posix();raw=path.read_bytes();text=raw.decode('utf-8-sig',errors='replace')
  header=text.splitlines()[:100]
  row={'path':str(path.relative_to(root)),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),
       'header_title':[s for s in header if s.startswith('Title:')],'header_language':[s for s in header if s.startswith('Language:')]}
  if relative in ISSUES:
   kind,language,title=ISSUES[relative];row.update(issue=kind,adjudicated_language=language,adjudicated_work=title)
   row['evidence']=[s for s in header if re.search('translation|English|Language:|Title:|empty',s,re.I)][:12]
  else:row['issue']='NO_HEADER_CONTRADICTION_DETECTED_NOT_FULLY_ADJUDICATED'
  files.append(row)
 for path in sorted(root.rglob('*.py')):
  if '.git' in path.parts or path.is_relative_to(Path(__file__).resolve().parent):continue
  if path in {root/'scripts/audit_historical_latin_loaders.py', root/'scripts/audit_remaining_reference_loaders.py'}:continue  # Explicit diagnostic exclusions, not historical corpus use
  text=path.read_text(encoding='utf-8',errors='replace')
  for name,(issue,_,_) in ISSUES.items():
   hits=[i for i,line in enumerate(text.splitlines(),1) if Path(name).name in line]
   if hits:references.append({'script':str(path.relative_to(root)),'input':name,'lines':hits,
      'status':'STATIC_REFERENCE_NOT_PROOF_OF_EXECUTION_OR_INVALID_RESULT',
      'mentions_english_stopword_filter':'english_stopwords' in text})
 print(json.dumps({'files':files,'issue_files':len(ISSUES),'static_references':references,
   'distinct_scripts_with_direct_reference':len({r['script'] for r in references}),
   'limits':['No historical output or claim retracted automatically.','References can be optional, unused, or subject to filters.','Importer and transitive dependencies are not exhaustively resolved.']},indent=2))
if __name__=='__main__':main()
