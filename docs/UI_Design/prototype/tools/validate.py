"""Validate the design package without touching production code.

Design-only checks:
  * 68 base screens, 68 specifications, 68 manifest entries, 73 PNGs
  * complete screen IDs and matching HTML/spec/manifest/PNG names
  * exact dimensions, readability and non-blank content for every PNG
  * local Markdown, HTML, CSS and prototype-asset references
  * inventory, gallery and README counts against verified artifacts
  * no remote scripts, remote styles or absolute service URLs in the prototype

Run from anywhere:
    python prototype/tools/validate.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[2]
DEPS = Path("/data/data/com.termux/files/usr/tmp/opencode/uideps")
sys.path.insert(0, str(DEPS))

try:
    from PIL import Image, ImageStat
except Exception as exc:  # noqa: BLE001
    raise SystemExit(f"Pillow is required for image checks: {exc}")

ERRORS: list[str] = []
WARNINGS: list[str] = []
EXTERNAL_PREFIXES = (
    "http://",
    "https://",
    "//",
    "mailto:",
    "tel:",
    "data:",
    "javascript:",
    "#",
)


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def screen_id_from_spec(path: Path) -> str:
    """Return the complete screen ID, e.g. AUTH-001 from AUTH-001-sign-in.md."""
    match = re.match(r"^([A-Z]+-\d{3})-", path.name)
    return match.group(1) if match else path.stem


def markdown_link_targets(text: str):
    for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if target.startswith(EXTERNAL_PREFIXES):
            continue
        yield target.split("#", 1)[0]


def check_markdown_links(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for target in markdown_link_targets(text):
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        check(resolved.exists(), f"broken link in {rel(path)}: {target}")


def check_reference(base_file: Path, target: str) -> None:
    if target.startswith(EXTERNAL_PREFIXES):
        return
    clean = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not clean:
        return
    if clean.startswith("/"):
        resolved = (ROOT / clean.lstrip("/")).resolve()
    else:
        resolved = (base_file.parent / clean).resolve()
    check(resolved.exists(), f"broken local reference in {rel(base_file)}: {target}")


def check_html_references(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", text, re.I):
        check_reference(path, match.group(1))


def check_css_references(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r"""url\(\s*["']?([^"')]+)["']?\s*\)""", text, re.I):
        check_reference(path, match.group(1).strip())


def check_png(path: Path, expected: tuple[int, int]) -> None:
    if not path.is_file():
        return
    if path.stat().st_size < 1024:
        ERRORS.append(f"{path.name}: file is too small to be a screenshot")
        return
    try:
        with Image.open(path) as image:
            check(image.format == "PNG", f"{path.name}: expected PNG, got {image.format}")
            check(image.size == expected, f"{path.name}: expected {expected}, got {image.size}")
            check(max(ImageStat.Stat(image.convert("RGB")).stddev) >= 0.5, f"{path.name}: image appears blank")
    except Exception as exc:  # noqa: BLE001
        ERRORS.append(f"{path.name}: cannot read PNG: {exc}")


def check_page_text(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    body = re.search(r"<body\b[^>]*>(.*?)</body>", text, re.S | re.I)
    if not body:
        ERRORS.append(f"{path.name}: no body element")
        return
    plain = re.sub(r"<(script|style)\b.*?</\1>", " ", body.group(1), flags=re.S | re.I)
    plain = re.sub(r"<[^>]+>", " ", plain)
    words = re.findall(r"[A-Za-z0-9]{2,}", plain)
    check(len(words) >= 20, f"{path.name}: page body has too little text (possible blank page)")
    check(re.search(r"<title>[^<]+</title>", text, re.I) is not None, f"{path.name}: missing page title")


def main() -> int:
    screens_dir = ROOT / "prototype" / "screens"
    specs_dir = ROOT / "Screens"
    shots_dir = ROOT / "screenshots"
    manifest_path = shots_dir / "manifest.json"

    html = sorted(screens_dir.glob("*.html"))
    base_html = [p for p in html if not p.stem.endswith(("-dark", "-wide"))]
    specs = sorted(specs_dir.glob("*.md"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    check(len(base_html) == 68, f"expected 68 base HTML pages, found {len(base_html)}")
    check(len(specs) == 68, f"expected 68 specs, found {len(specs)}")
    check(len(manifest) == 68, f"expected 68 manifest entries, found {len(manifest)}")

    ids = [item["id"] for item in manifest]
    items = {item["id"]: item for item in manifest}
    check(len(ids) == len(set(ids)), "manifest contains duplicate screen IDs")
    check(set(ids) == {p.stem for p in base_html}, "manifest IDs and base HTML pages differ")

    spec_ids = []
    for path in specs:
        match = re.match(r"^([A-Z]+-\d{3})-", path.name)
        check(match is not None, f"spec filename does not start with a complete screen ID: {path.name}")
        if match:
            spec_ids.append(match.group(1))
    check(len(spec_ids) == len(set(spec_ids)), "duplicate screen IDs in specification filenames")
    check(set(ids) == set(spec_ids), "manifest IDs and spec IDs differ")
    check(set(ids) == {screen_id_from_spec(p) for p in specs}, "spec ID extraction is incomplete")

    dark = [item["id"] for item in manifest if item.get("dark")]
    wide = [item["id"] for item in manifest if item.get("wide")]
    check(dark == ["DASH-001", "PAT-001", "SET-001"], f"unexpected dark variants: {dark}")
    check(wide == ["AUTH-001", "DASH-001"], f"unexpected wide variants: {wide}")

    expected_html = set()
    expected_pngs = {}
    expected_artifacts = {}
    for item in manifest:
        sid = item["id"]
        base_html_rel = f"prototype/screens/{sid}.html"
        base_png_rel = f"screenshots/{sid}.png"
        expected_html.add(base_html_rel)
        expected_pngs[base_png_rel] = (sid, (1366, 768))
        expected_artifacts[sid] = ("light", ROOT / base_png_rel)
        check(item.get("html") == base_html_rel, f"{sid}: manifest html path is not {base_html_rel}")
        check(item.get("png") == base_png_rel, f"{sid}: manifest png path is not {base_png_rel}")
        if item.get("dark"):
            expected_html.add(f"prototype/screens/{sid}-dark.html")
            expected_pngs[f"screenshots/{sid}-dark.png"] = (sid, (1366, 768))
            expected_artifacts[sid + "-dark"] = ("dark", ROOT / f"screenshots/{sid}-dark.png")
            check(item["dark"] == f"screenshots/{sid}-dark.png", f"{sid}: unexpected dark path")
        if item.get("wide"):
            expected_html.add(f"prototype/screens/{sid}-wide.html")
            expected_pngs[f"screenshots/{sid}-wide.png"] = (sid, (1920, 1080))
            expected_artifacts[sid + "-wide"] = ("wide", ROOT / f"screenshots/{sid}-wide.png")
            check(item["wide"] == f"screenshots/{sid}-wide.png", f"{sid}: unexpected wide path")

    actual_html = {rel(path) for path in html}
    check(actual_html == expected_html, "prototype HTML files do not match the manifest variants")
    check(
        len(actual_html) == 68 + len(dark) + len(wide),
        f"expected {68 + len(dark) + len(wide)} HTML files, found {len(actual_html)}",
    )

    pngs = sorted(shots_dir.glob("*.png"))
    actual_pngs = {rel(path) for path in pngs}
    check(len(pngs) == 73, f"expected 73 PNGs, found {len(pngs)}")
    check(actual_pngs == set(expected_pngs), "PNG files do not match the manifest paths")
    for relative, (_sid, size) in expected_pngs.items():
        check((ROOT / relative).is_file(), f"missing PNG: {relative}")
        check_png(ROOT / relative, size)

    # Render log must describe the PNG files that actually exist.
    render_log_path = shots_dir / "render-log.txt"
    check(render_log_path.is_file(), "render-log.txt is missing")
    if render_log_path.is_file():
        render_log = render_log_path.read_text(encoding="utf-8").splitlines()
        check(len(render_log) == 73, f"render-log.txt has {len(render_log)} entries, expected 73")
        logged = {}
        for line in render_log:
            parts = line.split("\t")
            check(len(parts) == 3, f"malformed render-log entry: {line}")
            if len(parts) != 3:
                continue
            sid, kind, size_text = parts
            match = re.fullmatch(r"(\d+) bytes", size_text)
            check(match is not None, f"malformed render-log size: {line}")
            if match:
                logged[sid] = (kind, int(match.group(1)))
        check(set(logged) == set(expected_artifacts), "render-log IDs do not match the manifest variants")
        for sid, (kind, size) in logged.items():
            expected = expected_artifacts.get(sid)
            if expected:
                check(kind == expected[0], f"render-log kind differs for {sid}")
                check(size == expected[1].stat().st_size, f"render-log byte count differs for {sid}")
    check(
        not (shots_dir / "render-failures.txt").exists(),
        "stale render-failures.txt exists although every screenshot renders",
    )

    # Screen inventory must map every ID to the matching spec, HTML and PNG.
    inventory = (ROOT / "Screen-Inventory.md").read_text(encoding="utf-8")
    row_pattern = re.compile(
        r"^\| \[`([A-Z]+-\d{3})`\]\((Screens/[^)]+)\) "
        r"\|[^\n]*?\[Prototype\]\((prototype/screens/[^)]+)\) "
        r"\| \[PNG\]\((screenshots/[^)]+)\) \|$",
        re.M,
    )
    rows = row_pattern.findall(inventory)
    check(len(rows) == 68, f"expected 68 inventory rows, found {len(rows)}")
    seen_inventory = []
    for sid, spec, html_path, png_path in rows:
        seen_inventory.append(sid)
        item = items.get(sid)
        check(item is not None, f"inventory contains unknown screen ID: {sid}")
        if item:
            check(html_path == item["html"], f"inventory HTML link differs for {sid}")
            check(png_path == item["png"], f"inventory PNG link differs for {sid}")
        matches = sorted(specs_dir.glob(f"{sid}-*.md"))
        expected_spec = f"Screens/{matches[0].name}" if len(matches) == 1 else None
        check(spec == expected_spec, f"inventory spec link differs for {sid}")
    check(len(seen_inventory) == len(set(seen_inventory)), "inventory repeats a screen ID")
    check(set(seen_inventory) == set(ids), "inventory screen IDs do not match the manifest")

    # Gallery counts and links.
    gallery_path = ROOT / "prototype" / "index.html"
    gallery = gallery_path.read_text(encoding="utf-8")
    check(len(re.findall(r'<article class="g-card"', gallery)) == 68, "gallery does not contain 68 cards")
    gallery_shots = set(
        re.findall(
            r'<a class="shot" href="screens/([A-Z]+-\d{3})\.html"><img src="\.\./screenshots/\1\.png"',
            gallery,
        )
    )
    check(gallery_shots == set(ids), "gallery screen/image links do not cover every screen")
    check(f'id="g-count">{len(ids)} screens<' in gallery, "gallery count label is not 68 screens")
    check_html_references(gallery_path)
    check_page_text(gallery_path)

    # Root README counts must match verified artifacts.
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_counts = {
        "Screen specifications": 68,
        "Standalone HTML prototype": 68,
        "Rendered PNG references": 73,
        "Screen inventory": 68,
    }
    for label, expected in readme_counts.items():
        match = re.search(
            rf"\| {re.escape(label)} \| \[[^\]]+\]\([^)]+\) \| (\d+)(?: pages| rows)? \|",
            readme,
        )
        check(match is not None, f"README count row is missing: {label}")
        if match:
            check(int(match.group(1)) == expected, f"README count for {label} is {match.group(1)}, expected {expected}")
    check("prototype/README.md" in readme, "README does not link the prototype preview guide")

    # Local links across Markdown, HTML and CSS.
    for path in sorted(ROOT.rglob("*.md")):
        check_markdown_links(path)
    for path in html:
        check_html_references(path)
    for path in sorted((ROOT / "prototype").rglob("*.css")):
        check_css_references(path)

    required_assets = [
        "prototype/index.html",
        "prototype/README.md",
        "prototype/assets/app.css",
        "prototype/assets/prototype.js",
        "prototype/assets/fonts/Figtree.ttf",
        "prototype/assets/fonts/NotoSans.ttf",
        "Validation.md",
    ]
    for relative in required_assets:
        path = ROOT / relative
        check(path.is_file() and path.stat().st_size > 0, f"required asset is missing or empty: {relative}")

    for path in html:
        text = path.read_text(encoding="utf-8")
        check("<script src=\"http" not in text and "<script src='http" not in text, f"remote script in {path.name}")
        check(
            "<link rel=\"stylesheet\" href=\"http" not in text
            and "<link rel='stylesheet' href='http" not in text,
            f"remote stylesheet in {path.name}",
        )
        check("supabase.co" not in text.lower(), f"service URL in {path.name}")
        check("service_role" not in text.lower(), f"service-role marker in {path.name}")
        check("eyJ" not in text, f"JWT-like marker in {path.name}")
        check("../assets/app.css" in text or "assets/app.css" in text, f"stylesheet link missing in {path.name}")
        if path.parent.name == "screens":
            check("../assets/prototype.js" in text, f"prototype script link missing in {path.name}")
        check_page_text(path)

    check("assets/app.css" in gallery, "gallery stylesheet link is missing")

    # Task-scoped hygiene: no generated Python caches and no empty workflow directory.
    caches = [path for path in ROOT.rglob("__pycache__") if path.is_dir()]
    check(not caches, f"generated Python cache directory present: {rel(caches[0]) if caches else ''}")
    pyc = list(ROOT.rglob("*.pyc"))
    check(not pyc, f"generated .pyc file present: {rel(pyc[0]) if pyc else ''}")
    workflows = ROOT / "workflows"
    check(not workflows.is_dir() or any(workflows.iterdir()), "empty workflows/ directory still exists")

    print(f"Screens: {len(base_html)}")
    print(f"Specs: {len(specs)}")
    print(f"Manifest entries: {len(manifest)}")
    print(f"PNGs: {len(pngs)} (base {len(manifest)}, dark {len(dark)}, wide {len(wide)})")
    print(f"Gallery cards: {len(re.findall(r'<article class=\"g-card\"', gallery))}")
    if WARNINGS:
        print("Warnings:")
        for warning in WARNINGS:
            print(f"  - {warning}")
    if ERRORS:
        print(f"FAIL: {len(ERRORS)} issue(s)")
        for error in ERRORS[:100]:
            print(f"  - {error}")
        return 1
    print("PASS: counts, IDs, dimensions, images, links and assets are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
