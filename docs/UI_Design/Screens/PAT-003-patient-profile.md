# PAT-003 · Patient profile

> **Design specification 10 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `PAT-003` |
| Section | Patients |
| Feature | Patient Management |
| Source specification | `04-Patient-Management.md` |
| Prototype | [PAT-003.html](../prototype/screens/PAT-003.html) |
| Rendered reference | [PAT-003.png](../screenshots/PAT-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Provide a complete chronological patient timeline across visits, vaccinations, consultations, payments, notes, documents and audit.

## Users

All clinical roles

## Permissions

Read role-scoped; financial actions require finance permission; clinical notes hidden from non-clinical roles.

## Entry points

Patient list or global search result.

## Navigation

Tabs, quick actions, edit, vaccination, consultation, payment, archive.

## Layout regions

- Page header
- Patient identity ribbon
- Tabs
- Timeline
- Record details rail
- Care summary and quick actions

## Components

- Identity ribbon
- Tabs
- Timeline
- Status badges
- Key-value rail
- Alert

## Data shown

- Fictional patient Aarav Sharma
- Visit and vaccination history
- ₹ payments
- Receipt reference

## Actions

- Record vaccination
- New consultation
- Edit
- Add note
- Add reminder
- Archive
- Open sync center

## Forms and fields



## States

- Ready
- Loading
- Empty timeline
- Pending sync
- Conflict
- Archived read-only
- Large timeline pagination

## Offline and data behavior

Timeline reads local data; pending records show local-only badges; cache invalidates after dependent writes.

## Keyboard

Tabs use arrow-key semantics; timeline items are links where applicable; focus ring visible on rail actions.

## Accessibility

Patient name is the page heading; timeline ordered list; dates and times explicit; badges not color-only.

## Dependencies

PAT-004; VAC; CON; FIN; RCP; REM; AUD; local cache.

## Open questions / not approved

Documents eligibility, note visibility, and whether archived records can be restored are unresolved.

## Design notes and evidence boundary

The timeline must not be cached independently from dependent writes.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
