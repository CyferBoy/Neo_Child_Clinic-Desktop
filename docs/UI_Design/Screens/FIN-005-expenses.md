# FIN-005 · Expenses

> **Design specification 43 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `FIN-005` |
| Section | Finance |
| Feature | Finance and Payments |
| Source specification | `12-Finance-and-Payments.md` |
| Prototype | [FIN-005.html](../prototype/screens/FIN-005.html) |
| Rendered reference | [FIN-005.png](../screenshots/FIN-005.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

List, search and filter clinic expenses separately from visit income.

## Users

Admin, doctor; receptionist may record but not edit (open)

## Permissions

Expense management role policy unresolved.

## Entry points

Finance overview; sidebar finance.

## Navigation

Record expense; filter; export.

## Layout regions

- Page header
- Summary strip
- Search/filter toolbar
- Expense table
- Income separation note

## Components

- Summary cards
- Table
- Status badges
- Method badge
- Pagination

## Data shown

- ₹63,760 this month
- 18 entries
- ₹4,280 today
- 7 fictional rows

## Actions

- Record expense
- Export
- Filter

## Forms and fields

- Search
- Category
- Date range

## States

- Loading
- Empty
- Ready
- Pending sync
- Permission denied

## Offline and data behavior

Local expense list and outbox.

## Keyboard

/ search; table rows open; filters accessible.

## Accessibility

Money and method labels; status text.

## Dependencies

FIN-001/006; reports; audit.

## Open questions / not approved

Who can edit expenses after reporting? Receipt attachment storage policy?

## Design notes and evidence boundary

Expenses are not netted into visit income rows.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
