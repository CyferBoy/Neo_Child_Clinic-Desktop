---
title: Decision Log
doc_status: baseline
evidence: project direction + architecture analysis + shared-backend investigation
updated: 2026-10-20
---

# Decision Log

> **ADR-0008 is accepted by explicit user direction.** The desktop must reuse the existing Supabase project and schema. All other ADRs below remain proposals for review; they must be compatible with ADR-0008.

## Status vocabulary

| Status | Meaning |
|---|---|
| Proposed | Drafted, not approved |
| Accepted | Approved and binding |
| Superseded | Replaced by a later ADR |
| Rejected | Considered and not adopted |

## Index

| ADR | Decision | Status |
|---|---|---|
| [[Decisions/ADR-0001-Desktop-Stack|ADR-0001]] | Go + Wails + React/TypeScript + Supabase | Proposed (stack fixed by project direction; details open) |
| [[Decisions/ADR-0002-Local-Persistence|ADR-0002]] | SQLite local working copy | Proposed |
| [[Decisions/ADR-0003-Offline-Sync|ADR-0003]] | Outbox + transaction groups + deletion reconciliation (contract TBD) | Proposed |
| [[Decisions/ADR-0004-Authentication-and-Session|ADR-0004]] | Supabase Auth in Go; tokens in OS keychain | Proposed |
| [[Decisions/ADR-0005-Wails-Boundary|ADR-0005]] | Typed Go bindings; no direct renderer data access | Proposed |
| [[Decisions/ADR-0006-Testing-and-Release|ADR-0006]] | Layered tests + signed release gates | Proposed |
| [[Decisions/ADR-0007-Money-Dates-and-Identity|ADR-0007]] | Integer money, typed dates, stable IDs | Proposed |
| [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] | Reuse the existing Supabase project and single schema; no new backend | **Accepted** (user direction) |

## Decision process

1. State the problem, constraints, and evidence.
2. List at least two options and the consequences.
3. Identify security, data, and operational impact.
4. Record the decision and owner.
5. Add validation evidence and a review trigger.

## Related

[[Architecture/System-Architecture|System Architecture]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Audits/Risk-Register|Risk Register]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]]
