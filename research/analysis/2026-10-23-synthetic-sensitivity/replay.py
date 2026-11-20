"""Replay full diagnostic into scratch and compare every scientific field."""
import json,subprocess,sys,tempfile
from pathlib import Path
BLOCK=Path(__file__).resolve().parent
sys.path.insert(0,str(BLOCK.parent/'2026-10-22-residual-order'))
from run_integrated import scientific_compare
with tempfile.TemporaryDirectory(prefix='voynich-synthetic-') as tmp:
 out=Path(tmp)/'results.json'
 with out.open('w') as stream:
  subprocess.run([sys.executable,str(BLOCK/'run.py')],stdout=stream,check=True)
 scientific_compare(json.loads((BLOCK/'results.json').read_text()),json.loads(out.read_text()))
subprocess.run([sys.executable,str(BLOCK/'verify.py')],check=True)
print('48 synthetic arms reproduced; scientific fields and hashes match.')
