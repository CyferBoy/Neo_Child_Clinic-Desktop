---
title: ADR-0010 Backup and Restore
doc_status: proposed
evidence: Android backup implementation + target security review
updated: 2026-10-21
---

# ADR-0010 — Backup and Restore

**Status:** Proposed — awaiting approval.
**Depends on:** [ADR-0002](ADR-0002-Local-Persistence.md), [ADR-0004](ADR-0004-Authentication-and-Session.md), [ADR-0008](ADR-0008-Shared-Supabase-Backend.md).
**Blocks:** backup/recovery, local encryption, pilot release.

## Context

The desktop local database contains PHI, financial records, audit records, and pending offline work. A backup is therefore both a recovery control and a high-risk data export. The Android reference has password-based AES-256-GCM backup, a checksum, a safety snapshot, and a restore path. The desktop has no approved backup format, key-recovery model, retention policy, or restore verification.

Restore is destructive: it replaces local state. A failed or partially applied restore can destroy the only usable copy of unsynced clinical work.

## Decision

1. **Encrypted local store.** The local working database is encrypted at rest with a key protected by the OS keychain. No plaintext PHI in temporary files, crash dumps, or logs.
2. **Versioned, authenticated backup.** A backup has an explicit format version, a manifest, a content checksum, and authenticated encryption. A wrong password, tamper, truncation, unsupported version, or broken relationship fails closed with a typed error.
3. **No silent cloud backup.** Local export is the Phase 1 baseline. Any cloud target requires a separate approved decision, explicit disclosure, and clinic-approved retention.
4. **Account/clinic binding.** A backup is bound to the originating clinic and account context. Restoring into a different clinic/account requires an explicit, audited rebind; it is not a default convenience.
5. **Secrets excluded.** Auth tokens, key material, device tokens, and transient caches are never included. Pending outbox state is included only if its restore semantics are defined; otherwise the UI must warn that unsynced work is not recoverable from the backup.
6. **Preview before restore.** The user sees backup version, creation time, clinic/account binding, row counts, schema version, and warnings before applying. The user must explicitly confirm.
7. **Safety snapshot first.** A local pre-restore snapshot is created and its integrity checked before the destructive step. If the restore fails, the app returns to the snapshot.
8. **Atomic restore.** The restore runs against a new database file or a single transaction, validates relationships and schema version, then swaps atomically. It never leaves a half-restored database as the live file.
9. **Re-authentication and authorization.** Restore requires an authorized role and a fresh authentication check. An expired session cannot restore PHI.
10. **Post-restore reconciliation.** After restore, local caches, search indexes, and sync cursors are rebuilt. The app verifies row counts and key relationships and reports the result. Sync does not start until validation succeeds.
11. **Audit without PHI.** Backup creation, restore preview, restore start/finish/failure, and account rebinding are audited with counts and identifiers, not clinical content.
12. **Retention and deletion.** Backup retention, secure deletion, and off-device handling require an approved policy. A “delete backup” action cannot be claimed secure until the storage medium's behaviour is defined.

## Alternatives considered

| Alternative | Assessment |
|---|---|
| Plain JSON/SQLite copy | PHI at rest and tamper-prone; rejected |
| Cloud backup by default | Adds confidentiality, residency, and retention risk without approval; rejected |
| Restore directly into the live database | Partial failure can destroy the only copy; rejected |
| Trust a checksum alone | Does not provide confidentiality or authentication; rejected |
| Include auth tokens for convenience | Extends credential exposure to backup files; rejected |
| Restore without re-authentication | Anyone at an unlocked workstation could replace PHI; rejected |

## Consequences

Positive:

- Restore is reversible and evidence-producing.
- A stolen backup does not directly expose PHI without the password/key.
- Users can see what will be replaced before committing.

Negative / risks:

- Password/key recovery remains a support burden and must not become a bypass.
- Large backups need streaming and storage headroom.
- Cross-device restore semantics are constrained by account/clinic binding.
- Excluding outbox state can lose pending work; including it requires conflict handling.
- No retention/legal policy is approved yet.

## Validation

- Export with PHI, restore on a clean profile, verify counts, relationships, and audit.
- Tamper with one byte; restore fails before touching live data.
- Wrong password; typed failure, no partial restore.
- Interrupt power during restore; previous database is intact.
- Unsupported future version; fails closed with a clear message.
- Restore into a different account/clinic; blocked unless explicitly rebound and audited.
- Inspect the backup and temp directory; no plaintext PHI or credentials.
- Restore with pending outbox rows; behaviour matches the approved inclusion rule.

## Open questions

- Is the backup password user-supplied, recovery-key-based, or both?
- Is cross-device restore required within one clinic?
- Does a backup include pending outbox work? If yes, how are duplicate server events prevented?
- What retention period and deletion standard apply?
- Is cloud backup in scope at all for Phase 1?
- Who may restore, and does it require a second approver?
- How is a backup from a newer schema handled after downgrade?

## Related

[[Decisions/README|Decision Log]] · [[Features/18-Backup-and-Recovery|Backup and Recovery]] · [[Security/Privacy-and-Backup|Privacy and Backup]] · [[Security/Threat-Model|Threat Model]] · [[Architecture/Android-Reference-Architecture|Android Reference Architecture]] · [[Audits/Performance-Review|Performance Review]] · [[Audits/Risk-Register|Risk Register]]
