#!/usr/bin/env python3
"""Emit the diagram catalog: index.html, DIAGRAM-INDEX.md, UML-COVERAGE.md.

A single CATALOG list is the source of truth for every diagram in the suite so
the interactive index, the Markdown index, and the UML coverage matrix stay in
sync. The HTML is fully self-contained (no CDN, no external fonts) and offers
search plus filtering by category, UML type, evidence class, and renderer.
"""
from __future__ import annotations

import html
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]

# evidence: ANDROID-SOURCE | DESKTOP-PROPOSED | SCHEMA-EXPORT | MIXED
CATALOG = [
    # ---- structural ----
    ("system-context", "System Context — Desktop & Shared Backend", "structural/system-context.html",
     "architecture", "System Context (non-UML)", "DESKTOP-PROPOSED", "archify",
     "Staff actors, the proposed desktop shell, and the shared Supabase project."),
    ("application-architecture", "Application Architecture — Desktop Layers", "structural/application-architecture.html",
     "architecture", "Component (layered)", "DESKTOP-PROPOSED", "archify",
     "React renderer → Wails bindings → services → repositories → SQLite + sync."),
    ("deployment-desktop", "Deployment — Desktop Runtime", "structural/deployment-desktop.html",
     "architecture", "Deployment", "DESKTOP-PROPOSED", "archify",
     "Single Wails process, webview, local SQLite file, shared Supabase."),
    ("component-android-reference", "Android Reference Components", "structural/component-android-reference.html",
     "architecture", "Component", "ANDROID-SOURCE", "archify",
     "Verified app/core/data/domain/feature module structure at ca4bed4."),
    ("build-packaging-android", "Build & Packaging (Android reference)", "structural/build-packaging-android.html",
     "workflow", "Activity (build)", "ANDROID-SOURCE", "archify",
     "Gradle pipeline; no desktop build, signing, or CI exists."),
    ("class-android-reference", "Class Diagram — Android Reference Model", "structural/class-android-reference.svg",
     "svg", "Class", "ANDROID-SOURCE", "svg",
     "Representative Room entities, DAOs, repositories, and services."),
    ("class-desktop-proposed", "Class Diagram — Desktop Proposed Layering", "structural/class-desktop-proposed.svg",
     "svg", "Class", "DESKTOP-PROPOSED", "svg",
     "Planned Go + React classes mirroring Android contracts; not implemented."),
    ("package-android-reference", "Package Diagram — Android Modules", "structural/package-android-reference.svg",
     "svg", "Package", "ANDROID-SOURCE", "svg",
     "Verified Gradle module and package layout at ca4bed4."),
    ("package-desktop-proposed", "Package Diagram — Desktop Proposed Modules", "structural/package-desktop-proposed.svg",
     "svg", "Package", "DESKTOP-PROPOSED", "svg",
     "Planned Go module layout; no go.mod/wails.json exists yet."),
    ("object-sync-queue-snapshot", "Object Diagram — Sync Queue Snapshot", "structural/object-sync-queue-snapshot.svg",
     "svg", "Object", "ANDROID-SOURCE", "svg",
     "Instance view of sync_queue rows during one vaccination upload."),
    ("composite-desktop-process", "Composite Structure — Desktop Process", "structural/composite-desktop-process.svg",
     "svg", "Composite Structure", "DESKTOP-PROPOSED", "svg",
     "Internal parts and ports of the single Wails process."),

    # ---- behavioral ----
    ("auth-authorization-flow", "Authentication & Authorization Flow", "behavioral/auth-authorization-flow.html",
     "workflow", "Activity (auth)", "MIXED", "archify",
     "Sign-in, JWT role claim, RLS gate. Live enforcement UNKNOWN."),
    ("error-recovery-flow", "Error Handling & Recovery", "behavioral/error-recovery-flow.html",
     "workflow", "Activity (error)", "DESKTOP-PROPOSED", "archify",
     "Fail-closed taxonomy with bounded retry; desktop code does not exist."),
    ("use-case-clinic-roles", "Use Case — Roles & Clinic Use Cases", "behavioral/use-case-clinic-roles.svg",
     "svg", "Use Case", "MIXED", "svg",
     "Five roles and the core use cases; authorization is server-enforced."),
    ("communication-vaccination-write", "Communication — Vaccination Write", "behavioral/communication-vaccination-write.svg",
     "svg", "Communication", "ANDROID-SOURCE", "svg",
     "Numbered message links for one vaccination record."),
    ("interaction-overview-consultation", "Interaction Overview — Consultation", "behavioral/interaction-overview-consultation.svg",
     "svg", "Interaction Overview", "ANDROID-SOURCE", "svg",
     "Frame overview where each box references a detailed interaction."),
    ("timing-sync-retry", "Timing — Sync Retry Backoff", "behavioral/timing-sync-retry.svg",
     "svg", "Timing", "ANDROID-SOURCE", "svg",
     "Duration-constrained state changes under a transient 5xx."),
    ("protocol-state-sync-item", "Protocol State Machine — Sync Item", "behavioral/protocol-state-sync-item.svg",
     "svg", "Protocol State Machine", "ANDROID-SOURCE", "svg",
     "Signatures and guards constraining accepted events per state."),
    ("sequence-login-session", "Sequence — Login & Session", "behavioral/sequence-login-session.html",
     "sequence", "Sequence", "ANDROID-SOURCE", "archify",
     "Verified Android login and bounded startup session restore."),
    ("sequence-vaccination-write", "Sequence — Vaccination & Receipt", "behavioral/sequence-vaccination-write.html",
     "sequence", "Sequence", "MIXED", "archify",
     "Local commit, queued sync, server-assigned receipt number."),
    ("sequence-sync-push-pull", "Sequence — Sync Push/Conflict/Pull", "behavioral/sequence-sync-push-pull.html",
     "sequence", "Sequence", "ANDROID-SOURCE", "archify",
     "Last-write-wins reconciliation, single-flight, bounded retry."),
    ("sequence-receipt-numbering", "Sequence — Receipt Numbering", "behavioral/sequence-receipt-numbering.html",
     "sequence", "Sequence", "SCHEMA-EXPORT", "archify",
     "Server-side receipt assignment and counter locking (export-reported)."),
    ("sequence-borrow-return", "Sequence — Borrow & Return", "behavioral/sequence-borrow-return.html",
     "sequence", "Sequence", "ANDROID-SOURCE", "archify",
     "Return path with outstanding-quantity cap and derived status."),
    ("sequence-backup-restore", "Sequence — Backup & Safe Restore", "behavioral/sequence-backup-restore.html",
     "sequence", "Sequence", "ANDROID-SOURCE", "archify",
     "Export and restore with a staged safety snapshot."),
    ("sequence-dashboard-refresh", "Sequence — Dashboard Refresh", "behavioral/sequence-dashboard-refresh.html",
     "sequence", "Sequence", "ANDROID-SOURCE", "archify",
     "Pull-then-render refresh with single-flight guard and debounced realtime."),
    ("state-sync-queue", "State Machine — Sync Queue Item", "behavioral/state-sync-queue.html",
     "lifecycle", "State Machine", "ANDROID-SOURCE", "archify",
     "PENDING → SYNCING → SYNCED / FAILED with requeue recovery."),
    ("state-reminder", "State Machine — Vaccination Reminder", "behavioral/state-reminder.html",
     "lifecycle", "State Machine", "ANDROID-SOURCE", "archify",
     "ACTIVE / COMPLETED / DISMISSED / EXTERNAL with a duplicate guard."),
    ("state-personal-reminder", "State Machine — Personal Reminder", "behavioral/state-personal-reminder.html",
     "lifecycle", "State Machine", "ANDROID-SOURCE", "archify",
     "PENDING → READY → COMPLETED with cancel and reverse side-paths."),
    ("state-borrow-record", "State Machine — Borrow Record", "behavioral/state-borrow-record.html",
     "lifecycle", "State Machine", "ANDROID-SOURCE", "archify",
     "Derived BORROWED / PARTIALLY_RETURNED / RETURNED status."),
    ("state-inventory-batch", "State Machine — Inventory Batch", "behavioral/state-inventory-batch.html",
     "lifecycle", "State Machine", "ANDROID-SOURCE", "archify",
     "Batch stock lifecycle and the history-based deletion guard."),
    ("state-finance-record", "State Machine — Financial Transaction", "behavioral/state-finance-record.html",
     "lifecycle", "State Machine", "ANDROID-SOURCE", "archify",
     "Append-only finance row with ambiguous-link failure."),
    ("state-session-readiness", "State Machine — Session Readiness", "behavioral/state-session-readiness.html",
     "lifecycle", "State Machine", "ANDROID-SOURCE", "archify",
     "USABLE / RETRY_LATER / LOGGED_OUT gating a sync group."),

    # ---- data-and-flows ----
    ("dataflow-offline-sync", "Data Flow — Offline Capture & Sync", "data-and-flows/dataflow-offline-sync.html",
     "dataflow", "Data Flow (DFD)", "MIXED", "archify",
     "Local-first write, queue, push, authority, pull. RLS UNKNOWN."),
    ("dataflow-patient-registration-offline", "Data Flow — Offline Registration", "data-and-flows/dataflow-patient-registration-offline.html",
     "dataflow", "Data Flow (DFD)", "DESKTOP-PROPOSED", "archify",
     "Planned desktop offline registration path mirroring Android."),
    ("erd-core-clinical", "ERD — Core Clinical Schema", "data-and-flows/erd-core-clinical.svg",
     "svg", "Entity Relationship (ERD)", "SCHEMA-EXPORT", "svg",
     "patients, visits, vaccination_items, consultations, notes."),
    ("erd-inventory", "ERD — Inventory & Stock Schema", "data-and-flows/erd-inventory.svg",
     "svg", "Entity Relationship (ERD)", "SCHEMA-EXPORT", "svg",
     "vaccines, batches, transactions, waste, borrow/return ledger."),
    ("erd-finance", "ERD — Finance & Receipt Schema", "data-and-flows/erd-finance.svg",
     "svg", "Entity Relationship (ERD)", "SCHEMA-EXPORT", "svg",
     "finance_transactions, expenses, receipt_sequences, reminders."),

    # ---- features ----
    ("activity-vaccination-record", "Activity — Record a Vaccination", "features/activity-vaccination-record.html",
     "workflow", "Activity", "ANDROID-SOURCE", "archify",
     "One transaction across visit, items, income, stock, and queue."),
    ("activity-inventory-decrement", "Activity — Inventory Decrement", "features/activity-inventory-decrement.html",
     "workflow", "Activity", "ANDROID-SOURCE", "archify",
     "FEFO decrement with reconciliation ledger and duplicate risk."),
    ("activity-borrow-return", "Activity — Borrow / Partial / Full Return", "features/activity-borrow-return.html",
     "workflow", "Activity", "ANDROID-SOURCE", "archify",
     "Borrow lifecycle with outstanding-quantity guard rails."),
    ("activity-patient-create", "Activity — Create a Patient", "features/activity-patient-create.html",
     "workflow", "Activity", "ANDROID-SOURCE", "archify",
     "Clinic-id generation, uniqueness check, insert, and enqueue in one tx."),
    ("activity-consultation-record", "Activity — Record a Consultation", "features/activity-consultation-record.html",
     "workflow", "Activity", "ANDROID-SOURCE", "archify",
     "Slot revalidation and an optional edit/no-change branch."),
    ("activity-batch-expiry", "Activity — Batch Selection & Expiry", "features/activity-batch-expiry.html",
     "workflow", "Activity", "ANDROID-SOURCE", "archify",
     "FEFO selection and expiry rules enforced at UI and repository."),
    ("activity-due-reminders", "Activity — Due Vaccinations & Reminders", "features/activity-due-reminders.html",
     "workflow", "Activity", "ANDROID-SOURCE", "archify",
     "Reminder pipeline; due dates are entered, not computed."),
    ("activity-dashboard-stats", "Activity — Dashboard Statistics", "features/activity-dashboard-stats.html",
     "workflow", "Activity", "ANDROID-SOURCE", "archify",
     "Local-first aggregation; no dashboard query reaches the network."),
    ("activity-staff-roles", "Activity — Staff & Role Management", "features/activity-staff-roles.html",
     "workflow", "Activity", "ANDROID-SOURCE", "archify",
     "Client gating is UX only; the Edge Function is the real boundary."),
    ("activity-backup-restore", "Activity — Backup & Restore", "features/activity-backup-restore.html",
     "workflow", "Activity", "ANDROID-SOURCE", "archify",
     "Fail-closed backup and staged-safety restore; ADR-0010 pending."),
]

EVIDENCE_LABEL = {
    "ANDROID-SOURCE": ("android", "ANDROID-SOURCE"),
    "DESKTOP-PROPOSED": ("proposed", "DESKTOP-PROPOSED"),
    "SCHEMA-EXPORT": ("export", "SCHEMA-EXPORT"),
    "MIXED": ("mixed", "MIXED / UNKNOWN"),
}

CATEGORY_LABEL = {
    "structural": "Structural",
    "behavioral": "Behavioral",
    "data-and-flows": "Data & Flows",
    "features": "Feature Workflows",
}

RENDERER_LABEL = {"archify": "Archify", "svg": "Supplementary SVG"}


def _cat(path: str) -> str:
    return path.split("/", 1)[0]


def build_html() -> str:
    import json
    cards = []
    for (did, title, path, cat, utype, ev, renderer, summary) in CATALOG:
        cls, evlabel = EVIDENCE_LABEL[ev]
        cards.append({
            "id": did, "title": title, "path": path, "cat": _cat(path), "utype": utype,
            "ev": evlabel, "evcls": cls, "renderer": renderer,
            "rendererLabel": RENDERER_LABEL[renderer], "summary": summary,
        })
    data = json.dumps(cards)
    cats = [c for c in CATEGORY_LABEL if any(_cat(x[2]) == c for x in CATALOG)]
    utypes = sorted({c[4] for c in CATALOG})
    evs = ["ANDROID-SOURCE", "DESKTOP-PROPOSED", "SCHEMA-EXPORT", "MIXED"]
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light" data-preset="classic">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Neo Child Clinic Desktop — Architecture &amp; UML Diagram Suite</title>
<style>
:root{{--bg:#0d1117;--surface:#161b22;--line:#30363d;--text:#e6edf3;--muted:#8b949e;
--accent:#ea580c;--accent2:#c2410c;--ring:#f97316;--ok:#047857;--warn:#b45309;--bad:#be123c;}}
html[data-theme="light"]{{--bg:#fffbeb;--surface:#fff7ed;--line:#fed7aa;--text:#1c1917;
--muted:#9a7a5a;--accent:#ea580c;--accent2:#c2410c;--ring:#f97316;}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);
font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.5}}
.wrap{{max-width:1180px;margin:0 auto;padding:32px 20px 80px}}
header h1{{font-size:26px;margin:0 0 6px;font-weight:700}}
header .sub{{color:var(--muted);font-size:14px;max-width:78ch;margin:0 0 18px}}
.legend{{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 20px}}
.legend .k{{display:inline-flex;align-items:center;gap:7px;font-size:12px;font-weight:600;
padding:5px 11px;border-radius:20px;border:1px solid var(--line);background:var(--surface)}}
.dot{{width:9px;height:9px;border-radius:50%}}
.dot.android{{background:#0369a1}}.dot.proposed{{background:#c2410c}}
.dot.export{{background:#047857}}.dot.mixed{{background:#a16207}}
.controls{{position:sticky;top:0;z-index:20;background:var(--bg);padding:14px 0;
border-bottom:1px solid var(--line);margin-bottom:22px}}
.search{{width:100%;padding:11px 14px;border-radius:10px;border:1px solid var(--line);
background:var(--surface);color:var(--text);font-size:14px;margin-bottom:12px}}
.search:focus{{outline:2px solid var(--ring);outline-offset:1px}}
.filters{{display:flex;flex-wrap:wrap;gap:18px}}
.fgroup{{display:flex;flex-direction:column;gap:6px}}
.fgroup .lbl{{font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}}
.chips{{display:flex;flex-wrap:wrap;gap:6px}}
.chip{{font-size:12px;font-weight:600;padding:5px 11px;border-radius:16px;cursor:pointer;
border:1px solid var(--line);background:var(--surface);color:var(--text)}}
.chip[aria-pressed="true"]{{background:var(--accent);border-color:var(--accent);color:#fff}}
.count{{font-size:12px;color:var(--muted);margin:14px 2px 16px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}}
.card{{display:block;text-decoration:none;color:inherit;background:var(--surface);
border:1px solid var(--line);border-radius:12px;padding:16px 16px 14px;transition:.12s;
border-left:4px solid var(--accent)}}
.card:hover{{transform:translateY(-2px);border-color:var(--ring);box-shadow:0 6px 20px rgba(234,88,12,.12)}}
.card.android{{border-left-color:#0369a1}}.card.proposed{{border-left-color:#c2410c}}
.card.export{{border-left-color:#047857}}.card.mixed{{border-left-color:#a16207}}
.card h3{{font-size:15px;margin:0 0 8px;font-weight:700}}
.badges{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:9px}}
.badge{{font-size:10px;font-weight:700;letter-spacing:.03em;padding:3px 8px;border-radius:6px;
border:1px solid var(--line)}}
.badge.type{{background:var(--surface);color:var(--muted)}}
.badge.ev.android{{background:#e0f2fe;color:#0369a1}}.badge.ev.proposed{{background:#ffedd5;color:#9a3412}}
.badge.ev.export{{background:#d1fae5;color:#047857}}.badge.ev.mixed{{background:#fef3c7;color:#92400e}}
.badge.rend{{background:var(--surface);color:var(--muted)}}
.card p{{font-size:12.5px;color:var(--muted);margin:0}}
.empty{{color:var(--muted);font-size:14px;padding:40px 0;text-align:center}}
footer{{margin-top:44px;padding-top:20px;border-top:1px solid var(--line);
font-size:12px;color:var(--muted)}}
footer a{{color:var(--accent)}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>Neo Child Clinic Desktop — Architecture &amp; UML Diagram Suite</h1>
  <p class="sub">Documentation-only. Every diagram labels its evidence on its face:
    <b>[ANDROID-SOURCE]</b> verified against Android source at commit ca4bed4 (reference implementation),
    <b>[DESKTOP-PROPOSED]</b> planned design from the Knowledge Base (NOT implemented),
    <b>[SCHEMA-EXPORT]</b> reported by docs/Schemas CSV exports (not exercised against live Supabase),
    <b>[UNKNOWN]</b> could not be verified. The desktop repository contains no application code.</p>
  <div class="legend">
    <span class="k"><span class="dot android"></span>Android reference (verified)</span>
    <span class="k"><span class="dot proposed"></span>Desktop proposed (not implemented)</span>
    <span class="k"><span class="dot export"></span>Schema export (not live-verified)</span>
    <span class="k"><span class="dot mixed"></span>Mixed / unknown</span>
  </div>
</header>

<div class="controls">
  <input id="q" class="search" type="search" placeholder="Search diagrams by title, type, or summary…" autocomplete="off"/>
  <div class="filters">
    <div class="fgroup"><span class="lbl">Category</span><div class="chips" data-dim="cat">
      {''.join(f'<button class="chip" data-v="{c}" aria-pressed="false">{CATEGORY_LABEL[c]}</button>' for c in cats)}
    </div></div>
    <div class="fgroup"><span class="lbl">UML type</span><div class="chips" data-dim="utype">
      {''.join(f'<button class="chip" data-v="{html.escape(u)}" aria-pressed="false">{html.escape(u)}</button>' for u in utypes)}
    </div></div>
    <div class="fgroup"><span class="lbl">Evidence</span><div class="chips" data-dim="ev">
      {''.join(f'<button class="chip" data-v="{EVIDENCE_LABEL[e][1]}" aria-pressed="false">{EVIDENCE_LABEL[e][1]}</button>' for e in evs)}
    </div></div>
    <div class="fgroup"><span class="lbl">Renderer</span><div class="chips" data-dim="renderer">
      <button class="chip" data-v="archify" aria-pressed="false">Archify</button>
      <button class="chip" data-v="svg" aria-pressed="false">Supplementary SVG</button>
    </div></div>
  </div>
</div>

<div class="count" id="count"></div>
<div class="grid" id="grid"></div>
<div class="empty" id="empty" style="display:none">No diagrams match the current filters.</div>

<footer>
  Generated by the Archify skill (renderers) plus a local SVG generator for UML types Archify cannot produce.
  Source evidence: Android source at ca4bed4; docs/Schemas metadata CSV exports; Knowledge Base baseline.
  Static, offline, no CDN. See <a href="UML-COVERAGE.md">UML-COVERAGE.md</a> for the diagram-type matrix and
  <a href="DIAGRAM-INDEX.md">DIAGRAM-INDEX.md</a> for the flat index.
</footer>
</div>

<script>
const DATA = {data};
const grid = document.getElementById('grid');
const countEl = document.getElementById('count');
const emptyEl = document.getElementById('empty');
const state = {{ q:'', cat:new Set(), utype:new Set(), ev:new Set(), renderer:new Set() }};
const dims = ['cat','utype','ev','renderer'];

function matches(d){{
  if(state.q){{
    const s=(d.title+' '+d.utype+' '+d.summary+' '+d.ev).toLowerCase();
    if(!s.includes(state.q)) return false;
  }}
  for(const dim of dims){{
    if(state[dim].size && !state[dim].has(d[dim])) return false;
  }}
  return true;
}}
function render(){{
  const list = DATA.filter(matches);
  grid.innerHTML = list.map(d => `
    <a class="card ${{d.evcls}}" href="${{d.path}}">
      <div class="badges">
        <span class="badge type">${{d.utype}}</span>
        <span class="badge ev ${{d.evcls}}">${{d.ev}}</span>
        <span class="badge rend">${{d.rendererLabel}}</span>
      </div>
      <h3>${{d.title}}</h3>
      <p>${{d.summary}}</p>
    </a>`).join('');
  countEl.textContent = `Showing ${{list.length}} of ${{DATA.length}} diagrams`;
  emptyEl.style.display = list.length ? 'none' : 'block';
}}
document.getElementById('q').addEventListener('input', e => {{ state.q = e.target.value.trim().toLowerCase(); render(); }});
document.querySelectorAll('.chips').forEach(box => {{
  const dim = box.dataset.dim;
  box.querySelectorAll('.chip').forEach(chip => chip.addEventListener('click', () => {{
    const v = chip.dataset.v;
    if(state[dim].has(v)){{ state[dim].delete(v); chip.setAttribute('aria-pressed','false'); }}
    else {{ state[dim].add(v); chip.setAttribute('aria-pressed','true'); }}
    render();
  }});
}});
render();
</script>
</body>
</html>
"""


def build_index_md() -> str:
    lines = ["# Diagram Index", "",
             "Flat index of every diagram in the generated suite. Evidence classes: "
             "`ANDROID-SOURCE` (verified at ca4bed4, reference only), `DESKTOP-PROPOSED` "
             "(planned, NOT implemented), `SCHEMA-EXPORT` (export-reported, not live-verified), "
             "`MIXED` (mixed or unknown).", ""]
    for cat in ["structural", "behavioral", "data-and-flows", "features"]:
        rows = [c for c in CATALOG if _cat(c[2]) == cat]
        if not rows:
            continue
        lines.append(f"## {CATEGORY_LABEL[cat]}")
        lines.append("")
        lines.append("| Diagram | UML type | Evidence | Renderer | Summary |")
        lines.append("|---|---|---|---|---|")
        for (did, title, path, _c, utype, ev, renderer, summary) in rows:
            evlabel = EVIDENCE_LABEL[ev][1]
            lines.append(f"| [{title}]({path}) | {utype} | `{evlabel}` | {RENDERER_LABEL[renderer]} | {summary} |")
        lines.append("")
    lines.append(f"**Total: {len(CATALOG)} diagrams** "
                 f"(33 Archify-rendered HTML + 14 supplementary SVG).")
    return "\n".join(lines) + "\n"


def build_coverage_md() -> str:
    # type -> (status, renderer, note)
    rows = [
        ("Class", "Implemented", "SVG", "Android reference + desktop proposed class models."),
        ("Object", "Implemented", "SVG", "Sync-queue instance snapshot."),
        ("Package", "Implemented", "SVG", "Android modules + desktop proposed modules."),
        ("Component", "Implemented", "Archify + SVG", "Layered desktop architecture (Archify) + Android reference."),
        ("Composite Structure", "Implemented", "SVG", "Desktop process internal parts and ports."),
        ("Deployment", "Implemented", "Archify", "Single Wails process, webview, SQLite, shared Supabase."),
        ("Profile", "Inapplicable", "—", "UML profiles/stereotypes have no meaning for this documentation set; "
                                          "the desktop is a greenfield app, not a UML-extensible platform."),
        ("Use Case", "Implemented", "SVG", "Five clinic roles and core use cases."),
        ("Activity", "Implemented", "Archify", "10 feature workflows + auth, error, and build flows."),
        ("State Machine (behavioral)", "Implemented", "Archify", "7 lifecycle diagrams (sync, reminders, borrow, batch, finance, session)."),
        ("Protocol State Machine", "Implemented", "SVG", "Sync-item protocol signatures and guards."),
        ("Sequence", "Implemented", "Archify", "7 sequence diagrams (login, vaccination, sync, receipt, borrow, backup, refresh)."),
        ("Communication", "Implemented", "SVG", "Vaccination write message links."),
        ("Interaction Overview", "Implemented", "SVG", "Consultation flow frame overview."),
        ("Timing", "Implemented", "SVG", "Sync retry backoff duration model."),
        ("System Context (non-UML)", "Implemented", "Archify", "Actors, desktop shell, shared Supabase."),
        ("Data Flow Diagram / DFD (non-UML)", "Implemented", "Archify", "Offline capture/sync and offline registration."),
        ("Entity Relationship / ERD (non-UML)", "Implemented", "SVG", "Core clinical, inventory, and finance domains from the schema export."),
        ("Model (UML 2.5)", "Inapplicable", "—", "A model-containment diagram adds no information beyond the package and component views."),
        ("Information Item (UML 2.5)", "Inapplicable", "—", "Information-item diagrams are superseded by the sequence and data-flow views already produced."),
        ("Macro (build/packaging pipeline)", "Implemented (Android only)", "Archify", "Android Gradle pipeline; the desktop build is BLOCKED — no go.mod, wails.json, or CI exists."),
        ("Decision / ADR view", "Documented elsewhere", "—", "10 ADRs (ADR-0008 accepted; 9 pending incl. ADR-0010 backup/encryption) live in the Knowledge Base, not as a diagram."),
        ("Live security / RLS enforcement", "Blocked (UNKNOWN)", "—", "Requires exercising the live Supabase project, which is out of scope; exports report {public} policies on 10 core tables and anon-executable functions."),
    ]
    lines = ["# UML & Diagram Coverage Matrix", "",
             "Every standard UML 2.5 diagram type plus the supplementary types the suite addresses. "
             "Archify natively renders architecture, workflow, sequence, dataflow, and lifecycle; "
             "the remaining types are produced by a local SVG generator so coverage is honest rather than "
             "claimed. Live Supabase security behavior is marked UNKNOWN because the live project is never "
             "exercised in this documentation-only pass.", "",
             "| Diagram type | Status | Renderer | Notes |", "|---|---|---|---|"]
    for t, status, renderer, note in rows:
        lines.append(f"| {t} | {status} | {renderer} | {note} |")
    lines += ["",
              f"**Summary:** {len(rows)} diagram types tracked — "
              f"{sum(1 for r in rows if r[1].startswith('Implemented'))} implemented, "
              f"{sum(1 for r in rows if r[1].startswith('Inapplicable'))} documented as inapplicable, "
              f"{sum(1 for r in rows if r[1].startswith('Blocked') or 'blocked' in r[1].lower())} blocked/unknown, "
              f"{sum(1 for r in rows if 'elsewhere' in r[1])} tracked elsewhere.", "",
              "The suite ships 33 Archify-rendered HTML diagrams and 14 supplementary SVG diagrams "
              "(47 total). See [DIAGRAM-INDEX.md](DIAGRAM-INDEX.md) for the flat list and "
              "[index.html](index.html) for the interactive, filterable catalog."]
    return "\n".join(lines) + "\n"


def main() -> None:
    (HERE / "index.html").write_text(build_html(), encoding="utf-8")
    (HERE / "DIAGRAM-INDEX.md").write_text(build_index_md(), encoding="utf-8")
    (HERE / "UML-COVERAGE.md").write_text(build_coverage_md(), encoding="utf-8")
    print(f"index.html, DIAGRAM-INDEX.md, UML-COVERAGE.md written ({len(CATALOG)} diagrams)")


if __name__ == "__main__":
    main()
