#!/usr/bin/env python3
"""Post-process Archify HTML for fully offline, self-contained delivery.

Two edits are applied to every rendered Archify artifact:

1. Remove the Google Fonts <link>/<style> elements. The Archify template
   preconnects to fonts.googleapis.com / fonts.gstatic.com. The diagram still
   renders offline because the CSS font stack falls through to ui-monospace and
   the platform monospace faces, and the SVG export path already uses
   local()-only @font-face declarations. Removing the links satisfies the
   "no external CDN" requirement for the generated suite.

2. Inject a fixed-position "Diagram index" link and a provenance banner so the
   suite is navigable and every artifact states its evidence class on its face.

Usage:  strip_cdn.py <file.html> [more.html ...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# External font-hosting references that must not ship in the offline suite.
FONT_LINK_RE = re.compile(
    r'^\s*<link[^>]*href="https://fonts\.(?:googleapis|gstatic)\.com[^>]*>\s*$',
    re.M,
)
PRECONNECT_RE = re.compile(
    r'^\s*<link[^>]*rel="preconnect"[^>]*>\s*$',
    re.M,
)

# Archify embeds "start here" navigation anchors to its hosted docs. They are not
# resource loads (the page renders fully offline), but the suite must carry no
# external references at all, so they are neutralized to in-page anchors.
EXTERNAL_LINK_RE = re.compile(
    r'(href=")https://tt-a1i\.github\.io/archify/[^"]*(")'
)

NAV_CSS = """
/* --- injected by tools/strip_cdn.py: offline navigation + provenance --- */
.ncc-backlink{position:fixed;left:14px;top:14px;z-index:9999;font:600 12px/1 ui-monospace,
SFMono-Regular,Menlo,Consolas,monospace;padding:8px 12px;border-radius:8px;text-decoration:none;
background:var(--surface-2,#1b2430);color:var(--text,#e6edf3);border:1px solid var(--line,#30363d);}
.ncc-backlink:hover{background:var(--surface,#22272e);}
.ncc-prov{position:fixed;right:14px;bottom:14px;z-index:9999;max-width:44ch;font:500 10px/1.5
ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;padding:8px 10px;border-radius:8px;
background:var(--surface-2,#1b2430);color:var(--text-muted,#8b949e);
border:1px solid var(--line,#30363d);}
@media (max-width:900px){.ncc-prov{display:none;}}
"""

NAV_MARKER = "</body>"


# Archify ships with data-theme="dark" and switches on prefers-color-scheme.
# The suite requests the orange/light look, so default to light while leaving
# the in-page theme toggle functional.
THEME_RE = re.compile(r'(<html\b[^>]*\bdata-theme=)"dark"')
PRESET_RE = re.compile(r'(<html\b[^>]*\bdata-preset=)"[^"]*"')


def process(path: Path, depth: int, evidence: str) -> bool:
    html = path.read_text(encoding="utf-8")

    stripped = FONT_LINK_RE.sub("", html)
    stripped = PRECONNECT_RE.sub("", stripped)
    stripped = EXTERNAL_LINK_RE.sub(r"\1#\2", stripped)
    stripped = THEME_RE.sub(r'\1"light"', stripped)
    stripped = PRESET_RE.sub(r'\1"classic"', stripped)
    changed = stripped != html

    if "ncc-backlink" not in stripped:
        prefix = "../" * depth
        nav = (
            f'<style>{NAV_CSS}</style>\n'
            f'<a class="ncc-backlink" href="{prefix}index.html">&larr; Diagram index</a>\n'
            f'<div class="ncc-prov">{evidence}</div>\n'
        )
        idx = stripped.rfind(NAV_MARKER)
        if idx == -1:
            stripped += nav
        else:
            stripped = stripped[:idx] + nav + stripped[idx:]
        changed = True

    if changed:
        path.write_text(stripped, encoding="utf-8")
    return changed


def main() -> int:
    if len(sys.argv) < 4:
        print("usage: strip_cdn.py <depth> <evidence-banner> <file.html> [...]", file=sys.stderr)
        return 2
    depth = int(sys.argv[1])
    evidence = sys.argv[2]
    for arg in sys.argv[3:]:
        p = Path(arg)
        if p.exists():
            print(f"{'post-processed' if process(p, depth, evidence) else 'unchanged'}: {p.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
