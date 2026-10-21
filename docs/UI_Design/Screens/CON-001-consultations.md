# CON-001 · Consultations

> **Design specification 20 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `CON-001` |
| Section | Consultations |
| Feature | Consultation Management |
| Source specification | `06-Consultation-Management.md` |
| Prototype | [CON-001.html](../prototype/screens/CON-001.html) |
| Rendered reference | [CON-001.png](../screenshots/CON-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Review consultations, linked payments, follow-ups and pending notes without exposing notes to non-clinical roles.

## Users

Admin, doctor; reception may schedule but not write clinical notes

## Permissions

Clinical notes admin/doctor; payment columns finance-permitted roles.

## Entry points

Sidebar Consultations; patient profile; dashboard.

## Navigation

New consultation; open detail; filter by doctor/date; export.

## Layout regions

- Page header
- Summary strip
- Search/filter toolbar
- Consultation table
- Role-scope note

## Components

- Summary cards
- Table
- Status badges
- Search
- Filters

## Data shown

- 6 consultations today
- 9 follow-ups in 7 days
- 1 pending note
- Fictional patients and amounts

## Actions

- New consultation
- Export
- Open consultation

## Forms and fields

- Search
- Doctor filter
- Date range

## States

- Loading
- Empty
- Ready
- Pending sync
- Permission denied
- Offline

## Offline and data behavior

Local reads; pending note badge; clinical notes remain local until sync.

## Keyboard

/ focuses search; table rows and actions keyboard accessible.

## Accessibility

Role-scoped columns explained; statuses textual; clinical note column not shown to unauthorized roles.

## Dependencies

CON-001–005; patients; finance; receipts.

## Open questions / not approved

Can receptionists create a consultation shell? Addenda vs edits? One consultation per visit?

## Design notes and evidence boundary

Clinical notes are deliberately absent from the list preview beyond the problem label.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
