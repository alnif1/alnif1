import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

spec = importlib.util.spec_from_file_location("prep_photo", ROOT / "scripts" / "prep_photo.py")
prep_photo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prep_photo)


class PrepPhotoFallbackTests(unittest.TestCase):
    def test_prep_uses_fallback_when_rembg_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            input_path = tmp_path / "input.png"
            output_path = tmp_path / "output.png"

            image = Image.new("RGB", (200, 200), (180, 180, 180))
            for x in range(50, 150):
                for y in range(50, 150):
                    image.putpixel((x, y), (40, 120, 220))
            image.save(input_path)

            original_remove = prep_photo.remove
            def fake_remove(img):
                raise ConnectionError("simulated download timeout")

            prep_photo.remove = fake_remove
            try:
                prep_photo.prep(str(input_path), str(output_path))
            finally:
                prep_photo.remove = original_remove

            self.assertTrue(output_path.exists())
            self.assertEqual(Image.open(output_path).size, (200, 200))


if __name__ == "__main__":
    unittest.main()
