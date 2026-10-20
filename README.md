# Neo Child Clinic Desktop

Documentation and implementation workspace for the Neo Child Clinic desktop application.

**Status:** specification and architecture baseline. The desktop application is not implemented yet. This repository contains documentation, design decisions, feature specifications, and supporting evidence; it does not yet contain Go, Wails, React, or TypeScript application source.

## About

Neo Child Clinic Desktop is the planned desktop companion to the Neo Child Clinic Android application. It is intended for clinic staff to manage patient registration, visits, vaccinations, consultations, vaccine inventory, wastage, borrowing, reminders, billing, receipts, reports, audit logging, and offline-first synchronization from a clinic workstation.

The application is planned around **Go + Wails + React + TypeScript**. It must reuse the **existing Supabase project and PostgreSQL schema** used by Android: the same Auth users, tables, RLS policies, Storage buckets, and Edge Functions. It must not create a new backend, a separate database, duplicate tables, or a parallel schema. See [ADR-0008](docs/Knowledge_Base/Decisions/ADR-0008-Shared-Supabase-Backend.md).

## Current status

| Area | Status |
|---|---|
| Desktop application source | Missing |
| Build and toolchain | Not initialized |
| Feature specifications | 22 of 22 proposed |
| Desktop tests | None |
| Shared-backend connection | Not implemented; same-project identity is not yet verified |
| Documentation baseline | Complete for the current pass |

The desktop connection status is **Missing**. The Android application is the only implementation available for reference. Live Supabase schema, grants, RLS behavior, Storage rules, and hosted project identity have not been verified.

## Documentation

- [Knowledge Base](docs/Knowledge_Base/Home.md) — entry point and index
- [Final Report](docs/Knowledge_Base/Audits/Final-Report.md) — discovery, findings, risks, and next gate
- [Shared Backend Investigation](docs/Knowledge_Base/Audits/Shared-Backend-Connection-Investigation.md) — CSV evidence, Android connection path, and same-project requirements
- [ADR-0008 — Shared Supabase Backend](docs/Knowledge_Base/Decisions/ADR-0008-Shared-Supabase-Backend.md) — accepted backend constraint
- [Feature Inventory](docs/Knowledge_Base/Product/Feature-Inventory.md) — 22-module scope and status
- [Roadmap](docs/Knowledge_Base/Roadmap/Desktop-Roadmap.md) — Phase 0 through pilot gates
- [Test Strategy](docs/Knowledge_Base/Testing/Test-Strategy.md) — test layers and release gates

## Repository layout

```text
docs/Knowledge_Base/              Desktop Knowledge Base and specifications
.opencode/skills/                 Documentation-maintenance skill definitions
Supabase Snippet List ...csv      User-supplied public column snapshot
LICENSE                           Apache License 2.0
```

The repository intentionally does not contain application code yet. It also does not contain environment files, API keys, database passwords, service-role keys, or production data.

## Backend and security rules

- Reuse the existing Supabase project and schema; do not provision a second backend.
- Authenticate as a staff user and use the user's JWT; let Supabase Auth and RLS enforce access.
- Never ship a service-role key, database password, or direct PostgreSQL credential in the desktop application.
- Keep privileged staff and notification operations in the existing server-side Edge Functions.
- Do not run migrations, modify production schema, or write production data without a separate approved change.
- Do not commit `.env` files, credentials, tokens, or patient data. `.gitignore` covers common local secret files.

## Getting started

This repository is currently a documentation project. Open [the Knowledge Base](docs/Knowledge_Base/Home.md) in a Markdown viewer or Obsidian. The notes use Obsidian wikilinks and are best read from the vault root at `docs/Knowledge_Base/`.

Application setup, build commands, and test commands will be added when the Go/Wails implementation is initialized.

## License

Licensed under the [Apache License 2.0](LICENSE).
