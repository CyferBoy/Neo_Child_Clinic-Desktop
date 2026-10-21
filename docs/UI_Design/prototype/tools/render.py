"""Render the static prototype to exact-size PNG references.

Design-only. Uses the isolated WeasyPrint/pypdfium2 installation under the Termux
temporary directory; nothing is installed into the repository.

Re-running skips existing PNGs unless --force is passed. A per-page alarm keeps
one pathological layout from blocking the rest of the batch; failures are
reported and left missing so they can be fixed explicitly.
"""
from __future__ import annotations

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
FORCE = "--force" in sys.argv
FAILED = []
TIMEOUT = 90


class PageTimeout(Exception):
    pass


def _alarm(_signum, _frame):
    raise PageTimeout("render timed out")


def render(html_path: Path, png_path: Path, size=TARGET):
    if png_path.exists() and png_path.stat().st_size > 0 and not FORCE:
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


def main():
    SHOTS.mkdir(parents=True, exist_ok=True)
    rendered = []
    for index, item in enumerate(MANIFEST, 1):
        jobs = [(item["id"], SCREENS / f"{item['id']}.html", SHOTS / f"{item['id']}.png", TARGET, "light")]
        if item.get("dark"):
            jobs.append((item["id"] + "-dark", SCREENS / f"{item['id']}-dark.html", SHOTS / f"{item['id']}-dark.png", TARGET, "dark"))
        if item.get("wide"):
            jobs.append((item["id"] + "-wide", SCREENS / f"{item['id']}-wide.html", SHOTS / f"{item['id']}-wide.png", (1920, 1080), "wide"))
        for sid, html_path, png_path, size, kind in jobs:
            label = f"[{index:02d}/{len(MANIFEST)}] {sid:14s}"
            try:
                size_bytes = render(html_path, png_path, size)
                rendered.append((sid, size_bytes, kind))
                print(f"{label} {size_bytes/1024:.0f} KB", flush=True)
            except Exception as exc:  # noqa: BLE001 - report and continue the batch
                FAILED.append((sid, f"{type(exc).__name__}: {exc}"))
                print(f"{label} FAILED  {type(exc).__name__}: {exc}", flush=True)
    (SHOTS / "render-log.txt").write_text(
        "\n".join(f"{sid}\t{kind}\t{size} bytes" for sid, size, kind in rendered) + "\n",
        encoding="utf-8",
    )
    if FAILED:
        (SHOTS / "render-failures.txt").write_text(
            "\n".join(f"{sid}\t{reason}" for sid, reason in FAILED) + "\n", encoding="utf-8"
        )
        print(f"Rendered {len(rendered)}; failed {len(FAILED)}. See screenshots/render-failures.txt", flush=True)
    else:
        print(f"Rendered {len(rendered)} PNG files into {SHOTS}", flush=True)


if __name__ == "__main__":
    main()
