# SET-001 · Appearance settings

> **Design specification 65 of 68.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.

| Field | Value |
|---|---|
| Screen ID | `SET-001` |
| Section | Settings |
| Feature | Settings |
| Source specification | `20-Settings.md` |
| Prototype | [SET-001.html](../prototype/screens/SET-001.html) |
| Rendered reference | [SET-001.png](../screenshots/SET-001.png) |
| Review status | Draft for product/clinical/security review |

## Purpose

Set personal theme, density and workspace display defaults without changing clinic policy.

## Users

All staff

## Permissions

Device preference only; no PHI and no secrets.

## Entry points

Sidebar Settings; user menu.

## Navigation

Notifications; security; clinic settings; save preferences.

## Layout regions

- Page header
- Settings secondary nav
- Theme cards
- Density control
- Workspace defaults
- Save row

## Components

- Secondary nav
- Theme choice cards
- Segmented control
- Select fields
- Save/reset

## Data shown

- Light/dark themes
- Comfortable density
- Dashboard landing
- 8 rows
- INR

## Actions

- Select theme
- Select density
- Save preferences
- Reset to defaults

## Forms and fields

- Theme
- Density
- Landing page
- Rows per table
- Sidebar mode
- Currency display

## States

- Ready
- Saving
- Invalid/corrupt preference
- Theme preview
- Permission not applicable

## Offline and data behavior

Local device preferences work offline. Corrupt values fall back to safe defaults.

## Keyboard

Theme cards and segmented control keyboard accessible; focus visible; save reachable.

## Accessibility

Theme choices not color-only (labels/descriptions); density does not reduce text below minimum; contrast maintained.

## Dependencies

SET-001–005; design tokens; local settings.

## Open questions / not approved

Is system theme supported? Density policy? Locale/currency beyond INR?

## Design notes and evidence boundary

Theme is device-local and does not alter clinical semantics.

## Evidence boundary

No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.

This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.
