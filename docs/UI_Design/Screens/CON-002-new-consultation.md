# CON-002 · New consultation

> **Design specification 21 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `CON-002` |
| Section | Consultations |
| Feature | Consultation Management |
| Source specification | `06-Consultation-Management.md` |
| Prototype | [CON-002.html](../prototype/screens/CON-002.html) |
| Rendered reference | [CON-002.png](../screenshots/CON-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Capture a doctor consultation linked to a patient, visit, doctor, date, follow-up and payment.

## Users

Admin, doctor

## Permissions

Receptionist may schedule but must not write clinical notes.

## Entry points

Consultation list; patient profile; dashboard.

## Navigation

Save → consultation detail. Cancel → prior screen.

## Layout regions

- Page header
- Patient ribbon
- Consultation form
- Payment section
- Patient context rail
- Linked visit rail

## Components

- Clinical text fields
- Follow-up date
- Payment split
- Role warnings

## Data shown

- Fictional Aarav Sharma
- Mild viral fever
- ₹500 paid
- Follow-up 27 Oct

## Actions

- Save consultation
- Cancel

## Forms and fields

- Patient (via context)
- Doctor (required)
- Date/time (required)
- Problem (required)
- Clinical notes
- Follow-up date
- Fee
- Cash + online = total
- Payment reconciliation acknowledgement

## States

- Ready
- Saving
- Validation error
- Missing visit
- Payment mismatch
- Offline
- Conflict

## Offline and data behavior

Local commit and outbox; conflict preserves both versions rather than overwriting notes.

## Keyboard

Form order; date controls keyboard accessible; save shortcut documented in implementation.

## Accessibility

Labels visible; error text linked; note length bounded; no PHI in placeholders.

## Dependencies

CON-003–005; patients; finance; receipts; audit.

## Open questions / not approved

Payment categories, addenda policy and one-consultation-per-visit rule are unresolved.

## Design notes and evidence boundary

The note shown is fictional clinical content for layout testing only.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
