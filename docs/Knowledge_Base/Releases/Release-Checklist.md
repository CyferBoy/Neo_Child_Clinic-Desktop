---
title: Release Checklist
doc_status: template
evidence: release risk + architecture
updated: 2026-10-20
---

# Release Checklist

> **Template only. Not executed.** No desktop build exists. Do not mark an item complete without attached evidence.

## Release identity

- [ ] Version and build number assigned.
- [ ] Git commit/tag recorded.
- [ ] Release notes drafted.
- [ ] Supported OS/architecture matrix confirmed.
- [ ] Rollback version identified and available.

## Build and supply chain

- [ ] Clean build from a clean clone.
- [ ] Dependencies locked; no unexpected updates.
- [ ] Dependency/security scan reviewed.
- [ ] Binary and installer signed.
- [ ] Update manifest signed; signature verified by the app.
- [ ] Version monotonicity checked.
- [ ] No secrets or debug endpoints in the build.

## Security

- [ ] Same-project fingerprint matches Android; no new project, separate remote PostgreSQL database, or parallel remote schema. Local SQLite is expected.
- [ ] RLS suite green with multiple roles and a deactivated account through the approved path.
- [ ] No service-role/database credential in the client.
- [ ] Renderer contains no tokens or PHI in storage/URLs.
- [ ] Local DB encryption/keychain verified.
- [ ] Logs/crash reports redacted.
- [ ] Threat model reviewed for changed surfaces.
- [ ] Open critical/high findings closed or approved exception.

## Data and sync

- [ ] Existing-project baseline/reconciliation evidence reviewed; no parallel schema.
- [ ] Schema drift check passed.
- [ ] Cross-client Android/desktop read/write test passed without duplicates.
- [ ] Outbox/transaction-group replay test passed.
- [ ] Deletion/absence reconciliation test passed; the contract is approved.
- [ ] Conflict handling tested for patient/payment/stock/note.
- [ ] Receipt sequence test passed.
- [ ] Stock ledger reconciliation passed.
- [ ] Backup export/restore/interruption test passed.
- [ ] Soft-delete/report filters verified.

## Functional acceptance

- [ ] All 22 module specs have acceptance evidence.
- [ ] Patient registration/search/detail/merge.
- [ ] Vaccination + stock + reminder + payment + receipt.
- [ ] Consultation + follow-up + payment.
- [ ] Inventory/waste/borrow/return.
- [ ] Dashboard/reports against golden data.
- [ ] Audit append-only and actor attribution.
- [ ] Settings/notifications/update behavior.

## UX and accessibility

- [ ] Keyboard-only core workflow.
- [ ] Focus/error announcements.
- [ ] Empty/loading/offline/error/permission states reviewed.
- [ ] Destructive confirmations and restore preview.
- [ ] No PHI in window title/notification preview.
- [ ] Print preview checked; spool/temp handling documented.

## Operations

- [ ] Clinic pilot owner identified.
- [ ] Staff training/quick reference ready.
- [ ] Support escalation and diagnostic export documented.
- [ ] Backup/restore runbook and passphrase custody.
- [ ] Rollback rehearsal passed.
- [ ] Monitoring/alerts for sync failures and DB integrity.
- [ ] Privacy/retention approval recorded.

## Sign-off

| Role | Name | Evidence | Date |
|---|---|---|---|
| Engineering lead | | | |
| Security owner | | | |
| Clinical owner | | | |
| Operations owner | | | |
| Product owner | | | |

## Post-release

- [ ] Smoke test on a real clinic workstation.
- [ ] Verify sync with an Android client.
- [ ] Verify receipt print.
- [ ] Monitor errors/sync for the agreed pilot window.
- [ ] Record incidents and rollback trigger.

## Related

[[Testing/Test-Strategy|Test Strategy]] · [[Roadmap/Phase-1-Implementation-Plan|Phase 1 Plan]] · [[Security/Security-Model|Security Model]] · [[Audits/Risk-Register|Risk Register]]
