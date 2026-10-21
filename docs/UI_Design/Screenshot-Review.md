# Screenshot Review

**Scope:** design-package verification only. No mockup, HTML page, production
application file or database object was regenerated or modified.

## Result

- Screens: **68**
- Screenshots: **73** (base + dark/wide variants)
- Batches: **8** (largest batch **10** images)
- Reviewed: **68** of **68** screens
- Failed review: **9**
- Unreviewed: **0**

Every batch was limited to 10 images. A screen with dark or wide variants
occupies multiple slots in its batch, and the variants are never split from
the base screen.

## Batch results

| Batch | Images | Screens | Status |
|---|---:|---:|---|
| `batch-001` | 10 | 7 | complete |
| `batch-002` | 10 | 9 | complete |
| `batch-003` | 10 | 10 | complete |
| `batch-004` | 10 | 10 | complete |
| `batch-005` | 10 | 10 | complete |
| `batch-006` | 10 | 10 | complete |
| `batch-007` | 10 | 9 | complete |
| `batch-008` | 3 | 3 | complete |

## Screens needing attention

| Screen | Status | Summary |
|---|---|---|
| `AUTH-001` | reviewed_fail | Sign-in base is clean and complete, but the 1920 wide variant is broken: the form is clipped at 1366px, the panel stops at 768px high and most of the canvas is blank. |
| `SHELL-001` | reviewed_pass_with_notes | Search overlay is complete and legible; only the wrapped footer key hint is a minor cosmetic flaw. |
| `DASH-001` | reviewed_fail | Base and dark dashboards look polished, but the wide variant loses the right column, fourth KPI, actions and status pills, leaving most of the canvas empty. |
| `PAT-001` | reviewed_pass_with_notes | Base list is complete and well aligned; the dark variant is coherent but its active 'All patients' filter chip loses its text label. |
| `VAC-003` | reviewed_pass_with_notes | Batch selection modal is clear and complete, with workable row states; only a product-name typo and an awkward subtitle wrap detract. |
| `VAC-004` | reviewed_pass_with_notes | Vaccination visit detail is legible with consistent totals, but the body uses only the left two-thirds, leaving a large empty right column. |
| `CON-001` | reviewed_pass_with_notes | Consultation list is clean, legible and well spaced; the pagination count does not match the number of visible rows. |
| `CON-002` | reviewed_fail | New consultation form layout is collapsed: fields are squeezed into narrow columns, text wraps word by word, and clinical notes overlap helper text. |
| `INV-001` | reviewed_pass_with_notes | Inventory overview is clear and well organised; the footer expiry note does not agree with the table's nearest PCV expiry. |
| `INV-003` | reviewed_fail | Edit vaccine drawer is legible but taller than the 768px viewport; save and cancel controls are off-screen and metadata is clipped. |
| `INV-004` | reviewed_pass_with_notes | Batch detail is complete and legible, with KPIs, ledger and batch facts aligned. Ledger dates and one reference truncate, and the Batch controls panel appears empty. |
| `INV-006` | reviewed_pass_with_notes | Adjust-stock data reconciles (28 - 2 = 26), but a detached select chevron renders outside the dialog edge and the action footer sits below the viewport. |
| `WAS-001` | reviewed_pass_with_notes | Wastage overview is well structured, with consistent KPIs, filters and chart. One reason cell clips 'Cold-chain breakage' mid-word. |
| `BRW-001` | reviewed_pass_with_notes | Borrow/return overview is legible, but status chips clip at the table edge, the active Open tab shows closed records, and BR-1042's due date conflicts with its overdue flag. |
| `BRW-002` | reviewed_fail | Record borrow/lend layout is broken: the direction and counterparty grid collapses, squeezing inputs to a few characters wide and wrapping helper text one word per line. |
| `BRW-003` | reviewed_pass_with_notes | Return dialog content and stock math are clear, but its confirm action is below the 768px fold, background status chips clip, and the due date is labelled overdue despite being in the future. |
| `REM-002` | reviewed_pass_with_notes | Reminder side panel is readable and matches Aarav Sharma's row, but no completion action is visible within the 768px viewport. |
| `REM-003` | reviewed_pass_with_notes | Personal reminders list is complete and legible, with clear tabs, table, pagination and advisory notices. Only small cosmetic text-fitting issues in the search field and linked-patient column. |
| `REM-004` | reviewed_fail | Create-reminder form layout is broken: the follow-up fields collapse into a narrow column, values wrap word-by-word outside their controls, labels collide, and most of the card is empty. |
| `FIN-006` | reviewed_fail | Record-expense form layout is broken: the field grid collapses into slivers, Title and Note values wrap vertically outside their controls, labels overlap, and the card is mostly blank. |
| `RPT-003` | reviewed_fail | The finance chart is clipped by the daily rows table, hiding the plot's lower area and x-axis labels; this layout overlap needs fixing. |
| `RPT-004` | reviewed_fail | The results table overlaps the milestone chart and the By vaccine panel, slicing the vaccine list mid-row; this is a blocking layout defect. |
| `STF-002` | reviewed_pass_with_notes | Add staff drawer is clear, but its primary action and role summary sit below the 768px viewport, requiring scroll without a visible footer. |
| `AUD-001` | reviewed_pass_with_notes | Audit log is legible and well structured; source and one action label are ellipsized, and later rows continue below the fold. |
| `AUD-002` | reviewed_pass_with_notes | Audit event drawer is complete and legible, with clear actor, event, integrity and redacted payload sections; the sidebar shows two emphasized destinations at once. |
| `SYS-001` | reviewed_pass_with_notes | Sync center is clear and consistent, with a complete outbox table and connection details, but the Sync actions panel is empty. |
| `SYS-004` | reviewed_pass_with_notes | Update and readiness cards are legible, but the Blocked state does not name a blocker and the Install update button still looks available. |
| `SYS-005` | reviewed_pass_with_notes | Backup stats, history and settings are complete and legible; the Retention helper reads like an implementation note rather than user guidance. |
| `SYS-007` | reviewed_pass_with_notes | Restore preview clearly presents manifest, compatibility and confirmation, but the primary restore action looks available before the safety snapshot and confirmation are complete. |
| `SET-001` | reviewed_pass_with_notes | Appearance settings are clean and consistent in both themes, but the dark variant still displays Light as the selected theme. |
| `SET-003` | reviewed_pass_with_notes | Complete security settings screen with clear hierarchy and consistent styling. Minor note: its save action sits below the card instead of in the top-right header used by sibling screens. |
| `SET-004` | reviewed_pass_with_notes | Complete clinic and safety form with consistent layout and controls. Two numeric fields duplicate their unit suffixes, showing '10 doses doses' and '30 days days'. |

## Unreviewed screens

None. Every screen has a review result.

## Method and safeguards

1. `review/review.py prepare` checked every PNG for existence, non-zero size,
   readability, non-blank content and expected dimensions before any visual
   review was requested.
2. Screens were packed into batches of at most 10 images. All variants of one
   screen stay in the same batch and count toward that batch's limit.
3. Each batch was reviewed in a fresh AI session with only that batch's image
   paths. No batch inherited earlier images, and concise per-screen summaries
   plus the manifest carried context between batches.
4. The batch prompts contain file paths only; they do not embed image data.
5. Failed or missing batch results stay `unreviewed` and are listed above.

## Request-size audit

Observed image parts in each isolated reviewer session. The count is the
maximum number of image parts present in a model request in that session.

| Batch | Reviewer session | Images | Max in request |
|---|---|---:|---:|
| `batch-001` | `ses_ea35c67fbffeIBAFx9HsNT8lpW` | 10 | 10 |
| `batch-002` | `ses_ea35c67f7ffeVDrJ9MLHGlvm3n` | 10 | 10 |
| `batch-003` | `ses_ea35c67f4ffe83POR1d6SlpDl8` | 10 | 10 |
| `batch-004` | `ses_ea35c67ddffeDoAiyHqciTuf6r` | 10 | 10 |
| `batch-005` | `ses_ea350d266ffeHHl7f5kvhpvlM3` | 10 | 10 |
| `batch-006` | `ses_ea350d260ffeEKuC44Cuq7kdnQ` | 10 | 10 |
| `batch-007` | `ses_ea350d25bffeUjRanwgv2OrW1Q` | 10 | 10 |
| `batch-008` | `ses_ea350d247ffev7bZQeL7lfAsup` | 3 | 3 |

Maximum observed: **10 / 10**.
Violations: **0**.

## Validation

- `python docs/UI_Design/review/review.py check` must pass.
- Maximum images in any batch: **10 / 10**.
- Screenshot coverage: **73** images across **68** screens.
