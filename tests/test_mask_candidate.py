import hashlib
import io
import unittest

from PIL import Image, PngImagePlugin
from scripts.export_mask_candidate import export_candidate


class MaskCandidateTests(unittest.TestCase):
    def setUp(self):
        image = Image.new('RGB', (12, 10), (100, 150, 200))
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text('Comment', 'SECRET_SOURCE_LABEL')
        stream = io.BytesIO()
        image.save(stream, format='PNG', pnginfo=metadata)
        self.source = stream.getvalue()
        self.plan = {'source_sha256': hashlib.sha256(self.source).hexdigest(),
                     'source_size': [12, 10], 'crop_xywh': [2, 1, 8, 8],
                     'mask_rectangles_xywh': [[3, 2, 2, 3]]}

    def test_pixels_crop_and_metadata(self):
        data = export_candidate(self.plan, self.source)
        self.assertNotIn(b'SECRET_SOURCE_LABEL', data)
        with Image.open(io.BytesIO(data)) as image:
            self.assertEqual(image.size, (8, 8))
            self.assertEqual(image.mode, 'RGB')
            self.assertFalse(image.info)
            for y in range(8):
                for x in range(8):
                    expected = (0, 0, 0) if 1 <= x < 3 and 1 <= y < 4 else (100, 150, 200)
                    self.assertEqual(image.getpixel((x, y)), expected)
        self.assertEqual(data, export_candidate(self.plan, self.source))

    def test_decoded_dimensions_not_just_plan(self):
        self.plan['source_size'] = [13, 10]
        with self.assertRaisesRegex(ValueError, 'Decoded'):
            export_candidate(self.plan, self.source)

    def test_wrong_hash_and_missing_mask(self):
        with self.assertRaises(ValueError):
            export_candidate(self.plan, self.source + b'x')
        self.plan['mask_rectangles_xywh'] = []
        with self.assertRaises(ValueError):
            export_candidate(self.plan, self.source)

    def test_invalid_geometry(self):
        for rect in [[-1, 0, 2, 2], [0, 0, 0, 2], [11, 9, 2, 2], [True, 0, 1, 1]]:
            self.plan['mask_rectangles_xywh'] = [rect]
            with self.assertRaises(ValueError):
                export_candidate(self.plan, self.source)


if __name__ == '__main__':
    unittest.main()
