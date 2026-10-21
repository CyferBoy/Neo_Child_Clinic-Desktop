---
title: Decision Log
doc_status: baseline
evidence: project direction + architecture/security review + Phase 0C exports
updated: 2026-10-21
---

# Decision Log

> **ADR-0008 is accepted by explicit project direction.** The desktop must reuse the existing Supabase project and schema. All other ADRs below are **proposed and awaiting approval**; they must be compatible with ADR-0008 and the security gates.

## Status vocabulary

| Status | Meaning |
|---|---|
| **Proposed — awaiting approval** | Drafted and reviewed enough to request a decision; not binding. |
| **Accepted** | Approved and binding. |
| **Superseded** | Replaced by a later ADR; retained for history. |
| **Rejected** | The whole decision was considered and not adopted. |
| **Deferred** | Decision intentionally postponed; a named prerequisite is missing. |

No ADR is currently `Rejected` or `Superseded`. Rejected alternatives inside individual ADRs are listed in the last table.

## Index

| ADR | Decision | Status | Depends on |
|---|---|---|---|
| [[Decisions/ADR-0001-Desktop-Stack|ADR-0001]] | Go + Wails + React/TypeScript + Supabase | Proposed — awaiting approval (stack fixed by direction; details open) | ADR-0008 |
| [[Decisions/ADR-0002-Local-Persistence|ADR-0002]] | SQLite local working copy, encryption, single writer | Proposed — awaiting approval | ADR-0001, ADR-0008 |
| [[Decisions/ADR-0003-Offline-Sync|ADR-0003]] | Outbox + transaction groups + deletion reconciliation (contract TBD) | Proposed — awaiting approval | ADR-0002, ADR-0007, ADR-0009 |
| [[Decisions/ADR-0004-Authentication-and-Session|ADR-0004]] | Supabase Auth in Go; tokens in OS keychain | Proposed — awaiting approval | ADR-0001, ADR-0008 |
| [[Decisions/ADR-0005-Wails-Boundary|ADR-0005]] | Typed Go bindings; no direct renderer data access | Proposed — awaiting approval | ADR-0001, ADR-0004 |
| [[Decisions/ADR-0006-Testing-and-Release|ADR-0006]] | Layered tests + signed release gates | Proposed — awaiting approval | ADR-0001, ADR-0010 |
| [[Decisions/ADR-0007-Money-Dates-and-Identity|ADR-0007]] | Integer money, typed dates, stable IDs, server receipts | Proposed — awaiting approval | ADR-0008 |
| [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] | Reuse the existing Supabase project and single schema; no new backend | **Accepted** (project direction) | None |
| [[Decisions/ADR-0009-Inventory-and-Financial-Integrity|ADR-0009]] | One stock ledger, idempotent events, one income identity, server receipts | Proposed — awaiting approval | ADR-0007, ADR-0008 |
| [[Decisions/ADR-0010-Backup-and-Restore|ADR-0010]] | Encrypted backup, preview, safety snapshot, atomic restore | Proposed — awaiting approval | ADR-0002, ADR-0004, ADR-0008 |

## Decision coverage

| Required decision area | Primary ADR | Additional authority | State |
|---|---|---|---|
| Desktop stack | ADR-0001 | System Architecture | Proposed |
| Shared Supabase project/schema | ADR-0008 | Shared Backend Investigation | **Accepted** |
| Authentication and role source | ADR-0004 | Security Model | Proposed |
| Local persistence and encryption | ADR-0002 | Privacy and Backup | Proposed |
| Cache ownership/invalidation | ADR-0002 | Cache Strategy | Proposed; no standalone ADR |
| Offline sync, conflicts, deletion | ADR-0003 | Offline and Sync Design | Proposed; deletion contract open |
| Inventory transaction integrity | ADR-0009 | Feature 07, Phase 0C §5.2 | Proposed; backend gate open |
| Financial integrity and receipt numbering | ADR-0007, ADR-0009 | Features 12–13 | Proposed; backend gate open |
| IST / business dates | ADR-0007 | Business Rules BR-08 | Proposed |
| Soft deletion | ADR-0003, ADR-0007 | Business Rules BR-10 | Proposed; contract open |
| Backup and restore | ADR-0010 | Privacy and Backup | Proposed |
| Testing and packaging | ADR-0006 | Test Strategy, Test Case Catalog | Proposed |
| Wails/desktop trust boundary | ADR-0005 | Frontend/Go architecture | Proposed |

## Review queue — awaiting approval

| Order | ADR | Why it must be decided before code |
|---|---|---|
| 1 | ADR-0008 | Already accepted; constrains every other choice. |
| 2 | ADR-0001, ADR-0004, ADR-0005 | The process, identity, and trust boundary determine the first executable spike. |
| 3 | ADR-0002, ADR-0010 | Local PHI, key recovery, and restore safety gate any local data work. |
| 4 | ADR-0007, ADR-0009 | Money/stock/receipt integrity gates clinical and inventory writes. |
| 5 | ADR-0003 | Sync/deletion contract gates any pilot with more than one writer. |
| 6 | ADR-0006 | Release/packaging gates distribution, but not the first local spike. |

## Rejected alternatives

These alternatives are rejected inside their ADRs. Rejecting an alternative is not a decision to implement its opposite without the ADR being accepted.

| Alternative | ADR | Reason |
|---|---|---|
| Direct remote-only client | ADR-0002 | Fails the offline clinical requirement. |
| In-memory or JSON-file local store | ADR-0002 | No durable relational transaction/corruption safety. |
| Per-row sync scheduling / unbounded worker chain | ADR-0003 | Historical sync defects and resource growth. |
| Silent last-write-wins for money/stock/clinical data | ADR-0003, ADR-0009 | Can lose doses, payments, or clinical notes. |
| Service-role key in the desktop client | ADR-0004, ADR-0005 | Bypasses RLS and exposes full backend authority. |
| Renderer direct access to DB/HTTP/tokens | ADR-0005 | Expands the attack surface and bypasses validation. |
| Floating-point money | ADR-0007 | Rounding/equality defects. |
| Device-local business dates | ADR-0007 | Breaks IST due lists and reports. |
| Client-generated receipt numbers | ADR-0007, ADR-0009 | Collisions and audit failure. |
| Direct batch-quantity edits | ADR-0009 | Stock drift and non-idempotent retries. |
| Deleting/recreating rows to correct visits | ADR-0009 | Loses history and can double-apply effects. |
| Plaintext SQLite/JSON backup | ADR-0010 | Exposes PHI at rest. |
| Restore directly into the live database | ADR-0010 | Partial failure destroys the only copy. |

## Decision process

1. State the problem, constraints, and evidence.
2. List at least two options and the consequences.
3. Identify security, data, and operational impact.
4. Record the decision and owner.
5. Add validation evidence and a review trigger.
6. Update this index, [Home](../Home.md), and any dependent spec/link.
7. Do not mark an ADR accepted without an explicit owner decision.

## Related

[[Home]] · [[Architecture/System-Architecture|System Architecture]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Audits/Risk-Register|Risk Register]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Product/Business-Rules|Business Rules]] · [[Security/Security-Model|Security Model]]
