import hashlib
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from scripts.render_coordinator_mask_preview import main, render

class CoordinatorMaskTests(unittest.TestCase):
    def setUp(self):
        self.source=b'fixture bytes, not a source image'
        self.plan={'source_sha256':hashlib.sha256(self.source).hexdigest(),
                   'source_size':[100,100],'crop_xywh':[5,5,90,90],
                   'mask_rectangles_xywh':[[10,10,20,20]]}

    def test_wrong_source_rejected(self):
        with self.assertRaises(ValueError): render(self.plan,b'changed')

    def test_invalid_geometry_rejected(self):
        for rect in [[-1,0,2,2],[0,0,0,2],[90,90,20,20],[True,0,1,1],[1.2,0,2,2]]:
            self.plan['mask_rectangles_xywh']=[rect]
            with self.assertRaises(ValueError): render(self.plan,self.source)

    def test_missing_plan_rejected(self):
        self.plan['crop_xywh']=None
        with self.assertRaises(ValueError): render(self.plan,self.source)

    def test_preview_warns_about_embedded_source_and_is_deterministic(self):
        data=render(self.plan,self.source)
        self.assertEqual(data,render(self.plan,self.source))
        self.assertIn(b'not blinded input',data)
        self.assertIn(b'Original image is embedded and recoverable',data)
        self.assertIn(b'<rect',data)
        self.assertIn(b'viewBox="5 5 90 90"',data)


    def _cli_paths(self, directory):
        root = Path(directory)
        source = root / 'source.jpg'
        plan = root / 'plan.json'
        source.write_bytes(self.source)
        plan.write_text(json.dumps({'plans': [dict(self.plan, folio='f2r')]}), encoding='utf-8')
        return source, plan

    def _run_cli(self, plan, source, output):
        args = ['render_coordinator_mask_preview.py', '--plan', str(plan),
                '--folio', 'f2r', '--source', str(source), '--out', str(output)]
        with patch('sys.argv', args), redirect_stdout(io.StringIO()):
            main()

    def test_cli_creates_new_preview_but_refuses_second_write(self):
        with TemporaryDirectory() as tmp:
            source, plan = self._cli_paths(tmp)
            output = Path(tmp) / 'nested' / 'preview.svg'
            self._run_cli(plan, source, output)
            first = output.read_bytes()
            self.assertIn(b'COORDINATOR ONLY', first)
            with self.assertRaises(FileExistsError):
                self._run_cli(plan, source, output)
            self.assertEqual(output.read_bytes(), first)

    def test_cli_cannot_overwrite_source_plan_or_existing_asset(self):
        with TemporaryDirectory() as tmp:
            source, plan = self._cli_paths(tmp)
            existing = Path(tmp) / 'reviewed.svg'
            existing.write_bytes(b'REVIEWED_ASSET_DO_NOT_REPLACE')
            originals = {p: p.read_bytes() for p in (source, plan, existing)}
            for target in originals:
                with self.subTest(target=target.name):
                    with self.assertRaises(FileExistsError):
                        self._run_cli(plan, source, target)
            for target, expected in originals.items():
                self.assertEqual(target.read_bytes(), expected)

    def test_cli_cannot_follow_output_symlink_to_source(self):
        with TemporaryDirectory() as tmp:
            source, plan = self._cli_paths(tmp)
            link = Path(tmp) / 'preview.svg'
            try:
                link.symlink_to(source)
            except (OSError, NotImplementedError):
                self.skipTest('Symlinks unsupported in test environment')
            with self.assertRaises(FileExistsError):
                self._run_cli(plan, source, link)
            self.assertEqual(source.read_bytes(), self.source)

if __name__=='__main__': unittest.main()
