# Validation

**Validated:** 21 October 2026

**Scope:** structural, artifact, link and screenshot validation of the design
package under `docs/UI_Design/`. No production application, backend, database,
Supabase configuration, Android file or Knowledge Base document was changed.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 docs/UI_Design/prototype/tools/validate.py` | 0 | PASS — counts, IDs, dimensions, images, links and assets are consistent |
| `python3 docs/UI_Design/review/review.py check` | 0 | PASS — 8 batches, largest 10 images, every screenshot covered |
| `python3 docs/UI_Design/review/review.py status` | 0 | 68 reviewed, 0 unreviewed, 9 visual-review failures recorded |
| `python3 docs/UI_Design/prototype/tools/render.py --force REM-003 RCP-002 RPT-002 SYS-002` | 0 | 4 PNGs re-rendered; no render failures |

The first command is the final acceptance check. It fails on any missing
screenshot, wrong dimension, blank image, broken local reference, missing asset,
incomplete screen ID, count mismatch or stale render log/failure file.

## Package counts

| Artifact | Count |
|---|---:|
| Screen specifications | 68 |
| Standalone base HTML screens | 68 |
| HTML files including variants and gallery | 74 |
| Screen-inventory rows | 68 |
| Rendered PNGs | 73 |
| Base PNGs at 1366×768 | 68 |
| Dark variants at 1366×768 | 3 |
| Wide variants at 1920×1080 | 2 |
| Review batches | 8 |
| Largest review batch | 10 images |

## Screen ID mapping

All 68 complete screen IDs, such as `AUTH-001`, `PAT-001` and `DASH-001`, match
across these five locations:

1. `Screen-Inventory.md`
2. `Screens/<ID>-<slug>.md`
3. `prototype/screens/<ID>.html`
4. `screenshots/manifest.json`
5. `screenshots/<ID>.png`

`validate.py` extracts IDs with `^([A-Z]+-\d{3})-` and does not split at the first
hyphen. It also verifies the inventory’s per-screen spec, HTML and PNG links and
the gallery’s 68 screen/image links.

## Screenshot verification

All 73 PNGs passed automated checks for existence, non-zero size, Pillow
readability, expected dimensions and non-blank content. Every SHA-256 hash and
byte count recorded in `review/review_manifest.json` matches the current image
files (73/73).

| Kind | Images | Expected size | Result |
|---|---:|---|---|
| Base | 68 | 1366×768 | PASS |
| Dark | 3 | 1366×768 | PASS |
| Wide | 2 | 1920×1080 | PASS |
| **Total** | **73** | — | **PASS** |

### Re-rendered screens

The four screens previously listed in `screenshots/render-failures.txt` were
re-rendered against the current HTML and CSS. Each produced exactly one PDF page,
converted to a readable 1366×768 PNG. The resulting files are byte-identical to
the images already reviewed, so the recorded review verdicts remain valid.

| Screen | PDF pages | PNG size | Bytes | SHA-256 (first 16) |
|---|---:|---|---:|---|
| `REM-003` | 1 | 1366×768 | 173,486 | `2fdfb82fd181930c` |
| `RCP-002` | 1 | 1366×768 | 149,586 | `658b178081da74aa` |
| `RPT-002` | 1 | 1366×768 | 156,821 | `1ee7192ef7ac0441` |
| `SYS-002` | 1 | 1366×768 | 145,899 | `f2c84f92da317356` |

Visual confirmation: `REM-003` is the personal-reminders list; `RCP-002` is the
print-queue error; `RPT-002` is the vaccination report; `SYS-002` is the sync
conflict resolver. All four show the intended screen with legible controls.

`screenshots/render-log.txt` now contains **73** entries and was rebuilt from the
PNG files that actually exist. The stale `screenshots/render-failures.txt` was
removed because no screenshot currently fails to render. `render.py` now accepts
screen IDs for targeted re-renders and reconciles both logs after each run.

## Links, assets and prototype checks

- All Markdown links in the package resolve locally.
- All **1,657** `href`/`src` references in 74 HTML files resolve or are local
  anchors; no remote scripts or stylesheets are used.
- Both `url(...)` font references in `app.css` resolve to bundled font files.
- Required assets exist: gallery, preview guide, `app.css`, `prototype.js`,
  Figtree and Noto Sans font files.
- No `supabase.co`, `service_role` or JWT-like marker appears in the prototype.
- The gallery contains 68 cards and 68 screen/image links; the README artifact
  counts match the files on disk.
- A preview-server smoke test returned HTTP 200 for the gallery, a screen page,
  the stylesheet, the script, a bundled font, a screenshot and a specification.
- Every HTML page has a non-empty body and title, and no page has a generated
  Python cache beside it.
- The empty `workflows/` directory was removed. `Navigation-and-Workflows.md`
  already contains ASCII diagrams for the eleven core workflows, so no extra
  diagram files were needed.

## Visual review status

The screenshot review covers every screen and remains separate from structural
validation:

| Verdict | Screens |
|---|---:|
| Pass | 36 |
| Pass with notes | 23 |
| Fail (visual defect) | 9 |
| Unreviewed | 0 |

The nine visual failures are existing layout/content findings recorded in
[`Screenshot-Review.md`](Screenshot-Review.md):

`AUTH-001`, `DASH-001`, `CON-002`, `INV-003`, `BRW-002`, `REM-004`, `FIN-006`,
`RPT-003`, `RPT-004`.

They were not redesigned in this validation pass. `AUTH-001` and `DASH-001` have
wide variants whose content stays inside a 1366×768 region on the 1920×1080
canvas.

## Corrections in this pass

- Added [`prototype/README.md`](prototype/README.md) with direct-file and
  local-server preview instructions.
- Re-rendered `REM-003`, `RCP-002`, `RPT-002` and `SYS-002`; all four are
  byte-identical to their reviewed images.
- Rebuilt `screenshots/render-log.txt` from all 73 current PNGs and removed the
  stale `screenshots/render-failures.txt`.
- Removed the empty `workflows/` directory; no extra diagrams were needed.
- Strengthened `prototype/tools/validate.py` and `prototype/tools/render.py`.
- No screen HTML or CSS was changed, so the design system and visual direction
  are preserved.

## Known limitations and warnings

- **No browser automation was available.** Chromium, Playwright, Selenium and
  Pyppeteer are not installed, so runtime console errors and interactive
  click-through behavior could not be tested. Static link, asset, script and
  page-text checks passed instead.
- Visual verdicts are AI-assisted design review, not pixel-diff regression tests
  or a substitute for clinical, accessibility or security review.
- No automated contrast-ratio or keyboard-interaction test is included.
- The nine visual-review failures and 23 notes above remain open design findings.
- The package is a design proposal. It does not validate production behavior,
  Android parity, Supabase connectivity or implementation readiness.

## Preview

Full instructions are in [`prototype/README.md`](prototype/README.md). From the
repository root:

```bash
cd /storage/emulated/0/Neo_Child_Clinic_Desktop
python3 -m http.server 8000 --directory docs/UI_Design
```

Open <http://localhost:8000/prototype/index.html> for the gallery and
<http://localhost:8000/prototype/screens/AUTH-001.html> for an individual screen.
Stop the server with `Ctrl+C`.

## Scope confirmation

All changes in this pass are inside `docs/UI_Design/`. No file outside that
directory was modified.
