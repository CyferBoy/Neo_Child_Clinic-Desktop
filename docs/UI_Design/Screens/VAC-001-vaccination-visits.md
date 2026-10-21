# VAC-001 · Vaccination visits

> **Design specification 15 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `VAC-001` |
| Section | Vaccinations |
| Feature | Vaccination Management |
| Source specification | `05-Vaccination-Management.md` |
| Prototype | [VAC-001.html](../prototype/screens/VAC-001.html) |
| Rendered reference | [VAC-001.png](../screenshots/VAC-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Review vaccination visits, payment state, batch usage, receipt status and pending local commits.

## Users

Admin, doctor, nurse; inventory manager may view stock only

## Permissions

Recording proposed for admin/doctor/nurse; deletion/correction requires admin/doctor confirmation.

## Entry points

Sidebar Vaccinations; patient profile; dashboard due list.

## Navigation

Open visit; record vaccination; filter pending/corrected; print receipt.

## Layout regions

- Page header
- Summary strip
- Saved status filters
- Search/filter toolbar
- Visit table
- Pagination

## Components

- Summary cards
- Search
- Status chips
- Table
- Receipt status
- Pagination

## Data shown

- 18 doses today
- 2 pending visits
- 1 provisional receipt
- Fictional patients and amounts

## Actions

- Record vaccination
- Export
- Open visit
- Filter

## Forms and fields

- Search
- Date range
- Vaccine filter

## States

- Loading
- Empty
- Ready
- Pending sync
- Provisional receipt
- Corrected/audit state
- Offline

## Offline and data behavior

Local visits remain visible; pending and provisional badges are explicit; no silent receipt numbering.

## Keyboard

/ focuses search; results are keyboard navigable; row actions named with patient/visit.

## Accessibility

Receipt and sync status have text; money uses tabular numerals; table headers scoped.

## Dependencies

VAC-001–007; INV; REM; FIN; RCP; sync.

## Open questions / not approved

Correction vs reversal semantics and who may delete after a receipt are unresolved.

## Design notes and evidence boundary

The list does not compute receipt numbers. A provisional receipt is deliberately marked.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
