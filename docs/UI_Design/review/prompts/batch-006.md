# Screenshot review — batch-006

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

- Batch JSON: `docs/UI_Design/review/batches/batch-006.json`
  (paths inside that JSON are relative to `docs/UI_Design/`)
- Result file to create: `docs/UI_Design/review/results/batch-006.json`

Images (read these exact paths):

- `docs/UI_Design/screenshots/RCP-003.png` — RCP-003 (base)
- `docs/UI_Design/screenshots/RPT-001.png` — RPT-001 (base)
- `docs/UI_Design/screenshots/RPT-002.png` — RPT-002 (base)
- `docs/UI_Design/screenshots/RPT-003.png` — RPT-003 (base)
- `docs/UI_Design/screenshots/RPT-004.png` — RPT-004 (base)
- `docs/UI_Design/screenshots/STF-001.png` — STF-001 (base)
- `docs/UI_Design/screenshots/STF-002.png` — STF-002 (base)
- `docs/UI_Design/screenshots/STF-003.png` — STF-003 (base)
- `docs/UI_Design/screenshots/STF-004.png` — STF-004 (base)
- `docs/UI_Design/screenshots/AUD-001.png` — AUD-001 (base)

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
  "batch_id": "batch-006",
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

Include every one of these screen IDs exactly once: RCP-003, RPT-001, RPT-002, RPT-003, RPT-004, STF-001, STF-002, STF-003, STF-004, AUD-001.

Keep each summary under 40 words. Do not include base64 or image data in the
result. Finish after writing the result file.
