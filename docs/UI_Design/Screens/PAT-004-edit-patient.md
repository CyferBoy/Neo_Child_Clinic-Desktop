# PAT-004 · Edit patient

> **Design specification 11 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `PAT-004` |
| Section | Patients |
| Feature | Patient Management |
| Source specification | `04-Patient-Management.md` |
| Prototype | [PAT-004.html](../prototype/screens/PAT-004.html) |
| Rendered reference | [PAT-004.png](../screenshots/PAT-004.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Edit demographic and contact details while preserving audit and avoiding clinical-note overwrite.

## Users

Admin, doctor, receptionist (proposed)

## Permissions

Edit demographics only where approved; archive is role-gated.

## Entry points

Patient profile Edit.

## Navigation

Save returns to profile with audit; archive opens its own confirmation.

## Layout regions

- Profile context behind scrim
- Right drawer form
- Record metadata
- Footer actions

## Components

- Drawer
- Form fields
- Audit metadata
- Archive link

## Data shown

- Fictional patient demographics
- Created/updated metadata

## Actions

- Save changes
- Cancel
- Archive

## Forms and fields

- Full name
- DOB
- Gender
- Phone
- Alternate phone
- Address

## States

- Ready
- Saving
- Validation error
- Conflict
- Permission denied

## Offline and data behavior

Local edit and outbox; conflict surfaces rather than silently overwriting.

## Keyboard

Focus enters drawer; Escape cancels if no unsaved changes; focus returns to Edit.

## Accessibility

Drawer is a labelled dialog; background inert; form errors announced.

## Dependencies

PAT-001–007; audit.

## Open questions / not approved

Whether receptionists may edit and whether edits to identifiers require re-verification are unresolved.

## Design notes and evidence boundary

Clinical history is deliberately not editable in this drawer.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
