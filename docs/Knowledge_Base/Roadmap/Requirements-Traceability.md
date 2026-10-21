---
title: Requirements Traceability
doc_status: proposed
evidence: 22 Phase 1 feature specifications + Android source + Phase 0C exports + architecture/security/test review
updated: 2026-10-21
---

# Requirements Traceability

> **All 150 requirements are Missing in the desktop.** The Android reference status is recorded per module in [[Product/Feature-Inventory|Feature Inventory]]. No requirement has a passing desktop test; 126 planned test cases are catalogued but none is implemented or executed.

## Module traceability

This table connects each requirement group to its specification, reference evidence, architecture decision, database dependency, security requirement, and planned tests. The detailed per-ID matrix follows. A link is not a test result.

| Module | Requirements | Spec | Evidence anchor | Architecture / decision | Database dependency | Security requirement | Planned tests |
|---|---|---|---|---|---|---|---|
| Desktop Shell | `PLAT-001..006` (6) | [[Features/01-Desktop-Shell-and-Navigation|01]] | Android `app/` navigation + desktop filesystem | [[Architecture/System-Architecture|System Architecture]]; ADR-0001 | No primary clinical table | SEC-003, SEC-008 | `TC-PLAT-01..05` |
| Authentication | `AUTH-001..006` (6) | [[Features/02-Authentication-and-Session|02]] | Android `core/security/`, `feature/auth/` | ADR-0004; ADR-0005 | Supabase Auth; `profiles`; local session | SEC-002, SEC-011 | `TC-AUTH-01..07` |
| Staff and roles | `STF-001..006` (6) | [[Features/03-Staff-and-Role-Management|03]] | Android `feature/staff/`; `manage-staff` | ADR-0004 | `profiles`; `audit_logs` | SEC-003, SEC-005, SEC-011 | `TC-STF-01..05` |
| Patients | `PAT-001..007` (7) | [[Features/04-Patient-Management|04]] | Android `feature/patient/` | [[Architecture/Data-Flows|Data Flows]] | `patients`, visits, notes, consultations, items, finance, reminders, audit | SEC-003, SEC-004 | `TC-PAT-01..06` |
| Vaccinations | `VAC-001..007` (7) | [[Features/05-Vaccination-Management|05]] | Android `feature/vaccination/` | ADR-0009; ADR-0003 | Visits, items, vaccines, batches, ledger, reminders, finance, receipt | SEC-003, SEC-009 | `TC-VAC-01..07` |
| Consultations | `CON-001..005` (5) | [[Features/06-Consultation-Management|06]] | Android `feature/consultation/` | ADR-0009; ADR-0007 | Consultations, visits, finance, receipt, audit | SEC-003, SEC-005 | `TC-CON-01..04` |
| Inventory | `INV-001..007` (7) | [[Features/07-Vaccine-and-Batch-Inventory|07]] | Android `feature/inventory/` | ADR-0009; Phase 0C §5.2 | Vaccines, batches, ledger, audit | SEC-009, SEC-010 | `TC-INV-01..06` |
| Wastage | `WAS-001..004` (4) | [[Features/08-Wastage|08]] | Android `feature/waste/` | ADR-0009 | Waste, batches, ledger, audit | SEC-003, SEC-005 | `TC-WAS-01..03` |
| Borrow/return | `BRW-001..005` (5) | [[Features/09-Borrowed-and-Lent-Vaccines|09]] | Android `feature/borrowed/` | ADR-0009 | Borrow records/returns, batches, ledger | SEC-003, SEC-005 | `TC-BRW-01..05` |
| Vaccination reminders | `REM-001..006` (6) | [[Features/10-Vaccination-Reminders|10]] | Android `feature/reminder/` | ADR-0007 | Reminders, patients, visits, items, audit | SEC-003, SEC-008 | `TC-REM-01..05` |
| Personal reminders | `PER-001..005` (5) | [[Features/11-Personal-Reminders|11]] | Android `feature/personalreminder/` | ADR-0007 | Personal reminders, patients, vaccines, audit | SEC-003, SEC-008 | `TC-PER-01..04` |
| Finance | `FIN-001..006` (6) | [[Features/12-Finance-and-Payments|12]] | Android `feature/finance/` | ADR-0007; ADR-0009 | Finance, expenses, visits, consultations, receipt | SEC-003, SEC-005 | `TC-FIN-01..05` |
| Receipts/printing | `RCP-001..005` (5) | [[Features/13-Receipts-and-Printing|13]] | Android receipt service + function | ADR-0007; ADR-0009 | Visits, finance, consultations, receipt sequence | SEC-006, SEC-008, SEC-009 | `TC-RCP-01..06` |
| Dashboard | `DSH-001..005` (5) | [[Features/14-Dashboard|14]] | Android `feature/dashboard/` | [[Architecture/Data-Flows|Data Flows]] | Read projections over patients, visits, reminders, batches, finance, todos | SEC-003 | `TC-DSH-01..04` |
| Statistics/reports | `RPT-001..007` (7) | [[Features/15-Statistics-and-Reports|15]] | Android `feature/statistics/` | ADR-0007 | Finance, expenses, visits, items, vaccines, patients, waste | SEC-003, SEC-006 | `TC-RPT-01..05` |
| Local persistence | `OFF-001..006` (6) | [[Features/16-Local-Persistence-and-Offline-Operation|16]] | Android Room/SQLCipher + backup source | ADR-0002; ADR-0010 | Local SQLite, outbox, cursors | SEC-004, SEC-008 | `TC-OFF-01..05` |
| Sync | `SYNC-001..007` (7) | [[Features/17-Supabase-Sync|17]] | Android `core/sync/` | ADR-0003; ADR-0008 | Syncable public tables, outbox, audit | SEC-003, SEC-008, SEC-009 | `TC-SYNC-01..09` |
| Backup/recovery | `BAK-001..006` (6) | [[Features/18-Backup-and-Recovery|18]] | Android `data/backup/` | ADR-0010 | Local snapshot/history; no remote business write | SEC-004, SEC-006 | `TC-BAK-01..06` |
| Notifications | `NOT-001..005` (5) | [[Features/19-Desktop-Notifications|19]] | Android notification path | ADR-0007; Security Model | Reminders, personal reminders, local settings | SEC-008 | `TC-NOT-01..04` |
| Settings | `SET-001..005` (5) | [[Features/20-Settings|20]] | Android `feature/settings/` | ADR-0002 | Local settings; `profiles` display | SEC-004, SEC-008 | `TC-SET-01..04` |
| Audit logging | `AUD-001..005` (5) | [[Features/21-Audit-Logging|21]] | Android `feature/audit/`; `audit_logs` | Security Model; ADR-0009 | `audit_logs`, local audit/outbox | SEC-005, SEC-008 | `TC-AUD-01..04` |
| Application updates | `UPD-001..005` (5) | [[Features/22-Application-Updates|22]] | Android `feature/update/`; `notify-update` | ADR-0006 | No business table; manifest/binary | SEC-007 | `TC-UPD-01..05` |

## Matrix

| Module | Requirement | Desktop status | Test status | Spec |
|---|---|---|---|---|
| Desktop Shell and Navigation | `PLAT-001` | Missing | No desktop test | [[Features/01-Desktop-Shell-and-Navigation|Spec]] |
| Desktop Shell and Navigation | `PLAT-002` | Missing | No desktop test | [[Features/01-Desktop-Shell-and-Navigation|Spec]] |
| Desktop Shell and Navigation | `PLAT-003` | Missing | No desktop test | [[Features/01-Desktop-Shell-and-Navigation|Spec]] |
| Desktop Shell and Navigation | `PLAT-004` | Missing | No desktop test | [[Features/01-Desktop-Shell-and-Navigation|Spec]] |
| Desktop Shell and Navigation | `PLAT-005` | Missing | No desktop test | [[Features/01-Desktop-Shell-and-Navigation|Spec]] |
| Desktop Shell and Navigation | `PLAT-006` | Missing | No desktop test | [[Features/01-Desktop-Shell-and-Navigation|Spec]] |
| Authentication and Session | `AUTH-001` | Missing | No desktop test | [[Features/02-Authentication-and-Session|Spec]] |
| Authentication and Session | `AUTH-002` | Missing | No desktop test | [[Features/02-Authentication-and-Session|Spec]] |
| Authentication and Session | `AUTH-003` | Missing | No desktop test | [[Features/02-Authentication-and-Session|Spec]] |
| Authentication and Session | `AUTH-004` | Missing | No desktop test | [[Features/02-Authentication-and-Session|Spec]] |
| Authentication and Session | `AUTH-005` | Missing | No desktop test | [[Features/02-Authentication-and-Session|Spec]] |
| Authentication and Session | `AUTH-006` | Missing | No desktop test | [[Features/02-Authentication-and-Session|Spec]] |
| Staff and Role Management | `STF-001` | Missing | No desktop test | [[Features/03-Staff-and-Role-Management|Spec]] |
| Staff and Role Management | `STF-002` | Missing | No desktop test | [[Features/03-Staff-and-Role-Management|Spec]] |
| Staff and Role Management | `STF-003` | Missing | No desktop test | [[Features/03-Staff-and-Role-Management|Spec]] |
| Staff and Role Management | `STF-004` | Missing | No desktop test | [[Features/03-Staff-and-Role-Management|Spec]] |
| Staff and Role Management | `STF-005` | Missing | No desktop test | [[Features/03-Staff-and-Role-Management|Spec]] |
| Staff and Role Management | `STF-006` | Missing | No desktop test | [[Features/03-Staff-and-Role-Management|Spec]] |
| Patient Management | `PAT-001` | Missing | No desktop test | [[Features/04-Patient-Management|Spec]] |
| Patient Management | `PAT-002` | Missing | No desktop test | [[Features/04-Patient-Management|Spec]] |
| Patient Management | `PAT-003` | Missing | No desktop test | [[Features/04-Patient-Management|Spec]] |
| Patient Management | `PAT-004` | Missing | No desktop test | [[Features/04-Patient-Management|Spec]] |
| Patient Management | `PAT-005` | Missing | No desktop test | [[Features/04-Patient-Management|Spec]] |
| Patient Management | `PAT-006` | Missing | No desktop test | [[Features/04-Patient-Management|Spec]] |
| Patient Management | `PAT-007` | Missing | No desktop test | [[Features/04-Patient-Management|Spec]] |
| Vaccination Management | `VAC-001` | Missing | No desktop test | [[Features/05-Vaccination-Management|Spec]] |
| Vaccination Management | `VAC-002` | Missing | No desktop test | [[Features/05-Vaccination-Management|Spec]] |
| Vaccination Management | `VAC-003` | Missing | No desktop test | [[Features/05-Vaccination-Management|Spec]] |
| Vaccination Management | `VAC-004` | Missing | No desktop test | [[Features/05-Vaccination-Management|Spec]] |
| Vaccination Management | `VAC-005` | Missing | No desktop test | [[Features/05-Vaccination-Management|Spec]] |
| Vaccination Management | `VAC-006` | Missing | No desktop test | [[Features/05-Vaccination-Management|Spec]] |
| Vaccination Management | `VAC-007` | Missing | No desktop test | [[Features/05-Vaccination-Management|Spec]] |
| Consultation Management | `CON-001` | Missing | No desktop test | [[Features/06-Consultation-Management|Spec]] |
| Consultation Management | `CON-002` | Missing | No desktop test | [[Features/06-Consultation-Management|Spec]] |
| Consultation Management | `CON-003` | Missing | No desktop test | [[Features/06-Consultation-Management|Spec]] |
| Consultation Management | `CON-004` | Missing | No desktop test | [[Features/06-Consultation-Management|Spec]] |
| Consultation Management | `CON-005` | Missing | No desktop test | [[Features/06-Consultation-Management|Spec]] |
| Vaccine and Batch Inventory | `INV-001` | Missing | No desktop test | [[Features/07-Vaccine-and-Batch-Inventory|Spec]] |
| Vaccine and Batch Inventory | `INV-002` | Missing | No desktop test | [[Features/07-Vaccine-and-Batch-Inventory|Spec]] |
| Vaccine and Batch Inventory | `INV-003` | Missing | No desktop test | [[Features/07-Vaccine-and-Batch-Inventory|Spec]] |
| Vaccine and Batch Inventory | `INV-004` | Missing | No desktop test | [[Features/07-Vaccine-and-Batch-Inventory|Spec]] |
| Vaccine and Batch Inventory | `INV-005` | Missing | No desktop test | [[Features/07-Vaccine-and-Batch-Inventory|Spec]] |
| Vaccine and Batch Inventory | `INV-006` | Missing | No desktop test | [[Features/07-Vaccine-and-Batch-Inventory|Spec]] |
| Vaccine and Batch Inventory | `INV-007` | Missing | No desktop test | [[Features/07-Vaccine-and-Batch-Inventory|Spec]] |
| Wastage | `WAS-001` | Missing | No desktop test | [[Features/08-Wastage|Spec]] |
| Wastage | `WAS-002` | Missing | No desktop test | [[Features/08-Wastage|Spec]] |
| Wastage | `WAS-003` | Missing | No desktop test | [[Features/08-Wastage|Spec]] |
| Wastage | `WAS-004` | Missing | No desktop test | [[Features/08-Wastage|Spec]] |
| Borrowed and Lent Vaccines | `BRW-001` | Missing | No desktop test | [[Features/09-Borrowed-and-Lent-Vaccines|Spec]] |
| Borrowed and Lent Vaccines | `BRW-002` | Missing | No desktop test | [[Features/09-Borrowed-and-Lent-Vaccines|Spec]] |
| Borrowed and Lent Vaccines | `BRW-003` | Missing | No desktop test | [[Features/09-Borrowed-and-Lent-Vaccines|Spec]] |
| Borrowed and Lent Vaccines | `BRW-004` | Missing | No desktop test | [[Features/09-Borrowed-and-Lent-Vaccines|Spec]] |
| Borrowed and Lent Vaccines | `BRW-005` | Missing | No desktop test | [[Features/09-Borrowed-and-Lent-Vaccines|Spec]] |
| Vaccination Reminders | `REM-001` | Missing | No desktop test | [[Features/10-Vaccination-Reminders|Spec]] |
| Vaccination Reminders | `REM-002` | Missing | No desktop test | [[Features/10-Vaccination-Reminders|Spec]] |
| Vaccination Reminders | `REM-003` | Missing | No desktop test | [[Features/10-Vaccination-Reminders|Spec]] |
| Vaccination Reminders | `REM-004` | Missing | No desktop test | [[Features/10-Vaccination-Reminders|Spec]] |
| Vaccination Reminders | `REM-005` | Missing | No desktop test | [[Features/10-Vaccination-Reminders|Spec]] |
| Vaccination Reminders | `REM-006` | Missing | No desktop test | [[Features/10-Vaccination-Reminders|Spec]] |
| Personal Reminders | `PER-001` | Missing | No desktop test | [[Features/11-Personal-Reminders|Spec]] |
| Personal Reminders | `PER-002` | Missing | No desktop test | [[Features/11-Personal-Reminders|Spec]] |
| Personal Reminders | `PER-003` | Missing | No desktop test | [[Features/11-Personal-Reminders|Spec]] |
| Personal Reminders | `PER-004` | Missing | No desktop test | [[Features/11-Personal-Reminders|Spec]] |
| Personal Reminders | `PER-005` | Missing | No desktop test | [[Features/11-Personal-Reminders|Spec]] |
| Finance and Payments | `FIN-001` | Missing | No desktop test | [[Features/12-Finance-and-Payments|Spec]] |
| Finance and Payments | `FIN-002` | Missing | No desktop test | [[Features/12-Finance-and-Payments|Spec]] |
| Finance and Payments | `FIN-003` | Missing | No desktop test | [[Features/12-Finance-and-Payments|Spec]] |
| Finance and Payments | `FIN-004` | Missing | No desktop test | [[Features/12-Finance-and-Payments|Spec]] |
| Finance and Payments | `FIN-005` | Missing | No desktop test | [[Features/12-Finance-and-Payments|Spec]] |
| Finance and Payments | `FIN-006` | Missing | No desktop test | [[Features/12-Finance-and-Payments|Spec]] |
| Receipts and Printing | `RCP-001` | Missing | No desktop test | [[Features/13-Receipts-and-Printing|Spec]] |
| Receipts and Printing | `RCP-002` | Missing | No desktop test | [[Features/13-Receipts-and-Printing|Spec]] |
| Receipts and Printing | `RCP-003` | Missing | No desktop test | [[Features/13-Receipts-and-Printing|Spec]] |
| Receipts and Printing | `RCP-004` | Missing | No desktop test | [[Features/13-Receipts-and-Printing|Spec]] |
| Receipts and Printing | `RCP-005` | Missing | No desktop test | [[Features/13-Receipts-and-Printing|Spec]] |
| Dashboard | `DSH-001` | Missing | No desktop test | [[Features/14-Dashboard|Spec]] |
| Dashboard | `DSH-002` | Missing | No desktop test | [[Features/14-Dashboard|Spec]] |
| Dashboard | `DSH-003` | Missing | No desktop test | [[Features/14-Dashboard|Spec]] |
| Dashboard | `DSH-004` | Missing | No desktop test | [[Features/14-Dashboard|Spec]] |
| Dashboard | `DSH-005` | Missing | No desktop test | [[Features/14-Dashboard|Spec]] |
| Statistics and Reports | `RPT-001` | Missing | No desktop test | [[Features/15-Statistics-and-Reports|Spec]] |
| Statistics and Reports | `RPT-002` | Missing | No desktop test | [[Features/15-Statistics-and-Reports|Spec]] |
| Statistics and Reports | `RPT-003` | Missing | No desktop test | [[Features/15-Statistics-and-Reports|Spec]] |
| Statistics and Reports | `RPT-004` | Missing | No desktop test | [[Features/15-Statistics-and-Reports|Spec]] |
| Statistics and Reports | `RPT-005` | Missing | No desktop test | [[Features/15-Statistics-and-Reports|Spec]] |
| Statistics and Reports | `RPT-006` | Missing | No desktop test | [[Features/15-Statistics-and-Reports|Spec]] |
| Statistics and Reports | `RPT-007` | Missing | No desktop test | [[Features/15-Statistics-and-Reports|Spec]] |
| Local Persistence and Offline Operation | `OFF-001` | Missing | No desktop test | [[Features/16-Local-Persistence-and-Offline-Operation|Spec]] |
| Local Persistence and Offline Operation | `OFF-002` | Missing | No desktop test | [[Features/16-Local-Persistence-and-Offline-Operation|Spec]] |
| Local Persistence and Offline Operation | `OFF-003` | Missing | No desktop test | [[Features/16-Local-Persistence-and-Offline-Operation|Spec]] |
| Local Persistence and Offline Operation | `OFF-004` | Missing | No desktop test | [[Features/16-Local-Persistence-and-Offline-Operation|Spec]] |
| Local Persistence and Offline Operation | `OFF-005` | Missing | No desktop test | [[Features/16-Local-Persistence-and-Offline-Operation|Spec]] |
| Local Persistence and Offline Operation | `OFF-006` | Missing | No desktop test | [[Features/16-Local-Persistence-and-Offline-Operation|Spec]] |
| Supabase Synchronization | `SYNC-001` | Missing | No desktop test | [[Features/17-Supabase-Sync|Spec]] |
| Supabase Synchronization | `SYNC-002` | Missing | No desktop test | [[Features/17-Supabase-Sync|Spec]] |
| Supabase Synchronization | `SYNC-003` | Missing | No desktop test | [[Features/17-Supabase-Sync|Spec]] |
| Supabase Synchronization | `SYNC-004` | Missing | No desktop test | [[Features/17-Supabase-Sync|Spec]] |
| Supabase Synchronization | `SYNC-005` | Missing | No desktop test | [[Features/17-Supabase-Sync|Spec]] |
| Supabase Synchronization | `SYNC-006` | Missing | No desktop test | [[Features/17-Supabase-Sync|Spec]] |
| Supabase Synchronization | `SYNC-007` | Missing | No desktop test | [[Features/17-Supabase-Sync|Spec]] |
| Backup and Recovery | `BAK-001` | Missing | No desktop test | [[Features/18-Backup-and-Recovery|Spec]] |
| Backup and Recovery | `BAK-002` | Missing | No desktop test | [[Features/18-Backup-and-Recovery|Spec]] |
| Backup and Recovery | `BAK-003` | Missing | No desktop test | [[Features/18-Backup-and-Recovery|Spec]] |
| Backup and Recovery | `BAK-004` | Missing | No desktop test | [[Features/18-Backup-and-Recovery|Spec]] |
| Backup and Recovery | `BAK-005` | Missing | No desktop test | [[Features/18-Backup-and-Recovery|Spec]] |
| Backup and Recovery | `BAK-006` | Missing | No desktop test | [[Features/18-Backup-and-Recovery|Spec]] |
| Desktop Notifications | `NOT-001` | Missing | No desktop test | [[Features/19-Desktop-Notifications|Spec]] |
| Desktop Notifications | `NOT-002` | Missing | No desktop test | [[Features/19-Desktop-Notifications|Spec]] |
| Desktop Notifications | `NOT-003` | Missing | No desktop test | [[Features/19-Desktop-Notifications|Spec]] |
| Desktop Notifications | `NOT-004` | Missing | No desktop test | [[Features/19-Desktop-Notifications|Spec]] |
| Desktop Notifications | `NOT-005` | Missing | No desktop test | [[Features/19-Desktop-Notifications|Spec]] |
| Settings | `SET-001` | Missing | No desktop test | [[Features/20-Settings|Spec]] |
| Settings | `SET-002` | Missing | No desktop test | [[Features/20-Settings|Spec]] |
| Settings | `SET-003` | Missing | No desktop test | [[Features/20-Settings|Spec]] |
| Settings | `SET-004` | Missing | No desktop test | [[Features/20-Settings|Spec]] |
| Settings | `SET-005` | Missing | No desktop test | [[Features/20-Settings|Spec]] |
| Audit Logging | `AUD-001` | Missing | No desktop test | [[Features/21-Audit-Logging|Spec]] |
| Audit Logging | `AUD-002` | Missing | No desktop test | [[Features/21-Audit-Logging|Spec]] |
| Audit Logging | `AUD-003` | Missing | No desktop test | [[Features/21-Audit-Logging|Spec]] |
| Audit Logging | `AUD-004` | Missing | No desktop test | [[Features/21-Audit-Logging|Spec]] |
| Audit Logging | `AUD-005` | Missing | No desktop test | [[Features/21-Audit-Logging|Spec]] |
| Application Updates | `UPD-001` | Missing | No desktop test | [[Features/22-Application-Updates|Spec]] |
| Application Updates | `UPD-002` | Missing | No desktop test | [[Features/22-Application-Updates|Spec]] |
| Application Updates | `UPD-003` | Missing | No desktop test | [[Features/22-Application-Updates|Spec]] |
| Application Updates | `UPD-004` | Missing | No desktop test | [[Features/22-Application-Updates|Spec]] |
| Application Updates | `UPD-005` | Missing | No desktop test | [[Features/22-Application-Updates|Spec]] |

## Cross-cutting requirements

| ID | Requirement | Spec / authority | Evidence | Planned tests |
|---|---|---|---|---|
| `ERR-001` | Stable error code, safe message, correlation ID | [[Architecture/Error-Handling|Error Handling]] | Target architecture | `TC-SYNC-03`, `TC-SYNC-06`, `TC-OFF-03` |
| `ERR-002` | No raw SQL/HTTP/token/PHI in UI or logs | Error Handling; Security Model | Target + security review | `TC-SEC-07`, `TC-AUD-03` |
| `ERR-003` | Idempotent, bounded retries | Error Handling; ADR-0003 | Target architecture | `TC-SYNC-06`, `TC-SYNC-09` |
| `ERR-004` | Local commit is not reported as cloud-saved | Error Handling; ADR-0003 | Target architecture | `TC-OFF-05` |
| `ERR-005` | Fatal local storage error stops writes safely | Error Handling; ADR-0002 | Target architecture | `TC-OFF-03` |
| `DB-001` | User JWT only; no service role | Access Patterns; Security Model | Target + Android source | `TC-SEC-07` |
| `DB-002` | RLS and grants verified with multiple roles through an approved non-destructive path | Access Patterns; Security Model | Phase 0C export, RLS SQL | `TC-SEC-02..04` |
| `DB-003` | Query only needed columns; no blanket `select *` on PHI | Access Patterns | Target architecture | `TC-SEC-03`, performance review |
| `DB-004` | Parameterized queries and server-side validation | Access Patterns | Target architecture | `TC-SEC-03` |
| `DB-005` | Receipt/stock arithmetic is server-authoritative; anon cannot execute those functions | Access Patterns; ADR-0009 | Phase 0C export | `TC-RCP-05`, `TC-INV-04` |
| `DB-006` | Audit is append-only and attributable | Access Patterns; Security Model | Repository intent + export defect | `TC-AUD-01` |
| `DB-007` | Both clients use the same existing project/schema; no new backend or duplicate remote schema; verify with a redacted fingerprint | Access Patterns; ADR-0008 | Shared Backend Investigation | `TC-SEC-12` |
| `DB-008` | Every new table/function has explicit least-privilege grants and is re-verified after 2026-10-30 | Access Patterns; Security Model | Phase 0C export | `TC-SEC-11` |
| `SEC-001` | No service-role/database credential in client | Security Model; ADR-0004/0005 | Target + Android source | `TC-SEC-07` |
| `SEC-002` | Refresh token only in OS keychain; renderer never receives it | Security Model; ADR-0004 | Target + Android reference | `TC-AUTH-01`, `TC-AUTH-06` |
| `SEC-003` | RLS **and** grants verified with real roles, including `anon`, non-staff, active staff, and deactivated | Security Model; Access Patterns | Phase 0C export | `TC-SEC-02..04`, `TC-SEC-08..10` |
| `SEC-004` | Local PHI encrypted at rest and cleared on logout/lock | Security Model; ADR-0002/0010 | Target + Android reference | `TC-OFF-04`, `TC-AUTH-07` |
| `SEC-005` | Audit append-only and attributable; only approved server/active-staff paths insert | Security Model; ADR-0009 | Repository intent + export defect | `TC-AUD-01` |
| `SEC-006` | Backups/exports encrypted and explicitly initiated | Security Model; ADR-0010 | Target | `TC-BAK-06`, `TC-RPT-05` |
| `SEC-007` | Updates signed and rollback-capable | Security Model; ADR-0006 | Target | `TC-UPD-01`, `TC-UPD-04` |
| `SEC-008` | No PHI/token in logs, crash reports, or telemetry | Security Model | Target + privacy review | `TC-SEC-07`, `TC-AUD-03`, `TC-NOT-03` |
| `SEC-009` | `anon` has no business-table/RPC access; legacy `{public}` policies and nurse fallback fail closed | Security Model; Phase 0C | Export L | `TC-SEC-01`, `TC-SEC-05`, `TC-RCP-05` |
| `SEC-010` | New tables/functions have explicit least-privilege grants and post-Oct-30 verification | Security Model; Database Architecture | Export L + migrations | `TC-SEC-06`, `TC-SEC-11` |
| `SEC-011` | Role authority is server-controlled; client-writable metadata cannot grant privileges | Security Model; ADR-0004 | Export L + Android source | `TC-SEC-04`, `TC-STF-03` |

## Status summary


| Status | Count |
|---|---|
| Requirements defined | 150 |
| Desktop implemented | 0 |
| Planned test cases catalogued | 126 |
| Desktop tests passing | 0 |
| Android reference modules | 22 |
| Desktop feature specs | 22 |

## Related

[[Product/Feature-Inventory|Feature Inventory]] · [[Product/Android-Desktop-Parity|Parity]] · [[Testing/Test-Strategy|Test Strategy]] · [[Roadmap/Desktop-Roadmap|Roadmap]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
