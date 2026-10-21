# BRW-001 · Borrow & return

> **Design specification 32 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `BRW-001` |
| Section | Borrow & Return |
| Feature | Borrowed and Lent Vaccines |
| Source specification | `09-Borrowed-and-Lent-Vaccines.md` |
| Prototype | [BRW-001.html](../prototype/screens/BRW-001.html) |
| Rendered reference | [BRW-001.png](../screenshots/BRW-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Track batch-linked loans, partial returns and outstanding quantities across counterparties.

## Users

Admin, nurse, inventory manager

## Permissions

Record proposed for these roles; write-off approval unresolved.

## Entry points

Sidebar Borrow & return; inventory ledger.

## Navigation

Record borrow/lend; record return; filter open/closed; export.

## Layout regions

- Page header
- Summary strip
- Status tabs
- Search/filter toolbar
- Borrow table
- Overdue alert

## Components

- Summary cards
- Tabs
- Table
- Progress text (returned/outstanding)
- Status badges

## Data shown

- 4 open records
- 16 doses lent out
- 10 borrowed in
- 1 overdue
- 6 fictional records

## Actions

- Record borrow/lend
- Record return
- Export
- Filter

## Forms and fields

- Search
- Direction filter
- Due filter

## States

- Loading
- Empty
- Open
- Partially returned
- Closed
- Overdue
- Over-return blocked
- Pending sync

## Offline and data behavior

Local records/returns with pending badges; balance from local ledger; server conflict visible.

## Keyboard

/ search; return action labelled; tabs arrow-key semantics.

## Accessibility

Outstanding not color-only; progress has text; status labels.

## Dependencies

BRW-001–005; inventory ledger; audit.

## Open questions / not approved

Cross-clinic borrowing, write-off authority, due-date reminders and batch split/merge policy are unresolved.

## Design notes and evidence boundary

Loans do not create receipts or finance transactions.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
