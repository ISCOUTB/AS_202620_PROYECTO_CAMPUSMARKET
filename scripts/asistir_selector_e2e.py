"""Opera únicamente el selector de archivos del navegador/emulador aislado de CI."""
import argparse
import json
import re
import subprocess
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("platform", choices=["web", "android"])
parser.add_argument("--width", type=int, default=1440)
parser.add_argument("--height", type=int, default=1000)
args = parser.parse_args()
fixture = (Path(__file__).resolve().parents[1] / "artifacts/e2e/campusmarket-e2e.png").resolve()
deadline = time.monotonic() + 1100


def chrome(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        "http://127.0.0.1:4444" + path, data=data,
        headers={"Content-Type": "application/json"}, method=method,
    )
    with urllib.request.urlopen(request, timeout=4) as response:
        return json.load(response)["value"]


if args.platform == "web":
    prepared_sessions = set()
    while time.monotonic() < deadline:
        try:
            sessions = chrome("GET", "/sessions")
            if not sessions:
                time.sleep(0.2)
                continue
            sid = sessions[0]["id"]
            prefix = "/session/" + sid
            if sid not in prepared_sessions:
                prepared_sessions.add(sid)
            value = chrome("POST", prefix + "/execute/sync", {
                "script": """
                    if (!window.__campusmarketPickerHook) {
                      const original = HTMLInputElement.prototype.click;
                      HTMLInputElement.prototype.click = function() {
                        if (this.type === 'file') {
                          window.__campusmarketFileInput = this;
                          return;
                        }
                        return original.call(this);
                      };
                      window.__campusmarketPickerHook = true;
                    }
                    const input = window.__campusmarketFileInput;
                    if (input && !input.__campusmarketSelected) {
                      if (!input.isConnected) document.body.appendChild(input);
                      return true;
                    }
                    return false;
                """,
                "args": [],
            })
            if value:
                elements = chrome("POST", prefix + "/elements", {"using": "css selector", "value": "input[type=file]"})
                if elements:
                    element = elements[-1].get("element-6066-11e4-a52e-4f735466cecf") or elements[-1]["ELEMENT"]
                    chrome("POST", prefix + "/execute/sync", {
                        "script": "window.__campusmarketFileInput.__campusmarketSelected = true;",
                        "args": [],
                    })
                    chrome("POST", prefix + "/element/" + element + "/value", {"text": str(fixture)})
                    print("Selector Web: archivo PNG real entregado por ChromeDriver.", flush=True)
        except (OSError, KeyError, IndexError, ValueError, urllib.error.HTTPError):
            pass
        time.sleep(0.2)
else:
    selected = False
    while time.monotonic() < deadline:
        try:
            subprocess.run(
                ["adb", "shell", "uiautomator", "dump", "/data/local/tmp/campusmarket-window.xml"],
                check=True, capture_output=True, timeout=8,
            )
            xml = subprocess.check_output(["adb", "shell", "cat", "/sdcard/campusmarket-window.xml"], timeout=4)
            nodes = list(ET.fromstring(xml).iter("node"))
            picker = any("documentsui" in node.get("package", "") for node in nodes)
            if not picker:
                selected = False
            elif not selected:
                target = next(
                    (node for node in nodes if fixture.name in node.get("text", "") or fixture.name in node.get("content-desc", "")),
                    None,
                )
                if target is None:
                    target = next(
                        (node for node in nodes if node.get("text", "") == "Downloads" and node.get("clickable") == "true"),
                        None,
                    )
                if target is None:
                    target = next(
                        (node for node in nodes if node.get("content-desc", "") in {"Show roots", "Open navigation drawer", "Navigate up"}),
                        None,
                    )
                if target is not None:
                    bounds = [int(value) for value in re.findall(r"\d+", target.get("bounds", ""))]
                    if len(bounds) == 4:
                        x, y = (bounds[0] + bounds[2]) // 2, (bounds[1] + bounds[3]) // 2
                        subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)], check=True, timeout=4)
                        if fixture.name in target.get("text", ""):
                            selected = True
                            print("Selector Android: PNG real elegido en DocumentsUI.", flush=True)
        except (subprocess.SubprocessError, ET.ParseError, ValueError):
            pass
        time.sleep(0.25)
