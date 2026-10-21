---
title: Desktop Roadmap
doc_status: proposed
evidence: audit + Android feature footprint + target architecture + documentation completion review
updated: 2026-10-21
---

# Desktop Roadmap

> **No dates and no delivery estimates are asserted.** The desktop has no code, so desktop effort cannot be evidence-based yet. "Reference footprint" is the Android feature package file count, used only to show relative surface area.
>
> **Accepted constraint:** the desktop reuses the existing Supabase project and schema under [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]. Do not create a new project, separate remote PostgreSQL database, duplicate remote tables, or parallel remote schema; local SQLite is expected.

## Prioritization

| Priority | Meaning |
|---|---|
| P0 | Required to protect patient safety, money, identity, or security; blocks a pilot |
| P1 | Required for the Phase 1 clinic workflow |
| P2 | Operational completeness or quality; can follow a controlled pilot |
| P3 | Enhancement or scale work; not Phase 1 |

Ordering principle: **security and data integrity before workflow breadth, workflow breadth before reporting polish.**

## Phase 0 — Audit and readiness (P0)

Exit criteria are verifiable outcomes, not elapsed time.

| Work item | Deliverable | Exit criterion | Depends on |
|---|---|---|---|
| Repository and documentation | Existing desktop Git repository and documentation baseline; future `AGENTS.md`, CI, issue/PR templates, and branch protection require separate approval | Docs links/validation pass; no application build is claimed; future configuration is explicitly gated | Git repository initialized |
| Toolchain | Pinned Go, Wails, Node/package manager, linter, formatter | Reproducible build on a clean machine | Repo |
| CI | Build, lint, unit tests, docs validation, dependency scan | CI required on every change | Toolchain |
| Shared-backend verification | Approved non-destructive access path to the **existing** Supabase project; test-account and synthetic-data protocol | Same project identity proven by a redacted fingerprint; no new backend; no production data mutation | Security approval |
| Schema baseline | Reviewed baseline migration + live catalog/grants/policies snapshot | Baseline reconciliation evidence; RLS suite runs; no parallel schema | Shared-backend verification |
| ADRs | Stack, local persistence, sync, auth, Wails boundary, money/date, inventory/financial integrity, backup/restore, testing/release | All ADRs reviewed; statuses recorded; ADR-0008 remains accepted; others awaiting approval | Architecture review |
| Auth spike | Login, refresh, revoke, role claim, inactive account | Works offline cold start and online refresh against the existing project | Shared-backend verification |
| Local DB spike | SQLite, migrations, WAL, transaction/outbox | Kill/restart preserves committed data | ADR-0002 |
| Sync contract | Outbox/group/idempotency/deletion-reconciliation design | Replay and duplicate tests pass; deletion contract approved and tested on a spike | ADR-0003 |
| Test harness | Go/React/integration/E2E skeletons | A failing test blocks CI | CI |
| Threat model | Reviewed threats and controls | P0 threats have tests or accepted controls | Architecture |

**Backend rule:** ADR-0008 forbids creating a new Supabase project or separate remote PostgreSQL database. The verification row must use the existing project, test accounts, and synthetic/reversible data unless a separate harness is explicitly approved. A separate harness must never become the desktop backend, and local SQLite remains expected.

**Phase 0 is not done while the schema cannot be rebuilt or RLS cannot be tested.** The documentation review is complete; live backend verification and remediation remain deferred to a separate phase.

## Phase 1 — Desktop foundation and core feature parity (P0/P1)

| Wave | Modules | Priority | Value | Reference footprint | Key dependencies | Main risk | Acceptance gate | Effort |
|---|---|---|---|---|---|---|---|---|
| A. Shell | Desktop shell, auth, staff/roles, settings | P0 | Safe sign-in, navigation, administration | 5+2+7+13 files | Auth spike, RLS | Token/role handling | Login/logout/role tests; inactive account blocked | Not estimated |
| B. Identity + core | Patients, dashboard | P0 | Find and register patients; see the day | 25+12 files | Shell, local DB | Duplicate identity, stale history | Create/search/edit/merge tests; offline read | Not estimated |
| C. Clinical | Vaccinations, inventory, reminders, personal reminders | P0 | Record care and protect stock | 11+16+12+8 files | Patients, local DB, sync contract | Stock/idempotency, due dates | Vaccination transaction replay; stock reconciliation; due-list clock tests | Not estimated |
| D. Revenue | Consultations, finance, receipts | P0 | Complete the visit and collect payment | 5+9+receipt code | Clinical, server receipt numbering | Double-count, duplicate receipt | Payment split tests; receipt sequence test; print preview | Not estimated |
| E. Operations | Wastage, borrow/return, audit, notifications, reports | P1/P2 | Reconcile stock, review activity, see trends | 4+8+5+12+23 files | Inventory, clinical, finance | Reporting correctness, audit completeness | Ledger tests; report golden data; audit append-only test | Not estimated |
| F. Resilience | Offline/sync hardening, backup/recovery, updates | P0/P1 | Survive outages and recover | 4+13+7 files | All writes, packaging | Data loss, destructive restore | Chaos sync; restore round-trip; signed update test | Not estimated |

Wave order is a dependency order, not a commitment that all work is sequential. Vertical slices may span waves.

## Phase 1 definition of done

A module is done only when:
1. Its specification and requirement IDs are approved.
2. The implementation is merged behind a feature flag or in a controlled build.
3. Unit, integration, and relevant E2E checks pass in CI.
4. Authorization is verified for at least the affected roles.
5. Offline behavior and sync state are verified.
6. Error states, empty states, and destructive confirmations are reviewed.
7. Accessibility and keyboard paths are checked.
8. Audit events are emitted where required.
9. Documentation and traceability are updated.
10. A manual acceptance record exists with evidence.

## Phase 2 — Reliability and desktop productivity (P1)

- Multi-workstation conflict drills and repair tooling.
- Performance under clinic-sized data and slow disks.
- Full accessibility audit.
- Localization if required.
- Report export/print formats approved by the clinic.
- Backup retention and restore drills.
- Observability dashboards and redacted diagnostics.
- Packaging for all target OSes; code signing; rollback rehearsal.
- Security review and penetration test.
- Data migration/backfill runbook if existing local data must move.

## Phase 3 — Future enhancements (approval required; P2/P3)

> **No Phase 3 item is approved.** This list is a candidate register only. Each item requires an explicit owner decision, a security/privacy review, and a specification before it can enter a delivery phase. It is not committed scope.

- Additional reports and trend analysis.
- Deeper inventory forecasting.
- Configurable workflow templates.
- Optional local-network sync or kiosk mode.
- Integrations approved by the clinic (printing hardware, messaging, accounting).
- Multi-clinic support only with a new tenancy/security design.

Not in Phase 1: patient portal, telemedicine, insurance, payroll, tax filing.

## Status

| Phase | Status |
|---|---|
| Phase 0 | Documentation review complete; live verification/remediation deferred; implementation gates open |
| Phase 1 | 22 specifications drafted; implementation missing |
| Phase 2 | Proposed; blocked by Phase 1 and pilot evidence |
| Phase 3 | Candidate only; none approved |

## Related

[[Roadmap/Phase-1-Implementation-Plan|Phase 1 Implementation Plan]] · [[Roadmap/Dependencies-and-Milestones|Dependencies and Milestones]] · [[Roadmap/Requirements-Traceability|Requirements Traceability]] · [[Testing/Test-Case-Catalog|Test Case Catalog]] · [[Audits/Performance-Review|Performance Review]] · [[Audits/Documentation-Completion-Report|Documentation Completion Report]] · [[Audits/Risk-Register|Risk Register]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
