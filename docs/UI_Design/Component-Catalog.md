# Component Catalogue

**Status:** prototype catalogue. These are design components generated as static HTML/CSS, not production React components.

**Implementation source:** [`prototype/tools/components.py`](prototype/tools/components.py)  
**Styles:** [`prototype/assets/app.css`](prototype/assets/app.css)  
**Icon source:** local inline SVG via `icon()`; no icon CDN.

## 1. Shell components

| Component | Class / helper | Used in | States | Notes |
|---|---|---|---|---|
| App frame | `.app` | All authenticated screens | default | 1366×768 fixed prototype frame; production should be responsive |
| Sidebar | `.sidebar`, `sidebar()` | All authenticated screens | active item, attention count | Deep teal; groups are labelled; active item has a high-contrast surface |
| Sidebar group | `.nav-group`, `.nav-label` | All authenticated screens | default | Uppercase group label; 10px |
| Sidebar item | `.nav-item` | All authenticated screens | hover, active, attention | Icon + label + optional count |
| Sidebar user | `.sidebar-user` | All authenticated screens | hover | Shows name/role; no token |
| Topbar | `.topbar`, `topbar()` | All authenticated screens | default | 56px; global search, sync, notifications, user |
| Global search | `.topbar-search` | All authenticated screens | focus, typed | `Ctrl/Cmd+K` focus in prototype; no real search |
| Sync chip | `.sync-chip` | All authenticated screens | Online, Syncing, Offline, Attention | Text + icon; not colour-only |
| Notification button | `.icon-btn` with dot | All authenticated screens | unread dot | Dot is decorative; accessible label required |
| User chip | `.user-chip` | All authenticated screens | hover | Name, role, menu affordance |
| Workspace | `.workspace` | All authenticated screens | default | 24px horizontal / 20px vertical padding |
| Page head | `.page-head`, `page_head()` | Most screens | with/without actions, with meta | Eyebrow, title, subtitle, actions, optional meta |
| Page actions | `.page-actions` | Most screens | stacked/wrapped | Primary action first visually, but DOM order should follow reading order |
| Card | `.card` | Most screens | default, selected, warning | White surface, 1px border, light shadow |
| Card head/body/foot | `.card-head`, `.card-body`, `.card-foot` | Most screens | default | Head may contain title, sub, badges and actions |

## 2. Navigation and controls

| Component | Class / helper | Used in | States | Notes |
|---|---|---|---|---|
| Primary button | `.btn.primary` | Forms, dialogs, page heads | default, hover, focus, disabled | One primary action per region |
| Secondary button | `.btn.secondary` | Page heads, forms | default, hover, focus | White surface, brand border |
| Ghost button | `.btn.ghost` | Tertiary actions, cancel | default, hover, focus | No border |
| Danger button | `.btn.danger` | Destructive confirmation | default, focus | Never used for ordinary cancel |
| Small button | `.btn.sm` | Row actions, compact cards | default, focus | 32px height |
| Icon button | `.icon-btn`, `icon_btn()` | Topbar, row actions | default, hover, focus | Must have accessible label; no unlabelled destructive icon |
| Button group | `.btn-group` | Segmented actions | default | Joined borders |
| Tabs | `.tabs`, `tabs()` | Lists, detail sections | active, hover | Text + count; active state has border/colour |
| Segmented control | `.segmented` | Density, filters | active, hover | Used in `SET-001` |
| Theme choice | `.theme-choice` | `SET-001` | selected, hover | Swatch + label + description + radio dot |
| Checkbox | `.checkbox`, `.check-row` | Forms, tables | checked, unchecked, focus | 16px visual box; label is part of the target |
| Radio | `.radio-dot` | Theme choice | checked/unchecked | Not used as a standalone unlabelled control |
| Toggle | `.toggle` | Settings where applicable | on/off | Not a substitute for a labelled checkbox in clinical forms |

## 3. Status and identity

| Component | Class / helper | Used in | States | Notes |
|---|---|---|---|---|
| Badge | `.badge` | Tables, cards, page heads | success, warning, danger, info, brand, neutral, outline | Text label always present |
| Status pill | `.status-pill` | Tables, system status | online/offline/pending/synced | Dot + text; dot is not the only cue |
| Avatar | `.avatar`, `avatar()` | Tables, patient identity | brand, info, apricot, success | Initials only; fictional names |
| Identity cell | `.identity`, `.identity-main` | Patient/staff tables | default | Avatar + name + stable identifier/role |
| Sync/status dot | `.status-dot` | Sync chip, status pill | semantic colour | Decorative; text carries meaning |
| Count / attention badge | `.nav-count` | Sidebar, tabs | default, attention | Number is textual |

## 4. Data display

| Component | Class / helper | Used in | States | Notes |
|---|---|---|---|---|
| Table | `.table`, `table()` | Lists, reports, audit, inventory | default, selected row, hover | Fixed layout; explicit width classes |
| Table header | `.table th` | All tables | default | 10px uppercase; must not collide with adjacent headers |
| Table cell | `.table td` | All tables | default, money, actions | 38px compact density; ellipsis for overflow |
| Row checkbox | `.checkbox` in table | Patient, staff, inventory lists | checked/unchecked | Header checkbox has accessible label |
| Money cell | `.money` | Finance, receipts, reports | default | Mono, tabular numerals, right-aligned |
| Row action | `.row-action` | Lists | hover, focus | Chevron or overflow menu; target at least 32px |
| Pagination | `.pagination`, `pagination()` | Lists | current page, disabled | Always states range and total |
| Filter bar | `.toolbar`, `.toolbar-select` | Lists, reports | default, active filter | Search + selects + filter button |
| Empty state | `.empty` | Lists, reports, audit | empty | Explains what will appear and the next safe action |
| Loading state | `.loading` / skeleton | Lists, reports, auth | loading | Static prototype shows representative copy, not a live spinner |
| Key-value list | `.kv-list`, `kv_list()` | Detail cards, system, receipts | default | Label/value rows; label is not colour-only |
| Stat line | `.stat-line` | System, settings, checks | default, success, warning, danger | Icon + text + value |
| Summary line | `.summary-line` | Backup preview, finance summaries | default, total | Label/value; total row separated |
| Metric card | `.metric`, `metric()` | Dashboard, reports, lists | default, trend | Value + label + foot; not a chart substitute |
| Timeline | `.timeline`, `timeline()` | Print history, audit, detail | neutral, success, warning, danger | Vertical line + event title/time/body |
| Alert | `.alert` | Forms, system, conflicts | info, success, warning, danger | Persistent; includes icon and text |
| Notice list | `.notice-list` | Dashboard alerts | compact | Used in the dashboard rail |

## 5. Forms

| Component | Class / helper | Used in | States | Notes |
|---|---|---|---|---|
| Field | `.field`, `field()` | All forms | default, focus, error, disabled | Label above control; optional help/error |
| Input | `.input` | All forms | default, focus-within, error | 38px; icon optional |
| Select | `.select` | Filters, forms, settings | default, focus-within | Text truncates with ellipsis; chevron is decorative |
| Textarea | `.textarea` | Notes, addresses, resolution notes | default, focus-within | Minimum height; label always present |
| Search input | `.search-input` | Lists, global search | default, focus | Placeholder is not the only label in production |
| Required marker | `.req` | Forms | default | Red asterisk plus explanatory copy |
| Help text | `.help` | Forms, settings | default | 10.5–11px; accessible muted token |
| Error text | `.error-text` | Forms | error | Inline; first error focused |
| Form section | `.form-section` | Long forms | default | Head + body; groups related fields |
| Form grid | `.grid-2`, `.grid-3`, `.grid-4` | Forms, settings | default | Fixed widths in print/prototype to avoid WeasyPrint flex bugs |
| Check row | `.check-row` | Settings, confirmations | checked/unchecked | Label wraps with control; target height ≥32px |
| Choice card | `.choice-card` | Sync conflict | selected/unselected | Used for deliberate resolution choices |
| Confirmation phrase | field with placeholder `RESTORE` | `SYS-007` | default, error | Typed phrase required for destructive restore |
| Passphrase field | field with lock icon | `SYS-006`, `SYS-007` | default, focus, error | No value shown; never logged |
| Settings section | `.settings-section` | `SET-001`–`SET-004` | default | Head + body + optional actions |
| Settings nav | `.settings-nav` | Settings | active | Secondary navigation inside the workspace |

## 6. Overlays

| Component | Class / helper | Used in | States | Notes |
|---|---|---|---|---|
| Dialog | `.dialog` | Delete, archive, merge, conflict, batch selection | default, wide, narrow, sheet | Focus trap and return focus required |
| Dialog header/body/foot | `.dialog-head`, `.dialog-body`, `.dialog-foot` | Dialogs | default | Destructive variant uses danger icon |
| Drawer | `.drawer` | Patient quick view, reminder detail, audit event | default, wide | Contextual detail without losing the list |
| Overlay backdrop | `.overlay`, `.overlay.soft` | Modal/drawer screens | default, soft | Background is dimmed; no click-through |
| Close button | `.close-x` | Dialog/drawer | hover, focus | Accessible label required |

## 7. Charts and visual evidence

| Component | Class / helper | Used in | States | Notes |
|---|---|---|---|---|
| Line chart | `.line-chart`, `line_chart()` | Dashboard, finance report | default | Inline SVG; fictional values; text labels |
| Mini bars | `.mini-bars`, `mini_bars()` | Reports, wastage | default | Labels below; values not only in colour |
| Donut | `.donut`, `donut()` | Finance report, payment split | default | Centre value/label; legend text |
| Sparkline / trend | inline SVG | Dashboard metrics | default | Supporting only; metric value is textual |
| Chart legend | `.legend` | Charts | default | Text label + swatch; no colour-only series |
| Chart empty/loading | text state | Reports | empty/loading | Must not render an empty white box without explanation |

## 8. Receipt and print

| Component | Class / helper | Used in | States | Notes |
|---|---|---|---|---|
| Receipt paper | `.receipt-paper` | `RCP-001`, `RCP-003` | preview, printed, duplicate | White paper, fixed width, print-specific CSS |
| Receipt table | `.receipt-table` | Receipt | default | Line items; amount right-aligned |
| Receipt total | `.receipt-total` | Receipt | default | Total separated by rule |
| QR placeholder | `.qr-box` | Receipt | default | Decorative placeholder; no real QR payload |
| Print settings | card with printer/paper | `RCP-001`, `RCP-002` | default | No extra PHI; duplicate marker optional |
| Print history | timeline | `RCP-002` | neutral/warning/danger | Reprints audited; original number retained |

## 9. State components

| State | Visual treatment | Used in | Rule |
|---|---|---|---|
| Loading | Skeleton or explicit “Loading…” with context | Lists, reports, auth | Do not show an empty table as if it were a result |
| Empty | Icon + explanation + safe next action | Lists, reports, audit | Distinguish “no records” from “no matches” |
| No results | Filter summary + clear filters | Search/lists | Keep the query visible |
| Offline | Global chip + local explanation | All operational screens | Offline is not an error; pending writes are allowed where specified |
| Pending sync | Badge/status + row-level marker | Vaccination, finance, stock | “Saved locally” is not “synced” |
| Conflict | Hard-stop card + both sides + resolution | `SYS-002` | Never last-write-wins |
| Permission denied | Explanation + safe route back | `AUTH-004`, reports, admin | Do not reveal restricted data |
| Stale data | Badge + “as of” timestamp | Dashboard, reports | Export must not imply completeness |
| Error | Inline alert + retry/back; no PHI in copy | Forms, system | Preserve user input where safe |
| Destructive confirmation | Danger dialog + consequence + reason/typed phrase | Delete, merge, restore, deactivate | No auto-submit; cancel is safe default |

## 10. Component usage rules

1. **No component is an authorization control.** Hiding a button or route is not enough.
2. **No unlabelled icon-only destructive action.** Overflow menus must expose text labels.
3. **No colour-only status.** Use text, icon or shape as well.
4. **No placeholder-only labels.** Clinical and financial fields need visible labels.
5. **No toast-only clinical error.** Critical errors persist until resolved.
6. **No automatic dismissal of destructive or clinical alerts.**
7. **No extra PHI in print.** The receipt and report print styles are explicit.
8. **No production dependency claim.** These components are HTML/CSS prototypes generated by local Python helpers.

## 11. Known component gaps

- No real combobox, date picker, file picker, toast system or data grid implementation exists; the prototype shows static representations.
- Dialog/drawer focus trapping is specified but not implemented in the static prototype.
- Table sorting, column visibility and keyboard row navigation are design requirements, not prototype features.
- The prototype does not include a production chart library.
- Dark variants exist only for three screens.
- Empty/loading states are represented in selected screens, not every list.
