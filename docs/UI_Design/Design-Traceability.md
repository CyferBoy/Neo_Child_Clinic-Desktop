# Design Traceability

**Status:** design traceability, not implementation evidence.

This document links every screen to its section, feature specification, source Knowledge Base document, prototype and rendered reference. It is deliberately explicit about the evidence level: a rendered PNG proves that a design page was rendered, not that a product feature exists.

## 1. Evidence levels

| Level | Evidence | What it proves | What it does not prove |
|---|---|---|---|
| E0 | Knowledge Base requirement or feature specification | The intended behaviour is documented | That it is implemented or correct |
| E1 | Screen specification under `Screens/` | The design covers the documented workflow/state | That the design is approved or buildable as-is |
| E2 | Static HTML prototype under `prototype/screens/` | A reviewable page exists with local fictional data | That interactions, APIs or persistence work |
| E3 | Rendered PNG under `screenshots/` | The page was rendered at the stated dimensions | That it is accessible, complete or production-ready |
| E4 | Executable production test | A real implementation behaves as specified | — (not present) |

No E4 evidence exists for desktop. All 22 desktop modules are recorded as **Missing** in the Knowledge Base. Android source is reference only and was not runtime-verified in this pass.

## 2. Coverage summary

| Section | Screens |
|---|---|
| Authentication | 5 |
| Shell | 1 |
| Dashboard | 1 |
| Patients | 7 |
| Vaccinations | 5 |
| Consultations | 4 |
| Inventory | 6 |
| Wastage | 2 |
| Borrow & Return | 3 |
| Follow-up | 4 |
| Finance | 6 |
| Receipts | 3 |
| Reports | 4 |
| Administration | 6 |
| System | 7 |
| Settings | 4 |
| **Total** | **68** |

The screen set covers all 22 Phase 1 modules. Some cross-cutting modules are represented by shared shell/system/settings surfaces rather than a dedicated module screen.

## 3. Module-to-screen matrix

| Module | Requirement prefix | Screens | Primary source |
|---|---|---|---|
| Desktop shell and navigation | `PLAT` | `SHELL-001` | `01-Desktop-Shell-and-Navigation.md` |
| Authentication and session | `AUTH` | `AUTH-001`–`AUTH-005` | `02-Authentication-and-Session.md` |
| Staff and role management | `STF` | `STF-001`–`STF-004` | `03-Staff-and-Role-Management.md` |
| Patient management | `PAT` | `PAT-001`–`PAT-007` | `04-Patient-Management.md` |
| Vaccination management | `VAC` | `VAC-001`–`VAC-005` | `05-Vaccination-Management.md` |
| Consultation management | `CON` | `CON-001`–`CON-004` | `06-Consultation-Management.md` |
| Vaccine and batch inventory | `INV` | `INV-001`–`INV-006` | `07-Vaccine-and-Batch-Inventory.md` |
| Wastage | `WAS` | `WAS-001`–`WAS-002` | `08-Wastage.md` |
| Borrowed and lent vaccines | `BRW` | `BRW-001`–`BRW-003` | `09-Borrowed-and-Lent-Vaccines.md` |
| Vaccination reminders | `REM` | `REM-001`–`REM-002` | `10-Vaccination-Reminders.md` |
| Personal reminders | `PER` (screened as `REM-003`–`REM-004`) | `REM-003`–`REM-004` | `11-Personal-Reminders.md` |
| Finance and payments | `FIN` | `FIN-001`–`FIN-006` | `12-Finance-and-Payments.md` |
| Receipts and printing | `RCP` | `RCP-001`–`RCP-003` | `13-Receipts-and-Printing.md` |
| Dashboard | `DSH` | `DASH-001` | `14-Dashboard.md` |
| Statistics and reports | `RPT` | `RPT-001`–`RPT-004` | `15-Statistics-and-Reports.md` |
| Local persistence and offline | `OFF` | Cross-cutting; `SYS-003` | `16-Local-Persistence-and-Offline-Operation.md` |
| Supabase synchronization | `SYNC` | `SYS-001`–`SYS-002` | `17-Supabase-Sync.md` |
| Backup and recovery | `BAK` | `SYS-005`–`SYS-007` | `18-Backup-and-Recovery.md` |
| Desktop notifications | `NOT` | `SET-002` | `19-Desktop-Notifications.md` |
| Settings | `SET` | `SET-001`–`SET-004` | `20-Settings.md` |
| Audit logging | `AUD` | `AUD-001`–`AUD-002` | `21-Audit-Logging.md` |
| Application updates | `UPD` | `SYS-004` | `22-Application-Updates.md` |

## 4. Full screen trace

| Screen | Section | Feature | Source specification | Prototype | Rendered | Status |
|---|---|---|---|---|---|---|
| `AUTH-001` | Authentication | Authentication and Session | [`02-Authentication-and-Session.md`](../Knowledge_Base/Features/02-Authentication-and-Session.md) | [HTML](prototype/screens/AUTH-001.html) | [PNG](screenshots/AUTH-001.png) | E2/E3 design |
| `AUTH-002` | Authentication | Authentication and Session | [`02-Authentication-and-Session.md`](../Knowledge_Base/Features/02-Authentication-and-Session.md) | [HTML](prototype/screens/AUTH-002.html) | [PNG](screenshots/AUTH-002.png) | E2/E3 design |
| `AUTH-003` | Authentication | Authentication and Session | [`02-Authentication-and-Session.md`](../Knowledge_Base/Features/02-Authentication-and-Session.md) | [HTML](prototype/screens/AUTH-003.html) | [PNG](screenshots/AUTH-003.png) | E2/E3 design |
| `AUTH-004` | Authentication | Authentication and Session | [`02-Authentication-and-Session.md`](../Knowledge_Base/Features/02-Authentication-and-Session.md) | [HTML](prototype/screens/AUTH-004.html) | [PNG](screenshots/AUTH-004.png) | E2/E3 design |
| `AUTH-005` | Authentication | Authentication and Session | [`02-Authentication-and-Session.md`](../Knowledge_Base/Features/02-Authentication-and-Session.md) | [HTML](prototype/screens/AUTH-005.html) | [PNG](screenshots/AUTH-005.png) | E2/E3 design |
| `SHELL-001` | Shell | Desktop Shell and Navigation | [`01-Desktop-Shell-and-Navigation.md`](../Knowledge_Base/Features/01-Desktop-Shell-and-Navigation.md) | [HTML](prototype/screens/SHELL-001.html) | [PNG](screenshots/SHELL-001.png) | E2/E3 design |
| `DASH-001` | Dashboard | Dashboard | [`14-Dashboard.md`](../Knowledge_Base/Features/14-Dashboard.md) | [HTML](prototype/screens/DASH-001.html) | [PNG](screenshots/DASH-001.png) | E2/E3 design |
| `PAT-001` | Patients | Patient Management | [`04-Patient-Management.md`](../Knowledge_Base/Features/04-Patient-Management.md) | [HTML](prototype/screens/PAT-001.html) | [PNG](screenshots/PAT-001.png) | E2/E3 design |
| `PAT-002` | Patients | Patient Management | [`04-Patient-Management.md`](../Knowledge_Base/Features/04-Patient-Management.md) | [HTML](prototype/screens/PAT-002.html) | [PNG](screenshots/PAT-002.png) | E2/E3 design |
| `PAT-003` | Patients | Patient Management | [`04-Patient-Management.md`](../Knowledge_Base/Features/04-Patient-Management.md) | [HTML](prototype/screens/PAT-003.html) | [PNG](screenshots/PAT-003.png) | E2/E3 design |
| `PAT-004` | Patients | Patient Management | [`04-Patient-Management.md`](../Knowledge_Base/Features/04-Patient-Management.md) | [HTML](prototype/screens/PAT-004.html) | [PNG](screenshots/PAT-004.png) | E2/E3 design |
| `PAT-005` | Patients | Patient Management | [`04-Patient-Management.md`](../Knowledge_Base/Features/04-Patient-Management.md) | [HTML](prototype/screens/PAT-005.html) | [PNG](screenshots/PAT-005.png) | E2/E3 design |
| `PAT-006` | Patients | Patient Management | [`04-Patient-Management.md`](../Knowledge_Base/Features/04-Patient-Management.md) | [HTML](prototype/screens/PAT-006.html) | [PNG](screenshots/PAT-006.png) | E2/E3 design |
| `PAT-007` | Patients | Patient Management | [`04-Patient-Management.md`](../Knowledge_Base/Features/04-Patient-Management.md) | [HTML](prototype/screens/PAT-007.html) | [PNG](screenshots/PAT-007.png) | E2/E3 design |
| `VAC-001` | Vaccinations | Vaccination Management | [`05-Vaccination-Management.md`](../Knowledge_Base/Features/05-Vaccination-Management.md) | [HTML](prototype/screens/VAC-001.html) | [PNG](screenshots/VAC-001.png) | E2/E3 design |
| `VAC-002` | Vaccinations | Vaccination Management | [`05-Vaccination-Management.md`](../Knowledge_Base/Features/05-Vaccination-Management.md) | [HTML](prototype/screens/VAC-002.html) | [PNG](screenshots/VAC-002.png) | E2/E3 design |
| `VAC-003` | Vaccinations | Vaccination Management | [`05-Vaccination-Management.md`](../Knowledge_Base/Features/05-Vaccination-Management.md) | [HTML](prototype/screens/VAC-003.html) | [PNG](screenshots/VAC-003.png) | E2/E3 design |
| `VAC-004` | Vaccinations | Vaccination Management | [`05-Vaccination-Management.md`](../Knowledge_Base/Features/05-Vaccination-Management.md) | [HTML](prototype/screens/VAC-004.html) | [PNG](screenshots/VAC-004.png) | E2/E3 design |
| `VAC-005` | Vaccinations | Vaccination Management | [`05-Vaccination-Management.md`](../Knowledge_Base/Features/05-Vaccination-Management.md) | [HTML](prototype/screens/VAC-005.html) | [PNG](screenshots/VAC-005.png) | E2/E3 design |
| `CON-001` | Consultations | Consultation Management | [`06-Consultation-Management.md`](../Knowledge_Base/Features/06-Consultation-Management.md) | [HTML](prototype/screens/CON-001.html) | [PNG](screenshots/CON-001.png) | E2/E3 design |
| `CON-002` | Consultations | Consultation Management | [`06-Consultation-Management.md`](../Knowledge_Base/Features/06-Consultation-Management.md) | [HTML](prototype/screens/CON-002.html) | [PNG](screenshots/CON-002.png) | E2/E3 design |
| `CON-003` | Consultations | Consultation Management | [`06-Consultation-Management.md`](../Knowledge_Base/Features/06-Consultation-Management.md) | [HTML](prototype/screens/CON-003.html) | [PNG](screenshots/CON-003.png) | E2/E3 design |
| `CON-004` | Consultations | Consultation Management | [`06-Consultation-Management.md`](../Knowledge_Base/Features/06-Consultation-Management.md) | [HTML](prototype/screens/CON-004.html) | [PNG](screenshots/CON-004.png) | E2/E3 design |
| `INV-001` | Inventory | Vaccine and Batch Inventory | [`07-Vaccine-and-Batch-Inventory.md`](../Knowledge_Base/Features/07-Vaccine-and-Batch-Inventory.md) | [HTML](prototype/screens/INV-001.html) | [PNG](screenshots/INV-001.png) | E2/E3 design |
| `INV-002` | Inventory | Vaccine and Batch Inventory | [`07-Vaccine-and-Batch-Inventory.md`](../Knowledge_Base/Features/07-Vaccine-and-Batch-Inventory.md) | [HTML](prototype/screens/INV-002.html) | [PNG](screenshots/INV-002.png) | E2/E3 design |
| `INV-003` | Inventory | Vaccine and Batch Inventory | [`07-Vaccine-and-Batch-Inventory.md`](../Knowledge_Base/Features/07-Vaccine-and-Batch-Inventory.md) | [HTML](prototype/screens/INV-003.html) | [PNG](screenshots/INV-003.png) | E2/E3 design |
| `INV-004` | Inventory | Vaccine and Batch Inventory | [`07-Vaccine-and-Batch-Inventory.md`](../Knowledge_Base/Features/07-Vaccine-and-Batch-Inventory.md) | [HTML](prototype/screens/INV-004.html) | [PNG](screenshots/INV-004.png) | E2/E3 design |
| `INV-005` | Inventory | Vaccine and Batch Inventory | [`07-Vaccine-and-Batch-Inventory.md`](../Knowledge_Base/Features/07-Vaccine-and-Batch-Inventory.md) | [HTML](prototype/screens/INV-005.html) | [PNG](screenshots/INV-005.png) | E2/E3 design |
| `INV-006` | Inventory | Vaccine and Batch Inventory | [`07-Vaccine-and-Batch-Inventory.md`](../Knowledge_Base/Features/07-Vaccine-and-Batch-Inventory.md) | [HTML](prototype/screens/INV-006.html) | [PNG](screenshots/INV-006.png) | E2/E3 design |
| `WAS-001` | Wastage | Wastage | [`08-Wastage.md`](../Knowledge_Base/Features/08-Wastage.md) | [HTML](prototype/screens/WAS-001.html) | [PNG](screenshots/WAS-001.png) | E2/E3 design |
| `WAS-002` | Wastage | Wastage | [`08-Wastage.md`](../Knowledge_Base/Features/08-Wastage.md) | [HTML](prototype/screens/WAS-002.html) | [PNG](screenshots/WAS-002.png) | E2/E3 design |
| `BRW-001` | Borrow & Return | Borrowed and Lent Vaccines | [`09-Borrowed-and-Lent-Vaccines.md`](../Knowledge_Base/Features/09-Borrowed-and-Lent-Vaccines.md) | [HTML](prototype/screens/BRW-001.html) | [PNG](screenshots/BRW-001.png) | E2/E3 design |
| `BRW-002` | Borrow & Return | Borrowed and Lent Vaccines | [`09-Borrowed-and-Lent-Vaccines.md`](../Knowledge_Base/Features/09-Borrowed-and-Lent-Vaccines.md) | [HTML](prototype/screens/BRW-002.html) | [PNG](screenshots/BRW-002.png) | E2/E3 design |
| `BRW-003` | Borrow & Return | Borrowed and Lent Vaccines | [`09-Borrowed-and-Lent-Vaccines.md`](../Knowledge_Base/Features/09-Borrowed-and-Lent-Vaccines.md) | [HTML](prototype/screens/BRW-003.html) | [PNG](screenshots/BRW-003.png) | E2/E3 design |
| `REM-001` | Follow-up | Vaccination Reminders | [`10-Vaccination-Reminders.md`](../Knowledge_Base/Features/10-Vaccination-Reminders.md) | [HTML](prototype/screens/REM-001.html) | [PNG](screenshots/REM-001.png) | E2/E3 design |
| `REM-002` | Follow-up | Vaccination Reminders | [`10-Vaccination-Reminders.md`](../Knowledge_Base/Features/10-Vaccination-Reminders.md) | [HTML](prototype/screens/REM-002.html) | [PNG](screenshots/REM-002.png) | E2/E3 design |
| `REM-003` | Follow-up | Personal Reminders | [`11-Personal-Reminders.md`](../Knowledge_Base/Features/11-Personal-Reminders.md) | [HTML](prototype/screens/REM-003.html) | [PNG](screenshots/REM-003.png) | E2/E3 design |
| `REM-004` | Follow-up | Personal Reminders | [`11-Personal-Reminders.md`](../Knowledge_Base/Features/11-Personal-Reminders.md) | [HTML](prototype/screens/REM-004.html) | [PNG](screenshots/REM-004.png) | E2/E3 design |
| `FIN-001` | Finance | Finance and Payments | [`12-Finance-and-Payments.md`](../Knowledge_Base/Features/12-Finance-and-Payments.md) | [HTML](prototype/screens/FIN-001.html) | [PNG](screenshots/FIN-001.png) | E2/E3 design |
| `FIN-002` | Finance | Finance and Payments | [`12-Finance-and-Payments.md`](../Knowledge_Base/Features/12-Finance-and-Payments.md) | [HTML](prototype/screens/FIN-002.html) | [PNG](screenshots/FIN-002.png) | E2/E3 design |
| `FIN-003` | Finance | Finance and Payments | [`12-Finance-and-Payments.md`](../Knowledge_Base/Features/12-Finance-and-Payments.md) | [HTML](prototype/screens/FIN-003.html) | [PNG](screenshots/FIN-003.png) | E2/E3 design |
| `FIN-004` | Finance | Finance and Payments | [`12-Finance-and-Payments.md`](../Knowledge_Base/Features/12-Finance-and-Payments.md) | [HTML](prototype/screens/FIN-004.html) | [PNG](screenshots/FIN-004.png) | E2/E3 design |
| `FIN-005` | Finance | Finance and Payments | [`12-Finance-and-Payments.md`](../Knowledge_Base/Features/12-Finance-and-Payments.md) | [HTML](prototype/screens/FIN-005.html) | [PNG](screenshots/FIN-005.png) | E2/E3 design |
| `FIN-006` | Finance | Finance and Payments | [`12-Finance-and-Payments.md`](../Knowledge_Base/Features/12-Finance-and-Payments.md) | [HTML](prototype/screens/FIN-006.html) | [PNG](screenshots/FIN-006.png) | E2/E3 design |
| `RCP-001` | Receipts | Receipts and Printing | [`13-Receipts-and-Printing.md`](../Knowledge_Base/Features/13-Receipts-and-Printing.md) | [HTML](prototype/screens/RCP-001.html) | [PNG](screenshots/RCP-001.png) | E2/E3 design |
| `RCP-002` | Receipts | Receipts and Printing | [`13-Receipts-and-Printing.md`](../Knowledge_Base/Features/13-Receipts-and-Printing.md) | [HTML](prototype/screens/RCP-002.html) | [PNG](screenshots/RCP-002.png) | E2/E3 design |
| `RCP-003` | Receipts | Receipts and Printing | [`13-Receipts-and-Printing.md`](../Knowledge_Base/Features/13-Receipts-and-Printing.md) | [HTML](prototype/screens/RCP-003.html) | [PNG](screenshots/RCP-003.png) | E2/E3 design |
| `RPT-001` | Reports | Statistics and Reports | [`15-Statistics-and-Reports.md`](../Knowledge_Base/Features/15-Statistics-and-Reports.md) | [HTML](prototype/screens/RPT-001.html) | [PNG](screenshots/RPT-001.png) | E2/E3 design |
| `RPT-002` | Reports | Statistics and Reports | [`15-Statistics-and-Reports.md`](../Knowledge_Base/Features/15-Statistics-and-Reports.md) | [HTML](prototype/screens/RPT-002.html) | [PNG](screenshots/RPT-002.png) | E2/E3 design |
| `RPT-003` | Reports | Statistics and Reports | [`15-Statistics-and-Reports.md`](../Knowledge_Base/Features/15-Statistics-and-Reports.md) | [HTML](prototype/screens/RPT-003.html) | [PNG](screenshots/RPT-003.png) | E2/E3 design |
| `RPT-004` | Reports | Statistics and Reports | [`15-Statistics-and-Reports.md`](../Knowledge_Base/Features/15-Statistics-and-Reports.md) | [HTML](prototype/screens/RPT-004.html) | [PNG](screenshots/RPT-004.png) | E2/E3 design |
| `AUD-001` | Administration | Audit Logging | [`21-Audit-Logging.md`](../Knowledge_Base/Features/21-Audit-Logging.md) | [HTML](prototype/screens/AUD-001.html) | [PNG](screenshots/AUD-001.png) | E2/E3 design |
| `AUD-002` | Administration | Audit Logging | [`21-Audit-Logging.md`](../Knowledge_Base/Features/21-Audit-Logging.md) | [HTML](prototype/screens/AUD-002.html) | [PNG](screenshots/AUD-002.png) | E2/E3 design |
| `STF-001` | Administration | Staff and Role Management | [`03-Staff-and-Role-Management.md`](../Knowledge_Base/Features/03-Staff-and-Role-Management.md) | [HTML](prototype/screens/STF-001.html) | [PNG](screenshots/STF-001.png) | E2/E3 design |
| `STF-002` | Administration | Staff and Role Management | [`03-Staff-and-Role-Management.md`](../Knowledge_Base/Features/03-Staff-and-Role-Management.md) | [HTML](prototype/screens/STF-002.html) | [PNG](screenshots/STF-002.png) | E2/E3 design |
| `STF-003` | Administration | Staff and Role Management | [`03-Staff-and-Role-Management.md`](../Knowledge_Base/Features/03-Staff-and-Role-Management.md) | [HTML](prototype/screens/STF-003.html) | [PNG](screenshots/STF-003.png) | E2/E3 design |
| `STF-004` | Administration | Staff and Role Management | [`03-Staff-and-Role-Management.md`](../Knowledge_Base/Features/03-Staff-and-Role-Management.md) | [HTML](prototype/screens/STF-004.html) | [PNG](screenshots/STF-004.png) | E2/E3 design |
| `SYS-001` | System | Supabase Synchronization | [`17-Supabase-Sync.md`](../Knowledge_Base/Features/17-Supabase-Sync.md) | [HTML](prototype/screens/SYS-001.html) | [PNG](screenshots/SYS-001.png) | E2/E3 design |
| `SYS-002` | System | Supabase Synchronization | [`17-Supabase-Sync.md`](../Knowledge_Base/Features/17-Supabase-Sync.md) | [HTML](prototype/screens/SYS-002.html) | [PNG](screenshots/SYS-002.png) | E2/E3 design |
| `SYS-003` | System | Local Persistence and Offline Operation | [`16-Local-Persistence-and-Offline-Operation.md`](../Knowledge_Base/Features/16-Local-Persistence-and-Offline-Operation.md) | [HTML](prototype/screens/SYS-003.html) | [PNG](screenshots/SYS-003.png) | E2/E3 design |
| `SYS-004` | System | Application Updates | [`22-Application-Updates.md`](../Knowledge_Base/Features/22-Application-Updates.md) | [HTML](prototype/screens/SYS-004.html) | [PNG](screenshots/SYS-004.png) | E2/E3 design |
| `SYS-005` | System | Backup and Recovery | [`18-Backup-and-Recovery.md`](../Knowledge_Base/Features/18-Backup-and-Recovery.md) | [HTML](prototype/screens/SYS-005.html) | [PNG](screenshots/SYS-005.png) | E2/E3 design |
| `SYS-006` | System | Backup and Recovery | [`18-Backup-and-Recovery.md`](../Knowledge_Base/Features/18-Backup-and-Recovery.md) | [HTML](prototype/screens/SYS-006.html) | [PNG](screenshots/SYS-006.png) | E2/E3 design |
| `SYS-007` | System | Backup and Recovery | [`18-Backup-and-Recovery.md`](../Knowledge_Base/Features/18-Backup-and-Recovery.md) | [HTML](prototype/screens/SYS-007.html) | [PNG](screenshots/SYS-007.png) | E2/E3 design |
| `SET-001` | Settings | Settings | [`20-Settings.md`](../Knowledge_Base/Features/20-Settings.md) | [HTML](prototype/screens/SET-001.html) | [PNG](screenshots/SET-001.png) | E2/E3 design |
| `SET-002` | Settings | Settings | [`20-Settings.md`](../Knowledge_Base/Features/20-Settings.md); [`19-Desktop-Notifications.md`](../Knowledge_Base/Features/19-Desktop-Notifications.md) | [HTML](prototype/screens/SET-002.html) | [PNG](screenshots/SET-002.png) | E2/E3 design |
| `SET-003` | Settings | Settings | [`20-Settings.md`](../Knowledge_Base/Features/20-Settings.md); [`02-Authentication-and-Session.md`](../Knowledge_Base/Features/02-Authentication-and-Session.md) | [HTML](prototype/screens/SET-003.html) | [PNG](screenshots/SET-003.png) | E2/E3 design |
| `SET-004` | Settings | Settings | [`20-Settings.md`](../Knowledge_Base/Features/20-Settings.md) | [HTML](prototype/screens/SET-004.html) | [PNG](screenshots/SET-004.png) | E2/E3 design |

## 5. Decision trace

| Decision | Status | How the design reflects it |
|---|---|---|
| ADR-0008 — reuse existing Supabase project/schema | Accepted | No new backend/project is shown; no project identifier or secret is present |
| ADR-0001 — Go + Wails + React/TypeScript | Proposed | Screens use component language compatible with React; no implementation claim |
| ADR-0002 — SQLite local working copy | Proposed | Offline/local states are designed; persistence is not implemented |
| ADR-0003 — outbox and deletion reconciliation | Proposed | Pending/conflict screens show target behaviour and flag contract gaps |
| ADR-0004 — Supabase Auth in Go, token in OS keychain | Proposed | No token appears in the renderer; auth states are design-only |
| ADR-0005 — typed Wails boundary | Proposed | Renderer is treated as untrusted presentation; no direct Supabase access is implied |
| ADR-0006 — testing/release gates | Proposed | Validation is design-level; no release claim |
| ADR-0007 — money/dates/identity | Proposed | Integer minor units and IST are design constraints; no calculation is claimed |
| D1–D14 | Unapproved | Unresolved policy is labelled in screens and the backlog |

## 6. State trace

The per-screen specifications list the state families that apply. The high-risk states are traced in [`States-and-Errors.md`](States-and-Errors.md):

- authentication/session: `AUTH-001`–`AUTH-005`;
- duplicate/merge/archive: `PAT-002`, `PAT-005`–`PAT-007`;
- stock ledger and batch validity: `INV-004`–`INV-006`, `VAC-002`–`VAC-003`, `WAS-002`;
- receipt/provisional/reprint: `VAC-001`, `RCP-001`–`RCP-003`;
- offline/pending/conflict: `SYS-001`–`SYS-003`;
- destructive restore: `SYS-005`–`SYS-007`;
- role and self-deactivation: `AUTH-004`, `STF-001`–`STF-003`.

## 7. What is not traced

- No requirement ID-level mapping is claimed here. The Knowledge Base requirements and feature specifications remain authoritative; per-screen “Source specification” links provide the trace to the feature level.
- No production test, API contract, schema or RLS policy is traced as implemented.
- No design has been approved by product, clinical, security or legal reviewers.
- No claim is made that every documented edge case has a unique static page. State families are specified per screen and summarized in `States-and-Errors.md`.

## 8. Maintenance rule

When a screen is added, renamed or removed:

1. update the registry in `prototype/tools/build.py`;
2. rebuild the 68 specs/gallery/manifest;
3. update `Screen-Inventory.md` and this trace;
4. re-render the PNG and verify dimensions;
5. update the coverage summary and validation record.

The trace is intentionally generated from the same registry that produces the specs, so count drift is detectable.
