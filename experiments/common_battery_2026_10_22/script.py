#!/usr/bin/env python3
"""BC-2026-10-22: batería descriptiva reproducible; véase PROTOCOL.md."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from contextlib import contextmanager, redirect_stdout
import gzip
import hashlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import platform
import random
import re
import statistics
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from scripts.audit_token_policy_sensitivity import read_records
from scripts.ivtff_lossless import tokens

SEEDS = list(range(17001, 17017))
FEATURES = {'h2': .2, 'longitud_media': 1., 'repeticion': .01, 'coincidencia_inicial': .2}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def encode(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, allow_nan=False, separators=(',', ':'))+'\n').encode()

def verify_freeze():
    frozen = json.loads((HERE/'freeze.json').read_text())
    for path, expected in frozen['files'].items():
        if sha((ROOT/path).read_bytes()) != expected:
            raise ValueError('Fuente congelada modificada: '+path)
    return frozen

def leaf(folio):
    match = re.match(r'f\d+', folio)
    if not match:
        raise ValueError(folio)
    return match[0]

def is_test(folio):
    return int(sha(leaf(folio).encode()), 16) % 5 == 0

def manuscript(path, comma='split'):
    _, rows = read_records(path)
    selected, excluded = [], Counter()
    for r in rows:
        if r['currier'] != 'B' or r['locus'] != 'P0':
            excluded['fuera_B_P0'] += 1
            continue
        words = tokens([r['payload']], uncertain_space=comma)
        if len(words) < 2:
            excluded['menos_2_tokens'] += 1
            continue
        selected.append({'id':r['id'], 'folio':r['folio'], 'hoja':leaf(r['folio']),
                         'raw':r['body'], 'source_line':r['source_line'], 'tokens':words})
    return selected, dict(excluded)

def budget(rows, limit=4000):
    out, used = [], 0
    for row in rows:
        if used + len(row['tokens']) > limit:
            break
        out.append(row)
        used += len(row['tokens'])
    if not out:
        raise ValueError('Partición vacía')
    return out

def words_of(lines):
    return [w for line in lines for w in line]

def reshape(words, sizes):
    if len(words) < sum(sizes):
        raise ValueError('Tokens insuficientes; no repetir fuentes')
    out, offset = [], 0
    for size in sizes:
        out.append(words[offset:offset+size]); offset += size
    return out

def entropy(counts):
    total = sum(counts.values())
    return -sum((n/total)*math.log2(n/total) for n in counts.values()) if total else 0.

def metrics(lines):
    words = words_of(lines)
    if not words:
        raise ValueError('Sin palabras')
    pairs = [(a,b) for line in lines for a,b in zip(line,line[1:])]
    chars = Counter((a,b) for w in words for a,b in zip(w,w[1:]))
    contexts = Counter()
    for (a,b), n in chars.items(): contexts[a] += n
    h2 = entropy(chars)-entropy(contexts)
    initials = Counter(w[0] for w in words)
    expected = sum((n/len(words))**2 for n in initials.values())
    def enrichment(predicate, end):
        base = sum(map(predicate, words))/len(words)
        return (sum(predicate(line[end]) for line in lines)/len(lines))/base if base else None
    return {'h2':h2, 'longitud_media':sum(map(len,words))/len(words),
            'repeticion':sum(a==b for a,b in pairs)/len(pairs) if pairs else None,
            'coincidencia_inicial':sum(a[0]==b[0] for a,b in pairs)/len(pairs)/expected if pairs else None,
            'am_ll':enrichment(lambda w:w.endswith('am'),-1),
            'y_lf':enrichment(lambda w:w.startswith('y'),0),
            'tokens':len(words), 'lineas':len(lines), 'tipos':len(set(words)),
            'soporte_am':sum(w.endswith('am') for w in words),
            'soporte_y':sum(w.startswith('y') for w in words)}

def predictive(train, test):
    # Solo transiciones internas: no inventar enlaces entre palabras o líneas.
    vocab = set(''.join(words_of(train)))
    unk = '\x00'
    v = len(vocab)+1
    uni, contexts, bi = Counter(), Counter(), Counter()
    for w in words_of(train):
        for a,b in zip(w,w[1:]):
            uni[b] += 1; contexts[a] += 1; bi[a,b] += 1
    n, u, b = 0, 0., 0.
    for word in words_of(test):
        word = [c if c in vocab else unk for c in word]
        for a,c in zip(word,word[1:]):
            u -= math.log2((uni[c]+.1)/(sum(uni.values())+.1*v))
            b -= math.log2((bi[a,c]+.1)/(contexts[a]+.1*v)); n += 1
    return {'transiciones':n, 'unigrama_bits':u/n, 'bigrama_bits':b/n, 'ganancia_bits':(u-b)/n}

def onset(w):
    for prefix in ('qok','qot','qo','cth','che','chi','ch','sh','ok','ot','ol','d','s','y','k','t','l','r'):
        if w.startswith(prefix): return prefix
    return w[:1]

def generate(train, n, seed, mode):
    rng = random.Random(seed)
    counts = Counter(words_of(train))
    top = sorted(counts, key=lambda w:(-counts[w],w))[:200]
    weights = [counts[w] for w in top]
    alphabet = sorted(set(''.join(counts)))
    frequencies = Counter(''.join(words_of(train)))
    lengths = [len(w) for w in words_of(train)]
    out = []
    for _ in range(n):
        if mode == 'iid':
            size = rng.choice(lengths)
            w = ''.join(rng.choices(alphabet, weights=[frequencies[c] for c in alphabet], k=size))
        elif out and rng.random() < .85:
            w = rng.choice(out[-50:])
            if rng.random() < .25:
                donor = rng.choices(top, weights=weights)[0]
                if mode == 'preserva':
                    w = onset(w)+donor[len(onset(donor)):]
                else:
                    i = rng.randrange(len(w)); w = w[:i]+rng.choice(alphabet)+w[i+1:]
        else:
            w = rng.choices(top,weights=weights)[0]
        out.append(w)
    return out

def body(raw, anchor):
    text = raw.decode('latin-1' if b'Character set encoding: ISO-8859-1' in raw[:4000] else 'utf-8-sig')
    start = text.find(anchor)
    if start < 0: raise ValueError('Ancla ausente')
    end = re.search(r'(?im)^(?:\*\*\* END OF|End of Project Gutenberg)',text[start:])
    if not end: raise ValueError('Fin ausente')
    return text[start:start+end.start()]

def normalize(text):
    text = unicodedata.normalize('NFD',text).lower()
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return re.findall('[a-z]+',text)

@contextmanager
def in_directory(path):
    old = Path.cwd()
    try:
        os.chdir(path); yield
    finally: os.chdir(old)

def load_naibbe():
    spec = importlib.util.spec_from_file_location('bc_naibbe', HERE/'vendor/naibbe_v2.py')
    mod = importlib.util.module_from_spec(spec)
    with in_directory(HERE/'vendor'), redirect_stdout(io.StringIO()): spec.loader.exec_module(mod)
    return mod

def encrypt(mod, lines, seed):
    random.seed(seed)
    out = []
    before = mod.ambiguity_retries
    for line in lines:
        cleaned = mod.clean_line(' '.join(line))
        if not re.fullmatch('[a-z]+',cleaned): raise ValueError('Alfabeto Naibbe no admitido')
        out.append(mod.encrypt_naibbe(cleaned,mod.naibbe_tables,mod.placeholder_to_glyph,use_78=True))
    return out, mod.ambiguity_retries-before

def quantile(values, p):
    values = sorted(values); index = (len(values)-1)*p
    lo = int(index); hi = min(lo+1,len(values)-1)
    return values[lo]+(values[hi]-values[lo])*(index-lo)

def bootstrap(rows):
    groups = defaultdict(list)
    for row in rows: groups[row['hoja']].append(row['tokens'])
    keys = sorted(groups); rng = random.Random(17099)
    values = defaultdict(list)
    for _ in range(400):
        sampled = [line for k in rng.choices(keys,k=len(keys)) for line in groups[k]]
        for key,value in metrics(sampled).items():
            if value is not None: values[key].append(value)
    return {'hojas':keys,'replicas':400,'intervalos':{k:[quantile(v,.025),quantile(v,.975)] for k,v in values.items()}}

def run(out):
    if out.exists() and any(out.iterdir()): raise ValueError('No sobrescribir resultados; usar directorio nuevo')
    frozen = verify_freeze()
    out.mkdir(parents=True,exist_ok=True)
    corpus_receipt = {}
    split = {}
    for label,path,comma in [('ZL3b_split','eva_zl3b.txt','split'),('ZL3b_join','eva_zl3b.txt','join'),('IT2a_split','eva_it2a.txt','split')]:
        rows, excluded = manuscript(ROOT/'data/transcriptions'/path,comma)
        train = budget([r for r in rows if not is_test(r['folio'])])
        test = budget([r for r in rows if is_test(r['folio'])])
        assert not {r['hoja'] for r in train} & {r['hoja'] for r in test}
        split[label] = (train,test)
        corpus_receipt[label] = {'exclusiones':excluded,'train':train,'test':test}
    (out/'seleccion.json').write_bytes(encode(corpus_receipt))
    train_rows,test_rows = split['ZL3b_split']
    real_train = [r['tokens'] for r in train_rows]; real_test = [r['tokens'] for r in test_rows]
    sizes = {'train':list(map(len,real_train)), 'test':list(map(len,real_test))}
    target = metrics(real_test)
    mod = load_naibbe()
    archive = bytearray(); results = []
    def record(name, seed, train, test, extra=None, matched=True):
        mt = metrics(test)
        delta = {k:(mt[k]-target[k])/tol for k,tol in FEATURES.items()}
        results.append({'brazo':name,'semilla':seed,'test':mt,'train':metrics(train),
                        'predictivo':predictive(train,test), 'D':statistics.mean(x*x for x in delta.values()),
                        'cercania_conjunta':all(abs(x)<=1 for x in delta.values()),
                        'tamano_igualado':matched,'delta_normalizada':delta, 'extra':extra or {}})
        archive.extend(encode({'brazo':name,'semilla':seed,'train':train,'test':test}))
    record('VMS_ZL3b',None,real_train,real_test)
    for label,(tr,te) in split.items():
        if label == 'ZL3b_split': continue
        record('VMS_'+label,None,[r['tokens'] for r in tr],[r['tokens'] for r in te],matched=False)
    sources = [
        ('latin','data/reference_corpora/latin/caesar_de_bello_gallico_latin.txt','C. IULI CAESARIS DE BELLO GALLICO COMMENTARIUS PRIMUS'),
        ('italiano','data/reference_corpora/italian/dante_divina_commedia.txt','Nel mezzo del cammin di nostra vita'),
        ('ingles_historico','data/reference_corpora/latin/vulgate.txt',frozen['english_anchor'])]
    views = {}
    for label,path,anchor in sources:
        text = body((ROOT/path).read_bytes(),anchor)
        lines = [normalize(line) for line in text.splitlines()]
        lines = [line for line in lines if line]
        words = words_of(lines)
        assert len(words)>=16000
        # Particiones contiguas por línea; el corte no puede compartir palabras.
        tr,te,used = [],[],0
        for line in lines:
            if used < 8000: tr.append(line)
            elif sum(map(len,te)) < 8000: te.append(line)
            else: break
            used += len(line)
        views[label] = {'train':tr,'test':te}
        record('lenguaje_'+label,None,reshape(words_of(tr),sizes['train']),reshape(words_of(te),sizes['test']))
        record('lenguaje_original_'+label,None,tr,te,matched=False)
    (out/'vistas_referencia.json').write_bytes(encode(views))
    for seed in SEEDS:
        for label,view in views.items():
            tr,retry_tr = encrypt(mod,view['train'],seed)
            te,retry_te = encrypt(mod,view['test'],seed+100000)
            extra={'reintentos_train':retry_tr,'reintentos_test':retry_te}
            record('naibbe_'+label,seed,reshape(words_of(tr),sizes['train']),reshape(words_of(te),sizes['test']),extra)
            record('naibbe_original_'+label,seed,tr,te,extra,matched=False)
        for mode in ('caracter','preserva','iid'):
            tr = reshape(generate(real_train,sum(sizes['train']),seed,mode),sizes['train'])
            te = reshape(generate(real_train,sum(sizes['test']),seed+100000,mode),sizes['test'])
            record('generador_'+mode,seed,tr,te)
        # Permutar ambos conjuntos por separado, sin contaminación de folios.
        shuffled = []
        for lines,s in ((real_train,seed),(real_test,seed+100000)):
            ws = words_of(lines); random.Random(s).shuffle(ws)
            shuffled.append(reshape(ws,list(map(len,lines))))
        record('VMS_permutado',seed,*shuffled)
        for label in ('ZL3b_join','IT2a_split'):
            tr,te = [[r['tokens'] for r in part] for part in split[label]]
            ws = words_of(te); random.Random(seed+100000).shuffle(ws)
            record('permutado_'+label,seed,tr,reshape(ws,list(map(len,te))),matched=False)
    (out/'tokens.jsonl.gz').write_bytes(gzip.compress(bytes(archive),mtime=0))
    groups = defaultdict(list)
    for row in results: groups[row['brazo']].append(row)
    summary = {}
    for name, rows in groups.items():
        fields = {k:[r['test'][k] for r in rows if r['test'][k] is not None] for k in target}
        summary[name]={'n':len(rows),'cercanos':sum(r['cercania_conjunta'] for r in rows),
                       'D_mediana':statistics.median(r['D'] for r in rows),
                       'metricas':{k:{'mediana':statistics.median(v),'P025':quantile(v,.025),'P975':quantile(v,.975)} for k,v in fields.items() if v},
                       'ganancia_mediana':statistics.median(r['predictivo']['ganancia_bits'] for r in rows)}
    positive = all(summary['lenguaje_'+k]['ganancia_mediana']>=.05 for k in ('latin','italiano'))
    negative = summary['generador_iid']['ganancia_mediana']<=.1
    alerts = [r for r in results if r['brazo'].startswith(('naibbe_','generador_')) and ((r['test']['am_ll'] or 0)>=3 or (r['test']['y_lf'] or 0)>=2)]
    payload = {'id':'BC-2026-10-22','estado':'NEGATIVE' if positive and negative else 'BLOCKED',
               'puertas':{'positiva':positive,'negativa':negative},'alertas_C001':alerts,
               'resultados':results,'resumen':summary,'bootstrap_VMS':bootstrap(test_rows),
               'python':platform.python_version(),'pandas':__import__('pandas').__version__,
               'semillas':SEEDS,'protocolo_sha256':sha((HERE/'PROTOCOL.md').read_bytes()),
               'script_sha256':sha(Path(__file__).read_bytes()),'tokens_descomprimidos_sha256':sha(bytes(archive))}
    (out/'resultados.json').write_bytes(encode(payload))
    manifest = {p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file()}
    (out/'SHA256.json').write_bytes(encode(manifest))
    print(json.dumps({'estado':payload['estado'],'brazos':len(summary),'evaluaciones':len(results),'puertas':payload['puertas'],'alertas_C001':len(alerts),'tokens_gzip_bytes':len((out/'tokens.jsonl.gz').read_bytes())},ensure_ascii=False))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args(); run(args.out)

if __name__ == '__main__': main()
