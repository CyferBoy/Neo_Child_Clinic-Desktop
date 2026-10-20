---
title: Android-Desktop Parity
doc_status: baseline
evidence: Android source + desktop filesystem inspection
updated: 2026-10-20
---

# Android-Desktop Parity

> **Result: 0 of 22 desktop modules have verified parity.** The desktop project has no application source. Every gap below is therefore a missing implementation, not a behavioural difference to debug.

## Method

1. Enumerated the Android feature packages and the 22 Phase 1 modules requested for desktop.
2. Read the Android source and existing Knowledge Base for each module's actual workflow.
3. Searched the desktop project for Go, Wails, React, TypeScript, package, test, and configuration files.
4. Classified Android reference status conservatively: source presence is not runtime verification.
5. Recorded the desktop target behavior as a proposed specification, not as an implemented feature.

**Desktop filesystem evidence** `[VERIFIED]`: at audit time the only files under `/storage/emulated/0/Neo_Child_Clinic_Desktop` were `.opencode/skills/**` (17 `SKILL.md` files) and the user-supplied `Supabase Snippet List Public Table Columns.csv`. A Git repository has since been initialized and pushed, but there is still no `go.mod`, `wails.json`, `package.json`, `src/`, `app/`, test suite, or CI configuration.

## Parity matrix

| Module | Android reference | Desktop | Parity | Main gap / risk |
|---|---|---|---|---|
| Desktop shell | Unverified | Missing | Gap | No shell, routing, window, or sync-status surface |
| Authentication | Unverified | Missing | Gap | No session, token storage, role claim handling, or lock screen |
| Staff/roles | Unverified | Missing | Gap | No account lifecycle or role administration |
| Patients | Unverified | Missing | Gap | Historical validation defects fixed; no supported stale-history defect remains; runtime unverified |
| Vaccinations | Unverified | Missing | Gap | Historical stock/retry defects fixed; runtime unverified |
| Consultations | Unverified | Missing | Gap | No clinical note or linked payment workflow |
| Inventory | Partially implemented | Missing | Gap | Historical sorting/lost-update/trigger defects fixed; NCC-027/NCC-030 low-severity gaps remain |
| Wastage | Unverified | Missing | Gap | No waste ledger or stock reconciliation |
| Borrow/return | Unverified | Missing | Gap | No batch-linked borrow/return lifecycle |
| Vaccination reminders | Partially implemented | Missing | Gap | Historical timezone/notification defects fixed; no deletion/absence contract (NCC-023) |
| Personal reminders | Unverified | Missing | Gap | NCC-034 reclassified as not a bug; no desktop reminder model |
| Finance/payments | Unverified | Missing | Gap | No income/expense ledger or payment split |
| Receipts/printing | Unverified | Missing | Gap | No server receipt number integration or desktop print path |
| Dashboard | Unverified | Missing | Gap | No today view, counts, or alert surface |
| Statistics/reports | Unverified | Missing | Gap | Historical income double-count/filter defects fixed; runtime unverified |
| Local persistence | Partially implemented | Missing | Gap | NCC-039 duplicate singleton; no deletion contract at sync boundary |
| Supabase sync | Partially implemented | Missing | Gap | Historical waiter/chain/conflict defects fixed; NCC-023/025/038 remain open |
| Backup/recovery | Partially implemented | Missing | Gap | Destructive restore; no end-to-end test; crypto/validator unit tests exist |
| Notifications | Unverified | Missing | Gap | Historical notification defects fixed; no desktop notification bridge yet |
| Settings | Unverified | Missing | Gap | No local/remote configuration boundary |
| Audit | Unverified | Missing | Gap | No append-only audit writer or viewer |
| Updates | Unverified | Missing | Gap | No packaging, signing, update feed, or rollback |

## Parity rules

- **Behavioural parity** means the same business result, not the same screen layout.
- **Data parity** means the same patient, visit, stock, payment, and audit facts survive a round trip.
- **Offline parity** means the desktop can perform the workflow without a network and reconcile later.
- **Security parity** means the desktop does not weaken RLS, token handling, or auditability.
- **Operational parity** means backups, receipts, updates, and errors are supportable.

## Non-parity that may be acceptable

- Desktop keyboard shortcuts and multi-column layouts replace mobile gestures.
- Desktop notifications replace Android home-screen widgets and push notifications where the workflow allows.
- Desktop printing replaces Android receipt printing.
- Desktop update delivery replaces Play Store distribution.
- Biometric app lock may be replaced by OS session lock and password re-authentication; this requires approval.

## Priority order for closing gaps

1. Trust boundary: auth, RLS verification, local encryption, IPC.
2. Data integrity: patient identity, vaccination transaction, stock ledger, payments, receipts.
3. Offline convergence: outbox, idempotency, approved deletion/absence reconciliation, pull cursor.
4. Recovery: backup/restore, audit, sync error resolution.
5. Reporting and operational polish.

## Related

[[Product/Feature-Inventory|Feature Inventory]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Audits/Risk-Register|Risk Register]] · [[Roadmap/Requirements-Traceability|Requirements Traceability]]
