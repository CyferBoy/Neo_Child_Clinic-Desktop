---
title: ADR-0003 Offline Sync
doc_status: proposed
evidence: Android sync reference + confirmed failure modes
updated: 2026-10-20
---

# ADR-0003 — Offline Sync

**Status:** Proposed.

## Context

Writes must succeed offline and converge with Android and other desktop clients. The Android reference has confirmed defects: a sync waiter that reports success on failure, unbounded work chains, an unreachable conflict branch, and pull paths that do not apply tombstones.

## Decision

Use an **outbox with transaction groups**, stable business IDs, idempotency keys, a pull cursor, tombstones, and explicit conflict states.

Rules:
- Local business write + outbox rows commit atomically.
- A group is acknowledged only when all required members are acknowledged.
- Retries reuse the same identity.
- Pull includes deletes and advances the cursor only after a local commit.
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
- Deletes propagate correctly.
- Conflicts become a product workflow rather than a silent data bug.

Negative / risks:
- More local schema and worker complexity.
- Requires server support for idempotency/unique constraints.
- Conflict UI is additional work.
- Tombstone retention must be designed.

## Validation

- Replay duplicate batches; one business event.
- Partial group failure; visible repair, no false ack.
- Delete/pull; no resurrection.
- Token expiry mid-batch; no duplicate after re-auth.
- Concurrent edits; conflict visible.

## Open questions

- Is there a server-side transaction-group RPC?
- Tombstone retention window?
- Who resolves stock/payment conflicts?
- Are Android clients required to adopt the same semantics?

## Related

[[Architecture/Offline-and-Sync-Design|Offline and Sync Design]] · [[Features/17-Supabase-Sync|Supabase Sync]] · [[Audits/Risk-Register|Risk Register]]
