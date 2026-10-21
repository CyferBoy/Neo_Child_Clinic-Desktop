# PAT-001 · Patient list

> **Design specification 8 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `PAT-001` |
| Section | Patients |
| Feature | Patient Management |
| Source specification | `04-Patient-Management.md` |
| Prototype | [PAT-001.html](../prototype/screens/PAT-001.html) |
| Rendered reference | [PAT-001.png](../screenshots/PAT-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Find, filter and act on active patient records without loading the full patient table into the renderer.

## Users

Admin, doctor, receptionist, nurse

## Permissions

Read all clinical roles; create per approved role; edit/merge/archive role-gated.

## Entry points

Sidebar Patients; dashboard links; global search 'view all'.

## Navigation

Open profile; register; merge; export; filter chips.

## Layout regions

- Page header
- Saved views
- Search and filters
- Patient table
- Pagination

## Components

- Search input
- Filter chips
- Data table
- Status badges
- Pagination
- Bulk selection box

## Data shown

- 2,418 active records (fictional)
- 8 visible patients
- Clinic IDs, ages, phones, last visit, next due

## Actions

- Register patient
- Merge records
- Filter
- Sort (not shown as active)
- Export
- Open patient

## Forms and fields

- Search query
- Filter chips

## States

- Loading skeleton
- Empty clinic
- No search results
- Offline/pending
- Permission-limited columns

## Offline and data behavior

Local index search; pending-sync filter remains available; archived records excluded.

## Keyboard

/ focuses search; arrow keys move rows in implementation; Enter opens; selection checkboxes have labels.

## Accessibility

Table caption and scope attributes required; status text as well as color; row actions labelled with patient name in implementation.

## Dependencies

PAT-001–007; local search; role gates.

## Open questions / not approved

Clinic ID format and whether nurses may create/edit are unresolved. Export scope is not approved.

## Design notes and evidence boundary

Rows are fictional. The table is bounded; the renderer must not fetch all patients to filter locally.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
