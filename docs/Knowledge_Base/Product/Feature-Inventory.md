---
title: Feature Inventory
doc_status: baseline
evidence: Android source tree + existing Android KB
updated: 2026-10-20
---

# Feature Inventory

> **Desktop status: all 22 Phase 1 modules are Missing.** No desktop source, Wails configuration, Go module, React application, or desktop test exists in `/storage/emulated/0/Neo_Child_Clinic_Desktop`. The Android reference is the only available implementation.
>
> **Shared backend:** every module must target the **existing** Supabase project/schema under [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]. No module may create a new project, separate database, duplicate tables, or parallel schema.

## Status vocabulary

| Status | Meaning in this KB |
|---|---|
| **Implemented and verified** | Source exists and behaviour is backed by executed tests or recorded runtime evidence. Not used for desktop in this baseline. |
| **Partially implemented** | Source exists but confirmed defects or gaps affect the intended workflow. |
| **Missing** | No implementation exists in the desktop project. |
| **Broken** | A confirmed defect prevents the intended behaviour. Used at finding level, not as a blanket module status. |
| **Unverified** | Source exists, but runtime/live behaviour was not verified in this pass. |
| **Proposed enhancement** | Not implemented; a target design or improvement. |

## Inventory

| # | Module | Requirement prefix | Android reference status | Desktop status | Primary evidence |
|---|---|---|---|---|---|
| 01 | Desktop shell and navigation | PLAT | Unverified | Missing | `app/Navigation.kt`, `feature/dashboard/` |
| 02 | Authentication and session | AUTH | Unverified | Missing | `core/security/AuthViewModel.kt`, `feature/auth/` |
| 03 | Staff and role management | STF | Unverified | Missing | `feature/staff/`, `supabase/functions/manage-staff/` |
| 04 | Patient management | PAT | Partially implemented | Missing | `feature/patient/`, Android KB `Patient Management` |
| 05 | Vaccination management | VAC | Partially implemented | Missing | `feature/vaccination/`, Android KB `Vaccination Management` |
| 06 | Consultation management | CON | Unverified | Missing | `feature/consultation/` |
| 07 | Vaccine and batch inventory | INV | Partially implemented | Missing | `feature/inventory/`, Android KB `Inventory Management` |
| 08 | Wastage | WAS | Unverified | Missing | `feature/waste/` |
| 09 | Borrowed and lent vaccines | BRW | Unverified | Missing | `feature/borrowed/` |
| 10 | Vaccination reminders | REM | Partially implemented | Missing | `feature/reminder/`, Android KB `Due Vaccination` |
| 11 | Personal reminders | PER | Partially implemented | Missing | `feature/personalreminder/`, Android KB `Due Vaccination` |
| 12 | Finance and payments | FIN | Unverified | Missing | `feature/finance/` |
| 13 | Receipts and printing | RCP | Unverified | Missing | `feature/patient/presentation/Receipt*`, `20260824_receipt_numbering.sql` |
| 14 | Dashboard | DSH | Unverified | Missing | `feature/dashboard/` |
| 15 | Statistics and reports | RPT | Partially implemented | Missing | `feature/statistics/`, Android KB `Statistics Dashboard` |
| 16 | Local persistence and offline operation | OFF | Partially implemented | Missing | `data/local/`, Android KB `Offline-First Architecture` |
| 17 | Supabase synchronization | SYNC | Partially implemented | Missing | `feature/sync/`, Android KB `Offline Synchronization` |
| 18 | Backup and recovery | BAK | Partially implemented | Missing | `data/backup/`, Android KB `Backup and Restore` |
| 19 | Desktop notifications | NOT | Partially implemented | Missing | `core/notification/`, Android KB `Due Vaccination` |
| 20 | Settings | SET | Unverified | Missing | `feature/settings/` |
| 21 | Audit logging | AUD | Unverified | Missing | `feature/audit/`, `core/logger/` |
| 22 | Application updates | UPD | Unverified | Missing | `feature/update/` |

**Counts:** desktop 0 implemented, 22 missing. Android reference: 10 partially implemented, 12 unverified in this pass, 0 modules claimed fully verified. No desktop tests were run because there is no desktop test suite.

## What "verified" means here

This baseline did **not** execute the Android app, run the Gradle test suite, or connect to the live Supabase project. Android status is based on source inspection plus the existing Android Knowledge Base, which records both passing-test history and confirmed defects. The exact limitations are in [[Audits/Initial-Audit|Initial Audit]] and [[Testing/Test-Strategy|Test Strategy]].

## Reading the inventory

- A module is not complete because a screen exists.
- A module is not secure because a button is hidden.
- A module is not offline-safe because it writes to a local table.
- A module is not synchronized because a queue row was enqueued.
- A module is not released because it compiles.

## Related

[[Product/Android-Desktop-Parity|Android-Desktop Parity]] · [[Roadmap/Requirements-Traceability|Requirements Traceability]] · [[Features/04-Patient-Management|Patient Management]] · [[Audits/Initial-Audit|Initial Audit]]
