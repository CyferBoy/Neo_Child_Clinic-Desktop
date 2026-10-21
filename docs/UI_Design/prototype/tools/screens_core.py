"""Core screens: authentication, shell, dashboard and patients."""
from __future__ import annotations

from components import (
    alert, avatar, badge, btn, checkbox, document, donut, drawer_overlay,
    field, icon, icon_btn, kv_list, line_chart, metric, mini_bars, modal_overlay,
    page_head, pagination, search_input, select_field, shell_page, sidebar,
    standalone, table, tabs, textarea, timeline, topbar, USER_ADMIN,
    USER_DOCTOR, USER_NURSE, USER_RECEPTION,
)

SCREENS = []


def add(**kwargs):
    kwargs.setdefault("dark_variant", False)
    kwargs.setdefault("wide_variant", False)
    SCREENS.append(kwargs)


def dashboard_content(user=USER_DOCTOR):
    metrics = f'''<div class="grid-4">
      {metric("Today's visits", "18", "3 waiting now", "users", hint="success:+2 vs last Tue")}
      {metric("Vaccinations due", "7", "2 overdue by 4 days", "syringe", variant="warn", hint="warning:Needs review")}
      {metric("Low stock", "3", "2 batches expire in 14 days", "package", variant="danger", hint="danger:Action needed")}
      {metric("Today's collections", "₹18,450", "Cash ₹11,200 · Online ₹7,250", "wallet", hint="success:+12%")}
    </div>'''
    schedule_rows = [
        ("09:00", "Aarav Sharma", "2y 4m · Vaccination · Pentavalent dose 3", "Waiting", "success", "MN"),
        ("09:30", "Diya Menon", "8m · Vaccination · Rotavirus dose 2", "In room", "info", "MN"),
        ("10:15", "Kabir Rao", "4y 1m · Consultation · Follow-up", "Confirmed", "neutral", "NV"),
        ("11:00", "Ishaan Gupta", "1y 2m · Vaccination · PCV booster", "Confirmed", "neutral", "RS"),
        ("11:45", "Myra Joshi", "6y · Consultation · New", "Confirmed", "neutral", "MN"),
    ]
    schedule = []
    for time, name, detail, status, tone, initials in schedule_rows:
        schedule.append(f'''<div class="schedule-line"><div class="schedule-time">{time}</div><div class="avatar sm">{initials}</div><div class="schedule-body"><div class="schedule-title">{name}</div><div class="schedule-sub">{detail}</div></div>{badge(status, tone)}<span class="row-action">{icon("chevron-right", 14)}</span></div>''')
    due_rows = [
        ("Aarav Sharma", "Pentavalent · Dose 3", "Today", "warning"),
        ("Sara Khan", "MMR · Dose 1", "2 days overdue", "danger"),
            ]
    due = "".join(f'''<div class="schedule-line" style="padding:4px 0"><div class="avatar sm apricot">{name[0]}</div><div class="schedule-body"><div class="schedule-title">{name}</div><div class="schedule-sub">{vac}</div></div><span class="badge {tone}">{when}</span></div>''' for name, vac, when, tone in due_rows)
    alerts = f'''<div class="compact-rows">
      <div class="stat-line">{icon("package", 14)}<div><div class="n-title">PCV-2411 expires in 12 days</div><div class="n-text">34 doses on hand · plan FEFO use</div></div></div>
      <div class="stat-line">{icon("alert-triangle", 14)}<div><div class="n-title">2 vaccinations overdue</div><div class="n-text">Sara Khan · Advik Mehta</div></div></div>
      <div class="stat-line">{icon("refresh", 14)}<div><div class="n-title">2 sync items need review</div><div class="n-text">Stock conflict · 1 receipt</div></div></div>
    </div>'''
    content = f'''{page_head("Tuesday, 20 October 2026", "Good morning, Dr. Nair", "6 visits scheduled · 7 vaccinations due · 2 stock and sync alerts need attention.", btn("Record vaccination", "primary", "syringe", href="VAC-002.html") + btn("Register patient", "secondary", "user-plus", href="PAT-002.html") + icon_btn("more", "More dashboard actions"))}
    {metrics}
    <div class="row mt-16" style="height:410px">
      <div class="card grow" style="display:flex;flex-direction:column">
        <div class="card-head"><div><div class="card-title">Today's clinic</div><div class="card-sub">Tuesday schedule · 6 of 18 visits shown</div></div><div class="card-action">{btn("Open patients", "ghost sm", "arrow-right", href="PAT-001.html")}</div></div>
        <div class="card-body" style="padding-top:4px;padding-bottom:4px">{''.join(schedule)}</div>
        <div class="card-foot" style="margin-top:auto;display:flex;align-items:center;gap:8px"><span class="muted small">Next available slot</span><strong style="font-size:11.5px">12:30 · Dr. Verma</strong><span class="spacer" style="flex:1"></span>{btn("New consultation", "ghost sm", "stethoscope", href="CON-002.html")}</div>
      </div>
      <div class="col w-side" style="display:block">
        <div class="card" style="height:230px;min-height:230px;margin-bottom:10px;overflow:hidden">
          <div class="card-head"><div><div class="card-title">Needs attention</div><div class="card-sub">Role-relevant alerts only</div></div><span class="badge danger">3</span></div>
          <div class="card-body compact-alerts">{alerts}</div>
        </div>
        <div class="card" style="height:170px;min-height:170px;overflow:hidden">
          <div class="card-head"><div class="card-title">Due today</div><div class="card-action">{btn("View all", "ghost sm", href="REM-001.html")}</div></div>
          <div class="card-body compact-due" style="padding-top:0;padding-bottom:0">{due}</div>
        </div>
      </div>
    </div>'''
    return content


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def auth_sign_in():
    body = f'''<div class="login-wrap">
      <aside class="login-aside">
        <div class="brand"><div class="brand-mark">{icon("logo", 18)}</div><div class="brand-text"><div class="brand-name">Neo Child Clinic</div><div class="brand-sub">Desktop workspace</div></div></div>
        <div><div class="eyebrow" style="color:#9ed0cc">Calm, connected clinic work</div><h1>Every visit,<br>in focus.</h1><p>One secure workspace for the front desk, the consultation room, and the stock room — online or offline.</p></div>
        <div class="login-art">
          <div class="art-card">
            <div class="art-title">TODAY AT A GLANCE</div>
            <div class="art-row">{icon("users", 14)} 18 visits <span style="margin-left:auto;color:#d7edea">3 waiting</span></div>
            <div class="art-row">{icon("syringe", 14)} 7 vaccinations due <span style="margin-left:auto;color:#f0c79f">2 overdue</span></div>
            <div class="art-row">{icon("package", 14)} 3 low-stock alerts <span style="margin-left:auto;color:#f0c79f">Review</span></div>
            <div class="art-row" style="border-top:1px solid rgba(255,255,255,.12);margin-top:6px;padding-top:8px">{icon("cloud", 14)} Local-first · works offline</div>
          </div>
          <div class="small" style="color:#7fa7a4;margin-top:14px">Clinic data stays on this device until it syncs securely.</div>
        </div>
      </aside>
      <main class="login-main">
        <div class="login-card">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:26px"><span class="badge brand">{icon("lock", 11)} Secure staff sign-in</span><button class="icon-btn" type="button" data-theme-toggle aria-label="Toggle dark theme">{icon("moon", 18)}</button></div>
          <h2>Welcome back</h2>
          <div class="sub">Sign in with your clinic account to open the shared patient record.</div>
          {field("Work email", "meera.nair@neoclinic.example", required=True, icon_name="user")}
          <div class="field"><div class="label-row"><label>Password <span class="req">*</span></label><span style="margin-left:auto"><a class="btn-link" href="#" style="font-size:10.5px">Show</a></span></div><div class="input">{icon("lock", 14)}<span>••••••••••••</span></div></div>
          <div style="display:flex;align-items:center;justify-content:space-between;margin:8px 0 16px 0"><span class="help">Role and access come from your clinic account.</span><span class="status-pill" style="height:24px"><span class="status-dot"></span>Auth reachable</span></div>
          <button class="btn primary block lg" type="button">Sign in {icon("arrow-right", 16)}</button>
          <div class="login-meta"><span>Need access? Contact your administrator.</span><span class="mono" style="font-size:9.5px">v0.1 preview</span></div>
          <div class="login-foot">Protected clinical workspace. Do not share your password or leave a signed-in device unattended.<br>Design preview only · fictional clinic data.</div>
        </div>
      </main>
    </div>'''
    return standalone(body, "Sign in")


def auth_restore():
    body = f'''<div class="splash"><div class="splash-card">
      <div class="splash-mark">{icon("logo", 30)}</div>
      <h1>Opening your clinic workspace</h1>
      <p>Restoring the secure session on this device</p>
      <div class="progress"><span style="width:64%"></span></div>
      <div class="splash-foot">Checking session · Verifying role · Unlocking local records</div>
      <div style="margin-top:30px;display:flex;flex-direction:column;gap:10px;text-align:left">
        <div class="art-row" style="display:flex;align-items:center;gap:9px;font-size:11px;color:#a9cbc8">{icon("check-circle", 15)} <span>Supabase session validated</span><span style="margin-left:auto;color:#9ed0dc">Done</span></div>
        <div class="art-row" style="display:flex;align-items:center;gap:9px;font-size:11px;color:#a9cbc8">{icon("refresh", 15)} <span>Loading local working copy</span><span style="margin-left:auto;color:#f0c79f">64%</span></div>
        <div class="art-row" style="display:flex;align-items:center;gap:9px;font-size:11px;color:#6f9895">{icon("lock", 15)} <span>Opening encrypted records</span><span style="margin-left:auto">Waiting</span></div>
      </div>
    </div></div>'''
    return standalone(body, "Restoring session")


def auth_session_expired():
    base = dashboard_content()
    modal = f'''<div class="dialog narrow" role="dialog" aria-modal="true" aria-labelledby="expired-title">
      <div class="dialog-head"><div class="dialog-icon warning">{icon("lock", 18)}</div><div><div class="dialog-title" id="expired-title">Your secure session expired</div><div class="dialog-sub">Patient data is hidden until you sign in again.</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        {alert("Any unsaved form text is kept in memory for this window. Local records are not deleted.", "info", "info")}
        <div class="field mt-16"><label>Work email</label><div class="input">{icon("user", 14)}<span>meera.nair@neoclinic.example</span></div></div>
        <div class="field mt-12"><label>Password</label><div class="input focus">{icon("lock", 14)}<span class="placeholder">Password</span></div></div>
        <div class="help mt-8">Use your own clinic account. Shared accounts are not supported.</div>
      </div>
      <div class="dialog-foot"><button class="btn ghost" type="button">Sign out</button><div class="spacer"></div><button class="btn primary" type="button">Sign in again</button></div>
    </div>'''
    return modal_overlay(base, "DASH-001", "Dashboard", USER_DOCTOR, modal, status="Session expired", status_tone="attention")


def auth_access_denied():
    body = f'''<div class="access-screen"><div>
      <div class="brand" style="justify-content:center;margin-bottom:18px;border:0;height:auto"><div class="brand-mark" style="background:var(--brand-900);color:#fff">{icon("logo", 18)}</div><div class="brand-text"><div class="brand-name" style="color:var(--ink-900)">Neo Child Clinic</div><div class="brand-sub" style="color:var(--ink-500)">Desktop workspace</div></div></div>
      <div class="access-card">
        <div class="access-icon">{icon("shield-alert", 26)}</div>
        <h1>Access is not available</h1>
        <p>This account is deactivated, or it does not have a valid clinic role. No patient records were opened on this device.</p>
        <div class="alert warning" style="text-align:left;margin-top:16px">{icon("info", 15)}<div><strong>What to do</strong><br>Contact your clinic administrator to restore access. If you are using a shared computer, sign out before leaving.</div></div>
        <div class="access-actions"><button class="btn secondary" type="button">Try another account</button><button class="btn primary" type="button">Close application</button></div>
        <div class="small muted mt-16">Reference: AUTH-DENIED-04 · No PHI displayed</div>
      </div>
    </div></div>'''
    return standalone(body, "Access denied")


def auth_sign_out_pending():
    base = dashboard_content()
    modal = f'''<div class="dialog narrow" role="dialog" aria-modal="true" aria-labelledby="signout-title">
      <div class="dialog-head"><div class="dialog-icon warning">{icon("cloud-off", 18)}</div><div><div class="dialog-title" id="signout-title">3 changes have not synced</div><div class="dialog-sub">Sign-out is paused to protect the shared record.</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        <p class="muted" style="font-size:11.5px;line-height:1.55">These local changes are still waiting for the shared Supabase record. Sync now, or cancel and keep working on this device.</p>
        <div class="notice-list mt-12">
          <div class="notice-item" style="padding:5px 7px"><span class="n-icon" style="width:22px;height:22px;flex-basis:22px;background:var(--info-100);color:var(--info-700)">{icon("syringe", 13)}</span><div><div class="n-title">Vaccination visit · Aarav Sharma</div><div class="n-text">Visit, 1 stock movement, 1 reminder · queued 2 min ago</div></div></div>
          <div class="notice-item"><span class="n-icon" style="background:var(--warning-100);color:var(--warning-700)">{icon("package", 13)}</span><div><div class="n-title">Stock adjustment · PCV-2411</div><div class="n-text">-2 doses · requires conflict review</div></div></div>
        </div>
        {alert("Do not close the application while a sync is in progress.", "warning", "alert-triangle")}
      </div>
      <div class="dialog-foot"><button class="btn ghost" type="button">Cancel</button><div class="spacer"></div><button class="btn secondary" type="button">Open sync center</button><button class="btn primary" type="button">{icon("refresh", 15)} Sync now</button></div>
    </div>'''
    return modal_overlay(base, "DASH-001", "Dashboard", USER_DOCTOR, modal, status="3 pending", status_tone="attention")


# ---------------------------------------------------------------------------
# Shell search
# ---------------------------------------------------------------------------

def shell_search():
    base = dashboard_content()
    modal = f'''<div class="dialog sheet" role="dialog" aria-modal="true" aria-labelledby="search-title" style="top:84px">
      <div style="padding:14px 16px 12px;border-bottom:1px solid var(--border-subtle)"><div style="display:flex;align-items:center;gap:10px">{icon("search", 19)}<input id="search-title" aria-label="Global search" style="border:0;outline:0;flex:1;font-size:15px;background:transparent;color:var(--ink-900)" placeholder="Search patients, clinic ID, batches, receipts…" value="aar"><span class="kbd">Esc</span></div><div class="tab-bar mt-12"><div class="tabs" style="border-bottom:0"><span class="tab active">All</span><span class="tab">Patients <span class="count">4</span></span><span class="tab">Batches</span><span class="tab">Receipts</span><span class="tab">Actions</span></div><div class="spacer"></div><span class="tiny muted">Permission-aware results</span></div></div>
      <div style="padding:8px 8px 6px">
        <div class="nav-label" style="padding:8px 10px 5px">Patients</div>
        <div class="queue-item" style="border-color:var(--brand-100);background:var(--brand-50)"><div class="avatar">AS</div><div><div class="strong">Aarav Sharma <span class="badge brand">Selected</span></div><div class="tiny muted">NCC-2026-00418 · 2y 4m · +91 98450 11223 · last visit 12 Aug</div></div><span class="spacer"></span><span class="badge warning">Due today</span>{icon("arrow-right", 14)}</div>
        <div class="queue-item"><div class="avatar apricot">AR</div><div><div class="strong">Anaya Reddy</div><div class="tiny muted">NCC-2026-00371 · 4y 1m · +91 99001 44556 · last visit 2 Sep</div></div><span class="spacer"></span><span class="badge success">Active</span>{icon("arrow-right", 14)}</div>
        <div class="queue-item"><div class="avatar info">AK</div><div><div class="strong">Aarohi Kulkarni</div><div class="tiny muted">NCC-2026-00286 · 7m · +91 98860 77221 · last visit 18 Oct</div></div><span class="spacer"></span><span class="badge success">Active</span>{icon("arrow-right", 14)}</div>
        <div class="queue-item"><div class="avatar success">AA</div><div><div class="strong">Aarav Anand</div><div class="tiny muted">NCC-2025-01102 · 6y 2m · +91 97400 22110 · last visit 4 May</div></div><span class="spacer"></span><span class="badge neutral">Archived</span>{icon("arrow-right", 14)}</div>
        <div class="nav-label" style="padding:12px 10px 5px">Quick actions</div>
        <div class="queue-item"><span class="n-icon" style="width:26px;height:26px;border-radius:7px;background:var(--brand-50);color:var(--brand-700);display:flex;align-items:center;justify-content:center">{icon("syringe", 13)}</span><div><div class="strong">Record vaccination</div><div class="tiny muted">Start with a patient search</div></div><span class="spacer"></span><span class="kbd">V</span></div>
        <div class="queue-item"><span class="n-icon" style="width:26px;height:26px;border-radius:7px;background:var(--brand-50);color:var(--brand-700);display:flex;align-items:center;justify-content:center">{icon("user-plus", 13)}</span><div><div class="strong">Register patient</div><div class="tiny muted">Create a new clinic record</div></div><span class="spacer"></span><span class="kbd">N</span></div>
      </div>
      <div class="dialog-foot"><span class="small muted">↑↓ to move · Enter to open</span><div class="spacer"></div><span class="small muted">No patient data leaves this device.</span></div>
    </div>'''
    return modal_overlay(base, "DASH-001", "Dashboard", USER_DOCTOR, modal, status="Online")


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def dashboard():
    return shell_page("DASH-001", "Dashboard", USER_DOCTOR, dashboard_content(), status="Online", attention=6)


# ---------------------------------------------------------------------------
# Patients
# ---------------------------------------------------------------------------

def patient_list_content():
    rows = [
        ("<span class='checkbox'></span>", "<div class='identity'><span class='avatar'>AS</span><div class='identity-main'><div class='identity-name'>Aarav Sharma</div><div class='identity-sub'>2y 4m · Male</div></div></div>", "NCC-2026-00418", "2y 4m", "+91 98450 11223", "12 Aug 2026", "Today", badge("Due today", "warning", "clock"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<span class='checkbox'></span>", "<div class='identity'><span class='avatar apricot'>DM</span><div class='identity-main'><div class='identity-name'>Diya Menon</div><div class='identity-sub'>8m · Female</div></div></div>", "NCC-2026-00502", "8m", "+91 99001 44556", "18 Oct 2026", "24 Nov", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<span class='checkbox'></span>", "<div class='identity'><span class='avatar info'>KR</span><div class='identity-main'><div class='identity-name'>Kabir Rao</div><div class='identity-sub'>4y 1m · Male</div></div></div>", "NCC-2026-00371", "4y 1m", "+91 98860 77221", "2 Sep 2026", "Today", badge("Confirmed", "brand"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<span class='checkbox'></span>", "<div class='identity'><span class='avatar success'>IG</span><div class='identity-main'><div class='identity-name'>Ishaan Gupta</div><div class='identity-sub'>1y 2m · Male</div></div></div>", "NCC-2026-00488", "1y 2m", "+91 97400 22110", "21 Jul 2026", "Today", badge("Due today", "warning", "clock"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<span class='checkbox'></span>", "<div class='identity'><span class='avatar info'>VN</span><div class='identity-main'><div class='identity-name'>Vivaan Nair</div><div class='identity-sub'>3y 7m · Male</div></div></div>", "NCC-2025-01102", "3y 7m", "+91 99000 12123", "16 Oct 2026", "12 Dec", badge("Pending sync", "info", "refresh"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<span class='checkbox'></span>", "<div class='identity'><span class='avatar apricot'>AR</span><div class='identity-main'><div class='identity-name'>Anaya Reddy</div><div class='identity-sub'>4y 1m · Female</div></div></div>", "NCC-2026-00323", "4y 1m", "+91 98800 44332", "2 Sep 2026", "21 Oct", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<span class='checkbox'></span>", "<div class='identity'><span class='avatar success'>SK</span><div class='identity-main'><div class='identity-name'>Sara Khan</div><div class='identity-sub'>5y 2m · Female</div></div></div>", "NCC-2025-00987", "5y 2m", "+91 97411 88990", "28 Aug 2026", "2 days overdue", badge("Overdue", "danger", "alert-circle"), f"<span class='row-action'>{icon('more', 16)}</span>"),
    ]
    toolbar = f'''<div class="toolbar">{search_input()}<span class="result-count">2,418 active patients</span><span class="spacer"></span>{btn("Filters", "", "filter", size="sm")}<span class="toolbar-select">All children {icon("chevron-down", 12)}</span><span class="toolbar-select">Last visit {icon("chevron-down", 12)}</span>{icon_btn("download", "Export patient list", bordered=True)}</div>'''
    content = f'''{page_head("Patient records", "Patients", "Search by name, clinic ID or phone. Results are limited to your role and this clinic.", btn("Register patient", "primary", "user-plus", href="PAT-002.html") + btn("Merge records", "secondary", "repeat", href="PAT-006.html"))}
    <div class="row tight" style="margin-bottom:10px"><span class="chip active">{icon("users", 12)} All patients</span><span class="chip">{icon("bell", 12)} Due vaccination</span><span class="chip">{icon("baby", 12)} Under 5</span><span class="chip">{icon("clock", 12)} Recently seen</span><span class="chip">{icon("cloud-off", 12)} Pending sync <span class="badge info">3</span></span><span class="spacer" style="flex:1"></span><span class="small muted">Showing active records only</span></div>
    {toolbar}
    <div class="table-card">{table(["<span class='checkbox'></span><span class='sr-only'>Select all patients</span>", "Patient", "Clinic ID", "Age", "Phone", "Last visit", "Next due", "Status", ""], rows, widths=["check", "w-name", "w-id", "w-age", "w-phone", "w-date", "", "w-status", "w-actions"])}{pagination("1–7 of 2,418", ("‹","1","2","3","…","303","›"))}</div>'''
    return content


def patient_list():
    return shell_page("PAT-001", "Patients", USER_RECEPTION, patient_list_content(), attention=6)


def patient_register_content(show_validation=False):
    name_error = "Enter the child's full name." if show_validation else ""
    right = f'''<div class="col tight w-side-sm">
      <div class="card"><div class="card-head"><div><div class="card-title">Before you save</div><div class="card-sub">Local duplicate check</div></div><span class="badge success">{icon("check", 10)} Clear</span></div><div class="card-body" style="padding-top:8px">
        <div class="stat-line">{icon("user", 13)} No exact name + phone match</div>
        <div class="stat-line">{icon("tag", 13)} Clinic ID generated after save</div>
        <div class="stat-line">{icon("refresh", 13)} Syncs once, even after restart</div>
        <div class="mt-12">{btn("Save & add vaccination", "secondary", "syringe", size="sm")}</div>
        <div class="help mt-8">{icon("cloud-off", 12)} Registration works offline.</div>
      </div></div>
    </div>'''
    content = f'''{page_head("Patient records", "Register a patient", "Create a demographic record now; clinical history starts with the first visit.", btn("Cancel", "ghost", href="PAT-001.html") + btn("Register patient", "primary", "check"))}
    <div class="row top">
      <div class="grow col">
        <div class="form-section"><div class="form-section-head">{icon("user", 15)}<div class="form-section-title">Child details</div><span class="badge neutral">Required</span></div><div class="form-section-body">
          <table class="form-table"><colgroup><col style="width:33.33%"><col style="width:33.33%"><col style="width:33.34%"></colgroup><tbody>
            <tr><td colspan="2">{field("Full name", "", required=True, placeholder="e.g. Aarav Sharma", error=name_error)}</td><td>{field("Date of birth", "18 Jun 2024", required=True, icon_name="calendar")}</td></tr>
            <tr><td>{select_field("Gender", "Male", required=True)}</td><td>{field("Clinic ID", "Generated on save")}</td><td>{field("Registration date", "20 Oct 2026", icon_name="calendar")}</td></tr>
          </tbody></table>
        </div></div>
        <div class="form-section"><div class="form-section-head">{icon("phone", 15)}<div class="form-section-title">Contact & address</div></div><div class="form-section-body">
          <table class="form-table"><colgroup><col style="width:50%"><col style="width:50%"></colgroup><tbody>
            <tr><td>{field("Phone", "", required=True, placeholder="+91 98450 00000", icon_name="phone")}</td><td>{field("Alternate phone", "", placeholder="Optional", icon_name="phone")}</td></tr>
            <tr><td colspan="2">{textarea("Address", "", placeholder="House / street, area, city, PIN")}</td></tr>
          </tbody></table>
        </div></div>
      </div>
      {right}
    </div>'''
    return content


def patient_register():
    return shell_page("PAT-002", "Register patient", USER_RECEPTION, patient_register_content(), attention=6)


def patient_profile_content():
    ribbon = f'''<div class="patient-ribbon"><div class="identity"><span class="avatar lg">AS</span><div><div class="identity-name" style="font-size:16px">Aarav Sharma</div><div class="identity-sub">NCC-2026-00418 · 2 years 4 months · Male · registered 18 Jun 2024</div></div></div><span class="badge success">{icon("check", 10)} Active</span><span class="badge neutral">Local record</span><span class="spacer" style="flex:1"></span><span class="small muted">Last updated 2 min ago</span>{btn("Edit", "secondary", "edit", size="sm", href="PAT-004.html")}</div>'''
    events = [
        {"title": "Vaccination · Pentavalent dose 3", "time": "Today · 09:04", "body": "Batch AV-2409 · 0.5 mL · Dr. Meera Nair", "meta": badge("Pending sync", "info", "refresh") + badge("₹850", "neutral") + badge("Receipt provisional", "outline"), "tone": "warning"},
        {"title": "Consultation · Mild viral fever", "time": "12 Aug 2026 · 11:20", "body": "Dr. Nikhil Verma · follow-up 19 Aug 2026 · notes added", "meta": badge("Paid", "success") + badge("₹500", "neutral") + badge("Receipt NCC-R-004182", "outline"), "tone": "success"},
        {"title": "Vaccination · Rotavirus dose 2", "time": "18 Jun 2026 · 10:10", "body": "Batch RV-2405 · 1.5 mL · Nurse Ritika Sen", "meta": badge("Synced", "success") + badge("₹1,200", "neutral"), "tone": ""},
        {"title": "Consultation · Feeding review", "time": "2 May 2026 · 16:40", "body": "Dr. Meera Nair · no follow-up required", "meta": badge("Paid", "success") + badge("₹500", "neutral"), "tone": "neutral"},
        {"title": "Patient note added", "time": "2 May 2026 · 16:42", "body": "“Parent prefers morning appointments.”", "meta": badge("Staff note", "outline"), "tone": "neutral"},
    ]
    right = f'''<div class="col tight w-side">
      <div class="card"><div class="card-head"><div class="card-title">Record details</div></div><div class="card-body" style="padding-top:8px">{kv_list([("Clinic ID", "NCC-2026-00418"), ("Date of birth", "18 Jun 2024"), ("Phone", "+91 98450 11223"), ("Alternate", "—"), ("Address", "Indiranagar, Bengaluru"), ("Created by", "Kavya Iyer")])}</div></div>
      <div class="card"><div class="card-head"><div><div class="card-title">Care summary</div><div class="card-sub">Next actions for this child</div></div></div><div class="card-body" style="padding-top:8px">
        <div class="stat-line"><span class="badge warning">Due today</span><span>Pentavalent · dose 3</span></div>
        <div class="stat-line"><span class="badge neutral">No follow-up</span><span>Last consultation 12 Aug</span></div>
        <div class="stat-line"><span class="badge success">No balance</span><span>Last payment ₹500</span></div>
        <div class="mt-12">{btn("Add note", "secondary", "message", size="sm")} {btn("Add reminder", "ghost", "bell", size="sm")}</div>
      </div></div>
      <div class="card"><div class="card-head"><div class="card-title">Quick actions</div></div><div class="card-body" style="display:flex;flex-direction:column;gap:6px">{btn("Record vaccination", "primary", "syringe", size="sm")} {btn("New consultation", "secondary", "stethoscope", size="sm")} {btn("Take payment", "secondary", "wallet", size="sm")} {btn("Archive record", "ghost", "archive", size="sm")}</div></div>
    </div>'''
    content = f'''{page_head("Patient records · NCC-2026-00418", "Patient profile", "A complete, chronological view of this child's clinical and financial history.", btn("Record vaccination", "primary", "syringe", href="VAC-002.html") + btn("New consultation", "secondary", "stethoscope", href="CON-002.html") + icon_btn("more", "More patient actions"))}
    {ribbon}
    <div style="margin-top:12px">{tabs([("Overview", None), ("Visits", "7"), ("Vaccinations", "11"), ("Payments", "8"), ("Notes & documents", "4")], 0, extra=f'<span class="spacer" style="flex:1"></span><span class="small muted">{icon("refresh", 12)} Timeline invalidates after every dependent write</span>')}</div>
    <div class="row top mt-12">
      <div class="grow col">
        <div class="card"><div class="card-head"><div><div class="card-title">Patient timeline</div><div class="card-sub">Newest first · all times shown in IST</div></div><div class="card-action">{btn("Filter", "ghost sm", "filter")}</div></div><div class="card-body">{timeline(events)}</div></div>
        <div class="alert warning">{icon("alert-triangle", 15)}<div><strong>One local vaccination is pending sync.</strong> The receipt number is provisional until the server assigns it. <a href="SYS-001.html">Open sync center</a>.</div></div>
      </div>
      {right}
    </div>'''
    return content


def patient_profile():
    return shell_page("PAT-003", "Patient profile", USER_DOCTOR, patient_profile_content(), status="Syncing", status_tone="syncing", attention=6)


def patient_edit_drawer():
    base = patient_profile_content()
    drawer = f'''<div class="drawer wide" role="dialog" aria-modal="true" aria-labelledby="edit-patient-title">
      <div class="drawer-head"><div><div class="drawer-title" id="edit-patient-title">Edit patient details</div><div class="drawer-sub">NCC-2026-00418 · changes are audited</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="drawer-body"><div class="alert info" style="margin-bottom:14px">{icon("info", 15)}<div>Clinical history is not edited here. Use the relevant visit, vaccination or consultation.</div></div>
        <div class="form-grid">
          {field("Full name", "Aarav Sharma", required=True, width="full")}
          {field("Date of birth", "18 Jun 2024", required=True, icon_name="calendar")}
          {select_field("Gender", "Male")}
          {field("Phone", "+91 98450 11223", required=True, icon_name="phone")}
          {field("Alternate phone", "", placeholder="Optional", icon_name="phone")}
          {textarea("Address", "12, 4th Cross, Indiranagar, Bengaluru 560038", width="full")}
        </div>
        <div class="divider"></div>
        <div class="label">Record metadata</div>
        <div class="mt-8">{kv_list([("Created", "18 Jun 2024 · Kavya Iyer"), ("Last updated", "20 Oct 2026 · Dr. Meera Nair"), ("Local status", badge("Pending sync", "info", "refresh"))])}</div>
      </div>
      <div class="drawer-foot"><button class="btn danger-ghost" type="button">Archive</button><div class="spacer"></div><button class="btn" type="button">Cancel</button><button class="btn primary" type="button">Save changes</button></div>
    </div>'''
    return drawer_overlay(base, "PAT-001", "Patient profile", USER_DOCTOR, drawer)


def patient_duplicate_dialog():
    base = patient_register_content(show_validation=True)
    modal = f'''<div class="dialog wide" role="dialog" aria-modal="true" aria-labelledby="duplicate-title">
      <div class="dialog-head"><div class="dialog-icon warning">{icon("alert-triangle", 18)}</div><div><div class="dialog-title" id="duplicate-title">Possible duplicate patient</div><div class="dialog-sub">Review before creating a new record.</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        <p class="muted" style="font-size:11.5px;line-height:1.55">The name and phone are similar to existing active patients. Duplicate records split clinical history and payments.</p>
        <div class="queue mt-12">
          <div class="queue-item" style="align-items:flex-start;padding:11px"><div class="avatar">AS</div><div><div class="strong">Aarav Sharma</div><div class="tiny muted">NCC-2026-00418 · 2y 4m · +91 98450 11223</div><div class="tl-meta" style="margin-top:5px">{badge("Same phone", "warning")}{badge("Last visit 12 Aug", "outline")}{badge("3 vaccinations", "outline")}</div></div><span class="spacer"></span><button class="btn sm secondary" type="button">Open</button></div>
          <div class="queue-item" style="align-items:flex-start;padding:11px"><div class="avatar apricot">AS</div><div><div class="strong">Aarav S.</div><div class="tiny muted">NCC-2025-01087 · 2y 5m · +91 98450 11223</div><div class="tl-meta" style="margin-top:5px">{badge("Same phone", "warning")}{badge("No visits", "danger")}{badge("Archived", "neutral")}</div></div><span class="spacer"></span><button class="btn sm secondary" type="button">Open</button></div>
        </div>
        {alert("If this is a different child, record the reason below. The duplicate warning is not a silent merge.", "warning", "info")}
        <div class="field mt-12"><label>Reason for continuing <span class="optional">(required to override)</span></label><div class="input"><span class="placeholder">e.g. Different child in the same household</span></div></div>
      </div>
      <div class="dialog-foot"><button class="btn ghost" type="button">Cancel</button><div class="spacer"></div><button class="btn secondary" type="button">Review existing record</button><button class="btn primary" type="button">Create new record</button></div>
    </div>'''
    return modal_overlay(base, "PAT-001", "Register patient", USER_RECEPTION, modal, status="Online")


def patient_merge_dialog():
    base = patient_list_content()
    modal = f'''<div class="dialog wide" role="dialog" aria-modal="true" aria-labelledby="merge-title">
      <div class="dialog-head"><div class="dialog-icon warning">{icon("repeat", 18)}</div><div><div class="dialog-title" id="merge-title">Merge patient records</div><div class="dialog-sub">Choose the surviving identity, then review dependent history.</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        {alert("Merge is queued only when the conflict policy allows it. If a conflicting visit is open on another device, the merge is blocked.", "warning", "alert-triangle")}
        <div class="grid-2 mt-12">
          <div class="card" style="border-color:var(--brand-200);background:var(--brand-50)"><div class="card-head" style="border-bottom:0;padding:10px 12px"><div class="card-title">Keep this record</div><span class="badge brand">Primary</span></div><div class="card-body" style="padding:0 12px 12px"><div class="identity"><span class="avatar">AS</span><div><div class="identity-name">Aarav Sharma</div><div class="identity-sub">NCC-2026-00418 · 2y 4m</div></div></div><div class="small muted mt-8">3 vaccinations · 2 consultations · 3 payments</div></div></div>
          <div class="card"><div class="card-head" style="border-bottom:0;padding:10px 12px"><div class="card-title">Merge into primary</div><span class="badge neutral">Secondary</span></div><div class="card-body" style="padding:0 12px 12px"><div class="identity"><span class="avatar apricot">AS</span><div><div class="identity-name">Aarav S.</div><div class="identity-sub">NCC-2025-01087 · 2y 5m</div></div></div><div class="small muted mt-8">0 vaccinations · 0 consultations · 0 payments</div></div></div>
        </div>
        <div class="table-card standalone mt-12">{table(["Field", "Primary", "Secondary", "Resolve"], [["Name", "Aarav Sharma", "Aarav S.", badge("Keep primary", "brand")], ["Date of birth", "18 Jun 2024", "12 Jun 2024", badge("Keep primary", "brand")], ["Phone", "+91 98450 11223", "+91 98450 11223", badge("Same", "success")], ["Clinic ID", "NCC-2026-00418", "NCC-2025-01087", badge("Keep primary", "brand")]], widths=["w-name", "", "", "w-status"])}</div>
        <div class="check-row mt-12"><span class="checkbox"></span><span class="check-text">I reviewed the history and understand that the secondary record will be archived after the merge.</span></div>
      </div>
      <div class="dialog-foot"><button class="btn ghost" type="button">Cancel</button><div class="spacer"></div><span class="small muted">Merge is audited</span><button class="btn primary" type="button">Merge records</button></div>
    </div>'''
    return modal_overlay(base, "PAT-001", "Patients", USER_ADMIN, modal)


def patient_archive_dialog():
    base = patient_profile_content()
    modal = f'''<div class="dialog narrow" role="dialog" aria-modal="true" aria-labelledby="archive-title">
      <div class="dialog-head"><div class="dialog-icon danger">{icon("archive", 18)}</div><div><div class="dialog-title" id="archive-title">Archive this patient?</div><div class="dialog-sub">NCC-2026-00418 · Aarav Sharma</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        <p class="muted" style="font-size:11.5px;line-height:1.55">Archiving is a soft delete. The record leaves active lists and reports, but its clinical and financial history stays intact for audit.</p>
        {alert("3 vaccinations, 2 consultations and 3 payments are linked to this record. They will not be deleted.", "warning", "alert-triangle")}
        <div class="field mt-12"><label>Reason for archiving <span class="req">*</span></label><div class="textarea"><span class="placeholder">e.g. Duplicate resolved, family moved, record created in error</span></div><div class="help">The reason is written to the audit log.</div></div>
        <div class="check-row mt-8"><span class="checkbox"></span><span class="check-text">I understand this record will no longer appear in active search.</span></div>
      </div>
      <div class="dialog-foot"><button class="btn ghost" type="button">Cancel</button><div class="spacer"></div><button class="btn danger" type="button">Archive patient</button></div>
    </div>'''
    return modal_overlay(base, "PAT-001", "Patient profile", USER_ADMIN, modal)


add(id="AUTH-001", name="Sign in", slug="sign-in", section="Authentication", feature="Authentication and Session",
    source="02-Authentication-and-Session.md", purpose="Authenticate a staff member with Supabase Auth without exposing tokens to the renderer.",
    users="All staff", permissions="Unauthenticated. Supabase Auth email/password; role resolved by the trusted core after sign-in.",
    entry="Application launch with no valid session, or explicit sign-out.", navigation="Successful sign-in → session restore → role-aware Dashboard. Failure stays on this screen.",
    layout=["Brand story panel (left, 46%)", "Sign-in card (right)", "Security and support note", "Preview theme control"],
    components=["Email field", "Password field with show control", "Primary sign-in", "Auth reachability indicator"],
    data=["Fictional staff email", "No patient data"],
    actions=["Sign in", "Show password", "Contact administrator"],
    forms=["Email (required, email format)", "Password (required, masked)"],
    states=["Ready", "Invalid credentials", "Rate limited", "Network unavailable", "Account deactivated"],
    offline="Sign-in requires the shared Supabase Auth service. A previously validated session may restore offline only under the approved session policy.",
    keyboard="Tab order: email → password → show → sign in. Enter submits. Escape clears focus; it does not dismiss the screen.",
    a11y="Visible labels; 4.5:1 contrast; focus ring; password field has explicit label; error announced via aria-live in implementation.",
    deps="AUTH-001–006; ADR-0004; ADR-0008; trusted Go auth boundary.",
    open="No desktop implementation. Session lifetime, offline cold-start policy and password reset surface remain unapproved.",
    notes="Tokens must stay in Go memory/OS keychain and never enter the renderer. This screen displays no clinic data.",
    html=auth_sign_in())

add(id="AUTH-002", name="Restoring session", slug="restoring-session", section="Authentication", feature="Authentication and Session",
    source="02-Authentication-and-Session.md", purpose="Show safe, non-PHI progress while the trusted core validates the cached session and role before opening records.",
    users="All staff", permissions="Cached session only; role must validate before PHI is unlocked.",
    entry="Warm or cold start with a stored refresh token.", navigation="Success → Dashboard (or last safe route). Failure → Sign in or Access denied.",
    layout=["Centered brand mark", "Progress and step list", "No navigation", "No patient data"],
    components=["Progress bar", "Three validation steps", "Security footnote"],
    data=["No patient identifiers", "No role name until verified"],
    actions=["None while validation runs", "Application quit via native window control"],
    forms=[],
    states=["Validating", "Offline validation", "Expired session", "Revoked session", "Local database unlock error"],
    offline="May validate cached session and open the local copy only if the approved policy permits. No new writes are silently marked synced.",
    keyboard="No interactive controls inside the content area. Native window close remains available.",
    a11y="Progress uses text, not color alone; steps are announced in order; no spinner-only state.",
    deps="AUTH-001; ADR-0004; local database unlock; role resolution.",
    open="Offline cold-start behavior is unresolved. Do not implement until the session policy is approved.",
    notes="The step labels describe intended checks, not verified desktop behavior.",
    html=auth_restore())

add(id="AUTH-003", name="Session expired", slug="session-expired", section="Authentication", feature="Authentication and Session",
    source="02-Authentication-and-Session.md", purpose="Re-authenticate after expiry without losing in-memory form work or exposing the previous screen's PHI.",
    users="Signed-in staff", permissions="Expired session; PHI must be masked until re-authentication.",
    entry="Token expiry, refresh failure or sensitive-action re-authentication.", navigation="Success → return to the interrupted route. Sign out → sign-in.",
    layout=["Dashboard context behind a modal scrim", "Narrow dialog", "Email and password", "Unsaved-work note"],
    components=["Modal dialog", "Warning icon", "Password field", "Sign-in and sign-out actions"],
    data=["Staff email", "No patient data in the dialog"],
    actions=["Sign in again", "Sign out", "Close (if safe)"],
    forms=["Email (read-only)", "Password (required)"],
    states=["Expired", "Invalid password", "Account revoked", "Network unavailable"],
    offline="Re-authentication requires Auth connectivity unless an approved offline policy exists.",
    keyboard="Focus trapped in dialog; Escape closes only if no sensitive operation is pending; Enter submits.",
    a11y="aria-modal dialog, labelled title, focus trap, error announced, no data behind accessible scrim.",
    deps="AUTH-001; ADR-0004.",
    open="Whether unsaved form drafts survive expiry is unresolved; this mockup shows a non-PHI memory note only.",
    notes="The background is intentionally dimmed; screenshot shows the dialog state, not a separate dashboard.",
    html=auth_session_expired())

add(id="AUTH-004", name="Access denied", slug="access-denied", section="Authentication", feature="Authentication and Session",
    source="02-Authentication-and-Session.md", purpose="Explain deactivated accounts or missing roles without opening patient data.",
    users="Any account that fails role or active-status validation", permissions="No clinic data. Access is denied.",
    entry="Deactivated account, missing/malformed app_metadata.role, or revoked session.", navigation="Try another account → Sign in. Close → exit application.",
    layout=["Centered access card", "Warning icon", "Explanation", "Two safe actions"],
    components=["Access card", "Warning alert", "Reference code"],
    data=["No patient identifiers", "No role details beyond the reason"],
    actions=["Try another account", "Close application"],
    forms=[],
    states=["Deactivated account", "Missing role", "Malformed role claim", "Revoked session"],
    offline="No PHI is opened. Local caches should be cleared on this transition per ADR-0004.",
    keyboard="Two actions in logical order; Enter activates focused action; Escape does not bypass denial.",
    a11y="Plain-language heading; reason not conveyed by color; no technical role claim shown.",
    deps="AUTH-002; ADR-0004; RLS role constraints.",
    open="Support contact details and audit visibility for denied attempts are not specified.",
    notes="This is a terminal state; no sidebar or patient route is rendered.",
    html=auth_access_denied())

add(id="AUTH-005", name="Sign out with pending writes", slug="sign-out-pending", section="Authentication", feature="Authentication and Session",
    source="02-Authentication-and-Session.md", purpose="Prevent an unsafe sign-out while local writes are pending, and offer a safe sync path.",
    users="Signed-in staff", permissions="Own session only.",
    entry="User chooses sign out while the outbox has pending or conflicted writes.", navigation="Sync now → Sync center. Cancel → previous screen. Sign out is blocked in this design.",
    layout=["Dashboard context behind scrim", "Narrow warning dialog", "Pending write summary", "Sync-first actions"],
    components=["Warning dialog", "Pending write list", "Sync now", "Sync center"],
    data=["Fictional patient name", "Visit and stock item counts", "No payment credentials"],
    actions=["Sync now", "Open sync center", "Cancel"],
    forms=[],
    states=["Pending writes", "Sync in progress", "Sync conflict", "No pending writes (dialog not shown)"],
    offline="When offline, the dialog should explain that sync is unavailable and block destructive sign-out; policy confirmation required.",
    keyboard="Focus trapped; Escape cancels; primary action syncs and remains in the app.",
    a11y="Warning uses text and icon; counts are readable; no auto-dismiss.",
    deps="SYNC-001–007; ADR-0004; local outbox.",
    open="The final sign-out policy and cache-clearing behavior are unresolved. This mockup deliberately blocks sign-out.",
    notes="The dialog does not claim that unsynced changes are safe across sign-out.",
    html=auth_sign_out_pending())

add(id="SHELL-001", name="Global search", slug="global-search", section="Shell", feature="Desktop Shell and Navigation",
    source="01-Desktop-Shell-and-Navigation.md", purpose="Find a patient, batch, receipt or permitted action from anywhere in the app using bounded, permission-aware results.",
    users="All staff", permissions="Results respect role and clinic scope; no all-patient scan in the renderer.",
    entry="Top-bar search, Ctrl/Cmd+K, or empty-state search.", navigation="Open result → permitted destination. Escape → prior screen.",
    layout=["Dashboard context behind a scrim", "Centered command palette", "Search field", "Grouped results and quick actions"],
    components=["Command palette", "Search input", "Result rows", "Keyboard hints"],
    data=["Fictional patient names, clinic IDs, ages, masked phones", "Batch and receipt groups are present but empty in this sample"],
    actions=["Open patient", "Start vaccination", "Register patient"],
    forms=["Global search (bounded query, minimum 2 characters)"],
    states=["Idle", "Searching", "Results", "No results", "Permission hidden", "Offline local results"],
    offline="Searches the encrypted local index; stale remote-only results are marked.",
    keyboard="Ctrl/Cmd+K opens; ↑/↓ moves; Enter opens; Escape closes; Tab does not leave the palette.",
    a11y="Combobox/listbox semantics, announced result count, no reliance on color for status, visible focus.",
    deps="PLAT-003; PAT-003; local search index.",
    open="Search ranking and whether batches/receipts are in Phase 1 global search remain unresolved.",
    notes="Phone values are fictional. Result cap and pagination must be enforced in implementation.",
    html=shell_search())

add(id="DASH-001", name="Dashboard", slug="dashboard", section="Dashboard", feature="Dashboard",
    source="14-Dashboard.md", purpose="Give each role a same-day operational view of visits, due vaccinations, stock risk and collections.",
    users="All staff (role-aware content)", permissions="Dashboard widgets are filtered by role; financial widget requires finance permission.",
    entry="Default post-login route; sidebar Dashboard.", navigation="Widgets and actions deep-link to patients, vaccinations, reminders, inventory, finance.",
    layout=["Page header with date and actions", "Four metric cards", "Today's clinic schedule", "Needs attention", "Due today"],
    components=["Metric cards", "Schedule rows", "Alert cards", "Status badges", "Quick actions"],
    data=["18 visits", "7 due vaccinations", "3 low-stock items", "₹18,450 collections (fictional)"],
    actions=["Record vaccination", "Register patient", "Open patients", "New consultation", "View due list"],
    forms=[],
    states=["Morning/ready", "Loading skeleton", "Offline (banner)", "No visits today", "Role without financial widget", "Sync conflict attention"],
    offline="Shows local data with an offline banner and pending badges; no silent freshness claim.",
    keyboard="Skip link to main content; action buttons reachable in DOM order; table/schedule rows expose links.",
    a11y="Metric values have text labels; alerts not color-only; heading hierarchy; schedule rows have descriptive links.",
    deps="DSH-001–005; PAT/VAC/REM/INV/FIN data; local cache; sync status.",
    open="Exact widget priority per role and whether collections belong on the doctor dashboard are unresolved.",
    notes="All numbers and names are fictional design data. The dashboard is a composition, not five separate screens.",
    html=dashboard())

# Patients
add(id="PAT-001", name="Patient list", slug="patient-list", section="Patients", feature="Patient Management",
    source="04-Patient-Management.md", purpose="Find, filter and act on active patient records without loading the full patient table into the renderer.",
    users="Admin, doctor, receptionist, nurse", permissions="Read all clinical roles; create per approved role; edit/merge/archive role-gated.",
    entry="Sidebar Patients; dashboard links; global search 'view all'.", navigation="Open profile; register; merge; export; filter chips.",
    layout=["Page header", "Saved views", "Search and filters", "Patient table", "Pagination"],
    components=["Search input", "Filter chips", "Data table", "Status badges", "Pagination", "Bulk selection box"],
    data=["2,418 active records (fictional)", "8 visible patients", "Clinic IDs, ages, phones, last visit, next due"],
    actions=["Register patient", "Merge records", "Filter", "Sort (not shown as active)", "Export", "Open patient"],
    forms=["Search query", "Filter chips"],
    states=["Loading skeleton", "Empty clinic", "No search results", "Offline/pending", "Permission-limited columns"],
    offline="Local index search; pending-sync filter remains available; archived records excluded.",
    keyboard="/ focuses search; arrow keys move rows in implementation; Enter opens; selection checkboxes have labels.",
    a11y="Table caption and scope attributes required; status text as well as color; row actions labelled with patient name in implementation.",
    deps="PAT-001–007; local search; role gates.",
    open="Clinic ID format and whether nurses may create/edit are unresolved. Export scope is not approved.",
    notes="Rows are fictional. The table is bounded; the renderer must not fetch all patients to filter locally.",
    html=patient_list())

add(id="PAT-002", name="Register patient", slug="register-patient", section="Patients", feature="Patient Management",
    source="04-Patient-Management.md", purpose="Create an offline-capable, idempotent demographic record with a stable UUID and unique clinic ID.",
    users="Admin, doctor, receptionist, nurse (create permission proposed)", permissions="Create is proposed for all four roles; confirm before implementation.",
    entry="Patient list Register; dashboard Register patient; global search action.", navigation="Save → patient profile. Save & add vaccination → vaccination form with patient prefilled.",
    layout=["Page header with actions", "Child details form", "Contact and address form", "Initial note", "Right validation and next-steps rail"],
    components=["Text/date/select fields", "Textarea", "Duplicate-check confirmation", "Context rail", "Primary and secondary save"],
    data=["Prefilled fictional DOB and registration date", "Generated clinic ID placeholder"],
    actions=["Register patient", "Save & add vaccination", "Cancel"],
    forms=["Full name (required)", "DOB (required, not future)", "Gender (required, allowed values)", "Phone (required, normalized)", "Alternate phone", "Address (optional, bounded)", "Initial note", "Duplicate-check acknowledgement"],
    states=["Ready", "Saving/local commit", "Validation error", "Duplicate warning", "Offline", "Conflict on clinic ID"],
    offline="Writes commit to the local database and outbox; retry is idempotent by patient UUID.",
    keyboard="Tab order follows visual order; date picker keyboard accessible; Ctrl/Cmd+Enter saves in implementation.",
    a11y="Labels are always visible; required fields indicated with text/asterisk; errors linked to fields; no placeholder-only labels.",
    deps="PAT-001–007; local persistence; audit; duplicate search.",
    open="Role permissions, clinic ID format, and whether initial notes are clinical are unresolved.",
    notes="The clinic ID is intentionally not editable in this design. A duplicate warning must appear before commit.",
    html=patient_register())

add(id="PAT-003", name="Patient profile", slug="patient-profile", section="Patients", feature="Patient Management",
    source="04-Patient-Management.md", purpose="Provide a complete chronological patient timeline across visits, vaccinations, consultations, payments, notes, documents and audit.",
    users="All clinical roles", permissions="Read role-scoped; financial actions require finance permission; clinical notes hidden from non-clinical roles.",
    entry="Patient list or global search result.", navigation="Tabs, quick actions, edit, vaccination, consultation, payment, archive.",
    layout=["Page header", "Patient identity ribbon", "Tabs", "Timeline", "Record details rail", "Care summary and quick actions"],
    components=["Identity ribbon", "Tabs", "Timeline", "Status badges", "Key-value rail", "Alert"],
    data=["Fictional patient Aarav Sharma", "Visit and vaccination history", "₹ payments", "Receipt reference"],
    actions=["Record vaccination", "New consultation", "Edit", "Add note", "Add reminder", "Archive", "Open sync center"],
    forms=[],
    states=["Ready", "Loading", "Empty timeline", "Pending sync", "Conflict", "Archived read-only", "Large timeline pagination"],
    offline="Timeline reads local data; pending records show local-only badges; cache invalidates after dependent writes.",
    keyboard="Tabs use arrow-key semantics; timeline items are links where applicable; focus ring visible on rail actions.",
    a11y="Patient name is the page heading; timeline ordered list; dates and times explicit; badges not color-only.",
    deps="PAT-004; VAC; CON; FIN; RCP; REM; AUD; local cache.",
    open="Documents eligibility, note visibility, and whether archived records can be restored are unresolved.",
    notes="The timeline must not be cached independently from dependent writes.",
    html=patient_profile())

add(id="PAT-004", name="Edit patient", slug="edit-patient", section="Patients", feature="Patient Management",
    source="04-Patient-Management.md", purpose="Edit demographic and contact details while preserving audit and avoiding clinical-note overwrite.",
    users="Admin, doctor, receptionist (proposed)", permissions="Edit demographics only where approved; archive is role-gated.",
    entry="Patient profile Edit.", navigation="Save returns to profile with audit; archive opens its own confirmation.",
    layout=["Profile context behind scrim", "Right drawer form", "Record metadata", "Footer actions"],
    components=["Drawer", "Form fields", "Audit metadata", "Archive link"],
    data=["Fictional patient demographics", "Created/updated metadata"],
    actions=["Save changes", "Cancel", "Archive"],
    forms=["Full name", "DOB", "Gender", "Phone", "Alternate phone", "Address"],
    states=["Ready", "Saving", "Validation error", "Conflict", "Permission denied"],
    offline="Local edit and outbox; conflict surfaces rather than silently overwriting.",
    keyboard="Focus enters drawer; Escape cancels if no unsaved changes; focus returns to Edit.",
    a11y="Drawer is a labelled dialog; background inert; form errors announced.",
    deps="PAT-001–007; audit.",
    open="Whether receptionists may edit and whether edits to identifiers require re-verification are unresolved.",
    notes="Clinical history is deliberately not editable in this drawer.",
    html=patient_edit_drawer())

add(id="PAT-005", name="Duplicate warning", slug="duplicate-warning", section="Patients", feature="Patient Management",
    source="04-Patient-Management.md", purpose="Warn before creating a likely duplicate and offer a clear route to the existing record.",
    users="Registration and clinical roles", permissions="Create/read patient records.",
    entry="Registration submit when name/phone fuzzy match exists.", navigation="Review existing → profile. Create new → requires documented reason.",
    layout=["Registration context behind scrim", "Wide warning dialog", "Match cards", "Reason field", "Decision footer"],
    components=["Warning dialog", "Match cards", "Badges", "Reason input"],
    data=["Two fictional similar records", "Same phone, different visit history"],
    actions=["Review existing record", "Create new record", "Cancel"],
    forms=["Override reason (required to continue with a new record)"],
    states=["One match", "Multiple matches", "Exact clinic ID conflict", "Offline local match"],
    offline="Duplicate checks use the local index; remote-only matches may appear later and must not merge silently.",
    keyboard="Focus trap; primary action is review, not blind creation; Escape cancels.",
    a11y="Dialog title names the risk; match similarity explained in text; destructive/override action visually distinct.",
    deps="PAT-003/007; local search; audit.",
    open="Override permissions, fuzzy-match threshold and whether phone is mandatory for registration remain unresolved.",
    notes="The dialog is a warning, not an automatic merge. It must not expose more PHI than needed.",
    html=patient_duplicate_dialog())

add(id="PAT-006", name="Merge patients", slug="merge-patients", section="Patients", feature="Patient Management",
    source="04-Patient-Management.md", purpose="Merge duplicate identities while preserving dependent history, payments and audit.",
    users="Admin and doctor (proposed)", permissions="Merge/archive requires admin or doctor confirmation; confirm policy.",
    entry="Patient list Merge records, or duplicate review.", navigation="Merge → surviving profile. Failure → both records remain.",
    layout=["Patient list context behind scrim", "Wide comparison dialog", "Primary/secondary cards", "Field resolution table", "Confirmation"],
    components=["Comparison table", "Primary/secondary cards", "Merge confirmation", "Warning alert"],
    data=["Fictional duplicate Aarav records", "Dependent record counts"],
    actions=["Merge records", "Cancel"],
    forms=["Primary record selection", "Field resolution", "Merge acknowledgement"],
    states=["Ready", "Blocked by open visit", "Conflict", "Merging", "Failed rollback", "Offline policy blocked"],
    offline="Merge is queued only if the policy supports it; otherwise this operation requires connectivity.",
    keyboard="Selection controls and comparison table are keyboard accessible; destructive merge requires explicit confirmation.",
    a11y="Diff table uses headers; primary vs secondary not color-only; consequence described plainly.",
    deps="PAT-001–007; FIN; VAC; CON; audit; sync conflict policy.",
    open="Is merge reversible? Who may merge? How are conflicting clinic IDs resolved?",
    notes="This is a high-risk flow. Do not implement until the merge policy and rollback behavior are approved.",
    html=patient_merge_dialog())

add(id="PAT-007", name="Archive patient", slug="archive-patient", section="Patients", feature="Patient Management",
    source="04-Patient-Management.md", purpose="Soft-delete a patient with a reason while keeping clinical and financial history for audit.",
    users="Admin and doctor (proposed)", permissions="Merge/archive requires admin or doctor confirmation.",
    entry="Patient profile more menu or edit drawer Archive.", navigation="Archive → active patient list; restore policy not approved.",
    layout=["Profile context behind scrim", "Narrow dialog", "Linked-record warning", "Reason field", "Confirmation"],
    components=["Destructive dialog", "Warning", "Reason textarea", "Confirmation checkbox"],
    data=["Fictional patient record", "3 vaccinations, 2 consultations, 3 payments"],
    actions=["Archive patient", "Cancel"],
    forms=["Archive reason (required)", "Confirmation checkbox (required)"],
    states=["Ready", "Validation error", "Archiving", "Linked record blocks", "Already archived"],
    offline="Archive may be queued only when the deletion contract supports it; current desktop behavior is unresolved.",
    keyboard="Focus trap; archive button requires explicit checkbox; Escape cancels.",
    a11y="Destructive action labelled; consequences in text; reason field associated with error.",
    deps="PAT-006; AUD; sync deletion contract.",
    open="Restore policy and whether archive is allowed offline are unresolved. NCC-039 deletion contract remains open.",
    notes="No hard delete. Linked history is preserved.",
    html=patient_archive_dialog())
