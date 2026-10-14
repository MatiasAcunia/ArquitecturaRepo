#!/usr/bin/env python3
"""Explicit opt-in feedback sender with minimal, verifiable receipt.

Never sends an arbitrary path or project content. Network use requires local mode enabled and an explicit repo-level
non-disabled transfer setting plus a preconfigured approved endpoint, a strict allowlisted schema and a safe HTTPS destination.
No network call occurs during import/tests without a provided fake transport.
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
from urllib.error import HTTPError, URLError

from jsonschema import Draft202012Validator, ValidationError, SchemaError
from architecture_feedback import ALLOWED_PROFILES, ALLOWED_STATUS_TOKENS, ALLOWED_REVIEW_RATINGS, safe_version


MAX_REPORT_BYTES = 32768
MAX_RECEIPT_BYTES = 4096


class FeedbackHold(ValueError):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def safe_endpoint(value: str) -> str:
    if not isinstance(value, str) or len(value) > 2048:
        raise FeedbackHold("INVALID_FEEDBACK_ENDPOINT")
    try:
        parsed = urlsplit(value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError:
        raise FeedbackHold("INVALID_FEEDBACK_ENDPOINT") from None
    if (parsed.scheme != "https" or not hostname or "." not in hostname
        or parsed.username or parsed.password or parsed.query or parsed.fragment
        or any(ch.isspace() for ch in value)
        or hostname.endswith((".local", ".internal")) or hostname in
        {"localhost", "metadata.google.internal"}):
        raise FeedbackHold("HTTPS_PUBLIC_COLLECTOR_REQUIRED")
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        pass
    else:
        raise FeedbackHold("IP_LITERAL_ENDPOINT_FORBIDDEN")
    if port is not None and port != 443:
        raise FeedbackHold("NONSTANDARD_ENDPOINT_PORT_FORBIDDEN")
    return value


def validate_privacy_categories(report: dict) -> None:
    if report.get("profile") not in ALLOWED_PROFILES:
        raise FeedbackHold("UNRECOGNIZED_PROFILE_VALUE")
    if report.get("starter_version") != safe_version(report.get("starter_version")):
        raise FeedbackHold("UNRECOGNIZED_VERSION_VALUE")
    fields = (
        (report.get("control", {}), ("bootstrap_status", "product_status")),
        (report.get("project_baseline", {}), (
            "technical_status", "machine_assessment_status", "network_mode",
            "delivery_status",
        )),
        (report.get("runtime", {}), ("campaign_status",)),
    )
    for container, keys in fields:
        if not isinstance(container, dict):
            raise FeedbackHold("NONOBJECT_METADATA")
        for key in keys:
            value = container.get(key)
            if value is not None and value not in ALLOWED_STATUS_TOKENS:
                raise FeedbackHold("FREE_TEXT_METADATA_VALUE_REFUSED")
    runtime = report.get("runtime", {})
    statuses = runtime.get("work_status_counts", {})
    if not isinstance(statuses, dict) or any(
        name not in ALLOWED_STATUS_TOKENS or
        type(count) is not int or not (0 <= count <= 1000000)
        for name, count in statuses.items()
    ):
        raise FeedbackHold("FREE_TEXT_METADATA_KEY_OR_COUNT_REFUSED")
    diagnostics = report.get("diagnostics")
    if diagnostics is not None:
        from architecture_feedback import DIAGNOSTIC_FIELDS
        if (not isinstance(diagnostics, dict)
            or set(diagnostics) != set(DIAGNOSTIC_FIELDS) | {"source"}
            or diagnostics.get("source") != "ENUM_EVENT_COUNTS_ONLY"
            or any(type(diagnostics[k]) is not int or not (0 <= diagnostics[k] <= 10000)
                   for k in DIAGNOSTIC_FIELDS)):
            raise FeedbackHold("UNTRUSTED_DIAGNOSTIC_FIELD_OR_COUNT")
    process = report.get("process", {})
    if process.get("operating_review_rating") not in ALLOWED_REVIEW_RATINGS:
        raise FeedbackHold("FREE_TEXT_REVIEW_RATING_REFUSED")


def submit(*, report_path: Path, config_path: Path, schema_path: Path,
           endpoint: str, repo_opt_in: str, opener=None) -> dict:
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise FeedbackHold("CONFIG_UNREADABLE:" + type(exc).__name__) from None
    if (config.get("enabled") is not True
        or config.get("external_submission_enabled") is not True
        or config.get("privacy_mode") != "STRICT_METADATA_ONLY"
        or repo_opt_in != "true"):
        raise FeedbackHold("EXTERNAL_FEEDBACK_REQUIRES_TWO_KEY_OPT_IN")
    url = safe_endpoint(endpoint)
    if not report_path.is_file() or report_path.stat().st_size > MAX_REPORT_BYTES:
        raise FeedbackHold("REPORT_MISSING_OR_TOO_LARGE")
    payload = report_path.read_bytes()
    try:
        report = json.loads(payload.decode("utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(report)
    except (OSError, ValueError, TypeError, UnicodeError, ValidationError, SchemaError) as exc:
        # Only a fixed category is logged; never echo project data or a token.
        raise FeedbackHold("REPORT_SCHEMA_INVALID:" + type(exc).__name__) from None
    validate_privacy_categories(report)
    if report.get("privacy") != {
        "mode": "STRICT_METADATA_ONLY",
        "free_text_included": False,
        "project_identifiers_included": False,
        "code_or_paths_included": False,
        "requirements_content_included": False,
        "credentials_included": False,
    }:
        raise FeedbackHold("PRIVACY_DECLARATION_INVALID")
    sha = hashlib.sha256(payload).hexdigest()
    request = Request(url, data=payload, method="POST",
                      headers={"Content-Type": "application/json",
                               "Accept": "application/json"})
    if opener is None:
        opener = build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=15) as response:
            if response.status not in (200, 201):
                raise FeedbackHold("COLLECTOR_HTTP_UNEXPECTED")
            data = response.read(MAX_RECEIPT_BYTES + 1)
    except (HTTPError, URLError, TimeoutError) as exc:
        raise FeedbackHold("COLLECTOR_TRANSPORT_FAILED:" + type(exc).__name__) from None
    if len(data) > MAX_RECEIPT_BYTES:
        raise FeedbackHold("COLLECTOR_RECEIPT_TOO_LARGE")
    try:
        receipt = json.loads(data.decode("utf-8"))
    except (ValueError, UnicodeError):
        raise FeedbackHold("COLLECTOR_RECEIPT_INVALID_JSON") from None
    if (not isinstance(receipt, dict)
        or receipt.get("schema_version") != "agentic-feedback-receipt-v1"
        or receipt.get("accepted") is not True
        or receipt.get("report_sha256") != sha):
        raise FeedbackHold("COLLECTOR_RECEIPT_HASH_MISMATCH")
    # The collector identity must still be approved separately by the adopter.
    return {"status": "HTTPS_RECEIPT_HASH_MATCH",
            "report_sha256": sha, "accepted": True,
            "external_collector_identity_approved": "CONFIGURATION_OWNER_RESPONSIBILITY"}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--schema", type=Path, required=True)
    args = p.parse_args()
    try:
        result = submit(
            report_path=args.report, config_path=args.config,
            schema_path=args.schema,
            endpoint=os.environ.get("AGENTIC_SDLC_FEEDBACK_ENDPOINT", ""),
            repo_opt_in=os.environ.get("AGENTIC_SDLC_FEEDBACK_SUBMIT", ""),
        )
    except FeedbackHold as exc:
        print("FEEDBACK HOLD: " + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
