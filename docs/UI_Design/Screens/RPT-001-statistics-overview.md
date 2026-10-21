# RPT-001 · Statistics overview

> **Design specification 48 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `RPT-001` |
| Section | Reports |
| Feature | Statistics and Reports |
| Source specification | `15-Statistics-and-Reports.md` |
| Prototype | [RPT-001.html](../prototype/screens/RPT-001.html) |
| Rendered reference | [RPT-001.png](../screenshots/RPT-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Provide role-restricted operational and financial aggregates with explicit IST windows, stale labels and drill-down.

## Users

Admin, doctor

## Permissions

Admin/doctor only (proposed); export may be admin-only.

## Entry points

Sidebar Reports; dashboard insights.

## Navigation

Vaccination report; finance report; patient milestones; full report; export.

## Layout regions

- Page header
- Date/filter bar
- Four metric cards
- Income/expense line chart
- Top vaccines bars
- Report view links
- Data health

## Components

- Metric cards
- Line chart
- Bar chart
- Drill-down links
- Stale badge

## Data shown

- 248 visits
- 312 vaccinations
- ₹3.86L income
- ₹63,760 expenses
- 2 pending writes

## Actions

- Export report
- Print
- Drill into reports

## Forms and fields

- Date range
- Vaccine filter

## States

- Loading
- Empty range
- Ready
- Stale/partial
- Error (not zero)
- Permission denied

## Offline and data behavior

Local aggregates labelled stale; do not claim a complete month while writes are pending.

## Keyboard

Charts have text alternatives; drill links keyboard accessible; filter controls labelled.

## Accessibility

Charts have tables/text alternatives; stale state not color-only; report totals labelled.

## Dependencies

RPT-001–007; finance; vaccinations; inventory; local aggregates.

## Open questions / not approved

Official report definitions, refunds/discounts, export formats, PHI export permissions.

## Design notes and evidence boundary

All report values are fictional design data. No aggregate is shown without a path to source records.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
