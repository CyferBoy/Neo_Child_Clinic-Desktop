---
title: Privacy and Backup
doc_status: proposed
evidence: Android backup format + target architecture
updated: 2026-10-20
---

# Privacy and Backup

> **Proposed.** The desktop backup format, retention policy, and privacy controls are not implemented or approved.

## Data classification

| Class | Examples | Handling |
|---|---|---|
| Clinical PHI | Patient identity, DOB, phone, address, notes, vaccinations, consultations, reminders | Encrypt at rest and in backup; least privilege; no logs/telemetry |
| Financial | Payments, expenses, receipt numbers, batch costs | Restricted roles; audit; encrypted backup |
| Staff personal data | Email, phone, employee ID, device token | Restricted profile access; retention policy |
| Security data | Tokens, keys, audit metadata | Keychain/secret storage; no export except redacted diagnostics |
| Operational | Sync counts, error codes, app version | May be logged redacted; no PHI |

## Privacy principles

1. **Collect only what the workflow needs.** Do not add fields because they are easy.
2. **Display only what the role needs.** Broad profile reads are a known reference risk.
3. **Retain only as long as required.** Retention periods need clinic/legal approval; none are invented here.
4. **Export is explicit.** No background upload to personal or shared storage.
5. **Deletion is auditable.** Soft delete preserves referential integrity but must not leave data visible in reports or exports.
6. **Logs are not a shadow record.** Do not duplicate clinical content into logs.
7. **Backups are PHI.** Treat them as a full clinical dataset, not an IT artifact.

## Android reference backup

`[VERIFIED]` The Android backup is an encrypted JSON envelope (`.nccb`) covering 22 Room tables, with a versioned header and a passphrase-derived key. It deliberately excludes `sync_queue`, `widget_due_cache`, and `backup_history`, and strips FCM tokens. The restore path is destructive and uses a safety backup. The Android KB records that the restore path has no automated tests and several crypto/atomicity gaps.

The desktop must not simply copy the Android file format without a compatibility decision. If cross-client restore is required, the format and crypto must be specified and tested. If not, the desktop backup is a separate, documented format.

## Proposed desktop backup design

- **Format:** versioned encrypted container with a manifest, checksums, schema version, app version, clinic/account binding, creation time, and record counts.
- **Crypto:** authenticated encryption; passphrase-derived key using a memory-hard KDF with a random salt; no key reuse; authenticated header.
- **Scope:** business tables plus required reference data; exclude device tokens, sync cursors, transient caches, and secrets.
- **Export:** consistent local snapshot; write to a user-selected path; no plaintext temp file; verify checksum before reporting success.
- **Restore:** preview counts and conflicts; require passphrase and explicit confirmation; create a safety snapshot; restore in one transaction; reconcile sync state; never leave a half-restored DB.
- **Scheduling:** optional local automatic backup with retention; no silent cloud upload.
- **Verification:** restore into a clean environment and compare counts/amounts; test wrong passphrase, truncation, tampering, disk full, and interruption.

## Proposed retention

No durations are asserted. The clinic must approve retention for:
- patient and clinical records;
- financial records and receipts;
- audit logs;
- local device copies;
- backup generations;
- redacted diagnostics.

Until approved, default to minimum operational retention and do not delete data automatically.

## Logging and telemetry

- No PHI, tokens, or full request/response bodies.
- Telemetry is opt-in or contractually approved; default off if uncertain.
- Crash reports must be scrubbed before upload.
- Diagnostic export contains versions, counts, error codes, and redacted metadata only.

## Data subject requests

The desktop must support an authorized export/correction workflow, but deletion may be constrained by clinical/financial retention and referential integrity. Any deletion must be soft-deleted, audited, and excluded from active views; a hard-delete procedure requires legal/clinical approval.

## Backup acceptance

- Export with a strong passphrase; verify no plaintext PHI remains in temp.
- Attempt restore with a wrong passphrase; no data changes.
- Tamper with one byte; restore rejects.
- Interrupt restore; previous database is intact.
- Restore into a clean install; counts and financial totals match the manifest.
- Sign out/switch account; backup is not readable by the other account without the passphrase.

## Open questions

- Is cross-restore between Android and desktop required?
- Who holds the backup passphrase, and what is the recovery procedure?
- Are cloud backups allowed? Under which provider/contract?
- What retention periods and deletion rules apply?
- Is device-level encryption mandated by clinic policy?

## Related

[[Security/Security-Model|Security Model]] · [[Security/Threat-Model|Threat Model]] · [[Features/18-Backup-and-Recovery|Backup and Recovery]] · [[Audits/Risk-Register|Risk Register]]
