---
title: ADR-0001 Desktop Stack
doc_status: proposed
evidence: explicit project direction
updated: 2026-10-20
---

# ADR-0001 — Desktop Stack

**Status:** Proposed — awaiting approval. The high-level stack is fixed by project direction; version and library choices remain open.

## Context

The clinic needs a desktop client for an existing Supabase-backed clinic system. The Android app is the functional reference. The team has selected Go, Wails, React + TypeScript, Supabase Auth/PostgreSQL/RLS, local persistence, caching, and offline-first sync.

## Decision

Use:
- **Go** for the trusted application core.
- **Wails** for the desktop shell and typed Go↔React bindings.
- **React + TypeScript** for the renderer.
- **Supabase Auth/PostgreSQL/RLS** as the shared identity and data authority.
- A **local working database** and **outbox** for offline operation.
- **No service-role key** in the client.

## Alternatives considered

| Alternative | Why not selected |
|---|---|
| Electron + Node | Larger runtime and a second trusted-language boundary; project direction is Go/Wails |
| Native per-OS UI | Higher cost across targets; slower parity |
| Web-only SPA | No local privileged database/printing/update control; offline is weaker |
| Flutter desktop | Not the selected stack; different team/tooling |
| Direct renderer→Supabase | Exposes tokens and bypasses the trusted validation boundary |

## Consequences

Positive:
- One trusted Go core for validation, local DB, sync, printing, and updates.
- React ecosystem for accessible, keyboard-efficient UI.
- Supabase reuse preserves identity and RLS investment.

Negative / risks:
- Wails version and packaging maturity must be validated.
- Go/React contract discipline is required.
- Desktop OS printing/update differences add work.
- The team must own a local database and sync engine, not just a UI.

## Validation

- Phase 0 spike builds a signed/packageable Wails app on each target OS.
- Typed bindings reject malformed input and never expose tokens/DB handles.
- A local write + offline sync spike passes.

## Open questions

- Wails v2 or v3?
- Supported OS matrix and architectures?
- Package manager/build pipeline?
- Is a shared design system with Android required?

## Related

[[Architecture/System-Architecture|System Architecture]] · [[Decisions/ADR-0002-Local-Persistence|ADR-0002]] · [[Decisions/ADR-0005-Wails-Boundary|ADR-0005]]
