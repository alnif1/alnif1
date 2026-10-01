import sys
import cv2
import numpy as np
from PIL import Image
from rembg import remove


def _fallback_remove(image: Image.Image) -> Image.Image:
    rgb = np.array(image.convert("RGB"))
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]

    bg_mask = (sat < 35) & (val > 30) & (val < 220)
    fg_mask = (~bg_mask).astype(np.uint8) * 255
    kernel = np.ones((5, 5), np.uint8)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)

    rgba = np.zeros((*rgb.shape[:2], 4), dtype=np.uint8)
    rgba[:, :, :3] = rgb
    rgba[:, :, 3] = fg_mask
    return Image.fromarray(rgba, "RGBA")


def prep(input_path="source-photo.jpg", output_path="source-prepped.png"):
    img = Image.open(input_path).convert("RGBA")
    try:
        nobg = remove(img)
    except Exception as exc:
        print(f"[!] rembg model download failed ({exc}); using built-in fallback.")
        nobg = _fallback_remove(img)

    white_bg = Image.new("RGBA", nobg.size, (255, 255, 255, 255))
    comp = Image.alpha_composite(white_bg, nobg).convert("L")

    arr = np.array(comp)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(arr)

    Image.fromarray(enhanced).save(output_path)
    print(f"[+] Photo prepped: {output_path}")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep(src)
