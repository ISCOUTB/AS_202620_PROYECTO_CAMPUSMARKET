"""Regresiones del diagnostico; no acceden a Docker, GHCR ni bases de datos."""

import contextlib
import io
import json
import subprocess
import unittest
from unittest.mock import Mock, patch

from scripts.ensayar_imagen_ghcr import IMAGE, Trial, TrialError, classify_pull_error


class PullDiagnosticsTests(unittest.TestCase):
    def trial(self):
        trial = Trial.__new__(Trial)
        trial.state = {}
        trial.save = Mock()
        return trial

    def test_classification_uses_explicit_markers(self):
        cases = {
            "manifest unknown": "REFERENCE_NOT_FOUND",
            "MANIFEST_UNKNOWN: manifest unknown": "REFERENCE_NOT_FOUND",
            "name unknown": "REFERENCE_NOT_FOUND",
            "unexpected status from HEAD request: 404 Not Found": "REFERENCE_NOT_FOUND",
            'failed to resolve reference "synthetic": synthetic: not found': "REFERENCE_NOT_FOUND",
            "no matching manifest for linux/arm64/v8": "PLATFORM_MISMATCH",
            "no match for platform in manifest": "PLATFORM_MISMATCH",
            "unauthorized: authentication required": "AUTHENTICATION",
            "denied: requested access to the resource is denied": "AUTHORIZATION",
            "unexpected status: 403 Forbidden": "AUTHORIZATION",
            "toomanyrequests: rate exceeded": "RATE_LIMIT",
            "invalid reference format": "INVALID_REFERENCE",
            "Cannot connect to the Docker daemon": "DAEMON_UNAVAILABLE",
            "dial tcp: lookup ghcr.io: no such host": "NETWORK",
            "net/http: TLS handshake timeout": "NETWORK",
            "x509: certificate signed by unknown authority": "TLS",
            "unexpected status: 503 Service Unavailable": "REGISTRY_SERVER",
            "write: no space left on device": "STORAGE",
            "unexpected EOF": "UNKNOWN",
            "": "UNKNOWN",
        }
        for stderr, expected in cases.items():
            with self.subTest(stderr=stderr):
                self.assertEqual(classify_pull_error(stderr), expected)

    def test_failure_records_only_safe_category_and_exit_code(self):
        for stderr, category in (("manifest unknown", "REFERENCE_NOT_FOUND"), ("unexpected EOF", "UNKNOWN")):
            with self.subTest(category=category):
                trial = self.trial()
                secret = "SYNTHETIC_PRIVATE_SENTINEL"
                result = subprocess.CompletedProcess([], 1, stdout=secret, stderr=stderr + " " + secret)
                output = io.StringIO()
                with patch("scripts.ensayar_imagen_ghcr.subprocess.run", return_value=result), contextlib.redirect_stdout(output), self.assertRaises(TrialError) as error:
                    trial.command(["docker", "pull", IMAGE], "descargar digest GHCR", diagnose_pull=True)
                self.assertEqual(trial.state, {"docker_pull_error": {"category": category, "exit_code": 1}})
                self.assertIn(category, str(error.exception))
                self.assertNotIn(secret, json.dumps(trial.state) + str(error.exception) + output.getvalue())
                self.assertNotIn(stderr, str(error.exception))
                trial.save.assert_called_once()

    def test_timeout_never_exposes_process_output(self):
        trial = self.trial()
        secret = "SYNTHETIC_TIMEOUT_SENTINEL"
        timeout = subprocess.TimeoutExpired("docker", 240, output=secret, stderr=secret)
        with patch("scripts.ensayar_imagen_ghcr.subprocess.run", side_effect=timeout), self.assertRaises(TrialError) as error:
            trial.command(["docker", "pull", IMAGE], "descargar digest GHCR", diagnose_pull=True)
        self.assertEqual(trial.state["docker_pull_error"], {"category": "TIMEOUT", "exit_code": None})
        self.assertNotIn(secret, str(error.exception) + json.dumps(trial.state))

    def test_other_commands_keep_original_private_failure(self):
        trial = self.trial()
        result = subprocess.CompletedProcess([], 1, stdout="PRIVATE_STDOUT", stderr="PRIVATE_STDERR")
        with patch("scripts.ensayar_imagen_ghcr.subprocess.run", return_value=result), self.assertRaises(TrialError) as error:
            trial.command(["docker", "inspect", "synthetic"], "inspeccionar")
        self.assertEqual(str(error.exception), "Fallo de infraestructura: inspeccionar")
        self.assertEqual(trial.state, {})
        trial.save.assert_not_called()

    def test_success_preserves_return_value_without_diagnostics(self):
        trial = self.trial()
        result = subprocess.CompletedProcess([], 0, stdout="synthetic result", stderr="")
        with patch("scripts.ensayar_imagen_ghcr.subprocess.run", return_value=result):
            self.assertEqual(trial.command(["docker", "pull", IMAGE], "descargar", diagnose_pull=True), "synthetic result")
        self.assertEqual(trial.state, {})
        trial.save.assert_not_called()


if __name__ == "__main__":
    unittest.main()
