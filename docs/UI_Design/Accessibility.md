# Accessibility

**Target:** WCAG 2.2 Level AA for the production desktop application.  
**Status:** design intent and prototype review. **No formal accessibility audit, screen-reader test or automated conformance run has been performed.**

**Related:** [`Design-System.md`](Design-System.md) · [`Component-Catalog.md`](Component-Catalog.md) · [`States-and-Errors.md`](States-and-Errors.md)

## 1. Scope and evidence boundary

The prototype is static HTML/CSS. It demonstrates layout, contrast, focus styling and content order, but it does **not** prove that the future React application is accessible. In particular:

- many visual controls are `div` elements rather than native inputs, so a screen reader would not treat them as real form controls;
- there is no focus trap implementation, no live region and no server-driven validation;
- there is no automated axe/Pa11y run, browser matrix or assistive-technology test;
- dark mode is rendered for only three screens;
- the prototype is fixed to 1366×768 and 1920×1080; it is not a reflow test.

The production implementation must use semantic HTML, native controls where possible, tested focus management and automated plus manual accessibility checks.

## 2. Design principles

1. **Clinical safety over visual minimalism.** Status, errors and destructive consequences must be explicit in text.
2. **Keyboard first for repetitive work.** Search, lists, forms and dialogs must be operable without a mouse.
3. **No colour-only meaning.** Every status has a label or icon.
4. **Readable density.** Dense tables are allowed, but text must remain legible at 100% and 200% zoom.
5. **Predictable focus.** Focus order follows visual order; dialogs trap focus and return it.
6. **Recoverable errors.** Errors identify the field, preserve input and explain the next safe action.
7. **Privacy by default.** Notifications and previews hide patient names; no PHI in URLs or logs.

## 3. Colour and contrast

Measured token pairs (WCAG relative luminance; normal text target 4.5:1):

| Pair | Ratio | Result |
|---|---|---|
| `ink-900` on `bg` | 13.83:1 | Pass |
| `ink-900` on white | 14.94:1 | Pass |
| `ink-600` on white | 6.06:1 | Pass |
| `ink-500` on white | 4.90:1 | Pass after adjustment |
| `ink-500` on `bg` | 4.54:1 | Pass |
| `brand-700` on `brand-50` | 6.96:1 | Pass |
| `success-700` on `success-100` | 7.04:1 | Pass |
| `warning-700` on `warning-100` | 6.88:1 | Pass |
| `danger-700` on `danger-100` | 7.34:1 | Pass |
| `info-700` on `info-100` | 8.25:1 | Pass |
| white on `brand-700` | 7.58:1 | Pass |
| white on `danger-600` | 6.87:1 | Pass |
| dark `ink-900` on dark `bg` | 15.07:1 | Pass |

The light `--ink-500` was darkened from `#6b7d80` to `#627477` during validation because the original pair measured 4.31:1 on white and failed AA for normal text. Placeholder text now uses `--ink-500` instead of the lighter `--ink-400`.

**Still required in production**

- Measure every final foreground/background pair, including hover, disabled, selected, dark mode and print.
- Do not use `ink-400` for instructional placeholder text.
- Do not use colour alone for overdue, expired, pending, conflict or selected states.
- Focus indicators must have at least 3:1 contrast against adjacent colours and remain visible on cards, tables and dark surfaces.
- Charts must not rely on colour alone; use labels, patterns or direct values.

## 4. Keyboard model

| Key | Expected behaviour |
|---|---|
| `Tab` / `Shift+Tab` | Move focus in visual order; focus is trapped in a modal |
| `Enter` | Activate the focused control; submit a form when focus is in a field |
| `Space` | Toggle checkboxes and selected rows; activate buttons |
| `Esc` | Close dialog/drawer, clear search, or cancel a menu; protect unsaved changes |
| Arrow keys | Move within menus, tabs, segmented controls and table rows where implemented |
| `Home` / `End` | First/last item in a list or table where implemented |
| `Ctrl/Cmd+K` | Focus global search (implemented in the static prototype) |
| `Ctrl/Cmd+S` | Save the current form where safe (proposed; must not bypass validation) |
| `Ctrl/Cmd+P` | Print preview where permitted (proposed) |

Rules:

- Every action available by mouse must be available by keyboard.
- Row actions must have accessible names that include the row identity, e.g. “Open visit for Aarav Sharma, V-10942”.
- Icon-only buttons require an accessible label.
- The prototype's `Ctrl/Cmd+K` handler focuses the global search; it does not implement real search.
- Focus must not be moved unexpectedly on load.
- A modal must not allow focus to escape to the background.
- On close, focus returns to the trigger, or to the next logical control if the trigger no longer exists.

## 5. Focus and skip navigation

The prototype adds a visible `:focus-visible` outline using `--focus` (`#0b6e78`, 5.97:1 on white) and a focus-within ring for field containers. Production must also provide:

- a visible “Skip to main content” link as the first focusable element;
- a landmark structure: banner, navigation, main, complementary where appropriate;
- a focus indicator that is not clipped by table overflow or card borders;
- a logical focus order that follows the visual reading order;
- no positive `tabindex` values.

## 6. Forms

- Labels are visible and programmatically associated with controls.
- Required fields are marked with `*` and an explanation; the marker is not the only cue.
- Help text is associated with the field, not only shown on hover.
- Errors are inline, specific and announced; the first invalid field receives focus.
- Do not rely on placeholder text as a label.
- Do not clear the form on a failed save.
- Use native `input`, `select`, `textarea`, `button` and `fieldset`/`legend` in production.
- Group related choices with a fieldset and legend.
- Password fields provide a show/hide control with an accessible name; the value is never logged.
- Destructive confirmations require an explicit choice; do not preselect the destructive option.
- Autocomplete attributes should be used for staff sign-in and patient contact fields where appropriate, subject to privacy review.

## 7. Tables and data grids

- Use a real `<table>` with `<caption>`, `<thead>`, `<th scope="col">` and, where needed, `scope="row"`.
- Do not use a table only for visual layout in production.
- Sortable headers expose `aria-sort`.
- Row selection is communicated in text, not only by a highlighted background.
- Pagination announces the current range and total.
- Horizontal scrolling must be keyboard-accessible and not hide the row action.
- Sticky headers must not obscure focused rows.
- Empty and no-results states are announced.
- Money and identifiers use readable text; mono font is not a substitute for accessible labels.

## 8. Dialogs, drawers and alerts

- Dialogs use `role="dialog"` with `aria-modal="true"` and an accessible title.
- Focus moves to the first meaningful control or the dialog container; it does not start on the destructive button.
- Background content is inert while the dialog is open.
- `Esc` closes only when it is safe; unsaved changes prompt.
- Critical alerts use `role="alert"` or a live region with appropriate politeness; they do not auto-dismiss.
- A success toast may be polite; a clinical, stock, payment or destructive error must persist.
- Do not move focus to a toast.
- The close control has an accessible name (“Close dialog”), not just an icon.

## 9. Charts and visual evidence

- Every chart has a title, unit, date range and text summary.
- Values are available as text or a table, not only as bar height or colour.
- Legends use text labels; patterns or direct labels supplement colour.
- A chart with no data says “No data for this range”, not an empty box.
- Do not use animation to convey a change in a clinical metric.
- Charts are decorative only when an equivalent text value is adjacent.

## 10. Target size, zoom and reflow

- Normal controls: 38px height; compact row actions: 32px minimum.
- Target size should meet WCAG 2.2 AA (24×24 CSS px minimum) with adequate spacing; the design prefers 32px+.
- The production app must support 200% zoom without loss of content or function.
- At 1366×768, the design is dense; at 200% zoom, tables and forms must reflow or scroll without clipping actions.
- Do not set `user-scalable=no` or block zoom.
- Text must not be truncated in a way that hides the only copy of a clinical value. Ellipsis is acceptable for secondary metadata only.

## 11. Timeouts and session safety

- Session expiry and idle lock must warn before logout where policy allows.
- A warning must state what will happen and offer “Stay signed in” where safe.
- Do not rely on a silent timeout to protect PHI; lock the screen.
- Pending writes must be surfaced before sign-out.
- The exact idle-lock duration and offline-unlock policy remain unresolved.
- Reauthentication must not expose patient data on the lock screen.

## 12. Motion and cognitive load

- Motion is minimal: 120–160ms hover/press feedback, no looping animation.
- `prefers-reduced-motion` disables transitions and animations.
- No flashing content.
- Critical state changes are not conveyed by motion alone.
- Error messages use plain language and avoid internal jargon.
- Long forms are grouped into labelled sections; the design does not rely on memory across screens.

## 13. Healthcare-specific accessibility

- Patient identity is shown in text before clinical commit.
- Clinical status (due, overdue, expired, pending, conflict) has a text label.
- Notifications hide patient names by default; the accessible notification text is still meaningful without PHI.
- Print previews are readable and do not rely on colour.
- Receipt numbers and amounts are readable as text, not images.
- A screen-reader user must be able to review a receipt before printing.
- Destructive and high-risk actions are not hidden behind unlabelled icons.

## 14. Known gaps in the prototype

| Gap | Impact | Required action |
|---|---|---|
| Visual controls are `div`s | Not a semantic form or table in places | Rebuild with native elements in production |
| No focus trap/live region | Dialogs and async status not fully operable | Implement and test with keyboard + screen reader |
| No screen-reader test | Unknown announcements | Test with NVDA/JAWS/VoiceOver on Windows |
| No automated axe run | Unknown violations | Add axe/Pa11y to CI |
| No 200% zoom test | Possible clipping | Test at 200% and 400% reflow |
| Dark mode limited to 3 screens | Dark contrast unverified elsewhere | Measure and test all tokens |
| No high-contrast/forced-colors test | Windows high-contrast unknown | Test forced-colors mode |
| No reduced-motion test | Motion preference untested | Verify CSS and component behaviour |
| No real validation/error announcements | Error UX unproven | Implement and test live regions |
| No browser matrix | Rendering differences unknown | Test Chromium/WebView2 baseline |

## 15. Manual accessibility checklist

### Keyboard

- [ ] Complete sign-in, search, patient open, vaccination record and sign-out with keyboard only.
- [ ] Open and close every dialog/drawer with `Esc`; focus returns correctly.
- [ ] Tab order follows visual order; no focus traps outside modals.
- [ ] All icon-only buttons have accessible names.
- [ ] Skip link works and is visible on focus.

### Screen reader

- [ ] Page title and main landmark are announced.
- [ ] Form labels, required state, help text and errors are announced.
- [ ] Table caption, headers, sort state and row actions are announced.
- [ ] Status changes (saved locally, synced, conflict) are announced without being noisy.
- [ ] Dialog title and description are announced; background is inert.
- [ ] Receipt content is readable in a logical order.

### Visual

- [ ] All text meets 4.5:1; large text meets 3:1.
- [ ] Focus ring is visible on every surface, including dark and selected rows.
- [ ] Status is not colour-only.
- [ ] At 200% zoom, no action is clipped or unreachable.
- [ ] Windows forced-colors mode preserves borders and focus.
- [ ] Reduced motion removes non-essential animation.

### Content

- [ ] Errors say what happened, what is safe and what to do next.
- [ ] No PHI in URLs, notification previews or error copy.
- [ ] Destructive consequences are explicit.
- [ ] Dates show IST where the boundary matters.
- [ ] Amounts and identifiers are not truncated in the only view.

## 16. Acceptance statement

The design intent is WCAG 2.2 AA, and the measured colour pairs above pass for the specified text pairs. **This is not a conformance claim.** Production accessibility must be verified with semantic implementation, automated checks, keyboard testing and assistive-technology testing before release.
