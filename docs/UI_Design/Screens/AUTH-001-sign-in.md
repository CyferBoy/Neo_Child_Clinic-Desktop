# AUTH-001 · Sign in

> **Design specification 1 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `AUTH-001` |
| Section | Authentication |
| Feature | Authentication and Session |
| Source specification | `02-Authentication-and-Session.md` |
| Prototype | [AUTH-001.html](../prototype/screens/AUTH-001.html) |
| Rendered reference | [AUTH-001.png](../screenshots/AUTH-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Authenticate a staff member with Supabase Auth without exposing tokens to the renderer.

## Users

All staff

## Permissions

Unauthenticated. Supabase Auth email/password; role resolved by the trusted core after sign-in.

## Entry points

Application launch with no valid session, or explicit sign-out.

## Navigation

Successful sign-in → session restore → role-aware Dashboard. Failure stays on this screen.

## Layout regions

- Brand story panel (left, 46%)
- Sign-in card (right)
- Security and support note
- Preview theme control

## Components

- Email field
- Password field with show control
- Primary sign-in
- Auth reachability indicator

## Data shown

- Fictional staff email
- No patient data

## Actions

- Sign in
- Show password
- Contact administrator

## Forms and fields

- Email (required, email format)
- Password (required, masked)

## States

- Ready
- Invalid credentials
- Rate limited
- Network unavailable
- Account deactivated

## Offline and data behavior

Sign-in requires the shared Supabase Auth service. A previously validated session may restore offline only under the approved session policy.

## Keyboard

Tab order: email → password → show → sign in. Enter submits. Escape clears focus; it does not dismiss the screen.

## Accessibility

Visible labels; 4.5:1 contrast; focus ring; password field has explicit label; error announced via aria-live in implementation.

## Dependencies

AUTH-001–006; ADR-0004; ADR-0008; trusted Go auth boundary.

## Open questions / not approved

No desktop implementation. Session lifetime, offline cold-start policy and password reset surface remain unapproved.

## Design notes and evidence boundary

Tokens must stay in Go memory/OS keychain and never enter the renderer. This screen displays no clinic data.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
