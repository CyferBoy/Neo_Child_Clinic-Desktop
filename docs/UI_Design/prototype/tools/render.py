"""Render the static prototype to exact-size PNG references.

Design-only. Uses the isolated WeasyPrint/pypdfium2 installation under the Termux
temporary directory; nothing is installed into the repository.

Re-running skips existing PNGs unless --force is passed. Pass one or more screen
IDs to render only those screens, for example:

    python prototype/tools/render.py --force REM-003 RCP-002 RPT-002 SYS-002

A per-page alarm keeps one pathological layout from blocking the rest of the
batch. The render log is rebuilt from the PNG files that actually exist, and the
failure log only contains screens that failed in this run or remain unrendered.
"""
from __future__ import annotations

import argparse
import json
import signal
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
UI = TOOLS.parents[1]
DEPS = Path("/data/data/com.termux/files/usr/tmp/opencode/uideps")
sys.path.insert(0, str(DEPS))
sys.path.insert(0, str(TOOLS))

import pypdfium2 as pdfium  # noqa: E402
from weasyprint import HTML  # noqa: E402

SCREENS = UI / "prototype" / "screens"
SHOTS = UI / "screenshots"
MANIFEST = json.loads((SHOTS / "manifest.json").read_text(encoding="utf-8"))
TARGET = (1366, 768)
FAILED: list[tuple[str, str]] = []
TIMEOUT = 90


class PageTimeout(Exception):
    pass


def _alarm(_signum, _frame):
    raise PageTimeout("render timed out")


def render(html_path: Path, png_path: Path, size=TARGET, force: bool = False):
    if png_path.exists() and png_path.stat().st_size > 0 and not force:
        return png_path.stat().st_size
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(TIMEOUT)
    try:
        pdf_bytes = HTML(filename=str(html_path)).write_pdf()
    finally:
        signal.alarm(0)
    doc = pdfium.PdfDocument(pdf_bytes)
    if len(doc) != 1:
        raise RuntimeError(f"rendered {len(doc)} PDF pages, expected 1")
    page = doc[0]
    width, height = page.get_size()
    scale_x = size[0] / width
    scale_y = size[1] / height
    if abs(scale_x - scale_y) > 0.002:
        raise RuntimeError(f"unexpected page aspect {width}x{height}")
    bitmap = page.render(scale=scale_x, fill_color=(255, 255, 255, 255))
    image = bitmap.to_pil().resize(size)
    image.save(png_path, "PNG", optimize=True)
    doc.close()
    return png_path.stat().st_size


def jobs_for(item: dict):
    jobs = [
        (item["id"], SCREENS / f"{item['id']}.html", SHOTS / f"{item['id']}.png", TARGET, "light"),
    ]
    if item.get("dark"):
        jobs.append(
            (
                item["id"] + "-dark",
                SCREENS / f"{item['id']}-dark.html",
                SHOTS / f"{item['id']}-dark.png",
                TARGET,
                "dark",
            )
        )
    if item.get("wide"):
        jobs.append(
            (
                item["id"] + "-wide",
                SCREENS / f"{item['id']}-wide.html",
                SHOTS / f"{item['id']}-wide.png",
                (1920, 1080),
                "wide",
            )
        )
    return jobs


def selected_manifest(ids: list[str]):
    if not ids:
        return MANIFEST
    known = {item["id"] for item in MANIFEST}
    unknown = sorted(set(ids) - known)
    if unknown:
        raise SystemExit(f"Unknown screen ID(s): {', '.join(unknown)}")
    requested = set(ids)
    return [item for item in MANIFEST if item["id"] in requested]


def write_render_log() -> None:
    """Reconcile the log with the PNG files that actually exist."""
    entries = []
    for item in MANIFEST:
        for sid, _html, png, _size, kind in jobs_for(item):
            if png.is_file() and png.stat().st_size > 0:
                entries.append(f"{sid}\t{kind}\t{png.stat().st_size} bytes")
    (SHOTS / "render-log.txt").write_text(
        "\n".join(entries) + ("\n" if entries else ""), encoding="utf-8"
    )


def write_failures(attempted: set[str]) -> None:
    """Keep unresolved failures for other screens, but clear IDs just rendered."""
    failure_path = SHOTS / "render-failures.txt"
    existing: dict[str, str] = {}
    if failure_path.is_file():
        for line in failure_path.read_text(encoding="utf-8").splitlines():
            if "\t" in line:
                sid, reason = line.split("\t", 1)
                existing[sid] = reason
    remaining = {sid: reason for sid, reason in existing.items() if sid not in attempted}
    remaining.update(dict(FAILED))
    if remaining:
        failure_path.write_text(
            "\n".join(f"{sid}\t{reason}" for sid, reason in remaining.items()) + "\n",
            encoding="utf-8",
        )
    elif failure_path.exists():
        failure_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*", metavar="SCREEN_ID", help="render only these base screen IDs")
    parser.add_argument("--force", action="store_true", help="re-render even when a PNG already exists")
    args = parser.parse_args()

    SHOTS.mkdir(parents=True, exist_ok=True)
    items = selected_manifest(args.ids)
    attempted: set[str] = set()
    for index, item in enumerate(items, 1):
        for sid, html_path, png_path, size, kind in jobs_for(item):
            attempted.add(sid)
            label = f"[{index:02d}/{len(items)}] {sid:14s}"
            try:
                size_bytes = render(html_path, png_path, size, force=args.force)
                print(f"{label} {size_bytes/1024:.0f} KB", flush=True)
            except Exception as exc:  # noqa: BLE001 - report and continue the batch
                FAILED.append((sid, f"{type(exc).__name__}: {exc}"))
                print(f"{label} FAILED  {type(exc).__name__}: {exc}", flush=True)

    write_render_log()
    write_failures(attempted)
    if FAILED:
        print(
            f"Rendered {len(attempted) - len(FAILED)}; failed {len(FAILED)}. "
            "See screenshots/render-failures.txt",
            flush=True,
        )
        return 1
    print(f"Rendered {len(attempted)} PNG file(s) into {SHOTS}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
