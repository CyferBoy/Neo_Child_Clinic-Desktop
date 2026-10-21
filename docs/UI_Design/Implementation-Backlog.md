# Implementation Backlog

**Status:** design-only. **No implementation is authorized by this document.**  
**Do not start production UI work until the user explicitly approves it and the Phase 0B blockers are resolved or explicitly accepted.**

This backlog translates the 68-screen design package into implementation-sized work. It deliberately contains **no dates, story points or delivery estimates**. The repository has no desktop source, so every item is a proposal.

## 1. Preconditions

### 1.1 Approval gates

- [ ] Product owner approves the design direction and screen set.
- [ ] Clinical reviewer approves clinical wording, identity safeguards and destructive flows.
- [ ] Security reviewer approves auth/session, PHI handling, local storage and audit visibility.
- [ ] Finance/receipt policy owner approves receipt, GST, void/reprint and export rules.
- [ ] The user explicitly authorizes implementation.

### 1.2 Phase 0B technical gates

These are recorded in the Knowledge Base and are not design decisions:

- [ ] Clean database rebuild and baseline reconciliation proven against the existing project.
- [ ] Live RLS policies and grants verified against the intended role matrix.
- [ ] Shared Supabase project/schema confirmed under ADR-0008; no new project.
- [ ] Auth role source (`app_metadata.role`) and trusted-core flow confirmed.
- [ ] Local SQLite schema, migration and recovery contract approved.
- [ ] Outbox, transaction-group and deletion/absence reconciliation contract approved.
- [ ] Receipt numbering, GST/legal wording and reprint policy approved.
- [ ] Backup destination, encryption, retention and restore rollback policy approved.
- [ ] Test strategy, release gates and Windows packaging approach approved.
- [ ] ADR-0001–ADR-0007 and D1–D14 resolved or explicitly accepted.

### 1.3 Design prerequisites

- [ ] Confirm role-to-screen matrix with RLS, not only UI gates.
- [ ] Confirm whether receptionists may see clinical notes.
- [ ] Confirm whether inventory managers may record vaccinations.
- [ ] Confirm second-person requirements for merge/delete/restore.
- [ ] Confirm idle-lock and offline-unlock policy.
- [ ] Confirm notification quiet-hours override and retention.
- [ ] Confirm report export permissions and watermarking.
- [ ] Confirm print/receipt field set and legal footer.

## 2. Priority model

| Priority | Meaning |
|---|---|
| **P0** | Safety, privacy, data integrity or a blocking architecture decision |
| **P1** | Foundation required by most screens |
| **P2** | Core clinical and inventory workflows |
| **P3** | Finance, receipts, reports and administration |
| **P4** | Polish, density, dark mode and non-blocking enhancements |

Priority is about risk and dependency, not delivery order.

## 3. Epics

### UI-001 — Design tokens, shell and semantic component foundation

**Outcome:** a reusable React/TypeScript shell and component layer that matches the design language and is accessible by construction.

**Screens:** `SHELL-001`, all authenticated screens.

**Scope**

- CSS variables/tokens for light and dark themes.
- 232px sidebar, 56px topbar, workspace padding, page head.
- Semantic primitives: button, link, badge, status, field, select, textarea, checkbox, table, dialog, drawer, alert, tabs, pagination.
- Native HTML controls; no `div`-based inputs.
- Focus-visible ring, skip link, landmark structure.
- Formatting utilities for IST dates and integer money.
- Error boundary and empty/loading primitives.

**Acceptance evidence**

- Component tests for keyboard and accessible names.
- Visual regression at 1366×768 and 1920×1080.
- axe scan with no critical violations.
- No production dependency on the prototype renderer.

**Depends on:** approval; frontend architecture decision.

---

### UI-002 — Authentication and session

**Screens:** `AUTH-001`–`AUTH-005`.

**Scope**

- Sign-in, session restore, expired session, access denied, sign-out with pending writes.
- No token in renderer; trusted core handles auth.
- Role-aware destination and safe reauth.
- Idle-lock warning and lock screen.
- Pending-write inspection before sign-out.

**Acceptance evidence**

- Auth error copy does not reveal account existence.
- Session restore works with no PHI in URL.
- Keyboard-only sign-in and sign-out.
- Pending-write block is tested.

**Depends on:** ADR-0004, Phase 0B auth gate.

---

### UI-003 — Patient management

**Screens:** `PAT-001`–`PAT-007`.

**Scope**

- List/search/filter, register, profile, edit, duplicate warning, merge, archive.
- Stable clinic ID; duplicate detection review.
- Role-scoped clinical sections.
- Unsaved-change guard and optimistic concurrency.
- Audit-linked merge/archive.

**Acceptance evidence**

- Duplicate override requires a reason and writes an audit event.
- Merge is irreversible and shows both records before confirmation.
- Archived patients are distinguishable and restorable.
- Search handles no-results and offline states.

**Depends on:** UI-001, patient schema/RLS, identity policy.

---

### UI-004 — Vaccination workflow

**Screens:** `VAC-001`–`VAC-005`.

**Scope**

- Visit list, record visit, batch selection, visit detail, correction/deletion.
- Atomic local commit for stock + clinical + reminder + payment link.
- FEFO suggestion with explicit batch choice.
- Provisional receipt state.
- Correction is a linked diff/reversal, not a quantity overwrite.

**Acceptance evidence**

- Expired/insufficient batch is blocked.
- Duplicate submission is prevented.
- Correction reverses stock exactly once and is audited.
- Receipt status is never invented client-side.

**Depends on:** UI-003, inventory ledger, ADR-0003/0007.

---

### UI-005 — Consultation management

**Screens:** `CON-001`–`CON-004`.

**Scope**

- List, new consultation, detail, delete.
- Role-scoped clinical notes.
- Follow-up date and linked reminder/payment.
- Audited deletion with linked-record warnings.

**Acceptance evidence**

- Unauthorized roles cannot read clinical notes.
- Follow-up dates use IST.
- Delete does not orphan linked records.

**Depends on:** UI-003, role policy.

---

### UI-006 — Inventory, wastage and borrowing

**Screens:** `INV-001`–`INV-006`, `WAS-001`–`WAS-002`, `BRW-001`–`BRW-003`.

**Scope**

- Catalogue, batch detail, receive stock, adjust stock, wastage, borrow/lend, return.
- Single stock ledger; every change has a reason, actor and timestamp.
- FEFO, expiry, low-stock and negative-stock guards.
- Borrow/return direction and counterparty.

**Acceptance evidence**

- No screen can overwrite a batch quantity directly.
- Adjustment and wastage create distinct ledger movements.
- Negative stock and expired batch are rejected.
- Return is a movement, not a deletion.

**Depends on:** UI-001, ledger contract, RLS.

---

### UI-007 — Reminders and follow-up

**Screens:** `REM-001`–`REM-004`.

**Scope**

- Due vaccination list, reminder detail, personal reminders, create reminder.
- IST boundaries and terminal completed/dismissed states.
- Privacy-safe desktop notification preview.
- Link to patient/visit.

**Acceptance evidence**

- Timezone change does not move a due date.
- Completed reminders do not silently reopen after sync.
- Notification preview hides names by default.

**Depends on:** UI-004, notifications policy, ADR-0007.

---

### UI-008 — Finance and receipts

**Screens:** `FIN-001`–`FIN-006`, `RCP-001`–`RCP-003`.

**Scope**

- Overview, transactions, payment detail, record payment, expenses, record expense.
- Integer minor units; split payment; no client-authoritative total.
- Receipt preview, print queue error, reprint.
- Server-assigned immutable receipt number; reprint audited.

**Acceptance evidence**

- Payment totals reconcile to ledger.
- Print failure never voids payment or renumbers.
- Reprint keeps the original number and adds a duplicate marker.
- Expense is separate from negative income.

**Depends on:** UI-004, receipt policy, finance RLS.

---

### UI-009 — Reports

**Screens:** `RPT-001`–`RPT-004`.

**Scope**

- Statistics overview, vaccination report, finance report, milestone report.
- Date range and IST context.
- Stale/pending/partial states.
- Drill-down to underlying records.
- Export/print permissions.

**Acceptance evidence**

- Every metric is reproducible from the ledger/visit source.
- Stale data is labelled before export.
- Unauthorized export is blocked server-side.
- Charts have text equivalents.

**Depends on:** UI-004/008, reporting queries, export policy.

---

### UI-010 — Staff, roles and audit

**Screens:** `STF-001`–`STF-004`, `AUD-001`–`AUD-002`.

**Scope**

- Staff list, add staff, deactivate, reset password.
- Self-deactivation and last-admin guards.
- Session revocation.
- Append-only audit list and event detail.
- No password display.

**Acceptance evidence**

- Self/last-admin deactivation is blocked in service, not only UI.
- Deactivation revokes sessions.
- Audit cannot be edited/deleted through the client.
- Audit detail redacts PHI by role.

**Depends on:** auth/role model, audit schema.

---

### UI-011 — Offline, sync and conflict

**Screens:** `SYS-001`–`SYS-003`; cross-cutting.

**Scope**

- Global sync chip, sync center, conflict resolution, local data recovery.
- Queue inspection and retry where safe.
- Conflict shows both sides and ledger effect; no last-write-wins.
- Deletion/absence reconciliation contract.
- Local recovery without a casual destructive reset.

**Acceptance evidence**

- Offline write is labelled local, not synced.
- Conflict cannot be resolved by overwrite.
- Retry is idempotent.
- Recovery follows the approved procedure.

**Depends on:** ADR-0002/0003, local DB, sync contract.

---

### UI-012 — Backup, restore and updates

**Screens:** `SYS-004`–`SYS-007`.

**Scope**

- Backup list, create encrypted backup, restore preview.
- Passphrase, manifest, checksum, compatibility, safety snapshot, typed confirmation.
- Failed restore preserves current data.
- Signed update check and install gating.

**Acceptance evidence**

- Backup is encrypted and contains no plaintext temp PHI.
- Restore is blocked until checks pass.
- Failed restore leaves current data intact.
- Update cannot install during pending writes.

**Depends on:** backup policy, ADR-0002/0006, update signing.

---

### UI-013 — Settings

**Screens:** `SET-001`–`SET-004`.

**Scope**

- Appearance/density, notifications, security/session, clinic & safety.
- Device-local vs clinic-wide settings.
- Admin-only audited changes.
- No secrets in settings.

**Acceptance evidence**

- Personal settings do not change clinic policy.
- Clinic changes are audited.
- Notification preview is privacy-safe.
- Session settings match approved policy.

**Depends on:** settings precedence decision, auth/session policy.

---

### UI-014 — Accessibility and quality engineering

**Scope**

- Semantic component audit.
- Keyboard and focus management.
- Screen-reader testing (NVDA/JAWS/VoiceOver).
- 200%/400% zoom and forced-colors.
- Automated axe/Pa11y in CI.
- Visual regression at both target sizes.
- Reduced-motion and high-contrast checks.

**Acceptance evidence**

- WCAG 2.2 AA target verified for core workflows.
- No critical axe violations.
- Keyboard-only completion of core workflows.
- Documented assistive-technology test results.

**Depends on:** UI-001 and each workflow epic.

---

### UI-015 — Print, receipt and export

**Scope**

- Receipt preview and print CSS.
- Print queue error/retry/PDF fallback.
- Report export and watermarking.
- No hidden PHI; explicit field set.
- Print failure does not alter payment state.

**Acceptance evidence**

- Printed receipt matches preview.
- No extra PHI in print output.
- Reprint is audited and retains number.
- Report export labels stale/partial data.

**Depends on:** receipt policy, reporting, UI-008/009.

---

### UI-016 — Privacy, observability and operations

**Scope**

- No PHI/tokens in logs, URLs, analytics or error reports.
- Redacted diagnostics and support bundle.
- Audit event coverage for high-risk actions.
- Crash/error boundary that does not expose PHI.
- Backup/restore operational runbook.

**Acceptance evidence**

- Log review shows no PHI/tokens.
- Support bundle is redacted.
- High-risk actions have audit events.
- Error screens are actionable and safe.

**Depends on:** security model, audit schema, UI-001.

## 4. Suggested implementation slices

These are dependency slices, not a schedule:

1. **Foundation slice** — tokens, shell, native components, formatting, test harness (`UI-001`).
2. **Identity slice** — auth/session and role guard (`UI-002`, `UI-010` start).
3. **Patient slice** — list/register/profile/duplicate/merge (`UI-003`).
4. **Clinical slice** — vaccination and consultation (`UI-004`, `UI-005`).
5. **Stock slice** — inventory/wastage/borrow (`UI-006`).
6. **Money slice** — finance/receipts (`UI-008`).
7. **Follow-up slice** — reminders and notifications (`UI-007`).
8. **Trust slice** — offline/sync/conflict (`UI-011`).
9. **Recovery slice** — backup/restore/update (`UI-012`).
10. **Reporting/admin slice** — reports, staff, audit, settings (`UI-009`, `UI-010`, `UI-013`).
11. **Hardening slice** — accessibility, print/export, privacy (`UI-014`–`UI-016`).

## 5. Open decisions that block UI behaviour

| Decision | Why it blocks | Owner role |
|---|---|---|
| Idle-lock duration and offline unlock | Affects `AUTH-003`, `AUTH-005`, `SET-003` | Security + product |
| Role visibility of clinical notes | Affects `PAT-003`, `CON-*`, `RPT-*` | Clinical + security |
| Who may record vaccinations | Affects `VAC-002`, `VAC-005` | Clinical operations |
| Second-person confirmation | Affects merge/delete/restore | Clinical + security |
| Deletion/absence reconciliation | Affects sync conflict and local recovery | Backend + product |
| Receipt/GST wording and void policy | Affects `RCP-001`–`RCP-003` | Finance/legal |
| Backup destination/retention/rollback | Affects `SYS-005`–`SYS-007` | Security + operations |
| Notification quiet-hours override | Affects `SET-002`, `REM-*` | Product |
| Report export permissions | Affects `RPT-*` | Admin/finance |
| Per-doctor patient restriction | Affects search, lists and audit | Clinical + security |

## 6. Definition of Ready

A backlog item is ready only when:

- the user-visible outcome and out-of-scope boundary are clear;
- the role and permission matrix is confirmed against RLS;
- the state family (loading/empty/error/offline/pending/conflict) is specified;
- the audit event and PHI boundary are known;
- destructive actions have a confirmation and recovery rule;
- acceptance evidence is testable;
- dependencies and open decisions are linked.

## 7. Definition of Done

- Behaviour matches the approved screen specification and state model.
- Server-side authorization and validation are enforced.
- No PHI/tokens in URLs, logs, analytics or error copy.
- Keyboard, focus, labels and announcements are tested.
- Automated tests and visual regression pass.
- Offline/pending/conflict behaviour is tested where applicable.
- Print/receipt output matches the approved field set.
- Audit events exist for high-risk actions.
- Documentation and traceability are updated.

## 8. Non-goals

- No new Supabase project, schema or remote database.
- No production connection or real patient data in this design phase.
- No replacement of Android business rules by UI assumptions.
- No silent settlement of ADR/D1–D14 decisions.
- No dark-mode parity claim for all screens.
- No claim that the static prototype is production code.

## 9. Current status

**Not started.** No implementation is authorized. The repository remains design-only until approval.
