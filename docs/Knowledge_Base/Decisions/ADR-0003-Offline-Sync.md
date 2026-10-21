---
title: ADR-0003 Offline Sync
doc_status: proposed
evidence: Android sync reference + confirmed failure modes
updated: 2026-10-21
---

# ADR-0003 — Offline Sync

**Status:** Proposed — awaiting approval.
**Depends on:** [[Decisions/ADR-0002-Local-Persistence|ADR-0002]], [[Decisions/ADR-0007-Money-Dates-and-Identity|ADR-0007]], [[Decisions/ADR-0009-Inventory-and-Financial-Integrity|ADR-0009]].

## Context

Writes must succeed offline and converge with Android and other desktop clients. The Android reference has a history of confirmed sync defects: a sync waiter that reported success on failure, unbounded work chains, and an unreachable conflict branch. Those three are fixed at `ca4bed4`. The remaining hard problem is that repository evidence contains no server tombstone table or change feed (live status is unverified), so Android cannot observe every hard delete on pull; NCC-023 is re-scoped as an absence-reconciliation gap.

## Decision

Use an **outbox with transaction groups**, stable business IDs, idempotency keys, a pull cursor, an approved deletion/absence reconciliation contract, and explicit conflict states.

Rules:
- Local business write + outbox rows commit atomically.
- A group is acknowledged only when all required members are acknowledged.
- Retries reuse the same identity.
- Pull includes soft-deleted rows where the schema exposes them and advances the cursor only after a local commit. Hard-delete propagation requires an approved contract; repository evidence contains no server tombstone feed; live status is unverified.
- Money, stock, clinical notes, and receipts are never silently last-write-wins.
- Failed groups are visible and repairable; no silent drop.

## Alternatives considered

| Alternative | Assessment |
|---|---|
| Direct write-through only | Fails offline; partial network failures lose work |
| Last-write-wins for everything | Corrupts stock/payments; discards clinical notes |
| Server-only conflict resolution | Still needs client identity and local state |
| Event sourcing for every field | Powerful but too broad for Phase 1 |

## Consequences

Positive:
- Predictable offline behavior.
- Replay-safe writes.
- Deletion behavior is explicit and testable once a contract is approved.
- Conflicts become a product workflow rather than a silent data bug.

Negative / risks:
- More local schema and worker complexity.
- Requires server support for idempotency/unique constraints.
- Conflict UI is additional work.
- A deletion/absence reconciliation contract must be designed, approved, and tested.

## Validation

- Replay duplicate batches; one business event.
- Partial group failure; visible repair, no false ack.
- Delete/pull; no resurrection. This test is blocked until a deletion/absence reconciliation contract is approved.
- Token expiry mid-batch; no duplicate after re-auth.
- Concurrent edits; conflict visible.

## Open questions

- Is there a server-side transaction-group RPC?
- Which deletion/absence reconciliation contract is approved, and what is its retention window?
- Who resolves stock/payment conflicts?
- Are Android clients required to adopt the same semantics?

## Related

[[Architecture/Offline-and-Sync-Design|Offline and Sync Design]] · [[Features/17-Supabase-Sync|Supabase Sync]] · [[Decisions/ADR-0002-Local-Persistence|ADR-0002]] · [[Decisions/ADR-0007-Money-Dates-and-Identity|ADR-0007]] · [[Decisions/ADR-0009-Inventory-and-Financial-Integrity|ADR-0009]] · [[Audits/Risk-Register|Risk Register]]
