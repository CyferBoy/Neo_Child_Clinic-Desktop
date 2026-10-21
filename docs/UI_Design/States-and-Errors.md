# States and Errors

**Status:** design specification. The static prototype shows representative states; it does not implement live loading, retry, sync or error handling.

**Related:** [`Design-System.md`](Design-System.md) · [`Component-Catalog.md`](Component-Catalog.md) · [`Accessibility.md`](Accessibility.md) · [`Screens/`](Screens/)

## 1. State vocabulary

This is a clinical and financial record system with an offline-capable desktop client. A misleading “Saved” message can cause a duplicate vaccination, a stock discrepancy or a receipt that appears valid when it is not. The interface must distinguish:

- **not saved** — input has not been persisted anywhere;
- **saved locally** — persisted on this device, not yet accepted by the server;
- **pending sync** — queued for upload;
- **synced** — acknowledged by the server;
- **stale** — previously synced, but newer server data may exist;
- **conflicted** — the server rejected or cannot reconcile the local change;
- **failed** — an operation did not complete and requires a decision.

These words are not interchangeable.

## 2. Global connection and freshness states

| State | Visual treatment | Copy rule | Where |
|---|---|---|---|
| Online / synced | Green status chip, cloud icon | “Online · all changes synced” | Global topbar |
| Syncing | Blue/green chip | “Syncing 2 changes…” — count is real | Global topbar, `SYS-001` |
| Offline / local only | Neutral/warning chip, cloud-off icon | “Offline · changes save locally” | Global topbar, operational screens |
| Pending sync | Info badge on row/card | “Saved locally · pending sync” | Vaccination, finance, stock, patient |
| Attention / conflict | Danger or warning chip with count | “1 conflict needs review” | Global topbar, `SYS-001` |
| Stale data | Warning badge + “as of” timestamp | “Showing data as of 09:30 IST; newer changes may exist” | Dashboard, reports, lists |
| Server unreachable | Persistent alert with retry | “Could not reach the server. Local data is still available.” | `SYS-001`, forms |

Rules:

1. The global sync chip is always visible on operational screens.
2. A local save is not described as “synced”.
3. A conflict is not a toast; it is a hard stop in `SYS-002`.
4. Offline mode does not block read-only review of local data.
5. A conflict offers “Review conflict”, not “Retry” or “Overwrite”.
6. A stale report says so before export or print.

## 3. Screen-state model

Every list and form has this state family, even where the static prototype only renders “ready”:

| State | What the user sees | Required behaviour |
|---|---|---|
| Loading | Contextual skeleton or “Loading patients…” | Do not show an empty table as a result |
| Ready | Normal content | — |
| Empty (no records) | Explanation + safe next action | Distinguish from “no matches” |
| No results (filtered) | Query summary + clear filters | Keep the query visible |
| Error (recoverable) | Inline alert + retry/back | Preserve input where safe |
| Error (blocking) | Hard-stop card + safe route | Do not imply success |
| Permission denied | Explanation + safe route back | Do not reveal restricted data |
| Offline | Global chip + local availability note | Allow local writes where the domain permits |
| Pending | Row/card badge + queue link | Do not claim server acceptance |
| Conflict | Both sides + ledger effect + resolution | Authorized review only |
| Stale | “As of” timestamp + refresh | Do not silently overwrite newer data |
| Locked / expired | Reauth or lock screen | Preserve safe context |

## 4. State coverage by workflow

### Authentication and session

| Screen | Key states | Notes |
|---|---|---|
| `AUTH-001` | idle, invalid credentials, auth service unreachable, rate-limited, locked account | Error copy does not reveal whether an email exists |
| `AUTH-002` | restoring, slow, failed restore, expired token | No token shown; safe retry |
| `AUTH-003` | expired, reauth required, destination preserved | No PHI in URL |
| `AUTH-004` | role denied, route denied, session valid | Explain what is allowed, not what is hidden |
| `AUTH-005` | pending writes, sync in progress, resolve required, sign out blocked | No silent discard |

### Patients

| Screen | Key states | Notes |
|---|---|---|
| `PAT-001` | loading, empty, no results, archived filter, offline, stale | Archived patients are visibly distinct |
| `PAT-002` | ready, validation error, duplicate detected, save failed, saved locally | Duplicate check is not a silent pass |
| `PAT-003` | ready, pending sync, archived, restricted clinical section, missing record | Profile is the stable anchor |
| `PAT-004` | dirty, validation error, save conflict, saved locally | Unsaved-change guard |
| `PAT-005` | possible duplicate, exact match, override reason required, no match | Override is audited |
| `PAT-006` | review, typed confirmation, merge in progress, merge failed, merged | Irreversible merge; no auto-merge |
| `PAT-007` | confirm archive, reason, archived, restore | Archive is not delete; audit trail retained |

### Vaccination and consultation

| Screen | Key states | Notes |
|---|---|---|
| `VAC-001` | loading, empty, pending sync, provisional receipt, corrected, offline | Receipt status is explicit |
| `VAC-002` | ready, validation error, batch unavailable, expired batch, insufficient stock, payment incomplete, saved locally, save failed | One atomic local commit in the target model |
| `VAC-003` | batch list, FEFO suggestion, expired/blocked, quantity exceeds stock, empty | Explicit batch choice |
| `VAC-004` | ready, pending sync, provisional receipt, corrected, deleted | Commit trail visible |
| `VAC-005` | correction, deletion, reason required, receipt-linked block, reversal preview | No direct quantity edit |
| `CON-001` | loading, empty, no results, permission-limited | Clinical notes are role-scoped |
| `CON-002` | ready, validation error, save failed, saved locally | Follow-up date is explicit |
| `CON-003` | ready, restricted, pending sync, linked payment/reminder | Links are textual |
| `CON-004` | delete confirmation, reason, linked-record warning, deleted | Audited clinical event |

### Inventory, wastage and borrowing

| Screen | Key states | Notes |
|---|---|---|
| `INV-001` | loading, empty, low stock, expiring, expired, offline, stale | Text + colour, never colour alone |
| `INV-002` | ready, inactive vaccine, no results | Catalogue is not stock |
| `INV-003` | dirty, validation error, schedule conflict, saved | Changes audited |
| `INV-004` | ready, expired, recalled, pending movement, no movements | Batch identity is stable |
| `INV-005` | ready, batch existing/new, duplicate batch, invalid expiry, save failed, saved locally | Receive creates a movement |
| `INV-006` | reason required, quantity validation, approval required, conflict, saved locally | Adjustment is not an overwrite |
| `WAS-001` | empty, ready, pending sync, offline | Wastage is batch-linked |
| `WAS-002` | ready, reason required, quantity exceeds batch, save failed, saved locally | No direct stock edit |
| `BRW-001` | empty, outstanding, overdue return, settled | Direction is explicit |
| `BRW-002` | ready, counterparty required, batch unavailable, save failed | Borrow/lend is a movement |
| `BRW-003` | partial return, full return, quantity validation, settled | Return is a movement, not deletion |

### Follow-up, finance and receipts

| Screen | Key states | Notes |
|---|---|---|
| `REM-001` | loading, empty, due today, overdue, no results, offline | IST boundaries; no silent reopen |
| `REM-002` | ready, complete, dismiss with reason, linked visit, stale | Completed is terminal across sync |
| `REM-003` | empty, upcoming, completed, no results | Personal reminders are separate from clinical due items |
| `REM-004` | ready, validation error, saved locally, save failed | No PHI in notification preview |
| `FIN-001` | loading, empty, stale, offline, permission-limited | Income/expense separation |
| `FIN-002` | loading, empty, no results, pending sync, refunded/void | Amounts are integer minor units in target model |
| `FIN-003` | ready, pending, receipt linked, refunded/void, restricted | Payment detail is the audit anchor |
| `FIN-004` | ready, split payment, balance due, invalid amount, save failed, saved locally | No authoritative client-side total |
| `FIN-005` | loading, empty, no results, pending sync | Expense ledger is separate |
| `FIN-006` | ready, receipt required, category required, save failed | No negative-income workaround |
| `RCP-001` | preview, provisional, ready to print, printer unavailable, printed | Server-assigned number |
| `RCP-002` | queue error, retry, alternate printer, save PDF, payment safe | Print failure never voids payment |
| `RCP-003` | reprint review, reason, duplicate marker, printed | Original number retained; reprint audited |

### Reports, administration and system

| Screen | Key states | Notes |
|---|---|---|
| `RPT-001` | loading, empty range, stale, permission denied, ready | Every metric has a range and timezone |
| `RPT-002` | loading, empty, partial/pending, stale, export denied | Drill-down to underlying visits |
| `RPT-003` | loading, empty, stale, export denied | Finance totals reconcile to ledger |
| `RPT-004` | loading, empty, stale, export denied | Milestones are not diagnoses |
| `STF-001` | loading, empty, inactive filter, self row, last admin | Self-deactivation blocked |
| `STF-002` | ready, duplicate email, invalid role, invite failed, invited | No password display |
| `STF-003` | confirm deactivate, self-block, last-admin block, deactivated | Sessions revoked |
| `STF-004` | reset requested, sent, rate-limited, failed | No password shown |
| `AUD-001` | loading, empty, no results, restricted | Append-only |
| `AUD-002` | ready, redacted, restricted | No PHI beyond need |
| `SYS-001` | online, syncing, offline, attention, queue empty, queue error | Counts are real |
| `SYS-002` | unresolved, reviewing, resolved, failed, unauthorized | Never last-write-wins |
| `SYS-003` | healthy, degraded, locked, recovery required, failed | No destructive reset in normal UI |
| `SYS-004` | up to date, available, downloading, verified, install blocked, offline | Signed updates only |
| `SYS-005` | no backups, ready, verifying, failed checksum, disk full, restore in progress, permission denied | Backups are PHI |
| `SYS-006` | ready, weak passphrase, mismatch, destination unavailable, disk full, interrupted, created | No plaintext temp files |
| `SYS-007` | preview, checks failed, snapshot required, typed confirmation, restoring, failed safely, restored | Failed restore leaves current data intact |
| `SET-001` | saved, dirty, save failed, theme preview | Device-local |
| `SET-002` | saved, permission denied, OS notification unavailable, test sent | Privacy-safe previews |
| `SET-003` | saved, session expiry, lock now, sign-out blocked | No secrets |
| `SET-004` | saved, validation error, permission denied, audited | Admin-only |

## 5. Error copy standard

Every error should answer: what happened, what is safe now, and what to do next.

| Situation | Preferred copy | Avoid |
|---|---|---|
| Local save failed | “Could not save on this device. Your entries are still on this screen. Try again.” | “Error 500” |
| Saved locally, not synced | “Saved on this device. Waiting to sync.” | “Saved successfully.” |
| Stock conflict | “This batch changed on another device. Review both movements before recording the dose.” | “Conflict. Overwrite?” |
| Receipt print failure | “The receipt did not print. The payment is safe and the receipt number is unchanged. Retry or choose another printer.” | “Print failed.” |
| Session expired | “Your session ended. Sign in again to continue. Unsaved entries on this screen may be lost.” | “Unauthorized.” |
| Permission denied | “Your role cannot view this section. Ask an administrator if you need access.” | “Forbidden.” |
| Duplicate warning | “A patient with a similar name and phone already exists. Review before creating a new record.” | “Duplicate.” |
| Restore blocked | “Restore is blocked because the safety snapshot has not been created. Create the snapshot first.” | “Invalid operation.” |
| Offline | “You are offline. Changes will be saved locally and synced when the connection returns.” | “Network error.” |
| Stale report | “This report is from cached data as of 09:30 IST. Refresh before export.” | “Data may be outdated.” |

Rules:

- Do not include tokens, SQL, table names, stack traces, patient names or full identifiers in error copy.
- Do not blame the user.
- Do not use “Oops”, “Uh oh” or humour for clinical/financial failures.
- Do not use a generic “Something went wrong” when the state is known.
- Do not auto-dismiss an error that affects a clinical, stock or payment record.
- Do not offer “Overwrite” for a sync conflict.

## 6. Destructive and high-risk confirmations

| Screen | Action | Required guard | Recovery / audit |
|---|---|---|---|
| `PAT-006` | Merge patients | Review both records; typed confirmation; reason; admin/doctor role | Irreversible merge; audit entry; no auto-merge |
| `PAT-007` | Archive patient | Reason; confirmation; role check | Restore path; audit; no hard delete in normal UI |
| `VAC-005` | Correct/delete visit | Reason; receipt/stock impact preview; admin/doctor | Linked diff/reversal; audit; receipt state checked |
| `CON-004` | Delete consultation | Reason; linked payment/reminder warning; role | Audited clinical event; no silent orphan |
| `INV-006` | Adjust stock | Reason; quantity validation; approval where required | Ledger movement; audit; no direct overwrite |
| `WAS-002` | Record wastage | Reason; batch/quantity validation | Ledger movement; audit |
| `STF-003` | Deactivate staff | Not self; not last admin; confirmation | Sessions revoked; audit; reactivation path |
| `SYS-002` | Resolve conflict | Authorized role; both sides visible; audit note | Ledger-safe resolution; no last-write-wins |
| `SYS-007` | Restore backup | Admin; compatibility checks; safety snapshot; typed `RESTORE` | Failed restore preserves current data; post-restore reconciliation |
| `RCP-003` | Reprint receipt | Reason; duplicate marker; role | Original number retained; reprint audited |

Rules:

- Cancel is the safe default and receives initial focus where the platform allows.
- Destructive buttons are not the primary visual action.
- A typed confirmation is used for irreversible or data-replacing actions, not routine edits.
- The confirmation states the consequence, scope and whether the action can be undone.
- High-risk actions require server-side authorization; the dialog is not the control.

## 7. Healthcare-specific safeguards

1. **Identity before action.** Clinical actions show the patient name and at least one stable identifier before commit.
2. **No silent stock overwrite.** Every stock change is a movement with a reason, actor and timestamp.
3. **No silent receipt renumbering.** A provisional receipt is labelled; a reprint keeps the original number.
4. **No duplicate vaccination by accident.** The due list and visit form show the last dose and next due date.
5. **No PHI leakage in notifications.** Preview text hides patient names by default.
6. **No PHI in URLs.** Deep links use opaque internal identifiers.
7. **Offline honesty.** “Saved locally” is distinct from “synced”; a stale report is labelled.
8. **Conflict is a hard stop.** The UI never offers a one-click overwrite of stock or receipt data.
9. **Critical alerts persist.** Clinical, stock, payment and destructive alerts do not auto-dismiss.
10. **Input preservation.** A failed save keeps entries on screen where safe.
11. **Session safety.** Idle lock and sign-out protect PHI; pending writes are surfaced before sign-out.
12. **Print preview.** Receipt and report printing shows what will be printed and excludes hidden PHI.

## 8. Unresolved states

The screens deliberately do not settle:

- exact idle-lock duration and offline-unlock policy;
- second-person confirmation for merge, delete, restore or controlled-drug actions;
- deletion/absence reconciliation when a local record is missing on the server;
- restore rollback triggers and post-restore reconciliation ownership;
- whether receptionists may see clinical notes;
- whether inventory managers may record vaccinations;
- notification quiet-hours override, sound and retention;
- GST/receipt legal wording and whether a printed receipt can be voided;
- report export permissions and watermarking.

These are marked in the relevant screen specifications and in [`Implementation-Backlog.md`](Implementation-Backlog.md).

## 9. State QA checklist

- [ ] Every list has loading, empty and no-results copy.
- [ ] Every form has validation, save-failed and saved-locally states.
- [ ] Every destructive action has a consequence statement and safe cancel.
- [ ] Every stock change names the batch and movement type.
- [ ] Every receipt state distinguishes provisional, assigned and reprinted.
- [ ] Every offline screen distinguishes local save from sync.
- [ ] Every conflict screen shows both sides and the ledger effect.
- [ ] Every error is actionable and free of PHI/secrets.
- [ ] Critical alerts do not auto-dismiss.
- [ ] Focus moves to the first error; focus returns after a dialog closes.
- [ ] Stale reports say “as of” before export.
- [ ] Permission-denied copy does not reveal restricted data.

## 10. Evidence boundary

These states are design specifications. The static prototype renders selected examples; it does not exercise real network failure, sync, authorization, printing or database errors. Production acceptance requires executable tests against the approved architecture.
