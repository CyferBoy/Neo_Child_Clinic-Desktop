# REM-003 · Personal reminders

> **Design specification 37 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `REM-003` |
| Section | Follow-up |
| Feature | Personal Reminders |
| Source specification | `11-Personal-Reminders.md` |
| Prototype | [REM-003.html](../prototype/screens/REM-003.html) |
| Rendered reference | [REM-003.png](../screenshots/REM-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Track non-clinical follow-ups separately from vaccination due reminders and clinic income.

## Users

Admin, doctor, receptionist, nurse

## Permissions

Clinical/reception create; admin override; finance role required to post any advance as income.

## Entry points

Sidebar Personal reminders; patient profile Add reminder.

## Navigation

New reminder; filter pending/completed/cancelled; open detail.

## Layout regions

- Page header
- Advance/income warning
- Status tabs
- Search/filter toolbar
- Personal reminder table
- Undated note

## Components

- Warning alert
- Tabs
- Table
- Status badges
- Advance amount column

## Data shown

- 8 pending
- 14 completed
- 2 cancelled
- ₹500 informational advance
- Fictional people

## Actions

- New personal reminder
- Filter
- Open detail

## Forms and fields

- Search
- Assignee filter
- Date filter

## States

- Loading
- Empty
- Pending
- Completed
- Cancelled
- Undated
- Conflict

## Offline and data behavior

Local create/status and outbox; no network needed for notification scheduling.

## Keyboard

/ search; table rows open; status tabs.

## Accessibility

Advance warning in text; status labels; phone/name fallback clear.

## Dependencies

PER-001–005; notifications; finance; patients.

## Open questions / not approved

Is an advance a real financial transaction? Who owns assignment? Are messages in scope? Can reminders be undated?

## Design notes and evidence boundary

This list does not create income. Advance amounts are explicitly informational.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
