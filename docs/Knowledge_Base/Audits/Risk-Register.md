---
title: Risk Register
doc_status: baseline
evidence: audit findings + Android KB + shared-backend investigation + target architecture + Phase 0C Supabase metadata exports (no SQL executed)
updated: 2026-10-21
---

# Risk Register

> Risks are assessed qualitatively. No probability percentages or delivery dates are invented. Owner is a role, not a named person.

## Scoring

**Likelihood:** Low / Medium / High. **Impact:** Low / Medium / High / Critical. **Severity** is the combination, with clinical safety and data loss weighted highest.

## Register

| ID | Risk | Likelihood | Impact | Severity | Evidence | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| RISK-001 | No desktop source delays all parity work | High | Critical | Critical | AUD-001 | Phase 0 repository and vertical-slice plan | Engineering lead | Open |
| RISK-002 | Clean database cannot be rebuilt | High | Critical | Critical | AUD-004; only 9 creates for 24 tables; 15 baseline tables and at least one missing migration (`todo_notification_events`) | Approved baseline-reconciliation test against the existing project; no new backend by default | Backend owner | Open |
| RISK-003 | Live RLS/grants differ from migrations | High | Critical | Critical | AUD-003; NSC-002/NSC-005. **Phase 0C export:** 179 policies; 13 tables retain `{public}` policies; 10 pass for `anon`; `reminders` is `true` for any authenticated user. Runtime not tested. | Confirm with anon/non-staff tests; remove legacy policies; separate table-GRANT and RLS verification | Security owner | Open — evidence narrowed, not closed |
| RISK-004 | Broad active-staff access exposes PHI | Medium | High | High | NSC-001; single-clinic model; exported `profiles`/active-staff reads | Role-scoped RLS, column grants, audit review | Security owner | Open |
| RISK-005 | Duplicate or corrupt stock movements | High | High | High | Historical Android stock defects fixed at `ca4bed4`; current NCC-027/NCC-030 guards remain open. **Phase 0C export:** two stock triggers and the old function body remain live; `20261017` did not take effect and its guard would fail as written. | Single ledger path, idempotency, server reconciliation; do not write inventory until the duplicate is removed and exactly one writer is verified | Inventory owner | Open — inventory writes blocked |
| RISK-006 | Sync retries duplicate payments/visits | High | Critical | Critical | Historical Android sync/retry findings; current NCC-023/025/038 gaps | Stable IDs, transaction groups, replay tests | Sync owner | Open |
| RISK-007 | Deleted rows resurrect on pull | Medium | High | High | NCC-023: repository evidence contains no server tombstone feed; Android pull cannot observe every hard delete; live unverified | Approve deletion/absence reconciliation contract; cursor and cross-client tests | Sync owner | Open |
| RISK-008 | Stolen laptop exposes local PHI | Medium | Critical | Critical | No desktop encryption decision | OS/local encryption, app lock, keychain | Security owner | Open |
| RISK-009 | Refresh token stolen from renderer | Medium | Critical | Critical | No desktop auth design yet | Tokens only in Go/keychain, CSP, no browser storage | Desktop lead | Open |
| RISK-010 | Receipt numbers duplicated or altered | Medium | High | High | Client must not compute; sequence is server-side | Server-assigned immutable sequence, duplicate tests | Finance owner | Open |
| RISK-011 | Statistics double-count income | High | High | High | Historical Android `FullReportViewModel` defect, fixed; regression risk remains | Single canonical payment per visit, aggregation tests | Reporting owner | Open |
| RISK-012 | Backup restore destroys data | Medium | Critical | Critical | Android restore path is destructive and has no end-to-end automated test | Preview, safety snapshot, interruption tests | Backup owner | Open |
| RISK-013 | Date/timezone drift changes due lists/reports | High | Medium | High | Historical Android device-vs-IST defects, fixed; risk remains | Typed dates, IST boundaries, fixed clock tests | Domain owner | Open |
| RISK-014 | No automated parity tests | High | High | High | AUD-009 | Test pyramid, golden workflows, CI gate | QA lead | Open |
| RISK-015 | Supply-chain compromise via dependencies/update | Medium | Critical | Critical | No dependency/update policy | Lockfiles, review, signed updates, pinned keys | Security owner | Open |
| RISK-016 | Documentation drifts from implementation | High | Medium | High | AUD-005/AUD-014 | Docs-as-code checks, stable IDs, review gate | Documentation owner | Open |
| RISK-017 | Shared workstation account destroys accountability | Medium | High | High | No deployment decision | Individual accounts, session switch, audit | Operations owner | Open |
| RISK-018 | Printing leaks PHI to spool/shared printer | Medium | High | High | No print design | Explicit preview, secure spool guidance, retention | Operations owner | Open |
| RISK-019 | Desktop connects to the wrong project or creates a parallel backend | Medium | Critical | Critical | CONN-001; actual project identity/config absent; ADR-0008 | Redacted same-project fingerprint test; config review; no new project or remote database; CI guard | Security owner | Open |
| RISK-020 | Stale CSV or unreviewed export drives wrong desktop schema/models | High | High | High | CONN-002; Android CSV 23/361, camelCase waste fields. Phase 0C exports are coherent but not runtime-certified; six live columns are absent from migrations. | Use the Phase 0C export as `L` evidence only; approve a baseline; do not generate from the old CSV or blindly from migrations; schema-drift tests | Backend owner | Open |
| RISK-021 | Unauthenticated PHI/inventory exposure through the anon key | High | Critical | Critical | SEC-0C-01: `get_my_role()` falls back to `'nurse'`; ten tables have matching `{public}` policies; 22 tables grant anon full table privileges. Logically derived from the export; no HTTP exploit test was run. | Treat as a possible breach until disproved; confirm with synthetic anon-only reads; drop/replace legacy policies and fail closed; verify anon has no business access | Security owner | Open — critical |
| RISK-022 | October 30 Data API change breaks future tables or leaves over-broad access | High | High | High | B-0C-03 / MIG-0C-01; no table-level `GRANT` in any migration; seven business tables rely on platform default ACLs, and `service_role` lacks explicit grants there | Add least-privilege forward grants for the seven tables; re-export default ACLs after 2026-10-30; verify with `has_table_privilege` | Backend owner | Open |
| RISK-023 | Duplicate live stock triggers double-apply each movement | High | Critical | Critical | SEC-0C/MIG-0C-04: `inventory_transactions_update_batch_stock` and `tr_update_batch_stock` both call the old `update_batch_stock()`; the proposed fix cannot pass its own guard. | Do not apply `20261017` unchanged; narrow the guard, remove the legacy trigger, install the corrected function, replay insert/update/delete, and reconcile ledger to physical stock | Inventory owner | Open — blocked |
| RISK-024 | Doctor-slot exception sync fails or writes the wrong contract | High | Medium | High | MIG-0C-11: Android sends `start_minute`/`end_minute`; the reported table has neither, so a custom SLOT upsert can return `PGRST204` | Freeze the desktop contract; add the columns through an approved migration or stop sending them; test exception create/update | Backend/scheduling owner | Open |

## Critical-path risks

RISK-001, RISK-002, RISK-003, RISK-006, RISK-008, RISK-019, RISK-021, and RISK-023 must be resolved or explicitly accepted before any production pilot. RISK-022 and RISK-024 must close before the affected table/write path is enabled. They are not "implementation details."

## Phase 0B gate blockers

These are the evidence/decision gates in [[Audits/Phase-0B-Architecture-Review|Phase 0B Architecture Review]]; they are not new documentation defects.

| ID | Gate blocker | Evidence/action required | Blocking impact | Owner | Acceptance |
|---|---|---|---|---|---|
| P0B-01 | Live database catalog/baseline | Run [[Database/Live-Verification-Queries|read-only catalog/constraint/index export]]; confirm 15 baseline tables and `todo_notification_events` | Wrong models; no reproducible test DB | Backend owner | Live diff reviewed; baseline plan approved |
| P0B-02 | Live RLS/grants/functions/Storage/Realtime | Same read-only export; approved role test or signed limitation acceptance | Cannot certify authorization/PHI isolation | Security owner | Policies/ACLs reconciled; exceptions signed |
| P0B-03 | Stock trigger mode | Prove `update_batch_stock()`/trigger state; choose trigger vs absolute writer | Double-applied or lost stock | Inventory owner | Exactly one writer; replay/concurrency tests pass |
| P0B-04 | Same-project identity | Approved configuration + redacted project fingerprint | Wrong project/parallel backend | Security owner | Same project proven without printing secrets |
| P0B-05 | Deletion/absence contract | Approve D4: soft delete + pull deleted rows, snapshot fallback, no client hard deletes | Resurrection/data loss | Sync owner | Contract + delete/revive tests approved |
| P0B-06 | ADR approvals | Accept/reject D1–D14; ADR-0001–0007 remain proposed; 0008 accepted | Rework and inconsistent clients | User/architecture owner | Decision log updated |
| P0B-07 | Toolchain and CI | Wails/Go/Node smoke build, pinned versions, CI, signed packaging | No verifiable build/release | Engineering lead | Clean build/tests/secret checks pass |
| P0B-08 | Phase 1 scope | Approve the staged pilot slice and exclusions | Scope creep/delayed value | Product/clinic owner | Signed in/out scope + acceptance criteria |
| P0B-09 | Local encryption/backup/retention | Approve D2/D12 and retention; restore drill | PHI exposure/unrecoverable data | Security/clinical owners | Encryption/restore/tamper tests pass |

### Phase 0C gate status update

The Phase 0B gate list is retained as the historical plan. The 2026-10-21 exports narrow several gates but close none completely.

| Gate | Phase 0C status | Remaining evidence/action |
|---|---|---|
| P0B-01 | **PARTIAL — narrowed** | 24 tables/416 columns/77 constraints/93 indexes reported; no project identity, migration history, or `todo_notification_events`; 15 baseline tables still lack `CREATE TABLE`. |
| P0B-02 | **PARTIAL — critical evidence found** | Grants/policies/functions reported; anon path and `reminders` defect identified. Runtime role tests, Storage buckets, Realtime authorization, and post-Oct-30 ACLs remain open. |
| P0B-03 | **EVIDENCE FOUND — not resolved** | The export shows two stock triggers and the old function. The fix migration is not deployed and its guard would fail; do not write inventory. |
| P0B-04 | **OPEN** | No URL/ref/issuer in exports; same-project identity still requires approved config and a redacted fingerprint. |
| P0B-05 | **OPEN** | No deletion/absence contract or tombstone feed evidence. |
| P0B-06 | **OPEN** | ADR-0001–0007 remain proposed; ADR-0008 accepted; D1–D14 still need approval. |
| P0B-07 | **OPEN** | No desktop toolchain/CI/test suite. |
| P0B-08 | **OPEN** | No approved pilot slice or acceptance sign-off. |
| P0B-09 | **OPEN** | No approved encryption, backup, key recovery, or retention decision. |

### Phase 0C implementation blockers

| ID | Blocker | Why it blocks desktop | Evidence |
|---|---|---|---|
| B-0C-01 | Same-project identity unverified | Wrong project/parallel backend | No URL/ref in 16 exports; ADR-0008 |
| B-0C-02 | Critical anon/legacy-policy and role-source exposure | PHI and inventory may be reachable with the public anon key; signup role path unverified | SEC-0C-01..04, SEC-0C-08 |
| B-0C-03 | No explicit grants / Oct 30 gap | Seven migration-created tables may return `42501`; `service_role` path also lacks explicit grants | MIG-0C-01 |
| B-0C-04 | Duplicate stock triggers + old function | Double-applied or lost stock; `20261017` not safely deployable | MIG-0C-04, §5.2 |
| B-0C-05 | No reproducible baseline + six live-only columns | Cannot build a trustworthy test DB or model set | MIG-0C-03/10/12 |
| B-0C-06 | Doctor-slot contract mismatch | Custom SLOT sync can fail with `PGRST204` | MIG-0C-11 |
| B-0C-07 | Storage bucket metadata unverified | Patient-document access cannot be certified | SEC-0C-11 |
| B-0C-08 | Realtime publication over-broad | Desktop subscription design must not assume filtering | SEC-0C-10 |
| B-0C-09 | All 21 functions anon-executable | Receipt sequence burn and stock/rate-limit side effects | SEC-0C-06, SEC-0C-09 |
| B-0C-10 | RLS not forced; owner/service bypass | Desktop must never use service role; role tests required | SEC-0C-12 |

## Risk review triggers

- Any schema/RLS migration.
- Any change to auth, sync, stock, payments, receipts, backup, or updates.
- A new operating system or packaging target.
- A new role or permission.
- A security incident or near miss.
- A release candidate.

## Related

[[Audits/Initial-Audit|Initial Audit]] · [[Audits/Phase-0B-Architecture-Review|Phase 0B Architecture Review]] · [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] · [[Database/Schema-Reconciliation|Schema Reconciliation]] · [[Database/Live-Verification-Queries|Live Verification Queries]] · [[Audits/Technical-Debt|Technical Debt]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Security/Threat-Model|Threat Model]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
