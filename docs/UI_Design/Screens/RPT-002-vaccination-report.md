# RPT-002 · Vaccination report

> **Design specification 49 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `RPT-002` |
| Section | Reports |
| Feature | Statistics and Reports |
| Source specification | `15-Statistics-and-Reports.md` |
| Prototype | [RPT-002.html](../prototype/screens/RPT-002.html) |
| Rendered reference | [RPT-002.png](../screenshots/RPT-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Report doses, income, brand mix and batch usage by stable vaccine identity with drill-down.

## Users

Admin, doctor

## Permissions

Admin/doctor only; export permission unresolved.

## Entry points

Statistics & reports; vaccine card drill-down.

## Navigation

Filter brand/date; export; inspect source visits (implementation).

## Layout regions

- Page header
- Filter bar
- Four metrics
- Doses bars
- Brand donut
- Vaccine table
- Grouping note

## Components

- Filters
- Bar chart
- Donut
- Table
- Status badges

## Data shown

- 312 doses
- ₹4.93L
- 14 batches
- Pentavalent top

## Actions

- Export CSV
- Print
- Filter

## Forms and fields

- Date range
- Brand
- Status

## States

- Loading
- Empty
- Ready
- Stale
- Partial error

## Offline and data behavior

Local aggregates labelled; unsynced vaccinations visible as stale.

## Keyboard

Chart text alternative; table drill links; filters.

## Accessibility

Brand/color has text labels; table headers; totals labeled.

## Dependencies

RPT-001/003/004; vaccination; catalog identity.

## Open questions / not approved

Brand drill-down definition and official dose-report rules.

## Design notes and evidence boundary

Grouping uses stable catalog identity, not display-name equality.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
