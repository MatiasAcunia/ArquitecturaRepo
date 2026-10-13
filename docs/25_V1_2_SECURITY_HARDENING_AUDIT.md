# v1.2 Security & Robustness Audit — candidate, not a release

Date: 2026-10-13. Owner: starter repository. Scope: the v1.2 development PR and inherited v1.1 mechanics. This is a threat model + code/CI hardening ledger, **not** an independent penetration test, Windows deployment certificate, provider audit or general-purpose proof of safety.

## Audit goals

No accidental Product State replacement, privilege escalation, external paid action, data exfiltration, stale writer acceptance, fabricated receipt, duplicate external effect, incorrect Goal continuation, in-band reviewer acceptance, irreversible cleanup or upgrade incompatibility. Controls must be proportional to profile; the smallest profile must not quietly install resident supervisors or enabled LLM calls.

## Findings and present dispositions

| Severity | Finding / falsifier | Candidate disposition | Acceptance boundary |
|---|---|---|---|
| HIGH | Reinstallation could erase unsaved CLIENT theory while still in DRAFT | v1.2 refuses --force regardless of apparently dormant state; tests unchanged byte preservation | Use explicit versioned migrations or a fresh sandbox, never silent overwrite |
| HIGH | Local Goal diagnostic accepted caller-supplied host-verified flags and could appear to grant execution authority | Removed forgeable CLI/argument path; the library now always returns may_execute_material_goal=false absent a separately verified host adapter | Real Codex Goal hook and remote currentness proof remain BLOCKED |
| HIGH | External effect record called a caller-asserted provider receipt VERIFIED | Changed to RECEIPT_ATTESTED_UNVERIFIED; idempotency and ambiguous timeout still HOLD | Actual provider readback and source identity must be demonstrated |
| HIGH | Generated/constructed feedback metadata might leak through arbitrary status strings or keys | Allowlist exporter fields, validate outgoing schema and enum keys, reject unrecognized value/key, no raw collector response logging | External collector receipt/real user consent remains independent |
| HIGH | Outbound feedback could treat HTTP success as delivery, echo arbitrary response or accept redirects | Opt-out intent only when a verified named HTTPS collector is configured; until then LOCAL_ONLY. Bounded schema, strict fixed categories, and exact report SHA receipt, no content echo | Authenticated/authorized collector identity and real reception remain unproven |
| MEDIUM | Mutable third-party GitHub Action tags could change content | Pin checkout/setup-python/upload-artifact to exact reviewed upstream commits and disable persisted checkout credentials | Recheck upstream SHA, update dependencies with review |
| MEDIUM | Gemini transport might be activated by a mere API key or unsafe model name | Require explicit AGENTIC_SDLC_GEMINI_ENABLED=true; restrict model name, request timeout and response size; no private data by default | Account/quota/data policy/real Goal consumption remain unproven |
| MEDIUM | Context resets/long tactical plans can drift from authorized Goal | Goal->charter exact digest + versioned I3 plan + revision conflict + active-progress review due; fresh Goal changes HOLD | Current host invocation and active-time accounting must be physical |
| MEDIUM | Stale mutator runs and self-review could falsely certify own output | Optional epoch-fenced local critical section, exact frozen candidate/source hash and reviewer separation | Never substitute for system physical gates or host-level permissions |
| MEDIUM | Optional five-task OWNER config could override deliberate pauses | Pure recovery policy includes explicit CLIENT/platform/safety suspension holds and no extra supervisor | Scheduling/reads/writes are not implemented by this policy |
| LOW | Language UI could claim GitHub README geo-locale auto-routing | Static explicit 8-language links; local OS/--language detection; fallback to English; offline docs | Translated *intro/FAQ* coverage, not translation of every technical protocol |

## Defense-in-depth suites

- Existing v1.1: schema/ownership/currentness/adoption, six profiles, transaction journal/crash recovery, independent review and shared state primitive.
- v1.2 operational: impossible synthetic Goal host PASS, changed-source/charter hold, source traversal rejection, tactical revision conflict, external-effect duplicate dispatch block, stale I4 advice, bounded Gemini opt-in, actor fencing, exact reviewer/source binding.
- v1.2 scaffolding: path traversal, nonstarter --force refusal, symlink rejection, no unrequested SMALL I4/OWNER deployment.
- v1.2 i18n: explicit and OS-locale resolution, unsupported override errors, fallback, offline docs existence, consistent FAQ questions across eight languages.
- v1.2 feedback: disabled-by-default external transport, safe HTTPS endpoint, wrong/missing digest refusal, unexpected status, schema-invalid payload, free-text metadata keys and status-value exfil tests.
- All candidate gates are run on the exact commit by GitHub Actions. Run/test screenshots, successful earlier SHA, or the user-facing PASS string do **not** count as evidence for a later SHA.

## Open / blocked items — do not promote

1. Codex Desktop **2.0.2** native Goal Resume, context re-anchor and daily close transport must be tested on the user's authorized disposable Windows pilot, including active-writer HOLD, quota truth, cloud readback and rollback. Do not touch active workstream Goals.
2. Gemini in a *real* continuing I3 Goal: verified export authority, quota, two distinct-evidence consultations, delivery, model consumption and falsifying test; read-only output cannot self-certify.
3. The OWNER five-task pack needs actual provider scheduler installation, mutual recovery for exactly five IDs, explicit suspensions preserved and readbacks; fake task IDs are not acceptance.
4. Opt-out remote telemetry is default-intent only; without a configured approved collector there is NO actual remote delivery. A real receipt, recipient identity, visible first-run disclosure, privacy guarantee and disable tests are needed before claiming central feedback.
5. Security posture of real adopter applications: auth, backup, licensing, data retention, deployment exposure, code-specific tests and human/subjective gates are always project-owned.
6. Current code still depends on Python/PyPI/GitHub runner supply chain; CI and SHA pins reduce but cannot eliminate that risk. No unrestricted auto-upgrade.
7. The starter has not undergone an independent external code audit. Threat-model pass and synthetic tests are not equivalent to a penetration test.

## Release verdict

**DO NOT RELEASE 1.2.0** until all required physical gate IDs in state/V1_2_ACCEPTANCE_CRITERIA.json are individually accepted from exact immutable candidates. Keep the PR as draft; stable main remains 1.1.x. Do not let test-gate success replace host or product proof.

## Additional synthetic endurance gate

`python tools/selftest_v12_longitudinal.py` exercises three separate interpreter processes, durable plan identity, a revision race, a changed charter, ambiguous external-effect replay refusal and metadata-only diagnostics. It does not simulate hours of actual L3 execution or prove an external provider readback.

## Post-plan critical finding: crash-journal reference confinement

A persisted transaction journal previously carried relative target and stage references directly into recovery. v1.2 now validates the *entire* journal (transaction ID format, phase, bounded operations, hashes, unique destinations, confinement, protected runtime paths, symlinks and stage references) before applying any operation. A malformed journal remains untouched for deliberate reconciliation; it cannot authorize writes or cleanup outside its control root. The adversarial synthetic suite checks traversal, absolute paths, Windows drive paths, duplicate operations, tampered stage references, protected lock/journal, unsafe metadata and a positive genuine recovery. This is an essential boundary, not an invitation to treat arbitrary local journal edits as authenticated evidence.

## Post-plan critical finding: partial first-install side effects

Scaffold generation now stages the project-local control directory in a private temporary folder of the same target filesystem, renames the complete control into place only after population, and removes its temporary stage on failure. An injected mid-copy exception must leave existing source bytes and workflows intact, and a newly created empty target root is removed. A preexisting workflow, including a recognizable but possibly user-modified managed one, is preserved rather than silently overwritten. The GitHub Actions workflow resides in a distinct directory and cannot be atomically committed together with the control; a failure after the control move records an explicit workflow HOLD and never erases newly generated CLIENT theory. Concurrency races and real Windows filesystem behavior still require the L3 physical pilot.
