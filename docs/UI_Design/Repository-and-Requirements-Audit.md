# Repository and Requirements Audit

**Audit date:** 21 October 2026  
**Baseline commit:** `9297003 docs: record Phase 0B commit state`  
**Design scope:** documentation and static prototype only, under `docs/UI_Design/`

## 1. Purpose

This audit records what the design package is based on, what actually exists in the repository, and what remains a proposal. It prevents the screen set from implying that desktop functionality has been implemented when it has not.

The audit is deliberately conservative:

- Documentation is evidence of intent, not proof of behaviour.
- Android source is a reference, not a runtime-verified desktop implementation.
- A rendered screen is a design artifact, not a working feature.
- A hidden button is not authorization.
- A pending-sync badge is not a sync implementation.

## 2. Repository baseline

| Check | Result |
|---|---|
| Git repository | Present |
| HEAD | `9297003 docs: record Phase 0B commit state` |
| Pre-existing tracked changes | None before design work |
| Desktop application source | **None** |
| `go.mod` / `wails.json` / `package.json` | Absent |
| `src/` / `app/` / desktop test suite / CI | Absent |
| Knowledge Base | 67 Markdown documents, including 22 feature specifications and 8 ADRs |
| Desktop feature modules | **22 of 22 Missing** |
| Android reference | Present but not executed in this pass |
| Production services contacted | None |
| Production data used | None |
| Commit / push / publish performed | None |

At audit time, the only untracked path after design work is `docs/UI_Design/`. This is intentional: the design package is isolated from production source and from the accepted Knowledge Base.

## 3. What was audited

The design work read and reconciled:

- `Product/Product-Scope.md`, `Product-Vision.md`, `Personas-and-Roles.md`, `Feature-Inventory.md`, `Android-Desktop-Parity.md`
- `Architecture/Frontend-Architecture.md`, `System-Architecture.md`, `Data-Flows.md`, `Offline-and-Sync-Design.md`, `Error-Handling.md`
- All 22 `Features/` specifications
- `Decisions/README.md`, `ADR-0001`–`ADR-0008`
- `Database/Data-Dictionary.md`, `Access-Patterns.md`, `Database-Architecture.md`
- `Audits/Risk-Register.md`, `Initial-Audit.md`, `Phase-0B-Architecture-Review.md`, `Technical-Debt.md`
- `Roadmap/Requirements-Traceability.md`, `Desktop-Roadmap.md`, `Phase-1-Implementation-Plan.md`
- `Security/Security-Model.md`, `Privacy-and-Backup.md`, `Threat-Model.md`
- `Testing/Test-Strategy.md`, `Regression-Matrix.md`

The screen set was checked against the 22 module specifications rather than invented from a generic clinic template. Where the specification did not settle a behaviour, the screen marks it as an open policy or proposal instead of presenting a false certainty.

## 4. Implemented versus planned

| Layer | Status | Meaning for this design |
|---|---|---|
| Desktop shell and navigation | Missing | The shell is a design proposal; no route or window exists |
| Desktop authentication | Missing | Sign-in, session, lock and role screens are proposals |
| Desktop patient, clinical, inventory, finance modules | Missing | Every workflow screen is a target design |
| Desktop local persistence / sync / backup | Missing | Offline, conflict, backup and restore screens are proposals |
| Desktop reports, audit, settings, updates | Missing | No desktop report engine, audit writer or updater exists |
| Android application | Source present, not runtime-verified | Used for business meaning and known edge cases only |
| Shared Supabase backend | Accepted direction (ADR-0008) | Must be reused; no new project, schema or remote database is proposed |
| Local SQLite working copy | Proposed (ADR-0002) | UI shows local-first states as a target, not an implementation |

The Knowledge Base records 5 Android modules as **partially implemented** (inventory, reminders, local persistence, sync, backup), 17 as **unverified**, and 0 as fully verified. None of those statuses transfers to desktop.

## 5. Screen-to-module map

The 68 screens cover all 22 Phase 1 modules, including cross-cutting shell, system and settings surfaces.

| Module | Requirement prefix | Screens | Primary source |
|---|---|---|---|
| Desktop shell and navigation | `PLAT` | `SHELL-001` | `Features/01-Desktop-Shell-and-Navigation.md` |
| Authentication and session | `AUTH` | `AUTH-001`–`AUTH-005` | `Features/02-Authentication-and-Session.md` |
| Staff and role management | `STF` | `STF-001`–`STF-004` | `Features/03-Staff-and-Role-Management.md` |
| Patient management | `PAT` | `PAT-001`–`PAT-007` | `Features/04-Patient-Management.md` |
| Vaccination management | `VAC` | `VAC-001`–`VAC-005` | `Features/05-Vaccination-Management.md` |
| Consultation management | `CON` | `CON-001`–`CON-004` | `Features/06-Consultation-Management.md` |
| Vaccine and batch inventory | `INV` | `INV-001`–`INV-006` | `Features/07-Vaccine-and-Batch-Inventory.md` |
| Wastage | `WAS` | `WAS-001`–`WAS-002` | `Features/08-Wastage.md` |
| Borrowed and lent vaccines | `BRW` | `BRW-001`–`BRW-003` | `Features/09-Borrowed-and-Lent-Vaccines.md` |
| Vaccination reminders | `REM` | `REM-001`–`REM-002` | `Features/10-Vaccination-Reminders.md` |
| Personal reminders | `PER` (screened as `REM-003`–`REM-004`) | `REM-003`–`REM-004` | `Features/11-Personal-Reminders.md` |
| Finance and payments | `FIN` | `FIN-001`–`FIN-006` | `Features/12-Finance-and-Payments.md` |
| Receipts and printing | `RCP` | `RCP-001`–`RCP-003` | `Features/13-Receipts-and-Printing.md` |
| Dashboard | `DSH` | `DASH-001` | `Features/14-Dashboard.md` |
| Statistics and reports | `RPT` | `RPT-001`–`RPT-004` | `Features/15-Statistics-and-Reports.md` |
| Local persistence and offline | `OFF` | Cross-cutting; `SYS-003` | `Features/16-Local-Persistence-and-Offline-Operation.md` |
| Supabase synchronization | `SYNC` | `SYS-001`–`SYS-002` | `Features/17-Supabase-Sync.md` |
| Backup and recovery | `BAK` | `SYS-005`–`SYS-007` | `Features/18-Backup-and-Recovery.md` |
| Desktop notifications | `NOT` | `SET-002` | `Features/19-Desktop-Notifications.md` |
| Settings | `SET` | `SET-001`–`SET-004` | `Features/20-Settings.md` |
| Audit logging | `AUD` | `AUD-001`–`AUD-002` | `Features/21-Audit-Logging.md` |
| Application updates | `UPD` | `SYS-004` | `Features/22-Application-Updates.md` |

`REM-003` and `REM-004` deliberately keep the `REM` screen prefix for navigation consistency even though the Knowledge Base requirement prefix for personal reminders is `PER`. The mapping is recorded in each screen specification and in [`Design-Traceability.md`](Design-Traceability.md).

## 6. Requirements that shaped the UI

The following requirements recur across the feature specifications and are treated as design constraints, not optional polish:

1. **Local-first with visible sync state.** Pending, failed, conflicted and stale data must be distinguishable from synced data.
2. **Server-authoritative identity and authorization.** Route guards are usability controls; RLS and Go services enforce access.
3. **Stable identity and server-assigned receipt numbers.** The renderer must not compute receipt numbers or invent patient identifiers.
4. **Integer money and IST dates.** Display may be localised, but the UI must not imply floating-point money or device-timezone due dates.
5. **Single stock ledger.** Vaccination, waste, borrow and adjustment write stock movements; no screen may imply a direct stock overwrite.
6. **No silent destructive action.** Merge, archive, delete, restore, deactivate and reprint require explicit confirmation, reason and/or audit.
7. **Privacy-safe notifications.** Patient names are hidden by default in OS previews.
8. **No PHI in URLs, browser storage, logs or analytics.** The prototype uses fictional data only.
9. **Keyboard and screen-reader support.** Core workflows must be operable without a mouse.
10. **Open policy must remain visible.** Unresolved decisions are labelled in screens and specifications rather than guessed.

## 7. Decision status at design time

| Decision | Status | Design consequence |
|---|---|---|
| ADR-0008 — reuse existing Supabase project/schema | **Accepted** | No new backend, project, remote database or parallel schema is shown |
| ADR-0001 — Go + Wails + React/TypeScript | Proposed | Screens use React-friendly component language but do not claim an implementation |
| ADR-0002 — SQLite local working copy | Proposed | Offline states are designed; no local database is claimed |
| ADR-0003 — outbox, transaction groups, deletion reconciliation | Proposed | Conflict and pending-write screens show target behaviour and flag contract gaps |
| ADR-0004 — Supabase Auth in Go; tokens in OS keychain | Proposed | The renderer never displays a token; sign-in is a target flow |
| ADR-0005 — typed Wails boundary | Proposed | Renderer reads formatted data only; no direct Supabase access is implied |
| ADR-0006 — testing and release gates | Proposed | Validation is design-level only; no release claim is made |
| ADR-0007 — money, dates, identity | Proposed | Integer minor units and IST are treated as constraints; no calculation is performed in the renderer |
| D1–D14 | Unapproved | Screens flag unresolved policy instead of settling it |

Specific unresolved items surfaced by the designs include:

- final idle-lock and offline-unlock policy;
- deletion/absence reconciliation contract;
- encryption, key custody and backup retention;
- receipt/GST legal policy;
- notification sound, quiet-hours override and retention;
- stock adjustment approval and FEFO enforcement;
- report export permissions;
- restore reconciliation ownership and rollback triggers;
- whether receptionists may see clinical notes;
- whether inventory managers may record vaccinations;
- per-doctor patient restriction and second-person confirmation.

## 8. Design-only boundaries

| Boundary | Status |
|---|---|
| Production Go/React/TypeScript/Android code | Not touched |
| Database, SQL, migrations, RLS, Supabase | Not touched |
| Auth, APIs, dependencies, business rules | Not touched |
| Production data or credentials | Not used |
| Commit, push, publish | Not performed |
| New files outside `docs/UI_Design/` | None |
| Production dependency installation | None; rendering libraries are isolated outside the repository |

The prototype is self-contained: local HTML, local CSS, local JavaScript and local font files. It does not call a backend.

## 9. Risks that directly shaped the UI

| Risk | Design response |
|---|---|
| `RISK-002` / `RISK-003` — schema and RLS uncertainty | No screen claims authorization is implemented; role and permission copy says server-side enforcement is required |
| `RISK-004` — broad active-staff PHI access | Role-scoped navigation, permission-denied states and explicit PHI warnings |
| `RISK-005` — duplicate/corrupt stock movements | Ledger language, batch identity, conflict screen and no direct stock overwrite |
| `RISK-006` / `RISK-007` — duplicate sync and resurrection | Pending-write, stale-data, conflict and deletion-reconciliation states |
| `RISK-008` / `RISK-009` — local PHI and token exposure | No tokens in the renderer, device-lock and local-data screens, privacy-safe previews |
| `RISK-010` — receipt number integrity | Server-assigned receipt copy; reprint never renumbers |
| `RISK-012` — destructive restore | Preview, safety snapshot, typed confirmation and failure-preservation language |
| `RISK-013` — date/timezone drift | IST labels, explicit due-date copy and timezone warnings |
| `RISK-018` — printing leaks PHI | Print preview, explicit fields, duplicate marker and no extra PHI |
| `RISK-019` — wrong backend/project | No project identifier or secret in any artifact; same-project requirement is stated as a gate |

## 10. Assumptions and limitations

**Assumptions**

- The Android app remains the functional reference for business meaning.
- The clinic operates in IST for reporting.
- Staff use individual accounts; shared logins are not acceptable.
- The desktop will use the existing Supabase project and schema.
- A local working copy is the intended offline model, subject to ADR approval.
- Existing Android clients may continue writing to the same tables; the deployment plan is unknown.

**Limitations**

- No desktop implementation exists to inspect.
- Android was not executed; its status is source/KB-based.
- The prototype uses static HTML; interactions are limited to local UI behaviour.
- No screen-reader, browser-matrix or automated accessibility test was run.
- The screenshots are design references, not acceptance evidence for a product.
- Counts, identifiers, amounts and clinical text are fictional.

## 11. Conclusion

The repository supports a design package, not an implementation claim. The 68 screens are traceable to the 22 module specifications and the accepted/known architecture. The design deliberately keeps unresolved policy visible, avoids production dependencies and does not cross the boundary into implementation.

Implementation must wait for explicit approval and for the Phase 0B blockers and ADR decisions that affect UI behaviour to be resolved or explicitly accepted.
