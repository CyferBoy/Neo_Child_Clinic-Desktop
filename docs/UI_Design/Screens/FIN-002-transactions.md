# FIN-002 · Transactions

> **Design specification 40 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `FIN-002` |
| Section | Finance |
| Feature | Finance and Payments |
| Source specification | `12-Finance-and-Payments.md` |
| Prototype | [FIN-002.html](../prototype/screens/FIN-002.html) |
| Rendered reference | [FIN-002.png](../screenshots/FIN-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Review visit-linked income rows, payment split, receipt status and pending local commits.

## Users

Admin, doctor, receptionist

## Permissions

Finance access role-scoped.

## Entry points

Finance overview; reports drill-down.

## Navigation

Open payment; filter; export; record payment.

## Layout regions

- Page header
- Summary strip
- Tabs
- Search/filter toolbar
- Transactions table
- Role-scope note

## Components

- Tabs
- Table
- Status badges
- Money columns
- Pagination

## Data shown

- 1,284 income rows
- ₹18,450 today
- Cash/online split
- 1 provisional receipt

## Actions

- Record payment
- Export
- Open payment
- Filter

## Forms and fields

- Search
- Date range
- Payment method

## States

- Loading
- Empty
- Ready
- Pending sync
- Provisional receipt
- Permission denied

## Offline and data behavior

Local transactions visible; pending and provisional badges explicit.

## Keyboard

/ search; table rows open; numeric values readable.

## Accessibility

Cash/online columns labelled; receipt status text; no color-only meaning.

## Dependencies

FIN-003/004; RCP; visits; reports.

## Open questions / not approved

Refund/void workflows, payment references and expense edit permissions.

## Design notes and evidence boundary

This list is income-first; expenses live in their own view.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
