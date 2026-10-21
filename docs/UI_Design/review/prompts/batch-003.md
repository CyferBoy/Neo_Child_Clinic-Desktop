# Screenshot review — batch-003

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

- Batch JSON: `docs/UI_Design/review/batches/batch-003.json`
  (paths inside that JSON are relative to `docs/UI_Design/`)
- Result file to create: `docs/UI_Design/review/results/batch-003.json`

Images (read these exact paths):

- `docs/UI_Design/screenshots/VAC-003.png` — VAC-003 (base)
- `docs/UI_Design/screenshots/VAC-004.png` — VAC-004 (base)
- `docs/UI_Design/screenshots/VAC-005.png` — VAC-005 (base)
- `docs/UI_Design/screenshots/CON-001.png` — CON-001 (base)
- `docs/UI_Design/screenshots/CON-002.png` — CON-002 (base)
- `docs/UI_Design/screenshots/CON-003.png` — CON-003 (base)
- `docs/UI_Design/screenshots/CON-004.png` — CON-004 (base)
- `docs/UI_Design/screenshots/INV-001.png` — INV-001 (base)
- `docs/UI_Design/screenshots/INV-002.png` — INV-002 (base)
- `docs/UI_Design/screenshots/INV-003.png` — INV-003 (base)

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
  "batch_id": "batch-003",
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

Include every one of these screen IDs exactly once: VAC-003, VAC-004, VAC-005, CON-001, CON-002, CON-003, CON-004, INV-001, INV-002, INV-003.

Keep each summary under 40 words. Do not include base64 or image data in the
result. Finish after writing the result file.
