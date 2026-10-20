---
title: Personas and Roles
doc_status: baseline
evidence: Android UserRole + UI gates + RLS notes
updated: 2026-10-20
---

# Personas and Roles

> **Desktop status: not implemented.** The role model below is verified from Android source. The desktop permission matrix is proposed and must be reconciled with RLS before implementation.

## Verified role model

`UserRole` is a five-value enum in `domain/model/Profile.kt`: `admin`, `doctor`, `receptionist`, `nurse`, `inventory_manager`.

`[VERIFIED]` The current authorization role is read from Supabase `app_metadata.role` (`core/security/CurrentUserProvider.kt`). It is not read from `user_metadata`, and the code deliberately returns null for a missing or malformed role instead of defaulting.

`[VERIFIED]` Android UI gates include:
- Admin-only staff management screens (`AdminGuard` in `app/NavigationDashboardGraph.kt`).
- Statistics access for admin and doctor (`app/NavigationStatisticsGraph.kt`).
- Patient edit/delete for admin or doctor (`feature/patient/presentation/PatientListScreen.kt`).
- Expense management for admin or doctor (`feature/finance/presentation/ExpenseListViewModel.kt`).
- Doctor slot management for admin, or a doctor editing their own slots.

These are UI affordances. They are **not** proof that RLS enforces the same policy. The existing Android security register records that the backend model is effectively "single clinic, active staff" for many tables, not per-role scoping.

## Personas

### Admin
Owns staff accounts, role changes, audit review, backup, settings, and exception resolution. Needs full reporting and the ability to correct data without bypassing audit.

### Doctor
Owns clinical notes, consultations, vaccination decisions, and clinical review. Needs patient history and reports; should not silently gain inventory or staff-administration privileges.

### Receptionist
Owns registration, search, scheduling/todos, payments, and receipts. Needs fast keyboard entry and clear duplicate warnings.

### Nurse
Owns vaccination administration, due lists, patient history, and stock consumption. Needs strong validation around batch, dose, and cold-chain/expiry data.

### Inventory manager
Owns catalog, batches, stock counts, waste, borrow/return, and expiry. Needs ledger-level traceability and no silent arithmetic corrections.

## Proposed desktop permission matrix

Legend: **A** allowed, **C** allowed with confirmation, **O** own records only, **—** not allowed. This matrix is `[PROPOSED]`; every cell must be implemented in RLS or a server-side function, not only in React.

| Action | Admin | Doctor | Receptionist | Nurse | Inventory manager |
|---|---|---|---|---|---|
| Sign in / view own profile | A | A | A | A | A |
| Read patient demographics and history | A | A | A | A | A |
| Create patient | A | A | A | A | — |
| Edit patient demographics | A | A | A | — | — |
| Merge patients | C | C | — | — | — |
| Delete/archive patient | C | C | — | — | — |
| Record vaccination | A | A | — | A | — |
| Record consultation | A | A | — | — | — |
| Read inventory and expiry | A | A | A | A | A |
| Add/edit vaccine catalog | A | — | — | — | A |
| Add batch / adjust stock | A | — | — | — | A |
| Record waste | A | — | — | A | A |
| Record borrow/return | A | — | — | A | A |
| Record payment / income | A | A | A | — | — |
| Record expense | A | A | — | — | — |
| Print/export receipt | A | A | A | — | — |
| View dashboard | A | A | A | A | A |
| View statistics/reports | A | A | — | — | — |
| Manage staff and roles | A | — | — | — | — |
| View audit log | A | — | — | — | — |
| Trigger full sync / resolve sync errors | A | — | — | — | — |
| Backup/restore | A | — | — | — | — |
| Change clinic settings | A | — | — | — | — |
| Check for updates | A | A | A | A | A |

## Security rules

1. **No client-only enforcement.** A hidden route or disabled button is not authorization.
2. **Least privilege.** The desktop should request only the tables and actions needed for the signed-in role.
3. **Self-service limits.** A staff member cannot change their own role, deactivate themselves, or delete themselves.
4. **Deactivation is immediate.** Existing sessions must be revoked or banned, not merely hidden.
5. **Audit is append-only.** No role may update or delete audit rows through the client.
6. **Support access is explicit.** Any break-glass or impersonation flow requires approval, logging, and a time limit. None is proposed for Phase 1.

## Open questions

- Should `inventory_manager` be allowed to record vaccinations in the target clinic?
- Should receptionists see clinical notes, or only scheduling and payment data?
- Does the clinic need per-doctor restriction of patient records?
- Which actions require a second-person confirmation?

## Related

[[Product/Product-Vision|Product Vision]] · [[Security/Security-Model|Security Model]] · [[Security/Threat-Model|Threat Model]] · [[Database/Access-Patterns|Database Access Patterns]] · [[Features/03-Staff-and-Role-Management|Staff and Role Management]]
