#!/usr/bin/env python3
"""Emit layout-safe Archify JSON IR for the Neo Child Clinic diagram suite.

Every diagram carries an explicit evidence class in meta.subtitle so a reader can
tell implemented, proposed, export-reported, and unknown behavior apart on the
face of the artifact.

Evidence classes:
  [ANDROID-SOURCE]   verified against Android source at ca4bed4 (reference only)
  [DESKTOP-PROPOSED] planned desktop behavior from the Knowledge Base; NOT implemented
  [SCHEMA-EXPORT]    reported by docs/Schemas metadata exports; not live-verified
  [UNKNOWN]          could not be verified from available evidence

The Archify renderers use fixed geometry, so the helpers below enforce the rules
that keep the strict layout validator happy:

  workflow   3 lanes do/guard/err. Only adjacent-lane drops (do->guard, guard->err)
             are used, so no edge crosses an unrelated node in an intermediate lane.
             guard nodes sit at columns {0,2,4} (well-spaced in colXs) and each err
             node sits directly below its guard source (same column).
  lifecycle  lane "main" = phase band (cols 0..4), lane "terminal" = outcome band
             (cols 0..2). Back-edges use bottom/top channels to route around states.
  sequence   participant labels stay short; self-messages (from==to) are dropped
             because they span 0px; the viewBox is tall enough for the last message.
  dataflow   meta.viewBox[0] is widened so every stage and node fits.
  architecture  a grid layout is attached and guided-view focus ids are pruned.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "sources" / "archify"
OUT.mkdir(parents=True, exist_ok=True)

DIAGRAMS: list[tuple[str, dict]] = []

# Workflow column origins (colXs) and the node width the renderer assumes.
WF_COL_XS = [88, 220, 300, 430, 500, 625]
WF_NODE_W = 92


def card(dot: str, title: str, *items: str) -> dict:
    return {"dot": dot, "title": title, "items": list(items)}


def view(vid: str, label: str, focus: list[str], note: str) -> dict:
    return {"id": vid, "label": label, "focus": focus, "note": note}


def _emit(name: str, doc: dict) -> None:
    doc.setdefault("schema_version", 1)
    DIAGRAMS.append((name, doc))


# --------------------------------------------------------------------------
# ARCHITECTURE — attach a grid layout and prune guided-view focus ids
# --------------------------------------------------------------------------

def arch(name: str, title: str, subtitle: str, components: list[dict],
         boundaries: list[dict], connections: list[dict], cards: list[dict],
         views: list[dict] | None = None) -> None:
    max_col = max((c.get("col", 0) for c in components), default=0)
    max_row = max((c.get("row", 0) for c in components), default=0)
    meta = {"title": title, "subtitle": subtitle, "quality_profile": "standard"}
    if views:
        valid = {c["id"] for c in components} | {c["id"] for c in connections}
        for v in views:
            v["focus"] = [f for f in v["focus"] if f in valid]
        meta["views"] = views
    _emit(name, {
        "diagram_type": "architecture",
        "meta": meta,
        "layout": {"mode": "grid", "cols": max(2, max_col + 1),
                   "cellW": 170, "cellH": 96 + max_row * 8, "gapX": 70, "gapY": 56},
        "cards": cards,
        "components": components,
        "boundaries": boundaries,
        "connections": connections,
    })


# --------------------------------------------------------------------------
# DATAFLOW — widen the viewBox so every stage fits
# --------------------------------------------------------------------------

def df(name: str, title: str, subtitle: str, stages: list[dict],
       nodes: list[dict], flows: list[dict], cards: list[dict],
       views: list[dict] | None = None) -> None:
    width = 100 + len(stages) * 215 + 60
    meta = {"title": title, "subtitle": subtitle,
            "quality_profile": "standard", "viewBox": [width, 760]}
    if views:
        valid = {n["id"] for n in nodes} | {f["id"] for f in flows}
        for v in views:
            v["focus"] = [f for f in v["focus"] if f in valid]
        meta["views"] = views
    _emit(name, {
        "diagram_type": "dataflow",
        "meta": meta,
        "cards": cards,
        "stages": stages,
        "nodes": nodes,
        "flows": flows,
    })


# --------------------------------------------------------------------------
# SEQUENCE — drop self-messages, size the viewBox to the last message
# --------------------------------------------------------------------------

def seq(name: str, title: str, subtitle: str, participants: list[dict],
        messages: list[dict], cards: list[dict],
        views: list[dict] | None = None) -> None:
    real = [m for m in messages if m["from"] != m["to"]]
    max_y = max((m["y"] for m in real), default=200)
    meta = {"title": title, "subtitle": subtitle,
            "quality_profile": "standard",
            "viewBox": [96 + len(participants) * 108 + 40, max_y + 130]}
    if views:
        valid = {p["id"] for p in participants} | {m["id"] for m in real if m.get("id")}
        for v in views:
            v["focus"] = [f for f in v["focus"] if f in valid]
        meta["views"] = views
    _emit(name, {
        "diagram_type": "sequence",
        "meta": meta,
        "cards": cards,
        "participants": participants,
        "messages": real,
    })


# --------------------------------------------------------------------------
# WORKFLOW — 3 lanes do/guard/err, adjacent drops only, err below its source
# --------------------------------------------------------------------------

def wf(name: str, title: str, subtitle: str, do_l: str, guard_l: str, err_l: str,
       do_nodes: list[dict], guard_nodes: list[dict], err_nodes: list[dict],
       edges: list[dict], cards: list[dict]) -> None:
    for n in do_nodes:
        n["lane"] = do_l
    for n in guard_nodes:
        n["lane"] = guard_l
    for n in err_nodes:
        n["lane"] = err_l
    # Validate guard columns are well spaced and err nodes sit under a guard col.
    gcols = sorted(n["col"] for n in guard_nodes)
    for a, b in zip(gcols, gcols[1:]):
        if abs(WF_COL_XS[b] - WF_COL_XS[a]) < WF_NODE_W + 8:
            raise SystemExit(f"{name}: guard cols {a},{b} too close")
    guard_col = {n["id"]: n["col"] for n in guard_nodes}
    for e in edges:
        src, dst = e["from"], e["to"]
        if dst in {n["id"] for n in err_nodes} and src in guard_col:
            if guard_col[src] != next(n["col"] for n in err_nodes if n["id"] == dst):
                raise SystemExit(f"{name}: err node {dst} not under {src}")
    _emit(name, {
        "diagram_type": "workflow",
        "meta": {"title": title, "subtitle": subtitle, "quality_profile": "standard"},
        "cards": cards,
        "lanes": [{"id": do_l, "label": do_l.replace("-", " ").title()},
                  {"id": guard_l, "label": guard_l.replace("-", " ").title()},
                  {"id": err_l, "label": err_l.replace("-", " ").title()}],
        "nodes": do_nodes + guard_nodes + err_nodes,
        "edges": edges,
    })


# --------------------------------------------------------------------------
# LIFECYCLE — lane main (phase band) + terminal (outcome band)
# --------------------------------------------------------------------------

def lc(name: str, title: str, subtitle: str, main_states: list[dict],
       term_states: list[dict], transitions: list[dict], cards: list[dict],
       main_label: str = "Progression", term_label: str = "Outcome") -> None:
    for s in main_states:
        s["lane"] = "main"
    for s in term_states:
        s["lane"] = "terminal"
    for tr in transitions:
        tr.setdefault("labelDy", 58)
    _emit(name, {
        "diagram_type": "lifecycle",
        "meta": {"title": title, "subtitle": subtitle, "quality_profile": "standard"},
        "cards": cards,
        "lanes": [{"id": "main", "label": main_label},
                  {"id": "terminal", "label": term_label}],
        "states": main_states + term_states,
        "transitions": transitions,
    })


# ==========================================================================
# DATA AND FLOWS
# ==========================================================================

arch("system-context",
     "System Context — Neo Child Clinic Desktop",
     "[DESKTOP-PROPOSED] Staff clients, the desktop shell, the shared Supabase project, and external services. No desktop process exists yet.",
     [
         {"id": "staff", "type": "external", "label": "Clinic Staff", "sublabel": "5 role values", "row": 0, "col": 0, "tag": "actors"},
         {"id": "desktop", "type": "frontend", "label": "Desktop App", "sublabel": "Go + Wails + React", "row": 0, "col": 1, "tag": "PROPOSED"},
         {"id": "supabase", "type": "cloud", "label": "Supabase", "sublabel": "shared project", "row": 0, "col": 3, "tag": "same as Android"},
         {"id": "authsvc", "type": "security", "label": "Supabase Auth", "sublabel": "JWT + app_metadata", "row": 1, "col": 2},
         {"id": "storage", "type": "database", "label": "Storage", "sublabel": "patient-docs bucket", "row": 1, "col": 3},
         {"id": "edgefn", "type": "backend", "label": "Edge Functions", "sublabel": "manage-staff", "row": 2, "col": 2},
         {"id": "backupsvc", "type": "cloud", "label": "Backup Target", "sublabel": "ADR-0010 pending", "row": 2, "col": 0, "tag": "UNDESIGNED"},
     ],
     [
         {"kind": "region", "label": "Clinic workstation", "wraps": ["staff", "desktop"]},
         {"kind": "region", "label": "Shared Supabase project (existing)", "wraps": ["supabase", "authsvc", "storage", "edgefn"]},
     ],
     [
         {"id": "c1", "from": "staff", "to": "desktop", "label": "keyboard / UI", "variant": "emphasis"},
         {"id": "c2", "from": "desktop", "to": "supabase", "label": "HTTPS REST", "variant": "security"},
         {"id": "c3", "from": "desktop", "to": "authsvc", "label": "sign-in", "variant": "security", "fromSide": "bottom", "toSide": "left"},
         {"id": "c4", "from": "desktop", "to": "storage", "label": "documents", "variant": "dashed", "fromSide": "bottom", "toSide": "left"},
         {"id": "c5", "from": "desktop", "to": "edgefn", "label": "invoke", "variant": "dashed", "fromSide": "bottom", "toSide": "left"},
         {"id": "c6", "from": "desktop", "to": "backupsvc", "label": "encrypted export", "variant": "dashed", "fromSide": "bottom", "toSide": "top"},
     ],
     [
         card("emerald", "Actors",
              "admin, doctor, nurse, receptionist, inventory_manager",
              "Roles come from Supabase JWT app_metadata, not local state",
              "Desktop must not become an independent authorization source"),
         card("cyan", "Shared backend",
              "One Supabase project, one PostgreSQL database [DECISION]",
              "Auth users, Storage buckets, and Edge Functions are shared",
              "Local SQLite is a working copy, not a second backend"),
         card("rose", "Unverified",
              "Runtime anonymous access has not been exercised [UNKNOWN]",
              "Realtime authorization is unverified [UNKNOWN]",
              "Live RLS enforcement is export-reported only"),
     ],
     [
         view("staff-to-desktop", "Staff to desktop", ["staff", "desktop"],
              "Clinic staff are the only actors; the desktop app is the system boundary."),
         view("shared-backend", "Shared Supabase backend", ["desktop", "supabase", "authsvc", "storage"],
              "Android and desktop share one Supabase project per ADR-0008."),
         view("backup-path", "Backup path", ["desktop", "backupsvc"],
              "Encrypted backup target is approved in ADR-0010 but not designed."),
     ])

arch("application-architecture",
     "Application Architecture — Desktop Layers",
     "[DESKTOP-PROPOSED] Layered desktop architecture from the Knowledge Base. No desktop source, binding, or worker exists yet.",
     [
         {"id": "ui", "type": "frontend", "label": "React Renderer", "sublabel": "screens + view state", "row": 0, "col": 0, "tag": "no PHI in storage"},
         {"id": "bindings", "type": "backend", "label": "Wails Bindings", "sublabel": "typed Go methods", "row": 0, "col": 1, "tag": "only crossing"},
         {"id": "svc", "type": "backend", "label": "App Services", "sublabel": "orchestration", "row": 0, "col": 2},
         {"id": "domain", "type": "backend", "label": "Domain Rules", "sublabel": "validation + totals", "row": 1, "col": 2, "tag": "pure"},
         {"id": "repo", "type": "backend", "label": "Repositories", "sublabel": "SQL ownership", "row": 0, "col": 3},
         {"id": "sqlite", "type": "database", "label": "Local SQLite", "sublabel": "working copy", "row": 0, "col": 4},
         {"id": "sync", "type": "messagebus", "label": "Sync Worker", "sublabel": "queue + retry", "row": 1, "col": 3},
         {"id": "remote", "type": "cloud", "label": "Supabase", "sublabel": "shared authority", "row": 1, "col": 4},
     ],
     [
         {"kind": "security-group", "label": "Desktop process", "wraps": ["ui", "bindings", "svc", "domain", "repo", "sqlite", "sync"]},
         {"kind": "security-group", "label": "Renderer trust boundary", "wraps": ["ui"]},
     ],
     [
         {"id": "a1", "from": "ui", "to": "bindings", "label": "typed call", "variant": "emphasis"},
         {"id": "a2", "from": "bindings", "to": "svc", "label": "invoke"},
         {"id": "a3", "from": "svc", "to": "domain", "label": "validate", "variant": "dashed"},
         {"id": "a4", "from": "svc", "to": "repo", "label": "read / write"},
         {"id": "a5", "from": "repo", "to": "sqlite", "label": "SQL"},
         {"id": "a6", "from": "sync", "to": "remote", "label": "HTTPS", "variant": "security"},
         {"id": "a7", "from": "sync", "to": "sqlite", "label": "queue + merge", "variant": "dashed", "fromSide": "left", "toSide": "bottom"},
     ],
     [
         card("emerald", "Layers",
              "React + TypeScript renderer (view state only)",
              "Typed Wails v3 Go bindings are the only crossing",
              "Go application services orchestrate domain work"),
         card("cyan", "Persistence",
              "Local SQLite working copy; encryption pending (ADR-0010)",
              "Repositories own all SQL; services never issue raw queries",
              "The local database is not a second source of truth"),
         card("rose", "Planned, not implemented",
              "0 of 22 desktop modules are implemented",
              "No Go/Wails/React source exists in the repository",
              "These boxes describe intent, not code"),
     ],
     [
         view("renderer-to-db", "Read/write path", ["ui", "bindings", "svc", "repo", "sqlite"],
              "Every read and write crosses the typed Wails binding boundary."),
         view("sync-path", "Sync path", ["svc", "sync", "remote"],
              "A Go sync worker owns all remote writes."),
         view("trust", "Trust boundaries", ["ui", "bindings", "remote"],
              "The React renderer never calls Supabase or opens the local database."),
     ])

arch("deployment-desktop",
     "Deployment Diagram — Desktop Runtime",
     "[DESKTOP-PROPOSED] Single desktop process, webview frontend, Go runtime, local storage, shared Supabase. Nothing is deployed yet.",
     [
         {"id": "host", "type": "external", "label": "Workstation", "sublabel": "clinic PC", "row": 0, "col": 0},
         {"id": "process", "type": "backend", "label": "Desktop Process", "sublabel": "Wails v3 runtime", "row": 0, "col": 1, "tag": "single process"},
         {"id": "webview", "type": "frontend", "label": "WebView", "sublabel": "React bundle", "row": 2, "col": 1},
         {"id": "dbfile", "type": "database", "label": "SQLite File", "sublabel": "working copy", "row": 0, "col": 2},
         {"id": "net", "type": "cloud", "label": "Clinic Network", "sublabel": "may be offline", "row": 1, "col": 3},
         {"id": "supa", "type": "cloud", "label": "Supabase", "sublabel": "shared project", "row": 1, "col": 4, "tag": "same as Android"},
     ],
     [
         {"kind": "region", "label": "Clinic workstation", "wraps": ["host", "process", "webview", "dbfile"]},
         {"kind": "security-group", "label": "Desktop process trust boundary", "wraps": ["process", "webview", "dbfile"]},
     ],
     [
         {"id": "d1", "from": "host", "to": "process", "label": "launch"},
         {"id": "d2", "from": "process", "to": "webview", "label": "host + bind", "variant": "emphasis"},
         {"id": "d3", "from": "process", "to": "dbfile", "label": "SQLCipher or plain", "variant": "dashed"},
         {"id": "d4", "from": "process", "to": "net", "label": "HTTPS"},
         {"id": "d5", "from": "net", "to": "supa", "label": "REST / Realtime", "variant": "security"},
     ],
     [
         card("emerald", "One process",
              "Wails v3 hosts the Go runtime and the webview in one process",
              "The renderer is served from embedded assets, not a network origin",
              "Local SQLite file is the only durable local state"),
         card("cyan", "Shared authority",
              "Supabase is the same project Android uses [DECISION]",
              "Auth, PostgREST, Realtime, Storage, and Edge Functions are all shared",
              "No new remote database or parallel schema is approved"),
         card("rose", "Open decisions",
              "Local database encryption is decided by ADR-0010 [PENDING]",
              "Backup target and retention are not designed [PENDING]",
              "Auto-update feed URL and signing chain are unknown [UNKNOWN]"),
     ])

arch("component-android-reference",
     "Android Reference Components",
     "[ANDROID-SOURCE] Verified module structure at ca4bed4. This is the reference implementation, not the desktop design.",
     [
         {"id": "app", "type": "frontend", "label": "app", "sublabel": "navigation + DI graph", "row": 0, "col": 0},
         {"id": "core", "type": "backend", "label": "core", "sublabel": "cache database network sync", "row": 0, "col": 1},
         {"id": "data", "type": "database", "label": "data", "sublabel": "local + remote sources", "row": 0, "col": 2},
         {"id": "room", "type": "database", "label": "Room", "sublabel": "25 entities v33", "row": 0, "col": 3},
         {"id": "domain", "type": "backend", "label": "domain", "sublabel": "models + repos", "row": 1, "col": 1},
         {"id": "supabase", "type": "cloud", "label": "Supabase", "sublabel": "shared project", "row": 1, "col": 4},
         {"id": "feature", "type": "frontend", "label": "feature", "sublabel": "21 packages", "row": 2, "col": 0},
     ],
     [
         {"kind": "region", "label": "Android application (reference)", "wraps": ["app", "core", "data", "domain", "feature", "room"]},
     ],
     [
         {"id": "r1", "from": "feature", "to": "domain", "label": "use cases", "variant": "emphasis"},
         {"id": "r2", "from": "domain", "to": "data", "label": "repo contracts", "variant": "dashed"},
         {"id": "r3", "from": "data", "to": "core", "label": "sync + network"},
         {"id": "r4", "from": "data", "to": "room", "label": "Room DAOs"},
         {"id": "r5", "from": "data", "to": "supabase", "label": "PostgREST", "variant": "security"},
         {"id": "r6", "from": "app", "to": "feature", "label": "routes", "variant": "emphasis", "fromSide": "bottom", "toSide": "top"},
     ],
     [
         card("emerald", "Verified modules",
              "app, core, data, domain, feature packages",
              "core splits into cache database di network sync security",
              "21 feature packages under feature/"),
         card("cyan", "Persistence",
              "Room AppDatabase version 33, 25 entities, 21 DAOs",
              "SQLCipher encrypted with a Keystore-derived passphrase",
              "16 migration objects from 17_18 through 32_33"),
         card("rose", "Known debt",
              "Duplicate stock triggers and a failed 20261017 guard block writes",
              "Receipt and stock RPCs are exposed to anon in the export",
              "The desktop must reproduce meaning, not Android's structure"),
     ])

df("dataflow-offline-sync",
   "Offline Capture and Sync Data Flow",
   "[ANDROID-SOURCE] Verified Android path, and the same contract the desktop must honor. Remote authorization is export-reported only.",
   [{"label": "Capture"}, {"label": "Queue"}, {"label": "Push"}, {"label": "Authority"}, {"label": "Pull"}],
   [
       {"id": "screen", "type": "frontend", "label": "Screen", "sublabel": "validated input", "stage": 0, "row": 1},
       {"id": "svc", "type": "backend", "label": "Service", "sublabel": "domain rules", "stage": 0, "row": 3, "tag": "atomic"},
       {"id": "sqlite", "type": "database", "label": "SQLite", "sublabel": "working copy", "stage": 1, "row": 1},
       {"id": "queue", "type": "messagebus", "label": "sync_queue", "sublabel": "PENDING rows", "stage": 1, "row": 3, "tag": "no unique idx"},
       {"id": "worker", "type": "backend", "label": "Sync Worker", "sublabel": "grouped upload", "stage": 2, "row": 2, "tag": "retry < 5"},
       {"id": "supabase", "type": "cloud", "label": "Supabase", "sublabel": "shared authority", "stage": 3, "row": 2, "tag": "RLS"},
       {"id": "merge", "type": "database", "label": "Merge", "sublabel": "last-write-wins", "stage": 4, "row": 2},
   ],
   [
       {"id": "f1", "from": "screen", "to": "svc", "label": "validated", "classification": "no PHI at rest", "variant": "emphasis"},
       {"id": "f2", "from": "svc", "to": "sqlite", "label": "one tx", "classification": "atomic write", "variant": "emphasis"},
       {"id": "f3", "from": "svc", "to": "queue", "label": "enqueue", "classification": "durable intent", "fromSide": "bottom", "toSide": "bottom"},
       {"id": "f4", "from": "queue", "to": "worker", "label": "drain", "classification": "ordered"},
       {"id": "f5", "from": "worker", "to": "supabase", "label": "upsert", "classification": "authenticated", "variant": "security"},
       {"id": "f6", "from": "supabase", "to": "merge", "label": "server rows", "classification": "last-write-wins"},
   ],
   [
       card("emerald", "Local first",
            "Writes land in SQLite and a sync_queue row in one transaction",
            "The UI never waits on the network to confirm a save",
            "sync_queue carries operation, priority, retryCount, groupId"),
       card("amber", "Push then pull",
            "Reconciler pushes outbound items first, then pulls inbound",
            "Groups are ordered by priority; DELETE runs negative priority",
            "Stale SYNCING rows are requeued after 5 minutes"),
       card("rose", "Unverified",
            "RLS evaluation at runtime is export-reported, not observed [UNKNOWN]",
            "Realtime authorization has not been exercised [UNKNOWN]"),
   ],
   [
       view("capture", "Capture and queue", ["screen", "svc", "sqlite", "queue"],
            "Writes land in SQLite and a sync_queue row in one transaction."),
       view("push", "Push to authority", ["queue", "worker", "supabase"],
            "The worker pushes outbound items before pulling inbound changes."),
   ])

df("dataflow-patient-registration-offline",
   "Patient Registration While Offline",
   "[DESKTOP-PROPOSED] Planned desktop offline registration path, mirroring verified Android behavior. Not implemented.",
   [{"label": "Form"}, {"label": "Local write"}, {"label": "Hold"}, {"label": "Upload"}, {"label": "Confirm"}],
   [
       {"id": "form", "type": "frontend", "label": "Patient Form", "sublabel": "required fields", "stage": 0, "row": 1},
       {"id": "validate", "type": "backend", "label": "Validation", "sublabel": "name + dob", "stage": 0, "row": 3, "tag": "fail closed"},
       {"id": "sqlite", "type": "database", "label": "Local DB", "sublabel": "patients row", "stage": 1, "row": 2, "tag": "commit"},
       {"id": "queue", "type": "messagebus", "label": "Pending Queue", "sublabel": "offline intent", "stage": 2, "row": 2},
       {"id": "upload", "type": "backend", "label": "Sync Upload", "sublabel": "on reconnect", "stage": 3, "row": 2},
       {"id": "supabase", "type": "cloud", "label": "Supabase", "sublabel": "patients table", "stage": 4, "row": 2},
   ],
   [
       {"id": "p1", "from": "form", "to": "validate", "label": "fields", "classification": "PHI in memory", "variant": "emphasis"},
       {"id": "p2", "from": "validate", "to": "sqlite", "label": "accepted", "classification": "PHI at rest", "variant": "security"},
       {"id": "p3", "from": "sqlite", "to": "queue", "label": "enqueue", "classification": "durable intent"},
       {"id": "p4", "from": "queue", "to": "upload", "label": "network up", "classification": "retry", "variant": "dashed"},
       {"id": "p5", "from": "upload", "to": "supabase", "label": "upsert", "classification": "authenticated", "variant": "security"},
   ],
   [
       card("emerald", "Confirmed locally",
            "The form confirms the save without a network round trip",
            "A temporary clinic id is replaced before the record is durable",
            "The audit row is written inside the same transaction"),
       card("amber", "Deferred",
            "Upload waits for a reconnect with exponential backoff",
            "Pending count surfaces on the dashboard sync chip"),
       card("rose", "Not designed",
            "Duplicate clinic-id collision handling on merge is open",
            "Remote soft-delete vs local hard-delete semantics are open"),
   ])

# ==========================================================================
# WORKFLOWS (3 lanes: do / guard / err)
# ==========================================================================

wf("auth-authorization-flow",
   "Authentication and Authorization Flow",
   "[SCHEMA-EXPORT + ANDROID-SOURCE] Sign-in, session, role, and RLS as reported by exports and Android code. Live enforcement is UNKNOWN.",
   "sign-in", "role-and-rls", "denial",
   [{"id": "creds", "col": 0, "type": "external", "label": "Credentials", "sublabel": "email + password"}],
   [
       {"id": "signin", "col": 0, "type": "security", "label": "Sign In", "sublabel": "issues JWT"},
       {"id": "role", "col": 2, "type": "backend", "label": "Role Claim", "sublabel": "app_metadata.role", "tag": "source of truth"},
       {"id": "gate", "col": 4, "type": "security", "label": "RLS Policy", "sublabel": "per-table qual", "tag": "get_my_role()"},
   ],
   [
       {"id": "denied", "col": 4, "type": "security", "label": "Denied", "sublabel": "no rows + audit"},
   ],
   [
       {"id": "e1", "from": "creds", "to": "signin", "label": "submit", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "e2", "from": "signin", "to": "role", "label": "decode JWT", "variant": "emphasis"},
       {"id": "e3", "from": "role", "to": "gate", "label": "request", "variant": "security"},
       {"id": "e4", "from": "gate", "to": "denied", "label": "qual false", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "Verified client side",
            "Role is read from the JWT app_metadata claim, not local state",
            "A missing or unknown role maps to no UI privilege",
            "Session restore resolves within a bounded timeout"),
       card("rose", "Export-reported backend",
            "get_my_role() falls back to 'nurse' when no profile matches",
            "Ten core clinical and inventory tables carry {public} policies",
            "All 21 functions are anon-executable in the export"),
       card("amber", "Unverified",
            "None of the above has been exercised against the live API [UNKNOWN]",
            "Post-October-30 default ACLs are unknown [UNKNOWN]"),
   ])

wf("error-recovery-flow",
   "Error Handling and Recovery Flow",
   "[DESKTOP-PROPOSED] Planned desktop failure taxonomy, modeled on verified Android error classes. Desktop code does not exist.",
   "action", "processing", "failure",
   [{"id": "action", "col": 0, "type": "external", "label": "User Action", "sublabel": "save or sync"}],
   [
       {"id": "guard", "col": 0, "type": "backend", "label": "Validation", "sublabel": "domain rules", "tag": "gate"},
       {"id": "commit", "col": 2, "type": "database", "label": "Commit", "sublabel": "local + queue"},
       {"id": "send", "col": 4, "type": "messagebus", "label": "Upload", "sublabel": "grouped, retry < 5"},
   ],
   [
       {"id": "fatal", "col": 4, "type": "security", "label": "Surface", "sublabel": "no auto retry"},
       {"id": "invalid", "col": 0, "type": "security", "label": "Blocked", "sublabel": "validation failed"},
   ],
   [
       {"id": "x1", "from": "action", "to": "guard", "label": "submit", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "x2", "from": "guard", "to": "commit", "label": "valid", "variant": "emphasis"},
       {"id": "x3", "from": "commit", "to": "send", "label": "drain"},
       {"id": "x4", "from": "guard", "to": "invalid", "label": "invalid", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "x5", "from": "send", "to": "fatal", "label": "401/schema", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "Fail closed",
            "Validation failures never leave a partial record",
            "Destructive operations confirm before they run",
            "Every recovery path returns the user to a known state"),
       card("amber", "Retry classification",
            "Transient network faults retry with exponential backoff",
            "Authorization and schema faults do not retry",
            "A bounded retry budget prevents hot loops"),
       card("rose", "Unproven",
            "No desktop error taxonomy is implemented yet",
            "Crash reporting and PHI redaction are undesigned",
            "No test has been executed against these paths"),
   ])

wf("build-packaging-android",
   "Build and Packaging Pipeline (Android Reference)",
   "[ANDROID-SOURCE] The only real pipeline in evidence is Android Gradle. No desktop build, package, signing, or CI configuration exists.",
   "source", "gradle", "blocked",
   [{"id": "kt", "col": 0, "type": "external", "label": "Kotlin Source", "sublabel": "352 files"}],
   [
       {"id": "catalog", "col": 0, "type": "backend", "label": "Catalog", "sublabel": "libs.versions.toml"},
       {"id": "assemble", "col": 2, "type": "backend", "label": "Assemble", "sublabel": "compile + dex"},
       {"id": "apk", "col": 4, "type": "cloud", "label": "APK / AAB", "sublabel": "signed release"},
   ],
   [
       {"id": "blocked", "col": 4, "type": "security", "label": "Desktop Build", "sublabel": "NOT CONFIGURED", "tag": "blocked"},
   ],
   [
       {"id": "b1", "from": "kt", "to": "catalog", "label": "declare", "variant": "dashed", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "b2", "from": "catalog", "to": "assemble", "label": "resolve", "variant": "emphasis"},
       {"id": "b3", "from": "assemble", "to": "apk", "label": "package + sign", "variant": "emphasis"},
       {"id": "b4", "from": "apk", "to": "blocked", "label": "desktop eq.", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "Verified Android stages",
            "Gradle Kotlin DSL with a version catalog",
            "Unit tests and instrumented tests are separate tasks",
            "Release signing is configured in Gradle, not in repository CI"),
       card("rose", "Desktop is blocked",
            "No go.mod, wails.json, or package.json exists",
            "No packaging, signing, or update feed is configured",
            "This diagram must not be read as a desktop release plan"),
   ])

wf("activity-vaccination-record",
   "Activity — Record a Vaccination",
   "[ANDROID-SOURCE] Verified flow from ClinicalVaccinationService.recordVaccination. Desktop implementation does not exist.",
   "screen", "clinical-write", "rejection",
   [{"id": "form", "col": 0, "type": "external", "label": "Vacc Form", "sublabel": "items + next dose"}],
   [
       {"id": "valid", "col": 0, "type": "backend", "label": "Validate Rows", "sublabel": "vaccine + batch"},
       {"id": "tx", "col": 2, "type": "database", "label": "One TX", "sublabel": "visit + items + income", "tag": "atomic"},
       {"id": "stock", "col": 4, "type": "backend", "label": "Deduct Stock", "sublabel": "FEFO + ledger"},
   ],
   [
       {"id": "bad", "col": 0, "type": "security", "label": "Rejected", "sublabel": "no write"},
       {"id": "short", "col": 4, "type": "security", "label": "Shortfall", "sublabel": "FAILED ledger"},
   ],
   [
       {"id": "v1", "from": "form", "to": "valid", "label": "save", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "v2", "from": "valid", "to": "tx", "label": "rows ok", "variant": "emphasis"},
       {"id": "v3", "from": "tx", "to": "stock", "label": "per item"},
       {"id": "v4", "from": "valid", "to": "bad", "label": "missing", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "v5", "from": "stock", "to": "short", "label": "insufficient", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "One transaction",
            "Visit, items, income, stock deduction, and reminders share one tx",
            "The record lands whole or not at all",
            "The sync queue is written inside the same transaction"),
       card("amber", "Stock shortfall",
            "An insufficient batch writes a FAILED ledger row instead of throwing",
            "The visit still commits with a PARTIAL or FAILED inventory status",
            "Stock is never silently driven negative"),
       card("rose", "Risks carried forward",
            "No idempotency key on stock deduction",
            "The save button has no ViewModel in-flight guard",
            "Receipt number is assigned server side, after commit"),
   ])

wf("activity-inventory-decrement",
   "Activity — Inventory Decrement and Reconciliation",
   "[ANDROID-SOURCE] Verified FEFO decrement with reconciliation ledger. Duplicate-event risk is documented, not resolved.",
   "request", "batch-selection", "refusal",
   [{"id": "req", "col": 0, "type": "external", "label": "Deduct Request", "sublabel": "batch + quantity"}],
   [
       {"id": "load", "col": 0, "type": "backend", "label": "Load Batch", "sublabel": "by batchId"},
       {"id": "expiry", "col": 2, "type": "backend", "label": "Expiry Gate", "sublabel": "vs given date", "tag": "allowExpired"},
       {"id": "enough", "col": 4, "type": "backend", "label": "Sufficient?", "sublabel": "remaining >= qty"},
   ],
   [
       {"id": "noBatch", "col": 0, "type": "security", "label": "Blocked", "sublabel": "batch missing"},
       {"id": "expired", "col": 2, "type": "security", "label": "Expired", "sublabel": "refused"},
       {"id": "short", "col": 4, "type": "security", "label": "Insufficient", "sublabel": "throws"},
   ],
   [
       {"id": "i1", "from": "req", "to": "load", "label": "load", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "i2", "from": "load", "to": "expiry", "label": "found", "variant": "emphasis"},
       {"id": "i3", "from": "expiry", "to": "enough", "label": "not expired", "variant": "emphasis"},
       {"id": "i4", "from": "load", "to": "noBatch", "label": "null", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "i5", "from": "expiry", "to": "expired", "label": "expired", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "i6", "from": "enough", "to": "short", "label": "no", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "FEFO order",
            "Batches are consumed soonest-expiry-first",
            "Expired batches are refused unless already used",
            "Remaining quantity is read-modify-write inside the tx"),
       card("rose", "Duplicate-event risk",
            "sync_queue has no unique constraint on entity + operation",
            "Concurrent enqueues can still produce duplicate rows",
            "reverseDeduction has no idempotency key by design"),
       card("amber", "Reconciliation",
            "Every movement writes an inventory_transactions row",
            "inventory_deductions records COMPLETED or FAILED per visit",
            "Stock can be reversed only from COMPLETED ledger rows"),
   ])

wf("activity-borrow-return",
   "Activity — Borrow, Partial Return, Full Return",
   "[ANDROID-SOURCE] Verified borrow lifecycle. Status is derived at read time from the sum of return rows, not stored.",
   "action", "validation", "rejection",
   [{"id": "choose", "col": 0, "type": "external", "label": "Choose Action", "sublabel": "borrow or return"}],
   [
       {"id": "batch", "col": 0, "type": "backend", "label": "Pick Batch", "sublabel": "single unexpired"},
       {"id": "cap", "col": 2, "type": "backend", "label": "Within Cap?", "sublabel": "outstanding guard"},
       {"id": "derive", "col": 4, "type": "backend", "label": "Derive Status", "sublabel": "sum of returns"},
   ],
   [
       {"id": "nobatch", "col": 0, "type": "security", "label": "No Batch", "sublabel": "insufficient"},
       {"id": "over", "col": 2, "type": "security", "label": "Over Return", "sublabel": "rejected"},
   ],
   [
       {"id": "n1", "from": "choose", "to": "batch", "label": "borrow", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "n2", "from": "batch", "to": "cap", "label": "record + deduct"},
       {"id": "n3", "from": "cap", "to": "derive", "label": "restored", "variant": "emphasis"},
       {"id": "n4", "from": "batch", "to": "nobatch", "label": "none fit", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "n5", "from": "cap", "to": "over", "label": "exceeds", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "Derived status",
            "BORROWED when nothing is returned",
            "PARTIALLY_RETURNED when some but not all is returned",
            "RETURNED when the sum meets the borrowed quantity"),
       card("rose", "Transaction boundaries",
            "Borrow, return, and delete each run in one transaction",
            "Cross-batch return writes a zero-quantity release row",
            "Deleting a record restores outstanding stock first"),
       card("amber", "Guard rails",
            "A return may not exceed the outstanding quantity",
            "A borrow must fit in a single unexpired batch",
            "No idempotency key exists on the return path"),
   ])

wf("activity-patient-create",
   "Activity — Create a Patient",
   "[ANDROID-SOURCE] Verified patient creation with clinic-id generation inside the transaction. Desktop equivalent is planned only.",
   "form", "identity", "rejection",
   [{"id": "fill", "col": 0, "type": "external", "label": "Patient Form", "sublabel": "name + dob"}],
   [
       {"id": "check", "col": 0, "type": "backend", "label": "Required Check", "sublabel": "name + dob"},
       {"id": "tx", "col": 2, "type": "database", "label": "One TX", "sublabel": "id + insert + audit", "tag": "atomic"},
       {"id": "uniq", "col": 4, "type": "backend", "label": "Unique ID?", "sublabel": "index check"},
   ],
   [
       {"id": "missing", "col": 0, "type": "security", "label": "Missing Field", "sublabel": "blocked"},
       {"id": "dupe", "col": 4, "type": "security", "label": "Duplicate ID", "sublabel": "aborts"},
   ],
   [
       {"id": "q1", "from": "fill", "to": "check", "label": "save", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "q2", "from": "check", "to": "tx", "label": "complete", "variant": "emphasis"},
       {"id": "q3", "from": "tx", "to": "uniq", "label": "probe"},
       {"id": "q4", "from": "check", "to": "missing", "label": "blank", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "q5", "from": "uniq", "to": "dupe", "label": "collision", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "Atomic",
            "Clinic-id generation, uniqueness check, insert, and enqueue share one tx",
            "The audit row is written inside the same transaction",
            "A conflict aborts before any row is durable"),
       card("rose", "Open questions",
            "Remote soft-delete vs local hard-delete semantics",
            "Clinic-id collision handling when two devices assign offline",
            "Whether desktop should keep the TEMP- prefix convention"),
   ])

wf("activity-consultation-record",
   "Activity — Record a Consultation",
   "[ANDROID-SOURCE] Verified consultation write with slot revalidation and an optional edit branch. Desktop equivalent is planned only.",
   "form", "availability", "rejection",
   [{"id": "fill", "col": 0, "type": "external", "label": "Consult Form", "sublabel": "problem + fee"}],
   [
       {"id": "req", "col": 0, "type": "backend", "label": "Required Check", "sublabel": "doctor + slot"},
       {"id": "recheck", "col": 2, "type": "backend", "label": "Slot Free?", "sublabel": "revalidate now"},
       {"id": "tx", "col": 4, "type": "database", "label": "Transaction", "sublabel": "visit + consult + fee"},
   ],
   [
       {"id": "stale", "col": 2, "type": "security", "label": "Slot Taken", "sublabel": "reload slots"},
       {"id": "nochange", "col": 4, "type": "security", "label": "No Changes", "sublabel": "NO_CHANGES"},
   ],
   [
       {"id": "w1", "from": "fill", "to": "req", "label": "save", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "w2", "from": "req", "to": "recheck", "label": "complete", "variant": "emphasis"},
       {"id": "w3", "from": "recheck", "to": "tx", "label": "available", "variant": "emphasis"},
       {"id": "w4", "from": "recheck", "to": "stale", "label": "taken", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "w5", "from": "tx", "to": "nochange", "label": "identical edit", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "Slot revalidation",
            "The chosen slot is re-checked immediately before the write",
            "A stale slot clears the selection and reloads availability",
            "No consultation row is written for a lost slot"),
       card("amber", "Edit branch",
            "An edit with no changed field reports NO_CHANGES and writes nothing",
            "A changed fee updates the linked finance row in the same tx",
            "The consultation is identified by a marker in remarks"),
       card("rose", "Unproven",
            "Doctor availability data is export-reported only",
            "Concurrent double-booking across devices is untested"),
   ])

wf("activity-batch-expiry",
   "Activity — Batch Selection and Expiry Handling",
   "[ANDROID-SOURCE] Verified FEFO selection and expiry rules in the clinic timezone. Expiry is enforced at both UI and repository.",
   "selection", "expiry-rules", "refusal",
   [{"id": "vaccine", "col": 0, "type": "external", "label": "Choose Vaccine", "sublabel": "row on form"}],
   [
       {"id": "stocked", "col": 0, "type": "backend", "label": "In-Stock Lots", "sublabel": "remaining > 0"},
       {"id": "filter", "col": 2, "type": "backend", "label": "Expired As Of?", "sublabel": "vs given date"},
       {"id": "revalidate", "col": 4, "type": "security", "label": "Write Gate", "sublabel": "allowExpired"},
   ],
   [
       {"id": "empty", "col": 0, "type": "security", "label": "No Usable Lot", "sublabel": "blocked"},
       {"id": "block", "col": 4, "type": "security", "label": "Blocked", "sublabel": "expired on date"},
   ],
   [
       {"id": "y1", "from": "vaccine", "to": "stocked", "label": "load", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "y2", "from": "stocked", "to": "filter", "label": "candidates", "variant": "emphasis"},
       {"id": "y3", "from": "filter", "to": "revalidate", "label": "soonest first", "variant": "emphasis"},
       {"id": "y4", "from": "stocked", "to": "empty", "label": "none", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "y5", "from": "revalidate", "to": "block", "label": "expired", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "FEFO",
            "Best batch = soonest expiry among unexpired, in-stock batches",
            "The repository repeats the same filter on write",
            "The UI dropdown and the write path agree on the rule"),
       card("amber", "Edge cases",
            "An unparseable expiry is deliberately treated as not expired",
            "An edit may keep a batch that was already consumed",
            "A same-day expiry is not yet expired"),
       card("rose", "Not verified",
            "Exported expiry formats were not parsed against live data",
            "Timezone handling across devices is untested"),
   ])

wf("activity-due-reminders",
   "Activity — Due Vaccinations and Reminders",
   "[ANDROID-SOURCE] Verified reminder pipeline. Due dates are entered by staff; no interval arithmetic exists in the codebase.",
   "write-path", "due-list", "dropped",
   [{"id": "spec", "col": 0, "type": "external", "label": "Next Dose", "sublabel": "type + due date"}],
   [
       {"id": "guard", "col": 0, "type": "backend", "label": "Complete?", "sublabel": "type and date"},
       {"id": "classify", "col": 2, "type": "backend", "label": "Classify", "sublabel": "overdue / today"},
       {"id": "summary", "col": 4, "type": "messagebus", "label": "Daily Summary", "sublabel": "hourly worker"},
   ],
   [
       {"id": "dismissed", "col": 0, "type": "security", "label": "Dropped", "sublabel": "logged, no row"},
   ],
   [
       {"id": "z1", "from": "spec", "to": "guard", "label": "submit", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "z2", "from": "guard", "to": "classify", "label": "save + group", "variant": "emphasis"},
       {"id": "z3", "from": "classify", "to": "summary", "label": "due or overdue"},
       {"id": "z4", "from": "guard", "to": "dismissed", "label": "blank field", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("amber", "Dates are entered, not computed",
            "No plusWeeks or schedule arithmetic exists under reminder or vaccination",
            "A blank type or due date drops the reminder with a log line",
            "Reschedule assigns a new date directly"),
       card("emerald", "Classification",
            "Overdue, today, tomorrow, and future are derived at read time",
            "The due list groups active reminders by patient and date",
            "A unique index prevents duplicate reminder rows"),
       card("rose", "Notification limits",
            "Only a daily summary and a 24-hour personal worker are scheduled",
            "There is no per-reminder exact-time scheduler",
            "Desktop notification behavior is undesigned"),
   ])

wf("activity-dashboard-stats",
   "Activity — Dashboard Statistics and Filtering",
   "[ANDROID-SOURCE] Verified local-first aggregation. No dashboard query reaches the network directly.",
   "local-sources", "presentation", "refresh",
   [{"id": "rooms", "col": 0, "type": "database", "label": "Room Flows", "sublabel": "patients visits stock"}],
   [
       {"id": "combine", "col": 0, "type": "backend", "label": "Combine", "sublabel": "reactive join"},
       {"id": "tiles", "col": 2, "type": "frontend", "label": "Tiles", "sublabel": "counts + charts"},
       {"id": "refine", "col": 4, "type": "frontend", "label": "Refined View", "sublabel": "filtered"},
   ],
   [
       {"id": "pull", "col": 2, "type": "cloud", "label": "Pull Remote", "sublabel": "push then pull"},
   ],
   [
       {"id": "s1", "from": "rooms", "to": "combine", "label": "flows", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "s2", "from": "combine", "to": "tiles", "label": "state", "variant": "emphasis"},
       {"id": "s3", "from": "tiles", "to": "refine", "label": "user filter", "variant": "emphasis"},
       {"id": "s4", "from": "tiles", "to": "pull", "label": "refresh", "variant": "dashed", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "Local only",
            "Every tile is a Room flow, never a live remote query",
            "A filter failure degrades to an empty filter, never a broken list",
            "Statistics recompute reactively as rows change"),
       card("amber", "Refresh",
            "Refresh pushes pending items first, then pulls",
            "A single-flight guard prevents overlapping refreshes",
            "Realtime changes are debounced before they trigger a pull"),
       card("rose", "Desktop gap",
            "No desktop dashboard exists",
            "Which tiles belong on the desktop dashboard is unresolved",
            "Exported statistics functions are anon-executable"),
   ])

wf("activity-staff-roles",
   "Activity — Staff and Role Management",
   "[ANDROID-SOURCE] Verified client-side role gating. The real boundary is the manage-staff Edge Function and RLS, both export-reported.",
   "admin-ui", "client-gate", "denial",
   [{"id": "action", "col": 0, "type": "external", "label": "Admin Action", "sublabel": "create / reset / role"}],
   [
       {"id": "rolecheck", "col": 0, "type": "security", "label": "Role Claim", "sublabel": "admin only", "tag": "UX only"},
       {"id": "guardwrap", "col": 2, "type": "security", "label": "AdminGuard", "sublabel": "route wrapper"},
       {"id": "invoke", "col": 4, "type": "backend", "label": "manage-staff", "sublabel": "Edge Function"},
   ],
   [
       {"id": "access", "col": 0, "type": "security", "label": "Access Denied", "sublabel": "screen"},
   ],
   [
       {"id": "m1", "from": "action", "to": "rolecheck", "label": "submit", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "m2", "from": "rolecheck", "to": "guardwrap", "label": "is admin", "variant": "emphasis"},
       {"id": "m3", "from": "guardwrap", "to": "invoke", "label": "invoke", "variant": "security"},
       {"id": "m4", "from": "rolecheck", "to": "access", "label": "not admin", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "Client gating is UX only",
            "AdminGuard wraps the staff routes in the navigation graph",
            "The drawer hides non-admin entries by role",
            "Comments state the server is the real boundary"),
       card("rose", "Export-reported",
            "All staff writes route through the manage-staff Edge Function",
            "No PostgREST or local write exists in the staff repository",
            "Function authorization has not been observed [UNKNOWN]"),
   ])

wf("activity-backup-restore",
   "Activity — Backup and Restore",
   "[ANDROID-SOURCE] Verified Android backup/restore with a staged safety snapshot. The desktop has no backup design; ADR-0010 is pending.",
   "trigger", "seal", "failure",
   [{"id": "trigger", "col": 0, "type": "external", "label": "Backup Request", "sublabel": "manual or scheduled"}],
   [
       {"id": "collect", "col": 0, "type": "database", "label": "Snapshot", "sublabel": "22 tables, one tx"},
       {"id": "seal", "col": 2, "type": "security", "label": "Encrypt + Hash", "sublabel": "AES-256-GCM"},
       {"id": "stage", "col": 4, "type": "database", "label": "Stage Safety", "sublabel": "pre-restore"},
   ],
   [
       {"id": "corrupt", "col": 2, "type": "security", "label": "Bad Checksum", "sublabel": "refuse"},
       {"id": "staging", "col": 4, "type": "security", "label": "Staging Fail", "sublabel": "abort restore"},
   ],
   [
       {"id": "k1", "from": "trigger", "to": "collect", "label": "start", "variant": "emphasis", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "k2", "from": "collect", "to": "seal", "label": "payload", "variant": "emphasis"},
       {"id": "k3", "from": "seal", "to": "stage", "label": "sealed", "variant": "emphasis"},
       {"id": "k4", "from": "seal", "to": "corrupt", "label": "verify fail", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
       {"id": "k5", "from": "stage", "to": "staging", "label": "cannot stage", "variant": "security", "fromSide": "bottom", "toSide": "top", "route": "drop"},
   ],
   [
       card("emerald", "Fail closed",
            "A safety snapshot is staged before any restore write",
            "If staging fails, the restore aborts before touching data",
            "The restore itself is one transaction; a throw rolls it back"),
       card("cyan", "Encryption",
            "Backups use password-based AES-256-GCM with PBKDF2",
            "The container is independent of the local database passphrase",
            "A checksum is verified before the payload is trusted"),
       card("rose", "Desktop",
            "No desktop backup format, target, or retention is designed",
            "ADR-0010 covers encrypted backup and restore safety and is pending"),
   ])

# ==========================================================================
# SEQUENCES
# ==========================================================================

seq("sequence-login-session",
    "Sequence — Login and Session Restoration",
    "[ANDROID-SOURCE] Verified Android login and startup restore. Desktop must reproduce the contract, not the class names.",
    [
        {"id": "user", "type": "external", "label": "Staff User", "sublabel": "email + password"},
        {"id": "ui", "type": "frontend", "label": "Login Screen", "sublabel": "form"},
        {"id": "authvm", "type": "backend", "label": "Auth Ctrl", "sublabel": "client logic"},
        {"id": "supaauth", "type": "security", "label": "Supa Auth", "sublabel": "issues JWT"},
        {"id": "profiles", "type": "database", "label": "profiles", "sublabel": "role + active"},
        {"id": "session", "type": "database", "label": "Session", "sublabel": "encrypted prefs"},
        {"id": "nav", "type": "frontend", "label": "Navigator", "sublabel": "start dest"},
    ],
    [
        {"from": "user", "to": "ui", "y": 180, "label": "enter credentials", "variant": "emphasis"},
        {"from": "ui", "to": "authvm", "y": 222, "label": "login(email, password)"},
        {"from": "authvm", "to": "supaauth", "y": 264, "label": "sign in", "variant": "security"},
        {"from": "supaauth", "to": "session", "y": 306, "label": "persist session", "variant": "dashed"},
        {"from": "supaauth", "to": "authvm", "y": 348, "label": "uid + JWT", "variant": "return"},
        {"from": "authvm", "to": "profiles", "y": 390, "label": "load profile"},
        {"from": "profiles", "to": "authvm", "y": 432, "label": "role, is_active", "variant": "return"},
        {"from": "authvm", "to": "nav", "y": 516, "label": "onLoginSuccess()", "variant": "emphasis"},
        {"from": "nav", "to": "session", "y": 566, "label": "restore on start", "variant": "dashed"},
        {"from": "session", "to": "authvm", "y": 608, "label": "resolved or null", "variant": "return"},
        {"from": "authvm", "to": "nav", "y": 650, "label": "dash or login", "variant": "emphasis"},
    ],
    [
        card("emerald", "Bounded startup",
             "Session resolution is awaited with a hard timeout",
             "A resolved session routes to the dashboard; otherwise to login",
             "An unresolved session with a cached user still opens the dashboard"),
        card("amber", "Account isolation",
             "Signing into a different account clears local data first",
             "The switch is blocked while unacknowledged sync items remain",
             "Sign-out is blocked for the same reason"),
        card("rose", "Authorization",
             "The role is read from the JWT app_metadata claim",
             "A disabled account is rejected after the profile loads",
             "Local profile role is display-only, never an authz source"),
    ])

seq("sequence-vaccination-write",
    "Sequence — Vaccination Write and Receipt Number",
    "[ANDROID-SOURCE + SCHEMA-EXPORT] Local commit, queued sync, then a server-assigned receipt number read back into the local row.",
    [
        {"id": "screen", "type": "frontend", "label": "Vacc Screen", "sublabel": "form"},
        {"id": "svc", "type": "backend", "label": "Clinical Svc", "sublabel": "orchestrates"},
        {"id": "db", "type": "database", "label": "Local DB", "sublabel": "Room"},
        {"id": "queue", "type": "messagebus", "label": "Sync Queue", "sublabel": "PENDING"},
        {"id": "worker", "type": "backend", "label": "Sync Worker", "sublabel": "upload"},
        {"id": "supa", "type": "cloud", "label": "Supabase", "sublabel": "PostgREST"},
        {"id": "trig", "type": "security", "label": "Trg Assign", "sublabel": "receipt no."},
    ],
    [
        {"from": "screen", "to": "svc", "y": 180, "label": "recordVaccination()", "variant": "emphasis"},
        {"from": "svc", "to": "db", "y": 222, "label": "BEGIN one tx", "variant": "emphasis"},
        {"from": "db", "to": "queue", "y": 348, "label": "enqueue VISIT/TXN", "variant": "dashed"},
        {"from": "db", "to": "svc", "y": 390, "label": "COMMIT", "variant": "return"},
        {"from": "svc", "to": "screen", "y": 432, "label": "saved (blank rcpt)", "variant": "return"},
        {"from": "worker", "to": "queue", "y": 482, "label": "drain by priority"},
        {"from": "worker", "to": "supa", "y": 524, "label": "upsert visit", "variant": "security"},
        {"from": "supa", "to": "trig", "y": 566, "label": "BEFORE INSERT", "variant": "security"},
        {"from": "trig", "to": "supa", "y": 608, "label": "NEO-26/27-0001", "variant": "return"},
        {"from": "supa", "to": "worker", "y": 650, "label": "return saved row", "variant": "return"},
        {"from": "worker", "to": "db", "y": 692, "label": "store receipt no.", "variant": "emphasis"},
        {"from": "worker", "to": "queue", "y": 734, "label": "delete queue row"},
    ],
    [
        card("emerald", "Local commit first",
             "The visit, items, income, and stock move in one local transaction",
             "The queue row is written inside that same transaction",
             "The user is never blocked on the network"),
        card("cyan", "Server-assigned identity",
             "The client uploads a blank receipt number",
             "A database trigger assigns NEO-FY-NNNNNN on insert",
             "The upsert reads the row back and stores the number locally"),
        card("rose", "Export-reported",
             "The receipt function is exposed to anon in the export",
             "The counter table is locked and revoked, per the export",
             "Trigger behavior has not been exercised live [UNKNOWN]"),
    ])

seq("sequence-sync-push-pull",
    "Sequence — Sync Push, Conflict, and Pull",
    "[ANDROID-SOURCE] Verified last-write-wins reconciliation with a single-flight guard and bounded retry.",
    [
        {"id": "recon", "type": "backend", "label": "Reconciler", "sublabel": "network aware"},
        {"id": "repo", "type": "backend", "label": "Sync Repo", "sublabel": "orchestrates"},
        {"id": "queue", "type": "database", "label": "sync_queue", "sublabel": "PENDING rows"},
        {"id": "up", "type": "backend", "label": "Uploader", "sublabel": "per entity"},
        {"id": "supa", "type": "cloud", "label": "Supabase", "sublabel": "PostgREST"},
        {"id": "db", "type": "database", "label": "Local DB", "sublabel": "merge target"},
    ],
    [
        {"from": "recon", "to": "repo", "y": 180, "label": "processNextItems()", "variant": "emphasis"},
        {"from": "repo", "to": "queue", "y": 222, "label": "read PENDING"},
        {"from": "queue", "to": "repo", "y": 264, "label": "group by txId", "variant": "return"},
        {"from": "repo", "to": "up", "y": 306, "label": "mark SYNCING"},
        {"from": "up", "to": "supa", "y": 348, "label": "fetch conflicts", "variant": "dashed"},
        {"from": "up", "to": "db", "y": 390, "label": "self-heal older", "variant": "dashed"},
        {"from": "up", "to": "supa", "y": 432, "label": "upsert / delete", "variant": "security"},
        {"from": "supa", "to": "up", "y": 474, "label": "2xx / 401 / 5xx", "variant": "return"},
        {"from": "up", "to": "repo", "y": 516, "label": "GroupResult", "variant": "return"},
        {"from": "repo", "to": "queue", "y": 558, "label": "retry<5? requeue"},
        {"from": "recon", "to": "repo", "y": 648, "label": "then pull inbound", "variant": "emphasis"},
        {"from": "repo", "to": "db", "y": 690, "label": "upsert merged"},
    ],
    [
        card("emerald", "Outbound first",
             "Pending items are grouped by transactionGroupId and pushed",
             "DELETE operations run at negative priority",
             "Stale SYNCING rows are requeued after five minutes"),
        card("amber", "Conflict rule",
             "A newer remote row is copied back into the local store",
             "The guard skips entities that still have pending local edits",
             "No version column exists; the rule is timestamp only"),
        card("rose", "Retry budget",
             "Transient faults retry up to five times, then fail permanently",
             "Authorization and schema faults never retry",
             "One session refresh is attempted on a 401"),
    ])

seq("sequence-receipt-numbering",
    "Sequence — Financial Transaction and Receipt Numbering",
    "[SCHEMA-EXPORT] Server-side receipt assignment and counter locking, reported by exports. The Android client uploads a blank number.",
    [
        {"id": "client", "type": "frontend", "label": "Client", "sublabel": "blank number"},
        {"id": "postgrest", "type": "cloud", "label": "PostgREST", "sublabel": "upsert"},
        {"id": "trig", "type": "security", "label": "Trg Assign", "sublabel": "BEFORE INS"},
        {"id": "fn", "type": "security", "label": "Rcpt Func", "sublabel": "SECURITY DEFINER"},
        {"id": "counter", "type": "database", "label": "Rcpt Seq", "sublabel": "row-locked"},
    ],
    [
        {"from": "client", "to": "postgrest", "y": 185, "label": "upsert, rcpt = ''", "variant": "emphasis"},
        {"from": "postgrest", "to": "trig", "y": 232, "label": "row insert", "variant": "security"},
        {"from": "trig", "to": "fn", "y": 279, "label": "call + visit date", "variant": "security"},
        {"from": "fn", "to": "counter", "y": 373, "label": "ON CONFLICT UPDATE", "variant": "emphasis"},
        {"from": "counter", "to": "fn", "y": 420, "label": "locked next value", "variant": "return"},
        {"from": "fn", "to": "trig", "y": 467, "label": "NEO-26/27-000042", "variant": "return"},
        {"from": "trig", "to": "postgrest", "y": 514, "label": "number on row", "variant": "return"},
        {"from": "postgrest", "to": "client", "y": 561, "label": "saved row", "variant": "return"},
    ],
    [
        card("cyan", "Assigned on the server",
             "A BEFORE INSERT OR UPDATE trigger assigns the number",
             "Format is NEO-<financial year>-<six digits>",
             "The financial year runs 1 April to 31 March from the visit date"),
        card("emerald", "Counter safety",
             "The counter row is incremented with ON CONFLICT DO UPDATE",
             "That pattern locks the row and closes the read-then-write gap",
             "The counter table is revoked from authenticated and anon"),
        card("rose", "Unknown",
             "Whether the trigger runs on the live project is unverified",
             "Concurrent assignment under load has not been measured"),
    ])

seq("sequence-borrow-return",
    "Sequence — Partial and Full Vaccine Return",
    "[ANDROID-SOURCE] Verified return path with an outstanding-quantity cap and a derived final status.",
    [
        {"id": "ui", "type": "frontend", "label": "Return Dialog", "sublabel": "qty + batch"},
        {"id": "vm", "type": "backend", "label": "Borrowed VM", "sublabel": "revalidates"},
        {"id": "repo", "type": "backend", "label": "Borrow Repo", "sublabel": "tx owner"},
        {"id": "db", "type": "database", "label": "Local DB", "sublabel": "borrow tables"},
        {"id": "queue", "type": "messagebus", "label": "Sync Queue", "sublabel": "enqueued"},
    ],
    [
        {"from": "ui", "to": "vm", "y": 185, "label": "submitReturn(qty)", "variant": "emphasis"},
        {"from": "vm", "to": "repo", "y": 271, "label": "submitReturn()", "variant": "emphasis"},
        {"from": "repo", "to": "db", "y": 314, "label": "BEGIN tx", "variant": "emphasis"},
        {"from": "db", "to": "repo", "y": 357, "label": "record + sum", "variant": "return"},
        {"from": "repo", "to": "db", "y": 443, "label": "restore stock", "variant": "emphasis"},
        {"from": "repo", "to": "db", "y": 486, "label": "insert return row"},
        {"from": "db", "to": "repo", "y": 572, "label": "COMMIT", "variant": "return"},
        {"from": "repo", "to": "queue", "y": 615, "label": "enqueue RETURN", "variant": "dashed"},
    ],
    [
        card("emerald", "Cap before write",
             "The outstanding quantity is computed before anything is written",
             "A return above the cap throws and nothing persists",
             "Status is derived from the sum of return rows, not stored"),
        card("rose", "Cross-batch",
             "A return into a new batch writes a release row on the original",
             "Stock is restored on the target batch in the same transaction",
             "No idempotency key exists on the return path"),
    ])

seq("sequence-backup-restore",
    "Sequence — Backup Export and Safe Restore",
    "[ANDROID-SOURCE] Verified Android export and restore with a staged safety snapshot and a single restore transaction.",
    [
        {"id": "ui", "type": "frontend", "label": "Backup UI", "sublabel": "settings"},
        {"id": "repo", "type": "backend", "label": "Backup Repo", "sublabel": "orchestrates"},
        {"id": "collector", "type": "database", "label": "Collector", "sublabel": "read snapshot"},
        {"id": "db", "type": "database", "label": "Local DB", "sublabel": "22 tables"},
        {"id": "crypto", "type": "security", "label": "Crypto", "sublabel": "AES-256-GCM"},
        {"id": "safety", "type": "security", "label": "Safety Store", "sublabel": "Keystore key"},
    ],
    [
        {"from": "ui", "to": "repo", "y": 180, "label": "exportBackup()", "variant": "emphasis"},
        {"from": "repo", "to": "collector", "y": 222, "label": "collect()"},
        {"from": "collector", "to": "db", "y": 264, "label": "BEGIN read tx", "variant": "emphasis"},
        {"from": "db", "to": "collector", "y": 306, "label": "22 snapshots", "variant": "return"},
        {"from": "collector", "to": "repo", "y": 348, "label": "payload, tokens off", "variant": "return"},
        {"from": "repo", "to": "crypto", "y": 390, "label": "seal + checksum", "variant": "security"},
        {"from": "crypto", "to": "ui", "y": 432, "label": ".nccb written", "variant": "return"},
        {"from": "ui", "to": "repo", "y": 482, "label": "restoreBackup()", "variant": "emphasis"},
        {"from": "repo", "to": "crypto", "y": 524, "label": "verify checksum", "variant": "security"},
        {"from": "repo", "to": "safety", "y": 566, "label": "stage snapshot", "variant": "emphasis"},
        {"from": "safety", "to": "repo", "y": 608, "label": "staged or FAILED", "variant": "return"},
        {"from": "repo", "to": "db", "y": 650, "label": "BEGIN restore tx", "variant": "emphasis"},
        {"from": "db", "to": "repo", "y": 692, "label": "COMMIT or rollback", "variant": "return"},
    ],
    [
        card("emerald", "Read is atomic",
             "Every table is collected inside one read transaction",
             "The envelope carries version, checksum, and record counts",
             "Profiles are stripped of device tokens before export"),
        card("rose", "Restore fails closed",
             "A safety snapshot is staged before any write",
             "Staging failure aborts the restore entirely",
             "The restore is one transaction; a throw rolls it back"),
    ])

seq("sequence-dashboard-refresh",
    "Sequence — Dashboard Refresh and Realtime Trigger",
    "[ANDROID-SOURCE] Verified pull-then-render refresh with a single-flight guard and debounced realtime hints.",
    [
        {"id": "ui", "type": "frontend", "label": "Dashboard", "sublabel": "tiles"},
        {"id": "vm", "type": "backend", "label": "Dash VM", "sublabel": "guards refresh"},
        {"id": "repo", "type": "backend", "label": "Sync + Ref", "sublabel": "push then pull"},
        {"id": "supa", "type": "cloud", "label": "Supabase", "sublabel": "tables"},
        {"id": "rt", "type": "messagebus", "label": "Realtime", "sublabel": "change hints"},
    ],
    [
        {"from": "ui", "to": "vm", "y": 185, "label": "refresh()", "variant": "emphasis"},
        {"from": "vm", "to": "repo", "y": 271, "label": "push pending first", "variant": "emphasis"},
        {"from": "repo", "to": "supa", "y": 314, "label": "push groups", "variant": "security"},
        {"from": "repo", "to": "supa", "y": 357, "label": "pull changed", "variant": "emphasis"},
        {"from": "supa", "to": "vm", "y": 400, "label": "rows or failure", "variant": "return"},
        {"from": "vm", "to": "ui", "y": 443, "label": "tiles or banner", "variant": "return"},
        {"from": "rt", "to": "vm", "y": 500, "label": "change, debounced", "variant": "dashed"},
        {"from": "vm", "to": "repo", "y": 543, "label": "pull only", "variant": "dashed"},
    ],
    [
        card("emerald", "Single flight",
             "An overlapping refresh returns immediately",
             "Outbound push runs before the inbound pull",
             "Realtime hints are debounced and only trigger a pull"),
        card("rose", "Unknown",
             "Realtime authorization has not been exercised live",
             "Whether the desktop will subscribe to Realtime is undecided"),
    ])

# ==========================================================================
# LIFECYCLE (lane main = phase band, lane terminal = outcome band)
# ==========================================================================

lc("state-sync-queue",
   "State Machine — Sync Queue Item",
   "[ANDROID-SOURCE] Verified SyncStatus enum and the transitions implemented in the sync repository.",
   [
       {"id": "pending", "type": "start", "label": "PENDING", "sublabel": "enqueued", "col": 0, "step": "01", "tag": "durable"},
       {"id": "syncing", "type": "active", "label": "SYNCING", "sublabel": "group in flight", "col": 1, "step": "02", "tag": "owned"},
       {"id": "requeue", "type": "waiting", "label": "Requeue", "sublabel": "retryCount + 1", "col": 3, "tag": "backoff"},
   ],
   [
       {"id": "synced", "type": "success", "label": "SYNCED", "sublabel": "acknowledged", "col": 0, "step": "03", "tag": "terminal"},
       {"id": "failed", "type": "failure", "label": "FAILED", "sublabel": "manual retry only", "col": 2, "tag": "terminal"},
   ],
   [
       {"from": "pending", "to": "syncing", "label": "dequeue", "variant": "emphasis"},
       {"from": "syncing", "to": "requeue", "label": "5xx, retry < 5", "variant": "security", "route": "drop", "labelDy": 58},
       {"from": "requeue", "to": "pending", "label": "backoff elapsed", "variant": "dashed", "route": "bottom-channel", "labelDy": 40},
       {"from": "syncing", "to": "synced", "label": "2xx", "variant": "emphasis", "route": "drop", "labelDy": 58},
       {"from": "syncing", "to": "failed", "label": "budget spent", "variant": "security", "route": "drop", "labelDy": 58},
   ],
   [
       card("emerald", "Four states",
            "PENDING on enqueue",
            "SYNCING while a group is in flight",
            "SYNCED after the server acknowledges",
            "FAILED after the retry budget is exhausted"),
       card("amber", "Recovery",
            "Transient faults return the item to PENDING with a higher retryCount",
            "Stale SYNCING rows are requeued after five minutes",
            "A session deferral returns items to PENDING without counting a failure"),
       card("rose", "Risk",
            "No unique constraint covers entity plus operation",
            "Duplicate rows are cleaned opportunistically, not prevented"),
   ],
   "Sync progression", "Outcome")

lc("state-reminder",
   "State Machine — Vaccination Reminder",
   "[ANDROID-SOURCE] Verified ReminderStatus enum with a unique index that prevents duplicate rows.",
   [
       {"id": "active", "type": "start", "label": "ACTIVE", "sublabel": "due list", "col": 0, "step": "01", "tag": "open"},
       {"id": "dismissed", "type": "failure", "label": "DISMISSED", "sublabel": "declined, reversible", "col": 2, "tag": "reversible"},
   ],
   [
       {"id": "completed", "type": "success", "label": "COMPLETED", "sublabel": "dose given", "col": 0, "step": "02", "tag": "terminal"},
       {"id": "external", "type": "neutral", "label": "EXTERNAL", "sublabel": "given elsewhere", "col": 2, "tag": "terminal"},
   ],
   [
       {"from": "active", "to": "completed", "label": "mark complete", "variant": "emphasis", "route": "drop", "labelDy": 58},
       {"from": "active", "to": "dismissed", "label": "dismiss", "variant": "security"},
       {"from": "dismissed", "to": "active", "label": "restore", "variant": "dashed", "route": "bottom-channel", "labelDy": 40},
       {"from": "dismissed", "to": "external", "label": "given elsewhere", "variant": "default", "route": "drop", "labelDy": 58},
   ],
   [
       card("emerald", "Four states",
            "ACTIVE until acted on",
            "COMPLETED when the dose is given",
            "DISMISSED when staff declines",
            "EXTERNAL for doses given elsewhere"),
       card("rose", "Guard",
            "A unique index on patient, visit, due date, type, and name blocks duplicates",
            "Completion and dismissal each run in a transaction",
            "Restore returns a dismissed reminder to ACTIVE"),
   ],
   "Reminder path", "Outcome")

lc("state-personal-reminder",
   "State Machine — Personal Reminder",
   "[ANDROID-SOURCE] Verified PersonalReminderStatus enum and the documented flow PENDING to READY to COMPLETED.",
   [
       {"id": "pending", "type": "start", "label": "PENDING", "sublabel": "created", "col": 0, "step": "01", "tag": "default"},
       {"id": "ready", "type": "active", "label": "READY", "sublabel": "prepared", "col": 1, "step": "02", "tag": "active"},
       {"id": "cancelled", "type": "failure", "label": "CANCELLED", "sublabel": "called off", "col": 3, "tag": "terminal"},
   ],
   [
       {"id": "completed", "type": "success", "label": "COMPLETED", "sublabel": "done", "col": 0, "step": "03", "tag": "terminal"},
   ],
   [
       {"from": "pending", "to": "ready", "label": "mark ready", "variant": "emphasis"},
       {"from": "ready", "to": "completed", "label": "mark completed", "variant": "emphasis", "route": "drop", "labelDy": 58},
       {"from": "ready", "to": "cancelled", "label": "cancel", "variant": "security", "route": "drop", "labelDy": 58},
   ],
   [
       card("emerald", "Documented flow",
            "PENDING is the creation default",
            "READY marks a reminder as prepared",
            "COMPLETED is terminal for the happy path"),
       card("amber", "Side paths",
            "PENDING may go straight to CANCELLED",
            "READY may return to PENDING",
            "A cancelled reminder is not deleted"),
   ],
   "Happy path", "Outcome")

lc("state-borrow-record",
   "State Machine — Borrow Record",
   "[ANDROID-SOURCE] Verified derived status. The stored flag is boolean; the three states are computed from the sum of return rows.",
   [
       {"id": "borrowed", "type": "start", "label": "BORROWED", "sublabel": "stock deducted", "col": 0, "step": "01", "tag": "out"},
       {"id": "partial", "type": "active", "label": "PARTIALLY_RETURNED", "sublabel": "sum < quantity", "col": 2, "step": "02", "tag": "open"},
   ],
   [
       {"id": "returned", "type": "success", "label": "RETURNED", "sublabel": "sum == quantity", "col": 1, "step": "03", "tag": "terminal"},
   ],
   [
       {"from": "borrowed", "to": "partial", "label": "partial return", "variant": "emphasis"},
       {"from": "borrowed", "to": "returned", "label": "full return", "variant": "emphasis", "route": "drop", "labelDy": 58},
       {"from": "partial", "to": "returned", "label": "final return", "variant": "emphasis", "route": "drop", "labelDy": 58},
   ],
   [
       card("emerald", "Derived, not stored",
            "BORROWED when the returned sum is zero",
            "PARTIALLY_RETURNED when the sum is below the borrowed quantity",
            "RETURNED when the sum meets it"),
       card("rose", "Stock coupling",
            "Each return restores stock in the same transaction",
            "Deleting a record restores outstanding stock first",
            "The stored boolean is only a coarse read filter"),
   ],
   "Return progress", "Terminal")

lc("state-inventory-batch",
   "State Machine — Inventory Batch Lifecycle",
   "[ANDROID-SOURCE] Batch status is a single-value enum; stock movement is modeled as ledger events, not states.",
   [
       {"id": "created", "type": "start", "label": "Created", "sublabel": "purchase row", "col": 0, "step": "01", "tag": "full"},
       {"id": "depleting", "type": "active", "label": "Depleting", "sublabel": "FEFO draws", "col": 1, "step": "02", "tag": "active"},
       {"id": "blocked", "type": "failure", "label": "Deletion Blocked", "sublabel": "history exists", "col": 3, "tag": "guard"},
   ],
   [
       {"id": "exhausted", "type": "success", "label": "Exhausted", "sublabel": "remaining = 0", "col": 1, "step": "03", "tag": "terminal"},
   ],
   [
       {"from": "created", "to": "depleting", "label": "first deduction", "variant": "emphasis"},
       {"from": "depleting", "to": "exhausted", "label": "remaining hits 0", "variant": "emphasis", "route": "drop", "labelDy": 58},
       {"from": "depleting", "to": "blocked", "label": "delete attempt", "variant": "security", "route": "drop", "labelDy": 58},
   ],
   [
       card("emerald", "Status is minimal",
            "BatchStatus carries only ACTIVE",
            "Stock level is a quantity on the row, not a state",
            "Expiry is evaluated against a reference date, not stored"),
       card("rose", "Deletion guard",
            "A batch with historical rows cannot be deleted",
            "Guard covers vaccinations, waste, borrows, returns, and movements"),
   ],
   "Stock level", "Deletion")

lc("state-finance-record",
   "State Machine — Financial Transaction",
   "[ANDROID-SOURCE] Finance rows are append-only in practice; edits rewrite a single identified row rather than creating state.",
   [
       {"id": "recorded", "type": "start", "label": "Recorded", "sublabel": "income row", "col": 0, "step": "01", "tag": "immutable id"},
       {"id": "updated", "type": "active", "label": "Updated", "sublabel": "fee corrected", "col": 1, "step": "02", "tag": "same row"},
   ],
   [
       {"id": "reported", "type": "success", "label": "Reported", "sublabel": "in totals", "col": 1, "step": "03", "tag": "read"},
       {"id": "ambiguous", "type": "failure", "label": "Ambiguous Link", "sublabel": "throws", "col": 0, "tag": "fail closed"},
   ],
   [
       {"from": "recorded", "to": "updated", "label": "edit fee", "variant": "emphasis"},
       {"from": "updated", "to": "reported", "label": "in totals", "variant": "emphasis", "route": "drop", "labelDy": 58},
       {"from": "recorded", "to": "ambiguous", "label": "multiple matches", "variant": "security", "route": "drop", "labelDy": 58},
   ],
   [
       card("emerald", "Append-only",
            "An income row is created once per visit",
            "An edit updates the identified row and never deletes",
            "A deterministic id key makes concurrent creates collide safely"),
       card("rose", "Identification",
            "A marker in remarks links a row to its consultation",
            "An ambiguous match raises instead of guessing",
            "Receipt numbers are immutable once issued"),
   ],
   "Row lifecycle", "Ambiguity")

lc("state-session-readiness",
   "State Machine — Session Readiness During Sync",
   "[ANDROID-SOURCE] Verified internal SessionReadiness enum that gates whether a sync group may proceed.",
   [
       {"id": "usable", "type": "success", "label": "USABLE", "sublabel": "token valid", "col": 0, "step": "01", "tag": "proceed"},
       {"id": "retrylater", "type": "waiting", "label": "RETRY_LATER", "sublabel": "refresh failed", "col": 2, "tag": "defer"},
   ],
   [
       {"id": "loggedout", "type": "failure", "label": "LOGGED_OUT", "sublabel": "no session", "col": 2, "tag": "stop"},
   ],
   [
       {"from": "usable", "to": "retrylater", "label": "expired, refresh", "variant": "security", "route": "drop", "labelDy": 58},
       {"from": "retrylater", "to": "usable", "label": "refresh ok", "variant": "emphasis", "route": "bottom-channel", "labelDy": 40},
       {"from": "retrylater", "to": "loggedout", "label": "no session", "variant": "security", "route": "drop", "labelDy": 58},
   ],
   [
       card("emerald", "Three readiness values",
            "USABLE lets the group proceed",
            "RETRY_LATER defers without counting a failure",
            "LOGGED_OUT stops the whole drain"),
       card("amber", "Grace window",
            "A token inside the grace window is still usable",
            "One refresh is attempted on a 401",
            "A second failure defers rather than burning the retry budget"),
   ],
   "Token check", "Recovery")


def main() -> None:
    for name, doc in DIAGRAMS:
        path = OUT / f"{name}.{doc['diagram_type']}.json"
        path.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(DIAGRAMS)} Archify sources")


if __name__ == "__main__":
    main()
