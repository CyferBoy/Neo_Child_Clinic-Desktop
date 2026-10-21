"""Validate the design package without touching production code.

Design-only checks:
  * 68 base screens, 68 specifications, 68 manifest entries
  * 73 rendered PNGs (68 base + 5 variants) at the exact target sizes
  * unique screen IDs and matching HTML/spec/PNG
  * local Markdown and prototype links resolve
  * no remote scripts, remote styles or absolute service URLs in the prototype

Run from anywhere:
    python prototype/tools/validate.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEPS = Path("/data/data/com.termux/files/usr/tmp/opencode/uideps")
sys.path.insert(0, str(DEPS))

try:
    from PIL import Image
except Exception as exc:  # noqa: BLE001
    raise SystemExit(f"Pillow is required for dimension checks: {exc}")

ERRORS: list[str] = []
WARNINGS: list[str] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def screen_id_from_spec(path: Path) -> str:
    """Return the complete screen ID, e.g. AUTH-001 from AUTH-001-sign-in.md."""
    match = re.match(r"^([A-Z]+-\d{3})-", path.name)
    return match.group(1) if match else path.stem


def link_targets(text: str):
    for match in re.finditer(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = match.group(1).strip()
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        yield target.split("#", 1)[0]


def check_markdown_links(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for target in link_targets(text):
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        check(resolved.exists(), f"broken link in {path.relative_to(ROOT)}: {target}")


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
    check(len(ids) == len(set(ids)), "manifest contains duplicate screen IDs")
    check(set(ids) == {p.stem for p in base_html}, "manifest IDs and base HTML pages differ")
    check(set(ids) == {screen_id_from_spec(p) for p in specs}, "manifest IDs and spec IDs differ")

    dark = [item["id"] for item in manifest if item.get("dark")]
    wide = [item["id"] for item in manifest if item.get("wide")]
    check(dark == ["DASH-001", "PAT-001", "SET-001"], f"unexpected dark variants: {dark}")
    check(wide == ["AUTH-001", "DASH-001"], f"unexpected wide variants: {wide}")

    expected_pngs = 68 + len(dark) + len(wide)
    pngs = sorted(shots_dir.glob("*.png"))
    check(len(pngs) == expected_pngs, f"expected {expected_pngs} PNGs, found {len(pngs)}")

    for item in manifest:
        sid = item["id"]
        html_path = screens_dir / f"{sid}.html"
        spec_glob = list(specs_dir.glob(f"{sid}-*.md"))
        png_path = shots_dir / f"{sid}.png"
        check(html_path.exists(), f"missing HTML for {sid}")
        check(len(spec_glob) == 1, f"expected one spec for {sid}, found {len(spec_glob)}")
        check(png_path.exists() and png_path.stat().st_size > 0, f"missing/empty PNG for {sid}")
        if item.get("dark"):
            check((screens_dir / f"{sid}-dark.html").exists(), f"missing dark HTML for {sid}")
            check((shots_dir / f"{sid}-dark.png").exists(), f"missing dark PNG for {sid}")
        if item.get("wide"):
            check((screens_dir / f"{sid}-wide.html").exists(), f"missing wide HTML for {sid}")
            check((shots_dir / f"{sid}-wide.png").exists(), f"missing wide PNG for {sid}")

    def check_png(path: Path, size: tuple[int, int]) -> None:
        try:
            with Image.open(path) as image:
                check(image.size == size, f"{path.name}: expected {size}, got {image.size}")
        except Exception as exc:  # noqa: BLE001
            ERRORS.append(f"{path.name}: cannot read PNG: {exc}")

    for item in manifest:
        check_png(shots_dir / f"{item['id']}.png", (1366, 768))
        if item.get("dark"):
            check_png(shots_dir / f"{item['id']}-dark.png", (1366, 768))
        if item.get("wide"):
            check_png(shots_dir / f"{item['id']}-wide.png", (1920, 1080))

    # Markdown links across the package.
    for path in [ROOT / "README.md", ROOT / "Screen-Inventory.md", ROOT / "Design-Traceability.md"]:
        if path.exists():
            check_markdown_links(path)
    for path in specs:
        check_markdown_links(path)
    for path in [ROOT / "Design-System.md", ROOT / "Navigation-and-Workflows.md", ROOT / "Component-Catalog.md",
                 ROOT / "States-and-Errors.md", ROOT / "Accessibility.md", ROOT / "Implementation-Backlog.md",
                 ROOT / "Repository-and-Requirements-Audit.md"]:
        if path.exists():
            check_markdown_links(path)

    # Prototype must be local-only: no remote scripts/styles and no service URLs.
    for path in html:
        text = path.read_text(encoding="utf-8")
        check("<script src=\"http" not in text and "<script src='http" not in text, f"remote script in {path.name}")
        check("<link rel=\"stylesheet\" href=\"http" not in text and "<link rel='stylesheet' href='http" not in text, f"remote stylesheet in {path.name}")
        check("supabase.co" not in text.lower(), f"service URL in {path.name}")
        check("service_role" not in text.lower(), f"service-role marker in {path.name}")
        check("eyJ" not in text, f"JWT-like marker in {path.name}")

    # Inventory links are checked explicitly because this file is generated.
    inventory = (ROOT / "Screen-Inventory.md").read_text(encoding="utf-8")
    for sid in ids:
        check(f"`{sid}`" in inventory, f"inventory missing {sid}")

    print(f"Screens: {len(base_html)}")
    print(f"Specs: {len(specs)}")
    print(f"Manifest entries: {len(manifest)}")
    print(f"PNGs: {len(pngs)} (base {len(manifest)}, dark {len(dark)}, wide {len(wide)})")
    if WARNINGS:
        print("Warnings:")
        for warning in WARNINGS:
            print(f"  - {warning}")
    if ERRORS:
        print(f"FAIL: {len(ERRORS)} issue(s)")
        for error in ERRORS[:100]:
            print(f"  - {error}")
        return 1
    print("PASS: counts, dimensions, IDs and local links are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
