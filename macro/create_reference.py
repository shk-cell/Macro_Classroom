"""
Generates empty seat reference images for V2 Image Recognition Macro.
CSS source:
  width: 28px; height: 28px;
  background: #0a1a0a;
  border: 1px solid #00cc33;

Generates images for common Windows DPI scales:
  100% -> 28x28  (empty_seat_100.png)
  125% -> 35x35  (empty_seat_125.png)
  150% -> 42x42  (empty_seat_150.png)
  default copy -> empty_seat.png (100% version)
"""

from PIL import Image, ImageDraw
import os

SCALES = {
    "100": 1.0,
    "125": 1.25,
    "150": 1.5,
}

BASE_SIZE   = 28
BG_COLOR    = (10, 26, 10)    # #0a1a0a
BORDER_COLOR = (0, 204, 51)   # #00cc33

os.makedirs("images", exist_ok=True)

for label, scale in SCALES.items():
    size = round(BASE_SIZE * scale)
    img  = Image.new("RGB", (size, size), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, size-1, size-1], outline=BORDER_COLOR, width=1)
    path = f"images/empty_seat_{label}.png"
    img.save(path)
    print(f"Saved: {path}  ({size}x{size}px)")

# default = 100%
import shutil
shutil.copy("images/empty_seat_100.png", "images/empty_seat.png")
print("\nDefault (100%): images/empty_seat.png")
print("\nDone! Use the image that matches your Windows display scale.")
print("  Settings -> Display -> Scale")
