#!/usr/bin/env python3
"""Iteratively repair Archify layout-validation failures.

Archify runs a strict layout validator after schema validation and prints an
actionable "Suggested fix" line for most problems. This tool runs the renderer's
`validate` command, parses those diagnostics, and applies the fixes to the JSON
IR, repeating until the diagram validates or no further progress is made.

Handled diagnostics:
  * architecture components missing pos  -> enable grid layout
  * guided-view focus ids that do not exist -> drop the unknown ids
  * "Label ... overlaps node ..."       -> apply the suggested labelAt
  * "Nodes ... less than 8px apart"     -> move the later node to a free column
  * "Edge ... is too short"             -> drop the offending edge label

Usage:  auto_fix_layout.py [name ...]
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
ARCHIFY = ROOT / ".opencode" / "skills" / "archify" / "bin" / "archify.mjs"
SRC = Path(__file__).resolve().parents[1] / "sources" / "archify"

# Column origins the workflow/lifecycle renderers use, with the node width they
# assume. Two nodes in one lane must not land in columns closer than this.
COL_XS = [88, 220, 300, 430, 500, 625]
NODE_W = 92
MIN_GAP = 8

LABEL_AT_RE = re.compile(r'Suggested fix: labelAt \[(-?[\d.]+), (-?[\d.]+)\]')
LABEL_DY_RE = re.compile(r'labelDy ([+-]?\d+)')
OVERLAP_RE = re.compile(r'Label "(.*?)" overlaps node "(.*?)"')
NODES_APART_RE = re.compile(r'Nodes "(.*?)" and "(.*?)" are less than \d+px apart in lane "(.*?)"')
EDGE_SHORT_RE = re.compile(r'Edge "(.*?)" -> "(.*?)" is too short')
COL_MOVE_RE = re.compile(r'move "(.*?)" to col (\d+)')


def run_validate(dtype: str, path: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        ["node", str(ARCHIFY), "validate", dtype, str(path)],
        capture_output=True, text=True, cwd=ROOT,
    )
    return proc.returncode == 0, (proc.stdout + proc.stderr)


def col_far_enough(col: int, taken: list[int]) -> bool:
    for other in taken:
        if abs(COL_XS[col] - COL_XS[other]) < NODE_W + MIN_GAP:
            return False
    return True


def fix_architecture(doc: dict) -> bool:
    """Give architecture diagrams a grid layout so components get real positions."""
    changed = False
    comps = doc.get("components", [])
    if any("pos" not in c for c in comps):
        max_col = max((c.get("col", 0) for c in comps), default=0)
        if "layout" not in doc:
            doc["layout"] = {"mode": "grid", "cols": max(3, max_col + 1),
                             "cellW": 170, "cellH": 96, "gapX": 70, "gapY": 56}
            changed = True
    return changed


def fix_views(doc: dict) -> bool:
    """Drop guided-view focus ids that do not map to a real element."""
    views = doc.get("meta", {}).get("views")
    if not views:
        return False
    valid = set()
    for key in ("components", "nodes", "states", "participants"):
        for item in doc.get(key, []):
            valid.add(item.get("id"))
    for conn_key in ("connections", "edges", "flows", "transitions", "messages"):
        for item in doc.get(conn_key, []):
            if item.get("id"):
                valid.add(item["id"])
    changed = False
    for view in views:
        focus = view.get("focus")
        if not focus:
            continue
        pruned = [f for f in focus if f in valid]
        if len(pruned) != len(focus):
            view["focus"] = pruned
            changed = True
    return changed


def fix_labels(doc: dict, log: str) -> bool:
    """Apply suggested labelAt / labelDy values from overlap diagnostics."""
    changed = False
    buckets = []
    for key in ("edges", "transitions", "flows", "connections"):
        if isinstance(doc.get(key), list):
            buckets.append(doc[key])
    for bucket in buckets:
        for item in bucket:
            label = item.get("label")
            if not label:
                continue
            for m in OVERLAP_RE.finditer(log):
                if m.group(1) != label:
                    continue
                # Prefer the exact labelAt suggestion that follows this message.
                tail = log[m.end():m.end() + 400]
                at = LABEL_AT_RE.search(tail)
                if at:
                    item["labelAt"] = [float(at.group(1)), float(at.group(2))]
                    item.pop("labelDx", None)
                    item.pop("labelDy", None)
                    changed = True
                    continue
                dy = LABEL_DY_RE.search(tail)
                if dy:
                    item["labelDy"] = int(dy.group(1))
                    changed = True
    return changed


def drop_short_edge_labels(doc: dict, log: str) -> bool:
    changed = False
    for key in ("edges", "transitions", "flows", "connections"):
        for item in doc.get(key) or []:
            label = item.get("label")
            if not label:
                continue
            for m in EDGE_SHORT_RE.finditer(log):
                if m.group(1) == item.get("from") and m.group(2) == item.get("to"):
                    item.pop("label", None)
                    changed = True
    return changed


def move_apart_nodes(doc: dict, log: str) -> bool:
    """Reassign a node's column when two same-lane nodes are too close."""
    key = "states" if doc["diagram_type"] == "lifecycle" else "nodes"
    nodes = doc.get(key) or []
    by_id = {n["id"]: n for n in nodes}
    changed = False
    for m in NODES_APART_RE.finditer(log):
        a, b, lane = m.group(1), m.group(2), m.group(3)
        tail = log[m.end():m.end() + 400]
        move = COL_MOVE_RE.search(tail)
        target = by_id.get(b) or by_id.get(a)
        if target is None:
            continue
        lane_nodes = [n for n in nodes if n.get("lane") == lane and n["id"] != target["id"]]
        taken = [n.get("col", 0) for n in lane_nodes]
        if move:
            new_col = int(move.group(1))
            if 0 <= new_col <= 5 and col_far_enough(new_col, taken):
                target["col"] = new_col
                changed = True
                continue
        # Fall back to the first well-separated free column.
        for candidate in range(6):
            if col_far_enough(candidate, taken):
                target["col"] = candidate
                changed = True
                break
    return changed


def main() -> int:
    names = sys.argv[1:]
    targets = sorted(SRC.glob("*.json"))
    if names:
        targets = [t for t in targets if t.stem.split(".")[0] in names]

    remaining = []
    for path in targets:
        doc = json.loads(path.read_text(encoding="utf-8"))
        dtype = doc["diagram_type"]
        fix_architecture(doc)
        fix_views(doc)
        path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")

        ok, log = run_validate(dtype, path)
        rounds = 0
        while not ok and rounds < 8:
            doc = json.loads(path.read_text(encoding="utf-8"))
            progressed = (
                fix_labels(doc, log)
                or drop_short_edge_labels(doc, log)
                or move_apart_nodes(doc, log)
            )
            if not progressed:
                break
            path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
            ok, log = run_validate(dtype, path)
            rounds += 1

        if ok:
            print(f"OK   {path.name}")
        else:
            first = [l for l in log.splitlines() if l.startswith("- ")]
            print(f"FAIL {path.name}")
            for line in first[:4]:
                print(f"     {line}")
            remaining.append(path.name)

    print(f"\n{len(targets) - len(remaining)}/{len(targets)} validate cleanly")
    if remaining:
        print("still failing:", ", ".join(remaining))
    return 1 if remaining else 0


if __name__ == "__main__":
    raise SystemExit(main())
