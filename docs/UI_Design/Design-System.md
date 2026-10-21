# Design System — Calm Clinical Precision

**Status:** proposed design system for a desktop application that does not yet exist.  
**Source of truth for the prototype:** [`prototype/assets/app.css`](prototype/assets/app.css)  
**Component usage:** [`Component-Catalog.md`](Component-Catalog.md)  
**Accessibility evidence:** [`Accessibility.md`](Accessibility.md)

## 1. Direction

The product is used at a clinic front desk and in clinical rooms, often for long shifts, with a mix of fast keyboard entry and careful review. The visual language therefore prioritises:

1. **Calm over decorative.** Deep teal anchors the shell; warm apricot is reserved for attention and humanity, not for every accent.
2. **Clinical legibility.** Dense tables remain readable at 1366×768. Status is never communicated by colour alone.
3. **Trustworthy surfaces.** White cards on a soft green-grey background; clear borders; restrained shadows.
4. **Deliberate danger.** Destructive actions, sync conflicts and PHI warnings use strong semantic colour and explicit language.
5. **Local-first honesty.** Pending, stale, offline and conflict states are visible in the interface rather than hidden behind a spinner.

The result is intentionally closer to a clinical record system than to a consumer dashboard. It is not playful, not glassy and not dependent on animation.

## 2. Layout and density

| Token | Value | Use |
|---|---|---|
| `--sidebar-width` | `232px` | Persistent primary navigation |
| `--topbar-height` | `56px` | Global search, sync status, notifications, user |
| `--page-pad-x` | `24px` | Workspace horizontal padding |
| `--page-pad-y` | `20px` | Workspace vertical padding |
| `--row-height` | `44px` | Base table row token |
| `--control-height` | `38px` | Buttons and fields |
| `--control-height-sm` | `32px` | Compact row actions |
| 1366×768 content width | `1086px` | 232px sidebar + 24px padding each side |
| 1920×1080 content width | `1640px` | Same shell rules |

The prototype uses a **compact table density** at 1366×768: 34px headers and approximately 38px body rows, 28px avatars and 11.5px identity names. This is a deliberate viewport fit, not a claim that 38px is the final production row height. The density control in `SET-001` exposes comfortable/compact preferences; production must validate readability with real content and OS scaling.

**Spacing scale:** 4, 6, 8, 10, 12, 14, 16, 20, 24, 28, 32px. The prototype uses the lower half of the scale heavily.

**Grid:** 12-column mental model, but screens use explicit flex/grid regions rather than a rigid 12-column library. Lists and forms are allowed to fill the available width. Right rails are 300–430px.

## 3. Colour

### 3.1 Core palette

| Token | Light | Role |
|---|---|---|
| `--bg` | `#f3f7f5` | Workspace background |
| `--surface` | `#ffffff` | Cards, dialogs, tables |
| `--surface-2` | `#f8fbfa` | Table headers, subtle bands |
| `--surface-3` | `#eaf1ef` | Neutral chips, secondary controls |
| `--brand-950` | `#072e32` | Sidebar depth |
| `--brand-900` | `#0a3a3f` | Sidebar |
| `--brand-800` | `#0d4a50` | Strong brand text |
| `--brand-700` | `#0f5d64` | Primary actions, focus-adjacent accents |
| `--brand-600` | `#14747c` | Hover/secondary brand |
| `--brand-300` | `#8bc3bf` | Borders, selected outlines |
| `--brand-100` | `#dcefed` | Selected rows, brand badges |
| `--brand-50` | `#eef7f6` | Quiet brand surfaces |
| `--apricot-600` | `#a94e28` | Warm accent text |
| `--apricot-500` | `#c26b43` | Warm accent |
| `--apricot-100` | `#fbeadf` | Warm badge/background |
| `--ink-900` | `#172a2d` | Primary text |
| `--ink-700` | `#3c5256` | Strong secondary text |
| `--ink-600` | `#52666a` | Secondary text |
| `--ink-500` | `#627477` | Muted text, table headers |
| `--border` | `#d7e2e0` | Default border |
| `--border-strong` | `#b5c6c3` | Input border |
| `--focus` | `#0b6e78` | Keyboard focus ring |

### 3.2 Semantic colours

| State | Text | Background | Meaning |
|---|---|---|---|
| Success | `--success-700 #145c3b` | `--success-100 #e5f4ec` | Synced, verified, paid, active |
| Warning | `--warning-700 #7a4900` | `--warning-100 #fff3dd` | Due, expiring, pending review, blocked-but-recoverable |
| Danger | `--danger-700 #8f241e` | `--danger-100 #fbe9e7` | Overdue, conflict, destructive, failed |
| Info | `--info-700 #174b6c` | `--info-100 #e8f3fa` | Neutral system guidance, offline explanation |
| Brand | `--brand-800 #0d4a50` | `--brand-100 #dcefed` | Selected, navigational, primary context |
| Neutral | `--ink-600 #52666a` | `--surface-3 #eaf1ef` | Default badge, inactive |

Status always has a text label or icon in addition to colour. Do not use a bare coloured dot for a clinical state.

### 3.3 Contrast measurements

Measured from the token values (WCAG relative luminance; normal text target 4.5:1):

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

The light `--ink-500` was darkened from `#6b7d80` to `#627477` during validation because the original pair measured 4.31:1 on white and failed AA for normal text. Placeholder text now uses the same accessible muted token rather than the lighter `ink-400`.

### 3.4 Dark theme

The dark theme is a **variant of the same semantics**, not a separate brand. It uses:

- background `#0e1c1e`, surface `#142628`, elevated surface `#1a3033`;
- light ink `#e8f0ef` / `#d4e2e0` / `#b7cac7`;
- brand accents `#6cc5c8` / `#83d3d4` / `#9edfe0`;
- the same success/warning/danger/info families with dark-appropriate text and background pairs.

Dark variants are provided for `DASH-001`, `PAT-001` and `SET-001`. The full screen set is designed to use tokens so a future dark mode can be applied consistently, but only those three dark pages are rendered evidence.

## 4. Typography

| Role | Family | Size / weight |
|---|---|---|
| Display / page title | Figtree | 24px / 700, -0.45px tracking |
| Card title | Figtree | 14px / 700 |
| Section title | Figtree | 13.5px / 700 |
| Eyebrow | Figtree | 10px / 700, uppercase, 0.9px tracking |
| Body | Noto Sans | 13px / 400, line-height 1.45 |
| Page subtitle | Noto Sans | 12.5px / 400 |
| Table header | Noto Sans | 10px / 700, uppercase, 0.45px tracking |
| Table body | Noto Sans | 12px / 400 |
| Identity name | Noto Sans | 11.5px / 600 |
| Identity sub | Noto Sans | 9.5px / 400 |
| Buttons | Noto Sans | 12px / 700 (small 11px) |
| Money / codes | DejaVu Sans Mono | 11.5px, tabular numerals |
| Helper text | Noto Sans | 10.5–11px |

Fonts are local files under [`prototype/assets/fonts/`](prototype/assets/fonts/): Figtree variable and Noto Sans variable. The prototype does not load a remote font.

**Rules**

- Do not go below 9.5px for metadata; 10px is the practical floor for dense clinical tables.
- Do not use uppercase for sentences; reserve it for eyebrows and table headers.
- Money and identifiers use the mono face to reduce digit ambiguity.
- Line length for clinical notes should be constrained; the current page subtitle max-width is 740px.

## 5. Shape, border and elevation

| Token | Value |
|---|---|
| `--radius-xs` | 4px |
| `--radius-sm` | 6px |
| `--radius-md` | 9px |
| `--radius-lg` | 12px |
| `--radius-xl` | 16px |
| `--radius-pill` | 999px |
| `--shadow-sm` | `0 1px 2px rgba(7,46,50,.06)` |
| `--shadow-md` | `0 8px 24px rgba(7,46,50,.09)` |
| `--shadow-lg` | `0 18px 48px rgba(7,46,50,.18)` |

Cards use a 1px border and a very light shadow. Dialogs and drawers may use the large shadow. Do not stack multiple heavy shadows.

## 6. Components and patterns

The full catalogue is in [`Component-Catalog.md`](Component-Catalog.md). The system-level rules are:

### Shell
- 232px deep-teal sidebar, 56px topbar, 24px workspace padding.
- Sidebar groups: Workspace, Inventory, Follow-up, Business, Administration.
- The sync chip is global and must remain visible on every operational screen.
- The search field is global; `Ctrl/Cmd+K` focuses it in the prototype.
- The topbar never contains patient-identifying information beyond the active user.

### Buttons
- One primary action per region.
- Secondary actions use a white surface with a brand border.
- Ghost buttons are for low-risk navigation or tertiary actions.
- Danger buttons are reserved for destructive confirmation, not for ordinary cancel.
- Disabled buttons must explain why nearby; opacity alone is not an explanation.
- Minimum target: 32px for compact row actions, 38px for normal controls.

### Tables
- Fixed layout for dense clinical tables; explicit column width classes prevent header collisions.
- Header labels are uppercase but readable; every table has a text caption or surrounding card title.
- Row actions are right-aligned; destructive row actions never appear as an unlabelled icon alone.
- Money uses mono, right-aligned, tabular numerals.
- Pagination always states the range and total; never show an unlabelled page control.
- Empty states explain what will appear and the next safe action.

### Forms
- Labels above controls; required fields marked with `*` and explained.
- Help text sits below the field, not inside a tooltip only.
- Errors are inline and focus the first invalid field.
- Destructive confirmations require a reason and/or typed phrase where specified.
- Forms must not rely on placeholder text as the only label.
- Offline is not an error: saving locally is allowed, and pending sync is shown.

### Dialogs and drawers
- Use a dialog for a decision that interrupts the workflow; use a drawer for contextual detail or editing without losing the list.
- Destructive dialogs use the danger icon and explicit consequence text.
- Focus moves into the dialog and returns to the trigger on close.
- Do not auto-dismiss a clinical error or a destructive confirmation.

### Status and alerts
- Use the semantic families consistently.
- A warning that can be recovered is not styled as a fatal error.
- A conflict is a hard stop, not a toast.
- Critical alerts stay until resolved or explicitly dismissed; the prototype shows persistent alert blocks.

### Charts
- Charts are supporting evidence, not the only representation of a number.
- Every chart has a text title, a unit and a table or metric equivalent.
- Don't rely on colour alone for series; label bars/legend.
- The prototype uses simple CSS/SVG charts with fictional values, not a charting dependency.

### Receipts and print
- Receipt preview is a white paper surface, independent of the app theme.
- The receipt shows only the fields intended for print; no hidden PHI.
- Receipt number is server-assigned and immutable.
- Print failure never voids a payment or changes the number.
- Print CSS uses a block layout and explicit page dimensions; it does not depend on app-level flex.

## 7. Content and tone

- Use plain clinical language: “Due today”, “Overdue by 4 days”, “Pending sync”, “Not yet printed”.
- Avoid vague success language: “Saved” is not enough when the write is local but not synced.
- State the consequence before the action: “This will merge two patient records and keep the audit trail.”
- Use “patient” and “child” consistently; do not alternate for style.
- Do not expose internal table names, tokens or implementation jargon in user-facing copy.
- Amounts use the Indian grouping style and `₹`; the prototype uses fictional amounts.
- Dates show IST explicitly where a due/report boundary matters.

## 8. Motion

Motion is minimal and functional:

- 120–160ms for hover/press feedback.
- No looping animation in clinical screens.
- No animation that could obscure a status change.
- `prefers-reduced-motion` disables transitions and animations.
- The static prototype does not depend on animation to convey state.

## 9. Print and 1920 behaviour

- Base page: 1366×768.
- Wide reference: 1920×1080 for `AUTH-001` and `DASH-001`. The shell remains 232px; the workspace expands and cards reflow within the same hierarchy.
- Print CSS fixes the workspace height and uses an absolutely positioned sidebar with a 232px offset main column. This is a rendering workaround for WeasyPrint; production should use a normal responsive shell.
- `@media print` uses CSS grid for form layouts where needed. Flex-wrap caused WeasyPrint layout hangs during prototype rendering and is avoided in print-only form rules.
- Receipt print styles reduce padding and table spacing so the document fits one page.

## 10. Implementation notes and non-claims

- The CSS is a **prototype stylesheet**, not a production design-token package.
- No component library, Tailwind configuration or production dependency is introduced.
- The renderer is static HTML; interactive behaviour is limited to local prototype JavaScript.
- No dark-mode parity is claimed for all 68 screens; only three dark variants are rendered.
- The design system is ready to be translated into React components only after approval and after the open decisions in the backlog are resolved.
