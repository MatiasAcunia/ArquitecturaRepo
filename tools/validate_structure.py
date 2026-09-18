#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "README.md",
    "AGENTS.md",
    "VERSION",
    "state/STARTER_MANIFEST.json",
    "state/V1_RELEASE_CRITERIA.json",
    "protocols/AUTHORITY_MODEL.md",
    "protocols/CLIENT_BOUNDARY.md",
    "protocols/IDENTITY_AND_EXECUTION_AUTHORITY.md",
    "protocols/CURRENTNESS_RECONSTRUCTION.md",
    "protocols/REPOSITORY_EFFICIENCY_AND_WORKSPACE_HYGIENE.md",
    "protocols/PLANNER_KERNEL.md",
    "protocols/PRODUCT_MODEL_AND_THEORY_LOADING.md",
    "protocols/CAMPAIGN_CHARTER_STANDARD.md",
    "protocols/EXECUTION_TEAM_OS.md",
    "protocols/CAPABILITY_DAG_AND_ISOLATION.md",
    "protocols/CAPABILITY_LIFECYCLE_AND_EVIDENCE.md",
    "protocols/REVIEW_FREEZE_AND_TERMINAL_INTEGRITY.md",
    "protocols/MASTER_OWNER_OS.md",
    "protocols/STATE_DB_LINEAGE_AND_IDEMPOTENCY.md",
    "protocols/STORAGE_AND_ARTIFACT_LIFECYCLE.md",
    "protocols/CAPACITY_DEADLINES_AND_RESUME.md",
    "protocols/COST_CAPACITY_AND_EXTERNAL_SERVICES.md",
    "protocols/SECURITY_PRIVACY_RIGHTS_AND_EXTERNAL_ACTIONS.md",
    "protocols/SYSTEMIC_ESCALATION_AND_ANTI_CHURN.md",
    "protocols/INTERACTION_LEDGER.md",
    "prompts/INSTALL_THIS_SDLC.md",
    "prompts/FRESH_CONTEXT_PROBE.md",
    "prompts/MASTER_OWNER_RECONCILIATION.md",
    "schemas/product-state.schema.json",
    "schemas/campaign-charter.schema.json",
    "schemas/campaign-checkpoint.schema.json",
    "schemas/campaign-terminal.schema.json",
    "schemas/identity-registry.schema.json",
    "schemas/execution-authority.schema.json",
    "schemas/current-bootstrap.schema.json",
    "schemas/current-bootstrap-v0.1.schema.json",
    "schemas/interaction-record.schema.json",
    "schemas/starter-manifest.schema.json",
    "schemas/profiles.schema.json",
    "schemas/profile-selection.schema.json",
    "schemas/campaign-runtime.schema.json",
    "schemas/transition-journal.schema.json",
    "schemas/migration-registry.schema.json",
    "schemas/owner-registry.schema.json",
    "profiles/profiles.json",
    "migrations/registry.json",
    "tools/validate_project.py",
    "tools/selftest_validation.py",
    "tools/scaffold_project.py",
    "tools/selftest_scaffold.py",
    "tools/campaignctl.py",
    "tools/selftest_runtime.py",
    "tools/migrate_state.py",
    "tools/selftest_migrations.py",
    "tools/selftest_ownership.py",
    "tools/reconstruct_context.py",
    "tools/selftest_reconstruction.py",
    "templates/PROJECT_OVERLAY.md",
    "templates/WORKSPACE_LIFECYCLE.json",
    "templates/INSTALLATION_REPORT.md",
    "templates/MASTER_OWNER_HANDOFF_CURRENT.md",
    "templates/IDENTITY_REGISTRY_CURRENT.json",
    "templates/EXECUTION_AUTHORITY_CURRENT.json",
    "docs/08_REFERENCE_PROJECT_LAYOUT.md",
    "docs/09_ADAPTATION_DECISION_TREE.md",
    "docs/10_EXECUTABLE_VALIDATION.md",
    "docs/11_REFERENCE_RUNTIME.md",
    "docs/12_TRANSACTION_RECOVERY.md",
    "docs/13_SCHEMA_EVOLUTION.md",
    "docs/14_CANONICAL_OWNERSHIP.md",
    "docs/15_STATEFUL_REFERENCE_AND_TRANSFER.md",
    "docs/16_TRANSFER_ADOPTION.md",
    "docs/17_V1_RELEASE_GATES.md",
    "docs/18_RELEASE_CANDIDATE_HARDENING.md",
    "docs/19_V1_RELEASE.md",
    "docs/20_REPOSITORY_EFFICIENCY_AND_LOCAL_HYGIENE.md",
    "examples/minimal/PRODUCT_STATE_CURRENT.json",
    "examples/active_campaign/PRODUCT_STATE_CURRENT.json",
    "examples/terminal_candidate/PRODUCT_STATE_CURRENT.json",
    "tools/selftest_stateful_reference.py",
    "tools/state_tx.py",
    "tools/discover_project.py",
    "tools/apply_adoption.py",
    "tools/selftest_adoption.py",
    "tools/selftest_contracts.py",
    "tools/selftest_hardening.py",
    "tools/repo_delta.py",
    "tools/commit_guard.py",
    "tools/workspace_gc.py",
    "tools/selftest_repository_hygiene.py",
    "tools/verify_v1_release.py",
    "schemas/adoption-spec.schema.json",
    "schemas/v1-release-criteria.schema.json",
    "schemas/workspace-lifecycle.schema.json",
    "examples/stateful_backend/app/note_store.py",
    "examples/stateful_backend/tests/test_note_store.py",
    "examples/stateful_backend/evidence/STATEFUL_REFERENCE_EVIDENCE.json",
    "examples/stateful_backend/control/state/PRODUCT_STATE_CURRENT.json",
    "examples/stateful_backend/control/state/CURRENT_BOOTSTRAP_STATE.json",
    "examples/stateful_backend/control/state/OWNER_REGISTRY_CURRENT.json",
]

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
SHA40_RE = re.compile(r"(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])", re.IGNORECASE)
PRIVATE_KEY_RE = re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY")
TOKEN_HINT_RE = re.compile(
    r"(?i)(?:api[_-]?key|secret|access[_-]?token|bearer)\s*[:=]\s*['\"][A-Za-z0-9_\-]{12,}"
)
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def parse_json_files(errors: list[str]) -> None:
    for path in ROOT.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"invalid JSON: {path.relative_to(ROOT)}: {exc}", errors)


def validate_schemas(errors: list[str]) -> None:
    for path in (ROOT / "schemas").glob("*.schema.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            fail(f"schema draft missing/incorrect: {path.relative_to(ROOT)}", errors)
        if not data.get("$id"):
            fail(f"schema id missing: {path.relative_to(ROOT)}", errors)
        if data.get("type") != "object":
            fail(f"top-level schema must be object: {path.relative_to(ROOT)}", errors)


def validate_version(errors: list[str]) -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    manifest = json.loads((ROOT / "state/STARTER_MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("version") != version:
        fail(f"VERSION ({version}) != manifest version ({manifest.get('version')})", errors)

    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
    if match is None:
        fail(f"VERSION must be semantic MAJOR.MINOR.PATCH: {version!r}", errors)
    else:
        major = int(match.group(1))
        expected_status = (
            "PUBLIC_STARTER_PREVIEW" if major == 0 else "PUBLIC_STARTER_STABLE"
        )
        if manifest.get("status") != expected_status:
            fail(
                f"VERSION {version} requires manifest status {expected_status!r}; "
                f"found {manifest.get('status')!r}",
                errors,
            )
    policy = manifest.get("content_policy", {})
    if policy.get("structure_only") is not True:
        fail("manifest content policy must set structure_only=true", errors)
    for key in [
        "project_specific_source_data_allowed",
        "real_source_names_allowed",
        "real_source_repositories_allowed",
        "real_source_branches_allowed",
        "real_source_identifiers_allowed",
        "real_source_provider_economics_allowed",
    ]:
        if policy.get(key) is not False:
            fail(f"manifest content policy must set {key}=false", errors)


def validate_required_paths(errors: list[str]) -> None:
    for rel in REQUIRED_PATHS:
        if not (ROOT / rel).exists():
            fail(f"missing required path: {rel}", errors)


def validate_structure_only(errors: list[str]) -> None:
    text_suffixes = {".md", ".json", ".py", ".yml", ".yaml", ".txt"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() not in text_suffixes and path.name != "VERSION":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        if EMAIL_RE.search(text):
            fail(f"possible personal email in public starter: {rel}", errors)
        if SHA40_RE.search(text):
            fail(f"40-char commit-like identifier in structure-only starter: {rel}", errors)
        if PRIVATE_KEY_RE.search(text):
            fail(f"private-key material detected: {rel}", errors)
        if TOKEN_HINT_RE.search(text):
            fail(f"possible embedded credential detected: {rel}", errors)


def validate_internal_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for target in MD_LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            resolved = (path.parent / clean).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"markdown link escapes repository: {path.relative_to(ROOT)} -> {target}", errors)
                continue
            if not resolved.exists():
                fail(f"broken internal markdown link: {path.relative_to(ROOT)} -> {target}", errors)



def validate_migration_registry(errors: list[str]) -> None:
    registry_path = ROOT / "migrations" / "registry.json"
    if not registry_path.exists():
        fail("missing migration registry", errors)
        return

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    manifest = json.loads(
        (ROOT / "state/STARTER_MANIFEST.json").read_text(encoding="utf-8")
    )
    declared_latest = manifest.get("latest_schema_versions", {})

    for contract, version in registry.get("latest_versions", {}).items():
        if declared_latest.get(contract) != version:
            fail(
                f"manifest latest schema for {contract} "
                f"({declared_latest.get(contract)!r}) != migration registry ({version!r})",
                errors,
            )

    seen_ids: set[str] = set()
    for migration in registry.get("migrations", []):
        migration_id = migration.get("migration_id")
        if migration_id in seen_ids:
            fail(f"duplicate migration_id: {migration_id}", errors)
        seen_ids.add(migration_id)

        for key in ("from_schema", "to_schema"):
            schema_name = migration.get(key)
            if not schema_name or not (ROOT / "schemas" / schema_name).exists():
                fail(
                    f"migration {migration_id!r} references missing {key}: {schema_name!r}",
                    errors,
                )

        if migration.get("from_version") == migration.get("to_version"):
            fail(f"migration {migration_id!r} has identical from/to version", errors)

def main() -> int:
    errors: list[str] = []
    validate_required_paths(errors)
    parse_json_files(errors)
    validate_schemas(errors)
    validate_version(errors)
    validate_migration_registry(errors)
    validate_structure_only(errors)
    validate_internal_links(errors)

    if errors:
        print("STRUCTURE VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print("STRUCTURE VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
