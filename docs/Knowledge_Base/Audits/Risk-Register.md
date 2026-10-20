---
title: Risk Register
doc_status: baseline
evidence: audit findings + Android KB + shared-backend investigation + target architecture
updated: 2026-10-20
---

# Risk Register

> Risks are assessed qualitatively. No probability percentages or delivery dates are invented. Owner is a role, not a named person.

## Scoring

**Likelihood:** Low / Medium / High. **Impact:** Low / Medium / High / Critical. **Severity** is the combination, with clinical safety and data loss weighted highest.

## Register

| ID | Risk | Likelihood | Impact | Severity | Evidence | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| RISK-001 | No desktop source delays all parity work | High | Critical | Critical | AUD-001 | Phase 0 repository and vertical-slice plan | Engineering lead | Open |
| RISK-002 | Clean database cannot be rebuilt | High | Critical | Critical | AUD-004; only 9 creates for 24 tables | Approved baseline-reconciliation test against the existing project; no new backend by default | Backend owner | Open |
| RISK-003 | Live RLS/grants differ from migrations | High | Critical | Critical | AUD-003; NSC-002/NSC-005 | Live policy/grant audit with multiple roles | Security owner | Open |
| RISK-004 | Broad active-staff access exposes PHI | Medium | High | High | NSC-001; single-clinic model | Role-scoped RLS, column grants, audit review | Security owner | Open |
| RISK-005 | Duplicate or corrupt stock movements | High | High | High | Android stock defects; trigger issues | Single ledger path, idempotency, server reconciliation | Inventory owner | Open |
| RISK-006 | Sync retries duplicate payments/visits | High | Critical | Critical | Android sync/retry findings | Stable IDs, transaction groups, replay tests | Sync owner | Open |
| RISK-007 | Deleted rows resurrect on pull | Medium | High | High | Android tombstone findings | Tombstone feed, cursor tests | Sync owner | Open |
| RISK-008 | Stolen laptop exposes local PHI | Medium | Critical | Critical | No desktop encryption decision | OS/local encryption, app lock, keychain | Security owner | Open |
| RISK-009 | Refresh token stolen from renderer | Medium | Critical | Critical | No desktop auth design yet | Tokens only in Go/keychain, CSP, no browser storage | Desktop lead | Open |
| RISK-010 | Receipt numbers duplicated or altered | Medium | High | High | Client must not compute; sequence is server-side | Server RPC, immutable number, duplicate tests | Finance owner | Open |
| RISK-011 | Statistics double-count income | High | High | High | Android `FullReportViewModel` finding | Single canonical payment per visit, aggregation tests | Reporting owner | Open |
| RISK-012 | Backup restore destroys data | Medium | Critical | Critical | Android restore path untested | Preview, safety snapshot, interruption tests | Backup owner | Open |
| RISK-013 | Date/timezone drift changes due lists/reports | High | Medium | High | Android device-vs-IST findings | Typed dates, IST boundaries, fixed clock tests | Domain owner | Open |
| RISK-014 | No automated parity tests | High | High | High | AUD-009 | Test pyramid, golden workflows, CI gate | QA lead | Open |
| RISK-015 | Supply-chain compromise via dependencies/update | Medium | Critical | Critical | No dependency/update policy | Lockfiles, review, signed updates, pinned keys | Security owner | Open |
| RISK-016 | Documentation drifts from implementation | High | Medium | High | AUD-005/AUD-014 | Docs-as-code checks, stable IDs, review gate | Documentation owner | Open |
| RISK-017 | Shared workstation account destroys accountability | Medium | High | High | No deployment decision | Individual accounts, session switch, audit | Operations owner | Open |
| RISK-018 | Printing leaks PHI to spool/shared printer | Medium | High | High | No print design | Explicit preview, secure spool guidance, retention | Operations owner | Open |
| RISK-019 | Desktop connects to the wrong project or creates a parallel backend | Medium | Critical | Critical | CONN-001; actual project identity/config absent; ADR-0008 | Redacted same-project fingerprint test; config review; no new project/database; CI guard | Security owner | Open |
| RISK-020 | Stale CSV drives wrong desktop schema/models | High | High | High | CONN-002; Android CSV 23/361, camelCase waste fields | Use live verified catalog or reviewed baseline; schema-drift tests; do not generate from old CSV | Backend owner | Open |

## Critical-path risks

RISK-001, RISK-002, RISK-003, RISK-006, RISK-008, and RISK-019 must be resolved or explicitly accepted before any production pilot. They are not "implementation details."

## Risk review triggers

- Any schema/RLS migration.
- Any change to auth, sync, stock, payments, receipts, backup, or updates.
- A new operating system or packaging target.
- A new role or permission.
- A security incident or near miss.
- A release candidate.

## Related

[[Audits/Initial-Audit|Initial Audit]] · [[Audits/Technical-Debt|Technical Debt]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Security/Threat-Model|Threat Model]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
