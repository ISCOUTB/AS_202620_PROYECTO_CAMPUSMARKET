"""Construye un índice visual de capturas de CI para revisar el producto."""
import base64
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "artifacts/e2e"
captures = [
    path for path in sorted(DIRECTORY.glob("*.png"))
    if path.name != "campusmarket-e2e.png" and not path.name.startswith("indice-")
]
if not captures:
    raise SystemExit("No hay capturas de flujo disponibles.")
width, height, padding = 460, 350, 16
sheet = Image.new("RGB", (width * 2 + padding * 3, height * ((len(captures) + 1) // 2) + padding), "#eef0f6")
draw = ImageDraw.Draw(sheet)
for index, path in enumerate(captures):
    x = padding + (index % 2) * (width + padding)
    y = padding + (index // 2) * height
    image = Image.open(path).convert("RGB")
    image.thumbnail((width, height - 35))
    sheet.paste(image, (x + (width - image.width) // 2, y + 25))
    draw.text((x, y), path.stem, fill="#29216b")
target = DIRECTORY / "indice-capturas.png"
sheet.save(target, optimize=True)
print("CAMPUSMARKET_SCREENSHOT_SHEET=" + base64.b64encode(target.read_bytes()).decode())
