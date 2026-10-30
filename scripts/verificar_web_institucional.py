"""Ensayo de Web compilada: solo Docker local de un runner efimero GitHub."""

import argparse
import base64
import hashlib
import json
import os
import re
import secrets
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from scripts.ensayar_imagen_ghcr import PROBE, TrialError, require

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts/web-institucional"
BASE = "http://127.0.0.1:8000"
CRITERIA = ("config", "identity", "sql", "routes", "cors", "browser", "navigation", "resources", "export", "cleanup")


def command(parts, operation, stdin=None, timeout=60):
    result = subprocess.run(parts, input=stdin, capture_output=True, text=True, timeout=timeout, check=False)
    require(result.returncode == 0, "Fallo: " + operation + "; exit=" + str(result.returncode))
    return result.stdout


def http(path, expected=200, headers=None):
    require(path.startswith("/") and not path.startswith("//"), "Ruta HTTP invalida")
    request = urllib.request.Request(BASE + path, headers=headers or {})
    try:
        response = urllib.request.urlopen(request, timeout=30)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        require(response.status == expected, "HTTP inesperado en " + path)
        return response.read(), {key.lower(): value for key, value in response.headers.items()}


class Chrome:
    def __init__(self):
        self.prefix = ""
        capabilities = {"browserName": "chrome", "goog:chromeOptions": {"args": ["--headless=new", "--window-size=1440,1000"]},
                        "goog:loggingPrefs": {"performance": "ALL", "browser": "ALL"}}
        deadline = time.monotonic() + 30
        while True:
            try:
                session = self.call("POST", "/session", {"capabilities": {"alwaysMatch": capabilities}})
                break
            except (OSError, ValueError):
                require(time.monotonic() < deadline, "ChromeDriver no disponible")
                time.sleep(0.5)
        require(bool(re.fullmatch(r"[a-zA-Z0-9-]+", session["sessionId"])), "Sesion Chrome invalida")
        self.prefix = "/session/" + session["sessionId"]

    def call(self, method, path, payload=None):
        raw = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request("http://127.0.0.1:4444" + self.prefix + path, data=raw,
                                         headers={"Content-Type": "application/json"}, method=method)
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)["value"]

    def cdp(self, name, params=None):
        return self.call("POST", "/goog/cdp/execute", {"cmd": name, "params": params or {}})

    def nodes(self):
        # Activa semantica del Flutter real, sin sustituir su UI ni sus datos.
        self.call("POST", "/execute/sync", {"script": """
            function enable(root) {
              for (const el of root.querySelectorAll('*')) {
                if (el.tagName === 'FLT-SEMANTICS-PLACEHOLDER') el.click();
                if (el.shadowRoot) enable(el.shadowRoot);
              }
            }
            enable(document); return true;
        """, "args": []})
        return self.cdp("Accessibility.getFullAXTree")["nodes"]

    def wait_text(self, text):
        deadline = time.monotonic() + 45
        while time.monotonic() < deadline:
            for node in self.nodes():
                if not node.get("ignored") and text in node.get("name", {}).get("value", ""):
                    return node
            time.sleep(0.5)
        raise TrialError("Texto no renderizado en Chrome: " + text)

    def click_text(self, text):
        node = self.wait_text(text)
        require("backendDOMNodeId" in node, "Falta nodo DOM accesible")
        resolved = self.cdp("DOM.resolveNode", {"backendNodeId": node["backendDOMNodeId"]})
        self.cdp("Runtime.callFunctionOn", {"objectId": resolved["object"]["objectId"], "functionDeclaration": "function(){ this.click(); }"})

    def screenshot(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_bytes(base64.b64decode(self.call("GET", "/screenshot")))


class Trial:
    def __init__(self):
        require(os.getenv("GITHUB_ACTIONS") == "true" and os.getenv("RUNNER_ENVIRONMENT") == "github-hosted", "Solo runner GitHub efimero")
        require(os.getenv("GITHUB_REPOSITORY") in {"ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET", "Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET"}, "Repositorio inesperado")
        require(not os.getenv("DOCKER_HOST") and os.getenv("DOCKER_CONTEXT", "default") in {"", "default"}, "Docker remoto no permitido")
        run = os.environ["GITHUB_RUN_ID"]; attempt = os.environ["GITHUB_RUN_ATTEMPT"]
        require(run.isdigit() and attempt.isdigit(), "Run invalido")
        self.project = "campusmarket-web-" + run + "-" + attempt
        self.directory = Path(os.environ["RUNNER_TEMP"]) / self.project
        self.envfile = self.directory / "compose.env"
        self.statefile = self.directory / "state.json"
        self.source = command(["git", "rev-parse", "HEAD"], "SHA checkout").strip()
        require(self.source == os.environ["GITHUB_SHA"], "Checkout distinto al run")
        self.database = self.project.replace("-", "_") + "_test"
        self.state = json.loads(self.statefile.read_text()) if self.statefile.exists() else {
            "commit": self.source, "project": self.project,
            "run": "https://github.com/" + os.environ["GITHUB_REPOSITORY"] + "/actions/runs/" + run, "checks": {},
        }
        self.compose = ["docker", "compose", "-p", self.project, "--env-file", str(self.envfile), "-f", "deploy/compose.lab.yaml", "-f", "deploy/compose.local.yaml"]

    def save(self):
        self.directory.mkdir(mode=0o700, exist_ok=True)
        self.statefile.write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")

    def checked(self, key, result):
        self.state["checks"][key] = {"status": "CUMPLE", "result": result}
        self.save(); print("PASS " + key)

    def guard(self):
        endpoint = command(["docker", "context", "inspect", "default", "--format", "{{.Endpoints.docker.Host}}"], "daemon local").strip()
        require(endpoint == "unix:///var/run/docker.sock", "Daemon remoto rechazado")

    def inventory(self):
        label = "label=com.docker.compose.project=" + self.project
        return {"containers": command(["docker", "ps", "-aq", "--filter", label], "inventario").split(),
                "volumes": command(["docker", "volume", "ls", "-q", "--filter", label], "volumenes").split(),
                "networks": command(["docker", "network", "ls", "-q", "--filter", label], "redes").split()}

    def prepare(self):
        self.guard()
        require(not self.directory.exists() and not any(self.inventory().values()), "No se reutiliza un proyecto existente")
        self.save()
        values = {"MYSQL_ROOT_PASSWORD": secrets.token_hex(24), "MYSQL_PASSWORD": secrets.token_hex(24),
                  "MYSQL_USER": "campusmarket_web", "MYSQL_DATABASE": self.database, "CAMPUSMARKET_REVISION": self.source}
        for key in ("MYSQL_ROOT_PASSWORD", "MYSQL_PASSWORD"):
            print("::add-mask::" + values[key])
        descriptor = os.open(self.envfile, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w") as stream:
            stream.write("\n".join(key + "=" + value for key, value in values.items()) + "\n")
        cfg = json.loads(command(self.compose + ["config", "--format", "json"], "config Compose"))
        require(cfg["name"] == self.project and set(cfg["services"]) == {"api", "db"}, "Solo dos contenedores propios")
        require(cfg["services"]["db"]["image"] == "mysql:8.4", "MySQL inesperado")
        api_env = cfg["services"]["api"]["environment"]
        require(api_env["CAMPUSMARKET_DB_HOST"] == "db" and api_env["CAMPUSMARKET_DB_NAME"] == self.database, "Solo base sintetica local")
        require(set(cfg["volumes"]) == {"mysql_data", "publication_images"}, "Volumenes inesperados")
        for name, volume in cfg["volumes"].items():
            require(not volume.get("external") and not volume.get("driver_opts") and volume["name"] == self.project + "_" + name, "Solo volumenes nuevos propios")
        for service in cfg["services"].values():
            limits = service["deploy"]["resources"]["limits"]
            require(int(limits["memory"]) == 268435456 and float(limits["cpus"]) == 0.5, "Cuota distinta a 256 MiB y 0.5 CPU")
        require(cfg["services"]["api"]["ports"][0]["host_ip"] == "127.0.0.1" and not cfg["services"]["db"].get("ports"), "Puertos solo loopback de CI")
        require((ROOT / "backend/web/source-revision.txt").read_text().strip() == self.source, "Build Web sin identidad exacta")
        self.state["prepared"] = True
        self.checked("config", "2 contenedores, 256 MiB + 256 MiB, 0.5 CPU por servicio; Compose existente")

    def probe(self, mode):
        data = {"mode": mode, "source_sha": self.source, "database": self.database, "fixture": self.state.get("fixture")}
        return json.loads(command(self.compose + ["exec", "-T", "api", "python", "-c", PROBE], "probe " + mode, stdin=json.dumps(data)))

    def inspect(self, service):
        cid = command(self.compose + ["ps", "-q", service], "contenedor " + service).strip()
        require(bool(re.fullmatch(r"[a-f0-9]{12,64}", cid)), "Contenedor no unico")
        data = json.loads(command(["docker", "inspect", cid], "inspect " + service))[0]
        require(data["Config"]["Labels"]["com.docker.compose.project"] == self.project, "Proyecto inesperado")
        return data

    def start(self):
        self.guard(); require(self.state.get("prepared"), "Falta preparacion")
        command(self.compose + ["up", "-d", "--build", "--wait", "--wait-timeout", "180"], "arranque aislado", timeout=600)
        api = self.inspect("api")
        require(api["Config"]["Labels"]["org.opencontainers.image.revision"] == self.source, "OCI incorrecta")
        require(command(self.compose + ["exec", "-T", "api", "cat", "/app/REVISION"], "REVISION").strip() == self.source, "REVISION incorrecta")
        require(http("/app/source-revision.txt")[0].decode().strip() == self.source, "SHA frontend incorrecto")
        self.state["image_id"] = api["Image"]
        self.checked("identity", {"oci_revision": self.source, "frontend_revision": self.source, "image_id": api["Image"]})
        self.checked("sql", self.probe("read"))
        self.state["fixture"] = self.probe("seed"); self.save()
        html, headers = http("/app/")
        require(b'<base href="/app/">' in html and b"flutter_bootstrap.js" in html, "HTML no es el build Flutter esperado")
        require(headers.get("x-campusmarket-revision") == self.source, "Cabecera incorrecta")
        for path in ("/app/flutter_bootstrap.js", "/app/main.dart.js", "/docs", "/openapi.json", "/health"):
            http(path)
        http("/app/asset-inexistente.js", 404); http("/", 404)
        self.checked("routes", "Flutter /app/, assets reales, /health, /docs y OpenAPI; raiz API 404 preservada")
        request = urllib.request.Request(BASE + "/catalogo", method="OPTIONS", headers={"Origin": "https://campusmarket.iscoutb.dev", "Access-Control-Request-Method": "GET"})
        with urllib.request.urlopen(request, timeout=10) as response:
            require(response.headers.get("Access-Control-Allow-Origin") == "https://campusmarket.iscoutb.dev", "CORS institucional no preservado")
        self.checked("cors", "Mismo origen /app/ y /catalogo; preflight institucional autorizado")

    def run(self):
        self.guard()
        chrome = Chrome()
        try:
            chrome.call("POST", "/url", {"url": BASE + "/app/"})
            chrome.wait_text("Catálogo")
            chrome.screenshot("01-inicio.png")
            self.checked("browser", "Flutter release renderizado en Chrome real")
            chrome.click_text("Catálogo")
            chrome.wait_text("Fixture sintetico GHCR")
            chrome.screenshot("02-catalogo.png")
            chrome.click_text("Fixture sintetico GHCR")
            chrome.wait_text("Detalle de publicación")
            chrome.wait_text("Descripción")
            chrome.screenshot("03-detalle.png")
            chrome.call("POST", "/back", {})
            chrome.wait_text("Catálogo")
            chrome.call("POST", "/refresh", {})
            chrome.wait_text("Catálogo")
            network = [json.loads(item["message"])["message"] for item in chrome.call("POST", "/log", {"type": "performance"})]
            responses = [item["params"]["response"] for item in network if item["method"] == "Network.responseReceived"]
            api = [{"path": urllib.parse.urlsplit(item["url"]).path, "status": item["status"]} for item in responses if item["url"].startswith(BASE + "/catalogo")]
            require(any(item["path"] == "/catalogo" and item["status"] == 200 for item in api), "Sin catalogo HTTP real")
            require(any(item["path"] == "/catalogo/" + str(self.state["fixture"]["publication_id"]) and item["status"] == 200 for item in api), "Sin detalle HTTP real")
            require(not any(item["status"] >= 400 for item in responses if item["url"].startswith(BASE + "/app/")), "Fallo de recurso Web")
            self.checked("navigation", {"inicio_catalogo_detalle_reload": True, "api_responses": api})
        finally:
            chrome.screenshot("04-ultimo-estado.png")
            chrome.call("DELETE", "")
        resources = {}
        for service, volume, destination in (("api", "publication_images", "/app/backend/uploads"), ("db", "mysql_data", "/var/lib/mysql")):
            data = self.inspect(service)
            require(data["HostConfig"]["Memory"] == 268435456 and data["HostConfig"]["NanoCpus"] == 500000000, "Limites efectivos distintos")
            require(data["State"]["Health"]["Status"] == "healthy" and not data["State"]["OOMKilled"] and data["RestartCount"] == 0, "Health/OOM/reinicio inesperado")
            require(any(m.get("Name") == self.project + "_" + volume and m["Destination"] == destination and m["RW"] for m in data["Mounts"]), "Montaje inesperado")
            peak = int(command(["docker", "exec", data["Id"], "cat", "/sys/fs/cgroup/memory.peak"], "pico memoria " + service).strip())
            require(0 < peak <= 268435456, "Pico fuera del limite")
            resources[service] = {"peak_bytes": peak, "limit_bytes": data["HostConfig"]["Memory"], "nano_cpus": data["HostConfig"]["NanoCpus"], "oom_killed": False}
        self.checked("resources", resources)

    def export(self):
        self.guard()
        require(all(self.state["checks"].get(key, {}).get("status") == "CUMPLE" for key in CRITERIA if key not in {"export", "cleanup"}), "Imagen no aprobada por todas las pruebas")
        OUT.mkdir(parents=True, exist_ok=True)
        archive = OUT / "api-web.tar"
        command(["docker", "save", self.state["image_id"], "-o", str(archive)], "exportar imagen", timeout=120)
        with archive.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        (OUT / "api-web.tar.sha256").write_text(digest + "  api-web.tar\n")
        self.checked("export", {"image_id": self.state["image_id"], "archive_sha256": digest, "published": False})

    def cleanup(self):
        self.guard()
        try:
            if self.state.get("prepared"):
                command(self.compose + ["down", "--volumes", "--remove-orphans"], "cleanup propio", timeout=120)
            remaining = self.inventory()
            require(not any(remaining.values()), "Quedan recursos del ensayo")
        finally:
            self.envfile.unlink(missing_ok=True)
        self.checked("cleanup", {**remaining, "credentials_removed": not self.envfile.exists()})

    def report(self):
        OUT.mkdir(parents=True, exist_ok=True)
        self.state["passed"] = not self.state.get("failure") and all(self.state["checks"].get(key, {}).get("status") == "CUMPLE" for key in CRITERIA)
        (OUT / "resultado.json").write_text(json.dumps(self.state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        text = "## Web institucional: ensayo aislado\n\nCommit: `" + self.source + "`\n\nRun: " + self.state["run"] + "\n\n"
        text += "| Criterio | Estado | Resultado |\n|---|---|---|\n"
        for key in CRITERIA:
            check = self.state["checks"].get(key, {"status": "BLOQUEADO", "result": "Sin verificacion real"})
            text += "| " + key + " | " + check["status"] + " | " + json.dumps(check["result"], ensure_ascii=False).replace("|", "/") + " |\n"
        text += "\nPublicacion institucional: BLOQUEADO, no se modifica Dokploy.\n"
        (OUT / "resultado.md").write_text(text, encoding="utf-8")
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as stream:
            stream.write(text)
        require(self.state["passed"], "Ensayo incompleto; revisar resultado")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("prepare", "start", "run", "export", "cleanup", "report"))
    phase = parser.parse_args().phase
    trial = Trial()
    try:
        getattr(trial, phase)()
    except (TrialError, OSError, ValueError, LookupError, TypeError, subprocess.SubprocessError) as error:
        message = str(error) if isinstance(error, TrialError) else type(error).__name__
        trial.state.setdefault("failure", phase + ": " + message)
        trial.save(); print("FAIL " + trial.state["failure"])
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
