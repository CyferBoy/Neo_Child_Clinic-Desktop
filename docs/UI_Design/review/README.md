# Screenshot Review Workflow

This directory contains the **only** supported way to run visual AI review of the
rendered screenshots in `docs/UI_Design/screenshots/`.

It exists because reviewing a large screenshot set in one agent conversation can
silently exceed the model provider's image limit. The provider rejects the whole
request when the **total number of image parts still attached to the
conversation** exceeds 30. Batching alone is not enough if the batches run in the
same conversation, because images from earlier turns remain attached.

## Root cause of `Too many images in request: 31 > 30`

The original validation pass had no enforced image budget:

- The agent read screenshots with ad-hoc `read` calls in groups of 8, 10 and 11.
- Those groups all ran in one long-lived session. Image parts from previous
  batches were still present when the next request was assembled.
- The immediate trigger was an 11-image `read` turn (`BRW-002`, `BRW-003`,
  `CON-002`, `FIN-004`, `FIN-006`, `INV-003`, `INV-005`, `PAT-004`, `REM-002`,
  `REM-004`, `STF-002`). Earlier images from the same session brought the request
  to 31 image parts.
- Measured composition of that failing request after the previous compaction:
  **7 single-image turns + 11-image batch + 3-image batch + 10 further single
  images = 31**. The 11-image batch was over the intended per-batch budget, and
  every earlier image was still attached.
- No script, manifest or prompt enforced a maximum, tracked which screenshots had
  already been reviewed, or required a fresh session per batch.

The fix is not "read fewer images per call". The fix is a hard batch budget plus
an isolated request per batch.

## Non-negotiable rules

1. **Maximum 10 images in any model request.** The count is image parts, not
   screenshot files. A dark or wide variant consumes a slot.
2. **All variants of a screen stay together.** If a screen has base, dark and wide
   images, those three images occupy three slots in the same batch. Never split a
   screen's variants across batches.
3. **One fresh session per batch.** A batch is reviewed once, by an agent that
   sees only that batch. Do not review batch 2 in the conversation that reviewed
   batch 1. Do not ask the same agent to "continue" with the next batch.
4. **Read each batch's images in one turn**, using parallel `read` calls for the
   exact paths in the batch JSON. Do not read extra images for context.
5. **Paths, not embedded payloads, in prompts and manifests.** Batch JSON and
   prompt files contain file paths and metadata only. The image bytes enter the
   request only when the reviewer opens the listed files.
6. **Automated checks run first.** Existence, non-zero size, Pillow readability,
   non-blank content and expected dimensions must pass before a batch is created.
7. **Manifest is the memory.** Each batch writes a small result JSON. The
   manifest and per-screen summaries carry context forward; a later reviewer must
   not re-open earlier screenshots.
8. **Retry only the failed batch**, in a new session, with the same batch file.
   Screens with no valid result remain `unreviewed` and are reported.
9. **Do not regenerate mockups.** This workflow only reads existing PNGs and
   writes under `docs/UI_Design/review/` plus `docs/UI_Design/Screenshot-Review.md`.

## Commands

Run from the repository root or from this directory:

```bash
python docs/UI_Design/review/review.py prepare
python docs/UI_Design/review/review.py check
python docs/UI_Design/review/review.py collect
python docs/UI_Design/review/review.py status
```

`prepare` reads `screenshots/manifest.json`, validates all 73 PNGs with Pillow,
writes `review_manifest.json` / `review_manifest.csv`, and creates batches with a
maximum of 10 images. It refuses to create batches if any image fails an
automated check.

`check` verifies that:

- every batch has 10 or fewer images and its `image_count` matches;
- every screenshot appears in exactly one batch;
- no screen is split across batches;
- every screenshot still exists, is readable, is not blank and has the expected
  dimensions;
- every result file, if present, reports no more than 10 images.

`collect` merges `results/batch-NNN.json` into the manifest, writes the CSV, and
regenerates [`Screenshot-Review.md`](../Screenshot-Review.md). Missing or invalid
batch results are marked `unreviewed`, not silently passed.

## Batch contract

Each `batches/batch-NNN.json` contains:

```json
{
  "batch_id": "batch-001",
  "image_count": 10,
  "max_images": 10,
  "screen_ids": ["AUTH-001", "..."],
  "images": [
    {
      "screen_id": "AUTH-001",
      "path": "screenshots/AUTH-001.png",
      "kind": "base",
      "width": 1366,
      "height": 768,
      "sha256": "..."
    }
  ],
  "prompt": "review/prompts/batch-001.md",
  "result": "review/results/batch-001.json"
}
```

Reviewer output:

```json
{
  "batch_id": "batch-001",
  "images_reviewed": 10,
  "reviewed_at": "2026-10-21T00:00:00+00:00",
  "notes": "Batch-level summary.",
  "screens": [
    {
      "screen_id": "AUTH-001",
      "verdict": "pass",
      "summary": "Sign-in form is complete and legible.",
      "issues": []
    }
  ]
}
```

Allowed verdicts: `pass`, `pass_with_notes`, `fail`. A screen with any blocking
defect must use `fail`. Cosmetic issues use `pass_with_notes`.

## How to run a batch

1. Generate the batch set with `prepare`.
2. Start a **new** agent session. Give it only:
   - the path to `review/prompts/batch-NNN.md`;
   - the instruction to follow that prompt exactly.
3. The reviewer reads the batch JSON, opens every listed image in one turn, and
   writes `review/results/batch-NNN.json`.
4. Close that session. Repeat from step 2 for the next batch. Never reuse a
   session.
5. Run `collect`, then `check`.
6. If a batch failed, start a new session for that batch only. Fix the result or
   leave the screens `unreviewed` and report them.

If the client cannot guarantee a fresh session per batch, do not run the visual
review automatically. Use the manifest and file paths for a manual review, or
review one batch per manual request.

## Status values

| Status | Meaning |
|---|---|
| `pending` | Batch prepared; visual review not collected yet. |
| `reviewed_pass` | Reviewed; no issues. |
| `reviewed_pass_with_notes` | Reviewed; non-blocking issue(s) recorded. |
| `reviewed_fail` | Reviewed; blocking visual defect. |
| `unreviewed` | No valid batch result; must be reported, not treated as passed. |
| `blocked_automated_checks` | Image check failed before AI review. |

## Files

| Path | Purpose |
|---|---|
| `review.py` | Prepare, validate, collect and report. |
| `review_manifest.json` | Authoritative screen → screenshot(s) → status record. |
| `review_manifest.csv` | Spreadsheet-friendly view of the same manifest. |
| `batches/` | Per-request input bundles, each ≤10 images. |
| `prompts/` | Ready-to-use reviewer prompts. Paths only, no image data. |
| `results/` | Reviewer output, one JSON per batch. |
| `request-audit.json` | Observed image count per isolated reviewer session. |
| `../Screenshot-Review.md` | Final human-readable result and unreviewed list. |

## Request-size guarantee

The workflow guarantees the **batch input** is at most 10 images. It also
guarantees the review step is isolated: each batch is one fresh session, and that
session reads only its own batch. Therefore the largest set of image parts in any
request created by this workflow is the largest batch — never the sum of all
batches. `review.py check` fails if any batch or result exceeds 10.
