# Screenshot review — batch-002

Review the rendered Neo Child Clinic Desktop screenshots in this batch.
This is a design-package review only. Do not edit mockups, HTML, specs or
production code.

## Hard request limits

- This batch contains exactly **10 images** (limit 10).
- Read every assigned image in **one assistant turn** using parallel `read`
  calls. Do not read any other image before or after that turn.
- Do not open a different batch. Do not paste images into your reply. The
  batch JSON contains paths only; it contains no image data.
- Use a fresh session for this batch. Never review a second batch in the
  same conversation, because earlier images remain attached to later requests.

## Inputs

All paths below are relative to the repository root.

- Batch JSON: `docs/UI_Design/review/batches/batch-002.json`
  (paths inside that JSON are relative to `docs/UI_Design/`)
- Result file to create: `docs/UI_Design/review/results/batch-002.json`

Images (read these exact paths):

- `docs/UI_Design/screenshots/PAT-001.png` — PAT-001 (base)
- `docs/UI_Design/screenshots/PAT-001-dark.png` — PAT-001 (dark)
- `docs/UI_Design/screenshots/PAT-002.png` — PAT-002 (base)
- `docs/UI_Design/screenshots/PAT-003.png` — PAT-003 (base)
- `docs/UI_Design/screenshots/PAT-004.png` — PAT-004 (base)
- `docs/UI_Design/screenshots/PAT-005.png` — PAT-005 (base)
- `docs/UI_Design/screenshots/PAT-006.png` — PAT-006 (base)
- `docs/UI_Design/screenshots/PAT-007.png` — PAT-007 (base)
- `docs/UI_Design/screenshots/VAC-001.png` — VAC-001 (base)
- `docs/UI_Design/screenshots/VAC-002.png` — VAC-002 (base)

Automated checks already passed for every path above: the file exists,
is readable, is not blank, and has the expected dimensions. If you cannot
read an image, record that as a `fail` issue instead of guessing.

## Review criteria

For each screen, check:

1. The image is a complete viewport, not cropped, blank or a browser error.
2. No overlapping, clipped or off-screen text, controls or table columns.
3. Typography is legible at 1366×768 (or the stated wide size).
4. The shell, navigation, spacing, colours and component variants are
   consistent with the design package.
5. Tables, forms, dialogs and empty/error states look purposeful and do not
   show `undefined`, `NaN`, raw template markers or obviously broken data.
6. Any visible patient data is fictional; no real personal or clinical data.

Use `pass` when the screen is fit for design review. Use
`pass_with_notes` for cosmetic or non-blocking issues. Use `fail` for a
blocking visual defect (unreadable content, missing core region, severe
clipping, or an image that is not the intended screen).

## Required output

Write valid JSON only to the result path. Do not wrap it in Markdown fences.
Use this shape:

```json
{
  "batch_id": "batch-002",
  "images_reviewed": 10,
  "reviewed_at": "ISO-8601 timestamp",
  "notes": "one or two sentences about the batch as a whole",
  "screens": [
    {
      "screen_id": "AUTH-001",
      "verdict": "pass",
      "summary": "Concise finding for this screen.",
      "issues": [
        {"image": "screenshots/AUTH-001.png", "severity": "minor", "observation": "..."}
      ]
    }
  ]
}
```

Include every one of these screen IDs exactly once: PAT-001, PAT-002, PAT-003, PAT-004, PAT-005, PAT-006, PAT-007, VAC-001, VAC-002.

Keep each summary under 40 words. Do not include base64 or image data in the
result. Finish after writing the result file.
