# VAC-003 · Batch selection

> **Design specification 17 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `VAC-003` |
| Section | Vaccinations |
| Feature | Vaccination Management |
| Source specification | `05-Vaccination-Management.md` |
| Prototype | [VAC-003.html](../prototype/screens/VAC-003.html) |
| Rendered reference | [VAC-003.png](../screenshots/VAC-003.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Choose an explicit, valid batch and make expiry and availability visible before commit.

## Users

Admin, doctor, nurse

## Permissions

Record vaccination; inventory visibility per role.

## Entry points

Record vaccination batch selector.

## Navigation

Use selected batch → form. Cancel → form unchanged.

## Layout regions

- Form context behind scrim
- Wide batch dialog
- Search/filter
- Batch comparison table
- FEFO note

## Components

- Batch table
- Expiry
- On-hand
- Net rate
- Status badges
- Selection acknowledgement

## Data shown

- AV-2409 (48)
- AV-2408 (12, expiring first)
- AV-2410 (60)
- Expired AV-2312 blocked

## Actions

- Use selected batch
- Cancel
- Search batch

## Forms and fields

- Batch selection (required)

## States

- Ready
- Selected
- Expired disabled
- Insufficient stock
- Batch changed since load

## Offline and data behavior

Uses local stock; selection is revalidated at commit because another device may consume the last dose.

## Keyboard

Table rows selectable with keyboard; Enter confirms; Escape closes.

## Accessibility

Expiry and stock numbers are text; expired rows not color-only; selection announced.

## Dependencies

VAC-004; inventory batches; FEFO policy.

## Open questions / not approved

Whether FEFO is mandatory or only a default is unresolved.

## Design notes and evidence boundary

The dialog makes FEFO visible but not silent. Manual selection remains explicit.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
