---
title: Supabase Synchronization
feature_id: SYNC
doc_status: proposed
desktop_status: Missing
android_status: Partially implemented
evidence: Android source + Knowledge Base
updated: 2026-10-20
---

# 17. Supabase Synchronization

> **Desktop status: Missing.** No desktop implementation exists. This is a Phase 1 specification, not a claim of completion.
> **Android reference status:** Partially implemented. Evidence: `feature/sync/`, Android KB `Offline Synchronization`. Historical waiter/work-chain/conflict-branch defects are fixed at `ca4bed4`; NCC-023, NCC-025, and NCC-038 remain open.
>
> **Shared backend:** sync uses the existing Supabase project and schema under [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]; it must not create a separate remote database or duplicate remote tables. Local SQLite is expected.

**Requirement IDs:** `SYNC-001`, `SYNC-002`, `SYNC-003`, `SYNC-004`, `SYNC-005`, `SYNC-006`, `SYNC-007`

## 1. Purpose and scope

Converge local writes with Supabase safely: outbox groups, idempotent uploads, paged pulls, an approved deletion/absence contract, retries, auth handling, and visible conflicts.

## 2. Actors

- All staff
- Admin (sync center)

## 3. Verified reference behavior

The Android reference contains this feature surface. Source inspection and the existing Android Knowledge Base were used to establish the workflows and failure modes. The Android implementation is not re-verified at runtime in this pass. Known reference defects are treated as risks, not copied as requirements.

## 4. Desktop workflows (proposed)

1. Enqueue a local write and show pending status.
2. Upload a transaction group in dependency order.
3. Retry transient failures with backoff.
4. Pull changes by cursor and apply the approved deletion/absence contract; no server tombstone feed is present in repository evidence; live status is unverified.
5. Classify conflicts and surface them for resolution.
6. Pause on auth expiry and resume after re-auth.
7. Show sync counts/errors in a sync center.

## 5. UI states

| State | Expected behavior |
|---|---|
| Idle | All acknowledged. |
| Pending | Count + last attempt. |
| Syncing | Progress, cancel not destructive. |
| Retrying | Backoff explanation. |
| Conflict | Record-level resolution. |
| Auth required | Re-authenticate; outbox intact. |
| Failed | Error code + retry/export. |

## 6. Requirements

| ID | Requirement | Priority |
|---|---|---|
| `SYNC-001` | A transaction group is acknowledged only when all required members are acknowledged. | P0 |
| `SYNC-002` | Every retry is idempotent and cannot duplicate a business event. | P0 |
| `SYNC-003` | Pull is paged, resumable, schema-checked, and cursor-safe. | P0 |
| `SYNC-004` | Deletes propagate through an approved reconciliation contract and cannot resurrect. The contract is unresolved; repository evidence contains no server tombstone feed, and live status is unverified. | P0 |
| `SYNC-005` | Conflicts on money, stock, clinical notes, and receipts are never silently last-write-wins. | P0 |
| `SYNC-006` | Auth expiry pauses sync and preserves the outbox. | P0 |
| `SYNC-007` | Sync failures are visible, classified, and recoverable without data loss. | P0 |

## 7. Validation and business rules

### Validation

- Outbox row has entity, operation, identity, group, idempotency key.
- Payload matches schema.
- Cursor is monotonic.
- No unknown columns.

### Business rules

- No false acknowledgement.
- Upload order follows dependencies.
- A group failure does not spawn new IDs.
- A stale pull does not overwrite an unacknowledged local write.
- The approved deletion/absence contract is applied; no server tombstone feed is present in repository evidence; live status is unverified.
- Receipt/stock conflicts are hard errors.

## 8. Permissions

- All roles sync their own writes.
- Admin can view/resolve sync center; sensitive conflict resolution may require role-specific approval.

## 9. Offline and data behavior

- Sync is the bridge; local writes never wait for it.
- Queue survives restart.
- Backoff is bounded.

## 10. Errors and recovery

- 401 -> pause/re-auth.
- 403 -> permission, no retry.
- 409 -> conflict.
- 429 -> respect Retry-After.
- 5xx/timeout -> retry.
- Schema drift -> stop and report.

## 11. Edge cases

- Server committed but response lost.
- Partial group.
- Duplicate outbox rows.
- Clock skew.
- Huge backlog.
- Deleted parent before child.
- Android/desktop concurrent edits.

## 12. Acceptance criteria

- [ ] Replay creates one event.
- [ ] Partial group is visible and repairable.
- [ ] Delete stays deleted.
- [ ] Auth expiry preserves queue.
- [ ] Conflict resolution is explicit.
- [ ] Sync center counts match DB.

## 13. Test notes

- Chaos suite: 401/403/409/429/500/timeout/duplicate/partial.
- Integration: outbox/cursor/deletion reconciliation (requires an approved contract).
- E2E: offline then reconnect.
- Security: RLS on sync calls.

No desktop test exists yet. Android tests were not run in this pass. See [[Testing/Test-Strategy|Test Strategy]].

## 14. Dependencies

- [[Architecture/Offline-and-Sync-Design|Offline and Sync]]
- [[Decisions/ADR-0003-Offline-Sync|ADR-0003]]
- [[Features/16-Local-Persistence-and-Offline-Operation|Local Persistence]]

## 15. Open questions

- Is there a server transaction-group RPC?
- Which deletion/absence reconciliation contract is approved, and what retention window applies?
- Who resolves stock/payment conflicts?
- Must Android adopt the same outbox semantics?

## 16. Related

- [[Audits/Risk-Register|Risk Register]]
- [[Features/18-Backup-and-Recovery|Backup]]

---

**Evidence boundary:** This specification is source-backed for the Android reference and explicitly proposed for desktop. It must be reviewed and accepted before implementation. See [[Audits/Initial-Audit|Initial Audit]].
