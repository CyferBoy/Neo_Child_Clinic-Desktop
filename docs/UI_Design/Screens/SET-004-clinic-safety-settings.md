# SET-004 · Clinic & safety settings

> **Design specification 68 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SET-004` |
| Section | Settings |
| Feature | Settings |
| Source specification | `20-Settings.md` |
| Prototype | [SET-004.html](../prototype/screens/SET-004.html) |
| Rendered reference | [SET-004.png](../screenshots/SET-004.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Let admins manage clinic identity, stock safety defaults, backup/update policy and view about/support information.

## Users

Admin only

## Permissions

Admin-only, enforced server-side; changes audited; no secrets.

## Entry points

Settings Clinic & safety.

## Navigation

Appearance; notifications; security; save clinic settings.

## Layout regions

- Page header
- Admin warning
- Settings nav
- Clinic identity
- Stock safety defaults
- Backup/update policy
- About/support
- Save row

## Components

- Form grids
- Selects/checkboxes
- Key-values
- Warnings
- Save/discard

## Data shown

- Neo Child Clinic
- GSTIN placeholder
- 10-dose threshold
- 30-day expiry
- daily backup
- stable channel

## Actions

- Save clinic settings
- Discard

## Forms and fields

- Clinic name/phone/GSTIN/address
- Low-stock threshold
- Expiry warning window
- FEFO behavior
- Adjustment approval
- Backup schedule/destination/retention
- Update channel/install timing
- Backup passphrase requirement

## States

- Ready
- Saving
- Validation
- Permission denied
- Offline disabled
- Conflict
- Audit write failure

## Offline and data behavior

Clinic-wide changes require connectivity; personal preferences remain local.

## Keyboard

Form order; save/discard labelled; errors linked.

## Accessibility

Admin boundary explicit; ranges explained; no color-only warning; receipt identity fields labelled.

## Dependencies

SET-001–005; STF; BAK; UPD; INV; RCP; audit.

## Open questions / not approved

Official clinic identity, receipt legal fields, stock thresholds/FEFO policy, backup destination allowlist, update channel.

## Design notes and evidence boundary

Clinic details are fictional. The screen distinguishes policy proposals from accepted settings.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
