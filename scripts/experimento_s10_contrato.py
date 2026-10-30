"""S10-CT-01: medir un consumidor incompatible contra una API desplegada.

Solo hace GET públicos. No necesita sesiones, secretos ni acceso a MySQL.
La métrica es del observador HTTP, no de la ventana EC-01 del servidor.
"""

import argparse
import hashlib
import json
import math
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen
from uuid import uuid4

SCENARIO_ID = "S10-CT-01"
LATENCY_BUDGET_MS = 10000


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def canonical_hash(value):
    content = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def adapt_sale_filter(value):
    """Adaptador explícito del consumidor de prueba; no modifica la API."""
    return {"sale": "venta"}.get(value, value)


def source_revision():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def observe(base_url, path, phase, repeat, sample, output):
    request_id = str(uuid4())
    request = Request(base_url + path, headers={
        "Accept": "application/json", "X-Request-ID": request_id,
        "Cache-Control": "no-cache", "Pragma": "no-cache",
        "User-Agent": "CampusMarket-S10-CT-01/1.0",
    })
    began = utc_now()
    clock = time.perf_counter()
    status, headers, body, error = None, {}, b"", None
    try:
        with urlopen(request, timeout=15) as response:
            status, headers, body = response.status, response.headers, response.read()
    except HTTPError as response:
        status, headers, body = response.code, response.headers, response.read()
    except (URLError, OSError, TimeoutError) as exc:
        error = type(exc).__name__
    elapsed = round((time.perf_counter() - clock) * 1000, 3)
    try:
        payload = json.loads(body)
    except (ValueError, UnicodeError):
        payload = None
    row = {
        "timestamp": began, "scenario_id": SCENARIO_ID,
        "phase": phase, "repeat": repeat, "sample": sample,
        "method": "GET", "path": path, "status_code": status,
        "duration_ms": elapsed, "request_id": request_id,
        "response_request_id": headers.get("X-Request-ID"),
        "correlated": headers.get("X-Request-ID") == request_id,
        "runtime_revision": headers.get("X-CampusMarket-Revision"),
        "content_type": headers.get("Content-Type"),
        "response_bytes": len(body), "response_sha256": canonical_hash(payload),
        "payload_is_list": isinstance(payload, list),
        "item_count": len(payload) if isinstance(payload, list) else None,
        "error": error,
    }
    if isinstance(payload, dict) and isinstance(payload.get("detail"), list):
        row["validation_errors"] = [
            {"loc": item.get("loc"), "type": item.get("type")}
            for item in payload["detail"] if isinstance(item, dict)
        ]
    if path == "/health" and isinstance(payload, dict):
        row["health_status"] = payload.get("status")
    with output.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps(row, ensure_ascii=False), flush=True)
    return row, payload


def phase_metric(rows, expected_status):
    durations = sorted(row["duration_ms"] for row in rows)
    success = sum(row["status_code"] == expected_status for row in rows)
    return {
        "requests": len(rows), "expected_status": expected_status,
        "matching_status": success, "matching_status_ratio": success / len(rows),
        "p95_ms": durations[math.ceil(len(durations) * .95) - 1],
        "max_ms": max(durations), "network_errors": sum(row["error"] is not None for row in rows),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="https://campusmarket.iscoutb.dev")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--expected-revision", required=True)
    parser.add_argument(
        "--reference-contract",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "contracts/openapi-v2.json",
    )
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--samples", type=int, default=5)
    args = parser.parse_args()
    parsed = urlparse(args.base_url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.query or parsed.fragment:
        parser.error("--base-url requiere un origen HTTPS sin query ni fragmento")
    if not 1 <= args.repeats <= 3 or not 1 <= args.samples <= 10:
        parser.error("Carga acotada: 1..3 repeticiones y 1..10 muestras por fase")
    if args.output.exists():
        parser.error("El directorio ya existe: usar otro para conservar las corridas previas")
    args.output.mkdir(parents=True)
    log_path = args.output / "observaciones.jsonl"
    plan = {
        "scenario_id": SCENARIO_ID, "declared_at": utc_now(),
        "base_url": args.base_url.rstrip("/"), "source_revision": source_revision(),
        "expected_runtime_revision": args.expected_revision,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "repeats": args.repeats, "samples_per_phase_per_repeat": args.samples,
        "independent_variable": "modalidad: venta -> sale -> venta por adaptador del consumidor",
        "thresholds": {"matching_status_ratio": 1.0, "correlation_ratio": 1.0,
                       "p95_ms_per_phase": LATENCY_BUDGET_MS, "health_status": "ok"},
        "load": "Un consumidor, peticiones seriales, sin reintentos ni esperas artificiales",
        "expected_statuses": {"baseline": 200, "incompatible": 422, "adapted": 200},
        "scope": "HTTP público observado; sin medición de CPU, memoria, SQL o navegador",
    }
    (args.output / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    all_rows, phases, health_rows, contracts = [], {name: [] for name in plan["expected_statuses"]}, [], []
    versioned = json.loads(args.reference_contract.read_text(encoding="utf-8"))
    for moment in ("before",):
        row, payload = observe(plan["base_url"], "/openapi.json", "contract_" + moment, 0, 0, log_path)
        all_rows.append(row)
        contracts.append(row["status_code"] == 200 and payload == versioned)
    full_before, _ = observe(plan["base_url"], "/catalogo", "catalog_before", 0, 0, log_path)
    all_rows.append(full_before)
    for repeat in range(1, args.repeats + 1):
        for phase, value in (("baseline", "venta"), ("incompatible", "sale"), ("adapted", adapt_sale_filter("sale"))):
            for sample in range(1, args.samples + 1):
                row, _ = observe(plan["base_url"], "/catalogo?" + urlencode({"modalidad": value}), phase, repeat, sample, log_path)
                phases[phase].append(row)
                all_rows.append(row)
            row, _ = observe(plan["base_url"], "/health", "health_after_" + phase, repeat, 0, log_path)
            all_rows.append(row)
            health_rows.append(row)
    full_after, _ = observe(plan["base_url"], "/catalogo", "catalog_after", 0, 0, log_path)
    all_rows.append(full_after)
    row, payload = observe(plan["base_url"], "/openapi.json", "contract_after", 0, 0, log_path)
    all_rows.append(row)
    contracts.append(row["status_code"] == 200 and payload == versioned)
    metrics = {name: phase_metric(rows, plan["expected_statuses"][name]) for name, rows in phases.items()}
    checks = {
        "phase_statuses": all(metric["matching_status_ratio"] == 1.0 for metric in metrics.values()),
        "phase_p95_within_budget": all(metric["p95_ms"] <= LATENCY_BUDGET_MS for metric in metrics.values()),
        "healthy_dependency": all(row["status_code"] == 200 and row.get("health_status") == "ok" for row in health_rows),
        "correlated_requests": all(row["correlated"] for row in all_rows),
        "single_expected_runtime_revision": all(row["runtime_revision"] == args.expected_revision for row in all_rows),
        "public_contract_equals_versioned_before_after": all(contracts),
        "valid_catalog_payloads": all(row["payload_is_list"] for name in ("baseline", "adapted") for row in phases[name]),
        "rejection_identifies_query_modalidad": all(
            any(item["loc"] == ["query", "modalidad"] and item["type"] == "literal_error" for item in row.get("validation_errors", []))
            for row in phases["incompatible"]
        ),
        "catalog_snapshot_unchanged": full_before["status_code"] == full_after["status_code"] == 200
            and full_before["payload_is_list"] and full_after["payload_is_list"]
            and full_before["response_sha256"] == full_after["response_sha256"],
    }
    summary = {
        "scenario_id": SCENARIO_ID, "started_at": plan["declared_at"], "finished_at": utc_now(),
        "metric_scope": "Observador externo HTTP, todas las muestras, percentil nearest-rank",
        "metrics": metrics, "checks": checks,
        "total_http_requests": len(all_rows), "health_checks": len(health_rows),
        "correlation_ratio": sum(row["correlated"] for row in all_rows) / len(all_rows),
        "observed_runtime_revisions": sorted({row["runtime_revision"] or "missing" for row in all_rows}),
        "catalog_before_sha256": full_before["response_sha256"], "catalog_after_sha256": full_after["response_sha256"],
        "catalog_items_before": full_before["item_count"], "catalog_items_after": full_after["item_count"],
        "passed": all(checks.values()),
    }
    (args.output / "resumen.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    raise SystemExit(0 if summary["passed"] else 1)


if __name__ == "__main__":
    main()
