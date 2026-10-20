---
name: security-review
description: "Review Neo Child Clinic Desktop authentication, authorization, RLS, secrets, token storage, Wails IPC, local database protection, sensitive data, logging, and update security. Use for source-grounded security and privacy findings with severity and evidence; never expose credentials."
metadata:
  version: "1.0"
  mode: "read-only"
  scope: "neo-child-clinic-desktop"
---

# Security Review

Identify security and privacy failures at real trust boundaries: authentication, authorization, Supabase RLS, Wails bindings, local storage, secrets, logging, and updates. A suspicious pattern is not a finding until the affected principal, resource, and impact are established.

## Invoke when

- Before a release, after auth/RLS changes, or when adding a Wails binding or local file access.
- When reviewing Supabase policies, RPCs, storage buckets, or service-role usage.
- When credentials, tokens, patient data, backups, or logs may be exposed.
- When the desktop update mechanism or IPC surface changes.

Do not use this skill to exploit a live service, rotate credentials, or change policies. Hand off remediation to `implementation-planner`.

## Inputs

- Audit report and architecture/data-flow notes, if available.
- Review scope: authentication, authorization, RLS, IPC, local data, secrets, logging, updates, or a named flow.
- Desktop root, Supabase migrations/config/functions, and any local database schema.
- Environment: source-only, local Supabase, or staging. Never assume production access.

## Before you start

1. Read the root and nested `AGENTS.md` when present, project instructions, and `git status --short --branch`; never reset, clean, checkout, or stash user changes. Then read the security policy.
2. Record the commit, branch, and dirty state.
3. Define the assets (patient data, financial records, inventory, credentials, backups), actors (unauthenticated user, staff role, admin, local attacker, malicious document/URL), and trust boundaries.
4. Confirm which environments are actually available. Do not describe a hosted setting as verified without evidence.

## Evidence standard

- `[VERIFIED]` — source/configuration or a bounded local test establishes the path. Cite `path:line`, migration/policy name, or command output.
- `[INFERENCE]` — a plausible issue derived from cited code, with stated assumptions.
- `[PROPOSED]` — a recommended control; not proof of a vulnerability or a fix.
- `[UNKNOWN]` — requires a live database, deployed policy, OS behavior, or credential you cannot inspect.

Severity: `Critical` (auth bypass, cross-tenant data, secret exposure, patient-safety or financial integrity), `High`, `Medium`, `Low`, `Info`. Distinguish a missing defense-in-depth control from an exploitable boundary failure.

**Never copy a secret, token, key, cookie, or personal record into the report.** Cite only the file and line and redact the value. If a real credential is present, stop, report the location, and recommend rotation through the owner.

## Procedure

1. **Authentication.** Trace sign-in, session creation, token storage, refresh, expiry, logout, account switching, password recovery, and deep-link/callback handling. Verify where tokens live on disk and whether they are protected by the OS keychain or an equivalent.
2. **Authorization.** Map roles and permissions from app metadata, Go checks, UI guards, and Supabase policies. Verify that every sensitive operation is authorized server-side, not only in the UI or a Wails binding.
3. **RLS and database authority.** For every exposed table/view/RPC, record whether RLS is enabled, which policies apply to SELECT/INSERT/UPDATE/DELETE, which roles they target, and whether `SECURITY DEFINER` functions validate the caller. Treat service-role keys as server-only. Do not infer a policy from documentation; read the migration or query the local schema.
4. **Wails IPC.** List every binding exposed to the frontend. Check argument validation, authorization, path traversal, file read/write scope, command execution, URL opening, and whether a compromised renderer can invoke privileged operations it should not.
5. **Local data protection.** Inspect the local database/cache, encryption at rest, key storage, backups, exports, temp files, logs, crash reports, and deletion on logout. Verify that patient and financial data are not left in world-readable locations.
6. **Secrets and configuration.** Check `.env*`, build-time variables, CI secrets, committed config, logs, and error messages. Report names and locations, never values. Note whether secrets are baked into the desktop binary or shipped to the frontend.
7. **Sensitive logging and privacy.** Look for patient identifiers, clinical notes, payment data, tokens, and sync payloads in logs, telemetry, crash handlers, and error UI. Check data minimization, retention, and access.
8. **Update security.** Inspect update source, signature/checksum verification, TLS, downgrade protection, channel selection, and rollback behavior. A downloaded update without independent integrity verification is a finding only when the attack path is established.
9. **Supply chain and dependencies.** Note unpinned dependencies, install scripts, CI permissions, and release signing. Do not call a dependency vulnerable without evidence.
10. **Report.** For each finding: ID, severity, confidence, boundary, affected principal, resource, evidence, preconditions, impact, reproduction/verification, recommended control, and residual unknowns. Separate confirmed defects from suspected issues.

## Output contract

```markdown
# Security and Privacy Review — <commit> — <YYYY-MM-DD>

## Scope and threat model
- Assets:
- Actors:
- Trust boundaries:
- Environments inspected:

## Authentication and authorization model
| Control | Observed behavior | Evidence | Verdict |
|---|---|---|---|

## RLS / database authorization matrix
| Object | Operation | Policy / role | Enforced server-side? | Evidence |
|---|---|---|---|---|

## Wails IPC surface
| Binding | Privilege | Validation | Authorization | Risk |
|---|---|---|---|---|

## Findings
| ID | Severity | Confidence | Finding | Evidence | Impact | Next action |
|---|---|---|---|---|---|---|

## Secrets and sensitive-data handling
| Location | Type | Exposure | Evidence | Action |
|---|---|---|---|---|

## Update security
## Open questions / live-environment checks
```

Use `BUG-SEC-<NNN>` for confirmed defects, `RISK-SEC-<NNN>` for risks, and `QUES-SEC-<NNN>` for unknowns. Do not reuse Android `NCC-*` or `NSC-*` IDs; cross-reference them instead.

## Stop conditions

Stop and report when:

- A finding requires a live production query, credentialed access, or an exploit against a shared service.
- A secret is found; do not reproduce it or continue using it.
- RLS cannot be verified because migrations are missing and no safe local database is available.
- The review would require modifying policies, data, or configuration.
- The trust boundary or affected principal cannot be established.

## Handoff

- `api-database-documenter` — document verified schema, policies, and RPCs.
- `bug-and-debt-tracker` — register confirmed findings and accepted risks.
- `test-strategy-planner` — design RLS, IPC, and auth regression tests.
- `implementation-planner` — sequence approved remediation.
- `documentation-sync` — correct inaccurate security documentation.

## Guardrails

- Never paste secrets, credentials, or identifiable patient data into outputs; never modify production data.

- Read-only. Do not alter migrations, policies, secrets, auth settings, or application code.
- Do not run live exploitation, password attacks, load tests, or production data queries.
- Do not paste credentials or patient data into documentation, issues, or chat.
- Do not label a defense-in-depth gap as an exploitable vulnerability without a concrete path and impact.
- Preserve every pre-existing user change; never reset, clean, or rewrite the worktree.
