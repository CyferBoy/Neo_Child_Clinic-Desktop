---
title: Desktop Knowledge Base Entry
doc_status: baseline
evidence: documentation completion pass + shared-backend connection investigation + Phase 0C metadata export review
updated: 2026-10-21
---

# Neo Child Clinic Desktop — Knowledge Base Entry

This folder is the desktop-specific Obsidian vault. It is separate from the Android Knowledge Base so Android notes are not overwritten or duplicated.

## Start

- Open [[Home]] for the dashboard and full index.
- Open [[Audits/Documentation-Completion-Report|Documentation Completion Report]] for the final reviewed/created/updated inventory, validation results, open questions, blockers, and implementation sequence.
- Open [[Product/Repository-Inventory|Repository Inventory]] for verified repository structure and commands.
- Open [[Product/Business-Rules|Business Rules]] for cross-cutting invariants and their authoritative specifications.
- Open [[Architecture/Android-Reference-Architecture|Android Reference Architecture]] for the current Android evidence snapshot.
- Open [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]] for the current schema/security evidence and blockers.
- Open [[Audits/Documentation-Validation|Documentation Validation]] for the historical second-pass claim/evidence matrix.
- Open [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] for the export/Android/desktop connection evidence and the same-project gate.
- Open [[Decisions/README|Decision Log]] for ADR status; [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] is the only accepted decision.
- Open [[Product/Feature-Inventory|Feature Inventory]] for the 22-module status.
- Open [[Testing/Test-Case-Catalog|Test Case Catalog]] for the 126 planned tests; none is implemented or executed.

## Status

The desktop application is **not implemented**. The 22 module specifications are proposed and now contain user stories and database dependencies. The Android reference and the supplied metadata exports are evidence, not proof of live desktop behavior or runtime security. The desktop must reuse the existing Supabase project and remote schema; no new project, separate remote PostgreSQL database, or parallel remote schema is approved. Local SQLite is expected.

Live Supabase verification and security remediation remain **deferred by the project owner** to a separate phase. No statement in this vault should be read as a live RLS certification or a claim that an exported exposure was exercised.

## Related

[[Home]] · [[Product/Product-Scope|Product Scope]] · [[Product/Business-Rules|Business Rules]] · [[Database/Database-Architecture|Database Architecture]] · [[Security/Security-Model|Security Model]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Audits/Documentation-Completion-Report|Documentation Completion Report]]
