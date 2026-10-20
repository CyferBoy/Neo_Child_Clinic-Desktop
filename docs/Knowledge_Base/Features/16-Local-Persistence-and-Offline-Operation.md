---
title: Local Persistence and Offline Operation
feature_id: OFF
doc_status: proposed
desktop_status: Missing
android_status: Partially implemented
evidence: Android source + Knowledge Base
updated: 2026-10-20
---

# 16. Local Persistence and Offline Operation

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Partially implemented. Evidence: `data/local/`, Android KB `Offline-First Architecture`, `Room Database`. Open gaps include NCC-039 (duplicate database singleton) and the unresolved deletion contract at the sync boundary; historical cache-staleness wording was not supported by current source.

**Requirement IDs:** `OFF-001`, `OFF-002`, `OFF-003`, `OFF-004`, `OFF-005`, `OFF-006`

## 1. Purpose and scope

Provide durable local storage, transactional writes, schema migrations, encryption, and recovery so clinical work continues without a network.

## 2. Actors

- All staff
- Support/admin

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Open the local DB and apply migrations.
2. Read/write business data offline.
3. Commit a business transaction plus outbox atomically.
4. Restart after crash and recover committed state.
5. Handle disk full, corruption, or failed migration.
6. Lock/clear PHI on sign-out or idle.

## 5. UI states

| State | Expected behavior |
|---|---|
| Opening | DB/migration progress. |
| Ready | Normal local-first operation. |
| Offline | Local reads/writes; sync paused. |
| Migration | Blocking progress; no partial writes. |
| Disk full | Stop writes; preserve data; recovery actions. |
| Corrupt | Safe recovery/export; no silent reset. |
| Locked | PHI hidden; re-auth. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `OFF-001` | A business write and its outbox rows commit atomically or not at all. | P0 |
| `OFF-002` | The local DB is encrypted at rest and the key is protected by the OS keychain. | P0 |
| `OFF-003` | Local schema migrations are versioned, tested, and fail safely. | P0 |
| `OFF-004` | A crash/restart preserves committed data and never reports a partial write as success. | P0 |
| `OFF-005` | Local reads remain available offline; writes that cannot be accepted show a clear error. | P0 |
| `OFF-006` | PHI is cleared from caches on logout/lock/account switch. | P0 |

## 7. Validation and business rules

### Validation

- Schema version known.
- Required fields/constraints enforced locally.
- No write without an outbox row for syncable entities.
- Encryption/key present before PHI load.

### Business rules

- Local DB is the working copy; server is shared authority.
- One writer.
- No raw DB access from renderer.
- A local commit is not a cloud acknowledgement.
- Migrations are forward-only with a tested recovery.

## 8. Permissions

- Only the Go core accesses the DB.
- Support cannot browse PHI without an approved, audited flow.

## 9. Offline and data behavior

- This module defines offline behavior.
- Sync is separate and observable.

## 10. Errors and recovery

- DB locked -> retry/backoff.
- Disk full -> stop writes.
- Corrupt -> integrity check/export.
- Migration fail -> restore old version.

## 11. Edge cases

- Power loss during commit.
- OS update.
- Multiple app instances.
- Clock change.
- Large DB.
- Keychain loss.

## 12. Acceptance criteria

- [ ] Kill during write -> no partial business row.
- [ ] Restart -> committed data present.
- [ ] Disk full -> no corruption.
- [ ] Migration fail -> old DB intact.
- [ ] No plaintext PHI in local files.
- [ ] Logout clears PHI.

## 13. Test notes

- Integration: transactions/crash/migration.
- Security: encryption/keychain.
- Fault: disk full/corruption.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

## 14. Dependencies

- [[Decisions/ADR-0002-Local-Persistence|ADR-0002]]
- [[Features/17-Supabase-Sync|Sync]]

## 15. Open questions

- Encryption approach?
- Key recovery?
- Local schema ownership?
- Portable mode?

## 16. Related

- [[Architecture/Go-Backend-Architecture|Go Backend]]
- [[Security/Privacy-and-Backup|Privacy]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
