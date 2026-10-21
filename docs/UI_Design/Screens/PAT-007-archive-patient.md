# PAT-007 · Archive patient

> **Design specification 14 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `PAT-007` |
| Section | Patients |
| Feature | Patient Management |
| Source specification | `04-Patient-Management.md` |
| Prototype | [PAT-007.html](../prototype/screens/PAT-007.html) |
| Rendered reference | [PAT-007.png](../screenshots/PAT-007.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Soft-delete a patient with a reason while keeping clinical and financial history for audit.

## Users

Admin and doctor (proposed)

## Permissions

Merge/archive requires admin or doctor confirmation.

## Entry points

Patient profile more menu or edit drawer Archive.

## Navigation

Archive → active patient list; restore policy not approved.

## Layout regions

- Profile context behind scrim
- Narrow dialog
- Linked-record warning
- Reason field
- Confirmation

## Components

- Destructive dialog
- Warning
- Reason textarea
- Confirmation checkbox

## Data shown

- Fictional patient record
- 3 vaccinations, 2 consultations, 3 payments

## Actions

- Archive patient
- Cancel

## Forms and fields

- Archive reason (required)
- Confirmation checkbox (required)

## States

- Ready
- Validation error
- Archiving
- Linked record blocks
- Already archived

## Offline and data behavior

Archive may be queued only when the deletion contract supports it; current desktop behavior is unresolved.

## Keyboard

Focus trap; archive button requires explicit checkbox; Escape cancels.

## Accessibility

Destructive action labelled; consequences in text; reason field associated with error.

## Dependencies

PAT-006; AUD; sync deletion contract.

## Open questions / not approved

Restore policy and whether archive is allowed offline are unresolved. NCC-039 deletion contract remains open.

## Design notes and evidence boundary

No hard delete. Linked history is preserved.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
