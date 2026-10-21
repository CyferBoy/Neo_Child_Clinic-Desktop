# REM-001 · Due vaccinations

> **Design specification 35 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `REM-001` |
| Section | Follow-up |
| Feature | Vaccination Reminders |
| Source specification | `10-Vaccination-Reminders.md` |
| Prototype | [REM-001.html](../prototype/screens/REM-001.html) |
| Rendered reference | [REM-001.png](../screenshots/REM-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Show active, overdue and upcoming vaccination reminders using IST boundaries and role-relevant ownership.

## Users

Admin, doctor, nurse, receptionist

## Permissions

View/complete/dismiss per policy; admin can reschedule/override with audit.

## Entry points

Sidebar Due vaccinations; dashboard due widget; notification deep link.

## Navigation

Open reminder detail; reschedule; complete; dismiss; open patient.

## Layout regions

- Page header
- Summary strip
- Status tabs
- Search/filter toolbar
- Reminder table
- IST and terminal-state note

## Components

- Summary cards
- Tabs
- Table
- Status badges
- Notification status

## Data shown

- 2 overdue
- 5 due today
- 16 in 7 days
- 23 completed this week
- Fictional patients

## Actions

- New reminder
- Export
- Open reminder
- Filter

## Forms and fields

- Search
- Vaccine filter
- Assignee filter

## States

- Loading
- Empty
- Ready
- Overdue
- Completed
- Dismissed
- Pending sync
- Notification permission denied

## Offline and data behavior

Local due list and status transitions; notifications local; terminal states must win over stale active updates.

## Keyboard

/ search; table rows open; tabs arrow-key semantics.

## Accessibility

Due state uses text and dates; overdue not color-only; external timezone note.

## Dependencies

REM-001–006; notifications; sync; patients; vaccinations.

## Open questions / not approved

Retention/legal status requirements, reschedule limits, dismissal roles, SMS/WhatsApp scope, deletion reconciliation contract.

## Design notes and evidence boundary

Reminder deletion/absence reconciliation (NCC-023) remains unresolved; the UI does not promise resurrection protection beyond terminal state handling.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
