---
title: ADR-0005 Wails Boundary
doc_status: proposed
evidence: Wails project direction + threat model
updated: 2026-10-20
---

# ADR-0005 — Wails Boundary

**Status:** Proposed.

## Context

Wails exposes Go methods to a web renderer. Without a strict contract, the renderer can become an over-privileged client with filesystem, database, or network access.

## Decision

- The renderer calls only explicitly exported, typed Go methods.
- No raw SQL, database handle, filesystem path traversal, shell command, or arbitrary URL fetch is exposed.
- Every method validates input and returns a stable result/error envelope.
- Long operations accept context/cancellation and have timeouts.
- The Go side performs authorization checks and never trusts a renderer-supplied role.
- Binding generation is part of the build; contract drift fails CI.
- No tokens, service-role keys, or secrets cross the boundary.

## Alternatives considered

| Alternative | Assessment |
|---|---|
| Renderer calls Supabase directly | Token exposure, bypass validation; rejected |
| Expose a generic RPC/SQL endpoint | Too broad; injection/privilege risk |
| Embed a local HTTP server | Additional attack surface; not needed for Wails |
| Put all logic in TypeScript | Duplicates trust boundary; weak local DB/printing control |

## Consequences

Positive:
- Narrow attack surface.
- Testable contracts.
- Clear ownership of validation and transactions.

Negative / risks:
- Binding boilerplate.
- Contract versioning during UI changes.
- Debugging across the boundary.

## Validation

- Contract tests for every binding, including malformed input.
- Attempt path traversal, SQL injection, role spoofing, and oversized payloads; all rejected.
- Renderer cannot read tokens/DB files.
- Cancellation/timeout leaves no partial transaction.

## Open questions

- Wails binding generation workflow and version.
- Are streaming subscriptions needed for live query updates?
- How are large exports/backups transferred without blocking the UI?

## Related

[[Architecture/Go-Backend-Architecture|Go Backend]] · [[Architecture/Frontend-Architecture|Frontend]] · [[Security/Threat-Model|Threat Model]]
