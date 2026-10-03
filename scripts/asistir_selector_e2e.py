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
        "http://127.0.0.1:4444" + path,
        data=data,
        headers={"Content-Type": "application/json"},
        method=method,
    )
    with urllib.request.urlopen(request, timeout=4) as response:
        return json.load(response)["value"]


def node_label(node):
    return " ".join(
        value.strip()
        for value in (node.get("text", ""), node.get("content-desc", ""))
        if value.strip()
    )


def node_bounds(node):
    values = [int(value) for value in re.findall(r"\d+", node.get("bounds", ""))]
    return values if len(values) == 4 else None


def tap_node(node):
    bounds = node_bounds(node)
    if not bounds:
        return False
    x = (bounds[0] + bounds[2]) // 2
    y = (bounds[1] + bounds[3]) // 2
    subprocess.run(
        ["adb", "shell", "input", "tap", str(x), str(y)],
        check=True,
        timeout=4,
    )
    return True


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
            value = chrome(
                "POST",
                prefix + "/execute/sync",
                {
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
                },
            )
            if value:
                elements = chrome(
                    "POST",
                    prefix + "/elements",
                    {"using": "css selector", "value": "input[type=file]"},
                )
                if elements:
                    element = (
                        elements[-1].get("element-6066-11e4-a52e-4f735466cecf")
                        or elements[-1]["ELEMENT"]
                    )
                    chrome(
                        "POST",
                        prefix + "/execute/sync",
                        {
                            "script": "window.__campusmarketFileInput.__campusmarketSelected = true;",
                            "args": [],
                        },
                    )
                    chrome(
                        "POST",
                        prefix + "/element/" + element + "/value",
                        {"text": str(fixture)},
                    )
                    print(
                        "Selector Web: archivo PNG real entregado por ChromeDriver.",
                        flush=True,
                    )
        except (OSError, KeyError, IndexError, ValueError, urllib.error.HTTPError):
            pass
        time.sleep(0.2)
else:
    selected = False
    ui_xml = "/data/local/tmp/campusmarket-window.xml"
    previous_controls = None
    last_anr_action = 0.0

    while time.monotonic() < deadline:
        try:
            activities = subprocess.check_output(
                ["adb", "shell", "dumpsys", "activity", "activities"],
                text=True, timeout=4,
            )
            app_resumed = any(
                "com.example.campusmarket" in line
                for line in activities.splitlines() if "ResumedActivity" in line
            )
            if app_resumed:
                selected = False
                time.sleep(0.25)
                continue
            # Pausar en CampusMarket evita activar semántica durante el test.
            # En la UI nativa conservamos el manejo de DocumentsUI y ANR del launcher.
            subprocess.run(
                ["adb", "shell", "uiautomator", "dump", "--compressed", ui_xml],
                check=True,
                capture_output=True,
                timeout=8,
            )
            xml = subprocess.check_output(
                ["adb", "shell", "cat", ui_xml],
                timeout=4,
            )
            nodes = list(ET.fromstring(xml).iter("node"))

            # El emulador de GitHub puede mostrar un ANR transitorio del Pixel Launcher
            # encima del selector. Elegir "Wait" mantiene vivo DocumentsUI y permite
            # continuar el flujo sin falsear la prueba funcional de CampusMarket.
            wait_button = next(
                (
                    node
                    for node in nodes
                    if node.get("enabled") == "true"
                    and node_label(node).strip().upper() == "WAIT"
                ),
                None,
            )
            if wait_button is not None and time.monotonic() - last_anr_action > 1.0:
                if tap_node(wait_button):
                    last_anr_action = time.monotonic()
                    print(
                        "Selector Android: ANR transitorio del launcher descartado con Wait.",
                        flush=True,
                    )
                time.sleep(0.5)
                continue

            document_nodes = [
                node
                for node in nodes
                if "documentsui" in node.get("package", "").lower()
            ]
            if not document_nodes:
                selected = False
                time.sleep(0.25)
                continue

            controls = [
                {
                    "text": node.get("text", ""),
                    "description": node.get("content-desc", ""),
                    "id": node.get("resource-id", ""),
                }
                for node in document_nodes
                if node.get("password") != "true"
                and (node.get("text") or node.get("content-desc"))
            ]
            if controls != previous_controls:
                print(
                    "Controles públicos del selector: "
                    + json.dumps(controls[-25:], ensure_ascii=False),
                    flush=True,
                )
                previous_controls = controls

            if selected:
                confirm = next(
                    (
                        node
                        for node in document_nodes
                        if node.get("enabled") == "true"
                        and node_label(node).strip().upper()
                        in {"OPEN", "SELECT", "DONE", "ABRIR", "SELECCIONAR", "LISTO"}
                    ),
                    None,
                )
                if confirm is not None and tap_node(confirm):
                    print(
                        "Selector Android: selección múltiple confirmada.",
                        flush=True,
                    )
                    time.sleep(0.5)
                    continue

                # Si DocumentsUI desaparece después de tocar el archivo, el picker
                # ya devolvió el resultado a Flutter. No hacemos taps adicionales.
                time.sleep(0.25)
                continue

            target = next(
                (
                    node
                    for node in document_nodes
                    if fixture.name.lower() in node_label(node).lower()
                ),
                None,
            )

            # En la vista "Recent images" de Android 15 el nombre del archivo puede
            # no exponerse como texto. Con un único fixture real en MediaStore,
            # seleccionamos la primera celda grande, clicable y habilitada del grid.
            if target is None:
                candidates = []
                for node in document_nodes:
                    if node.get("clickable") != "true" or node.get("enabled") != "true":
                        continue
                    bounds = node_bounds(node)
                    if not bounds:
                        continue
                    x1, y1, x2, y2 = bounds
                    width = x2 - x1
                    height = y2 - y1
                    resource_id = node.get("resource-id", "").lower()
                    label = node_label(node).lower()
                    if y1 < 250 or width < 120 or height < 120:
                        continue
                    if any(
                        token in resource_id or token in label
                        for token in (
                            "toolbar",
                            "menu",
                            "search",
                            "drawer",
                            "large files",
                            "this week",
                            "recent",
                        )
                    ):
                        continue
                    candidates.append((y1, x1, -(width * height), node))
                if candidates:
                    candidates.sort(key=lambda item: (item[0], item[1], item[2]))
                    target = candidates[0][3]
                    print(
                        "Selector Android: usando la única celda de imagen visible del fixture.",
                        flush=True,
                    )

            if target is None:
                target = next(
                    (
                        node
                        for node in document_nodes
                        if node_label(node).strip().lower()
                        in {"downloads", "descargas"}
                    ),
                    None,
                )

            if target is None:
                target = next(
                    (
                        node
                        for node in document_nodes
                        if node.get("content-desc", "")
                        in {"Show roots", "Open navigation drawer", "Navigate up"}
                    ),
                    None,
                )

            if target is not None and tap_node(target):
                label = node_label(target).lower()
                if fixture.name.lower() in label or (
                    target.get("clickable") == "true"
                    and node_bounds(target)
                    and node_bounds(target)[1] >= 250
                ):
                    selected = True
                    print(
                        "Selector Android: PNG real elegido en DocumentsUI.",
                        flush=True,
                    )
                time.sleep(0.5)
        except (subprocess.SubprocessError, ET.ParseError, ValueError):
            pass
        time.sleep(0.25)
