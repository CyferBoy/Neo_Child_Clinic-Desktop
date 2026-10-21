---
title: Desktop Knowledge Base Entry
doc_status: baseline
evidence: documentation pass + shared-backend connection investigation + Phase 0C metadata export review
updated: 2026-10-21
---

# Neo Child Clinic Desktop — Knowledge Base Entry

This folder is the desktop-specific Obsidian vault. It is separate from the Android Knowledge Base so Android notes are not overwritten or duplicated.

## Start

- Open [[Home]] for the dashboard and full index.
- Open [[Audits/Final-Report|Final Report]] for the end-to-end discovery, audit, status, risks, and next gate.
- Open [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] for the current schema/security evidence and blockers.
- Open [[Audits/Documentation-Validation|Documentation Validation]] for the historical second-pass claim/evidence matrix.
- Open [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] for the export/Android/desktop connection evidence and the same-project gate.
- Open [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] for the accepted shared-backend decision.
- Open [[Product/Feature-Inventory|Feature Inventory]] for the 22-module status.

## Status

The desktop application is **not implemented**. The 22 module specifications are proposed. The Android reference and the supplied metadata exports are evidence, not proof of live desktop behavior or runtime security. The desktop must reuse the existing Supabase project and remote schema; no new project, separate remote PostgreSQL database, or parallel remote schema is approved. Local SQLite is expected.

## Related

[[Home]] · [[Product/Product-Scope|Product Scope]] · [[Database/Database-Architecture|Database Architecture]] · [[Security/Security-Model|Security Model]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]]
