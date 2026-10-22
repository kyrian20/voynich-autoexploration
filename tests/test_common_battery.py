#!/usr/bin/env python3
"""Contratos de datos/evaluación; no validación de conclusiones científicas."""
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT/'experiments/common_battery_2026_10_22'
spec = importlib.util.spec_from_file_location('battery',HERE/'script.py')
bc = importlib.util.module_from_spec(spec); spec.loader.exec_module(bc)

class BatteryTests(unittest.TestCase):
    def test_reconstruction_rejects_missing_or_changed_files(self):
        from scripts.verify_common_battery_reconstruction import verify
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            manifest=root/'manifest.json'
            (root/'result.json').write_bytes(b'original')
            manifest.write_text(json.dumps({'result.json':hashlib.sha256(b'original').hexdigest()}))
            self.assertEqual(verify(root,manifest)['status'],'EXACT_HISTORICAL_HASH_MATCH')
            (root/'result.json').write_bytes(b'changed')
            with self.assertRaises(ValueError):verify(root,manifest)
            (root/'result.json').unlink()
            with self.assertRaises(FileNotFoundError):verify(root,manifest)

    def test_metricas_con_conteos_independientes(self):
        m=bc.metrics([['am','yam'],['yam','am']])
        self.assertEqual(m['tokens'],4)
        self.assertEqual(m['longitud_media'],2.5)
        self.assertEqual(m['repeticion'],0)
        self.assertEqual(m['am_ll'],1)
        self.assertEqual(m['y_lf'],1)
        self.assertEqual(m['coincidencia_inicial'],0)
        self.assertAlmostEqual(bc.metrics([['abab']]*20)['h2'],0)

    def test_denominadores_ausentes_no_son_cero(self):
        m=bc.metrics([['bbb','ccc']])
        self.assertIsNone(m['am_ll']); self.assertIsNone(m['y_lf'])

    def test_control_positivo_y_vocabulario_desconocido(self):
        train=[['abababab','babababa']]*50
        self.assertGreater(bc.predictive(train,train)['ganancia_bits'],.9)
        self.assertTrue(__import__('math').isfinite(bc.predictive(train,[['zzzz']])['bigrama_bits']))

    def test_split_hoja_fisica(self):
        self.assertEqual(bc.is_test('f100r'),bc.is_test('f100v'))
        self.assertEqual(bc.is_test('f100r1'),bc.is_test('f100v2'))
        rows,_=bc.manuscript(ROOT/'data/transcriptions/eva_zl3b.txt')
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row['hoja'],bc.leaf(row['folio']))

    def test_copia_preserva_prefijo_y_es_reproducible(self):
        train=[['qokedy','qokain']]*30
        first=bc.generate(train,1000,17001,'preserva')
        self.assertEqual(first,bc.generate(train,1000,17001,'preserva'))
        self.assertTrue(all(w.startswith('qok') for w in first))
        self.assertNotEqual(first,bc.generate(train,1000,17002,'preserva'))

    def test_fuentes_y_version_exacta(self):
        bc.verify_freeze()
        self.assertEqual(hashlib.sha256((HERE/'script.py').read_bytes()).hexdigest(),json.loads((HERE/'implementation-freeze.json').read_text())['sha256'])
        expected={'vendor/naibbe_v2.py':'b566ad82e4b6ff0782ecdddebf77718dac44f292','vendor/references/naibbe_tables.csv':'5cd34fb81d80faf3b4d57dbf1719c05ffde25302'}
        for name,digest in expected.items():
            raw=(HERE/name).read_bytes()
            self.assertEqual(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),digest)
        self.assertEqual(bc.normalize('cæsar à é'),'c sar a e'.split())
        with self.assertRaises(ValueError): bc.reshape(['a'],[2])

    def test_archivo_reconstruye_todas_las_metricas(self):
        explicit=os.environ.get('BC_REPLAY_DIR')
        out=Path(explicit) if explicit else HERE/'data/run-03'
        if not (out/'tokens.jsonl.gz').exists():
            if explicit:
                self.fail('Requested replay directory has no tokens.jsonl.gz')
            self.skipTest('Archivo crudo solo local: publicación bloqueada por revisión automática; no se verifica replay en CI')
        data=json.loads((out/'resultados.json').read_text())
        for name,digest in json.loads((out/'SHA256.json').read_text()).items():
            self.assertEqual(bc.sha((out/name).read_bytes()),digest)
        raw=gzip.decompress((out/'tokens.jsonl.gz').read_bytes())
        self.assertEqual(bc.sha(raw),data['tokens_descomprimidos_sha256'])
        records=[json.loads(line) for line in raw.splitlines()]
        self.assertEqual(len(records),len(data['resultados']))
        for row,result in zip(records,data['resultados']):
            self.assertEqual((row['brazo'],row['semilla']),(result['brazo'],result['semilla']))
            self.assertEqual(bc.metrics(row['test']),result['test'])
            self.assertEqual(bc.metrics(row['train']),result['train'])
        selected=json.loads((out/'seleccion.json').read_text())
        for parts in selected.values():
            self.assertFalse({r['hoja'] for r in parts['train']} & {r['hoja'] for r in parts['test']})

if __name__=='__main__': unittest.main()
