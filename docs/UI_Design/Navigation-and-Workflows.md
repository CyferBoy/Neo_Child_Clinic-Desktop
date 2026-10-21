# Navigation and Workflows

**Status:** target design. No route, guard or workflow is implemented.  
**Screen index:** [`Screen-Inventory.md`](Screen-Inventory.md)  
**Per-screen details:** [`Screens/`](Screens/)

## 1. Global shell

Every authenticated operational screen uses the same shell:

```text
┌───────────────┬──────────────────────────────────────────────────────────────┐
│ 232px sidebar │ 56px topbar: global search · sync chip · notifications · user │
│               ├──────────────────────────────────────────────────────────────┤
│ Workspace     │ 24px workspace padding                                       │
│ Inventory     │ page head                                                    │
│ Follow-up     │ cards / tables / forms                                       │
│ Business      │                                                              │
│ Administration│                                                              │
└───────────────┴──────────────────────────────────────────────────────────────┘
```

The sidebar is persistent. The topbar is global. The workspace scrolls conceptually, but the prototype is fixed to a 768px frame so that each screen can be reviewed as a single desktop view.

### Sidebar groups

| Group | Items |
|---|---|
| Workspace | Dashboard, Patients, Vaccinations, Consultations |
| Inventory | Inventory, Wastage, Borrow & return |
| Follow-up | Due vaccinations, Personal reminders |
| Business | Finance, Receipts, Reports |
| Administration | Staff, Audit log, Sync center, Backups, Updates, Settings |

The exact item ordering is a design proposal. The screen set uses a consistent order so that muscle memory can form.

### Topbar

- **Global search** — patients, invoices, batches, clinic IDs. `Ctrl/Cmd+K` focuses it in the prototype.
- **Sync chip** — Online / Syncing / Offline / Attention. The chip is a status surface, not a button that silently performs a sync.
- **Notifications** — due reminders and system events. Preview text hides patient names by default.
- **Help / keyboard shortcut affordance** — visible but not a substitute for documentation.
- **User chip** — name, role, account menu.

No topbar element displays a token, secret or full patient record.

## 2. Screen map

The 68 screens are grouped as follows. Use [`Screen-Inventory.md`](Screen-Inventory.md) for links to every prototype and PNG.

| Section | Screens |
|---|---|
| Authentication | `AUTH-001` sign in, `AUTH-002` restoring session, `AUTH-003` session expired, `AUTH-004` access denied, `AUTH-005` sign out with pending writes |
| Shell | `SHELL-001` global search |
| Dashboard | `DASH-001` dashboard |
| Patients | `PAT-001` list, `PAT-002` register, `PAT-003` profile, `PAT-004` edit, `PAT-005` duplicate warning, `PAT-006` merge, `PAT-007` archive |
| Vaccinations | `VAC-001` visits, `VAC-002` record, `VAC-003` batch selection, `VAC-004` visit detail, `VAC-005` correct/delete |
| Consultations | `CON-001` list, `CON-002` new, `CON-003` detail, `CON-004` delete |
| Inventory | `INV-001` overview, `INV-002` catalogue, `INV-003` edit catalogue, `INV-004` batch detail, `INV-005` receive stock, `INV-006` adjust stock |
| Wastage | `WAS-001` overview, `WAS-002` record wastage |
| Borrow & return | `BRW-001` overview, `BRW-002` record borrow/lend, `BRW-003` record return |
| Follow-up | `REM-001` due vaccinations, `REM-002` reminder detail, `REM-003` personal reminders, `REM-004` create personal reminder |
| Finance | `FIN-001` overview, `FIN-002` transactions, `FIN-003` payment detail, `FIN-004` record payment, `FIN-005` expenses, `FIN-006` record expense |
| Receipts | `RCP-001` preview, `RCP-002` print queue error, `RCP-003` reprint |
| Reports | `RPT-001` statistics overview, `RPT-002` vaccination report, `RPT-003` finance report, `RPT-004` milestone report |
| Administration | `STF-001` staff list, `STF-002` add staff, `STF-003` deactivate, `STF-004` reset password, `AUD-001` audit log, `AUD-002` audit event |
| System | `SYS-001` sync center, `SYS-002` conflict, `SYS-003` local data recovery, `SYS-004` updates, `SYS-005` backups, `SYS-006` create backup, `SYS-007` restore preview |
| Settings | `SET-001` appearance, `SET-002` notifications, `SET-003` security, `SET-004` clinic & safety |

## 3. Navigation rules

1. **Role-aware navigation.** A user sees only the sections their role can use. Hiding a route is not authorization; the Go service and RLS must enforce it.
2. **Page first, dialog for decisions.** Lists and detail pages carry context. A dialog is used for a focused decision (archive, merge, deactivate, conflict resolution) rather than a whole workflow.
3. **Drawer for context.** Patient quick view, reminder detail and audit event detail can use a drawer when the underlying list must stay visible.
4. **Unsaved changes.** Navigating away from a dirty form prompts: stay, discard, or save draft where a draft store is approved.
5. **Back is explicit.** Detail screens provide a labelled back link; browser-style back alone is not the only path.
6. **No PHI in URLs.** Use opaque internal identifiers in any deep link. The prototype uses static filenames only.
7. **Sync and offline are global.** A screen may show local context, but the global sync chip remains the source of cross-screen status.
8. **Destructive actions are never the default focus.** Cancel is the safe default; destructive confirmation requires an explicit action.

## 4. Core workflows

### 4.1 Sign in and session

```text
AUTH-001 Sign in
  → AUTH-002 Restoring session (returning user / token restore)
  → Dashboard
  → AUTH-003 Session expired (reauth required)
  → AUTH-004 Access denied (role/route not permitted)
  → AUTH-005 Sign out blocked by pending writes
```

Design rules:

- Sign-in errors do not reveal whether an email exists.
- The restoring-session screen explains why the user is waiting and offers a safe retry.
- Session expiry preserves the intended destination where safe, without putting PHI in a URL.
- Sign-out with pending writes explains what is pending and offers sync/resolve, not silent data loss.
- No token, refresh token or secret is ever shown in the renderer.

### 4.2 Register a patient

```text
PAT-001 Patient list
  → PAT-002 Register patient
      → PAT-005 Duplicate warning (possible match)
          → open existing PAT-003
          → continue with explicit override + reason
  → PAT-003 Patient profile
```

Design rules:

- Search before create. Duplicate detection uses name, phone, date of birth and clinic identifiers as available.
- The duplicate warning is a review step, not an automatic block; overriding requires a reason.
- The profile is the stable anchor for vaccination, consultation, payment and receipt context.
- Merge (`PAT-006`) and archive (`PAT-007`) are separate, audited, destructive decisions.

### 4.3 Vaccination visit → stock → payment → receipt

```text
PAT-003 profile / VAC-001 visits
  → VAC-002 Record vaccination
      → VAC-003 Batch selection (FEFO, expiry, stock)
      → payment capture (FIN-004 or embedded payment step)
      → receipt preview (RCP-001)
          → print success
          → RCP-002 print queue error (payment safe; retry)
  → VAC-004 Visit detail
      → VAC-005 Correct/delete (audited; stock reversal)
```

Design rules:

- The batch is chosen before the dose is recorded; expired or insufficient stock is blocked with a reason.
- Stock deduction and the clinical record are one transaction group in the target model. The UI must not imply that either succeeded alone.
- Payment and receipt are linked to the visit; the receipt number is server-assigned.
- A print failure never voids payment or changes the number. The print queue offers retry, another printer, or save as PDF.
- Correct/delete is audited and may require a reason; historical stock effects must be shown.

### 4.4 Consultation

```text
CON-001 Consultations
  → CON-002 New consultation
  → CON-003 Consultation detail
      → follow-up reminder (REM-003/REM-004)
      → linked payment (FIN-004)
      → CON-004 Delete (audited, reason)
```

Design rules:

- Clinical notes are role-scoped; the screen does not assume every role can read them.
- Follow-up dates are explicit IST dates, not free text.
- Deleting a consultation is a clinical event and must not silently remove linked payment or stock facts.

### 4.5 Inventory: receive, adjust, waste, borrow

```text
INV-001 Inventory overview
  → INV-002 Catalogue → INV-003 Edit catalogue
  → INV-004 Batch detail
  → INV-005 Receive stock
  → INV-006 Adjust stock (reason, audit)
WAS-001 Wastage → WAS-002 Record wastage
BRW-001 Borrow & return → BRW-002 Record borrow/lend → BRW-003 Record return
```

Design rules:

- Every stock change is a ledger movement with a reason, actor and timestamp.
- Receive stock creates or updates a batch; it does not overwrite an existing batch count.
- Adjustments require a reason and are visibly different from wastage, borrowing and vaccination consumption.
- Wastage is batch-linked and never a direct quantity edit.
- Borrow/return shows direction, counterparty, batch and expected return; a return is a movement, not a deletion.
- Expiry and low-stock states use text plus colour.

### 4.6 Due vaccinations and reminders

```text
DASH-001 due card / REM-001 Due vaccinations
  → REM-002 Reminder detail
      → PAT-003 profile
      → VAC-002 Record vaccination
      → dismiss / complete with reason
REM-003 Personal reminders
  → REM-004 Create personal reminder
```

Design rules:

- Due dates use IST boundaries. Changing the OS timezone must not move a due date.
- Completed and dismissed are terminal states across sync; the UI must not silently reopen them.
- Personal reminders are separate from clinical vaccination due items, even though both use the `REM` screen prefix.
- Desktop notification previews hide patient names by default (`SET-002`).

### 4.7 Finance and receipts

```text
FIN-001 Finance overview
  → FIN-002 Transactions → FIN-003 Payment detail → RCP-001 Receipt preview
  → FIN-004 Record payment
  → FIN-005 Expenses → FIN-006 Record expense
  → RCP-003 Reprint
  → RPT-003 Finance report
```

Design rules:

- Income and expenses are separate ledgers. A negative income edit is not a refund workflow.
- Payment methods and split payments are explicit; the renderer does not calculate authoritative totals.
- Receipts are immutable once assigned; reprint uses the original number and is audited.
- Report exports state whether data is stale or pending; an export must not imply completeness when writes are pending.

### 4.8 Reports

```text
RPT-001 Statistics overview
  → RPT-002 Vaccination report
  → RPT-003 Finance report
  → RPT-004 Patient milestone report
```

Design rules:

- Every metric has a date range and timezone context.
- Drill-down goes to the underlying visit/payment/batch, not to a parallel calculation.
- Empty, loading, stale and permission-denied states are designed, not left as blank pages.
- Export/print is role-restricted; the design marks this as policy-dependent.

### 4.9 Offline and sync

```text
Any operational screen
  → global sync chip
  → SYS-001 Sync center
      → SYS-002 Resolve conflict (hard stop)
      → retry / inspect queue
  → SYS-003 Local data recovery
```

Design rules:

- Offline is a normal mode, not an error page. Local writes are allowed where the domain permits.
- Pending writes are visible; “Saved” is not used when the write is only local.
- A conflict is never resolved by last-write-wins. Both sides and the ledger effect are shown.
- The conflict screen requires an authorized person and an audit note.
- Deletion/absence reconciliation remains an open contract; the UI does not invent a resolution.

### 4.10 Backup, restore and update

```text
SYS-005 Backups
  → SYS-006 Create encrypted backup
  → SYS-007 Restore preview
      → create safety snapshot
      → typed confirmation
      → restore (blocked until checks pass)
SYS-004 Application updates
```

Design rules:

- Backups contain PHI and require an approved encrypted destination.
- Restore is destructive and admin-only. Preview, compatibility checks, safety snapshot and typed confirmation are mandatory.
- A failed restore must leave current data intact.
- Updates are signed and verified; no silent install; no downgrade.
- Update checks fail gracefully offline.

### 4.11 Staff, audit and settings

```text
STF-001 Staff list
  → STF-002 Add staff
  → STF-003 Deactivate
  → STF-004 Reset password
AUD-001 Audit log → AUD-002 Audit event
SET-001 Appearance
SET-002 Notifications
SET-003 Security & sessions
SET-004 Clinic & safety
```

Design rules:

- Self-service cannot change one’s own role, deactivate oneself, or remove the last admin.
- Deactivation revokes sessions; hiding a row is not enough.
- Password reset never displays a password; it uses a secure recovery flow.
- Audit is append-only; no role may edit or delete audit rows through the client.
- Personal settings are device-local; clinic-wide settings are admin-only and audited.
- Settings never expose secrets.

## 5. Keyboard and focus model

The prototype is static, but the target design supports:

- `Ctrl/Cmd+K` — focus global search.
- `Esc` — close a dialog/drawer or clear a search, with unsaved-change protection.
- `Tab` / `Shift+Tab` — move through controls; focus is trapped in a modal.
- `Enter` — activate the focused button or submit a form; not used for destructive confirmation by default.
- `Space` — toggle checkboxes and selected rows.
- Arrow keys — navigate tables and menus where implemented.
- First invalid field receives focus on submit.
- Focus returns to the triggering control when a dialog closes.

No screen requires a mouse for a core workflow.

## 6. Screen transitions and guards

| From | Action | To | Guard |
|---|---|---|---|
| `AUTH-001` | Successful sign-in | `DASH-001` | Role resolved; session established |
| `AUTH-001` | Restore existing session | `AUTH-002` | Token restore in Go only |
| `AUTH-003` | Reauthenticate | `AUTH-001` | Intended destination preserved without PHI |
| Any | Global search result | Patient/invoice/batch detail | Role check on destination |
| `PAT-001` | Register | `PAT-002` | Create permission |
| `PAT-002` | Possible duplicate | `PAT-005` | Review before create |
| `PAT-003` | Record vaccination | `VAC-002` | Clinical role + stock access |
| `VAC-002` | Batch | `VAC-003` | Batch available, not expired |
| `VAC-002` | Complete | `RCP-001` | Payment captured; server receipt assigned |
| `RCP-001` | Print failure | `RCP-002` | Payment remains valid |
| `FIN-002` | Payment detail | `FIN-003` | Finance role |
| `SYS-001` | Conflict | `SYS-002` | Admin/sync authority |
| `SYS-005` | Restore | `SYS-007` | Admin + backup file selected |
| `SYS-007` | Restore | `SYS-005` | Safety snapshot + checks + typed confirmation |
| `STF-001` | Deactivate | `STF-003` | Admin; not self; not last admin |
| Any | Sign out with pending writes | `AUTH-005` | Pending queue inspection |

## 7. Open workflow questions

These are not silently resolved by the screens:

- Which role may record vaccinations, and may an inventory manager do so?
- May receptionists see clinical notes, or only scheduling and payment data?
- Is per-doctor patient restriction required?
- Which actions need a second-person confirmation?
- What is the exact deletion/absence reconciliation contract?
- What is the final idle-lock/offline-unlock policy?
- What is the approved backup destination and retention policy?
- Are report exports admin-only?
- Is GST required on receipts, and what legal wording is required?
- What is the notification retention and quiet-hours override policy?
- Does the clinic use a shared or individual Windows account in practice?

These questions are repeated in the relevant screen specifications and in [`Implementation-Backlog.md`](Implementation-Backlog.md).
