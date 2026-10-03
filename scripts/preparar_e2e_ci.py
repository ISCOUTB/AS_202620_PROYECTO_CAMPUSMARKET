"""Prepara fixtures de imágenes y ChromeDriver oficial para CI, sin datos reales."""
import json
import os
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/e2e"
OUTPUT.mkdir(parents=True, exist_ok=True)
image = Image.new("RGB", (900, 650), "#eae7ff")
draw = ImageDraw.Draw(image)
draw.rounded_rectangle((155, 70, 590, 580), 25, fill="#5b4cf0")
draw.rectangle((180, 80, 200, 570), fill="#2d246f")
draw.rounded_rectangle((225, 115, 535, 235), 12, fill="#ffffff")
draw.text((250, 150), "CAMPUS MARKET", fill="#29216b")
draw.text((250, 180), "LIBRO DE PRUEBA E2E", fill="#29216b")
draw.rounded_rectangle((490, 295, 730, 590), 25, fill="#253341")
draw.rectangle((515, 320, 705, 385), fill="#a4d1b0")
for row in range(4):
    for column in range(4):
        left = 515 + column * 48
        top = 410 + row * 37
        draw.rounded_rectangle((left, top, left + 34, top + 23), 5, fill="#f7f8fc")
fixture = OUTPUT / "campusmarket-e2e.png"
image.save(fixture)
print("Fixture PNG generado para probar selección y subida reales; no se carga en producción.")

if "--chrome" in sys.argv:
    version = subprocess.check_output(["google-chrome", "--product-version"], text=True).strip()
    build = ".".join(version.split(".")[:3])
    url = "https://googlechromelabs.github.io/chrome-for-testing/latest-patch-versions-per-build-with-downloads.json"
    with urllib.request.urlopen(url, timeout=30) as response:
        metadata = json.load(response)
    release = metadata["builds"][build]
    download = next(item["url"] for item in release["downloads"]["chromedriver"] if item["platform"] == "linux64")
    archive = OUTPUT / "chromedriver.zip"
    urllib.request.urlretrieve(download, archive)
    directory = OUTPUT / "chrome-driver"
    with zipfile.ZipFile(archive) as zipped:
        for member in zipped.infolist():
            target = (directory / member.filename).resolve()
            if not target.is_relative_to(directory.resolve()):
                raise RuntimeError("Archivo ChromeDriver fuera de su directorio.")
        zipped.extractall(directory)
    binary = directory / "chromedriver-linux64/chromedriver"
    binary.chmod(0o755)
    with open(os.environ["GITHUB_PATH"], "a") as path_file:
        path_file.write(str(binary.parent) + "\n")
    (OUTPUT / "chrome-version.txt").write_text("Chrome " + version + "\nChromeDriver " + release["version"] + "\n")
    print("ChromeDriver oficial instalado para la versión de Chrome del runner.")
