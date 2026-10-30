"""Controles de procedencia, integridad y privacidad del publicador sin builds."""

import copy
import json
import os
import subprocess
import unittest
from unittest.mock import patch

from scripts import publicar_web_verificada as publisher


def metadata():
    run = {"id": publisher.RUN, "head_sha": publisher.SOURCE, "repository": {"full_name": publisher.REPOSITORY},
           "head_repository": {"full_name": publisher.REPOSITORY}, "event": "push", "head_branch": publisher.BRANCH,
           "path": ".github/workflows/web-institucional.yml", "status": "completed", "conclusion": "success"}
    artifact = {"id": publisher.ARTIFACT, "expired": False, "name": f"web-institucional-{publisher.SOURCE}-1",
                "digest": "sha256:" + publisher.ZIP_SHA, "workflow_run": {"id": publisher.RUN, "head_sha": publisher.SOURCE}}
    return run, artifact


def evidence():
    checks = {key: {"status": "CUMPLE", "result": {}} for key in publisher.CRITERIA}
    checks["export"]["result"] = {"image_id": publisher.IMAGE_ID, "archive_sha256": publisher.TAR_SHA}
    checks["cleanup"]["result"] = {"containers": [], "volumes": [], "networks": []}
    return {"commit": publisher.SOURCE, "run": f"https://github.com/{publisher.REPOSITORY}/actions/runs/{publisher.RUN}",
            "passed": True, "checks": checks, "image_id": publisher.IMAGE_ID}


class PublisherTests(unittest.TestCase):
    def test_provenance_rejects_wrong_run_fork_event_source_status_and_zip(self):
        run, artifact = metadata()
        publisher.verify_provenance(run, artifact)
        for field, value in (("head_sha", "0" * 40), ("id", 1), ("event", "pull_request"),
                             ("conclusion", "failure"), ("status", "in_progress"), ("path", "other.yml"),
                             ("head_branch", "master"), ("head_repository", {"full_name": "other/repo"})):
            broken = {**run, field: value}
            with self.subTest(field=field), self.assertRaises(publisher.VerificationError):
                publisher.verify_provenance(broken, artifact)
        for field, value in (("expired", True), ("id", 1), ("digest", "sha256:" + "0" * 64),
                             ("workflow_run", {"id": 1, "head_sha": publisher.SOURCE}), ("name", "other")):
            broken = {**artifact, field: value}
            with self.subTest(field=field), self.assertRaises(publisher.VerificationError):
                publisher.verify_provenance(run, broken)

    def test_partial_checks_or_wrong_identity_cannot_be_published(self):
        data = evidence()
        publisher.verify_evidence(data)
        for key in publisher.CRITERIA:
            broken = copy.deepcopy(data)
            broken["checks"][key]["status"] = "BLOQUEADO"
            with self.subTest(key=key), self.assertRaises(publisher.VerificationError):
                publisher.verify_evidence(broken)
        for key, value in (("passed", False), ("image_id", "sha256:" + "0" * 64), ("commit", "0" * 40), ("failure", "export failed")):
            broken = {**data, key: value}
            with self.subTest(key=key), self.assertRaises(publisher.VerificationError):
                publisher.verify_evidence(broken)
        broken = copy.deepcopy(data)
        broken["checks"]["cleanup"]["result"]["volumes"] = ["remaining"]
        with self.assertRaises(publisher.VerificationError):
            publisher.verify_evidence(broken)

    def test_failed_docker_command_never_exposes_output(self):
        failure = subprocess.CompletedProcess(["docker"], 1, b"synthetic-private-token", b"synthetic-password")
        with patch.object(publisher.subprocess, "run", return_value=failure), self.assertRaises(publisher.VerificationError) as result:
            publisher.command(["docker", "push", "safe-reference"])
        self.assertEqual(str(result.exception), "Operacion docker rechazada: exit=1")

    def test_publish_requires_manual_fork_branch(self):
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": "ISCOUTB/AS_202620_PROYECTO_CAMPUSMARKET"}), self.assertRaises(publisher.VerificationError):
            publisher.publish("synthetic")
        with patch.dict(os.environ, {"GITHUB_REPOSITORY": publisher.REPOSITORY, "GITHUB_EVENT_NAME": "push"}), self.assertRaises(publisher.VerificationError):
            publisher.publish("synthetic")

    def test_auth_directory_is_removed_on_failed_push(self):
        recorded = []

        def fail(args, **kwargs):
            if args[1] == "push":
                recorded.append(os.environ["DOCKER_CONFIG"])
                raise publisher.VerificationError("push rejected")
            return b""

        env = {"GITHUB_REPOSITORY": publisher.REPOSITORY, "GITHUB_EVENT_NAME": "workflow_dispatch",
               "GITHUB_REF": "refs/heads/" + publisher.BRANCH, "GITHUB_ACTOR": "Nnigarp", "DOCKER_CONFIG": "/previous"}
        with patch.dict(os.environ, env), patch.object(publisher, "command", side_effect=fail):
            with self.assertRaises(publisher.VerificationError):
                publisher.publish("synthetic")
            self.assertEqual(os.environ["DOCKER_CONFIG"], "/previous")
        self.assertFalse(os.path.exists(recorded[0]))

    def test_remote_manifest_and_image_id_are_verified(self):
        calls = []

        def docker(args, **kwargs):
            calls.append(args)
            if args[1] == "push":
                return b"tag: digest: sha256:" + b"1" * 64 + b" size: 123"
            if args[1] == "buildx":
                return json.dumps({"config": {"digest": "sha256:" + "0" * 64}}).encode()
            return b""

        env = {"GITHUB_REPOSITORY": publisher.REPOSITORY, "GITHUB_EVENT_NAME": "workflow_dispatch",
               "GITHUB_REF": "refs/heads/" + publisher.BRANCH, "GITHUB_ACTOR": "Nnigarp"}
        with patch.dict(os.environ, env), patch.object(publisher, "command", side_effect=docker), self.assertRaisesRegex(publisher.VerificationError, "Manifest GHCR contiene otra imagen"):
            publisher.publish("synthetic")
        self.assertFalse(any(args[1] == "pull" for args in calls))
        self.assertFalse(any(args[1] == "build" for args in calls))


if __name__ == "__main__":
    unittest.main()
