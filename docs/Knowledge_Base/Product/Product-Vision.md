---
title: Product Vision
doc_status: baseline
evidence: source inspection + explicit project direction
updated: 2026-10-20
---

# Product Vision

> **Desktop status: not implemented.** This document describes the intended desktop product. It does not claim that any desktop feature exists.
> Android reference inspected at `/data/data/com.termux/files/home/Neo_Child_Clinic` (`ca4bed4`, 2026-10-18).

## Why a desktop application

The existing Android application is the functional reference for a single-clinic workflow: patients, vaccinations, consultations, batch-level inventory, reminders, payments, receipts, reporting, audit, and encrypted backup. A desktop client is intended to make the same operational data usable at the front desk and in the back office, where a larger screen, keyboard data entry, window management, and local printing matter.

**Verified reference facts** `[VERIFIED]`
- The Android repository contains feature packages for patient, vaccination, consultation, inventory, waste, borrowed vaccines, reminders, personal reminders, finance, dashboard, statistics, audit, sync, settings, staff, update, and auth.
- The Android app is offline-first: writes are committed locally and uploaded through a sync queue.
- The backend is Supabase (Auth, PostgreSQL, RLS, Edge Functions).
- The Android Knowledge Base records historical inventory, sync, statistics, and backup defects. Many are fixed at `ca4bed4`; open gaps include deletion/absence reconciliation, sync queue priority, a local-only inventory ledger, a duplicate database singleton, and missing end-to-end restore coverage.

**Product intent** `[PROPOSED]`
The desktop client should be a trustworthy, offline-capable workstation for the same clinic, not a second source of truth. Staff should be able to register a patient, record a vaccination, consult, take payment, print a receipt, and reconcile stock even when the clinic network is unavailable. When connectivity returns, the same data should converge safely with the Android clients and Supabase.

## Users

| Role | Primary desktop use |
|---|---|
| Admin | Staff administration, audit review, settings, backup, full reporting, exception handling |
| Doctor | Patient history, consultations, vaccination review, clinical reports |
| Receptionist | Registration, search, appointments/todos, payments, receipts |
| Nurse | Vaccination recording, due lists, patient history, stock consumption |
| Inventory manager | Vaccine catalog, batches, stock movements, waste, borrow/return, expiry review |

The role names are verified from `app/src/main/java/com/neochildclinic/domain/model/Profile.kt`. The desktop permission matrix is proposed in [[Product/Personas-and-Roles|Personas and Roles]].

## Goals

1. **Clinical continuity.** A staff member can find a patient and see the complete timeline without waiting for the network.
2. **Data integrity over convenience.** Stock, payments, receipts, and audit records are never silently lost or double-applied.
3. **Offline-first by design.** Local writes commit first; synchronization is observable, retryable, and idempotent.
4. **Role-appropriate access.** Authorization is enforced by the backend, not only by hidden buttons.
5. **Operational confidence.** A failed sync, print, update, or backup produces an actionable state, not a silent failure.
6. **Desktop-native efficiency.** Keyboard-first entry, large tables, multi-column detail views, and local printing.

## Non-goals for Phase 1

- Patient-facing portal, telemedicine, or messaging.
- Insurance claims, accounting ledgers, payroll, or statutory tax filing.
- Multi-clinic tenancy or cross-clinic data sharing.
- Replacing Supabase as the authoritative shared store.
- Mobile parity for every Android widget, notification, or biometric detail.
- Automatic migration of production data without an approved, tested runbook.

These are scope boundaries, not permanent product decisions. Changing them requires an explicit decision record.

## Principles

- **Local database is the working copy; Supabase is the shared authority.** Neither side is allowed to invent a second identity for the same business event.
- **Every write has an idempotency key.** A retry must not create a second patient, vaccination, payment, or stock movement.
- **Money is stored and calculated in integer minor units.** The Android client maps most shared-schema `numeric` amounts to `Double`; the desktop should not repeat the floating-point calculation risk.
- **Dates are typed, timezone-explicit values.** Clinic reporting uses IST (`Asia/Kolkata`), matching the Android reference; storage and transport must be unambiguous.
- **Soft deletion is a synchronization concern, not only a UI filter.** Deletes need an approved reconciliation contract (tombstones or absence reconciliation) and consistent filters across reads, reports, and sync.
- **No service-role key in the client.** The desktop authenticates as a staff user and is subject to RLS.
- **No PHI in logs, crash reports, window titles, or telemetry.** Redaction is a release gate.
- **The UI may guide, but the database decides.** UI guards are usability features; RLS and server-side validation are the security boundary.

## Constraints and decisions

`[DECISION]` The project direction supplied on 2026-10-20 specifies Go, Wails, React + TypeScript, Supabase Auth/PostgreSQL/RLS, local persistence, caching, and offline-first sync.

`[DECISION]` The desktop must reuse the **same existing Supabase project and PostgreSQL schema** as Android. No new project, separate remote PostgreSQL database, duplicate remote tables, or parallel remote schema is approved; local SQLite is expected. See [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]].

`[PROPOSED]` Local persistence technology, Wails major version, sync conflict policy, packaging targets, and test tooling are not yet approved. They are recorded as proposed ADRs under [[Decisions/README|Decisions]].

## What success looks like

No numeric targets are invented. Phase 1 is successful when:
- all 22 Phase 1 modules have an approved specification and a traceable acceptance test;
- a new desktop install can authenticate, work offline, and reconcile a defined set of writes without duplication;
- RLS is verified with at least two real roles through an approved non-destructive path against the existing Supabase project;
- Android-created and desktop-created rows are mutually visible without duplication, and both clients use the same project identity;
- a vaccination write, stock movement, payment, and receipt can be replayed without changing the business result;
- a backup can be restored into a clean environment and reconciled;
- the release checklist is completed with recorded evidence, not assertions.

## Open questions

- Is the desktop app single-workstation or multi-workstation per clinic in Phase 1?
- Which operating systems are release targets?
- Does the clinic need a local server or peer sync, or is Supabase the only shared transport?
- Which reports are legally or operationally required on paper?
- Who approves role changes and data-retention exceptions?

## Related

[[Product/Product-Scope|Product Scope]] · [[Product/Personas-and-Roles|Personas and Roles]] · [[Product/Feature-Inventory|Feature Inventory]] · [[Architecture/System-Architecture|System Architecture]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
