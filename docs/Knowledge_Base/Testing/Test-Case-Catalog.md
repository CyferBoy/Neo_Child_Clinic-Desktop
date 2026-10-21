---
title: Test Case Catalog
doc_status: proposed
evidence: 22 feature specifications + regression matrix + security/database review; no test implemented or executed
updated: 2026-10-21
---

# Test Case Catalog

> **Every test below is planned. None has been implemented or run.** Desktop tests run: 0. IDs are stable; a passing result must record build hash, environment, dataset, and evidence link. Android evidence must not be relabelled as a desktop pass.

## Conventions

| Column | Meaning |
|---|---|
| **ID** | Stable planned identifier. Do not renumber; add a new ID for a changed scenario. |
| **Covers** | Requirement IDs or cross-cutting rule. |
| **Type** | Unit, local integration, contract, security, migration, E2E, manual accessibility, or performance. |
| **Planned check** | Preconditions and expected outcome, stated as a testable assertion. |
| **Status** | Always `Planned` until a real test exists and has run. |

Test data must be synthetic. No production PHI, project URL, key, or live Supabase request is allowed in this catalog's execution without separate approval. Backend tests require an approved non-destructive environment; the exported anon path must not be exercised as a test without authorization.

## Foundation

### Desktop shell — PLAT

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-PLAT-01 | PLAT-001, PLAT-003 | E2E | Launch offline with a populated local DB; shell opens, reads local data, and labels the state local-only. | Planned |
| TC-PLAT-02 | PLAT-002 | E2E | Deep link to a permitted patient; authorization is re-checked; an unauthorized role gets a safe denial. | Planned |
| TC-PLAT-03 | PLAT-003, PLAT-004 | E2E | Toggle offline, syncing, and attention states by keyboard; focus order, labels, and announcements are correct; no stale success is shown. | Planned |
| TC-PLAT-04 | PLAT-001 | E2E | Launch a second instance; the existing window focuses; no second writer opens the DB. | Planned |
| TC-PLAT-05 | UPD-003 | E2E | Trigger an update prompt during a local transaction; the transaction completes before the prompt is actionable. | Planned |

### Authentication and session — AUTH

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-AUTH-01 | AUTH-001, AUTH-002, SEC-002 | E2E | Sign in with valid credentials; role resolves from `app_metadata.role`; no token is exposed to renderer storage or logs. | Planned |
| TC-AUTH-02 | AUTH-002 | Security | Sign in with no role or an unknown role; access is denied, never defaulted to nurse/admin. | Planned |
| TC-AUTH-03 | AUTH-001 | Contract | Expire the access token; refresh succeeds once; concurrent requests share one refresh. | Planned |
| TC-AUTH-04 | AUTH-005 | E2E | Start offline with a previously valid session; local read works within the approved offline window; remote calls fail closed. | Planned |
| TC-AUTH-05 | AUTH-003 | E2E | Deactivate the account server-side; next privileged request is denied and the UI returns to a locked state. | Planned |
| TC-AUTH-06 | AUTH-004, SEC-002 | Security | Sign out with pending outbox rows; tokens are cleared; local clinical data remains protected; no silent wipe. | Planned |
| TC-AUTH-07 | AUTH-004, OFF-006, SEC-004 | Security | Switch accounts without restarting; previous user's cached PHI and search results are not visible. | Planned |

### Staff and roles — STF

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-STF-01 | STF-001, STF-002, STF-006 | Contract | Admin creates staff; profile and Auth identity are consistent; audit records the actor. | Planned |
| TC-STF-02 | STF-005 | Security | Admin attempts self-role change or self-deactivation; blocked server-side, not only in UI. | Planned |
| TC-STF-03 | STF-003, SEC-011 | Contract | Role change refreshes the claim; the old token cannot retain the old role indefinitely. | Planned |
| TC-STF-04 | STF-004 | Contract | Deactivate staff; refresh/session capability is revoked; historical records remain attributable. | Planned |
| TC-STF-05 | STF-001, SEC-003 | Security | Non-admin calls the staff-management function directly; denied. | Planned |

## Clinical

### Patients — PAT

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-PAT-01 | PAT-001, PAT-002 | Local integration | Create a patient offline; patient row and outbox commit atomically; UI says local-only. | Planned |
| TC-PAT-02 | PAT-001, PAT-003, PAT-007 | Unit/integration | Duplicate clinic ID is rejected; duplicate name/phone warns but does not auto-merge. | Planned |
| TC-PAT-03 | PAT-005 | Integration | Merge duplicates; dependents reassign; history remains; audit records the merge. | Planned |
| TC-PAT-04 | PAT-004 | E2E | Open timeline with visits, vaccinations, consultations, payments, reminders; counts match details. | Planned |
| TC-PAT-05 | PAT-006 | Security | Soft-deleted patient is absent from active list, global search, reports, and detail counts; historical financial/audit rows remain. | Planned |
| TC-PAT-06 | PAT-001, PAT-007 | Migration | Import a legacy patient with missing/duplicate clinic ID; dry-run reports conflicts; no partial apply. | Planned |

### Vaccinations — VAC

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-VAC-01 | VAC-001, VAC-002 | Local integration | Record visit with two vaccines, batches, payment, reminder; all local rows and outbox group commit once. | Planned |
| TC-VAC-02 | VAC-003 | Contract | Submit the same event ID twice; server accepts once; retry UI converges. | Planned |
| TC-VAC-03 | VAC-001, VAC-004 | Integration | Attempt expired, insufficient, or negative stock; transaction rolls back fully; no partial payment/reminder. | Planned |
| TC-VAC-04 | VAC-005 | Unit | Edit a two-item vaccine visit; stock diff equals new minus old per batch; payment/receipt identity is preserved. | Planned |
| TC-VAC-05 | VAC-006 | Integration | Delete/reverse a visit; stock and money reverse once; audit and reminder state are correct. | Planned |
| TC-VAC-06 | VAC-007 | Contract | Server assigns receipt number after commit; a timeout is shown as pending, not as a locally invented number. | Planned |
| TC-VAC-07 | SEC-003 | Security | Doctor/nurse/admin matrix for create/edit/delete; UI and backend agree; receptionist cannot record clinical items. | Planned |

### Consultations — CON

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-CON-01 | CON-001, CON-002, CON-005 | Local integration | Create consultation linked to patient and visit; follow-up date appears on the timeline under IST; no orphan; audit written. | Planned |
| TC-CON-02 | CON-003 | Contract | Consultation payment and vaccination payment for one visit count once in finance and reports. | Planned |
| TC-CON-03 | CON-004 | Integration | Edit/delete a consultation with a payment; linked correction preserves receipt/audit and does not duplicate stock or income. | Planned |
| TC-CON-04 | CON-002, SEC-003 | Security | Doctor can create/edit own clinical content; receptionist cannot; admin correction requires audit reason. | Planned |

### Vaccination reminders — REM

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-REM-01 | REM-001 | Unit | Due classification around IST midnight, DST-free `Asia/Kolkata`, and month/year boundaries. | Planned |
| TC-REM-02 | REM-002, REM-003 | Integration | Complete/dismiss/cancel reminder; no further notification; stale update cannot reopen terminal state. | Planned |
| TC-REM-03 | REM-003, REM-004 | Unit | Rescheduling preserves the prior due date/reason; editing/deleting a vaccination reconciles the generated reminder exactly once. | Planned |
| TC-REM-04 | REM-005 | Contract | One due vaccination produces one active reminder; duplicate creates are idempotent. | Planned |
| TC-REM-05 | REM-006 | Security | Reminder list/detail does not expose another clinician's restricted notes; notification payload omits PHI. | Planned |

### Personal reminders — PER

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-PER-01 | PER-001, PER-002 | Unit | Blank date, past date, and missing patient/title validation; explicit error messages. | Planned |
| TC-PER-02 | PER-003 | Integration | Advance reminder state (pending/completed/cancelled); no clinical due date is changed. | Planned |
| TC-PER-03 | PER-001, PER-004 | E2E | Advance amounts are not counted as clinic income unless linked to an approved payment; an undated reminder stays visible and does not notify repeatedly. | Planned |
| TC-PER-04 | PER-005 | Security | Reminder notes are visible only to authorized staff; notification preview is non-identifying. | Planned |

## Inventory

### Vaccine and batch inventory — INV

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-INV-01 | INV-001, INV-002, INV-007 | Local integration | Receive a new batch with expiry/cost; ledger and projection agree; duplicate event is idempotent. | Planned |
| TC-INV-02 | INV-002, INV-003 | Unit | FEFO selection excludes expired batches and prefers earliest usable expiry; manual override is explicit. | Planned |
| TC-INV-03 | INV-006 | Security/gate | Inventory writes are blocked while the exported duplicate-trigger state is unresolved. | Planned |
| TC-INV-04 | INV-003, DB-005 | Integration | Two offline devices consume the last dose; server accepts one and returns a typed conflict to the other. | Planned |
| TC-INV-05 | INV-004 | Unit | Low-stock/out-of-stock boundary is exact; no false “in stock” at zero. | Planned |
| TC-INV-06 | INV-001, INV-005, INV-006 | Migration | Legacy batch balance reconciles to the ledger; a manual adjustment requires reason, actor, audit; mismatch is reported, not silently overwritten. | Planned |

### Wastage — WAS

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-WAS-01 | WAS-001, WAS-003 | Local integration | Record wastage once with reason and batch; stock decreases once; audit written. | Planned |
| TC-WAS-02 | WAS-002 | Integration | Wastage greater than remaining stock is rejected with no partial movement. | Planned |
| TC-WAS-03 | WAS-003, WAS-004 | Security | Only authorized roles record waste; correction requires reason and audit. | Planned |

### Borrowed and lent vaccines — BRW

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-BRW-01 | BRW-001 | Local integration | Record a lend/borrow with batch identity; outstanding balance appears once. | Planned |
| TC-BRW-02 | BRW-004 | Integration | Record a partial return; outstanding decreases; record remains open. | Planned |
| TC-BRW-03 | BRW-002 | Unit | Return exceeding outstanding is rejected; exact-full return closes the record. | Planned |
| TC-BRW-04 | BRW-003, BRW-005 | Integration | Mark lost/damaged; no phantom stock; audit and outstanding status are correct. | Planned |
| TC-BRW-05 | BRW-001, BRW-004 | Contract | Replay a lend/return event; no duplicate balance change. | Planned |

## Money and printing

### Finance — FIN

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-FIN-01 | FIN-001, FIN-002, FIN-004 | Unit | Cash + online equals visit amount; negative/overpayment rejected; exact minor-unit totals. | Planned |
| TC-FIN-02 | FIN-003 | Integration | Split payment creates components but one income identity; dashboard/report count once. | Planned |
| TC-FIN-03 | FIN-005 | Integration | Record expense; it reduces net cash flow but not clinical income; category/date required. | Planned |
| TC-FIN-04 | FIN-006 | Security | Refund/correction requires authorized role, reason, and audit; original row is not deleted. | Planned |
| TC-FIN-05 | FIN-003 | Contract | Timeout after server commit; client retries by identity and does not duplicate payment. | Planned |

### Receipts and printing — RCP

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-RCP-01 | RCP-001, RCP-002 | Contract | Server assigns receipt number; client displays it only after confirmation; FY derives from visit date. | Planned |
| TC-RCP-02 | RCP-004 | E2E | Reprint uses the same number and records actor/time; no new sequence consumed. | Planned |
| TC-RCP-03 | RCP-003, RCP-005 | E2E | Printer unavailable; job remains pending/retryable; no PHI in OS spool/log claims. | Planned |
| TC-RCP-04 | RCP-001 | Unit | Receipt at financial-year boundary and leap day gets the correct series. | Planned |
| TC-RCP-05 | SEC-009, SEC-010, RCP-001, DB-005 | Security | Anon/non-staff cannot call the receipt function or read `receipt_sequences` after remediation. | Planned |
| TC-RCP-06 | RCP-002, RCP-003 | E2E | Preview shows clinic/patient/items/total/receipt; print output matches; no hidden PHI in title. | Planned |

## Insight

### Dashboard — DSH

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-DSH-01 | DSH-001, DSH-004 | Integration | Today's patients, due reminders, low stock, and pending sync counts match their detail queries. | Planned |
| TC-DSH-02 | DSH-001 | Unit | “Today” uses IST across device timezones; boundary at 00:00 IST is tested. | Planned |
| TC-DSH-03 | DSH-003 | E2E | Offline/stale dashboard is labelled; no count claims cloud freshness. | Planned |
| TC-DSH-04 | DSH-002, DSH-005 | Integration | One Realtime event does not rebuild unrelated cards; deleted rows disappear consistently. | Planned |

### Statistics and reports — RPT

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-RPT-01 | RPT-001, RPT-003 | Integration | Date-bounded income counts each visit once across vaccination/consultation paths. | Planned |
| TC-RPT-02 | RPT-002, RPT-005 | Integration | Vaccine grouping uses catalog identity; deleted/merged patients are excluded consistently. | Planned |
| TC-RPT-03 | RPT-001 | Unit | Inclusive start/end dates and IST boundaries; no off-by-one day. | Planned |
| TC-RPT-04 | RPT-004, RPT-006 | Contract | Export/report totals reconcile to detail; a partial failure does not present a complete report. | Planned |
| TC-RPT-05 | RPT-007, SEC-006 | Security | Only admin/doctor see reports; export file is encrypted or explicitly warned; no PHI in logs. | Planned |

## Platform, reliability, and security

### Offline persistence — OFF

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-OFF-01 | OFF-001, OFF-004 | Local integration | Kill the process during a multi-table transaction; committed data survives; partial data is absent. | Planned |
| TC-OFF-02 | OFF-003 | Migration | Run forward migrations on a populated encrypted DB; no data loss; failed migration leaves the original intact. | Planned |
| TC-OFF-03 | OFF-005, ERR-005, PLAT-006 | E2E | Disk full/permission error during local write; UI reports a safe failure and no false success. | Planned |
| TC-OFF-04 | OFF-002, SEC-004 | Security | DB file, WAL, temp files, and crash artifact contain no plaintext PHI when encryption is enabled. | Planned |
| TC-OFF-05 | PLAT-003, ERR-004 | E2E | Local-only, syncing, failed, conflicted, and acknowledged states are distinguishable. | Planned |

### Sync — SYNC

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-SYNC-01 | SYNC-001, SYNC-002 | Contract | Replay the same outbox group; server applies each business effect once. | Planned |
| TC-SYNC-02 | SYNC-001, SYNC-007 | Integration | One member of a group fails; group is not acknowledged; UI shows partial state and repair path. | Planned |
| TC-SYNC-03 | SYNC-006, ERR-001 | Contract | 401 pauses sync for re-auth; no data is discarded; resumed group is intact. | Planned |
| TC-SYNC-04 | SYNC-007, SEC-003 | Security | 403 is treated as authorization failure, not transient retry. | Planned |
| TC-SYNC-05 | SYNC-005 | Integration | 409 by identity reconciles or surfaces conflict; no duplicate row/payment/stock. | Planned |
| TC-SYNC-06 | SYNC-007, ERR-003 | Contract | 429/5xx use bounded backoff and jitter; no unbounded worker chain. | Planned |
| TC-SYNC-07 | SYNC-004 | Integration | Deleted/absent remote row follows the approved deletion contract; local row is not silently resurrected. | Planned |
| TC-SYNC-08 | SYNC-003, SYNC-005 | Integration | Stale pull does not overwrite a newer local edit; conflict is visible. | Planned |
| TC-SYNC-09 | ERR-003, SYNC-007 | Performance | 1,000 queued groups sync with bounded memory and coalesced scheduling. | Planned |

### Backup and restore — BAK

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-BAK-01 | BAK-001, BAK-002, BAK-006 | E2E | Export encrypted backup; restore on clean profile; counts/relationships/audit match. | Planned |
| TC-BAK-02 | BAK-001, BAK-002 | Security | Wrong password and one-byte tamper fail before live DB is touched. | Planned |
| TC-BAK-03 | BAK-003, BAK-004 | E2E | Interrupt restore; previous DB remains usable via safety snapshot. | Planned |
| TC-BAK-04 | BAK-001, BAK-005 | Contract | Unsupported version/schema fails closed with clear recovery instructions. | Planned |
| TC-BAK-05 | BAK-002, AUTH-006, SEC-003 | Security | Restore requires fresh auth and authorized role; different account/clinic requires explicit audited rebind. | Planned |
| TC-BAK-06 | BAK-001, BAK-005, SEC-006 | Security | Backup/temp files contain no plaintext PHI, tokens, or DB keys. | Planned |

### Notifications — NOT

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-NOT-01 | NOT-004 | E2E | OS permission denied; due list still works; no repeated permission nag. | Planned |
| TC-NOT-02 | NOT-001, NOT-003 | Integration | One due item notifies once per approved interval; completed reminder cancels future notification. | Planned |
| TC-NOT-03 | NOT-002, NOT-005, SEC-008 | Security | Notification preview omits patient name/phone/clinical detail; click-through re-checks authorization. | Planned |
| TC-NOT-04 | NOT-003 | Integration | Dismissing a notification does not alter the reminder's clinical status and does not re-notify the same item. | Planned |

### Settings — SET

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-SET-01 | SET-002 | Unit | Invalid thresholds, paths, and formats are rejected with field-level errors. | Planned |
| TC-SET-02 | SET-003, SEC-003 | Security | Admin-only clinic settings are enforced server-side; change is audited. | Planned |
| TC-SET-03 | SET-004 | Security | Settings never store tokens/passwords in plaintext; export excludes secrets. | Planned |
| TC-SET-04 | SET-001, SET-005 | E2E | Local preference change survives restart and does not alter clinic-wide policy. | Planned |

### Audit logging — AUD

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-AUD-01 | AUD-001, AUD-002, DB-006, SEC-005 | Integration | Sensitive action writes actor/action/entity/time; audit row cannot be updated/deleted by a client role. | Planned |
| TC-AUD-02 | AUD-003 | Integration | Offline audit intent syncs with the business group or is visibly unresolved. | Planned |
| TC-AUD-03 | AUD-004, ERR-002, SEC-008 | Security | Audit list/export redacts clinical content and supports date/actor filters. | Planned |
| TC-AUD-04 | AUD-005 | Security | Failed audit write blocks or flags the sensitive action according to the approved rule. | Planned |

### Updates and packaging — UPD

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-UPD-01 | UPD-001, SEC-007 | Security | Unsigned/tampered update is rejected; signature verification fails closed. | Planned |
| TC-UPD-02 | UPD-003 | E2E | Defer update with unsynced or dirty work; no forced restart; prompt state is visible. | Planned |
| TC-UPD-03 | OFF-003, UPD-005 | Migration | Upgrade from previous schema with live local data; migration and rollback/restore path verified. | Planned |
| TC-UPD-04 | UPD-004, SEC-008 | Security | Update check sends no PHI; a failed/tampered update leaves the current version intact and does not block clinical work. | Planned |
| TC-UPD-05 | UPD-002, UPD-005 | Manual | Signed package installs on each supported OS; unsupported/downgrade installs are refused; uninstall/reinstall preserves or safely removes local PHI per policy. | Planned |

## Cross-cutting security and database

| ID | Covers | Type | Planned check | Status |
|---|---|---|---|---|
| TC-SEC-01 | SEC-009 | Security | `anon` has no table/function access for PHI, inventory, finance, receipts, or audit. | Planned |
| TC-SEC-02 | SEC-003, DB-002 | Security | A non-staff authenticated user is denied on every business table/function. | Planned |
| TC-SEC-03 | SEC-003, DB-003, DB-004 | Security | Each active role passes its allowed matrix and fails every denied operation; query review confirms parameterization and minimal PHI column selection. | Planned |
| TC-SEC-04 | SEC-003, SEC-011 | Security | Deactivated/soft-deleted staff are denied even with a still-valid token; role authority is server-controlled. | Planned |
| TC-SEC-05 | SEC-009 | Security | Policy review detects permissive OR leakage; no `{public}` legacy policy widens a target policy. | Planned |
| TC-SEC-06 | SEC-009, SEC-010 | Security | New tables/functions have explicit grants, no anon execution, pinned `search_path`, and a role test. | Planned |
| TC-SEC-07 | SEC-001, SEC-008, PLAT-005, DB-001, ERR-002 | Security | Desktop and Wails diagnostics contain no service-role key, JWT, DB key, or PHI. | Planned |
| TC-SEC-08 | SEC-003 | Security | Storage object access is denied to anon/non-staff and permitted only within the intended patient/staff scope. | Planned |
| TC-SEC-09 | SEC-003 | Security | Realtime subscription authorization is tested with anon/non-staff/active roles; revoked users stop receiving events. | Planned |
| TC-SEC-10 | SEC-009, SEC-010 | Security | Receipt sequence/function is not anon-executable and cannot be called by a non-staff role. | Planned |
| TC-SEC-11 | SEC-010, DB-008 | Migration | Default ACLs for future objects are documented and tested; a newly created table is not silently exposed. | Planned |
| TC-SEC-12 | DB-007 | Security | A redacted project fingerprint proves desktop and Android target the same existing project; no separate backend is configured. | Planned |

## Traceability summary

| Domain | Test IDs |
|---|---|
| Shell | `TC-PLAT-01`–`TC-PLAT-05` |
| Auth/roles | `TC-AUTH-01`–`TC-AUTH-07`, `TC-STF-01`–`TC-STF-05` |
| Patients/clinical | `TC-PAT-*`, `TC-VAC-*`, `TC-CON-*`, `TC-REM-*`, `TC-PER-*` |
| Inventory | `TC-INV-*`, `TC-WAS-*`, `TC-BRW-*` |
| Money/receipts | `TC-FIN-*`, `TC-RCP-*` |
| Insight | `TC-DSH-*`, `TC-RPT-*` |
| Reliability | `TC-OFF-*`, `TC-SYNC-*`, `TC-BAK-*`, `TC-NOT-*`, `TC-SET-*`, `TC-AUD-*`, `TC-UPD-*` |
| Security/database | `TC-SEC-01`–`TC-SEC-12` |

## Related

[[Home]] · [[Testing/Test-Strategy|Test Strategy]] · [[Testing/Regression-Matrix|Regression Matrix]] · [[Roadmap/Requirements-Traceability|Requirements Traceability]] · [[Audits/Performance-Review|Performance Review]] · [[Security/Security-Model|Security Model]] · [[Product/Business-Rules|Business Rules]]
