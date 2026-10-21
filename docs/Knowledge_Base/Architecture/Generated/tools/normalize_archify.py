#!/usr/bin/env python3
"""Normalize Archify JSON IR against the shipped schemas.

The Archify schemas are strict (additionalProperties: false at every level),
so a few authoring conveniences are rejected by the renderers:

  * `cards` must be a TOP-LEVEL array, not a member of `meta`.
  * card items accept only `dot`, `title`, `items` — drop stray keys.
  * lifecycle `lanes` accept only `id` and `label` (no `variant`).
  * lifecycle `transitions` have no `role` field; `role` is workflow-only.
  * lifecycle transition `route` excludes `return-left` and `outside-right`.
  * workflow node `type` has no `decision` member; use `backend` and keep the
    diamond meaning in the label.
  * architecture `connections` have no `tag` field.

Run after build_archify_sources.py and before rendering.
"""
from __future__ import annotations

import json
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "sources" / "archify"

CARD_KEYS = {"dot", "title", "items"}
WORKFLOW_ROUTES = {"auto", "straight", "drop", "outside-right", "return-left", "bottom-channel", "up-channel"}
LIFECYCLE_ROUTES = {"auto", "straight", "drop", "bottom-channel", "top-channel", "right-channel", "left-channel"}
COMPONENT_TYPES = {"frontend", "backend", "database", "cloud", "security", "messagebus", "external"}


def clean_cards(cards):
    out = []
    for c in cards or []:
        out.append({k: v for k, v in c.items() if k in CARD_KEYS})
    return out


def normalize(doc: dict) -> dict:
    dtype = doc["diagram_type"]
    meta = doc.get("meta", {})

    # `cards` may not live inside meta.
    cards = clean_cards(meta.pop("cards", None)) or clean_cards(doc.get("cards"))
    if cards:
        doc["cards"] = cards

    if dtype == "workflow":
        for lane in doc.get("lanes", []):
            lane.pop("variant", None)
        for node in doc.get("nodes", []):
            if node.get("type") == "decision":
                node["type"] = "backend"
        for edge in doc.get("edges", []):
            if edge.get("route") not in WORKFLOW_ROUTES:
                edge.pop("route", None)

    elif dtype == "lifecycle":
        for lane in doc.get("lanes", []):
            lane.pop("variant", None)
        for st in doc.get("states", []):
            if st.get("type") not in {"start", "active", "waiting", "decision", "success", "failure", "neutral", "external"}:
                st["type"] = "active"
        for tr in doc.get("transitions", []):
            tr.pop("role", None)
            if tr.get("route") not in LIFECYCLE_ROUTES:
                tr.pop("route", None)

    elif dtype == "architecture":
        for comp in doc.get("components", []):
            if comp.get("type") not in COMPONENT_TYPES:
                comp["type"] = "backend"
        for conn in doc.get("connections", []):
            conn.pop("tag", None)

    elif dtype == "dataflow":
        for node in doc.get("nodes", []):
            if node.get("type") not in COMPONENT_TYPES:
                node["type"] = "backend"

    doc["meta"] = meta
    return doc


def main() -> int:
    changed = 0
    for path in sorted(SRC.glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        fixed = normalize(doc)
        text = json.dumps(fixed, indent=2) + "\n"
        if text != path.read_text(encoding="utf-8"):
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"normalized {path.name}")
    print(f"{changed} file(s) rewritten")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
