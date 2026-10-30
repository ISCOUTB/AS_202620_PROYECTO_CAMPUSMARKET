"""Promueve exclusivamente la imagen Web del run auditado; nunca construye ni despliega."""

import argparse
import hashlib
import json
import os
import re
import subprocess
import tarfile
import tempfile
import zipfile
from pathlib import Path

from scripts.ensayar_imagen_ghcr import classify_pull_error

REPOSITORY = "Nnigarp/AS_202620_PROYECTO_CAMPUSMARKET"
BRANCH = "feat/web-institucional-20261030-40be256"
SOURCE = "a9b6709a67f8036346acb64b9c2b9849ee355cf2"
RUN = 41094945507
ARTIFACT = 12996575905
ZIP_SHA = "e51664f3e6a6833b541f9143e5ea18d607f6f8b93f258fd409e7be3f99796113"
TAR_SHA = "8edab5dca0c28063970c0183e8b8df458df302d7721c07a972203648cb3dc940"
IMAGE_ID = "sha256:15a6fee324bc315d27ab85674781dfd1bded727243cb6ff752370e70b5d6fd19"
IMAGE = "ghcr.io/nnigarp/campusmarket-web-candidate"
PUBLISH_MESSAGE = "ci: publicar solo candidato Web a9b6709 verificado sin desplegar"
CRITERIA = {"config", "identity", "sql", "routes", "cors", "browser", "navigation", "resources", "export", "cleanup"}
OUT = Path("artifacts/publicacion-web")


class VerificationError(Exception):
    pass


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def command(args, stdin=None, timeout=180):
    result = subprocess.run(args, input=stdin, capture_output=True, timeout=timeout, check=False)
    # Nunca imprimir stdout/stderr de herramientas autenticadas.
    if result.returncode:
        category = classify_pull_error(result.stderr.decode(errors="replace"))
        raise VerificationError(f"Operacion {args[0]} rechazada: exit={result.returncode}; category={category}")
    return result.stdout


def api(path):
    return json.loads(command(["gh", "api", f"repos/{REPOSITORY}/{path}"]))


def verify_provenance(run, artifact):
    require(run["id"] == RUN and run["head_sha"] == SOURCE, "Run o fuente distintos")
    require(run["repository"]["full_name"] == REPOSITORY and run["head_repository"]["full_name"] == REPOSITORY, "Repositorio distinto")
    require(run["event"] == "push" and run["head_branch"] == BRANCH, "Evento o rama distintos")
    require(run["path"] == ".github/workflows/web-institucional.yml" and run["status"] == "completed" and run["conclusion"] == "success", "Workflow no aprobado")
    require(artifact["id"] == ARTIFACT and not artifact["expired"], "Artefacto ausente o caducado")
    require(artifact["name"] == f"web-institucional-{SOURCE}-1" and artifact["digest"] == "sha256:" + ZIP_SHA, "Identidad ZIP distinta")
    require(artifact["workflow_run"]["id"] == RUN and artifact["workflow_run"]["head_sha"] == SOURCE, "Artefacto de otro run")


def verify_archive(path, destination):
    require(sha256(path) == ZIP_SHA, "ZIP modificado")
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) and {"api-web.tar", "resultado.json", "api-web.tar.sha256"} <= set(names), "ZIP ambiguo o incompleto")
        # No extraer rutas arbitrarias del ZIP.
        for name in ("api-web.tar", "resultado.json", "api-web.tar.sha256"):
            with archive.open(name) as src, (destination / name).open("wb") as dst:
                while chunk := src.read(1024 * 1024):
                    dst.write(chunk)
    require(sha256(destination / "api-web.tar") == TAR_SHA, "TAR modificado")
    require((destination / "api-web.tar.sha256").read_text().strip() == TAR_SHA + "  api-web.tar", "Checksum interno distinto")
    evidence = json.loads((destination / "resultado.json").read_text())
    verify_evidence(evidence)
    with tarfile.open(destination / "api-web.tar") as archive:
        manifest = json.load(archive.extractfile("manifest.json"))
        require(len(manifest) == 1, "TAR con varias imagenes")
        config = archive.extractfile(manifest[0]["Config"]).read()
        require("sha256:" + hashlib.sha256(config).hexdigest() == IMAGE_ID, "Image ID distinto")
        config = json.loads(config)
        require(config["architecture"] == "amd64" and config["os"] == "linux", "Plataforma distinta")
        require(config["config"]["Labels"]["org.opencontainers.image.revision"] == SOURCE, "OCI distinto")
    return evidence


def verify_evidence(data):
    require(data["commit"] == SOURCE and data["run"] == f"https://github.com/{REPOSITORY}/actions/runs/{RUN}", "Evidencia de otra fuente")
    require(data["passed"] is True and not data.get("failure") and set(data["checks"]) == CRITERIA, "Ensayo incompleto")
    require(all(item["status"] == "CUMPLE" for item in data["checks"].values()), "Criterio sin aprobar")
    require(data["image_id"] == IMAGE_ID and data["checks"]["export"]["result"]["image_id"] == IMAGE_ID, "Identidad de evidencia distinta")
    require(data["checks"]["export"]["result"]["archive_sha256"] == TAR_SHA, "TAR no acreditado")
    require(data["checks"]["cleanup"]["result"]["containers"] == [] and data["checks"]["cleanup"]["result"]["volumes"] == [] and data["checks"]["cleanup"]["result"]["networks"] == [], "Cleanup incompleto")


def inspect_identity(reference):
    data = json.loads(command(["docker", "image", "inspect", reference]))[0]
    require(data["Id"] == IMAGE_ID and data["Architecture"] == "amd64" and data["Os"] == "linux", "Imagen cargada/remota distinta")
    require(data["Config"]["Labels"]["org.opencontainers.image.revision"] == SOURCE, "Revision OCI distinta")
    for path in ("/app/REVISION", "/app/backend/web/source-revision.txt"):
        raw = command(["docker", "run", "--rm", "--pull=never", "--network=none", "--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges", "--memory=64m", "--cpus=0.5", "--entrypoint=cat", reference, path])
        require(raw.decode().strip() == SOURCE, "REVISION API/Web distinta")


def authorize_publication(env, event):
    require(env.get("GITHUB_REPOSITORY") == REPOSITORY and env.get("GITHUB_REF") == "refs/heads/" + BRANCH, "Publicacion solo desde rama del fork autorizada")
    if env.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
        return
    require(env.get("GITHUB_EVENT_NAME") == "push" and event.get("head_commit", {}).get("message") == PUBLISH_MESSAGE
            and event.get("after") == env.get("GITHUB_SHA") and event.get("repository", {}).get("full_name") == REPOSITORY,
            "Push sin orden puntual de publicacion")


def publish(token):
    require(bool(token), "Token efimero ausente")
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text()) if os.environ.get("GITHUB_EVENT_NAME") == "push" else {}
    authorize_publication(os.environ, event)
    with tempfile.TemporaryDirectory(prefix="cm-ghcr-auth-") as auth:
        previous = os.environ.get("DOCKER_CONFIG")
        os.environ["DOCKER_CONFIG"] = auth
        try:
            command(["docker", "login", "ghcr.io", "--username", os.environ["GITHUB_ACTOR"], "--password-stdin"], stdin=token.encode())
            tag = IMAGE + ":web-" + SOURCE
            command(["docker", "tag", IMAGE_ID, tag])
            output = command(["docker", "push", tag], timeout=600).decode()
            matches = re.findall(r"digest: (sha256:[0-9a-f]{64})", output)
            require(len(matches) == 1, "Digest de push no unico")
            reference = IMAGE + "@" + matches[0]
            manifest = json.loads(command(["docker", "buildx", "imagetools", "inspect", "--raw", reference]))
            require(manifest["config"]["digest"] == IMAGE_ID, "Manifest GHCR contiene otra imagen")
            command(["docker", "pull", "--platform=linux/amd64", reference], timeout=600)
            inspect_identity(reference)
            return reference
        finally:
            if previous is None:
                os.environ.pop("DOCKER_CONFIG", None)
            else:
                os.environ["DOCKER_CONFIG"] = previous


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--archive", type=Path, help="Copia conservada del ZIP original; valida hashes fijados en codigo aun despues de caducar Actions")
    args = parser.parse_args()
    record = {"source_sha": SOURCE, "source_repository": REPOSITORY, "source_run": RUN, "artifact_id": ARTIFACT,
              "zip_sha256": ZIP_SHA, "archive_sha256": TAR_SHA, "image_id": IMAGE_ID,
              "publisher_sha": os.getenv("GITHUB_SHA"), "publisher_run_id": os.getenv("GITHUB_RUN_ID"),
              "publication_attempted": False, "published": False}
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        require(os.getenv("GITHUB_ACTIONS") == "true" and os.getenv("RUNNER_ENVIRONMENT") == "github-hosted", "Solo runner GitHub efimero")
        require(not os.getenv("DOCKER_HOST") and os.getenv("DOCKER_CONTEXT", "default") in {"", "default"}, "Docker remoto no permitido")
        require(command(["docker", "context", "inspect", "default", "--format", "{{.Endpoints.docker.Host}}"]).decode().strip() == "unix:///var/run/docker.sock", "Daemon no local")
        if args.archive:
            # Los hashes fijados y revisados autentican la copia completa; no
            # consultar un endpoint que puede desaparecer al caducar Actions.
            record["provenance"] = "Copia original autenticada por ZIP/TAR/Image ID fijados en codigo"
        else:
            verify_provenance(api(f"actions/runs/{RUN}"), api(f"actions/artifacts/{ARTIFACT}"))
            record["provenance"] = "Metadatos GitHub vigentes y hashes fijados en codigo"
        with tempfile.TemporaryDirectory(prefix="cm-web-original-") as temp:
            directory = Path(temp)
            path = args.archive or directory / "artifact.zip"
            if not args.archive:
                path.write_bytes(command(["gh", "api", f"repos/{REPOSITORY}/actions/artifacts/{ARTIFACT}/zip"], timeout=300))
            verify_archive(path, directory)
            command(["docker", "load", "-i", str(directory / "api-web.tar")])
            inspect_identity(IMAGE_ID)
            record["integrity_verified"] = True
            if args.publish:
                record["publication_attempted"] = True
                record["ghcr_reference"] = publish(os.environ.get("GH_TOKEN"))
                record["published"] = True
        record["passed"] = True
    except (VerificationError, OSError, ValueError, KeyError, TypeError, tarfile.TarError, zipfile.BadZipFile, subprocess.SubprocessError) as error:
        record["passed"] = False
        record["failure"] = str(error) if isinstance(error, VerificationError) else type(error).__name__
    (OUT / "resultado.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    summary = "## Imagen Web original\n\n```json\n" + json.dumps(record, indent=2) + "\n```\n\nNo despliega ni acredita acceso desde Dokploy.\n"
    if os.getenv("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as stream:
            stream.write(summary)
    print(summary)
    return 0 if record["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
