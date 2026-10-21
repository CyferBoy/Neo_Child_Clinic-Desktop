# REM-004 · Create personal reminder

> **Design specification 38 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `REM-004` |
| Section | Follow-up |
| Feature | Personal Reminders |
| Source specification | `11-Personal-Reminders.md` |
| Prototype | [REM-004.html](../prototype/screens/REM-004.html) |
| Rendered reference | [REM-004.png](../screenshots/REM-004.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Create a dated or explicitly undated personal follow-up with optional patient linkage and informational advance.

## Users

Clinical/reception roles

## Permissions

Create per role; finance posting separate.

## Entry points

Personal reminders New reminder.

## Navigation

Save → list. Cancel → list.

## Layout regions

- Page header
- Person form
- Follow-up form
- Notification preview rail
- Rules

## Components

- Patient link/name/phone
- Reminder text
- Vaccine interest
- Advance amount
- Date/undated
- Assignee
- Note

## Data shown

- Aarav Sharma linked
- PCV interest
- ₹0 advance
- 21 Oct 2026

## Actions

- Save reminder
- Cancel

## Forms and fields

- Linked patient (optional)
- Name + phone if unlinked
- Reminder (required)
- Vaccine interest
- Advance ≥ 0
- Date or explicit undated
- Assignee
- Note

## States

- Ready
- Saving
- Blank date warning
- Invalid amount
- Offline
- Conflict

## Offline and data behavior

Local create/outbox; notifications scheduled locally using IST.

## Keyboard

Form order; undated checkbox; save shortcut documented.

## Accessibility

Required unlinked fields clear; notification preview text; no PHI in placeholder.

## Dependencies

PER-001–005; notifications; finance boundary.

## Open questions / not approved

Advance/refund semantics, assignment ownership, messaging scope and undated support.

## Design notes and evidence boundary

No advance is posted as income here.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
