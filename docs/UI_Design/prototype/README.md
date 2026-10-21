# Prototype Preview

This directory contains the static HTML preview of the Neo Child Clinic Desktop
design package. It has no build step, no package install and no backend
connection. All fonts, styles, scripts, screen links and screenshots are local.

## Recommended preview: local HTTP server

From the repository root:

```bash
cd /storage/emulated/0/Neo_Child_Clinic_Desktop
python3 -m http.server 8000 --directory docs/UI_Design
```

Keep that terminal running, then open:

- **Gallery:** <http://localhost:8000/prototype/index.html>
- **Individual screen:** <http://localhost:8000/prototype/screens/AUTH-001.html>
- **Any other screen:** replace `AUTH-001` with an ID from the gallery or
  [`Screen-Inventory.md`](../Screen-Inventory.md), for example
  <http://localhost:8000/prototype/screens/PAT-001.html>.

On Termux/Android, this optional command opens the gallery in the device browser:

```bash
termux-open-url http://localhost:8000/prototype/index.html
```

The server must be rooted at `docs/UI_Design/` as shown above. Starting it from
inside `prototype/` will break the gallery's `../screenshots/` and `../Screens/`
links. Stop the server with `Ctrl+C`.

If port 8000 is already in use, choose another port:

```bash
python3 -m http.server 8001 --directory docs/UI_Design
```

Then use `http://localhost:8001/prototype/index.html`.

## Direct file preview

You can also open the gallery without a server:

```text
file:///storage/emulated/0/Neo_Child_Clinic_Desktop/docs/UI_Design/prototype/index.html
```

From a different checkout, open `docs/UI_Design/prototype/index.html` directly.
Desktop convenience commands from the repository root:

| Platform | Command |
|---|---|
| Linux | `xdg-open docs/UI_Design/prototype/index.html` |
| macOS | `open docs/UI_Design/prototype/index.html` |
| Windows | `start docs\UI_Design\prototype\index.html` |

The HTTP server is recommended because some browsers restrict local-file
behaviour. No page requires a server for its content, but the server gives the
most predictable result.

## Relative path contract

The delivered links assume this structure:

```text
docs/UI_Design/
├── prototype/
│   ├── index.html                 # gallery
│   ├── assets/
│   │   ├── app.css
│   │   ├── prototype.js
│   │   └── fonts/{Figtree.ttf,NotoSans.ttf}
│   └── screens/
│       ├── AUTH-001.html
│       └── ...
├── screenshots/                   # 73 PNG references
└── Screens/                       # 68 Markdown specifications
```

- `prototype/index.html` links to `screens/<ID>.html`, `assets/app.css`,
  `../screenshots/<ID>.png` and `../Screens/<ID>-<slug>.md`.
- Each `prototype/screens/<ID>.html` page loads `../assets/app.css` and
  `../assets/prototype.js`; its navigation links use sibling `<ID>.html` files.
- Do not move an individual screen HTML file out of `prototype/screens/`.
  Moving it breaks the stylesheet, script, font and screenshot/spec links.

## What to inspect

1. The gallery should show **68** screen cards.
2. Use the search field and section selector to filter cards.
3. Select **Open** on a card to inspect the standalone screen at 1366×768.
4. Use **Spec** to open the matching screen specification and **Dark** or
   **1920** where a reference variant exists.
5. Screen navigation in the sidebar is static; links resolve to sibling HTML
   pages. No form submits, no service is called and all patient data is fictional.

The rendered PNG references are in [`../screenshots/`](../screenshots/). The
visual review results are in [`../Screenshot-Review.md`](../Screenshot-Review.md).

## Validation

From the repository root:

```bash
python3 docs/UI_Design/prototype/tools/validate.py
```

The command checks screen/specification/HTML/PNG counts, complete screen IDs,
image dimensions and readability, local Markdown/HTML/CSS references, required
assets and the absence of remote scripts or service URLs. A passing run ends
with `PASS: counts, IDs, dimensions, images, links and assets are consistent.`
