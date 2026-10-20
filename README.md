# Neo Child Clinic Desktop

A cross-platform desktop application for Neo Child Clinic, planned around Go, Wails, React, TypeScript, and the existing Supabase backend.

> **Project status: documentation and architecture baseline — not implemented.** No Go/Wails/React application source, build configuration, or desktop test suite exists yet. Consult the [Feature Inventory](docs/Knowledge_Base/Product/Feature-Inventory.md) and [Roadmap](docs/Knowledge_Base/Roadmap/Desktop-Roadmap.md) for verified status.

## About

Neo Child Clinic Desktop is intended to provide a desktop workspace for managing clinic patients, vaccinations, consultations, vaccine inventory, reminders, finances, receipts, and reporting.

The desktop application is designed to work with the existing Neo Child Clinic Android application's Supabase backend: the same Auth users, PostgreSQL schema, tables, Row Level Security policies, Storage buckets, and Edge Functions. It must not create a new backend, a separate database, duplicate tables, or a parallel schema.

See [ADR-0008](docs/Knowledge_Base/Decisions/ADR-0008-Shared-Supabase-Backend.md) for the accepted shared-backend decision.

## Overview

The repository currently contains the product and technical baseline for the desktop application. It does not contain application code. The Android application remains the only implementation available for reference.

Feature status must be verified against the source code and documented requirements. The current baseline records **22 proposed desktop modules, 0 implemented modules, and 0 desktop tests**.

## Features

### Core clinic management

- Patient management
- Vaccination management
- Consultation management
- Vaccine and batch inventory
- Wastage tracking
- Borrowed and lent vaccines
- Vaccination reminders
- Personal reminders

### Administration and reporting

- Staff and role management
- Dashboard and statistics
- Financial management
- Receipts and printing
- Audit logging
- Settings

### Reliability and security

- Supabase authentication and authorization
- Reuse of the existing database
- Row Level Security
- Local persistence and offline synchronization — proposed, not implemented
- Backup and recovery — proposed, not implemented

Feature status is recorded in the [Feature Inventory](docs/Knowledge_Base/Product/Feature-Inventory.md) and the [Desktop Roadmap](docs/Knowledge_Base/Roadmap/Desktop-Roadmap.md).

## Technology stack

| Component | Technology | Current status |
|---|---|---|
| Desktop framework | Wails | Planned; not initialized |
| Backend | Go | Planned; not initialized |
| Frontend | React + TypeScript | Planned; not initialized |
| Database | Existing Supabase PostgreSQL project | Required; live schema not verified |
| Authentication | Existing Supabase Auth | Required; live configuration not verified |
| Authorization | Existing RLS policies and role claims | Required; live policies not verified |
| Local persistence | SQLite working copy plus outbox | Proposed; not implemented |

No dependency versions or build commands are asserted yet. They must be pinned when the application toolchain is initialized.

## Architecture

The intended architecture is:

- React and TypeScript provide the desktop interface.
- Wails exposes typed bindings between the frontend and Go services.
- Go owns application logic, local persistence, synchronization, and privileged desktop operations.
- Supabase provides the shared backend through Auth, PostgREST, Storage, Functions, and Realtime.
- A local SQLite working copy and outbox support offline-first operation.
- The desktop never opens a direct PostgreSQL connection and never ships a service-role key.

See the [System Architecture](docs/Knowledge_Base/Architecture/System-Architecture.md), [Go Backend Architecture](docs/Knowledge_Base/Architecture/Go-Backend-Architecture.md), and [Offline and Sync Design](docs/Knowledge_Base/Architecture/Offline-and-Sync-Design.md) for verified components, proposed designs, and unresolved decisions.

## Requirements

The application toolchain is not initialized, so runtime versions are not yet defined. The eventual implementation will need pinned versions of:

- Go
- Wails CLI and platform dependencies
- Node.js and the chosen frontend package manager
- Required compilers and system libraries
- A SQLite driver and local encryption approach
- Approved access to the existing Supabase project for integration testing

Do not infer versions or installation instructions before the project configuration exists.

## Getting started

This repository is currently a documentation project. To review it:

1. Clone the repository.
2. Open [the Knowledge Base](docs/Knowledge_Base/Home.md).
3. Read the [Final Report](docs/Knowledge_Base/Audits/Final-Report.md) and [Shared Backend Investigation](docs/Knowledge_Base/Audits/Shared-Backend-Connection-Investigation.md).
4. Consult the [Phase 1 Implementation Plan](docs/Knowledge_Base/Roadmap/Phase-1-Implementation-Plan.md) before starting implementation.

Application setup, build, and test commands will be added after the Go/Wails toolchain is initialized and verified. Do not publish placeholder commands as working instructions.

## Configuration and database

The desktop application must use the existing Neo Child Clinic Supabase project. Before connecting it, verify:

- Project URL and public client configuration through an approved channel
- Authentication initialization
- Database tables and relationships
- Row Level Security policies, grants, and triggers
- Role and permission handling
- Storage policies
- Offline synchronization behavior, if implemented

Never commit passwords, service-role keys, access tokens, or other secrets. The repository ignores common local environment files. The actual project URL, publishable key, and hosted identity are not present in this repository.

Do not create a new production database or duplicate the existing schema. See the [Database Architecture](docs/Knowledge_Base/Database/Database-Architecture.md) and [Access Patterns](docs/Knowledge_Base/Database/Access-Patterns.md).

## Security

- Keep privileged credentials out of the frontend and distributed desktop application.
- Use authenticated-user access and existing Row Level Security policies.
- Verify authorization on the server and database side.
- Protect sensitive local data and backups.
- Avoid logging patient information, credentials, tokens, or database connection strings.
- Review database migrations and security-policy changes before applying them.
- Treat the Android security findings as inherited risks until they are verified or fixed.

See the [Security Model](docs/Knowledge_Base/Security/Security-Model.md), [Threat Model](docs/Knowledge_Base/Security/Threat-Model.md), and [Privacy and Backup](docs/Knowledge_Base/Security/Privacy-and-Backup.md).

## Development

Verified development commands are not available yet because the application source and toolchain are missing.

When implementation begins, document and verify commands for:

- Development mode
- Production build
- Unit tests
- Integration tests
- Frontend tests
- Linting and formatting
- Packaging for each supported operating system

Documentation changes can be reviewed directly in `docs/Knowledge_Base/`.

## Project structure

```text
README.md                         This repository entry point
LICENSE                           Apache License 2.0
.gitignore                        Local secret and OS-file exclusions
.opencode/skills/                 Documentation-maintenance skill definitions
docs/Knowledge_Base/              Desktop Knowledge Base and specifications
Supabase Snippet List ...csv      User-supplied public table-column snapshot
```

Application directories such as `cmd/`, `internal/`, `frontend/`, and `build/` do not exist yet and are not listed as if they did.

## OpenCode skills

Project-specific OpenCode skills are maintained under `.opencode/skills/` when present. They cover repository audits, feature specifications, architecture documentation, database analysis, security review, roadmap planning, testing strategy, and release documentation.

Follow project instructions and review proposed changes before implementation.

## Knowledge Base

Detailed documentation is maintained in [docs/Knowledge_Base](docs/Knowledge_Base/Home.md). Start with the index and consult the relevant architecture, database, security, feature, testing, and roadmap documents.

Key entry points:

- [Final Report](docs/Knowledge_Base/Audits/Final-Report.md)
- [Shared Backend Investigation](docs/Knowledge_Base/Audits/Shared-Backend-Connection-Investigation.md)
- [ADR-0008 — Shared Supabase Backend](docs/Knowledge_Base/Decisions/ADR-0008-Shared-Supabase-Backend.md)
- [Feature Inventory](docs/Knowledge_Base/Product/Feature-Inventory.md)
- [Desktop Roadmap](docs/Knowledge_Base/Roadmap/Desktop-Roadmap.md)
- [Test Strategy](docs/Knowledge_Base/Testing/Test-Strategy.md)

## Roadmap

- **Phase 0:** Discovery, architecture, shared-backend verification, security review, and testing foundation.
- **Phase 1:** Core desktop clinic-management functionality.
- **Phase 2:** Advanced desktop productivity and reporting.
- **Phase 3:** Additional clinical and automation capabilities.

These phases are planning targets, not claims that features are implemented. See the [Desktop Roadmap](docs/Knowledge_Base/Roadmap/Desktop-Roadmap.md) for exit gates.

## Testing

There is currently no desktop test suite. The Android reference has 41 unit-test files and 8 instrumented test files, but those tests were not run in this baseline and are not desktop results.

Future tests must prioritize:

- Inventory reconciliation
- Financial calculations
- Receipt numbering
- Reminder logic
- Authorization and RLS
- Synchronization replay and tombstones
- Backup and restore

See the [Test Strategy](docs/Knowledge_Base/Testing/Test-Strategy.md) and [Regression Matrix](docs/Knowledge_Base/Testing/Regression-Matrix.md).

## Troubleshooting

There is no application build yet, so installation and runtime troubleshooting is not available.

Known baseline blockers are documented in the [Final Report](docs/Knowledge_Base/Audits/Final-Report.md) and [Home](docs/Knowledge_Base/Home.md): missing desktop source, unverified same-project configuration, no reproducible schema baseline, unverified live RLS and Storage, and no approved non-destructive verification path.

## Contributing

- Preserve unrelated user changes.
- Follow the documented architecture and coding conventions.
- Add tests for business-critical changes.
- Update the Knowledge Base when requirements or architecture change.
- Review database and security changes before applying them.
- Do not commit secrets, production data, or generated credentials.

Implementation is gated on approval of the shared-backend verification path and the proposed architecture decisions.

## License

Licensed under the [Apache License 2.0](LICENSE).
