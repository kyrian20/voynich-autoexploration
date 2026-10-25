import hashlib
import unittest
from scripts.render_coordinator_mask_preview import render

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

if __name__=='__main__': unittest.main()
