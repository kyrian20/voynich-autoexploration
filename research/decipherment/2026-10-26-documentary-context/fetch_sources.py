"""Recover archived public source URLs and compare the exact received bytes."""
import argparse,hashlib,json,urllib.request
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--cache-dir',type=Path,required=True);p.add_argument('--execute',action='store_true');a=p.parse_args()
    if not a.execute:print('DRY_RUN: no downloads; use --execute');return
    if a.cache_dir.exists():raise SystemExit('Refuse existing destination')
    a.cache_dir.mkdir(parents=True)
    sources=json.loads(Path(__file__).with_name('download-receipts.json').read_text());out=[]
    for source in sources:
        if source['status']!='retrieved':continue
        name=source['file'];url=source['url']
        if Path(name).name!=name or not url.startswith('https://'):raise ValueError('Invalid archived source')
        result={'file':name,'url':url,'expected_sha256':source['sha256']}
        try:
            with urllib.request.urlopen(url,timeout=40) as response:raw=response.read()
            (a.cache_dir/name).write_bytes(raw);observed=hashlib.sha256(raw).hexdigest()
            result.update(status='MATCH' if observed==source['sha256'] else 'BYTES_CHANGED',sha256=observed,bytes=len(raw))
        except Exception as error:result.update(status='DOWNLOAD_FAILED',category=type(error).__name__)
        out.append(result);print(name,result['status'],flush=True)
    (a.cache_dir/'retrieval-check.json').write_text(json.dumps(out,indent=2)+'\n')

if __name__=='__main__':main()
