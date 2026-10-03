"""Prueba HTTP/MySQL y cgroups de un Compose efímero; nunca producción."""
import argparse
import hashlib
import json
import os
import re
import secrets
import subprocess
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8000"
parser = argparse.ArgumentParser()
parser.add_argument("--env-file", required=True)
parser.add_argument("--project", required=True)
parser.add_argument("--revision", required=True)
args = parser.parse_args()
if not os.getenv("GITHUB_ACTIONS") or not re.fullmatch(r"campusmarket-ci-[0-9]+", args.project):
    raise SystemExit("Solo se permite el proyecto efímero del runner de CI.")
if not re.fullmatch(r"[0-9a-f]{40}", args.revision):
    raise SystemExit("Se requiere el SHA completo.")
COMPOSE = [
    "docker", "compose", "--project-name", args.project, "--env-file", args.env_file,
    "-f", str(ROOT / "deploy/compose.lab.yaml"),
    "-f", str(ROOT / "deploy/compose.local.yaml"),
]
OUT = ROOT / "artifacts/compose"
OUT.mkdir(parents=True, exist_ok=True)
evidence = {"hash": args.revision, "checks": [], "resource_snapshots": []}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def command(parts, stdin=None):
    result = subprocess.run(parts, input=stdin, text=True, capture_output=True, check=False)
    if result.returncode:
        # No incluir stdout/stderr: config/inspect pueden contener Environment.
        raise RuntimeError(f"Falló comando de infraestructura (exit {result.returncode}).")
    return result.stdout


def request(method, path, token=None, payload=None, body=None, content_type=None):
    headers = {}
    if token:
        headers["Authorization"] = "Bearer " + token
    if payload is not None:
        body = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    elif content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method=method)
    try:
        response = urllib.request.urlopen(req, timeout=60)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        data = response.read()
        value = json.loads(data) if data and "application/json" in response.headers.get("Content-Type", "") else data
        return response.status, value, response.headers


def expect(method, path, status, **options):
    actual, value, headers = request(method, path, **options)
    require(actual == status, f"{method} {path}: esperado {status}, observado {actual}")
    return value, headers


def wait_health():
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        try:
            status, value, headers = request("GET", "/health")
            if status == 200 and value.get("status") == "ok":
                require(headers.get("X-CampusMarket-Revision") == args.revision, "Health no identifica el hash construido.")
                return
        except (urllib.error.URLError, TimeoutError):
            pass
        time.sleep(0.5)
    raise RuntimeError("Health no estuvo disponible en el plazo.")


def register(label):
    credentials = {
        "correo": secrets.token_hex(12) + "@compose.test",
        "password": secrets.token_urlsafe(24),
    }
    user, _ = expect("POST", "/usuarios/registro", 201, payload={"nombre": label, **credentials})
    session, _ = expect("POST", "/usuarios/login", 200, payload=credentials)
    require(session["usuario"]["id"] == user["id"], "Login no corresponde al usuario registrado.")
    return {"id": user["id"], "token": session["access_token"], "es_admin": user["es_admin"]}


def png(width=32, height=24):
    stream = BytesIO()
    Image.new("RGB", (width, height), "#7257ec").save(stream, format="PNG")
    return stream.getvalue()


def multipart(content):
    boundary = "CampusMarket" + secrets.token_hex(12)
    body = (
        ("--" + boundary + "\r\nContent-Disposition: form-data; name=\"archivo\"; filename=\"camara.png\"\r\n"
         "Content-Type: image/png\r\n\r\n").encode()
        + content + ("\r\n--" + boundary + "--\r\n").encode()
    )
    return {"body": body, "content_type": "multipart/form-data; boundary=" + boundary}


def snapshot(label):
    result = {}
    for service in ("api", "db"):
        cid = command(COMPOSE + ["ps", "-q", service]).strip()
        require(bool(cid), f"Falta contenedor {service}.")
        # Selectores: nunca publicar docker inspect completo con variables.
        data = json.loads(command(["docker", "inspect", "--format",
            '{"memory":{{.HostConfig.Memory}},"nano_cpus":{{.HostConfig.NanoCpus}},"oom":{{.State.OOMKilled}},"restarts":{{.RestartCount}},"image":{{json .Image}},"revision":{{json (index .Config.Labels "org.opencontainers.image.revision")}}}', cid]))
        peak = int(command(["docker", "exec", cid, "cat", "/sys/fs/cgroup/memory.peak"]).strip())
        require(data["memory"] == 256 * 1024 * 1024, f"Memoria efectiva incorrecta: {service}.")
        require(data["nano_cpus"] == 500_000_000, f"CPU efectiva incorrecta: {service}.")
        require(not data["oom"] and data["restarts"] == 0, f"OOM/reinicio inesperado: {service}.")
        require(peak <= data["memory"], f"Peak supera cuota: {service}.")
        data["peak_bytes"] = peak
        if service == "api":
            require(data["revision"] == args.revision, "Etiqueta OCI distinta del hash.")
            require(command(["docker", "exec", cid, "cat", "/app/REVISION"]).strip() == args.revision, "REVISION distinta.")
            uid = command(["docker", "exec", cid, "id", "-u"]).strip()
            require(uid == "10001", "API debe ejecutarse sin root.")
            data["uid"] = uid
        result[service] = data
    require(sum(item["memory"] for item in result.values()) <= 512 * 1024 * 1024, "Cuota total supera 512 MiB.")
    evidence["resource_snapshots"].append({"phase": label, "containers": result})


def add_check(name):
    evidence["checks"].append({"requirement": name, "passed": True})


def verify():
    config = json.loads(command(COMPOSE + ["config", "--format", "json"]))
    require(set(config["services"]) == {"api", "db"}, "El monolito requiere API y MySQL.")
    require(config["services"]["db"]["environment"]["MYSQL_DATABASE"].endswith("_test"), "Requiere base efímera _test.")
    lab = json.loads(command(COMPOSE[:-2] + ["config", "--format", "json"]))
    for service in lab["services"].values():
        require(not service.get("ports"), "Compose del laboratorio no puede publicar puertos.")
        require(not service.get("privileged") and not service.get("container_name"), "Configuración privilegiada no permitida.")
        require(all(v["type"] == "volume" for v in service.get("volumes", [])), "Solo volúmenes con nombre.")
    wait_health()
    snapshot("startup")
    a, b, moderator = register("Usuario A"), register("Usuario B"), register("Moderador")
    require(moderator["id"] == 3 and moderator["es_admin"], "Capability de prueba no corresponde al ID configurado.")
    require(not a["es_admin"] and not b["es_admin"], "Registro ordinario adquirió moderación.")
    add_check("usuarios-registro-login-capability")

    publication = {
        "titulo": "Calculadora para ingeniería", "descripcion": "Publicación de prueba real en Compose.",
        "precio": 65000.5, "modalidad": "venta", "estado": "usado",
    }
    created, _ = expect("POST", "/publicaciones", 201, token=a["token"], payload=publication)
    pid = created["id"]
    require(created["propietario_id"] == a["id"], "Propiedad real incorrecta.")
    first, _ = expect("POST", f"/publicaciones/{pid}/imagenes", 201, token=a["token"], **multipart(png()))
    second, _ = expect("POST", f"/publicaciones/{pid}/imagenes", 201, token=a["token"], **multipart(png(40, 30)))
    third, _ = expect("POST", f"/publicaciones/{pid}/imagenes", 201, token=a["token"], **multipart(png(50, 40)))
    expect("POST", f"/publicaciones/{pid}/imagenes", 400, token=a["token"], **multipart(png()))
    principal, _ = expect("PUT", f"/publicaciones/{pid}/imagenes/{third['id']}/principal", 200, token=a["token"])
    require(next(x for x in principal if x["es_principal"])["id"] == third["id"], "Principal incorrecta.")
    expect("DELETE", f"/publicaciones/{pid}/imagenes/{second['id']}", 204, token=a["token"])
    expect("GET", second["imagen_url"], 404)
    updated = {**publication, "titulo": "Calculadora editada", "precio": 70000}
    expect("PUT", f"/publicaciones/{pid}", 200, token=a["token"], payload=updated)
    expect("PATCH", f"/publicaciones/{pid}/estado", 200, token=a["token"], payload={"estado_publicacion": "reservado"})
    own, private_headers = expect("GET", "/publicaciones/mias", 200, token=a["token"])
    require(len(own) == 1 and own[0]["id"] == pid, "Listado propio incorrecto.")
    require(private_headers.get("Cache-Control") == "no-store", "Respuesta privada permite caché.")
    stable, _ = expect("GET", f"/catalogo/{pid}", 200)
    add_check("publicaciones-galeria-edicion-estado")

    attacks = [
        ("PUT", f"/publicaciones/{pid}", {"payload": publication}),
        ("DELETE", f"/publicaciones/{pid}", {}),
        ("PATCH", f"/publicaciones/{pid}/estado", {"payload": {"estado_publicacion": "vendido"}}),
        ("PUT", f"/publicaciones/{pid}/imagenes/{first['id']}/principal", {}),
        ("DELETE", f"/publicaciones/{pid}/imagenes/{first['id']}", {}),
        ("POST", f"/publicaciones/{pid}/imagenes", multipart(png())),
        ("PUT", f"/publicaciones/{pid}?propietario_id={a['id']}", {"payload": publication}),
        ("DELETE", f"/publicaciones/{pid}?propietario_id={a['id']}", {}),
        ("PATCH", f"/publicaciones/{pid}/estado?propietario_id={a['id']}", {"payload": {"estado_publicacion": "vendido"}}),
        ("DELETE", f"/publicaciones/{pid}/imagenes/{third['id']}?propietario_id={a['id']}", {}),
    ]
    for method, path, options in attacks:
        expect(method, path, 404, token=b["token"], **options)
        current, _ = expect("GET", f"/catalogo/{pid}", 200)
        require(current == stable, "EC-02 alteró datos del propietario.")
    empty, _ = expect("GET", "/publicaciones/mias", 200, token=b["token"])
    require(empty == [], "Usuario B obtuvo publicaciones de A.")
    expect("GET", "/administracion/reportes", 403, token=b["token"])
    evidence["ec02"] = {"attempts": len(attacks), "rejected": len(attacks), "data_unchanged": True}
    add_check("EC-02-diez-intentos-y-datos-intactos")

    moderation_pub, _ = expect("POST", "/publicaciones", 201, token=a["token"], payload={**publication, "titulo": "Publicación reportable"})
    report, _ = expect("POST", "/administracion/reportes", 201, token=b["token"],
        payload={"publicacion_id": moderation_pub["id"], "motivo": "Contenido que requiere una revisión real."})
    queue, _ = expect("GET", "/administracion/reportes", 200, token=moderator["token"])
    require(any(x["id"] == report["id"] for x in queue), "Reporte no llegó a moderación.")
    expect("PATCH", f"/administracion/reportes/{report['id']}", 200, token=moderator["token"],
        payload={"decision": "ocultado", "nota": "Revisión de la publicación completada."})
    expect("GET", f"/catalogo/{moderation_pub['id']}", 404)
    add_check("administracion-reportar-y-ocultar")

    # Simultaneidad real: dos hashes y foto de cámara, admitidos en la API acotada.
    camera, _ = expect("POST", "/publicaciones", 201, token=a["token"], payload={**publication, "titulo": "Foto de cámara"})
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [
            pool.submit(register, "Carga concurrente uno"),
            pool.submit(register, "Carga concurrente dos"),
            pool.submit(expect, "POST", f"/publicaciones/{camera['id']}/imagenes", 201,
                token=a["token"], **multipart(png(4000, 3000))),
        ]
        results = [future.result() for future in futures]
    large_image = results[2][0]
    normalized, _ = expect("GET", large_image["imagen_url"], 200)
    with Image.open(BytesIO(normalized)) as photo:
        require(photo.size == (2048, 1536), "Cámara no se normalizó a 2048.")
    add_check("recursos-hashes-concurrentes-y-camara-12MP")
    snapshot("after-concurrent-work")

    # Solo fixture de rendimiento en MySQL efímero; no SQL añadido al catálogo.
    fixture = """
import os
from backend.app.db import transaction
assert os.environ["CAMPUSMARKET_DB_NAME"].endswith("_test")
with transaction() as cursor:
    cursor.executemany(
        "INSERT INTO publicaciones (titulo, descripcion, precio, modalidad, estado, propietario_id) VALUES (%s, %s, %s, 'venta', 'usado', %s)",
        [("Rendimiento " + str(i), "Fixture de medición MySQL real", 1000 + i, OWNER) for i in range(1000)]
    )
""".replace("OWNER", str(a["id"]))
    command(COMPOSE + ["exec", "-T", "api", "python", "-"], stdin=fixture)
    samples = []
    for index in range(10):
        start = time.perf_counter()
        status, rows, _ = request("GET", "/catalogo?texto=Rendimiento&modalidad=venta&estado=usado&precio_min=1000&precio_max=1999")
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        require(status == 200 and len(rows) == 1000, "Medición no leyó 1000 filas reales.")
        samples.append(duration_ms)
    evidence["ec01"] = {
        "scope": "HTTP loopback + MySQL real, 1000 filas, cuota 512 MiB",
        "samples_ms": samples, "within_2000ms": sum(x <= 2000 for x in samples),
        "required": 9, "public_network_verified": False,
    }
    snapshot("after-catalog-measurement")

    before_image, _ = expect("GET", first["imagen_url"], 200)
    before_digest = hashlib.sha256(before_image).hexdigest()
    restart_start = time.perf_counter()
    command(COMPOSE + ["up", "-d", "--force-recreate", "--wait", "--wait-timeout", "180"])
    wait_health()
    evidence["recreation_ms"] = round((time.perf_counter() - restart_start) * 1000, 2)
    me, _ = expect("GET", "/usuarios/me", 200, token=a["token"])
    require(me["id"] == a["id"], "Sesión no persistió al recrear API y MySQL.")
    restored, _ = expect("GET", f"/catalogo/{pid}", 200)
    require(restored == stable, "Publicación/galería no persistieron.")
    after_image, _ = expect("GET", first["imagen_url"], 200)
    require(hashlib.sha256(after_image).hexdigest() == before_digest, "Archivo no persistió.")
    snapshot("after-recreation")
    add_check("persistencia-sesiones-publicaciones-y-fotos")

    expect("DELETE", f"/publicaciones/{pid}", 204, token=a["token"])
    expect("GET", f"/catalogo/{pid}", 404)
    expect("GET", first["imagen_url"], 404)
    expect("GET", third["imagen_url"], 404)
    expect("POST", "/usuarios/logout", 204, token=a["token"])
    expect("GET", "/usuarios/me", 401, token=a["token"])
    expect("POST", "/usuarios/logout", 204, token=b["token"])
    expect("GET", "/usuarios/me", 401, token=b["token"])
    add_check("eliminar-y-logout-revocado")
    require(evidence["ec01"]["within_2000ms"] >= 9, "EC-01 no alcanzó 9/10 en 2 s bajo cuota.")
    add_check("EC-01-medicion-HTTP-MySQL-bajo-cuota")
    evidence["passed"] = True


try:
    verify()
except Exception as failure:
    evidence["passed"] = False
    # Solo mensaje diseñado arriba; excepciones de red no incluyen payload/token.
    evidence["failure_type"] = type(failure).__name__
    if isinstance(failure, (AssertionError, RuntimeError)):
        evidence["failure"] = str(failure)
    raise
finally:
    output = json.dumps(evidence, ensure_ascii=False, indent=2)
    (OUT / "resultado.json").write_text(output, encoding="utf-8")
    print("CAMPUSMARKET_COMPOSE_RESULT=" + json.dumps(evidence, ensure_ascii=False))
