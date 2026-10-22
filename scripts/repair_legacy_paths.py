#!/usr/bin/env python3
"""Reproducible, AST-verified maintenance codemod. Preview by default."""
import ast,hashlib,json
from pathlib import Path
import argparse, sys
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from scripts.audit_legacy_portability import algorithm_digest
parser=argparse.ArgumentParser(description='Preview legacy root repairs; --apply explicitly writes verified path-only changes.')
parser.add_argument('--apply',action='store_true')
APPLY=parser.parse_args().apply
legacy=('/Users/asash/voynich-cryptanalyst','~/voynich-cryptanalyst')
records=[]
for p in sorted((root/'experiments').rglob('*.py')):
 raw=p.read_bytes();text=raw.decode();tree=ast.parse(text);lines=text.splitlines(keepends=True)
 offsets=[];n=0
 for line in lines:offsets.append(n);n+=len(line)
 def pos(line,col):return offsets[line-1]+len(lines[line-1].encode()[:col].decode())
 edits=[];targets=[]
 for node in ast.walk(tree):
  if not isinstance(node,ast.Constant) or not isinstance(node.value,str):continue
  for old in legacy:
   if node.value==old or node.value.startswith(old+'/'):
    rel=node.value[len(old):].lstrip('/')
    expression='str(_RepositoryPath(__file__).resolve().parents[2]'+(' / '+repr(rel) if rel else '')+')'
    edits.append((pos(node.lineno,node.col_offset),pos(node.end_lineno,node.end_col_offset),expression))
    targets.append({'relative_path':rel or '.', 'exists_at_audit':(root/(rel or '.')).exists()})
 if not edits:continue
 assert not any(isinstance(n,ast.Name) and n.id=='_RepositoryPath' for n in ast.walk(tree))
 for start,end,replacement in sorted(edits,reverse=True):text=text[:start]+replacement+text[end:]
 # Insert after module docstring and __future__ imports, preserving shebang/encoding.
 revised=ast.parse(text);prefix=[]
 for node in revised.body:
  if isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and isinstance(node.value.value,str) and not prefix:
   prefix.append(node);continue
  if isinstance(node,ast.ImportFrom) and node.module=='__future__':prefix.append(node);continue
  break
 if prefix:insert_line=prefix[-1].end_lineno
 else:insert_line=revised.body[0].lineno-1
 ls=text.splitlines(keepends=True);ls.insert(insert_line,'from pathlib import Path as _RepositoryPath\n');text=''.join(ls)
 ast.parse(text)
 assert len(p.relative_to(root).parts)==3, 'Unexpected script depth'
 assert algorithm_digest(raw.decode())==algorithm_digest(text), 'Non-path algorithm change'
 if APPLY:p.write_text(text)
 records.append({'path':p.relative_to(root).as_posix(),'before_sha256':hashlib.sha256(raw).hexdigest(),'after_sha256':hashlib.sha256(text.encode()).hexdigest(),'algorithm_ast_sha256':algorithm_digest(raw.decode()),'replacement_count':len(edits),'targets':targets})
folder=root/'research/maintenance/2026-10-22-intensive';folder.mkdir(parents=True,exist_ok=True)
manifest=folder/'path-migration.json'
existing=json.loads(manifest.read_text())['files'] if manifest.exists() else []
combined={entry['path']:entry for entry in existing}
combined.update({entry['path']:entry for entry in records})
if APPLY and records:manifest.write_text(json.dumps({'policy':'Only legacy root literals and one import changed; no input substitution or statistical parameter changes. Missing targets remain explicit external prerequisites.','files':sorted(combined.values(),key=lambda x:x['path'])},indent=2)+'\n')
print(len(records),'files;',sum(r['replacement_count'] for r in records),'replacements')
