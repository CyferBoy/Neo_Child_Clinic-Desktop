#!/usr/bin/env python3
"""Generate supplementary UML SVG diagrams that Archify cannot produce.

Archify renders architecture, workflow, sequence, dataflow, and lifecycle
diagrams. The remaining UML diagram types are drawn here as self-contained,
offline SVG in the suite's orange/light palette so the coverage matrix can be
completed honestly. Every diagram states its evidence class on its face.

Evidence classes:
  [ANDROID-SOURCE]   verified against Android source at ca4bed4 (reference only)
  [DESKTOP-PROPOSED] planned desktop design from the Knowledge Base; NOT implemented
  [SCHEMA-EXPORT]    reported by docs/Schemas metadata exports; not live-verified
  [UNKNOWN]          could not be verified from available evidence

No external fonts, scripts, or CDN references are emitted.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE
SCHEMA = json.loads((HERE / "sources" / "schema-model.json").read_text(encoding="utf-8"))

# Orange / light palette (matches the Archify light theme the suite requests).
INK = "#1c1917"
MUTED = "#78716c"
LINE = "#c2410c"
BOX = "#fff7ed"
BOX2 = "#ffedd5"
HEAD = "#ea580c"
HEAD2 = "#9a3412"
ROSE = "#9f1239"
ROSE_BG = "#fff1f2"
EMER = "#047857"
EMER_BG = "#ecfdf5"
BAND = "#fed7aa"


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def text(x, y, s, size=13, fill=INK, anchor="start", weight=400, mono=True, italic=False):
    fam = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" if mono else \
        "ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif"
    it = ' font-style="italic"' if italic else ""
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}"{it}>'
            f"{esc(s)}</text>")


def header(w, h, title, subtitle, evidence):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
        f'<rect width="{w}" height="{h}" fill="#fffbeb"/>',
        text(28, 44, title, size=22, weight=700, mono=False),
        text(28, 68, subtitle, size=13, fill=MUTED, mono=False),
        text(28, 88, evidence, size=11, fill=HEAD2, weight=600, mono=False),
    ]
    return parts


FOOT = ('<a class="ncc-backlink" href="../index.html">&larr; Diagram index</a>'
        '<style>.ncc-backlink{position:fixed;left:14px;top:14px;z-index:9999;'
        'font:600 12px/1 ui-monospace,Menlo,Consolas,monospace;padding:8px 12px;'
        'border-radius:8px;text-decoration:none;background:#fff7ed;color:#1c1917;'
        'border:1px solid #c2410c;}.ncc-backlink:hover{background:#ffedd5;}</style>')


def footer():
    # A valid-SVG backlink placed INSIDE the <svg> element (not HTML after it),
    # so the file stays well-formed XML while remaining navigable.
    link = (
        '<a href="../index.html" style="text-decoration:none">'
        '<rect x="14" y="14" width="156" height="30" rx="8" fill="#fff7ed" stroke="#c2410c" stroke-width="1.2"/>'
        '<text x="30" y="33" font-family="ui-monospace,Menlo,Consolas,monospace" font-size="12" '
        'font-weight="600" fill="#1c1917">&#8592; Diagram index</text></a>'
    )
    return [link, "</svg>"]


def class_box(x, y, w, name, attrs, methods, fill=BOX, head=HEAD, stere=None, tag=None):
    """Draw a UML class with name / attributes / methods compartments."""
    rowh = 18
    headh = 30 + (16 if stere else 0)
    h = headh + max(len(attrs), 1) * rowh + (10 if methods else 0) + max(len(methods), 1) * rowh
    p = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" '
         f'stroke="{LINE}" stroke-width="1.5"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{headh}" rx="8" fill="{head}"/>',
         f'<rect x="{x}" y="{y + headh - 8}" width="{w}" height="8" fill="{head}"/>']
    ty = y + 20
    if stere:
        p.append(text(x + w / 2, y + 15, "«" + stere + "»", size=10, fill="#fff7ed",
                      anchor="middle", mono=False))
        ty = y + 30
    p.append(text(x + w / 2, ty, name, size=13, fill="#ffffff", anchor="middle", weight=700))
    if tag:
        p.append(text(x + w - 8, y + headh - 6, tag, size=9, fill="#fff7ed", anchor="end",
                      weight=600, mono=False))
    cy = y + headh + 16
    for a in attrs:
        p.append(text(x + 12, cy, a, size=11, fill=INK))
        cy += rowh
    if methods:
        cy += 10
        p.append(f'<line x1="{x}" y1="{cy - 12}" x2="{x + w}" y2="{cy - 12}" stroke="{LINE}" stroke-width="1"/>')
        for m in methods:
            p.append(text(x + 12, cy, m, size=11, fill=MUTED))
            cy += rowh
    return p, h


def arrow(x1, y1, x2, y2, label=None, color=INK, dashed=False, kind="open"):
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    mid = ((x1 + x2) / 2, (y1 + y2) / 2)
    p = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
         f'stroke-width="1.6"{dash} marker-end="url(#ah-{kind})"/>']
    if label:
        p.append(text(mid[0], mid[1] - 6, label, size=10, fill=color, anchor="middle", mono=False))
    return p


def marker(kind="open"):
    if kind == "diamond":
        return ('<marker id="ah-diamond" markerWidth="14" markerHeight="14" refX="12" '
                'refY="6" orient="auto"><path d="M0,6 L6,2 L12,6 L6,10 Z" fill="#fff7ed" '
                'stroke="#1c1917" stroke-width="1"/></marker>')
    return (f'<marker id="ah-{kind}" markerWidth="12" markerHeight="12" refX="10" refY="6" '
            f'orient="auto"><path d="M0,1 L10,6 L0,11" fill="none" stroke="{INK}" '
            f'stroke-width="1.6"/></marker>')


# --------------------------------------------------------------------------
# STRUCTURAL — class, package, object, composite
# --------------------------------------------------------------------------

def svg_class_android():
    W, H = 980, 720
    parts = header(W, H, "Class Diagram — Android Reference Model",
                   "Representative entities, DAOs, repositories, and services verified at ca4bed4.",
                   "[ANDROID-SOURCE] Reference implementation only — the desktop does not share these classes.")
    parts.append(marker())
    boxes = [
        (40, 120, 250, "PatientEntity", ["+ id: UUID", "+ clinicId: String", "+ fullName: String", "+ dateOfBirth: LocalDate"],
         ["@Entity(tableName=\"patients\")"], BOX, HEAD, "entity"),
        (40, 360, 250, "VaccinationItemEntity", ["+ id: UUID", "+ visitId: UUID", "+ vaccineId: UUID", "+ batchId: UUID"],
         ["@Entity(tableName=\"vaccination_items\")"], BOX, HEAD, "entity"),
        (360, 120, 250, "PatientDao", ["+ observeAll(): Flow<List<Patient>>", "+ upsert(patient)"],
         ["@Dao interface"], BOX2, HEAD2, "dao"),
        (360, 360, 250, "VaccinationDao", ["+ insertVisitWithItems(tx)", "+ observeDueVaccines()"],
         ["@Dao interface"], BOX2, HEAD2, "dao"),
        (690, 120, 250, "ClinicalVaccinationService", ["+ recordVaccination(req): Result", "- deductBatch(tx)"],
         ["orchestrates one tx"], EMER_BG, EMER, "service"),
        (690, 360, 250, "SyncRepository", ["+ processNextItems()", "- pushGroup(groupId)"],
         ["owns outbound + inbound"], EMER_BG, EMER, "repository"),
    ]
    pos = {}
    for x, y, w, name, attrs, methods, fill, head, stere in boxes:
        bp, h = class_box(x, y, w, name, attrs, methods, fill, head, stere)
        parts.extend(bp)
        pos[name] = (x, y, w, h)
    # edges
    parts += arrow(290, 200, 360, 200, "queries")
    parts += arrow(290, 440, 360, 440, "queries")
    parts += arrow(610, 200, 690, 200, "calls")
    parts += arrow(610, 440, 690, 440, "calls")
    parts += arrow(815, 250, 815, 360, "syncs", dashed=True)
    parts += arrow(165, 260, 165, 360, "1..* ")
    # legend
    parts.append(text(40, 640, "Evidence: Room AppDatabase v33 · 25 entities · 21 DAOs · SQLCipher at rest. "
                               "Desktop must reproduce meaning, not these classes.", size=11, fill=MUTED, mono=False))
    parts.append(text(40, 662, "Verified source: app/src/main/java/com/neochildclinic/ (core/database, core/sync, data, domain).",
                      size=11, fill=MUTED, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


def svg_class_desktop():
    W, H = 980, 700
    parts = header(W, H, "Class Diagram — Desktop Proposed Layering",
                   "Planned Go + React classes that mirror the Android contracts. No desktop code exists.",
                   "[DESKTOP-PROPOSED] Intended design from the Knowledge Base — NOT implemented.")
    parts.append(marker())
    boxes = [
        (40, 120, 240, "ReactScreen", ["- viewState", "+ onValidate()", "+ onSubmit()"],
         ["renderer, no PHI"], BOX, HEAD, "component"),
        (340, 120, 240, "Binding (Wails)", ["+ SaveVisit(req) error", "+ LoadDashboard()"],
         ["typed crossing"], BOX2, HEAD2, "interface"),
        (640, 120, 260, "VisitService", ["+ RecordVaccination(req)", "- Validate(rows)"],
         ["orchestration"], EMER_BG, EMER, "service"),
        (340, 380, 240, "DomainRules", ["+ CheckBatchFefo(batch)", "+ Totals(items)"],
         ["pure, no I/O"], EMER_BG, EMER, "service"),
        (640, 380, 260, "VisitRepository", ["+ InsertVisitTx(visit)", "- NextReceipt()"],
         ["owns all SQL"], BOX, HEAD, "repository"),
        (40, 380, 240, "LocalStore (SQLite)", ["+ Begin() / Commit()", "+ SyncQueue table"],
         ["working copy"], BOX2, HEAD2, "component"),
    ]
    pos = {}
    for x, y, w, name, attrs, methods, fill, head, stere in boxes:
        bp, h = class_box(x, y, w, name, attrs, methods, fill, head, stere)
        parts.extend(bp)
        pos[name] = (x, y, w, h)
    parts += arrow(280, 200, 340, 200, "typed call")
    parts += arrow(580, 200, 640, 200, "invoke")
    parts += arrow(770, 250, 770, 380, "SQL", dashed=True)
    parts += arrow(700, 440, 580, 440, "validate", dashed=True)
    parts += arrow(640, 470, 280, 470, "queue + merge", dashed=True)
    parts.append(text(40, 640, "The renderer never calls Supabase or opens SQLite directly; every read and write "
                               "crosses the typed Wails binding boundary.", size=11, fill=MUTED, mono=False))
    parts.append(text(40, 662, "0 of 22 planned desktop modules are implemented; no Go/Wails/React source exists.",
                      size=11, fill=ROSE, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


def svg_package_android():
    W, H = 900, 560
    parts = header(W, H, "Package Diagram — Android Modules",
                   "Verified Gradle module and package structure at ca4bed4.",
                   "[ANDROID-SOURCE] Reference implementation — 352 Kotlin files, 21 feature packages.")
    packs = [
        (50, 120, 220, 150, "app", ["navigation", "MainActivity", "DI graph"], HEAD),
        (320, 120, 220, 180, "core", ["cache · database", "network · sync", "security · di"], HEAD2),
        (590, 120, 260, 150, "domain", ["models", "repository contracts"], EMER),
        (590, 340, 260, 180, "data", ["local sources", "remote sources"], EMER),
        (50, 340, 220, 160, "feature (21)", ["clinical · inventory", "finance · reminders"], HEAD),
    ]
    for x, y, w, h, name, items, col in packs:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{BOX}" stroke="{LINE}" stroke-width="1.5"/>')
        parts.append(f'<path d="M{x},{y} L{x + 90},{y} L{x + 100},{y + 22} L{x + w},{y + 22} '
                     f'L{x + w},{y + h} L{x},{y + h} Z" fill="{col}"/>')
        parts.append(text(x + 14, y + 16, name, size=14, fill="#ffffff", weight=700))
        iy = y + 48
        for it in items:
            parts.append(text(x + 16, iy, it, size=12, fill=INK, mono=False))
            iy += 22
    parts += arrow(270, 190, 320, 190, "hosts")
    parts += arrow(540, 190, 590, 190, "contracts")
    parts += arrow(720, 300, 720, 340, "implements")
    parts += arrow(590, 400, 540, 400, "serves")
    parts += arrow(160, 340, 160, 270, "routes")
    parts.append(text(50, 540, "core splits into cache, database, di, network, sync, security. "
                               "Room AppDatabase v33 lives under core/database.", size=11, fill=MUTED, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


def svg_package_desktop():
    W, H = 900, 560
    parts = header(W, H, "Package Diagram — Desktop Proposed Modules",
                   "Planned Go module layout mirroring the Android contracts. Nothing is implemented.",
                   "[DESKTOP-PROPOSED] Intended structure from the Knowledge Base — NOT implemented.")
    packs = [
        (50, 120, 220, 150, "cmd/desktop", ["main.go", "Wails bootstrap"], HEAD),
        (320, 120, 220, 180, "internal/app", ["services", "domain rules"], HEAD2),
        (590, 120, 260, 150, "internal/store", ["repositories", "SQLite + migrations"], EMER),
        (590, 340, 260, 180, "internal/sync", ["queue worker", "retry + conflict"], EMER),
        (50, 340, 220, 160, "web/renderer", ["React + TS screens", "view state only"], HEAD),
    ]
    for x, y, w, h, name, items, col in packs:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{BOX}" stroke="{LINE}" stroke-width="1.5"/>')
        parts.append(f'<path d="M{x},{y} L{x + 110},{y} L{x + 120},{y + 22} L{x + w},{y + 22} '
                     f'L{x + w},{y + h} L{x},{y + h} Z" fill="{col}"/>')
        parts.append(text(x + 14, y + 16, name, size=14, fill="#ffffff", weight=700))
        iy = y + 48
        for it in items:
            parts.append(text(x + 16, iy, it, size=12, fill=INK, mono=False))
            iy += 22
    parts += arrow(270, 190, 320, 190, "wires")
    parts += arrow(540, 190, 590, 190, "calls")
    parts += arrow(720, 300, 720, 340, "feeds")
    parts += arrow(590, 400, 540, 400, "persists")
    parts += arrow(160, 340, 160, 270, "binds")
    parts.append(text(50, 540, "No go.mod, wails.json, or package.json exists in the repository today.",
                      size=11, fill=ROSE, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


def svg_object_diagram():
    W, H = 940, 560
    parts = header(W, H, "Object Diagram — Sync Queue Instance Snapshot",
                   "A moment-in-time instance view of the offline sync queue during one vaccination upload.",
                   "[ANDROID-SOURCE] Mirrors verified sync_queue rows; desktop store is proposed.")
    parts.append(marker())
    objs = [
        (50, 130, 260, "queueItem1 : SyncQueueItem", ["entityType = \"patient_visits\"", "operation = UPSERT",
                                                      "status = SYNCING", "groupId = g-101", "retryCount = 0"]),
        (360, 130, 260, "queueItem2 : SyncQueueItem", ["entityType = \"vaccination_items\"", "operation = UPSERT",
                                                       "status = PENDING", "groupId = g-101", "retryCount = 0"]),
        (360, 360, 260, "group : TxGroup", ["groupId = g-101", "priority = 10", "size = 2"]),
        (670, 130, 240, "visit : PatientVisit", ["id = 8f2c…", "receiptNumber = \"\"", "synced = false"]),
    ]
    for x, y, w, name, attrs in objs:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{30 + len(attrs) * 18}" rx="8" '
                     f'fill="{BOX2}" stroke="{LINE}" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="8" fill="{HEAD2}"/>')
        parts.append(text(x + 12, y + 19, name, size=12, fill="#ffffff", weight=700))
        ay = y + 46
        for a in attrs:
            parts.append(text(x + 12, ay, a, size=11, fill=INK))
            ay += 18
    parts += arrow(310, 180, 360, 180, "belongs to")
    parts += arrow(490, 250, 490, 360, "groups")
    parts += arrow(620, 180, 670, 180, "writes")
    parts.append(text(50, 500, "receiptNumber is uploaded blank; a server trigger assigns it on insert and the "
                               "worker stores it back.", size=11, fill=MUTED, mono=False))
    parts.append(text(50, 522, "sync_queue has no unique constraint on (entityType, operation); duplicate rows are "
                               "cleaned opportunistically, not prevented.", size=11, fill=ROSE, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


def svg_composite():
    W, H = 900, 540
    parts = header(W, H, "Composite Structure — Desktop Process Internals",
                   "The single Wails process exposes provided ports to the renderer and requires the shared backend.",
                   "[DESKTOP-PROPOSED] One process hosts Go runtime + webview; nothing is deployed yet.")
    parts.append(marker())
    parts.append(f'<rect x="60" y="120" width="780" height="360" rx="14" fill="{BOX}" stroke="{LINE}" stroke-width="2"/>')
    parts.append(text(76, 146, "Desktop Process (Wails v3)", size=15, weight=700, fill=HEAD2, mono=False))
    inner = [
        (90, 180, 220, "React WebView", ["provides: UI events", "requires: bindings"], HEAD),
        (350, 180, 220, "Binding Layer", ["provides: typed methods", "requires: services"], HEAD2),
        (610, 180, 200, "App Services", ["provides: use cases", "requires: store"], EMER),
        (350, 360, 220, "Local Store (SQLite)", ["provides: repositories", "requires: SQLCipher?"], HEAD2),
        (610, 360, 200, "Sync Worker", ["provides: push/pull", "requires: network"], EMER),
    ]
    for x, y, w, name, ports, col in inner:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="120" rx="10" fill="#ffffff" stroke="{col}" stroke-width="1.8"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="10" fill="{col}"/>')
        parts.append(text(x + 12, y + 20, name, size=12, fill="#ffffff", weight=700))
        parts.append(text(x + 12, y + 52, ports[0], size=10, fill=INK, mono=False))
        parts.append(text(x + 12, y + 74, ports[1], size=10, fill=MUTED, mono=False))
    parts += arrow(310, 230, 350, 230, "call")
    parts += arrow(570, 230, 610, 230, "use")
    parts += arrow(460, 300, 460, 360, "SQL", dashed=True)
    parts += arrow(710, 300, 710, 360, "queue", dashed=True)
    parts += arrow(810, 240, 830, 400, "HTTPS", color=ROSE)
    parts.append(text(60, 512, "The renderer crosses exactly one boundary (bindings). Encryption of the local store "
                               "is pending ADR-0010.", size=11, fill=MUTED, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


# --------------------------------------------------------------------------
# BEHAVIORAL — use-case, communication, interaction-overview, timing, protocol
# --------------------------------------------------------------------------

def svg_usecase():
    W, H = 960, 620
    parts = header(W, H, "Use-Case Diagram — Roles and Clinic Use Cases",
                   "Five clinic roles and the core use cases they may invoke. Authorization is server-enforced.",
                   "[SCHEMA-EXPORT + ANDROID-SOURCE] Roles from JWT app_metadata; live RLS enforcement UNKNOWN.")
    parts.append(f'<rect x="230" y="110" width="500" height="470" rx="12" fill="{BOX}" stroke="{LINE}" stroke-width="1.5" stroke-dasharray="8 5"/>')
    parts.append(text(246, 134, "Clinic Desktop System", size=13, fill=HEAD2, weight=600, mono=False))
    actors = [("Admin", 90), ("Doctor", 210), ("Nurse", 330), ("Reception", 450), ("Inventory", 570)]
    for name, y in actors:
        parts.append(f'<circle cx="120" cy="{y}" r="16" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
        parts.append(f'<line x1="120" y1="{y + 16}" x2="120" y2="{y + 52}" stroke="{INK}" stroke-width="1.6"/>')
        parts.append(f'<line x1="98" y1="{y + 30}" x2="142" y2="{y + 30}" stroke="{INK}" stroke-width="1.6"/>')
        parts.append(f'<line x1="120" y1="{y + 52}" x2="104" y2="{y + 76}" stroke="{INK}" stroke-width="1.6"/>')
        parts.append(f'<line x1="120" y1="{y + 52}" x2="136" y2="{y + 76}" stroke="{INK}" stroke-width="1.6"/>')
        parts.append(text(120, y + 92, name, size=12, anchor="middle", weight=600, mono=False))
    ucs = [("Register patient", 180), ("Record consultation", 250), ("Record vaccination", 320),
           ("Manage inventory", 390), ("Issue receipt / finance", 460), ("Manage staff & roles", 530)]
    for label, y in ucs:
        parts.append(f'<ellipse cx="480" cy="{y}" rx="150" ry="28" fill="#ffffff" stroke="{HEAD}" stroke-width="1.6"/>')
        parts.append(text(480, y + 4, label, size=12, anchor="middle", mono=False))
    # associations
    assoc = [(90, 180), (90, 530), (210, 250), (210, 320), (330, 320), (330, 390),
             (450, 180), (450, 460), (570, 390), (570, 460)]
    for ay, uy in assoc:
        parts.append(f'<line x1="150" y1="{ay}" x2="330" y2="{uy}" stroke="{MUTED}" stroke-width="1.2"/>')
    parts.append(text(250, 604, "Client-side role gating is UX only; the manage-staff Edge Function and RLS are the "
                                "real boundary (export-reported).", size=11, fill=MUTED, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


def svg_communication():
    W, H = 940, 520
    parts = header(W, H, "Communication Diagram — Vaccination Write",
                   "Numbered message flows between objects for one vaccination record, mirroring the sequence view.",
                   "[ANDROID-SOURCE] Same verified contract as sequence-vaccination-write.")
    parts.append(marker())
    objs = [(120, 200, "screen"), (360, 120, "service"), (600, 200, "localDB"),
            (600, 380, "syncQueue"), (360, 380, "worker")]
    r = 52
    for cx, cy, name in objs:
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{BOX}" stroke="{LINE}" stroke-width="1.8"/>')
        parts.append(text(cx, cy + 4, name, size=12, anchor="middle", weight=600))
    msgs = [
        (172, 200, 308, 150, "1: recordVacc()"),
        (412, 150, 548, 190, "2: beginTx"),
        (600, 252, 600, 328, "3: enqueue"),
        (548, 380, 412, 380, "4: drain"),
        (412, 380, 308, 220, "5: upsert", True),
    ]
    for m in msgs:
        x1, y1, x2, y2, lab = m[0], m[1], m[2], m[3], m[4]
        dashed = len(m) > 5
        parts += arrow(x1, y1, x2, y2, lab, color=ROSE if dashed else INK, dashed=dashed)
    parts.append(text(120, 470, "Numbered arrows show link traversal order; the local commit (steps 2–3) never waits "
                                "on the network (steps 4–5).", size=11, fill=MUTED, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


def svg_interaction_overview():
    W, H = 960, 600
    parts = header(W, H, "Interaction Overview — Consultation Flow",
                   "Activity-style overview where each frame is a reference to a detailed interaction.",
                   "[ANDROID-SOURCE] Slot revalidation and optional edit branch verified at ca4bed4.")
    parts.append(marker())
    frames = [
        (70, 160, 200, "ref [Open Form]", "ConsultationForm"),
        (330, 160, 200, "ref [Check Slot]", "AvailabilityVM"),
        (590, 160, 200, "alt [slot free?]", "free : write / taken : reload"),
        (330, 360, 200, "ref [Persist]", "ConsultationService"),
        (590, 360, 200, "ref [Sync]", "SyncQueue"),
    ]
    for x, y, w, frame, sub in frames:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="96" rx="8" fill="{BOX}" stroke="{LINE}" stroke-width="1.6"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="8" fill="{HEAD}"/>')
        parts.append(text(x + 12, y + 17, frame, size=11, fill="#ffffff", weight=700, mono=False))
        parts.append(text(x + 12, y + 52, sub, size=11, fill=INK, mono=False))
        parts.append(text(x + 12, y + 74, "→ see sequence", size=10, fill=MUTED, mono=False))
    parts += arrow(270, 208, 330, 208, "start")
    parts += arrow(530, 208, 590, 208, "decide")
    parts += arrow(690, 256, 430, 360, "free", color=EMER)
    parts += arrow(690, 200, 530, 200, "taken", color=ROSE, dashed=True)
    parts += arrow(530, 408, 590, 408, "queued")
    parts.append(text(70, 540, "Each frame is a placeholder for a full sequence; the alt frame captures the lost-slot "
                               "and no-change branches.", size=11, fill=MUTED, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


def svg_timing():
    W, H = 960, 520
    parts = header(W, H, "Timing Diagram — Sync Retry Backoff",
                   "Duration-constrained state changes for one queue item under a transient 5xx.",
                   "[ANDROID-SOURCE] INITIAL_RETRY_DELAY_MS=1000, MAX=60000, budget=5, stale guard=5 min.")
    parts.append(f'<rect x="240" y="120" width="640" height="300" rx="8" fill="{BOX}" stroke="{LINE}" stroke-width="1.5"/>')
    lifelines = [("status", 170), ("retryCount", 240), ("timer", 310)]
    for name, y in lifelines:
        parts.append(text(60, y + 4, name, size=12, weight=600))
        parts.append(f'<line x1="240" y1="{y}" x2="880" y2="{y}" stroke="{MUTED}" stroke-width="1" stroke-dasharray="4 4"/>')
    # time axis (log-ish)
    t = [240, 340, 440, 570, 720, 880]
    labels = ["t0", "1s", "2s", "4s", "8s", "…60s"]
    for x, lab in zip(t, labels):
        parts.append(f'<line x1="{x}" y1="130" x2="{x}" y2="410" stroke="{BAND}" stroke-width="1"/>')
        parts.append(text(x, 148, lab, size=10, anchor="middle", fill=MUTED))
    # status segments
    segs = [(240, 340, 170, "SYNCING", HEAD), (340, 880, 170, "PENDING (backoff)", BOX2)]
    for x1, x2, y, lab, col in segs:
        parts.append(f'<rect x="{x1}" y="{y - 18}" width="{x2 - x1}" height="36" fill="{col}" opacity="0.85"/>')
        parts.append(text((x1 + x2) / 2, y + 4, lab, size=11, anchor="middle", fill=INK, weight=600, mono=False))
    # retryCount steps
    steps = [(240, 170, 240, 240), (340, 240, 440, 240), (440, 240, 570, 240), (570, 240, 720, 240)]
    parts.append(f'<polyline points="240,258 340,258 340,240 440,240 440,258 570,258 570,240 720,240 720,258 880,258" '
                 f'fill="none" stroke="{EMER}" stroke-width="2"/>')
    parts.append(text(560, 232, "retryCount 0 → 1 → 2 …", size=10, fill=EMER, anchor="middle", mono=False))
    # timer pulse
    for x in [340, 440, 570, 720]:
        parts.append(f'<line x1="{x}" y1="300" x2="{x}" y2="320" stroke="{ROSE}" stroke-width="2"/>')
        parts.append(f'<circle cx="{x}" cy="310" r="4" fill="{ROSE}"/>')
    parts.append(text(560, 350, "exponential timer fires; stale SYNCING rows requeue after 5 min", size=10,
                      fill=ROSE, anchor="middle", mono=False))
    parts.append(text(60, 460, "Authorization and schema faults never retry; transient 5xx retries up to five times.",
                      size=11, fill=MUTED, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


def svg_protocol():
    W, H = 940, 520
    parts = header(W, H, "Protocol State Machine — Sync Item Protocol",
                   "Signatures and guards that constrain when a sync item may accept a trigger.",
                   "[ANDROID-SOURCE] Protocol view of the verified SyncStatus transitions.")
    parts.append(marker())
    states = [
        (70, 180, 160, 70, "PENDING", "in: enqueue()", HEAD),
        (300, 180, 160, 70, "SYNCING", "in: dequeue()", HEAD2),
        (530, 130, 160, 70, "SYNCED", "in: ack()", EMER),
        (530, 300, 160, 70, "FAILED", "in: budgetSpent()", ROSE),
        (300, 360, 160, 70, "REQUEUE", "in: retry()", HEAD2),
    ]
    for x, y, w, h, name, proto, col in states:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{BOX}" stroke="{col}" stroke-width="2"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="28" rx="10" fill="{col}"/>')
        parts.append(text(x + w / 2, y + 19, name, size=13, fill="#ffffff", anchor="middle", weight=700))
        parts.append(text(x + 12, y + 50, proto, size=10, fill=MUTED, mono=False))
    parts.append(f'<circle cx="70" cy="215" r="8" fill="{EMER}"/>')
    parts += arrow(78, 215, 70, 215)
    parts += arrow(230, 215, 300, 215, "dequeue")
    parts += arrow(460, 200, 530, 165, "2xx")
    parts += arrow(460, 230, 530, 330, "5xx / retry<5", color=ROSE)
    parts += arrow(460, 215, 530, 215)
    parts += arrow(380, 360, 380, 250, "backoff", dashed=True)
    parts += arrow(530, 335, 460, 360, "budget spent", color=ROSE, dashed=True)
    parts.append(text(70, 470, "Protocol constrains accepted events per state; a stale SYNCING may be requeued by "
                               "the 5-minute guard without counting a failure.", size=11, fill=MUTED, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


# --------------------------------------------------------------------------
# ERD — generated from schema-model.json (SCHEMA-EXPORT evidence)
# --------------------------------------------------------------------------

DOMAINS = {
    "core-clinical": {
        "title": "ERD — Core Clinical Schema",
        "tables": ["patients", "patient_visits", "vaccination_items", "consultations", "patient_notes"],
        "subtitle": "Patients, visits, vaccination items, and consultations as reported by the metadata export.",
    },
    "inventory": {
        "title": "ERD — Inventory and Stock Schema",
        "tables": ["vaccines", "vaccine_batches", "inventory_transactions", "waste_records",
                   "borrow_records", "borrow_returns"],
        "subtitle": "Vaccine catalog, batches, movements, waste, and the borrow/return ledger.",
    },
    "finance": {
        "title": "ERD — Finance and Receipt Schema",
        "tables": ["finance_transactions", "expenses", "receipt_sequences", "reminders"],
        "subtitle": "Finance rows, expenses, the receipt counter, and vaccination reminders.",
    },
}


def _table(name):
    for t in SCHEMA["tables"]:
        if t["name"] == name:
            return t
    return None


def erd(key):
    cfg = DOMAINS[key]
    names = cfg["tables"]
    W = 1180
    # layout tables in a row-based grid
    per_row = 3
    colw, gapx, gapy = 320, 60, 60
    boxh_est = 240
    rows = (len(names) + per_row - 1) // per_row
    H = 150 + rows * (boxh_est + gapy)
    parts = header(W, H, cfg["title"], cfg["subtitle"],
                   "[SCHEMA-EXPORT] Reported by docs/Schemas CSV exports; not exercised against live Supabase.")
    parts.append(marker())
    positions = {}
    for i, name in enumerate(names):
        t = _table(name)
        if not t:
            continue
        r, c = divmod(i, per_row)
        x = 50 + c * (colw + gapx)
        y = 120 + r * (boxh_est + gapy)
        cols = t["columns"]
        rowh = 17
        h = 34 + len(cols) * rowh + 12
        pk = set(t["pk"] or [])
        parts.append(f'<rect x="{x}" y="{y}" width="{colw}" height="{h}" rx="8" fill="{BOX}" stroke="{LINE}" stroke-width="1.5"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="{colw}" height="28" rx="8" fill="{HEAD2}"/>')
        parts.append(text(x + 12, y + 19, name, size=12, fill="#ffffff", weight=700))
        if t["rls_enabled"]:
            parts.append(text(x + colw - 10, y + 19, "RLS", size=9, fill="#fed7aa", anchor="end", weight=700))
        cy = y + 46
        for col in cols:
            marker_ = "PK" if col["name"] in pk else ("FK" if any(col["name"] in (fk["columns"] or []) for fk in t["fks"]) else "")
            if marker_:
                parts.append(text(x + 12, cy, marker_, size=9, fill=HEAD if marker_ == "PK" else EMER, weight=700))
            nn = "" if col["nullable"] else " *"
            parts.append(text(x + 40, cy, f"{col['name']}{nn}", size=10, fill=INK))
            parts.append(text(x + colw - 10, cy, col["type"], size=9, fill=MUTED, anchor="end"))
            cy += rowh
        positions[name] = (x, y, colw, h)
    # FK edges (only within the drawn set)
    for name in names:
        t = _table(name)
        if not t:
            continue
        for fk in t["fks"]:
            ref = fk["ref_table"]
            if ref in positions and name in positions:
                x1, y1, w1, h1 = positions[name]
                x2, y2, w2, h2 = positions[ref]
                # connect right edge of child to left edge of parent if parent is to the right
                if x2 > x1:
                    parts += arrow(x1 + w1, y1 + h1 / 2, x2, y2 + h2 / 2, color=HEAD2, kind="diamond")
                elif x2 < x1:
                    parts += arrow(x1, y1 + h1 / 2, x2 + w2, y2 + h2 / 2, color=HEAD2, kind="diamond")
                else:
                    parts += arrow(x1 + w1 / 2, y1 + h1, x2 + w2 / 2, y2, color=HEAD2, kind="diamond")
    legend_y = H - 26
    parts.append(text(50, legend_y, "PK primary key · FK foreign key · * not-null · lines show foreign-key relationships "
                                    "(diamond = many-to-one). get_my_role() falls back to 'nurse'.",
                      size=11, fill=MUTED, mono=False))
    parts.extend(footer())
    return "\n".join(parts)


DIAGRAMS = {
    "structural/class-android-reference.svg": svg_class_android,
    "structural/class-desktop-proposed.svg": svg_class_desktop,
    "structural/package-android-reference.svg": svg_package_android,
    "structural/package-desktop-proposed.svg": svg_package_desktop,
    "structural/object-sync-queue-snapshot.svg": svg_object_diagram,
    "structural/composite-desktop-process.svg": svg_composite,
    "behavioral/use-case-clinic-roles.svg": svg_usecase,
    "behavioral/communication-vaccination-write.svg": svg_communication,
    "behavioral/interaction-overview-consultation.svg": svg_interaction_overview,
    "behavioral/timing-sync-retry.svg": svg_timing,
    "behavioral/protocol-state-sync-item.svg": svg_protocol,
    "data-and-flows/erd-core-clinical.svg": lambda: erd("core-clinical"),
    "data-and-flows/erd-inventory.svg": lambda: erd("inventory"),
    "data-and-flows/erd-finance.svg": lambda: erd("finance"),
}


def main():
    n = 0
    for rel, fn in DIAGRAMS.items():
        p = OUT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(fn(), encoding="utf-8")
        n += 1
        print(f"wrote {rel}")
    print(f"wrote {n} SVG diagrams")


if __name__ == "__main__":
    main()
