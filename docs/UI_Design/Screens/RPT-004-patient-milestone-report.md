# RPT-004 · Patient milestone report

> **Design specification 51 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `RPT-004` |
| Section | Reports |
| Feature | Statistics and Reports |
| Source specification | `15-Statistics-and-Reports.md` |
| Prototype | [RPT-004.html](../prototype/screens/RPT-004.html) |
| Rendered reference | [RPT-004.png](../screenshots/RPT-004.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Show due, overdue and completed milestone populations with drill-down to patient records.

## Users

Admin, doctor

## Permissions

Admin/doctor only.

## Entry points

Statistics & reports; due vaccination dashboard.

## Navigation

Filter window/vaccine; open due list; drill to patient.

## Layout regions

- Page header
- Filter bar
- Four metrics
- Milestone status bars
- By-vaccine summary
- Milestone table

## Components

- Metric cards
- Bar chart
- Summary list
- Patient table
- Status badges

## Data shown

- 23 due
- 2 overdue
- 87% coverage
- 6 fictional patients

## Actions

- Export CSV
- Print
- Filter
- Open due list

## Forms and fields

- Date range
- Vaccine
- Milestone

## States

- Loading
- Empty
- Ready
- Stale
- Permission denied

## Offline and data behavior

Local due list labelled; terminal reminder states reflected.

## Keyboard

Table drill links; chart alternative; filters.

## Accessibility

Status textual; due dates explicit; coverage explained.

## Dependencies

RPT-001; reminders; patients; reports.

## Open questions / not approved

Official milestone definitions and coverage calculation method.

## Design notes and evidence boundary

Coverage is illustrative; no clinical target is asserted.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
