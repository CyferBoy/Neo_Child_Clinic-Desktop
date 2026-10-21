# REM-002 · Vaccination reminder detail

> **Design specification 36 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `REM-002` |
| Section | Follow-up |
| Feature | Vaccination Reminders |
| Source specification | `10-Vaccination-Reminders.md` |
| Prototype | [REM-002.html](../prototype/screens/REM-002.html) |
| Rendered reference | [REM-002.png](../screenshots/REM-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Act on one reminder with explicit completion, dismissal or reschedule and preserve prior state in history.

## Users

Clinical roles; admin override

## Permissions

Complete/dismiss per policy; reschedule admin or approved role.

## Entry points

Due list row; notification.

## Navigation

Open patient; reschedule; dismiss; complete. Close returns to list.

## Layout regions

- Due list context behind scrim
- Right drawer
- Patient context
- Reminder details
- Completion form
- History

## Components

- Drawer
- Patient ribbon
- Key-value details
- Completion fields
- Timeline

## Data shown

- Aarav Sharma
- Pentavalent dose 3
- Due 20 Oct 2026
- Notification delivered 08:00

## Actions

- Open patient
- Reschedule
- Dismiss
- Complete

## Forms and fields

- Performed date
- Performed by
- Outcome
- Completion note

## States

- Ready
- Completing
- Dismissal reason required
- Conflict/stale state
- Offline
- Permission denied

## Offline and data behavior

Local completion/dismissal and outbox; terminal state wins on sync.

## Keyboard

Focus enters drawer; Escape closes; actions in logical order.

## Accessibility

Drawer labelled dialog; completion status text; history ordered list.

## Dependencies

REM-001/003/004; vaccinations; notifications; audit.

## Open questions / not approved

Whether a completed reminder can be reopened and who may dismiss it.

## Design notes and evidence boundary

The UI states that completion is terminal; corrections go through the vaccination workflow.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
