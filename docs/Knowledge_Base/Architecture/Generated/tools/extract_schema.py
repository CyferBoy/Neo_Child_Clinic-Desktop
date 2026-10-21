#!/usr/bin/env python3
"""Derive an ERD dataset from the local Supabase metadata CSV exports.

Evidence: docs/Schemas/*.csv (exported 2026-10-20 and 2026-10-21).
These are EXPORT artifacts, not live-verified configuration. This script
reads them only; it never contacts a database.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SCHEMAS = ROOT / "docs" / "Schemas"


def rows(name: str) -> list[dict]:
    with open(SCHEMAS / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


columns = rows("Supabase Snippet List Public Table Columns.csv")
relations = rows("Supabase Snippet List Relations in Public and Storage Schemas.csv")
constraints = rows("Supabase Snippet List constraints in public schema.csv")

# ---- tables -------------------------------------------------------------
rls = {
    r["relation_name"]: (r["rls_enabled"] == "true", r["relation_kind"])
    for r in relations
    if r["schema_name"] == "public"
}

tables: dict[str, dict] = {}
for c in columns:
    if c["table_schema"] != "public":
        continue
    t = tables.setdefault(
        c["table_name"],
        {"name": c["table_name"], "columns": [], "pk": [], "fks": [], "checks": [], "uniques": [],
         "rls_enabled": rls.get(c["table_name"], (False, "r"))[0]},
    )
    t["columns"].append(
        {
            "name": c["column_name"],
            "position": int(c["ordinal_position"]),
            "type": c["data_type"],
            "nullable": c["is_nullable"] == "YES",
            "default": c["column_default"],
        }
    )

# ---- constraints --------------------------------------------------------
FK_RE = re.compile(
    r"FOREIGN KEY\s*\((?P<cols>[^)]*)\)\s*REFERENCES\s+(?P<ref>[^\s(]+)\s*\((?P<refcols>[^)]*)\)"
    r"(?P<tail>.*)",
    re.I,
)
UQ_RE = re.compile(r"UNIQUE\s*\((?P<cols>[^)]*)\)", re.I)

for c in constraints:
    t = tables.get(c["table_name"])
    if t is None:
        continue
    definition = c["definition"]
    ctype = c["constraint_type"]
    if ctype == "p":
        t["pk"] = [x.strip() for x in definition.split("(", 1)[1].rsplit(")", 1)[0].split(",")]
    elif ctype == "f":
        m = FK_RE.search(definition)
        if m:
            t["fks"].append(
                {
                    "name": c["constraint_name"],
                    "columns": [x.strip() for x in m.group("cols").split(",")],
                    "ref_table": m.group("ref").split(".")[-1],
                    "ref_columns": [x.strip() for x in m.group("refcols").split(",")],
                    "on_delete": (re.search(r"ON DELETE ([A-Z_ ]+)", m.group("tail"), re.I).group(1).strip()
                                  if re.search(r"ON DELETE ([A-Z_ ]+)", m.group("tail"), re.I) else None),
                    "on_update": (re.search(r"ON UPDATE ([A-Z_ ]+)", m.group("tail"), re.I).group(1).strip()
                                  if re.search(r"ON UPDATE ([A-Z_ ]+)", m.group("tail"), re.I) else None),
                }
            )
    elif ctype == "c":
        t["checks"].append({"name": c["constraint_name"], "definition": definition})
    elif ctype == "u":
        m = UQ_RE.search(definition)
        t["uniques"].append(
            {"name": c["constraint_name"],
             "columns": [x.strip() for x in m.group("cols").split(",")] if m else [],
             "definition": definition}
        )

# ---- indices ------------------------------------------------------------
# NOTE: the file named "…Indexes in Public Schema (1).csv" is actually a
# row-level-security POLICY export; the file without "(1)" holds indexes.
indexes = rows("Supabase Snippet List Indexes in Public Schema.csv")
for i in indexes:
    t = tables.get(i.get("tablename", ""))
    if t is None:
        continue
    idxdef = i.get("indexdef", "")
    t.setdefault("indexes", []).append(
        {"name": i.get("indexname", ""), "unique": "UNIQUE" in idxdef.upper(), "definition": idxdef}
    )

# ---- row-level security policies ----------------------------------------
policies = rows("Supabase Snippet List Indexes in Public Schema (1).csv")
for p in policies:
    t = tables.get(p.get("tablename", ""))
    if t is None:
        continue
    t.setdefault("policies", []).append(
        {"name": p.get("policyname", ""), "roles": p.get("roles", ""),
         "cmd": p.get("cmd", ""), "using": p.get("qual", ""), "with_check": p.get("with_check", "")}
    )

# ---- triggers -----------------------------------------------------------
try:
    triggers = rows("Supabase Snippet List Public Schema Triggers.csv")
except FileNotFoundError:
    triggers = []
for tr in triggers:
    tname = tr.get("table_name") or ""
    t = tables.get(tname)
    if t is None:
        continue
    t.setdefault("triggers", []).append(
        {"name": tr.get("trigger_name", ""),
         "enabled": tr.get("tgenabled", ""),
         "definition": tr.get("definition", "")}
    )

# ---- cardinality: derive from FK nullability + uniqueness ---------------
for t in tables.values():
    for fk in t["fks"]:
        cols = {c["name"]: c for c in t["columns"]}
        nullable = all(cols[c]["nullable"] for c in fk["columns"] if c in cols)
        parent = tables.get(fk["ref_table"])
        parent_unique = parent is not None and (
            fk["ref_columns"] == parent["pk"]
            or any(u["columns"] == fk["ref_columns"] for u in parent.get("uniques", []))
        )
        fk["nullable"] = nullable
        fk["many_to_one"] = not parent_unique
        fk["child_required"] = not nullable

# ---- functions ----------------------------------------------------------
functions = rows("Supabase Snippet List Public Functions with Definitions.csv")

out = {
    "evidence": {
        "source": "docs/Schemas/*.csv (Supabase metadata exports)",
        "export_dates": ["2026-10-20", "2026-10-21"],
        "verification": "export-reported; not live-verified",
    },
    "tables": sorted(tables.values(), key=lambda t: t["name"]),
    "functions": [
        {"schema": f["schema_name"], "name": f["function_name"], "arguments": f["arguments"],
         "security_definer": f["security_definer"] == "true", "provolatile": f["provolatile"]}
        for f in functions
    ],
}

dest = Path(__file__).resolve().parents[1] / "sources" / "schema-model.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
print(f"tables={len(tables)} fks={sum(len(t['fks']) for t in tables.values())} "
      f"functions={len(out['functions'])} -> {dest}")
