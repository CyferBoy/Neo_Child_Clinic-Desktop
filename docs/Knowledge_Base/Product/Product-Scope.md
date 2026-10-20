---
title: Product Scope
doc_status: baseline
evidence: explicit project direction + Android feature inventory
updated: 2026-10-20
---

# Product Scope

> **Desktop status: not implemented.** Scope is a proposed Phase 1 boundary. No delivery date or effort estimate is asserted.

## Phase 1 scope

Phase 1 is the minimum desktop product that can run the clinic's core workflow with the same business meaning as the Android reference.

| Group | Modules | Why it is in Phase 1 |
|---|---|---|
| Foundation | Desktop shell, authentication, staff/roles | Every workflow depends on identity, navigation, and authorization |
| Clinical | Patients, vaccinations, consultations, vaccination reminders, personal reminders | The clinic's primary record-keeping loop |
| Inventory | Vaccine catalog/batches, wastage, borrow/return | Vaccination recording must not corrupt stock |
| Money | Finance/payments, receipts/printing | A visit is not complete until payment and receipt are correct |
| Insight | Dashboard, statistics/reports | Front desk and management need same-day visibility |
| Reliability | Local persistence/offline, Supabase sync, backup/recovery | The clinic must keep working during network loss and recover safely |
| Operations | Notifications, settings, audit, updates | Day-to-day administration and release safety |

The 22 module specifications are in `Features/`. Requirement IDs are stable and are traced in [[Roadmap/Requirements-Traceability|Requirements Traceability]].

## In scope

- Desktop application for staff, using Supabase Auth and RLS.
- Local-first reads and writes with a visible sync state.
- Patient registration, search, detail, merge, notes/todos/documents where specified.
- Vaccination recording with batch selection, stock deduction, due-date creation, payment, and receipt.
- Consultation recording with follow-up and payment integration.
- Vaccine catalog, batch stock, wastage, borrow/return, and stock history.
- Due vaccination and personal reminder workflows.
- Finance transactions, expenses, receipts, and report views.
- Audit log read and append-only write paths.
- Backup export/import and restore conflict handling.
- Application update check and release metadata.
- Desktop notification behavior for due reminders.
- Accessibility and keyboard operation for core workflows.

## Out of scope

- Building a new backend or changing the production schema as part of this documentation task.
- Implementing any desktop feature in this pass.
- Migrating or modifying production data.
- Installing dependencies or creating a desktop codebase.
- Replacing Android-specific features such as home-screen widgets or biometrics with identical desktop behavior.
- Multi-tenant clinic separation unless separately approved.
- Legal, tax, or insurance compliance certification.

## Assumptions

| ID | Assumption | Status |
|---|---|---|
| A-01 | The Android app is the functional reference, not a specification of every edge case | `[VERIFIED]` project direction |
| A-02 | Supabase remains the shared backend and RLS remains the enforcement layer; the desktop reuses the existing project and schema | `[DECISION]` project direction + ADR-0008 |
| A-03 | The desktop app can use a local database as its working copy | `[PROPOSED]` architecture |
| A-04 | Staff have individual Supabase accounts; shared logins are not acceptable | `[PROPOSED]` security baseline |
| A-05 | The clinic operates in IST for reporting | `[VERIFIED]` Android `DateUtils` reference |
| A-06 | Existing Android clients will continue to write to the same tables during transition | `[UNKNOWN]` deployment plan |

## Delivery boundaries

- Phase 0 must establish repository, instructions, CI, an approved non-destructive verification path against the existing Supabase project, a reviewed baseline schema, and the sync contract before feature work. Do not create a new project, separate database, duplicate tables, or parallel schema.
- Phase 1 is complete only when every module has an accepted specification, implementation, automated checks, and a recorded manual acceptance result.
- A module cannot be marked complete solely because a screen renders or a happy-path request succeeds.
- No production rollout until RLS, backup restore, and sync idempotency have evidence.

## Change control

New scope enters through a written change request that states the user problem, affected requirements, data impact, security impact, and acceptance evidence. A scope change that touches schema, RLS, money, stock, or patient identity requires an ADR and a migration review.

## Related

[[Product/Product-Vision|Product Vision]] · [[Product/Feature-Inventory|Feature Inventory]] · [[Product/Android-Desktop-Parity|Android-Desktop Parity]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Audits/Initial-Audit|Initial Audit]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
