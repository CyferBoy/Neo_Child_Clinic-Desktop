---
title: ADR-0009 Inventory and Financial Ledger Integrity
doc_status: proposed
evidence: Android inventory/finance behaviour + Phase 0C exports + target architecture
updated: 2026-10-21
---

# ADR-0009 — Inventory and Financial Ledger Integrity

**Status:** Proposed — awaiting approval.
**Depends on:** [ADR-0007](ADR-0007-Money-Dates-and-Identity.md), [ADR-0008](ADR-0008-Shared-Supabase-Backend.md).
**Blocks:** vaccination, inventory, wastage, borrow/return, finance, receipts, reporting, sync.

## Context

A vaccination visit changes stock, money, reminders, and audit state. The Android reference has had historical duplicate-stock and double-payment defects. The 2026-10-21 export reports:

- two triggers on `inventory_transactions` that both call the old `update_batch_stock()` function;
- a migration intended to remove the duplicate that would fail its own guard on the live trigger set;
- broad function execution and table grants, including an anon-executable receipt-number function;
- duplicate unique indexes that make upsert conflict targets ambiguous.

The desktop cannot compensate for a backend that may apply a stock movement twice. This decision defines the integrity contract the desktop and backend must share.

## Decision

1. **One stock ledger path.** Every stock change is an explicit inventory movement linked to a business event. No client writes `vaccine_batches.remaining_quantity` as an independent “adjustment” outside the ledger.
2. **Server remains authoritative for accepted stock.** The desktop may calculate an optimistic local projection, but it reports success only after local validation; it reports stock as acknowledged only after the server accepts the movement.
3. **Idempotent event identity.** Each movement carries a stable event ID generated before the first attempt. Retries and duplicate submissions reuse it. The server must reject or no-op a repeated event rather than applying it again.
4. **Exactly one active stock trigger.** The backend must have one reviewed writer path. Until that is verified, desktop inventory writes are blocked. A migration that drops/replaces triggers must be tested against the complete live trigger set, not only its own precondition guard.
5. **Corrections are linked events.** Editing or deleting a vaccination does not mutate history silently. The system records a linked reversal/correction with the original event identity, actor, reason, and audit record. Stock and money are recomputed from the resulting ledger, not patched by unrelated writes.
6. **No negative stock.** A movement that would make available quantity negative is rejected before commit. Expired batches cannot be consumed clinically.
7. **One income identity per visit.** Vaccination and consultation payment paths must converge on the same income identity. A visit's income is counted once. A split payment creates payment components, not duplicate income.
8. **Money is exact.** Desktop arithmetic is in integer minor units per ADR-0007. The shared `numeric` boundary is converted explicitly and tested, including legacy `Double`-origin values.
9. **Receipts are server-issued.** The client never generates, guesses, or reuses a receipt number. The financial year is derived from the visit date by the server. A provisional local label must be visibly provisional.
10. **Corrections are audited and never hidden.** Refunds, reversals, write-offs, and manual adjustments require an authorized role, a reason, and an audit record. Deleting the original financial row is not an acceptable correction.
11. **Concurrency conflicts are visible.** A stale batch balance, duplicate receipt request, or conflicting payment correction returns a typed conflict. Silent last-write-wins is prohibited.
12. **Reports use the same ledger definitions.** “Income”, “stock on hand”, “wasted”, “borrowed”, and “returned” have one definition shared by dashboard, reports, and detail views.

## Alternatives considered

| Alternative | Assessment |
|---|---|
| Let each screen update batch quantities directly | Causes drift and makes retries non-idempotent; rejected |
| Use last-write-wins for stock/payments | Can lose doses or double-count money; rejected |
| Generate receipt numbers on the client | Collides across devices and breaks audit; rejected |
| Delete/recreate rows to correct a visit | Loses history and can double-apply stock; rejected |
| Treat the local projection as authoritative | Conflicts with the shared backend and multi-device reality; rejected |
| Keep both stock triggers until later | The export reports double application; inventory writes must stay blocked; rejected |

## Consequences

Positive:

- One reproducible stock and money story across Android, desktop, and server.
- Retries and offline replays become safe.
- Reports and receipt audits can be reconciled.

Negative / risks:

- Requires a backend migration and a verified single trigger before desktop inventory work.
- Requires event IDs and correction records in both local and remote schemas.
- Legacy rows may lack clean event identity; a one-time reconciliation may be needed.
- The desktop may show an optimistic stock value that later becomes conflicted.

## Validation

- Replay the same vaccination event 10 times; stock and income change once.
- Insert the same payment from both vaccination and consultation paths; report counts it once.
- Edit a multi-item visit; each batch’s stock and the visit total reconcile.
- Delete/reverse a visit; stock and money reverse exactly once and remain auditable.
- Race two devices for the last dose; one succeeds, one receives a typed conflict.
- Attempt an expired/negative/over-return movement; it is rejected without partial writes.
- Request receipts at a financial-year boundary; sequence is server-assigned and gap policy is understood.
- Verify the deployed trigger set and function definition before enabling writes.

## Open questions

- What is the canonical event ID format and where is it stored?
- Does the backend expose a transactional RPC for a complete visit, or must the desktop sequence writes? If sequenced, how is partial failure recovered?
- Which role may issue refunds/write-offs, and what approval threshold applies?
- What is the receipt gap policy on failed prints or cancelled visits?
- How are legacy rows without event IDs reconciled?
- Is a stock movement ever allowed to be edited, or only reversed?

## Related

[[Decisions/README|Decision Log]] · [[Features/05-Vaccination-Management|Vaccination Management]] · [[Features/07-Vaccine-and-Batch-Inventory|Vaccine and Batch Inventory]] · [[Features/08-Wastage|Wastage]] · [[Features/09-Borrowed-and-Lent-Vaccines|Borrowed and Lent Vaccines]] · [[Features/12-Finance-and-Payments|Finance and Payments]] · [[Features/13-Receipts-and-Printing|Receipts and Printing]] · [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] · [[Product/Business-Rules|Business Rules]]
