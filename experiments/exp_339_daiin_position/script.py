"""
exp_339: daiin and d-Onset Positional Grammar — A vs B Dialect Divergence (H541)

Background:
- F339 (exp_337): A-dialect 'aiin' suffix LL_enr=1.225× vs B-dialect 0.634×
- H541: Is A-dialect daiin LL-enriched? Does this explain the aiin LL enrichment?
- B-dialect: d-onset is known to be LF-enriched (exp_293, F294)
"""

import os, re
from collections import Counter, defaultdict

REPO_DIR  = os.path.expanduser('~/voynich-cryptanalyst')
DATA_PATH = os.path.join(REPO_DIR, 'data/transcriptions/eva_zl3b.txt')

ONSET_ORDER=[('qok','qok'),('qot','qot'),('qo','qo'),('cth','cth'),
    ('ch','ch'),('sh','sh'),('ok','ok'),('ot','ot'),('ol','ol'),
    ('d','d'),('s','s'),('y','y'),('k','k'),('t','t'),
    ('l','l'),('r','r'),('p','p'),('f','f'),('o','o')]

def folio_base(folio): return re.sub(r'[rv]$', '', folio)
def classify_dialect(stats):
    total=stats['total']
    if total==0: return 'unknown'
    return 'B' if (stats['edy']+stats['eedy'])/total>=0.05 else 'A'

folio_word_stats=defaultdict(lambda:{'total':0,'edy':0,'eedy':0})
with open(DATA_PATH,'r',encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line or line.startswith('#'): continue
        m=re.match(r'<([^.]+)\.(\d+),([^>]+)>',line)
        if not m: continue
        folio=m.group(1).lstrip('+*=&~'); fb=folio_base(folio)
        text=re.sub(r'<[^>]+>','',line)
        words=[w for w in re.split(r'[-.\s]',text) if re.match(r'^[a-z]+$',w) and len(w)>=2]
        for w in words:
            folio_word_stats[fb]['total']+=1
            if w.endswith('eedy'): folio_word_stats[fb]['eedy']+=1
            elif w.endswith('edy'): folio_word_stats[fb]['edy']+=1
folio_dialect={fb:classify_dialect(stats) for fb,stats in folio_word_stats.items()}
records = []
with open(DATA_PATH,'r',encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line or line.startswith('#'): continue
        m=re.match(r'<([^.]+)\.(\d+),([^>]+)>',line)
        if not m: continue
        folio=m.group(1); locus_code=m.group(3)
        folio=folio.lstrip('+*=&~'); fb=folio_base(folio)
        dialect=folio_dialect.get(fb,'unknown')
        if dialect not in ('A','B'): continue
        lc=locus_code.lstrip('+*=/~&')
        if not lc.lstrip('@').startswith('P'): continue
        text=re.sub(r'<[^>]+>','',line)
        words=[w for w in re.split(r'[-.\s]',text) if re.match(r'^[a-z]+$',w) and len(w)>=2]
        if len(words)<2: continue
        for i,w in enumerate(words):
            if i==0: pos='LF'
            elif i==len(words)-1: pos='LL'
            else: pos='MID'
            records.append((w,pos,dialect))

for dialect in ['B','A']:
    recs = [(w,pos) for w,pos,d in records if d==dialect]
    total = len(recs)
    pos_c = Counter(pos for w,pos in recs)
    P_LF = pos_c['LF']/total
    P_LL = pos_c['LL']/total
    print(f"\n  {dialect}-dialect baseline: P_LF={P_LF:.3f}, P_LL={P_LL:.3f}")
    for w in ['daiin','dain','dar','dal','dol','dam']:
        ws = [(w2,pos) for w2,pos in recs if w2==w]
        if len(ws) >= 5:
            wc = Counter(pos for w2,pos in ws)
            n2 = len(ws)
            ll_e = (wc['LL']/n2)/P_LL if P_LL>0 else 0
            lf_e = (wc['LF']/n2)/P_LF if P_LF>0 else 0
            print(f"    {w:<10} N={n2:>4}: LF={wc['LF']:>3}({100*wc['LF']/n2:.1f}%, E={lf_e:.2f}×) MID={wc['MID']:>4}({100*wc['MID']/n2:.1f}%) LL={wc['LL']:>3}({100*wc['LL']/n2:.1f}%, E={ll_e:.2f}×)")
