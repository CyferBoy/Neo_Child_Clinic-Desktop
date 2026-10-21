---
title: Backup and Recovery
feature_id: BAK
doc_status: proposed
desktop_status: Missing
android_status: Partially implemented
evidence: Android source + Knowledge Base + Phase 0C export metadata
updated: 2026-10-21
---

# 18. Backup and Recovery

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Partially implemented. Evidence: `data/backup/`, Android KB `Backup and Restore`. The restore path is destructive and lacks an end-to-end automated test; crypto and validation helpers do have unit tests, and NCC-037's TOCTOU issue is fixed.

**Requirement IDs:** `BAK-001`, `BAK-002`, `BAK-003`, `BAK-004`, `BAK-005`, `BAK-006`

## 1. Purpose and scope

Export an encrypted clinical backup and restore it safely with preview, integrity checks, a safety snapshot, and post-restore reconciliation.

### User stories

- As an admin, I can export an encrypted backup and preview a restore before applying it.
- As an admin, I can interrupt a restore and keep the previous database intact.

## 2. Actors

- Admin

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Export a backup with a passphrase.
2. Preview a backup's manifest/counts.
3. Restore with explicit destructive confirmation.
4. Create a safety snapshot before restore.
5. Reconcile sync state after restore.
6. Handle wrong passphrase, tamper, disk full, interruption.

## 5. UI states

| State | Expected behavior |
|---|---|
| Exporting | Progress; passphrase; no plaintext temp. |
| Exported | Path, checksum, counts. |
| Preview | Counts, version, conflicts, warning. |
| Restoring | Blocking; progress; do not close. |
| Restored | Reconciliation summary. |
| Failed | Safety snapshot preserved; recovery. |
| Wrong passphrase | No data change. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `BAK-001` | Backups are encrypted and authenticated; no plaintext PHI remains in temp files. | P0 |
| `BAK-002` | Restore requires a fresh authorized session, preview, passphrase, and explicit destructive confirmation; a different account/clinic requires an audited rebind. | P0 |
| `BAK-003` | A safety snapshot is created and remains recoverable if restore fails. | P0 |
| `BAK-004` | Restore is atomic; interruption does not leave a half-restored DB. | P0 |
| `BAK-005` | Backup excludes secrets/tokens/caches and records schema/app versions. | P0 |
| `BAK-006` | Post-restore reconciliation detects duplicates/conflicts and audits the restore. | P1 |

## 7. Validation and business rules

### Validation

- Passphrase strength policy.
- File manifest/checksum.
- Schema/app version compatibility.
- Account/clinic binding.
- Enough disk space.

### Business rules

- Backup is PHI.
- Restore is destructive and admin-only.
- No automatic cloud upload.
- Never restore into a different account without explicit binding.
- Audit export/restore.
- Do not restore secrets.

## 8. Permissions

- Admin only.
- Support cannot restore without an approved, audited procedure.

## 9. Offline and data behavior

- Export/restore local.
- Post-restore sync requires network; reconciliation queue.

## 10. Errors and recovery

- Wrong passphrase -> no change.
- Tamper -> reject.
- Interrupted -> safety snapshot.
- Disk full -> abort before write.
- Version mismatch -> block/upgrade path.

## 11. Edge cases

- Cross-version restore.
- Cross-account restore.
- Large DB.
- Corrupt backup.
- Restore while sync pending.
- Passphrase loss.

## 12. Acceptance criteria

- [ ] Round-trip counts/amounts match.
- [ ] Tamper rejected.
- [ ] Interruption leaves previous DB.
- [ ] No plaintext temp.
- [ ] Audit record exists.
- [ ] Restore does not duplicate synced rows.

## 13. Test notes

- CLI/integration: export/import/tamper/interruption.
- Security: temp/log inspection.
- E2E: preview/confirm/restore.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

Planned test cases: [[Testing/Test-Case-Catalog|Test Case Catalog]] (`TC-BAK-*`). No test is implemented or executed.

## 14. Dependencies

- [[Features/16-Local-Persistence-and-Offline-Operation|Local Persistence]]
- [[Security/Privacy-and-Backup|Privacy and Backup]]

### Database dependencies

`[REPORTED]` The following table names are reported by the 2026-10-21 metadata export or migration evidence; live access is not verified. See [[Database/Data-Dictionary|Data Dictionary]].

Local SQLite snapshot, local backup history, and settings. No remote business table is written by backup or restore itself.

## 15. Open questions

- Android/desktop compatibility?
- Retention?
- Passphrase custody/recovery?
- Cloud backup allowed?

## 16. Related

- [[Audits/Risk-Register|Risk Register]]
- [[Releases/Release-Checklist|Release Checklist]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
