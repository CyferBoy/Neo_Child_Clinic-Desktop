# RPT-003 · Finance report

> **Design specification 50 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `RPT-003` |
| Section | Reports |
| Feature | Statistics and Reports |
| Source specification | `15-Statistics-and-Reports.md` |
| Prototype | [RPT-003.html](../prototype/screens/RPT-003.html) |
| Rendered reference | [RPT-003.png](../screenshots/RPT-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Report income, expenses, net and payment split with one income count per visit and IST daily boundaries.

## Users

Admin, doctor

## Permissions

Reports role-restricted; export may be admin-only.

## Entry points

Statistics & reports; finance overview; payment detail.

## Navigation

Date filter; source payment drill-down; export/print.

## Layout regions

- Page header
- Filter bar
- Four metrics
- Income/expense chart
- Payment split donut
- Daily table
- Stale warning

## Components

- Filters
- Line chart
- Donut
- Daily table
- Stale badge

## Data shown

- ₹3.86L income
- ₹63,760 expenses
- ₹3.22L net
- 1 provisional receipt

## Actions

- Export CSV
- Print
- Filter

## Forms and fields

- Date range
- Payment method

## States

- Loading
- Empty
- Ready
- Stale/partial
- Error
- Permission denied

## Offline and data behavior

Local aggregates labelled stale; no completeness claim with pending writes.

## Keyboard

Chart alternative; table headers; filters.

## Accessibility

Cash/online legend text; amounts labelled; stale state textual.

## Dependencies

RPT-001/002/004; finance; receipts; audit.

## Open questions / not approved

Refund/discount treatment, official report definitions, export scope.

## Design notes and evidence boundary

A visit's income is counted once; expenses are separate.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
