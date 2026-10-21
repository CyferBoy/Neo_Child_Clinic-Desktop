---
title: Documentation Validation — Second Pass
doc_status: baseline
evidence: validation and correction pass against Android source at ca4bed4, 23 migrations, two CSV snapshots, repository state + Phase 0B recheck + Phase 0C metadata exports (addendum)
updated: 2026-10-21
---

# Documentation Validation — Second Pass

> **Validation and correction pass.** This pass checked every pre-existing desktop Knowledge Base note (63) and every installed skill (17) against Android source at `ca4bed4`, repository migrations, the two CSV snapshots, tests, and the desktop Git state. Verified documentation and skill corrections were applied; no application source, schema, migration, RLS policy, or dependency was changed.

> **Phase 0C addendum (2026-10-21).** The PASS/PARTIAL/FAIL verdicts below are retained as the 2026-10-20 pre-correction snapshot. A 16-file metadata export now narrows several blocked live-evidence items and changes two material conclusions: the **live database still has duplicate stock triggers/the old function**, despite the client-side fix noted under VAL-011; and the exported RLS/ACL state contains a critical anon path. The current evidence layer is [[Audits/Phase-0C-Schema-Export-Review|Phase 0C Schema Export Review]]; this note is not a current security certification.

> **Verdict convention.** `PASS` means the document's claims were supported and its links/structure were valid. `PARTIAL` means the document was usable but had a stale reference, imprecise status, or ambiguity. `FAIL` means a material claim was wrong, unsupported, or internally contradictory. `BLOCKED` is reserved for claims that require live Supabase or GitHub metadata that was unavailable. Verdicts below are the **pre-correction** result; the correction column records the applied fix.

## 1. Verdict summary

| Set | PASS | PARTIAL | FAIL | BLOCKED | Total |
|---|---:|---:|---:|---:|---:|
| Pre-existing Knowledge Base documents | 20 | 25 | 18 | 0 | 63 |
| Installed skills | 0 | 17 | 0 | 0 | 17 |
| **Combined** | **20** | **42** | **18** | **0** | **80** |
| Live-evidence items (separate from document quality) | — | — | — | 8 | 8 |

No document was marked `BLOCKED` merely because it correctly labels live state as unknown. The eight live-evidence blockers are listed in section 6 and are not documentation defects.

## 2. Document matrix

### Audits

| Document | Verdict | Severity | Evidence checked | Correction applied |
|---|---|---|---|---|
| [[Audits/Final-Report|Final Report]] | FAIL | High | Android source/Bug Register at `ca4bed4`; Git state; counts | Replaced stale defect list with fixed/open split; corrected 10/12 to 5/17; removed tombstone/RPC assumptions; qualified branch protection; corrected backup and database wording |
| [[Audits/Initial-Audit|Initial Audit]] | FAIL | High | Bug Register; source at `ca4bed4`; local Git only | Corrected AUD-002 branch-protection claim and AUD-008 defect status; qualified remote-database wording |
| [[Audits/Risk-Register|Risk Register]] | FAIL | High | NCC-023/025/027/030/038/039; receipt functions; backup source | Replaced stale defect/tombstone/RPC claims with current evidence and deletion-contract risk |
| [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] | FAIL | Medium | CSV headers; migration policy loops; current Bug Register | Corrected the “same seven CSV fields” error; removed tombstone assumptions; clarified local SQLite versus remote database |
| [[Audits/Technical-Debt|Technical Debt]] | FAIL | Medium | Sync source; Bug Register; migrations | Corrected “last-write-wins” characterization, fixed trigger/backup status, and replaced tombstone policy wording |

### Architecture

| Document | Verdict | Severity | Evidence checked | Correction applied |
|---|---|---|---|---|
| [[Architecture/Cache-Strategy|Cache Strategy]] | FAIL | Medium | `PatientCache`, `PatientEntity`, invalidation source | Removed unsupported stale-history claim; replaced with source-supported cache boundary |
| [[Architecture/Data-Flows|Data Flows]] | FAIL | Medium | Shared schema/migrations; Android pull behavior | Replaced tombstone pull claims with soft-delete fields plus unresolved deletion contract |
| [[Architecture/Error-Handling|Error Handling]] | PASS | — | Proposed codes and boundaries | No change |
| [[Architecture/Frontend-Architecture|Frontend Architecture]] | PASS | — | Proposed renderer boundary | No change |
| [[Architecture/Go-Backend-Architecture|Go Backend Architecture]] | PARTIAL | Low | ADR-0002/0008; local schema wording | Clarified local physical projection versus remote contract; local SQLite is expected |
| [[Architecture/Offline-and-Sync-Design|Offline and Sync Design]] | FAIL | High | NCC-009/019/020/023/038/039; sync source | Split fixed defects from remaining gaps; added explicit deletion-contract section; corrected restore and stock wording |
| [[Architecture/System-Architecture|System Architecture]] | FAIL | Medium | ADR-0008; local SQLite design | Qualified remote database wording; removed “no desktop-only database” contradiction; fixed tombstone layer description |

### Database

| Document | Verdict | Severity | Evidence checked | Correction applied |
|---|---|---|---|---|
| [[Database/Access-Patterns|Access Patterns]] | FAIL | High | PostgREST call count; `refreshPatients`; trigger migrations; RLS intent | Removed stale N+1 claim; retained the trigger double-apply as unresolved and Phase 0C now reports it live; replaced tombstone pull steps; clarified local SQLite |
| [[Database/Data-Dictionary|Data Dictionary]] | PASS | — | Desktop CSV: 24 tables, 416 columns; section counts | No change |
| [[Database/Database-Architecture|Database Architecture]] | FAIL | Medium | 23 migrations; RLS loops; policy occurrences; CSV tables | Corrected RLS coverage to 25 tables; replaced unreliable 37-policy count; fixed tombstone and remote-contract wording |

### Decisions

| Document | Verdict | Severity | Evidence checked | Correction applied |
|---|---|---|---|---|
| [[Decisions/ADR-0001-Desktop-Stack|ADR-0001]] | PASS | — | Stack direction; shared backend compatibility | No change |
| [[Decisions/ADR-0002-Local-Persistence|ADR-0002]] | PARTIAL | Medium | SQLite design; ADR-0008 contract | Clarified separate local physical schema versus shared remote contract |
| [[Decisions/ADR-0003-Offline-Sync|ADR-0003]] | FAIL | High | NCC-009/019/020/023; sync source | Moved fixed defects to historical evidence; added unresolved deletion contract; corrected pull and validation rules |
| [[Decisions/ADR-0004-Authentication-and-Session|ADR-0004]] | PASS | — | Android auth/session source; target boundary | No change |
| [[Decisions/ADR-0005-Wails-Boundary|ADR-0005]] | PASS | — | Stack direction; trust boundary | No change |
| [[Decisions/ADR-0006-Testing-and-Release|ADR-0006]] | PASS | — | Test/release evidence | No change |
| [[Decisions/ADR-0007-Money-Dates-and-Identity|ADR-0007]] | PARTIAL | Low | Schema types; deletion evidence | Replaced tombstone policy with approved deletion/absence contract |
| [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]] | PARTIAL | Medium | Explicit decision; local SQLite permission | Clarified “same contract” as remote-facing; distinguished local SQLite from a remote backend; corrected validation wording |
| [[Decisions/README|Decision Log]] | PARTIAL | Low | ADR-0003 status | Replaced tombstone summary with deletion reconciliation (contract TBD) |

### Features

| Document | Verdict | Severity | Evidence checked | Correction applied |
|---|---|---|---|---|
| [[Features/01-Desktop-Shell-and-Navigation|01 Shell and Navigation]] | PASS | — | Source paths; proposed behavior | No change |
| [[Features/02-Authentication-and-Session|02 Authentication and Session]] | PASS | — | Auth source; role/session claims | No change |
| [[Features/03-Staff-and-Role-Management|03 Staff and Roles]] | PASS | — | Staff source; edge function | No change |
| [[Features/04-Patient-Management|04 Patient Management]] | PARTIAL | Medium | Patient validation; `PatientCache`; source at HEAD | Changed to Unverified; removed unsupported stale-cache defect |
| [[Features/05-Vaccination-Management|05 Vaccination Management]] | PARTIAL | Medium | Vaccination transaction; Bug Register | Changed to Unverified; marked historical stock/retry defects fixed |
| [[Features/06-Consultation-Management|06 Consultation Management]] | PASS | — | Proposed workflow; links | No change |
| [[Features/07-Vaccine-and-Batch-Inventory|07 Inventory]] | PARTIAL | Medium | NCC-016/017/021/027/030; migrations | Retained Partial; replaced fixed-defect note with open low-severity gaps |
| [[Features/08-Wastage|08 Wastage]] | PASS | — | Proposed workflow; links | No change |
| [[Features/09-Borrowed-and-Lent-Vaccines|09 Borrow and Return]] | PASS | — | Proposed workflow; links | No change |
| [[Features/10-Vaccination-Reminders|10 Reminders]] | FAIL | High | NCC-023; reminder source | Retained Partial; removed tombstone defect; made deletion contract an explicit blocker |
| [[Features/11-Personal-Reminders|11 Personal Reminders]] | PARTIAL | Medium | NCC-034 reclassification | Changed to Unverified; removed blank-date “defect” |
| [[Features/12-Finance-and-Payments|12 Finance and Payments]] | PASS | — | Finance source; proposed rules | No change |
| [[Features/13-Receipts-and-Printing|13 Receipts and Printing]] | PASS | — | Receipt function/migration; proposed workflow | No change |
| [[Features/14-Dashboard|14 Dashboard]] | PASS | — | Dashboard source; proposed flow | No change |
| [[Features/15-Statistics-and-Reports|15 Statistics]] | PARTIAL | Medium | NCC-008/041; source | Changed to Unverified; marked double-count/filter defects fixed |
| [[Features/16-Local-Persistence-and-Offline-Operation|16 Local Persistence]] | PARTIAL | Medium | NCC-039; Room/source | Retained Partial; recorded open singleton and deletion-contract gaps |
| [[Features/17-Supabase-Sync|17 Supabase Sync]] | FAIL | High | NCC-009/019/020/023/025/038 | Retained Partial; corrected historical defects and tombstone requirements |
| [[Features/18-Backup-and-Recovery|18 Backup and Recovery]] | PARTIAL | Medium | NCC-037; backup source/tests | Retained Partial; corrected test coverage and crypto wording |
| [[Features/19-Desktop-Notifications|19 Notifications]] | PARTIAL | Medium | NCC-033/035; notification source | Changed to Unverified; removed stale defect note |
| [[Features/20-Settings|20 Settings]] | PASS | — | Settings source; proposed flow | No change |
| [[Features/21-Audit-Logging|21 Audit Logging]] | PASS | — | Audit source; append-only intent | No change |
| [[Features/22-Application-Updates|22 Application Updates]] | PASS | — | Update source; proposed flow | No change |

### Product

| Document | Verdict | Severity | Evidence checked | Correction applied |
|---|---|---|---|---|
| [[Product/Android-Desktop-Parity|Android-Desktop Parity]] | FAIL | High | Bug Register/source at HEAD | Corrected ten module statuses/reasons; split fixed defects from open gaps |
| [[Product/Feature-Inventory|Feature Inventory]] | FAIL | High | All 22 modules; Bug Register | Corrected 10/12 to 5/17 and reclassified six modules |
| [[Product/Personas-and-Roles|Personas and Roles]] | PASS | — | `UserRole`; UI gates; RLS caveat | No change |
| [[Product/Product-Scope|Product Scope]] | PARTIAL | Low | ADR-0008; local SQLite | Qualified remote-database wording |
| [[Product/Product-Vision|Product Vision]] | PARTIAL | Medium | Bug Register; ADR-0008; deletion evidence | Replaced stale defect claim, tombstone principle, and remote-database ambiguity |

### Releases, Roadmap, Security, Testing, Root

| Document | Verdict | Severity | Evidence checked | Correction applied |
|---|---|---|---|---|
| [[Releases/Release-Checklist|Release Checklist]] | PARTIAL | Low | Release gates; ADR-0008 | Replaced tombstone gate and qualified remote database |
| [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] | PARTIAL | Medium | Phase gates; receipt functions; Git state | Replaced tombstone/RPC wording; qualified branch protection and remote database |
| [[Roadmap/Dependencies-and-Milestones|Dependencies and Milestones]] | PARTIAL | Medium | Milestone graph/table | Fixed M7/M8 critical-path inconsistency; replaced tombstone test |
| [[Roadmap/Phase-1-Implementation-Plan|Phase 1 Implementation Plan]] | PARTIAL | Medium | Workstreams; local/remote boundary | Replaced tombstone wording; clarified branch protection and remote database |
| [[Roadmap/Requirements-Traceability|Requirements Traceability]] | PARTIAL | Low | 138 requirement rows | Qualified DB-007 with local SQLite/remote boundary |
| [[Security/Privacy-and-Backup|Privacy and Backup]] | PARTIAL | Medium | Backup source/tests | Corrected “no automated tests” and crypto/atomicity overstatement |
| [[Security/Security-Model|Security Model]] | PARTIAL | Medium | NSC-013; migration functions | Named live-only `get_my_role()` and distinguished pinned migration functions; qualified remote database |
| [[Security/Threat-Model|Threat Model]] | PARTIAL | Low | ADR-0008 boundary | Qualified remote database and local SQLite |
| [[Testing/Regression-Matrix|Regression Matrix]] | FAIL | High | Bug Register; fixed/open defects | Replaced stale defect risks for 8 rows; corrected tombstone test wording |
| [[Testing/Test-Strategy|Test Strategy]] | PARTIAL | Medium | Sync/delete tests; local DB boundary | Replaced tombstone suite, qualified deletion test as blocked, clarified local SQLite |
| [[Home|Home]] | FAIL | High | Counts; Git state; branch protection | Corrected 5/17 status, added validation link, qualified branch protection and remote database |
| [[README|Knowledge Base Entry]] | PARTIAL | Low | ADR-0008; local SQLite | Added validation link; qualified remote database and local SQLite |

## 3. Skill matrix

All 17 skills use the V2 directory form `.opencode/skills/<id>/SKILL.md` with valid `name` and `description` frontmatter. Sixteen skills had the same low-severity step-1 grammar corruption (`Then read, ...` or `Then read and ...`); all 17 assumed a root/nested `AGENTS.md` that does not exist. All were corrected; no skill was deleted or renamed.

| Skill | Verdict | Severity | Correction applied |
|---|---|---|---|
| `api-database-documenter` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `architecture-documenter` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `bug-and-debt-tracker` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `change-impact-analyzer` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `data-flow-auditor` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `documentation-sync` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `feature-inventory` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `feature-specification` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `implementation-planner` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `knowledge-base-manager` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `performance-auditor` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `product-roadmap` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `project-audit` | PARTIAL | Low | Made `AGENTS.md`/config reads conditional |
| `release-documenter` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `requirements-traceability` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `security-review` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |
| `test-strategy-planner` | PARTIAL | Low | Fixed step-1 grammar; made `AGENTS.md` conditional |

## 4. Material findings and exact corrections

| ID | Finding | Evidence | Severity | Correction | Status |
|---|---|---|---|---|---|
| VAL-001 | Multiple docs treated fixed Android defects as current | `ca4bed4`; commits `b27d945`, `dbc5986`, `8b14795`; Bug Register | High | Rewrote status/risk/regression text to fixed-versus-open split | Corrected |
| VAL-002 | Desktop design assumed a server tombstone feed absent from repository evidence | NCC-023; migrations; Android source; live state unverified | High | Replaced with explicit deletion/absence contract; blocked delete test until approved | Corrected |
| VAL-003 | Android feature status was inflated to 10 partial / 12 unverified | Current Bug Register and source | High | Recomputed 5 partial / 17 unverified | Corrected |
| VAL-004 | `PatientCache` was said to serve stale patient history | `PatientCache` stores only `PatientEntity`; no history relation | Medium | Removed claim; documented actual cache boundary | Corrected |
| VAL-005 | RLS coverage was reported as 13 tables and 37 policies | 18 literal enables + loops; 56 `CREATE POLICY` occurrences | Medium | Reported 25-table union and non-reproducible policy count | Corrected |
| VAL-006 | Both CSV snapshots were said to use the same seven fields | CSV headers differ | Medium | Recorded each header exactly | Corrected |
| VAL-007 | “No separate desktop database” contradicted permitted local SQLite | ADR-0002 vs ADR-0008 wording | Medium | Qualified all relevant claims as remote PostgreSQL; local SQLite explicit | Corrected |
| VAL-008 | Android backup was said to have no automated tests and several crypto/atomicity gaps | `BackupCryptoTest`, `BackupValidatorTest`; NCC-037 fixed | Medium | Specified no end-to-end restore test; crypto/validator tests exist | Corrected |
| VAL-009 | Branch protection was reported absent | Repository contents cannot prove GitHub settings | Medium | Changed to “not verifiable; confirm in GitHub settings” | Corrected |
| VAL-010 | `refreshPatients` N+1 was reported as current | Fixed at `b27d945`; batched source | Low | Marked historical; retained set-based guidance | Corrected |
| VAL-011 | Trigger double-apply was reported as current | 2026-10-20 migration review appeared to fix it; the Phase 0C export reports two live stock triggers and the old `update_batch_stock()` | High | Reclassified from fixed to unresolved: `20261017` did not take effect and its guard would fail as written; keep inventory writes blocked | Reopened |
| VAL-012 | M8 critical path omitted M7 while the milestone table required it | Roadmap graph/table | Medium | Added the M6/M7 gate before M8 | Corrected |
| VAL-013 | “Server receipt RPC” implied an RPC call | No `postgrest.rpc` calls; receipt logic is trigger/function driven | Low | Renamed to server receipt numbering | Corrected |
| VAL-014 | NSC-013 was described generically | It is the live-only legacy `get_my_role()`; 13 migration functions pin `search_path` | Low | Named the function and recorded the migration fact | Corrected |
| VAL-015 | 16 of 17 skills had step-1 grammar corruption; all 17 assumed `AGENTS.md` | Skill bodies | Low | Fixed grammar; made absent instruction/config reads conditional | Corrected |
| VAL-016 | Architecture gates named only ADR-0002–ADR-0005, omitting ADR-0001/0006/0007 | ADR index shows ADR-0001 through ADR-0007 are proposed | Medium | Updated gates to require all seven proposed ADRs to be accepted | Corrected |

## 5. Post-correction result

- All 43 pre-existing notes with a `PARTIAL` or `FAIL` verdict were corrected.
- The 20 `PASS` notes were left unchanged in the second pass; the Phase 0B recheck later corrected Data Dictionary key rows and money-type wording in affected notes (see addendum).
- The repository root `README.md` was also corrected for remote-database and deletion wording; it is outside the 63-note matrix.
- All 17 skills were corrected without renaming or changing their frontmatter contract.
- No application source, migration, RLS policy, schema, dependency, credential, or Android file was modified.

## 6. Live evidence blocked

| # | Missing evidence | Why it matters | Required source |
|---|---|---|---|
| B-01 | Actual Supabase project identity, URL, and publishable key | Same-project reuse cannot be proven | Approved secure configuration channel; redacted fingerprint |
| B-02 | Live schema/catalog and constraints | CSVs have no keys/indexes/policies/grants; ordinal gaps are not omission proof | Read-only catalog export |
| B-03 | Live RLS, roles, and grants | Migration SQL is intent, not deployed state | Approved role/RLS verification |
| B-04 | Live triggers, functions, and `search_path` | NSC-013 and stock/receipt behavior cannot be certified from repo | Read-only `pg_proc`/trigger inspection |
| B-05 | Storage and Realtime configuration | Private bucket and channel behavior are unverified live | Read-only Storage/Realtime evidence |
| B-06 | GitHub branch protection and About metadata | Not readable from Git objects; only SSH Git access was available | Authenticated GitHub API or manual settings evidence |
| B-07 | Android runtime/Gradle/instrumented test results | Historical 277-test result was not re-run | CI run or local Gradle execution |
| B-08 | Desktop implementation/build/tests | No Go/Wails/React source exists | Phase 0 implementation |

## 7. Residual observations

- The Android Bug Register's NCC-007 index row says Fixed while its detail row still says Open. It was not used as evidence for any desktop claim; resolve it in the Android vault before citing.
- `inventory_deductions` is local-only (NCC-038). It is a missing sync feature/decision, not a current server-side defect.
- The deletion contract is an architecture decision gap, not a documentation typo. Sync implementation remains blocked until it is approved.
- No live vulnerability or live policy-correctness claim is made by this pass.

## 8. Readiness

| Question | Answer |
|---|---|
| Is the documentation ready for architecture review? | Yes, after the verified corrections above. |
| Is the architecture approved? | No. ADR-0008 is accepted; ADR-0001 through ADR-0007 remain proposed. ADR-0003 needs an approved deletion contract. |
| Is the desktop implementation ready to start? | No. Phase 0 gates, live backend verification, and ADR approvals are still open. |
| Is live security verified? | No. Live RLS/grants/functions/Storage are `BLOCKED` (section 6). |
| Are there unresolved documentation errors? | No known material error remains after the Phase 0B corrections (P0B-DOC-01 and P0B-DOC-02). Live-state claims remain unverified. |

## 9. Phase 0B addendum (2026-10-20)

The Phase 0B recheck extended the validation without regenerating the 63-note matrix or the 17 skills.

- **Counts:** the dual-snapshot discrepancy is reconciled at file level. Desktop 24 tables/416 columns; Android 23/361; the 55-row delta is `45 + 4 + 3 + 3` from soft-delete additions, the `waste_records` rename, and `api_write_rate_limits`. The Android snapshot brackets between `20260911` and `20260919`; the desktop snapshot is after `20260929` `[INFERRED, high]`.
- **Baseline:** migrations create 9 of 24 tables. The other 15 are baseline tables present in both snapshots, not evidence of missing production tables. `20261016` explicitly records one missing migration and manual application; a live catalog is still required.
- **P0B-DOC-01:** `Data-Dictionary` listed `patients → vaccination_items` by `patient_id` and `patient_visits → vaccination_items` by `visit_id`; `vaccination_items` has `vaccination_id`. Corrected to `patients → patient_visits` and `patient_visits → vaccination_items (vaccination_id)`.
- **P0B-DOC-02:** several notes said the shared schema uses floating-point money. The CSV shows `numeric` amounts (and `expenses.amount_paise bigint`); the floating risk is the Android `Double`/client calculation and boundary conversion. Corrected in the Data Dictionary, Database Architecture, Product Vision, Technical Debt, and ADR-0007 context without changing ADR status.
- **No status changes:** ADR-0008 remains accepted; ADR-0001–ADR-0007 remain proposed. No live security control is verified.

New notes: [[Database/Schema-Reconciliation|Schema Reconciliation]], [[Database/Live-Verification-Queries|Live Verification Queries]], and [[Audits/Phase-0B-Architecture-Review|Phase 0B Architecture Review]]. Read them with the historical matrix above; the 18 FAIL/25 PARTIAL verdicts are not current defect counts.

## 10. Related

[[Home]] · [[Audits/Final-Report|Final Report]] · [[Audits/Phase-0B-Architecture-Review|Phase 0B Architecture Review]] · [[Database/Schema-Reconciliation|Schema Reconciliation]] · [[Database/Live-Verification-Queries|Live Verification Queries]] · [[Audits/Initial-Audit|Initial Audit]] · [[Audits/Shared-Backend-Connection-Investigation|Shared Backend Investigation]] · [[Product/Feature-Inventory|Feature Inventory]] · [[Roadmap/Desktop-Roadmap|Desktop Roadmap]] · [[Decisions/ADR-0008-Shared-Supabase-Backend|ADR-0008]]
