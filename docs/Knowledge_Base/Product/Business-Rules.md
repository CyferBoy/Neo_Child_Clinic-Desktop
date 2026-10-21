---
title: Business Rules
doc_status: proposed
evidence: 22 feature specifications + Android reference + Phase 0C metadata exports (no SQL executed)
updated: 2026-10-21
---

# Business Rules

> **Cross-cutting index, not a second specification.** Detailed validation, workflows, and acceptance criteria remain in each feature note. This page records the invariants that no desktop module may violate. Every rule is proposed for desktop unless marked otherwise.

## Status legend

| Label | Meaning |
|---|---|
| `[REPORTED]` | Backend shape/behaviour reported by an export; not runtime-certified. |
| `[VERIFIED]` | Checked in Android source, migrations, or repository artifacts. |
| `[PROPOSED]` | Desktop requirement, not implemented. |
| `[DECISION]` | Accepted project direction. Only ADR-0008 is accepted. |

## Core invariants

| ID | Rule | Evidence / authority | Status | Detailed spec |
|---|---|---|---|---|
| BR-01 | **Two patient identities.** A UUID is the database identity; the clinic ID is the human key. Neither name, phone, nor formatted date is a primary key. | Android `PatientEntity`; `patients` export | `[VERIFIED]` reference pattern | [[Features/04-Patient-Management|Patients]] |
| BR-02 | **The visit is the clinical/financial aggregate.** A vaccination or consultation must not exist as an orphan; dependent stock, payment, reminder, and audit intent belong to one logical local transaction. | Android visit model; `patient_visits`, `vaccination_items`, `consultations` | `[PROPOSED]` desktop | [[Features/05-Vaccination-Management|Vaccinations]] · [[Features/06-Consultation-Management|Consultations]] |
| BR-03 | **One stock ledger.** Stock changes go through a single auditable movement path. Do not edit `vaccine_batches.remaining_quantity` directly from the renderer or as an independent convenience write. | Android inventory engines; exported `inventory_transactions`; [[Audits/Phase-0C-Schema-Export-Review|Phase 0C]] §5.2 | `[PROPOSED]` desktop; backend is **not** in the fixed state | [[Features/07-Vaccine-and-Batch-Inventory|Inventory]] |
| BR-04 | **Stock is never negative and never double-applied.** A retry, duplicate submit, edit, or replay must not create a second movement. The exported database currently reports two stock triggers and the old function, so inventory writes are blocked until exactly one writer is verified. | [[Audits/Phase-0C-Schema-Export-Review|Phase 0C]] §5.2; [[Audits/Risk-Register|Risk Register]] RISK-023 | `[REPORTED]` defect / `[PROPOSED]` control | [[Features/05-Vaccination-Management|Vaccinations]] · [[Features/07-Vaccine-and-Batch-Inventory|Inventory]] |
| BR-05 | **One income identity per visit.** Vaccination and consultation payments linked to a visit are counted once. Edits preserve the payment identity; refunds/corrections are audited events, not silent negative edits. | Android finance bugs fixed at `ca4bed4`; `finance_transactions` | `[VERIFIED]` historical defect; `[PROPOSED]` desktop | [[Features/12-Finance-and-Payments|Finance]] · [[Features/15-Statistics-and-Reports|Reports]] |
| BR-06 | **Money is exact.** Calculate in integer minor units; convert explicitly at the shared numeric boundary; never compare floating-point values for equality. | ADR-0007; shared schema uses `numeric` except `expenses.amount_paise` | `[PROPOSED]` desktop | [[Features/12-Finance-and-Payments|Finance]] |
| BR-07 | **Receipts are server-assigned and immutable.** The desktop must never compute, reuse, or alter a receipt number. The financial year comes from the visit date. | `20260824_receipt_numbering.sql`; exported `receipt_sequences`; Phase 0C anon-executable function | `[VERIFIED]` repository intent / `[REPORTED]` exposure | [[Features/13-Receipts-and-Printing|Receipts]] |
| BR-08 | **Business dates use IST.** Due lists, dashboard “today”, and report windows use `Asia/Kolkata`, not the workstation timezone. Store typed dates/timestamps; never sort formatted strings. | Android `DateUtils`; ADR-0007 | `[VERIFIED]` reference / `[PROPOSED]` desktop | [[Features/10-Vaccination-Reminders|Reminders]] · [[Features/14-Dashboard|Dashboard]] |
| BR-09 | **Reminder terminal states win.** Completed, dismissed, or cancelled reminders do not notify again and are not resurrected by a stale sync. One active clinical reminder per due item unless duplication is explicitly approved. | Feature 10; Android reminder defects fixed | `[PROPOSED]` desktop | [[Features/10-Vaccination-Reminders|Vaccination Reminders]] · [[Features/11-Personal-Reminders|Personal Reminders]] |
| BR-10 | **Soft deletion is consistent.** Deleted rows are excluded from active reads, reports, exports, notifications, and detail counts. Deletion propagation requires an approved absence/tombstone contract; no complete server tombstone feed is evidenced. | Migrations; NCC-023; [[Architecture/Offline-and-Sync-Design|Offline and Sync Design]] | `[VERIFIED]` gap / `[PROPOSED]` contract | [[Features/16-Local-Persistence-and-Offline-Operation|Offline]] · [[Features/17-Supabase-Sync|Sync]] |
| BR-11 | **Audit is append-only and attributable.** Actor, action, entity, and time are required. No client role updates or deletes audit rows. A failed sensitive-action audit blocks or flags the action. | Android audit logger; exported broad insert policy is a defect | `[VERIFIED]` reference intent / `[REPORTED]` policy defect | [[Features/21-Audit-Logging|Audit Logging]] |
| BR-12 | **Authorization fails closed.** The role comes from validated `app_metadata.role`; a missing/unknown role is denied. UI guards are not authorization. RLS and grants are enforced separately. | Android `CurrentUserProvider`; Phase 0C | `[VERIFIED]` client / `[PROPOSED]` target | [[Security/Security-Model|Security Model]] · [[Features/02-Authentication-and-Session|Auth]] |
| BR-13 | **A local commit is not a cloud acknowledgement.** The UI must distinguish local-only, syncing, failed, conflicted, and acknowledged states. | Feature 16; ADR-0003 | `[PROPOSED]` desktop | [[Features/16-Local-Persistence-and-Offline-Operation|Offline]] |
| BR-14 | **One business event, one transaction group.** A group is acknowledged only when all required members are acknowledged; retries reuse identity; a partial apply is visible and repairable. | ADR-0003; [[Architecture/Offline-and-Sync-Design|Offline and Sync Design]] | `[PROPOSED]` desktop | [[Features/17-Supabase-Sync|Sync]] |
| BR-15 | **No silent last-write-wins for money, stock, clinical notes, or receipts.** Conflicts are surfaced with a resolution workflow. | ADR-0003; ADR-0007 | `[PROPOSED]` desktop | [[Features/17-Supabase-Sync|Sync]] |
| BR-16 | **Backup is PHI; restore is destructive.** Export requires encryption and integrity checks; restore requires preview, explicit confirmation, a safety snapshot, and atomic completion. | Android backup reference; [[Security/Privacy-and-Backup|Privacy and Backup]] | `[PROPOSED]` desktop | [[Features/18-Backup-and-Recovery|Backup]] |
| BR-17 | **Printing/export is explicit and minimised.** Preview before print; no PHI in window titles, notification previews, logs, crash reports, or telemetry. Printer spool retention is an operational risk. | [[Security/Threat-Model|Threat Model]]; Security Model | `[PROPOSED]` desktop | [[Features/13-Receipts-and-Printing|Receipts]] · [[Security/Privacy-and-Backup|Privacy]] |
| BR-18 | **Staff lifecycle is server-controlled.** No self-role change, self-deactivation, or shared accounts. Deactivation revokes refresh capability, not just UI access. | Android `manage-staff`; Phase 0C role-source split | `[VERIFIED]` client intent / `[REPORTED]` backend split | [[Features/03-Staff-and-Role-Management|Staff]] |
| BR-19 | **Report cards and details use the same definitions.** Every total has a matching detail query; deleted rows are excluded; vaccine grouping uses the catalog identity, not display text. | Feature 15; Android statistics defects fixed | `[PROPOSED]` desktop | [[Features/14-Dashboard|Dashboard]] · [[Features/15-Statistics-and-Reports|Reports]] |
| BR-20 | **Every new backend object has an explicit grant and role test.** Do not rely on default ACLs. GRANT and RLS are separate controls; neither proves the other. | [[Database/Database-Architecture|Database Architecture]] §Migration convention corrections | `[REPORTED]` gap | [[Database/Database-Architecture|Database Architecture]] · [[Decisions/ADR-0009-Inventory-and-Financial-Integrity|ADR-0009]] |

## Domain summaries

### Patient and visit

- Registration requires a name and a valid, normalised phone; DOB cannot be in the future; clinic ID is unique.
- Duplicate names/phones produce a warning, not an automatic merge.
- A merge reassigns dependent rows and preserves audit; a patient with clinical/financial history is not hard-deleted.
- A visit date is the user-entered clinical date. `created_at`/`updated_at` are metadata, not the business date.

### Vaccination and inventory

- At least one vaccine item is required; quantity must be positive and available; expired batches cannot be used clinically.
- FEFO is the preferred selection policy; manual batch choice must be explicit and visible.
- Wastage is a stock movement with a reason. Borrow/lend preserves batch identity and outstanding balance; a return cannot exceed the outstanding amount.
- The exported backend's stock-trigger state is not safe for writes. This is a gate, not a rule that the desktop may work around.

### Money and receipts

- Cash plus online must equal the visit amount; amounts are non-negative; zero-price/free doses need an explicit flag.
- A visit's income is counted once, regardless of whether it came from a vaccination or consultation path.
- Receipt numbers are assigned by PostgreSQL. A provisional local display must be labelled and must never be printed as final.
- Expense category, title, date, and payment method are required; expenses do not reduce income totals.

### Reminders and notifications

- Vaccination due dates and personal reminders are separate records.
- A personal reminder may be undated only with an explicit undated state; an undated reminder must not notify repeatedly.
- Notification previews omit patient identifiers by default. Click-through re-checks authorization.
- Completed/dismissed records do not notify; a stale update cannot reopen a terminal state.

### Offline and recovery

- A local business write and its outbox rows commit atomically or not at all.
- A local commit is reported as local-only until server acknowledgement.
- Sync failures are classified and visible; 401 pauses for re-authentication, 403 is an authorization failure, 409 is reconciled by identity, 429/5xx use bounded backoff.
- Backup/restore does not bypass authentication, audit, or account binding.

## Rules that are not approved

The following remain open and must not be implemented as if settled:

- the deletion/absence reconciliation contract;
- the desktop local-encryption product and key-recovery procedure;
- cross-client backup compatibility between Android and desktop;
- whether FEFO is mandatory or a default;
- whether a visit may contain both vaccination and consultation;
- per-role read access to clinical notes;
- the retention period for audit, clinical, financial, and backup data;
- whether any Phase 3 enhancement is approved.

## Related

[[Home]] · [[Product/Feature-Inventory|Feature Inventory]] · [[Database/Data-Dictionary|Data Dictionary]] · [[Database/Access-Patterns|Access Patterns]] · [[Security/Security-Model|Security Model]] · [[Audits/Risk-Register|Risk Register]] · [[Roadmap/Requirements-Traceability|Requirements Traceability]]
