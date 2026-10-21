"""Build the static design preview and screen specifications.

Design-only. No production code or network access is used here.
"""
from __future__ import annotations

import csv
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from components import PATHS, SCREENS_DIR, SCREENSHOTS, SPECS, document  # noqa: E402

import screens_admin
import screens_clinical
import screens_core
import screens_inventory
import screens_ops

MODULES = [screens_core, screens_clinical, screens_inventory, screens_ops, screens_admin]
SCREENS = []
for module in MODULES:
    SCREENS.extend(module.SCREENS)

ROOT = TOOLS.parents[1]  # docs/UI_Design
PROTOTYPE = ROOT / "prototype"
DARK_IDS = {"DASH-001", "PAT-001", "SET-001"}
WIDE_IDS = {"AUTH-001", "DASH-001"}

FIELD_ORDER = [
    ("purpose", "Purpose"),
    ("users", "Users"),
    ("permissions", "Permissions"),
    ("entry", "Entry points"),
    ("navigation", "Navigation"),
    ("layout", "Layout regions"),
    ("components", "Components"),
    ("data", "Data shown"),
    ("actions", "Actions"),
    ("forms", "Forms and fields"),
    ("states", "States"),
    ("offline", "Offline and data behavior"),
    ("keyboard", "Keyboard"),
    ("a11y", "Accessibility"),
    ("deps", "Dependencies"),
    ("open", "Open questions / not approved"),
    ("notes", "Design notes and evidence boundary"),
]


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def md_list(value) -> str:
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value)
    return str(value)


def validate():
    errors = []
    ids = [s["id"] for s in SCREENS]
    for screen_id, count in Counter(ids).items():
        if count > 1:
            errors.append(f"Duplicate screen id: {screen_id}")
    expected = {
        "id", "name", "slug", "section", "feature", "source", "purpose", "users",
        "permissions", "entry", "navigation", "layout", "components", "data",
        "actions", "forms", "states", "offline", "keyboard", "a11y", "deps",
        "open", "notes", "html",
    }
    for screen in SCREENS:
        missing = expected - set(screen)
        if missing:
            errors.append(f"{screen.get('id')}: missing {sorted(missing)}")
        if screen["slug"] != slugify(screen["slug"]):
            errors.append(f"{screen['id']}: bad slug {screen['slug']}")
        for icon_name in re.findall(r"icon\(\"([^\"]+)\"", screen["html"]):
            if icon_name not in PATHS:
                errors.append(f"{screen['id']}: unknown icon {icon_name}")
    if len(SCREENS) < 60:
        errors.append(f"Expected at least 60 screens, found {len(SCREENS)}")
    if errors:
        raise SystemExit("BUILD VALIDATION FAILED\n" + "\n".join(errors))
    return Counter(ids)


def write_screen_html(screen):
    target = SCREENS_DIR / f"{screen['id']}.html"
    body = screen["html"]
    if body.lstrip().lower().startswith("<!doctype"):
        content = body
    else:
        content = document(f"{screen['id']} · {screen['name']}", body)
    target.write_text(content, encoding="utf-8")
    return target


def write_variant_html(screen, mode: str):
    source = SCREENS_DIR / f"{screen['id']}.html"
    content = source.read_text(encoding="utf-8")
    if mode == "dark":
        content = content.replace("<body>", '<body data-theme="dark">', 1)
        target = SCREENS_DIR / f"{screen['id']}-dark.html"
    elif mode == "wide":
        extra = '''<style>@page { size: 1920px 1080px; margin: 0; }
        .app { width: 1920px; height: 1080px; }
        .sidebar { height: 1080px; }
        .main { height: 1080px; }
        .workspace { height: 1024px; }
        .login-wrap, .splash { width: 1920px; height: 1080px; }
        .access-screen { height: 1080px; }
        .workspace { padding: 26px 32px; }
        </style>'''
        content = content.replace("</head>", extra + "\n</head>", 1)
        target = SCREENS_DIR / f"{screen['id']}-wide.html"
    else:
        raise ValueError(mode)
    target.write_text(content, encoding="utf-8")
    return target


def spec_markdown(screen, number, total):
    lines = []
    lines.append(f"# {screen['id']} · {screen['name']}")
    lines.append("")
    lines.append(f"> **Design specification {number} of {total}.** Desktop status: **Missing** in the repository; this is a design artifact, not an implemented screen.")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    lines.append(f"| Screen ID | `{screen['id']}` |")
    lines.append(f"| Section | {screen['section']} |")
    lines.append(f"| Feature | {screen['feature']} |")
    lines.append(f"| Source specification | `{screen['source']}` |")
    lines.append(f"| Prototype | [{screen['id']}.html](../prototype/screens/{screen['id']}.html) |")
    lines.append(f"| Rendered reference | [{screen['id']}.png](../screenshots/{screen['id']}.png) |")
    lines.append("| Review status | Draft for product/clinical/security review |")
    lines.append("")
    for key, label in FIELD_ORDER:
        value = screen[key]
        lines.append(f"## {label}")
        lines.append("")
        lines.append(md_list(value))
        lines.append("")
    lines.append("## Evidence boundary")
    lines.append("")
    lines.append("No desktop implementation exists for this screen. All names, identifiers, amounts, stock counts, dates and clinical text in the prototype are fictional design data. The screen must not be presented as shipped functionality.")
    lines.append("")
    lines.append("This specification does not approve unresolved workflow behavior. Items marked as open must be decided before implementation.")
    lines.append("")
    return "\n".join(lines)


def write_specs():
    SPECS.mkdir(parents=True, exist_ok=True)
    for idx, screen in enumerate(SCREENS, 1):
        name = f"{screen['id']}-{screen['slug']}.md"
        (SPECS / name).write_text(spec_markdown(screen, idx, len(SCREENS)), encoding="utf-8")

    grouped = []
    sections = []
    for screen in SCREENS:
        if screen["section"] not in sections:
            sections.append(screen["section"])
    for section in sections:
        items = [s for s in SCREENS if s["section"] == section]
        rows = "\n".join(
            f"| [`{s['id']}`](Screens/{s['id']}-{s['slug']}.md) | {s['name']} | {s['feature']} | [Prototype](prototype/screens/{s['id']}.html) | [PNG](screenshots/{s['id']}.png) |"
            for s in items
        )
        grouped.append(f"### {section}\n\n| ID | Screen | Feature | Prototype | Rendered |\n|---|---|---|---|---|\n{rows}\n")

    inventory = f"""# Screen Inventory

**{len(SCREENS)} screen specifications** across {len(sections)} sections. Every listed screen has a static HTML prototype and a rendered PNG reference at 1366×768.

> These screens are design proposals. The repository contains **no desktop implementation**; all 22 desktop feature modules are recorded as Missing. Names, IDs, amounts, stock and clinical text are fictional.

## Summary

| Section | Screens |
|---|---|
""" + "\n".join(f"| {section} | {len([s for s in SCREENS if s['section'] == section])} |" for section in sections) + "\n\n" + "\n".join(grouped)
    inventory += """
## Rendering and evidence

- Primary viewport: **1366×768** for all screens.
- Selected **1920×1080** wide variants: `AUTH-001`, `DASH-001`.
- Selected **dark theme** variants: `DASH-001`, `PAT-001`, `SET-001`.
- Screenshots are generated from the same HTML files by rendering to PDF with WeasyPrint and rasterizing with pypdfium2. They are not SVG illustrations.
- Dialog and drawer screenshots deliberately include their parent context behind a scrim.

## Scope boundary

The prototype covers authentication, shell, dashboard, patient administration, clinical records, inventory, wastage, borrow/return, reminders, finance, receipts, reports, staff, audit, sync, local data, backup/restore, updates and settings. It does **not** implement production behavior, connect to Supabase, prove Android parity, or replace the 138 desktop requirements in the Knowledge Base.
"""
    (ROOT / "Screen-Inventory.md").write_text(inventory, encoding="utf-8")


def gallery():
    sections = []
    for screen in SCREENS:
        if screen["section"] not in sections:
            sections.append(screen["section"])
    options = "".join(f'<option value="{html.escape(s)}">{html.escape(s)}</option>' for s in sections)
    cards = []
    for s in SCREENS:
        variants = []
        if s["id"] in DARK_IDS:
            variants.append(f'<a href="../screenshots/{s["id"]}-dark.png">Dark</a>')
        if s["id"] in WIDE_IDS:
            variants.append(f'<a href="../screenshots/{s["id"]}-wide.png">1920</a>')
        variant_html = f'<span class="variant-links">{" · ".join(variants)}</span>' if variants else ""
        cards.append(f'''<article class="g-card" data-section="{html.escape(s['section'])}" data-search="{html.escape((s['id'] + ' ' + s['name'] + ' ' + s['feature']).lower())}">
  <a class="shot" href="screens/{s['id']}.html"><img src="../screenshots/{s['id']}.png" alt="Rendered screen: {html.escape(s['name'])}" loading="lazy"></a>
  <div class="g-meta"><div><span class="g-id">{s['id']}</span><span class="g-section">{html.escape(s['section'])}</span><h2>{html.escape(s['name'])}</h2><p>{html.escape(s['feature'])}</p></div><div class="g-links"><a href="screens/{s['id']}.html">Open</a><a href="../Screens/{s['id']}-{s['slug']}.md">Spec</a>{variant_html}</div></div>
</article>''')
    body = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Neo Child Clinic Desktop · UI Design Gallery</title><link rel="stylesheet" href="assets/app.css"><style>
    body {{ background: #eef4f2; }}
    .g-head {{ background: #072e32; color: #fff; padding: 26px 34px 22px; }}
    .g-head .kicker {{ font-size: 10px; letter-spacing: 1.2px; text-transform: uppercase; color: #9ed0cc; font-weight: 700; }}
    .g-head h1 {{ font-family: var(--font-display); font-size: 30px; letter-spacing: -0.8px; margin-top: 4px; }}
    .g-head p {{ color: #b9d8d5; font-size: 12px; max-width: 860px; line-height: 1.55; margin-top: 7px; }}
    .g-toolbar {{ position: sticky; top: 0; z-index: 3; display: flex; gap: 10px; align-items: center; padding: 12px 34px; background: rgba(255,255,255,.94); border-bottom: 1px solid #d7e2e0; }}
    .g-toolbar input, .g-toolbar select {{ height: 34px; border: 1px solid #b5c6c3; border-radius: 7px; background: #fff; padding: 0 10px; font: inherit; font-size: 11px; }}
    .g-toolbar input {{ width: 320px; }}
    .g-count {{ color: #6b7d80; font-size: 11px; }}
    .g-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 16px; padding: 20px 34px 44px; }}
    .g-card {{ background: #fff; border: 1px solid #d7e2e0; border-radius: 10px; overflow: hidden; box-shadow: 0 1px 2px rgba(7,46,50,.06); }}
    .shot {{ display: block; background: #dce9e6; aspect-ratio: 1366/768; overflow: hidden; border-bottom: 1px solid #e7eeec; }}
    .shot img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .g-meta {{ padding: 10px 12px 11px; display: flex; gap: 10px; align-items: flex-start; }}
    .g-meta > div:first-child {{ min-width: 0; flex: 1; }}
    .g-id {{ font-family: var(--font-mono); font-size: 9.5px; color: #0f5d64; font-weight: 700; }}
    .g-section {{ font-size: 9px; color: #6b7d80; margin-left: 6px; text-transform: uppercase; letter-spacing: .4px; }}
    .g-meta h2 {{ font-family: var(--font-display); font-size: 13px; margin-top: 3px; }}
    .g-meta p {{ color: #6b7d80; font-size: 10px; margin-top: 2px; }}
    .g-links {{ display: flex; flex-wrap: wrap; gap: 5px; justify-content: flex-end; max-width: 95px; }}
    .g-links a, .variant-links {{ font-size: 9.5px; color: #0f5d64; font-weight: 700; text-decoration: none; background: #eef7f6; border-radius: 4px; padding: 3px 5px; }}
    .variant-links {{ text-align: right; }}
    .g-foot {{ padding: 0 34px 34px; color: #6b7d80; font-size: 10.5px; }}
    @media (max-width: 980px) {{ .g-grid {{ grid-template-columns: 1fr 1fr; }} }}
    @media (max-width: 640px) {{ .g-grid {{ grid-template-columns: 1fr; padding: 14px; }} }}
    </style></head><body>
    <header class="g-head"><div class="kicker">Design artifact · not production UI</div><h1>Neo Child Clinic · Desktop screen gallery</h1><p>{len(SCREENS)} screen specifications rendered at 1366×768 from the static prototype. This gallery is the visual index for review; all clinical and financial content is fictional. No production service is connected.</p></header>
    <div class="g-toolbar"><input id="g-search" type="search" placeholder="Filter by screen ID, name or feature…" aria-label="Filter screens"><select id="g-section" aria-label="Filter by section"><option value="">All sections</option>{options}</select><span class="g-count" id="g-count">{len(SCREENS)} screens</span></div>
    <main class="g-grid" id="g-grid">{''.join(cards)}</main>
    <div class="g-foot">Generated from <code>prototype/tools/build.py</code>. Screen specifications are in <code>Screens/</code>; screenshots are in <code>screenshots/</code>. Source requirements remain proposed in the Knowledge Base.</div>
    <script>
    const search = document.getElementById('g-search');
    const section = document.getElementById('g-section');
    const cards = [...document.querySelectorAll('.g-card')];
    const count = document.getElementById('g-count');
    function apply() {{
      const q = search.value.trim().toLowerCase(); const s = section.value;
      let n = 0;
      cards.forEach(c => {{ const ok = (!q || c.dataset.search.includes(q)) && (!s || c.dataset.section === s); c.style.display = ok ? '' : 'none'; if (ok) n++; }});
      count.textContent = n + ' screen' + (n === 1 ? '' : 's');
    }}
    search.addEventListener('input', apply); section.addEventListener('change', apply);
    </script></body></html>'''
    (PROTOTYPE / "index.html").write_text(body, encoding="utf-8")


def write_manifest():
    records = []
    for s in SCREENS:
        records.append({
            "id": s["id"], "name": s["name"], "section": s["section"], "feature": s["feature"],
            "html": f"prototype/screens/{s['id']}.html",
            "png": f"screenshots/{s['id']}.png",
            "dark": f"screenshots/{s['id']}-dark.png" if s["id"] in DARK_IDS else None,
            "wide": f"screenshots/{s['id']}-wide.png" if s["id"] in WIDE_IDS else None,
        })
    (SCREENSHOTS / "manifest.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    with (SCREENSHOTS / "manifest.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["id", "name", "section", "feature", "html", "png", "dark", "wide"])
        writer.writeheader()
        writer.writerows(records)


def main():
    validate()
    SCREENS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    for screen in SCREENS:
        write_screen_html(screen)
    for screen in SCREENS:
        if screen["id"] in DARK_IDS:
            write_variant_html(screen, "dark")
        if screen["id"] in WIDE_IDS:
            write_variant_html(screen, "wide")
    write_specs()
    gallery()
    write_manifest()
    print(f"Built {len(SCREENS)} screen HTML files, {len(SCREENS)} specs and the gallery.")
    print(f"Screens: {SCREENS_DIR}")
    print(f"Screenshots manifest: {SCREENSHOTS / 'manifest.json'}")


if __name__ == "__main__":
    main()
