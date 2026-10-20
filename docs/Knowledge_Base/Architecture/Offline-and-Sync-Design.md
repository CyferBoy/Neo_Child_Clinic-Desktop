---
title: Offline and Sync Design
doc_status: proposed
evidence: Android offline-first reference + confirmed failure modes
updated: 2026-10-20
---

# Offline and Sync Design

> **Proposed only.** The Android app is the reference for offline-first intent, but its confirmed sync defects are explicit anti-patterns for the desktop. Sync targets the **existing** Supabase project and schema under [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]; it does not create a separate backend.

## Guarantee

A user action that the local domain accepts must be durably committed locally before the UI reports success. Network availability must not decide whether the clinic can record care. Synchronization is a separate, observable process.

## Local transaction and outbox

Every mutating use case runs in one local transaction:
1. Validate domain rules.
2. Write the business rows.
3. Write audit intent.
4. Write outbox rows with a shared `transaction_group_id`.
5. Commit.
6. Return a committed result with `sync_state = pending`.

If step 3, 4, or 5 fails, the business write rolls back. A business row without an outbox row is a data-loss bug.

### Proposed outbox fields

| Field | Purpose |
|---|---|
| `id` | Stable outbox row ID |
| `transaction_group_id` | Groups a logical business event |
| `entity_type` / `entity_id` | Target record |
| `operation` | CREATE, UPDATE, DELETE |
| `payload` | Canonical JSON or a safe reference |
| `base_version` | Version/updated_at observed before write |
| `idempotency_key` | Stable key for retries |
| `attempts` / `next_attempt_at` | Backoff state |
| `status` | PENDING, SYNCING, FAILED, CONFLICT, ACK |
| `last_error_code` / `last_error_message` | Redacted diagnostics |

## Ordering

- Upload within a group in dependency order: parent identity, visit, items, stock movements, payment, receipt link, audit.
- Do not acknowledge a group until every required member is acknowledged.
- If the server rejects one member, mark the group `CONFLICT` or `REPAIRABLE` and surface the exact record. Do not silently retry the whole group with new IDs.
- A failed group must not block unrelated groups indefinitely; use a bounded, observable scheduler.

## Idempotency

- Client-generated UUIDs for business rows.
- Deterministic IDs for singleton rows such as a visit's vaccination income transaction.
- Server-side uniqueness for receipt numbers and other invariants.
- Retries reuse the same payload identity and idempotency key.
- The client treats a duplicate/already-exists response as success **only** when the server row matches the intended business identity.

## Pull and tombstones

- Pull by a monotonic cursor, ordered by `(updated_at, id)`, with a safety overlap window.
- Include deleted rows or a separate tombstone feed. A deleted row must be applied as deleted, not skipped.
- Do not let an older remote `updated_at` overwrite a local unacknowledged write.
- Advance the cursor only after the page is committed locally.
- Detect schema drift and stop with a visible error rather than writing unknown shapes.

## Conflict policy

| Data | Proposed policy |
|---|---|
| Patient demographics | Field-aware merge with explicit conflict UI; never silently overwrite a different phone/DOB |
| Clinical note / consultation | Preserve both versions; clinician resolves; never discard a note |
| Vaccination event | Immutable event; edits create a linked correction, not an in-place destructive rewrite |
| Stock movement | Append-only ledger; conflict means recompute or manual reconciliation, never overwrite quantity |
| Payment | Immutable/audited correction; no silent amount overwrite |
| Receipt number | Server-assigned, immutable; conflict is a hard error |
| Reminder status | Last intentional transition with audit; terminal states win over stale pending updates |
| Settings | Device-local unless explicitly clinic-wide; clinic-wide changes require admin |

## Authentication and sync

- Refresh tokens before a batch when close to expiry.
- On 401, refresh once; on failure, pause sync and request re-authentication. Do not drop the outbox.
- On 403, classify as permission/RLS failure and surface it; retrying will not fix it.
- On 409/duplicate, reconcile by identity; do not create a new ID.
- On 429/5xx/timeout, retry with exponential backoff and jitter.
- Never log payloads, tokens, or PHI.

## Time

- All reporting and due-date classification uses IST (`Asia/Kolkata`), matching the Android reference.
- The visit date is the user-entered business date, not `now()`.
- Store timestamps with timezone or UTC; display in IST.
- Do not sort formatted date strings.
- Use server time only for metadata and cursor safety, not to rewrite clinical dates.

## Anti-patterns from the reference

The Android Knowledge Base records these confirmed problems; the desktop must not repeat them:
- A sync waiter that discards the failure result and reports success.
- Unbounded work chains created per queued row.
- A conflict branch that is unreachable because status is committed before upload.
- Pull paths that never apply tombstones, allowing deleted rows to resurrect.
- A single stock deduction applied through multiple non-atomic paths.
- Date strings compared lexicographically.
- A destructive restore path with no automated tests.

See Android KB `Offline Synchronization`, `Inventory Management`, and `Backup and Restore` for the evidence.

## Requirements

| ID | Requirement |
|---|---|
| OFF-001 | A local business transaction and its outbox rows commit atomically or not at all. |
| OFF-002 | The UI distinguishes local commit from server acknowledgement. |
| OFF-003 | A retry never creates a duplicate business event. |
| OFF-004 | Deletes propagate as tombstones and cannot resurrect on pull. |
| OFF-005 | Sync failures are visible, classified, and recoverable without data loss. |
| SYNC-001 | A transaction group is acknowledged only when all required members are acknowledged. |
| SYNC-002 | Pull is paged, resumable, schema-checked, and cursor-safe. |
| SYNC-003 | Conflicts on money, stock, clinical notes, and receipts are never silently last-write-wins. |
| SYNC-004 | Auth expiry pauses sync and preserves the outbox. |

## Acceptance

- Kill the network during patient, vaccination, payment, and stock writes; restart; all committed work is present and syncs once.
- Retry the same outbox batch twice; server row counts and amounts are unchanged.
- Delete a row on device A, pull on device B; it stays deleted.
- Edit the same patient on two devices; the conflict is visible and resolvable.
- Expire the token during a batch; re-authenticate; no duplicate rows.
- Simulate a 500 after the server committed; retry is idempotent.

## Open questions

- Is the outbox payload canonical JSON or a typed per-entity record?
- Does the backend expose a transaction-group RPC, or must the client order independent upserts?
- What is the retention window for tombstones?
- How are server-side stock triggers reconciled with client-side stock movements?
- Is multi-workstation conflict resolution a Phase 1 requirement or a Phase 2 hardening item?

## Related

[[Architecture/Data-Flows|Data Flows]] · [[Architecture/Cache-Strategy|Cache Strategy]] · [[Features/17-Supabase-Sync|Supabase Sync]] · [[Audits/Risk-Register|Risk Register]] · [[Decisions/ADR-0003-Offline-Sync|ADR-0003]]
