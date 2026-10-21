# PAT-002 · Register patient

> **Design specification 9 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `PAT-002` |
| Section | Patients |
| Feature | Patient Management |
| Source specification | `04-Patient-Management.md` |
| Prototype | [PAT-002.html](../prototype/screens/PAT-002.html) |
| Rendered reference | [PAT-002.png](../screenshots/PAT-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Create an offline-capable, idempotent demographic record with a stable UUID and unique clinic ID.

## Users

Admin, doctor, receptionist, nurse (create permission proposed)

## Permissions

Create is proposed for all four roles; confirm before implementation.

## Entry points

Patient list Register; dashboard Register patient; global search action.

## Navigation

Save → patient profile. Save & add vaccination → vaccination form with patient prefilled.

## Layout regions

- Page header with actions
- Child details form
- Contact and address form
- Initial note
- Right validation and next-steps rail

## Components

- Text/date/select fields
- Textarea
- Duplicate-check confirmation
- Context rail
- Primary and secondary save

## Data shown

- Prefilled fictional DOB and registration date
- Generated clinic ID placeholder

## Actions

- Register patient
- Save & add vaccination
- Cancel

## Forms and fields

- Full name (required)
- DOB (required, not future)
- Gender (required, allowed values)
- Phone (required, normalized)
- Alternate phone
- Address (optional, bounded)
- Initial note
- Duplicate-check acknowledgement

## States

- Ready
- Saving/local commit
- Validation error
- Duplicate warning
- Offline
- Conflict on clinic ID

## Offline and data behavior

Writes commit to the local database and outbox; retry is idempotent by patient UUID.

## Keyboard

Tab order follows visual order; date picker keyboard accessible; Ctrl/Cmd+Enter saves in implementation.

## Accessibility

Labels are always visible; required fields indicated with text/asterisk; errors linked to fields; no placeholder-only labels.

## Dependencies

PAT-001–007; local persistence; audit; duplicate search.

## Open questions / not approved

Role permissions, clinic ID format, and whether initial notes are clinical are unresolved.

## Design notes and evidence boundary

The clinic ID is intentionally not editable in this design. A duplicate warning must appear before commit.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
