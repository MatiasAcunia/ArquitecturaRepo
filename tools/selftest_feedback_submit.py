#!/usr/bin/env python3
"""No-network adversarial sender checks, including strict opt-in/receipt."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from feedback_submit import FeedbackHold, safe_endpoint, submit


ROOT = Path(__file__).resolve().parents[1]


def refused(action) -> None:
    try:
        action()
    except FeedbackHold:
        pass
    else:
        raise AssertionError("Unsafe telemetry operation was accepted")


class Response:
    status = 200

    def __init__(self, payload: bytes):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def read(self, limit: int):
        return self.payload[:limit]


class Collector:
    def __init__(self, receipt_hash: str | None = None, status: int = 200):
        self.receipt_hash = receipt_hash
        self.status = status
        self.calls = 0
        self.body = b""

    def open(self, request, *, timeout: float):
        self.calls += 1
        self.body = request.data
        assert timeout <= 15
        assert request.full_url == "https://feedback.example.org/collect"
        data = json.dumps({
            "schema_version": "agentic-feedback-receipt-v1",
            "report_sha256": self.receipt_hash or hashlib.sha256(request.data).hexdigest(),
            "accepted": True,
        }).encode("utf-8")
        response = Response(data)
        response.status = self.status
        return response


def main() -> int:
    for bad in ("http://feedback.example.org", "https://localhost/x",
                "https://127.0.0.1/x", "https://x.local/", "https://a.org:444/",
                "https://user:password" + "@" + "a.org/x", "https://a.org/?secret=x",
                "https://metadata.google.internal/x", "file:///etc/passwd"):
        refused(lambda: safe_endpoint(bad))
    assert safe_endpoint("https://feedback.example.org/collect") == "https://feedback.example.org/collect"
    with tempfile.TemporaryDirectory(prefix="feedback-submit-") as tmp:
        project = Path(tmp) / "project"
        install = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "scaffold_project.py"),
             "--target", str(project), "--profile", "SMALL", "--product-id", "SYNTHETIC"],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if install.returncode:
            raise AssertionError("fixture scaffold failed: " + install.stderr)
        control = project / ".agentic-sdlc"
        report = Path(tmp) / "feedback.json"
        build = subprocess.run(
            [sys.executable, str(control / "tools" / "architecture_feedback.py"),
             "--control-root", str(control), "--trigger", "MANUAL", "--output", str(report)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if build.returncode:
            raise AssertionError("synthetic report not generated: " + build.stderr)
        config = control / "feedback" / "ARCHITECTURE_FEEDBACK_CONFIG.json"
        schema = control / "schemas" / "architecture-feedback-report.schema.json"
        request = dict(report_path=report, config_path=config, schema_path=schema,
                       endpoint="https://feedback.example.org/collect", repo_opt_in="true")
        transport = Collector()
        # Even default opt-out transmission intent cannot send without a
        # configured endpoint, and explicit user disable always wins.
        refused(lambda: submit(**{**request, "endpoint": ""}, opener=transport))
        assert transport.calls == 0, "Missing collector endpoint initiated external POST"
        data = json.loads(config.read_text(encoding="utf-8"))
        assert data["external_submission_enabled"] is True
        refused(lambda: submit(**{**request, "repo_opt_in": "false"}, opener=transport))
        assert transport.calls == 0, "Explicit recipient disable initiated external POST"
        data["external_submission_enabled"] = False
        config.write_text(json.dumps(data), encoding="utf-8")
        refused(lambda: submit(**request, opener=transport))
        assert transport.calls == 0, "Config opt-out initiated external POST"
        data["external_submission_enabled"] = True
        config.write_text(json.dumps(data), encoding="utf-8")
        accepted = submit(**request, opener=transport)
        assert accepted["status"] == "HTTPS_RECEIPT_HASH_MATCH"
        assert transport.calls == 1 and transport.body == report.read_bytes()
        refused(lambda: submit(**request, opener=Collector(receipt_hash="0" * 64)))
        refused(lambda: submit(**request, opener=Collector(status=302)))
        raw = json.loads(report.read_text(encoding="utf-8"))
        raw["unexpected_code"] = "DO_NOT_EXFILTRATE"
        report.write_text(json.dumps(raw), encoding="utf-8")
        rejected_transport = Collector()
        refused(lambda: submit(**request, opener=rejected_transport))
        assert rejected_transport.calls == 0, "Out-of-schema data leaked to HTTP collector"
        # Valid JSON Schema is insufficient when a free-text dictionary key
        # could smuggle private data through aggregated work-status counts.
        safe = json.loads(transport.body.decode("utf-8"))
        safe["runtime"]["work_status_counts"]["PRIVATE_SOURCE_KEY_DO_NOT_SEND"] = 1
        report.write_text(json.dumps(safe), encoding="utf-8")
        collision = Collector()
        refused(lambda: submit(**request, opener=collision))
        assert collision.calls == 0, "Free-text status key exfiltrated through metadata"
        safe["runtime"]["work_status_counts"].pop("PRIVATE_SOURCE_KEY_DO_NOT_SEND")
        safe["profile"] = "PRIVATE_PROJECT_ID"
        report.write_text(json.dumps(safe), encoding="utf-8")
        collision2 = Collector()
        refused(lambda: submit(**request, opener=collision2))
        assert collision2.calls == 0, "Free-text profile exfiltrated"

        safe["profile"] = json.loads(transport.body.decode("utf-8"))["profile"]
        safe["diagnostics"] = {"source": "ENUM_EVENT_COUNTS_ONLY",
                              "erratic_agent_observations": 0, "misconfiguration_observations": 0,
                              "stale_authority_observations": 0, "unbounded_retry_observations": 0,
                              "ambiguous_external_effect_observations": 0,
                              "resource_contention_observations": 0,
                              "PRIVATE_INFORMATION": 1}
        report.write_text(json.dumps(safe), encoding="utf-8")
        collision3 = Collector()
        refused(lambda: submit(**request, opener=collision3))
        assert collision3.calls == 0, "Unallowlisted diagnosis leaked"
        report.write_bytes(b"{}")
        refused(lambda: submit(**request, opener=Collector()))
        report.write_bytes(b"0" * 33000)
        refused(lambda: submit(**request, opener=Collector()))
    print("FEEDBACK SUBMISSION SELF-TEST PASSED — two-key opt-in, HTTPS, bounded schema, exact digest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
