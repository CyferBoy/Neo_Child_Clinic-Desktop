# AUTH-002 · Restoring session

> **Design specification 2 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `AUTH-002` |
| Section | Authentication |
| Feature | Authentication and Session |
| Source specification | `02-Authentication-and-Session.md` |
| Prototype | [AUTH-002.html](../prototype/screens/AUTH-002.html) |
| Rendered reference | [AUTH-002.png](../screenshots/AUTH-002.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Show safe, non-PHI progress while the trusted core validates the cached session and role before opening records.

## Users

All staff

## Permissions

Cached session only; role must validate before PHI is unlocked.

## Entry points

Warm or cold start with a stored refresh token.

## Navigation

Success → Dashboard (or last safe route). Failure → Sign in or Access denied.

## Layout regions

- Centered brand mark
- Progress and step list
- No navigation
- No patient data

## Components

- Progress bar
- Three validation steps
- Security footnote

## Data shown

- No patient identifiers
- No role name until verified

## Actions

- None while validation runs
- Application quit via native window control

## Forms and fields



## States

- Validating
- Offline validation
- Expired session
- Revoked session
- Local database unlock error

## Offline and data behavior

May validate cached session and open the local copy only if the approved policy permits. No new writes are silently marked synced.

## Keyboard

No interactive controls inside the content area. Native window close remains available.

## Accessibility

Progress uses text, not color alone; steps are announced in order; no spinner-only state.

## Dependencies

AUTH-001; ADR-0004; local database unlock; role resolution.

## Open questions / not approved

Offline cold-start behavior is unresolved. Do not implement until the session policy is approved.

## Design notes and evidence boundary

The step labels describe intended checks, not verified desktop behavior.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
