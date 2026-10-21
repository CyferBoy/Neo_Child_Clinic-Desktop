"""Follow-up, finance, receipt and reporting screens."""
from __future__ import annotations

from components import (
    alert, avatar, badge, btn, checkbox, donut, drawer_overlay, field, icon,
    icon_btn, kv_list, line_chart, metric, mini_bars, modal_overlay, page_head,
    pagination, search_input, select_field, shell_page, table, tabs, textarea,
    timeline, USER_ADMIN, USER_DOCTOR, USER_RECEPTION, USER_NURSE,
)

SCREENS = []


def add(**kwargs):
    kwargs.setdefault("dark_variant", False)
    kwargs.setdefault("wide_variant", False)
    SCREENS.append(kwargs)


def strip(label, value, foot, ic):
    return f'''<div class="card" style="flex:1;padding:10px 12px;display:flex;align-items:center;gap:10px"><span style="width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;background:var(--surface-3);color:var(--ink-600)">{icon(ic, 15)}</span><div><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">{label}</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700;line-height:1.1">{value} <span class="small muted" style="font-family:var(--font-body);font-weight:500">{foot}</span></div></div></div>'''


def revenue_mini():
    return f'''<div class="chart-card" style="padding:0"><div class="chart-head"><div><div class="chart-title">Collections trend</div><div class="chart-sub">Last 14 days · IST · fictional values</div></div><div class="card-action"><span class="badge success">{icon("trending-up", 10)} 12.4%</span></div></div>{line_chart([9200, 10800, 8400, 12200, 14600, 13200, 17400, 15800, 18200, 16100, 19400, 17600, 21800, 18450], ["7","8","9","10","11","12","13","14","15","16","17","18","19","20"], height=142, width=560)}</div>'''


# ---------------------------------------------------------------------------
# Vaccination reminders
# ---------------------------------------------------------------------------

def due_list_content():
    rows = [
        ("<div class='identity'><span class='avatar'>AS</span><div class='identity-main'><div class='identity-name'>Aarav Sharma</div><div class='identity-sub'>NCC-2026-00418 · 2y 4m</div></div></div>", "<div class='strong'>Pentavalent · dose 3</div><div class='sub'>DTwP-HepB-Hib</div>", "20 Oct 2026<span class='sub'>Today</span>", badge("Due today", "warning", "clock"), "V-10882", "Dr. Meera Nair", f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("<div class='identity'><span class='avatar success'>SK</span><div class='identity-main'><div class='identity-name'>Sara Khan</div><div class='identity-sub'>NCC-2025-00987 · 5y 2m</div></div></div>", "<div class='strong'>MMR · dose 1</div><div class='sub'>Measles, mumps, rubella</div>", "18 Oct 2026<span class='sub'>2 days overdue</span>", badge("Overdue", "danger", "alert-circle"), "V-10764", "Dr. Nikhil Verma", f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("<div class='identity'><span class='avatar info'>IG</span><div class='identity-main'><div class='identity-name'>Ishaan Gupta</div><div class='identity-sub'>NCC-2026-00488 · 1y 2m</div></div></div>", "<div class='strong'>PCV · booster</div><div class='sub'>Pneumococcal conjugate</div>", "20 Oct 2026<span class='sub'>Today</span>", badge("Due today", "warning", "clock"), "V-10844", "Dr. Meera Nair", f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("<div class='identity'><span class='avatar apricot'>AR</span><div class='identity-main'><div class='identity-name'>Anaya Reddy</div><div class='identity-sub'>NCC-2026-00323 · 4y 1m</div></div></div>", "<div class='strong'>Hepatitis B · dose 2</div><div class='sub'>Paediatric schedule</div>", "21 Oct 2026<span class='sub'>Tomorrow</span>", badge("Upcoming", "info", "calendar"), "V-10901", "Dr. Nikhil Verma", f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("<div class='identity'><span class='avatar'>MJ</span><div class='identity-main'><div class='identity-name'>Myra Joshi</div><div class='identity-sub'>NCC-2026-00210 · 6y</div></div></div>", "<div class='strong'>Influenza · annual</div><div class='sub'>Seasonal</div>", "23 Oct 2026<span class='sub'>In 3 days</span>", badge("Upcoming", "info", "calendar"), "V-10908", "Dr. Meera Nair", f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("<div class='identity'><span class='avatar info'>VN</span><div class='identity-main'><div class='identity-name'>Vivaan Nair</div><div class='identity-sub'>NCC-2025-01102 · 3y 7m</div></div></div>", "<div class='strong'>Varicella · dose 2</div><div class='sub'>Live attenuated</div>", "16 Oct 2026<span class='sub'>4 days overdue</span>", badge("Overdue", "danger", "alert-circle"), "V-10799", "Dr. Nikhil Verma", f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
    ]
    content = f'''{page_head("Follow-up · vaccination reminders", "Due vaccinations", "IST due boundaries, terminal reminder states and a clear path from due item to patient context.", btn("New reminder", "primary", "bell") + btn("Export due list", "secondary", "download"))}
    <div class="row tight" style="margin-bottom:12px">{strip("Overdue", "2", "oldest 4 days", "alert-circle")}{strip("Due today", "5", "2 already arrived", "clock")}{strip("Next 7 days", "16", "reminders", "calendar")}{strip("Completed this week", "23", "audited", "check-circle")}</div>
    <div style="margin-bottom:10px">{tabs([("All active", "23"), ("Overdue", "2"), ("Today", "5"), ("Next 7 days", "16"), ("Completed", None), ("Dismissed", None)], 0, extra=f'<span class="spacer" style="flex:1"></span><span class="small muted">{icon("bell", 12)} Desktop notifications enabled · quiet hours 20:00–08:00</span>')}</div>
    <div class="toolbar">{search_input("Search patient, vaccine or clinic ID")}<span class="spacer"></span><span class="toolbar-select">All vaccines {icon("chevron-down", 12)}</span><span class="toolbar-select">Assigned: anyone {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
    <div class="table-card">{table(["Patient", "Vaccine / dose", "Due", "Status", "Source visit", "Assigned to", ""], rows, widths=["w-name", "w-name", "w-date", "w-status", "w-date", "", "w-actions"])}{pagination("1–6 of 23 active reminders", ("‹","1","2","3","›"))}</div>
'''
    return content


def due_list():
    return shell_page("REM-001", "Due vaccinations", USER_NURSE, due_list_content(), attention=7)


def reminder_detail_drawer():
    base = due_list_content()
    drawer = f'''<div class="drawer" role="dialog" aria-modal="true" aria-labelledby="reminder-title">
      <div class="drawer-head"><div><div class="drawer-title" id="reminder-title">Vaccination reminder</div><div class="drawer-sub">Aarav Sharma · Pentavalent dose 3</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="drawer-body">
        <div class="patient-ribbon" style="padding:10px"><div class="identity"><span class="avatar">AS</span><div><div class="identity-name">Aarav Sharma</div><div class="identity-sub">NCC-2026-00418 · 2y 4m</div></div></div></div>
        <div class="mt-12">{kv_list([("Vaccine", "Pentavalent · dose 3"), ("Due", "20 Oct 2026 · IST"), ("Status", badge("Active · due today", "warning", "clock")), ("Source visit", "V-10882 · 18 Jun 2026"), ("Assigned to", "Dr. Meera Nair"), ("Notification", "Today · delivered 08:00")])}</div>
        <div class="divider"></div>
        <div class="label">Complete this reminder</div>
        <div class="form-grid mt-8">{field("Performed date", "20 Oct 2026", icon_name="calendar")}{select_field("Performed by", "Nurse Ritika Sen")}{select_field("Outcome", "Vaccination recorded")}{textarea("Completion note", "Recorded against the visit created today.", width="full")}</div>
        <div class="alert info mt-12">{icon("link", 15)}<div><strong>Completion is terminal.</strong> If a stale device reopens this reminder, the completed state wins. A correction must use the vaccination workflow.</div></div>
        <div class="divider"></div>
        <div class="label">History</div>
        {timeline([{"title":"Reminder created","time":"18 Jun 2026","body":"From vaccination visit V-10882","tone":"neutral"},{"title":"Notification delivered","time":"20 Oct · 08:00","body":"Desktop · no duplicate for same due item/day","tone":"success"}])}
      </div>
      <div class="drawer-foot"><button class="btn ghost" type="button">Dismiss</button><div class="spacer"></div><button class="btn" type="button">Reschedule</button><button class="btn primary" type="button">Open patient</button></div>
    </div>'''
    return drawer_overlay(base, "REM-001", "Due vaccinations", USER_NURSE, drawer)


def personal_reminder_list_content():
    rows = [
        ("<div class='identity'><span class='avatar'>AS</span><div class='identity-main'><div class='identity-name'>Aarav Sharma</div><div class='identity-sub'>Linked patient · NCC-2026-00418</div></div></div>", "Call parent about PCV booster", "PCV", "₹0", "21 Oct 2026", "Kavya Iyer", badge("Pending", "warning"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar info'>SK</span><div class='identity-main'><div class='identity-name'>Sara Khan</div><div class='identity-sub'>Linked patient · NCC-2025-00987</div></div></div>", "Follow up after missed MMR", "MMR", "₹500", "20 Oct 2026", "Dr. Meera Nair", badge("Pending", "warning"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar apricot'>RK</span><div class='identity-main'><div class='identity-name'>Riya Kapoor</div><div class='identity-sub'>Walk-in · +91 98450 77112</div></div></div>", "Call about influenza availability", "Influenza", "₹0", "—", "Kavya Iyer", badge("Undated", "neutral"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar success'>VN</span><div class='identity-main'><div class='identity-name'>Vivaan Nair</div><div class='identity-sub'>Linked patient · NCC-2025-01102</div></div></div>", "Confirm varicella dose 2 appointment", "Varicella", "₹0", "22 Oct 2026", "Dr. Nikhil Verma", badge("Pending", "warning"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar'>MJ</span><div class='identity-main'><div class='identity-name'>Myra Joshi</div><div class='identity-sub'>Linked patient · NCC-2026-00210</div></div></div>", "Advance received for influenza", "Influenza", "₹500", "23 Oct 2026", "Kavya Iyer", badge("Completed", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
    ]
    content = f'''{page_head("Follow-up · personal reminders", "Personal reminders", "Non-clinical follow-ups with an optional patient link, advance amount and explicit status.", btn("New personal reminder", "primary", "plus", href="REM-004.html"))}
    <div class="alert warning">{icon("alert-triangle", 15)}<div><strong>Advance amounts are informational.</strong> They are not clinic income unless a separate approved payment record links them. This design does not post an advance as income.</div></div>
    <div style="margin-bottom:10px;margin-top:12px">{tabs([("Pending", "8"), ("Completed", "14"), ("Cancelled", "2"), ("All", "24")], 0, extra=f'<span class="spacer" style="flex:1"></span><span class="small muted">Separate from clinical vaccination due reminders</span>')}</div>
    <div class="toolbar">{search_input("Search name, phone, note or vaccine interest")}<span class="spacer"></span><span class="toolbar-select">Assigned: anyone {icon("chevron-down", 12)}</span><span class="toolbar-select">Date: all {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
    <div class="table-card">{table(["Person", "Reminder", "Vaccine interest", "Advance", "Date", "Owner", "Status", ""], rows, widths=["w-name", "", "w-date", "w-money", "w-date", "", "w-status", "w-actions"])}{pagination("1–5 of 8 pending", ("‹","1","2","›"))}</div>
    <div class="alert info mt-12">{icon("info", 15)}<div>An undated reminder is allowed only when notifications are explicitly off. Blank dates must never notify repeatedly.</div></div>'''
    return content


def personal_reminder_list():
    return shell_page("REM-003", "Personal reminders", USER_RECEPTION, personal_reminder_list_content(), attention=7)


def personal_reminder_form_content():
    right = f'''<div class="col tight w-side">
      <div class="card"><div class="card-head"><div class="card-title">Notification preview</div></div><div class="card-body"><div class="notice-item" style="background:var(--surface)"><div class="n-icon" style="background:var(--brand-50);color:var(--brand-700)">{icon("bell", 13)}</div><div><div class="n-title">Personal reminder · 21 Oct</div><div class="n-text">Call parent about PCV booster · assigned to Kavya Iyer</div></div></div><div class="help mt-8">Notification uses IST. No SMS or WhatsApp message is sent from this screen.</div></div></div>
      <div class="card"><div class="card-head"><div class="card-title">Rules</div></div><div class="card-body" style="padding-top:8px"><div class="stat-line">{icon("check-circle", 13)}<span>Patient link optional</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Name + phone if unlinked</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Advance ≥ 0</span></div><div class="stat-line">{icon("alert-circle", 13)}<span>Blank date needs explicit undated</span></div></div></div>
      {alert("Advance is not income. Posting it requires a separately approved finance transaction.", "warning", "info")}
    </div>'''
    content = f'''{page_head("Personal reminders · new", "Create a personal reminder", "Track a non-clinical follow-up without mixing it into clinical due reminders or income.", btn("Cancel", "ghost", href="REM-003.html") + btn("Save reminder", "primary", "check"))}
    <div class="row top">
      <div class="grow col">
        <div class="form-section"><div class="form-section-head">{icon("user", 15)}<div class="form-section-title">Who is this about?</div></div><div class="form-section-body"><div class="form-grid">{field("Linked patient", "Aarav Sharma · NCC-2026-00418", icon_name="search", help_text="Optional. When linked, use the stable patient ID.")}{field("Patient name", "", placeholder="Required if not linked", help_text="Unlinked walk-in name.")}{field("Phone", "", placeholder="+91 00000 00000", icon_name="phone")}</div></div></div>
        <div class="form-section"><div class="form-section-head">{icon("bell", 15)}<div class="form-section-title">Follow-up</div></div><div class="form-section-body"><div class="form-grid">{field("Reminder", "Call parent about PCV booster", required=True, width="full")}{select_field("Vaccine interest", "PCV")}{field("Advance amount", "₹0", icon_name="banknote", help_text="Informational only; not posted as income.")}{field("Reminder date", "21 Oct 2026", icon_name="calendar")}{select_field("Assigned to", "Kavya Iyer · Receptionist")}{textarea("Note", "Parent asked for a call after 4 pm. Confirm PCV booster availability.", width="full")}</div>{checkbox("Save as undated · notifications off", checked=False)}</div></div>
      </div>
      {right}
    </div>'''
    return content


def personal_reminder_form():
    return shell_page("REM-003", "Personal reminders", USER_RECEPTION, personal_reminder_form_content(), attention=7)


add(id="REM-001", name="Due vaccinations", slug="due-vaccinations", section="Follow-up", feature="Vaccination Reminders",
    source="10-Vaccination-Reminders.md", purpose="Show active, overdue and upcoming vaccination reminders using IST boundaries and role-relevant ownership.",
    users="Admin, doctor, nurse, receptionist", permissions="View/complete/dismiss per policy; admin can reschedule/override with audit.",
    entry="Sidebar Due vaccinations; dashboard due widget; notification deep link.", navigation="Open reminder detail; reschedule; complete; dismiss; open patient.",
    layout=["Page header", "Summary strip", "Status tabs", "Search/filter toolbar", "Reminder table", "IST and terminal-state note"],
    components=["Summary cards", "Tabs", "Table", "Status badges", "Notification status"],
    data=["2 overdue", "5 due today", "16 in 7 days", "23 completed this week", "Fictional patients"],
    actions=["New reminder", "Export", "Open reminder", "Filter"],
    forms=["Search", "Vaccine filter", "Assignee filter"],
    states=["Loading", "Empty", "Ready", "Overdue", "Completed", "Dismissed", "Pending sync", "Notification permission denied"],
    offline="Local due list and status transitions; notifications local; terminal states must win over stale active updates.",
    keyboard="/ search; table rows open; tabs arrow-key semantics.",
    a11y="Due state uses text and dates; overdue not color-only; external timezone note.",
    deps="REM-001–006; notifications; sync; patients; vaccinations.",
    open="Retention/legal status requirements, reschedule limits, dismissal roles, SMS/WhatsApp scope, deletion reconciliation contract.",
    notes="Reminder deletion/absence reconciliation (NCC-023) remains unresolved; the UI does not promise resurrection protection beyond terminal state handling.",
    html=due_list())

add(id="REM-002", name="Vaccination reminder detail", slug="vaccination-reminder-detail", section="Follow-up", feature="Vaccination Reminders",
    source="10-Vaccination-Reminders.md", purpose="Act on one reminder with explicit completion, dismissal or reschedule and preserve prior state in history.",
    users="Clinical roles; admin override", permissions="Complete/dismiss per policy; reschedule admin or approved role.",
    entry="Due list row; notification.", navigation="Open patient; reschedule; dismiss; complete. Close returns to list.",
    layout=["Due list context behind scrim", "Right drawer", "Patient context", "Reminder details", "Completion form", "History"],
    components=["Drawer", "Patient ribbon", "Key-value details", "Completion fields", "Timeline"],
    data=["Aarav Sharma", "Pentavalent dose 3", "Due 20 Oct 2026", "Notification delivered 08:00"],
    actions=["Open patient", "Reschedule", "Dismiss", "Complete"],
    forms=["Performed date", "Performed by", "Outcome", "Completion note"],
    states=["Ready", "Completing", "Dismissal reason required", "Conflict/stale state", "Offline", "Permission denied"],
    offline="Local completion/dismissal and outbox; terminal state wins on sync.",
    keyboard="Focus enters drawer; Escape closes; actions in logical order.",
    a11y="Drawer labelled dialog; completion status text; history ordered list.",
    deps="REM-001/003/004; vaccinations; notifications; audit.",
    open="Whether a completed reminder can be reopened and who may dismiss it.",
    notes="The UI states that completion is terminal; corrections go through the vaccination workflow.",
    html=reminder_detail_drawer())

add(id="REM-003", name="Personal reminders", slug="personal-reminders", section="Follow-up", feature="Personal Reminders",
    source="11-Personal-Reminders.md", purpose="Track non-clinical follow-ups separately from vaccination due reminders and clinic income.",
    users="Admin, doctor, receptionist, nurse", permissions="Clinical/reception create; admin override; finance role required to post any advance as income.",
    entry="Sidebar Personal reminders; patient profile Add reminder.", navigation="New reminder; filter pending/completed/cancelled; open detail.",
    layout=["Page header", "Advance/income warning", "Status tabs", "Search/filter toolbar", "Personal reminder table", "Undated note"],
    components=["Warning alert", "Tabs", "Table", "Status badges", "Advance amount column"],
    data=["8 pending", "14 completed", "2 cancelled", "₹500 informational advance", "Fictional people"],
    actions=["New personal reminder", "Filter", "Open detail"],
    forms=["Search", "Assignee filter", "Date filter"],
    states=["Loading", "Empty", "Pending", "Completed", "Cancelled", "Undated", "Conflict"],
    offline="Local create/status and outbox; no network needed for notification scheduling.",
    keyboard="/ search; table rows open; status tabs.",
    a11y="Advance warning in text; status labels; phone/name fallback clear.",
    deps="PER-001–005; notifications; finance; patients.",
    open="Is an advance a real financial transaction? Who owns assignment? Are messages in scope? Can reminders be undated?",
    notes="This list does not create income. Advance amounts are explicitly informational.",
    html=personal_reminder_list())

add(id="REM-004", name="Create personal reminder", slug="create-personal-reminder", section="Follow-up", feature="Personal Reminders",
    source="11-Personal-Reminders.md", purpose="Create a dated or explicitly undated personal follow-up with optional patient linkage and informational advance.",
    users="Clinical/reception roles", permissions="Create per role; finance posting separate.",
    entry="Personal reminders New reminder.", navigation="Save → list. Cancel → list.",
    layout=["Page header", "Person form", "Follow-up form", "Notification preview rail", "Rules"],
    components=["Patient link/name/phone", "Reminder text", "Vaccine interest", "Advance amount", "Date/undated", "Assignee", "Note"],
    data=["Aarav Sharma linked", "PCV interest", "₹0 advance", "21 Oct 2026"],
    actions=["Save reminder", "Cancel"],
    forms=["Linked patient (optional)", "Name + phone if unlinked", "Reminder (required)", "Vaccine interest", "Advance ≥ 0", "Date or explicit undated", "Assignee", "Note"],
    states=["Ready", "Saving", "Blank date warning", "Invalid amount", "Offline", "Conflict"],
    offline="Local create/outbox; notifications scheduled locally using IST.",
    keyboard="Form order; undated checkbox; save shortcut documented.",
    a11y="Required unlinked fields clear; notification preview text; no PHI in placeholder.",
    deps="PER-001–005; notifications; finance boundary.",
    open="Advance/refund semantics, assignment ownership, messaging scope and undated support.",
    notes="No advance is posted as income here.",
    html=personal_reminder_form())


# ---------------------------------------------------------------------------
# Finance
# ---------------------------------------------------------------------------

def finance_overview_content():
    rows = [
        ("20 Oct 2026 · 09:05", "Aarav Sharma", "Vaccination · V-10942", "₹2,050", badge("Cash + online", "success"), badge("Pending sync", "info", "refresh")),
        ("20 Oct 2026 · 08:58", "Diya Menon", "Vaccination · V-10938", "₹1,200", badge("Online", "info"), badge("Synced", "success")),
        ("19 Oct 2026 · 17:05", "Myra Joshi", "Consultation · C-2081", "₹600", badge("Online", "info"), badge("Synced", "success")),
        ("19 Oct 2026 · 15:12", "Ishaan Gupta", "Vaccination · V-10936", "₹1,450", badge("Mixed", "neutral"), badge("Synced", "success")),
        ("18 Oct 2026 · 11:20", "Sara Khan", "Vaccination · V-10918", "₹0", badge("Free dose", "success"), badge("Synced", "success")),
    ]
    content = f'''{page_head("Business · finance", "Finance overview", "Visit income, expenses and reconciliation with one income count per visit.", btn("Record payment", "primary", "wallet", href="FIN-004.html") + btn("Record expense", "secondary", "banknote", href="FIN-006.html") + btn("Export", "secondary", "download"))}
    <div class="grid-4" style="margin-bottom:12px">
      {metric("Today's income", "₹18,450", "12 payments · 11 synced", "wallet", hint="success:+12%")}
      {metric("Today's expenses", "₹4,280", "3 entries", "banknote")}
      {metric("Net today", "₹14,170", "Cash ₹8,920 · Online ₹5,250", "trending-up", hint="success:Positive")}
      {metric("Receivable / pending", "₹1,200", "1 provisional receipt", "receipt", variant="warn", hint="warning:Review")}
    </div>
    <div class="row" style="height:252px">
      <div class="card grow" style="display:flex;flex-direction:column"><div class="card-head"><div><div class="card-title">Collections</div><div class="card-sub">Today by payment method</div></div><span class="badge success">{icon("trending-up", 10)} 12.4% vs last Tue</span></div><div class="card-body" style="padding-top:2px">{revenue_mini()}</div></div>
      <div class="card w-side-sm"><div class="card-head"><div><div class="card-title">Today's mix</div><div class="card-sub">Payment method</div></div></div><div class="card-body"><div class="donut-wrap">{donut([(11200, "var(--chart-1)"), (7250, "var(--chart-3)")], "₹18,450", "collected")}<div class="legend" style="flex-direction:column;align-items:flex-start;gap:8px"><span><i style="background:var(--chart-1)"></i>Cash <strong style="color:var(--ink-900)">₹11,200</strong></span><span><i style="background:var(--chart-3)"></i>Online <strong style="color:var(--ink-900)">₹7,250</strong></span><span class="muted">Cash + online = total</span></div></div></div></div>
    </div>
    <div class="row tight mt-12">
      <div class="card grow"><div class="card-head"><div><div class="card-title">Recent transactions</div><div class="card-sub">Income and expense ledger</div></div><div class="card-action">{btn("View all", "ghost sm", "arrow-right", href="FIN-002.html")}</div></div><div style="padding:0">{table(["Time", "Patient / payee", "Reference", "Amount", "Method", "Status"], rows, widths=["w-date", "w-name", "", "w-money", "w-status", "w-status"])}</div></div>
      <div class="card w-side-sm"><div class="card-head"><div><div class="card-title">Expenses today</div><div class="card-sub">3 entries</div></div></div><div class="card-body"><div class="stat-line"><span>Cold-chain supplies</span><span class="spacer" style="flex:1"></span><strong class="mono">₹2,180</strong></div><div class="stat-line"><span>Courier</span><span class="spacer" style="flex:1"></span><strong class="mono">₹600</strong></div><div class="stat-line"><span>Housekeeping</span><span class="spacer" style="flex:1"></span><strong class="mono">₹1,500</strong></div><div class="divider"></div><div class="summary-line"><span>Total expenses</span><strong class="mono">₹4,280</strong></div><div class="mt-8">{btn("View expenses", "ghost sm", "arrow-right", href="FIN-005.html")}</div></div></div>
    </div>'''
    return content


def finance_overview():
    return shell_page("FIN-001", "Finance", USER_ADMIN, finance_overview_content(), status="Syncing", status_tone="syncing")


def transactions_content():
    rows = [
        ("20 Oct 2026<span class='sub'>09:05</span>", "Aarav Sharma<span class='sub'>NCC-2026-00418</span>", "Vaccination · V-10942", "₹2,050.00", "₹1,500 / ₹550", badge("Cash + online", "success"), "Provisional", badge("Pending sync", "info", "refresh"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("20 Oct 2026<span class='sub'>08:58</span>", "Diya Menon<span class='sub'>NCC-2026-00502</span>", "Vaccination · V-10938", "₹1,200.00", "₹0 / ₹1,200", badge("Online", "info"), "NCC-R-004196", badge("Synced", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("19 Oct 2026<span class='sub'>17:05</span>", "Myra Joshi<span class='sub'>NCC-2026-00210</span>", "Consultation · C-2081", "₹600.00", "₹0 / ₹600", badge("Online", "info"), "NCC-R-004195", badge("Synced", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("19 Oct 2026<span class='sub'>15:12</span>", "Ishaan Gupta<span class='sub'>NCC-2026-00488</span>", "Vaccination · V-10936", "₹1,450.00", "₹1,000 / ₹450", badge("Mixed", "neutral"), "NCC-R-004191", badge("Synced", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("18 Oct 2026<span class='sub'>11:20</span>", "Sara Khan<span class='sub'>NCC-2025-00987</span>", "Vaccination · V-10918", "₹0.00", "₹0 / ₹0", badge("Free dose", "success"), "NCC-R-004182", badge("Synced", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("18 Oct 2026<span class='sub'>10:05</span>", "Vivaan Nair<span class='sub'>NCC-2025-01102</span>", "Consultation · C-2076", "₹500.00", "₹500 / ₹0", badge("Cash", "neutral"), "NCC-R-004179", badge("Synced", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
            ]
    content = f'''{page_head("Business · finance", "Transactions", "Every income row links to a visit and reconciles cash + online to the amount.", btn("Record payment", "primary", "wallet", href="FIN-004.html") + btn("Export", "secondary", "download"))}
    <div class="row tight" style="margin-bottom:12px">{strip("Income today", "₹18,450", "12 payments", "wallet")}{strip("Cash", "₹11,200", "61%", "banknote")}{strip("Online", "₹7,250", "39%", "credit-card")}{strip("Pending receipts", "1", "provisional", "receipt")}</div>
    <div style="margin-bottom:10px">{tabs([("Income", "1,284"), ("Expenses", "316"), ("Pending sync", "2"), ("Provisional receipts", "1")], 0, extra=f'<span class="spacer" style="flex:1"></span><span class="small muted">One income row per visit · no double count</span>')}</div>
    <div class="toolbar">{search_input("Search patient, visit, receipt or amount")}<span class="spacer"></span><span class="toolbar-select">Today {icon("chevron-down", 12)}</span><span class="toolbar-select">All methods {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
    <div class="table-card">{table(["Date", "Patient", "Reference", "Amount", "Cash / online", "Method", "Receipt", "Status", ""], rows, widths=["w-date", "w-name", "w-date", "w-money", "w-money", "w-status", "w-date", "w-status", "w-actions"])}{pagination("1–7 of 1,284 income rows", ("‹","1","2","3","…","161","›"))}</div>
    <div class="help mt-8">{icon("lock", 12)} Role-scoped data; the renderer receives formatted minor-unit values and does not calculate money.</div>'''
    return content


def transactions():
    return shell_page("FIN-002", "Transactions", USER_ADMIN, transactions_content(), status="Syncing", status_tone="syncing")


def transaction_detail_content():
    content = f'''{page_head("Transaction · PAY-40871", "Payment detail", "Aarav Sharma · vaccination visit V-10942", btn("View receipt", "secondary", "receipt", href="RCP-001.html") + btn("Edit payment", "secondary", "edit") + icon_btn("more", "More payment actions"))}
    <div class="row top">
      <div class="grow col">
        <div class="card"><div class="card-head"><div><div class="card-title">Payment</div><div class="card-sub">Linked to one visit and one vaccination income row</div></div><span class="badge warning">Provisional receipt</span></div><div class="card-body"><div class="row"><div class="grow"><div class="tiny muted">AMOUNT</div><div class="amount-in">₹2,050.00</div><div class="small muted mt-4">Cash ₹1,500.00 · Online ₹550.00</div></div><div><div class="tiny muted">METHOD</div><div class="mt-4">{badge("Cash + online", "success")}</div></div><div><div class="tiny muted">STATUS</div><div class="mt-4">{badge("Pending sync", "info", "refresh")}</div></div></div><div class="divider"></div>{kv_list([("Visit", "V-10942 · Vaccination"), ("Patient", "Aarav Sharma · NCC-2026-00418"), ("Receipt", "Provisional · server number pending"), ("Recorded by", "Kavya Iyer · 20 Oct 2026 · 09:05 IST"), ("Income identity", "Deterministic per visit"), ("Balance", "₹0.00")])}</div></div>
        <div class="card"><div class="card-head"><div class="card-title">Linked service</div><span class="badge info">One visit</span></div><div class="card-body" style="padding:0">{table(["Service", "Qty", "Amount"], [["Pentavalent dose 3 · AV-2409", "1", "₹850.00"], ["Rotavirus dose 2 · RV-2408", "1", "₹1,200.00"]], widths=["", "w-money", "w-money"])}</div><div class="card-foot" style="display:flex"><span class="muted small">Amount must equal the receipt line total.</span><span style="flex:1"></span><strong class="mono">₹2,050.00</strong></div></div>
        <div class="alert warning">{icon("alert-triangle", 15)}<div><strong>Edits preserve this payment identity.</strong> A change updates the same visit income row; it must not create a duplicate. Refunds/corrections require an explicit audited workflow.</div></div>
      </div>
      <div class="col tight w-side">
        <div class="card"><div class="card-head"><div class="card-title">Audit</div></div><div class="card-body">{timeline([{"title":"Payment created","time":"09:05","body":"Kavya Iyer · ₹2,050 · local commit","tone":"success"},{"title":"Receipt number requested","time":"09:05","body":"Server assignment pending","tone":"warning"},{"title":"Visit group queued","time":"09:06","body":"Upload after related stock/reminder rows","tone":"neutral"}])}</div></div>
        <div class="card"><div class="card-head"><div class="card-title">Related</div></div><div class="card-body" style="display:flex;flex-direction:column;gap:6px">{btn("Open vaccination visit", "secondary", "syringe", size="sm")} {btn("Open patient", "ghost", "user", size="sm")} {btn("Open finance report", "ghost", "chart", size="sm")}</div></div>
        {alert("Receipt number is immutable and server-assigned. This preview never invents a number.", "info", "info")}
      </div>
    </div>'''
    return content


def transaction_detail():
    return shell_page("FIN-002", "Payment detail", USER_ADMIN, transaction_detail_content(), status="Syncing", status_tone="syncing")


def payment_form_content():
    right = f'''<div class="col tight w-side">
      <div class="sticky-summary"><div class="small muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Payment total</div><div class="total mt-4">₹2,050.00</div><div class="summary-line"><span>Cash</span><strong>₹1,500.00</strong></div><div class="summary-line"><span>Online</span><strong>₹550.00</strong></div><div class="summary-line total-line"><span>Allocated</span><strong>₹2,050.00</strong></div><div class="summary-line"><span>Remaining</span><strong class="amount-positive">₹0.00</strong></div></div>
      <div class="card"><div class="card-head"><div class="card-title">Reconciliation</div><span class="badge success">{icon("check", 10)} Balanced</span></div><div class="card-body" style="padding-top:8px"><div class="stat-line">{icon("check-circle", 13)}<span>Cash + online = amount</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Visit linked</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Single income row</span></div><div class="stat-line">{icon("alert-circle", 13)}<span>Receipt awaits server</span></div></div></div>
      {alert("Money is handled as integer minor units by the trusted core. The renderer never computes authoritative totals.", "info", "info")}
    </div>'''
    content = f'''{page_head("Finance · record payment", "Record a payment", "Link income to one visit; split cash and online without creating a duplicate income row.", btn("Cancel", "ghost", href="FIN-001.html") + btn("Save payment", "primary", "check"))}
    <div class="patient-ribbon"><div class="identity"><span class="avatar lg">AS</span><div><div class="identity-name" style="font-size:15px">Aarav Sharma</div><div class="identity-sub">NCC-2026-00418 · 2y 4m · visit V-10942</div></div></div><span class="badge info">Vaccination visit</span><span class="spacer" style="flex:1"></span><span class="small muted">Cash + online = amount</span></div>
    <div class="row top mt-12">
      <div class="grow col">
        <div class="form-section"><div class="form-section-head">{icon("wallet", 15)}<div class="form-section-title">Payment</div><span class="badge neutral">INR</span></div><div class="form-section-body"><div class="form-grid">{field("Amount", "₹2,050.00", required=True, icon_name="banknote")}{select_field("Payment status", "Paid")}{field("Cash", "₹1,500.00", icon_name="banknote")}{field("Online", "₹550.00", icon_name="credit-card")}{select_field("Online reference", "UPI · 20 Oct 2026", width="full")}</div><div class="alert success mt-12">{icon("check-circle", 15)}<div>Cash + online equals the amount due. Method is derived as <strong>Cash + online</strong>.</div></div><div class="mt-12">{field("Payment note", "Balance settled at reception; provisional receipt offered.")}</div><div class="help mt-8">{icon("lock", 12)} Receipt number is server-assigned after sync; no local number is generated.</div></div></div>
      </div>
      {right}
    </div>'''
    return content


def payment_form():
    return shell_page("FIN-001", "Record payment", USER_RECEPTION, payment_form_content(), status="Online")


def expenses_content():
    rows = [
        ("20 Oct 2026", "Cold-chain supplies", "Ice packs and temperature logger", "₹2,180.00", badge("UPI", "info"), "UPI-882041", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("20 Oct 2026", "Courier", "Vaccine delivery · Bharat Biotech", "₹600.00", badge("Cash", "neutral"), "—", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("20 Oct 2026", "Housekeeping", "Monthly deep clean", "₹1,500.00", badge("Cash", "neutral"), "HK-1024", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("18 Oct 2026", "Utilities", "Electricity · September", "₹8,420.00", badge("Online", "info"), "ELEC-0918", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("16 Oct 2026", "Medical supplies", "Syringes and alcohol swabs", "₹3,660.00", badge("UPI", "info"), "UPI-881002", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("12 Oct 2026", "Rent", "Clinic premises · October", "₹45,000.00", badge("Online", "info"), "RENT-OCT", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("10 Oct 2026", "Maintenance", "Refrigerator service", "₹2,400.00", badge("Cash", "neutral"), "—", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
    ]
    content = f'''{page_head("Business · finance", "Expenses", "Record and review clinic expenses separately from visit income, with category and method required.", btn("Record expense", "primary", "banknote", href="FIN-006.html") + btn("Export", "secondary", "download"))}
    <div class="row tight" style="margin-bottom:12px">{strip("This month", "₹63,760", "18 entries", "banknote")}{strip("Today", "₹4,280", "3 entries", "wallet")}{strip("Cash share", "₹4,500", "7%", "banknote")}{strip("Pending sync", "0", "all synced", "refresh")}</div>
    <div class="toolbar">{search_input("Search title, category or reference")}<span class="spacer"></span><span class="toolbar-select">All categories {icon("chevron-down", 12)}</span><span class="toolbar-select">This month {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
    <div class="table-card">{table(["Date", "Category", "Title", "Amount", "Method", "Reference", "Status", ""], rows, widths=["w-date", "", "", "w-money", "w-status", "w-date", "w-status", "w-actions"])}{pagination("1–6 of 18 expenses", ("‹","1","2","3","›"))}</div>
    <div class="help mt-8">{icon("info", 12)} Expenses are excluded from visit income; a negative income edit is not a refund workflow.</div>'''
    return content


def expenses():
    return shell_page("FIN-005", "Expenses", USER_ADMIN, expenses_content())


def expense_form_content():
    right = f'''<div class="col tight w-side">
      <div class="card"><div class="card-head"><div class="card-title">Expense summary</div></div><div class="card-body"><div class="summary-line"><span>Amount</span><strong class="mono">₹2,180.00</strong></div><div class="summary-line"><span>Method</span><strong>UPI</strong></div><div class="summary-line"><span>Category</span><strong>Cold-chain supplies</strong></div><div class="summary-line total-line"><span>Posted to</span><strong>Expenses · October</strong></div></div></div>
      <div class="card"><div class="card-head"><div class="card-title">Rules</div></div><div class="card-body" style="padding-top:8px"><div class="stat-line">{icon("check-circle", 13)}<span>Date required</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Category and title required</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Amount &gt; 0</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Method required</span></div></div></div>
      {alert("Editing an expense after reporting is audited. Refunds and discounts are not part of this design until approved.", "warning", "info")}
    </div>'''
    content = f'''{page_head("Finance · record expense", "Record an expense", "Keep clinic costs separate from visit income and receipts.", btn("Cancel", "ghost", href="FIN-005.html") + btn("Save expense", "primary", "check"))}
    <div class="row top">
      <div class="grow col">
        <div class="form-section"><div class="form-section-head">{icon("banknote", 15)}<div class="form-section-title">Expense details</div></div><div class="form-section-body"><div class="form-grid">{field("Date", "20 Oct 2026", required=True, icon_name="calendar")}{select_field("Category", "Cold-chain supplies", required=True)}{field("Title", "Ice packs and temperature logger", required=True, width="full")}{field("Amount", "₹2,180.00", required=True, icon_name="banknote")}{select_field("Payment method", "UPI")}{field("Reference", "UPI-882041", help_text="Optional, length-bounded.")}{textarea("Note", "Reorder placed for outreach camp. Invoice attached to the monthly finance folder.", width="full")}</div></div></div>
        <div class="form-section"><div class="form-section-head">{icon("upload", 15)}<div class="form-section-title">Supporting document</div><span class="badge neutral">Optional</span></div><div class="form-section-body"><div class="upload-zone">{icon("upload", 20)}<div class="strong">Drop a receipt image or browse</div><div>PDF, PNG or JPG · local-only preview in this prototype</div></div></div></div>
      </div>
      {right}
    </div>'''
    return content


def expense_form():
    return shell_page("FIN-005", "Record expense", USER_ADMIN, expense_form_content())


add(id="FIN-001", name="Finance overview", slug="finance-overview", section="Finance", feature="Finance and Payments",
    source="12-Finance-and-Payments.md", purpose="Give finance-authorized staff a same-day view of income, expenses, net and reconciliation risk.",
    users="Admin, doctor, receptionist (income); expenses admin/doctor", permissions="Finance permission scoped; reports restricted by role.",
    entry="Sidebar Finance; dashboard collections widget.", navigation="Record payment; record expense; transactions; expenses; reports.",
    layout=["Page header", "Four metric cards", "Collections chart", "Payment mix", "Recent transactions", "Expenses today"],
    components=["Metric cards", "Line chart", "Donut", "Tables", "Quick actions"],
    data=["₹18,450 income", "₹4,280 expenses", "₹14,170 net", "₹1,200 pending", "Fictional payments"],
    actions=["Record payment", "Record expense", "Export", "View all"],
    forms=[],
    states=["Loading", "Empty day", "Ready", "Pending sync", "Permission denied", "Stale/partial data"],
    offline="Local aggregates labelled with pending/stale state; never claim a complete day while writes are pending.",
    keyboard="Chart has text alternative; actions reachable; tables use headers.",
    a11y="Money values tabular and labelled; donut has legend/text; color not sole method.",
    deps="FIN-001–006; RCP; RPT; visit income identity.",
    open="Refunds/discounts, expense edit roles, payment reference storage and money schema migration.",
    notes="Totals are illustrative. One visit income row is counted once.",
    html=finance_overview())

add(id="FIN-002", name="Transactions", slug="transactions", section="Finance", feature="Finance and Payments",
    source="12-Finance-and-Payments.md", purpose="Review visit-linked income rows, payment split, receipt status and pending local commits.",
    users="Admin, doctor, receptionist", permissions="Finance access role-scoped.",
    entry="Finance overview; reports drill-down.", navigation="Open payment; filter; export; record payment.",
    layout=["Page header", "Summary strip", "Tabs", "Search/filter toolbar", "Transactions table", "Role-scope note"],
    components=["Tabs", "Table", "Status badges", "Money columns", "Pagination"],
    data=["1,284 income rows", "₹18,450 today", "Cash/online split", "1 provisional receipt"],
    actions=["Record payment", "Export", "Open payment", "Filter"],
    forms=["Search", "Date range", "Payment method"],
    states=["Loading", "Empty", "Ready", "Pending sync", "Provisional receipt", "Permission denied"],
    offline="Local transactions visible; pending and provisional badges explicit.",
    keyboard="/ search; table rows open; numeric values readable.",
    a11y="Cash/online columns labelled; receipt status text; no color-only meaning.",
    deps="FIN-003/004; RCP; visits; reports.",
    open="Refund/void workflows, payment references and expense edit permissions.",
    notes="This list is income-first; expenses live in their own view.",
    html=transactions())

add(id="FIN-003", name="Payment detail", slug="payment-detail", section="Finance", feature="Finance and Payments",
    source="12-Finance-and-Payments.md", purpose="Show one visit-linked payment, its split, receipt state, linked service and audit identity.",
    users="Finance-authorized staff", permissions="Role-scoped; receipt access required.",
    entry="Transactions list; receipt preview; visit detail.", navigation="View receipt; edit payment; open visit/patient/report.",
    layout=["Page header", "Payment summary card", "Linked services", "Edit warning", "Audit rail", "Related actions"],
    components=["Summary", "Key-value list", "Service table", "Audit timeline", "Status badges"],
    data=["PAY-40871", "₹2,050", "Cash ₹1,500 / Online ₹550", "Provisional receipt", "Aarav Sharma"],
    actions=["View receipt", "Edit payment", "Open visit", "Open patient"],
    forms=[],
    states=["Ready", "Pending sync", "Receipt conflict", "Edited", "Permission denied"],
    offline="Local read; provisional receipt; conflict does not renumber.",
    keyboard="Actions reachable; receipt link labelled.",
    a11y="Payment split text; audit ordered; balance label.",
    deps="FIN-002/004/006; RCP; audit.",
    open="Refund/correction workflow and receipt void policy.",
    notes="The page never presents a locally computed receipt number.",
    html=transaction_detail())

add(id="FIN-004", name="Record payment", slug="record-payment", section="Finance", feature="Finance and Payments",
    source="12-Finance-and-Payments.md", purpose="Record or update one visit-linked income row with a reconciled cash/online split.",
    users="Admin, doctor, receptionist", permissions="Income recording proposed for these roles.",
    entry="Finance overview/transactions; visit detail.", navigation="Save → payment detail/transactions. Cancel → finance.",
    layout=["Page header", "Patient ribbon", "Payment form", "Receipt/note", "Payment summary rail", "Reconciliation rail"],
    components=["Money fields", "Payment status", "Online reference", "Balanced alert", "Integer-minor-unit note"],
    data=["Aarav Sharma", "₹2,050", "Cash ₹1,500 / Online ₹550", "Receipt pending"],
    actions=["Save payment", "Cancel"],
    forms=["Amount (required)", "Payment status", "Cash (non-negative)", "Online (non-negative)", "Cash + online = amount", "Online reference", "Note"],
    states=["Ready", "Saving", "Mismatch", "Duplicate income", "Receipt issued", "Offline", "Permission denied"],
    offline="Local record/outbox; receipt finalization waits for server; conflict visible.",
    keyboard="Form order; money values announced as text; save shortcut documented.",
    a11y="Balanced/mismatch in text; amount fields labelled with currency; no color-only error.",
    deps="FIN-001–006; RCP; visits; integer money handling.",
    open="Refunds/discounts, partial payments and expense edit roles.",
    notes="The renderer displays values; the Go core owns authoritative arithmetic.",
    html=payment_form())

add(id="FIN-005", name="Expenses", slug="expenses", section="Finance", feature="Finance and Payments",
    source="12-Finance-and-Payments.md", purpose="List, search and filter clinic expenses separately from visit income.",
    users="Admin, doctor; receptionist may record but not edit (open)", permissions="Expense management role policy unresolved.",
    entry="Finance overview; sidebar finance.", navigation="Record expense; filter; export.",
    layout=["Page header", "Summary strip", "Search/filter toolbar", "Expense table", "Income separation note"],
    components=["Summary cards", "Table", "Status badges", "Method badge", "Pagination"],
    data=["₹63,760 this month", "18 entries", "₹4,280 today", "7 fictional rows"],
    actions=["Record expense", "Export", "Filter"],
    forms=["Search", "Category", "Date range"],
    states=["Loading", "Empty", "Ready", "Pending sync", "Permission denied"],
    offline="Local expense list and outbox.",
    keyboard="/ search; table rows open; filters accessible.",
    a11y="Money and method labels; status text.",
    deps="FIN-001/006; reports; audit.",
    open="Who can edit expenses after reporting? Receipt attachment storage policy?",
    notes="Expenses are not netted into visit income rows.",
    html=expenses())

add(id="FIN-006", name="Record expense", slug="record-expense", section="Finance", feature="Finance and Payments",
    source="12-Finance-and-Payments.md", purpose="Capture a valid expense with date, category, title, positive amount and method.",
    users="Admin, doctor, receptionist (record only; edit open)", permissions="Admin/doctor manage; reception record may be permitted.",
    entry="Expenses list; finance overview.", navigation="Save → expenses. Cancel → finance.",
    layout=["Page header", "Expense form", "Supporting document", "Summary rail", "Rules"],
    components=["Date/category/title", "Amount/method/reference", "Upload zone", "Summary", "Warning"],
    data=["Cold-chain supplies", "₹2,180", "UPI", "UPI-882041"],
    actions=["Save expense", "Cancel", "Upload supporting document"],
    forms=["Date (required)", "Category (required)", "Title (required)", "Amount > 0 (required)", "Method (required)", "Reference", "Note", "Attachment (optional)"],
    states=["Ready", "Saving", "Validation", "Duplicate", "Offline", "Permission denied"],
    offline="Local expense/outbox; attachment handling and storage policy unresolved.",
    keyboard="Upload accessible by keyboard; form order; errors linked.",
    a11y="Amount label; upload instructions; no color-only validation.",
    deps="FIN-005; audit; reports.",
    open="Receipt attachment storage, expense edit roles, refunds/discounts.",
    notes="Supporting document is shown as an optional local preview, not an implemented upload.",
    html=expense_form())


# ---------------------------------------------------------------------------
# Receipts
# ---------------------------------------------------------------------------

def receipt_preview_content():
    receipt = f'''<div class="receipt-paper">
      <div style="display:flex;align-items:flex-start;gap:10px"><div style="width:34px;height:34px;border-radius:9px;background:#0f5d64;color:#fff;display:flex;align-items:center;justify-content:center">{icon("logo", 18)}</div><div><div class="strong" style="font-family:var(--font-display);font-size:15px">Neo Child Clinic</div><div class="receipt-small">12, 4th Cross, Indiranagar · Bengaluru 560038<br>+91 80 4123 7788 · GSTIN 29ABCDE1234F1Z5</div></div><div style="margin-left:auto;text-align:right"><div class="badge success">PAID</div><div class="receipt-small mt-4">Original</div></div></div>
      <div class="r-rule"></div>
      <h3>Vaccination receipt</h3>
      <div class="receipt-sub">Receipt NCC-R-004182 · 20 Oct 2026 · 09:05 IST</div>
      <div style="display:flex;gap:16px;margin-top:14px"><div style="flex:1"><div class="receipt-small">PATIENT</div><div class="strong">Aarav Sharma</div><div class="receipt-small">NCC-2026-00418</div></div><div style="flex:1"><div class="receipt-small">VISIT</div><div class="strong">V-10942 · Vaccination</div><div class="receipt-small">Given by Dr. Meera Nair</div></div></div>
      <div class="r-rule"></div>
      <table class="receipt-table"><thead><tr><td>DESCRIPTION</td><td style="text-align:right">AMOUNT</td></tr></thead><tbody><tr><td>Pentavalent dose 3 · batch AV-2409</td><td>₹850.00</td></tr><tr><td>Rotavirus dose 2 · batch RV-2408</td><td>₹1,200.00</td></tr></tbody></table>
      <div class="r-rule"></div>
      <div style="margin-left:auto;width:220px"><div class="summary-line"><span>Subtotal</span><strong>₹2,050.00</strong></div><div class="summary-line"><span>Discount</span><strong>₹0.00</strong></div><div class="receipt-total"><span>Total paid</span><span>₹2,050.00</span></div><div class="summary-line mt-8"><span>Cash</span><strong>₹1,500.00</strong></div><div class="summary-line"><span>Online</span><strong>₹550.00</strong></div></div>
      <div class="r-rule"></div>
      <div style="display:flex;align-items:flex-end;gap:14px"><div class="receipt-small" style="flex:1">Linked to visit V-10942 · payment PAY-40871. Receipt numbers are server-assigned and immutable. Please retain for your records.</div><div class="qr-box" style="width:40px;height:40px"></div></div>
      <div style="border-top:1px solid #d7e2e0;margin-top:10px;padding-top:6px;display:flex;justify-content:space-between" class="receipt-small"><span>Printed 20 Oct 2026 · 09:07 · Page 1 of 1</span><span>Thank you</span></div>
    </div>'''
    content = f'''{page_head("Receipts · NCC-R-004182", "Receipt preview", "Final receipt number assigned by the shared backend; printing does not change the payment.", btn("Print receipt", "primary", "printer") + btn("Save PDF", "secondary", "download") + btn("Reprint", "secondary", "copy", href="RCP-003.html"))}
    <div class="row top">
      <div class="grow" style="display:flex;justify-content:center">{receipt}</div>
      <div class="col tight w-side-sm">
        <div class="card"><div class="card-head"><div class="card-title">Receipt status</div><span class="badge success">Final</span></div><div class="card-body" style="padding-top:8px">{kv_list([("Receipt", "NCC-R-004182"), ("Visit", "V-10942"), ("Payment", "PAY-40871"), ("Amount", "₹2,050.00")])}<div class="help mt-8">Assigned by server · 20 Oct 2026 09:05 · not yet printed.</div></div></div>
        <div class="card"><div class="card-head"><div class="card-title">Print settings</div></div><div class="card-body">{select_field("Printer", "Reception A4", width="full")}<div class="mt-8">{select_field("Paper", "A4 · portrait", width="full")}</div><div class="mt-8">{checkbox("Print duplicate marker on reprint", checked=False)}</div><div class="help mt-8">Prints only the fields shown; no extra PHI is added.</div><div class="mt-8">{btn("Print receipt", "primary", "printer", size="sm")}</div></div></div>
      </div>
    </div>'''
    return content


def receipt_preview():
    return shell_page("RCP-001", "Receipt preview", USER_RECEPTION, receipt_preview_content(), status="Online")


def print_queue_content():
    content = f'''{page_head("Receipts · print queue", "Print queue", "Handle printer failures without losing the payment or changing the receipt number.", btn("Retry print", "primary", "refresh") + btn("Choose printer", "secondary", "settings"))}
    <div class="row top">
      <div class="grow col">
        <div class="card"><div class="card-head"><div><div class="card-title">Print job · NCC-R-004182</div><div class="card-sub">Aarav Sharma · ₹2,050.00 · final receipt</div></div><span class="badge danger">Printer error</span></div><div class="card-body">{alert("The printer did not respond. The payment and receipt number are safe; retry after checking paper and connection.", "danger", "alert-triangle")}<div class="row tight mt-12"><div class="grow">{kv_list([("Printer", "Reception A4"), ("Status", "Offline · last seen 09:05"), ("Attempts", "2"), ("Queued", "20 Oct 2026 · 09:07")])}</div><div class="grow">{kv_list([("Receipt number", "NCC-R-004182"), ("Payment", "PAY-40871 · Paid"), ("Amount", "₹2,050.00"), ("Reprint", "Not yet printed")])}</div></div><div class="row tight mt-12">{btn("Retry print", "primary", "refresh")} {btn("Choose another printer", "secondary", "settings")} {btn("Save as PDF", "secondary", "download")}</div></div></div>
        <div class="card"><div class="card-head"><div><div class="card-title">Print history</div><div class="card-sub">Reprints are audited and use the original number.</div></div></div><div class="card-body">{timeline([{"title":"Printer did not respond","time":"09:07","body":"No pages produced; payment unchanged","tone":"danger"},{"title":"Retry requested","time":"09:08","body":"Waiting for printer selection","tone":"warning"}])}</div></div>
      </div>
      <div class="col tight w-side-sm">
        <div class="card"><div class="card-head"><div class="card-title">Print options</div></div><div class="card-body">{select_field("Printer", "Reception A4", width="full")}<div class="mt-8">{select_field("Paper size", "A4", width="full")}</div><div class="mt-8">{checkbox("Print duplicate marker", checked=False)}</div></div></div>
        {alert("If the receipt is already printed, use Reprint. Do not create a new payment.", "warning", "info")}
      </div>
    </div>'''
    return content


def print_queue():
    return shell_page("RCP-001", "Print queue", USER_RECEPTION, print_queue_content(), status="Attention", status_tone="attention")


def reprint_dialog():
    base = receipt_preview_content()
    modal = f'''<div class="dialog narrow" role="dialog" aria-modal="true" aria-labelledby="reprint-title">
      <div class="dialog-head"><div class="dialog-icon warning">{icon("copy", 18)}</div><div><div class="dialog-title" id="reprint-title">Reprint this receipt?</div><div class="dialog-sub">NCC-R-004182 · original receipt number</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        <p class="muted" style="font-size:11.5px;line-height:1.55">A reprint uses the original server-assigned number. It is marked as a duplicate and written to the audit log.</p>
        <div class="mt-12">{kv_list([("Receipt", "NCC-R-004182"), ("Visit", "V-10942"), ("Amount", "₹2,050.00"), ("Original print", "20 Oct 2026 · 09:07")])}</div>
        <div class="field mt-12"><label>Reason for reprint <span class="req">*</span></label><div class="select"><span>Patient copy damaged</span>{icon("chevron-down", 14)}</div></div>
        <div class="check-row mt-8"><span class="checkbox checked">{icon("check", 10)}</span><span class="check-text">Mark as duplicate and keep the original receipt number.</span></div>
      </div>
      <div class="dialog-foot"><button class="btn ghost" type="button">Cancel</button><div class="spacer"></div><button class="btn primary" type="button">Reprint duplicate</button></div>
    </div>'''
    return modal_overlay(base, "RCP-001", "Receipt preview", USER_RECEPTION, modal)


add(id="RCP-001", name="Receipt preview", slug="receipt-preview", section="Receipts", feature="Receipts and Printing",
    source="13-Receipts-and-Printing.md", purpose="Preview a final, server-numbered receipt linked to the visit and payment before printing or saving a copy.",
    users="Admin, doctor, receptionist", permissions="Print proposed for these roles; void/reprint role policy unresolved.",
    entry="Payment detail; vaccination/consultation detail; receipt queue.", navigation="Print; save PDF; reprint; back to payment.",
    layout=["Page header", "Centered receipt paper", "Receipt status rail", "Print settings", "Privacy note"],
    components=["Receipt document", "Status key-values", "Printer settings", "Reprint link"],
    data=["NCC-R-004182", "Aarav Sharma", "V-10942", "₹2,050", "Cash/online split"],
    actions=["Print receipt", "Save PDF", "Reprint", "Change printer"],
    forms=["Printer (required for print)", "Paper size", "Duplicate marker (reprint only)"],
    states=["Provisional (blocked final print)", "Ready/final", "Printing", "Printer error", "Printed", "Reprint"],
    offline="Final print is blocked until the server assigns a receipt number. A provisional preview must be labelled.",
    keyboard="Print settings reachable before print; receipt text selectable; focus returns after dialog.",
    a11y="Document heading hierarchy; table has headers; amounts labelled; screen readers can read receipt text.",
    deps="RCP-001–005; finance; visits; local print bridge.",
    open="Offline final receipt legality, template/legal text, void/reprint policy, PDF export requirement.",
    notes="The receipt number is server-assigned; the preview cannot create one. Clinic details are fictional.",
    html=receipt_preview())

add(id="RCP-002", name="Print queue error", slug="print-queue-error", section="Receipts", feature="Receipts and Printing",
    source="13-Receipts-and-Printing.md", purpose="Recover from printer failure without losing the payment or issuing a different receipt number.",
    users="Admin, doctor, receptionist", permissions="Print/reprint role policy.",
    entry="Print request failure; receipt queue.", navigation="Retry; choose printer; save PDF; return to receipt.",
    layout=["Page header", "Failed job card", "Job/payment details", "Print history", "Safety rail", "Print options"],
    components=["Error alert", "Key-values", "Timeline", "Printer select", "Actions"],
    data=["NCC-R-004182", "PAY-40871", "₹2,050", "2 attempts", "Reception A4 offline"],
    actions=["Retry print", "Choose another printer", "Save as PDF", "Print test page"],
    forms=["Printer", "Paper size", "Duplicate marker"],
    states=["Printer offline", "Paper out", "Retrying", "Printed", "Spool failure"],
    offline="Print job is retained; payment remains recorded. A server-numbered receipt may be previewed but not newly numbered.",
    keyboard="Actions reachable; printer selection keyboard accessible; error announced.",
    a11y="Error in text, not color-only; payment safety stated; print history ordered.",
    deps="RCP-001/003; print bridge; audit.",
    open="Spool retention and failure-recovery policy.",
    notes="Printer failure does not change payment or receipt identity.",
    html=print_queue())

add(id="RCP-003", name="Reprint receipt", slug="reprint-receipt", section="Receipts", feature="Receipts and Printing",
    source="13-Receipts-and-Printing.md", purpose="Reprint with the original number, a duplicate marker and an audit reason.",
    users="Admin, doctor, receptionist", permissions="Reprint/void requires audit and role policy.",
    entry="Receipt preview Reprint.", navigation="Reprint → print queue/preview. Cancel → receipt.",
    layout=["Receipt preview behind scrim", "Narrow dialog", "Original receipt context", "Reason", "Duplicate acknowledgement"],
    components=["Dialog", "Key-values", "Reason select", "Duplicate checkbox"],
    data=["NCC-R-004182", "Original print time", "₹2,050"],
    actions=["Reprint duplicate", "Cancel"],
    forms=["Reprint reason (required)", "Duplicate marker acknowledgement"],
    states=["Ready", "Permission denied", "Printer error", "Already printed", "Voided record"],
    offline="Reprint requires the original receipt record; final number must be server-assigned.",
    keyboard="Focus trap; explicit duplicate acknowledgement; Escape cancel.",
    a11y="Reason and consequence text; no color-only warning.",
    deps="RCP-001/002; audit; print bridge.",
    open="Who can reprint/void; duplicate marking policy; void-after-refund.",
    notes="Reprint never changes the receipt number.",
    html=reprint_dialog())


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------

def reports_overview_content():
    content = f'''{page_head("Insight · statistics", "Statistics & reports", "Trustworthy operational and financial reports with explicit IST windows and drill-down to source records.", btn("Export report", "secondary", "download") + btn("Print", "secondary", "printer"))}
    <div class="row tight" style="align-items:center;margin-bottom:12px"><span class="badge brand">October 2026</span><span class="toolbar-select">01–20 Oct 2026 {icon("chevron-down", 12)}</span><span class="toolbar-select">All vaccines {icon("chevron-down", 12)}</span><span class="spacer" style="flex:1"></span><span class="small muted">{icon("info", 12)} IST · excludes archived records</span></div>
    <div class="grid-4" style="margin-bottom:12px">{metric("Visits", "248", "20 days · 12.4/day", "users", hint="success:+8%")}{metric("Vaccinations", "312", "1.26 per visit", "syringe")}{metric("Income", "₹3.86L", "cash ₹2.14L · online ₹1.72L", "wallet", hint="success:+11%")}{metric("Expenses", "₹63,760", "18 entries", "banknote")}</div>
    <div class="row" style="height:268px">
      <div class="card grow"><div class="card-head"><div><div class="card-title">Income & expenses</div><div class="card-sub">Daily totals · 1–20 October 2026</div></div><div class="legend"><span><i style="background:var(--chart-1)"></i>Income</span><span><i style="background:var(--chart-4)"></i>Expenses</span></div></div><div class="card-body">{line_chart([14200, 15800, 15100, 18400, 17200, 21000, 19800, 20400, 18900, 22600, 21800, 23900, 23100, 24500], ["1","4","7","10","13","16","19","20"], height=164, width=650)}</div></div>
      <div class="card w-side-sm"><div class="card-head"><div><div class="card-title">Top vaccines</div><div class="card-sub">Doses administered</div></div></div><div class="card-body">{mini_bars([86, 72, 54, 38, 31, 21], ["Penta","PCV","Rota","MMR","Hep B","Var"], alt_every=True)}</div></div>
    </div>
    <div class="row tight mt-12">
      <div class="card grow"><div class="card-head"><div><div class="card-title">Report views</div><div class="card-sub">Drill into the same source records</div></div></div><div class="card-body"><div class="grid-2"><div>{btn("Vaccination report", "secondary", "syringe", href="RPT-002.html")} <span class="small muted">Brand, dose and batch detail</span></div><div>{btn("Finance report", "secondary", "wallet", href="RPT-003.html")} <span class="small muted">Income, expenses and payment split</span></div><div class="mt-12">{btn("Patient milestones", "secondary", "baby")} <span class="small muted">Due/overdue populations</span></div><div class="mt-12">{btn("Full report", "secondary", "file")} <span class="small muted">Combined operational summary</span></div></div></div></div>
      <div class="card w-side-sm"><div class="card-head"><div><div class="card-title">Data health</div><span class="badge warning">Stale</span></div></div><div class="card-body"><div class="stat-line">{icon("refresh", 13)}<span>2 writes pending</span></div><div class="stat-line">{icon("receipt", 13)}<span>1 provisional receipt</span></div><div class="stat-line">{icon("trash", 13)}<span>Archived records excluded</span></div><div class="help mt-8">The month is not presented as complete while writes are pending.</div></div></div>
    </div>'''
    return content


def reports_overview():
    return shell_page("RPT-001", "Statistics & reports", USER_DOCTOR, reports_overview_content(), status="Syncing", status_tone="syncing")


def vaccination_report_content():
    rows = [
        ("Pentavalent", "DTwP-HepB-Hib", "86", "₹73,100", "3 brands", badge("27.6%", "success"), "AV-2409"),
        ("PCV", "Pneumococcal conjugate", "72", "₹2,77,200", "2 brands", badge("23.1%", "success"), "PCV-2411"),
        ("Rotavirus", "Oral rotavirus", "54", "₹56,700", "3 brands", badge("17.3%", "neutral"), "RV-2408"),
        ("MMR", "Measles, mumps, rubella", "38", "₹31,920", "1 brand", badge("5.5%", "neutral"), "MMR-2404"),
        ("Hepatitis B", "Hepatitis B", "31", "₹10,540", "2 brands", badge("4.5%", "neutral"), "HB-2403"),
        ("Varicella", "Live attenuated", "21", "₹34,020", "1 brand", badge("3.0%", "neutral"), "VAR-2407"),
        ("Influenza", "Seasonal influenza", "10", "₹9,800", "2 brands", badge("1.4%", "warning"), "FLU-2405"),
    ]
    content = f'''{page_head("Insight · vaccination report", "Vaccination report", "Doses, income and batch usage grouped by stable vaccine identity · 01–20 Oct 2026.", btn("Export CSV", "secondary", "download") + btn("Print report", "secondary", "printer"))}
    <div class="row tight" style="margin-bottom:12px"><span class="badge brand">01–20 Oct 2026</span><span class="toolbar-select">All brands {icon("chevron-down", 12)}</span><span class="toolbar-select">All statuses {icon("chevron-down", 12)}</span><span class="spacer" style="flex:1"></span><span class="small muted">Counts exclude archived patients and soft-deleted visits</span></div>
    <div class="grid-4" style="margin-bottom:12px">{metric("Doses", "312", "in selected window", "syringe")}{metric("Vaccination income", "₹4.93L", "one row per visit", "wallet")}{metric("Average dose price", "₹1,580", "weighted", "banknote")}{metric("Batches used", "14", "FEFO preferred", "package")}</div>
    <div class="row" style="height:190px"><div class="card grow"><div class="card-head"><div><div class="card-title">Doses by vaccine</div><div class="card-sub">Click a bar to inspect source visits in the full implementation</div></div></div><div class="card-body">{mini_bars([86, 72, 54, 38, 31, 21, 10], ["Penta","PCV","Rota","MMR","Hep B","Var","Flu"], alt_every=True)}</div></div><div class="card w-side-sm"><div class="card-head"><div><div class="card-title">Brand mix</div><div class="card-sub">Pentavalent</div></div></div><div class="card-body"><div class="donut-wrap">{donut([(52, "var(--chart-1)"), (24, "var(--chart-2)"), (10, "var(--chart-3)")], "86", "doses")}<div class="legend" style="flex-direction:column;align-items:flex-start;gap:7px"><span><i style="background:var(--chart-1)"></i>Pentavac SD · 52</span><span><i style="background:var(--chart-2)"></i>Easyfive · 24</span><span><i style="background:var(--chart-3)"></i>Others · 10</span></div></div></div></div></div>
    <div class="table-card standalone mt-12">{table(["Vaccine", "Category", "Doses", "Income", "Brands", "Share", "Top batch"], rows[:3], widths=["w-name", "", "w-money", "w-money", "w-date", "w-status", "w-date"])}{pagination("3 of 7 vaccine groups · 312 doses", ("‹","1","2","3","›"))}</div>
'''
    return content


def vaccination_report():
    return shell_page("RPT-001", "Vaccination report", USER_DOCTOR, vaccination_report_content(), status="Syncing", status_tone="syncing")


def finance_report_content():
    rows = [
        ("20 Oct 2026", "₹18,450", "₹4,280", "₹14,170", "₹11,200", "₹7,250", badge("Pending", "info")),
        ("19 Oct 2026", "₹21,800", "₹8,420", "₹13,380", "₹9,400", "₹12,400", badge("Synced", "success")),
        ("18 Oct 2026", "₹17,600", "₹2,400", "₹15,200", "₹8,600", "₹9,000", badge("Synced", "success")),
        ("17 Oct 2026", "₹19,400", "₹3,660", "₹15,740", "₹10,200", "₹9,200", badge("Synced", "success")),
        ("16 Oct 2026", "₹16,100", "₹0", "₹16,100", "₹8,700", "₹7,400", badge("Synced", "success")),
        ("15 Oct 2026", "₹18,200", "₹18,000", "₹200", "₹9,100", "₹9,100", badge("Synced", "success")),
        ("14 Oct 2026", "₹15,800", "₹1,500", "₹14,300", "₹8,300", "₹7,500", badge("Synced", "success")),
    ]
    content = f'''{page_head("Insight · finance report", "Finance report", "Income, expenses and payment split with one income count per visit · 01–20 Oct 2026.", btn("Export CSV", "secondary", "download") + btn("Print report", "secondary", "printer"))}
    <div class="row tight" style="margin-bottom:12px"><span class="badge brand">01–20 Oct 2026</span><span class="toolbar-select">All payment methods {icon("chevron-down", 12)}</span><span class="spacer" style="flex:1"></span><span class="small muted">Excludes archived records · not a complete month</span></div>
    <div class="grid-4" style="margin-bottom:12px">{metric("Income", "₹3.86L", "248 visits", "wallet")}{metric("Expenses", "₹63,760", "18 entries", "banknote")}{metric("Net", "₹3.22L", "income minus expenses", "trending-up", hint="success:Positive")}{metric("Pending", "₹1,200", "1 provisional receipt", "receipt", variant="warn")}</div>
    <div class="row" style="height:155px"><div class="card grow"><div class="card-head"><div><div class="card-title">Income vs expenses</div><div class="card-sub">Daily · IST</div></div><div class="legend"><span><i style="background:var(--chart-1)"></i>Income</span><span><i style="background:var(--chart-4)"></i>Expenses</span></div></div><div class="card-body">{line_chart([14200, 15800, 15100, 18400, 17200, 21000, 19800, 20400, 18900, 22600, 21800, 23900, 23100, 24500], ["1","4","7","10","13","16","19","20"], height=152, width=600)}</div></div><div class="card w-side-sm"><div class="card-head"><div><div class="card-title">Payment split</div><div class="card-sub">Income in window</div></div></div><div class="card-body"><div class="donut-wrap">{donut([(214000, "var(--chart-1)"), (172000, "var(--chart-3)")], "₹3.86L", "income")}<div class="legend" style="flex-direction:column;align-items:flex-start;gap:7px"><span><i style="background:var(--chart-1)"></i>Cash · 55.4%</span><span><i style="background:var(--chart-3)"></i>Online · 44.6%</span><span class="muted">Cash + online = income</span></div></div></div></div></div>
    <div class="table-card standalone mt-12">{table(["Date", "Income", "Expenses", "Net", "Cash", "Online", "Status"], rows[:3], widths=["w-date", "w-money", "w-money", "w-money", "w-money", "w-money", "w-status"])}{pagination("1–3 of 20 daily rows · 2 writes pending", ("‹","1","2","3","›"))}</div>
'''
    return content


def finance_report():
    return shell_page("RPT-001", "Finance report", USER_DOCTOR, finance_report_content(), status="Syncing", status_tone="syncing")


def milestone_report_content():
    rows = [
        ("<div class='identity'><span class='avatar'>AS</span><div><div class='identity-name'>Aarav Sharma</div><div class='identity-sub'>NCC-2026-00418 · 2y 4m</div></div></div>", "Pentavalent dose 3", "20 Oct 2026", "Today", badge("Due", "warning", "clock"), "Dr. Meera Nair"),
        ("<div class='identity'><span class='avatar success'>SK</span><div><div class='identity-name'>Sara Khan</div><div class='identity-sub'>NCC-2025-00987 · 5y 2m</div></div></div>", "MMR dose 1", "18 Oct 2026", "2 days", badge("Overdue", "danger", "alert-circle"), "Dr. Nikhil Verma"),
        ("<div class='identity'><span class='avatar info'>IG</span><div><div class='identity-name'>Ishaan Gupta</div><div class='identity-sub'>NCC-2026-00488 · 1y 2m</div></div></div>", "PCV booster", "20 Oct 2026", "Today", badge("Due", "warning", "clock"), "Dr. Meera Nair"),
        ("<div class='identity'><span class='avatar apricot'>AR</span><div><div class='identity-name'>Anaya Reddy</div><div class='identity-sub'>NCC-2026-00323 · 4y 1m</div></div></div>", "Hepatitis B dose 2", "21 Oct 2026", "Tomorrow", badge("Upcoming", "info", "calendar"), "Dr. Nikhil Verma"),
        ("<div class='identity'><span class='avatar success'>DM</span><div><div class='identity-name'>Diya Menon</div><div class='identity-sub'>NCC-2026-00502 · 8m</div></div></div>", "Rotavirus dose 2", "24 Oct 2026", "4 days", badge("Upcoming", "info", "calendar"), "Dr. Meera Nair"),
        ("<div class='identity'><span class='avatar info'>VN</span><div><div class='identity-name'>Vivaan Nair</div><div class='identity-sub'>NCC-2025-01102 · 3y 7m</div></div></div>", "Varicella dose 2", "16 Oct 2026", "4 days", badge("Overdue", "danger", "alert-circle"), "Dr. Nikhil Verma"),
    ]
    content = f'''{page_head("Insight · patient milestones", "Patient milestone report", "Due and overdue populations for the selected window, with drill-down to the patient record.", btn("Export CSV", "secondary", "download") + btn("Print report", "secondary", "printer"))}
    <div class="row tight" style="margin-bottom:12px"><span class="badge brand">20–27 Oct 2026</span><span class="toolbar-select">All vaccines {icon("chevron-down", 12)}</span><span class="toolbar-select">All milestones {icon("chevron-down", 12)}</span><span class="spacer" style="flex:1"></span><span class="small muted">Active patients only · IST</span></div>
    <div class="grid-4" style="margin-bottom:12px">{metric("Due this week", "23", "7 days", "calendar")}{metric("Overdue", "2", "oldest 4 days", "alert-circle", variant="danger")}{metric("Completed", "23", "this week", "check-circle", hint="success:On track")}{metric("Coverage", "87%", "due items completed", "shield")}</div>
    <div class="row" style="height:170px"><div class="card grow"><div class="card-head"><div><div class="card-title">Milestone status</div><div class="card-sub">Children with at least one due item</div></div></div><div class="card-body">{mini_bars([23, 2, 23, 8], ["Due this week","Overdue","Completed","No contact"], alt_every=True)}</div></div><div class="card w-side-sm"><div class="card-head"><div><div class="card-title">By vaccine</div><div class="card-sub">Due in selected window</div></div></div><div class="card-body"><div class="stat-line"><span>Pentavalent</span><span class="spacer" style="flex:1"></span><strong>9</strong></div><div class="stat-line"><span>PCV</span><span class="spacer" style="flex:1"></span><strong>6</strong></div><div class="stat-line"><span>MMR</span><span class="spacer" style="flex:1"></span><strong>4</strong></div><div class="stat-line"><span>Hepatitis B</span><span class="spacer" style="flex:1"></span><strong>3</strong></div><div class="stat-line"><span>Other</span><span class="spacer" style="flex:1"></span><strong>1</strong></div><div class="mt-8">{btn("Open due list", "ghost sm", "arrow-right", href="REM-001.html")}</div></div></div></div>
    <div class="table-card standalone mt-12">{table(["Patient", "Milestone", "Due", "Days", "Status", "Assigned"], rows[:3], widths=["w-name", "", "w-date", "w-date", "w-status", "w-date"])}{pagination("1–3 of 23 due items", ("‹","1","2","3","4","›"))}</div>'''
    return content


def milestone_report():
    return shell_page("RPT-001", "Patient milestone report", USER_DOCTOR, milestone_report_content())


add(id="RPT-001", name="Statistics overview", slug="statistics-overview", section="Reports", feature="Statistics and Reports",
    source="15-Statistics-and-Reports.md", purpose="Provide role-restricted operational and financial aggregates with explicit IST windows, stale labels and drill-down.",
    users="Admin, doctor", permissions="Admin/doctor only (proposed); export may be admin-only.",
    entry="Sidebar Reports; dashboard insights.", navigation="Vaccination report; finance report; patient milestones; full report; export.",
    layout=["Page header", "Date/filter bar", "Four metric cards", "Income/expense line chart", "Top vaccines bars", "Report view links", "Data health"],
    components=["Metric cards", "Line chart", "Bar chart", "Drill-down links", "Stale badge"],
    data=["248 visits", "312 vaccinations", "₹3.86L income", "₹63,760 expenses", "2 pending writes"],
    actions=["Export report", "Print", "Drill into reports"],
    forms=["Date range", "Vaccine filter"],
    states=["Loading", "Empty range", "Ready", "Stale/partial", "Error (not zero)", "Permission denied"],
    offline="Local aggregates labelled stale; do not claim a complete month while writes are pending.",
    keyboard="Charts have text alternatives; drill links keyboard accessible; filter controls labelled.",
    a11y="Charts have tables/text alternatives; stale state not color-only; report totals labelled.",
    deps="RPT-001–007; finance; vaccinations; inventory; local aggregates.",
    open="Official report definitions, refunds/discounts, export formats, PHI export permissions.",
    notes="All report values are fictional design data. No aggregate is shown without a path to source records.",
    html=reports_overview())

add(id="RPT-002", name="Vaccination report", slug="vaccination-report", section="Reports", feature="Statistics and Reports",
    source="15-Statistics-and-Reports.md", purpose="Report doses, income, brand mix and batch usage by stable vaccine identity with drill-down.",
    users="Admin, doctor", permissions="Admin/doctor only; export permission unresolved.",
    entry="Statistics & reports; vaccine card drill-down.", navigation="Filter brand/date; export; inspect source visits (implementation).",
    layout=["Page header", "Filter bar", "Four metrics", "Doses bars", "Brand donut", "Vaccine table", "Grouping note"],
    components=["Filters", "Bar chart", "Donut", "Table", "Status badges"],
    data=["312 doses", "₹4.93L", "14 batches", "Pentavalent top"],
    actions=["Export CSV", "Print", "Filter"],
    forms=["Date range", "Brand", "Status"],
    states=["Loading", "Empty", "Ready", "Stale", "Partial error"],
    offline="Local aggregates labelled; unsynced vaccinations visible as stale.",
    keyboard="Chart text alternative; table drill links; filters.",
    a11y="Brand/color has text labels; table headers; totals labeled.",
    deps="RPT-001/003/004; vaccination; catalog identity.",
    open="Brand drill-down definition and official dose-report rules.",
    notes="Grouping uses stable catalog identity, not display-name equality.",
    html=vaccination_report())

add(id="RPT-003", name="Finance report", slug="finance-report", section="Reports", feature="Statistics and Reports",
    source="15-Statistics-and-Reports.md", purpose="Report income, expenses, net and payment split with one income count per visit and IST daily boundaries.",
    users="Admin, doctor", permissions="Reports role-restricted; export may be admin-only.",
    entry="Statistics & reports; finance overview; payment detail.", navigation="Date filter; source payment drill-down; export/print.",
    layout=["Page header", "Filter bar", "Four metrics", "Income/expense chart", "Payment split donut", "Daily table", "Stale warning"],
    components=["Filters", "Line chart", "Donut", "Daily table", "Stale badge"],
    data=["₹3.86L income", "₹63,760 expenses", "₹3.22L net", "1 provisional receipt"],
    actions=["Export CSV", "Print", "Filter"],
    forms=["Date range", "Payment method"],
    states=["Loading", "Empty", "Ready", "Stale/partial", "Error", "Permission denied"],
    offline="Local aggregates labelled stale; no completeness claim with pending writes.",
    keyboard="Chart alternative; table headers; filters.",
    a11y="Cash/online legend text; amounts labelled; stale state textual.",
    deps="RPT-001/002/004; finance; receipts; audit.",
    open="Refund/discount treatment, official report definitions, export scope.",
    notes="A visit's income is counted once; expenses are separate.",
    html=finance_report())

add(id="RPT-004", name="Patient milestone report", slug="patient-milestone-report", section="Reports", feature="Statistics and Reports",
    source="15-Statistics-and-Reports.md", purpose="Show due, overdue and completed milestone populations with drill-down to patient records.",
    users="Admin, doctor", permissions="Admin/doctor only.",
    entry="Statistics & reports; due vaccination dashboard.", navigation="Filter window/vaccine; open due list; drill to patient.",
    layout=["Page header", "Filter bar", "Four metrics", "Milestone status bars", "By-vaccine summary", "Milestone table"],
    components=["Metric cards", "Bar chart", "Summary list", "Patient table", "Status badges"],
    data=["23 due", "2 overdue", "87% coverage", "6 fictional patients"],
    actions=["Export CSV", "Print", "Filter", "Open due list"],
    forms=["Date range", "Vaccine", "Milestone"],
    states=["Loading", "Empty", "Ready", "Stale", "Permission denied"],
    offline="Local due list labelled; terminal reminder states reflected.",
    keyboard="Table drill links; chart alternative; filters.",
    a11y="Status textual; due dates explicit; coverage explained.",
    deps="RPT-001; reminders; patients; reports.",
    open="Official milestone definitions and coverage calculation method.",
    notes="Coverage is illustrative; no clinical target is asserted.",
    html=milestone_report())