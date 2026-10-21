# PAT-006 · Merge patients

> **Design specification 13 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `PAT-006` |
| Section | Patients |
| Feature | Patient Management |
| Source specification | `04-Patient-Management.md` |
| Prototype | [PAT-006.html](../prototype/screens/PAT-006.html) |
| Rendered reference | [PAT-006.png](../screenshots/PAT-006.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Merge duplicate identities while preserving dependent history, payments and audit.

## Users

Admin and doctor (proposed)

## Permissions

Merge/archive requires admin or doctor confirmation; confirm policy.

## Entry points

Patient list Merge records, or duplicate review.

## Navigation

Merge → surviving profile. Failure → both records remain.

## Layout regions

- Patient list context behind scrim
- Wide comparison dialog
- Primary/secondary cards
- Field resolution table
- Confirmation

## Components

- Comparison table
- Primary/secondary cards
- Merge confirmation
- Warning alert

## Data shown

- Fictional duplicate Aarav records
- Dependent record counts

## Actions

- Merge records
- Cancel

## Forms and fields

- Primary record selection
- Field resolution
- Merge acknowledgement

## States

- Ready
- Blocked by open visit
- Conflict
- Merging
- Failed rollback
- Offline policy blocked

## Offline and data behavior

Merge is queued only if the policy supports it; otherwise this operation requires connectivity.

## Keyboard

Selection controls and comparison table are keyboard accessible; destructive merge requires explicit confirmation.

## Accessibility

Diff table uses headers; primary vs secondary not color-only; consequence described plainly.

## Dependencies

PAT-001–007; FIN; VAC; CON; audit; sync conflict policy.

## Open questions / not approved

Is merge reversible? Who may merge? How are conflicting clinic IDs resolved?

## Design notes and evidence boundary

This is a high-risk flow. Do not implement until the merge policy and rollback behavior are approved.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
