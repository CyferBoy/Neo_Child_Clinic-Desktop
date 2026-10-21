"""Administration, system health and settings screens."""
from __future__ import annotations

from components import (
    alert, avatar, badge, btn, checkbox, drawer_overlay, field, icon, icon_btn,
    kv_list, modal_overlay, page_head, pagination, search_input, select_field,
    shell_page, table, tabs, textarea, timeline, toggle, USER_ADMIN,
)

SCREENS = []


def add(**kwargs):
    kwargs.setdefault("dark_variant", False)
    kwargs.setdefault("wide_variant", False)
    SCREENS.append(kwargs)


def settings_nav(active: str):
    items = [
        ("SET-001", "Appearance", "sun"),
        ("SET-002", "Notifications", "bell"),
        ("SET-003", "Security & sessions", "shield"),
        ("SET-004", "Clinic & safety", "settings"),
    ]
    links = "".join(
        f'<a class="settings-link {"active" if sid == active else ""}" href="{sid}.html">{icon(ic, 15)}<span>{label}</span></a>'
        for sid, label, ic in items
    )
    return f'''<aside class="settings-nav"><div class="settings-nav-label">Settings</div>{links}<div class="settings-nav-note">{icon("info", 13)} Device preferences are personal. Clinic policy is admin-only.</div></aside>'''


def settings_page(active, title, subtitle, content):
    # Page content supplies its own page head; rendering a second Settings head
    # here wasted 100px of the 1366x768 viewport and clipped every settings page.
    body = f'''<div class="settings-shell">{settings_nav(active)}<div class="settings-content">{content}</div></div>'''
    return shell_page(active, "Settings", USER_ADMIN, body)


# ---------------------------------------------------------------------------
# Staff
# ---------------------------------------------------------------------------

def staff_list_content():
    rows = [
        ("<div class='identity'><span class='avatar'>AR</span><div class='identity-main'><div class='identity-name'>Ananya Rao <span class='tiny muted'>· You</span></div><div class='identity-sub'>Admin · EMP-001</div></div></div>", "ananya.rao@neoclinic.example", badge("Admin", "brand"), "Today · 09:02", "Current session", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar info'>MN</span><div class='identity-main'><div class='identity-name'>Dr. Meera Nair</div><div class='identity-sub'>Doctor · EMP-004</div></div></div>", "meera.nair@neoclinic.example", badge("Doctor", "info"), "Today · 08:47", "2 sessions", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar success'>RS</span><div class='identity-main'><div class='identity-name'>Ritika Sen</div><div class='identity-sub'>Nurse · EMP-007</div></div></div>", "ritika.sen@neoclinic.example", badge("Nurse", "success"), "Today · 08:51", "1 session", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar apricot'>KI</span><div class='identity-main'><div class='identity-name'>Kavya Iyer</div><div class='identity-sub'>Receptionist · EMP-009</div></div></div>", "kavya.iyer@neoclinic.example", badge("Receptionist", "neutral"), "Today · 08:40", "1 session", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar' style='opacity:.65'>NV</span><div class='identity-main'><div class='identity-name'>Dr. Nikhil Verma</div><div class='identity-sub'>Doctor · EMP-016</div></div></div>", "nikhil.verma@neoclinic.example", badge("Doctor", "info"), "3 Oct 2026", "—", badge("Deactivated", "neutral"), f"<span class='row-action'>{icon('more', 16)}</span>"),
    ]
    content = f'''{page_head("Administration · access", "Staff", "Create and manage clinic accounts. Staff administration requires connectivity and an active admin session.", btn("Add staff member", "primary", "user-plus", href="STF-002.html") + btn("Export staff list", "secondary", "download"))}
    <div class="alert warning">{icon("shield", 15)}<div><strong>Admin-only area.</strong> Staff account changes use the existing <code>manage-staff</code> Edge Function. Service-role credentials never enter the desktop app.</div></div>
    <div style="margin-top:12px;margin-bottom:10px">{tabs([("All staff", "12"), ("Active", "11"), ("Deactivated", "1"), ("Pending", "0")], 0, extra=f'<span class="spacer" style="flex:1"></span><span class="small muted">Auth users and profiles stay in sync</span>')}</div>
    <div class="toolbar">{search_input("Search name, email, role or employee ID")}<span class="spacer"></span><span class="toolbar-select">All roles {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
    <div class="table-card">{table(["Staff", "Work email", "Role", "Last active", "Sessions", "Status", ""], rows, widths=["w-name", "", "w-status", "w-date", "w-session", "w-status", "w-actions"])}{pagination("1–5 of 12 staff", ("‹", "1", "2", "›"))}</div>
    <div class="alert info mt-12">{icon("info", 15)}<div><strong>Self-protection is enforced.</strong> You cannot change your own role, deactivate yourself, or delete your own account. The last-admin guard is still under review.</div></div>'''
    return content


def staff_list():
    return shell_page("STF-001", "Staff", USER_ADMIN, staff_list_content(), attention=6)


def staff_form_drawer():
    base = staff_list_content()
    drawer = f'''<div class="drawer wide" role="dialog" aria-modal="true" aria-labelledby="add-staff-title">
      <div class="drawer-head"><div><div class="drawer-title" id="add-staff-title">Add staff member</div><div class="drawer-sub">Creates an Auth user and clinic profile together</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="drawer-body">
        {alert("Account administration requires connectivity. This form is not queued offline and temporary passwords are never logged. If profile creation fails, the backend must roll back the Auth user.", "warning", "shield")}
        <div class="form-grid mt-12">
          {field("Full name", "", required=True, placeholder="e.g. Dr. Asha Menon", width="full")}
          {field("Work email", "", required=True, placeholder="name@neoclinic.example", icon_name="mail")}
          {select_field("Role", "Doctor", required=True)}
          {field("Temporary password", "", required=True, icon_name="lock")}
          <div class="field"><label>Confirm password <span class="req">*</span></label><div class="input">{icon("lock", 14)}<span class="placeholder">Re-enter temporary password</span></div></div>
          {field("Employee ID", "", placeholder="EMP-000")}
          {field("Phone", "", placeholder="+91 00000 00000", icon_name="phone")}
        </div>
        <div class="help mt-8">{icon("info", 12)} Password: minimum 12 characters, shown once. Email uniqueness and the role claim are checked by the shared backend. Roles: doctor (clinical), nurse (vaccinations/reminders), receptionist (patients/payments), inventory manager (stock/batches).</div>
      </div>
      <div class="drawer-foot"><button class="btn" type="button">Cancel</button><div class="spacer"></div><button class="btn primary" type="button">Create staff account</button></div>
    </div>'''
    return drawer_overlay(base, "STF-001", "Staff", USER_ADMIN, drawer)


def deactivate_staff_dialog():
    base = staff_list_content()
    modal = f'''<div class="dialog narrow" role="dialog" aria-modal="true" aria-labelledby="deactivate-title">
      <div class="dialog-head"><div class="dialog-icon danger">{icon("user-x", 18)}</div><div><div class="dialog-title" id="deactivate-title">Deactivate this staff account?</div><div class="dialog-sub">Ritika Sen · Nurse · ritika.sen@neoclinic.example</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        <p class="muted" style="font-size:11.5px;line-height:1.55">Deactivation blocks future sign-in and revokes refresh capability for existing sessions. The profile and its audit history are preserved.</p>
        {alert("This is not a soft-delete. The account remains in the staff list with a deactivated status and can be reactivated by an admin.", "warning", "alert-triangle")}
        <div class="mt-12">{kv_list([("Role", "Nurse"), ("Last active", "Today · 08:51"), ("Open sessions", "1"), ("Linked records", "Clinical actions remain attributed")])}</div>
        <div class="field mt-12"><label>Reason <span class="req">*</span></label><div class="select"><span>Role change / no longer at clinic</span>{icon("chevron-down", 14)}</div></div>
        <div class="field mt-12"><label>Admin note</label><div class="textarea"><span class="placeholder">Visible to admins in the audit log</span></div></div>
        <div class="check-row mt-8"><span class="checkbox"></span><span class="check-text">I understand existing refresh capability must be revoked, not just hidden in the UI.</span></div>
      </div>
      <div class="dialog-foot"><button class="btn ghost" type="button">Cancel</button><div class="spacer"></div><button class="btn danger" type="button">Deactivate account</button></div>
    </div>'''
    return modal_overlay(base, "STF-001", "Staff", USER_ADMIN, modal)


def reset_password_dialog():
    base = staff_list_content()
    modal = f'''<div class="dialog narrow" role="dialog" aria-modal="true" aria-labelledby="reset-title">
      <div class="dialog-head"><div class="dialog-icon">{icon("key", 18)}</div><div><div class="dialog-title" id="reset-title">Send a password reset?</div><div class="dialog-sub">Dr. Meera Nair · meera.nair@neoclinic.example</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        <p class="muted" style="font-size:11.5px;line-height:1.55">A reset link is sent to the staff member's work email through the shared Auth service. No password is displayed, generated in the renderer, or written to logs.</p>
        {alert("The current session is not revoked by a reset request unless the backend policy says so. Existing refresh capability may remain valid.", "info", "info")}
        <div class="mt-12">{kv_list([("Account", "Dr. Meera Nair"), ("Role", "Doctor"), ("Status", "Active"), ("Delivery", "Work email")])}</div>
        <div class="check-row mt-12"><span class="checkbox"></span><span class="check-text">I verified the staff member's identity before sending this reset.</span></div>
      </div>
      <div class="dialog-foot"><button class="btn ghost" type="button">Cancel</button><div class="spacer"></div><button class="btn primary" type="button">Send reset email</button></div>
    </div>'''
    return modal_overlay(base, "STF-001", "Staff", USER_ADMIN, modal)


add(id="STF-001", name="Staff list", slug="staff-list", section="Administration", feature="Staff and Role Management",
    source="03-Staff-and-Role-Management.md", purpose="List clinic staff, roles, status and sessions; provide admin-only entry points for account lifecycle actions.",
    users="Admin only", permissions="Admin-only. Non-admin direct backend calls must return 401/403 without staff data.",
    entry="Sidebar Staff, visible only to admins.", navigation="Add staff; reset password; deactivate; edit role/profile (proposed).",
    layout=["Page header", "Admin boundary alert", "Status tabs", "Search/filter toolbar", "Staff table", "Self-protection note"],
    components=["Tabs", "Table", "Role/status badges", "Row actions", "Search"],
    data=["12 fictional staff", "5 roles", "1 deactivated account", "Current and last-active sessions"],
    actions=["Add staff member", "Export staff list", "Row actions", "Filter"],
    forms=["Search", "Role filter"],
    states=["Loading", "Empty", "Ready", "Permission denied", "Offline read-only", "Conflict/stale"],
    offline="Cached list may be read-only. Account administration is disabled offline and must not be queued for replay.",
    keyboard="/ search; row menus labelled with name; tabs arrow-key semantics.",
    a11y="Role/status text; self badge; table headers; no color-only meaning.",
    deps="STF-001–006; AUTH; manage-staff Edge Function; audit.",
    open="Last-admin protection server-side? Email verification? Who can reset passwords? Role changes forcing sign-out?",
    notes="No passwords are displayed. Shared accounts are prohibited.",
    html=staff_list())


add(id="STF-002", name="Add staff member", slug="add-staff-member", section="Administration", feature="Staff and Role Management",
    source="03-Staff-and-Role-Management.md", purpose="Create an Auth user and clinic profile with a role, temporary password and optional employee data.",
    users="Admin only", permissions="Admin only; online only; backend service-role handled by the Edge Function.",
    entry="Staff list Add staff member.", navigation="Create → staff list. Cancel → staff list. Auth/profile failure must roll back.",
    layout=["Staff list context behind scrim", "Wide right drawer", "Account fields", "Password fields", "Role summary", "Create action"],
    components=["Drawer", "Text/email/password fields", "Role select", "Role capability summary", "Warnings"],
    data=["Fictional placeholder identity", "Role choices: Admin, Doctor, Nurse, Receptionist, Inventory manager"],
    actions=["Create staff account", "Cancel"],
    forms=["Full name (required)", "Work email (required, unique)", "Role (required, allowed values)", "Temporary password ≥12 chars (required)", "Confirm password", "Employee ID", "Phone", "Admin note"],
    states=["Ready", "Saving", "Validation", "Duplicate email", "Offline disabled", "Partial backend failure/rollback", "Permission denied"],
    offline="Disabled. Account creation cannot be queued offline.",
    keyboard="Focus enters drawer; password visibility control keyboard accessible; Escape cancels if no unsaved changes.",
    a11y="Labelled fields; password guidance text; errors linked; role descriptions readable.",
    deps="STF-001/003; manage-staff; Auth; audit.",
    open="Password delivery method, email verification, employee-ID uniqueness and rollback observability.",
    notes="The temporary password is never logged or stored in plaintext. This preview displays no real credential.",
    html=staff_form_drawer())


add(id="STF-003", name="Deactivate staff", slug="deactivate-staff", section="Administration", feature="Staff and Role Management",
    source="03-Staff-and-Role-Management.md", purpose="Deactivate an account with a reason, revoking refresh capability without deleting history.",
    users="Admin only; self-deactivation forbidden", permissions="Admin only; cannot target own account.",
    entry="Staff list row Deactivate.", navigation="Deactivate → staff list with audited status. Cancel → list.",
    layout=["Staff list behind scrim", "Narrow confirmation dialog", "Session/consequence warning", "Reason and note", "Acknowledgement"],
    components=["Destructive dialog", "Warning", "Key-values", "Reason select", "Note", "Checkbox"],
    data=["Ritika Sen · Nurse", "1 open session", "Last active today"],
    actions=["Deactivate account", "Cancel"],
    forms=["Reason (required)", "Admin note", "Refresh-revocation acknowledgement"],
    states=["Ready", "Validation", "Self-target blocked", "Last-admin blocked", "Offline disabled", "Conflict"],
    offline="Disabled. Deactivation requires backend Auth session revocation.",
    keyboard="Focus trap; Escape cancels; explicit acknowledgement.",
    a11y="Consequence text; destructive action labelled; no color-only status.",
    deps="STF-001/004; Auth; audit; session revocation.",
    open="Reactivation policy, last-admin guard and immediate session invalidation.",
    notes="Deactivation is not deletion; clinical attribution is preserved.",
    html=deactivate_staff_dialog())


add(id="STF-004", name="Reset staff password", slug="reset-staff-password", section="Administration", feature="Staff and Role Management",
    source="03-Staff-and-Role-Management.md", purpose="Trigger a password reset email without exposing or generating a password in the desktop UI.",
    users="Admin only (open question)", permissions="Admin only; reset authorization policy unresolved.",
    entry="Staff list row Reset password.", navigation="Send → staff list with audit. Cancel → list.",
    layout=["Staff list behind scrim", "Narrow dialog", "Reset consequence", "Account context", "Identity verification"],
    components=["Dialog", "Info alert", "Key-values", "Verification checkbox"],
    data=["Dr. Meera Nair", "Work email delivery", "Active account"],
    actions=["Send reset email", "Cancel"],
    forms=["Identity verification acknowledgement"],
    states=["Ready", "Sending", "Email delivery failure", "Inactive account", "Permission denied"],
    offline="Disabled; reset requires Auth connectivity.",
    keyboard="Focus trap; Escape cancel; primary action explicit.",
    a11y="No password disclosure; delivery and session caveats in text.",
    deps="STF-001/003; Auth; audit.",
    open="Who may reset passwords, whether reset revokes sessions, inactive-user reset behavior.",
    notes="No password is displayed or generated in the renderer.",
    html=reset_password_dialog())


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

def audit_list_content():
    rows = [
        ("20 Oct 2026<span class='sub'>09:06:12 IST</span>", "<div class='identity'><span class='avatar sm'>KI</span><div><div class='identity-name'>Kavya Iyer</div><div class='identity-sub'>Receptionist</div></div></div>", badge("Payment created", "success"), "PAY-40871", "Aarav Sharma · NCC-2026-00418", "Local → queued", badge("Pending sync", "info", "refresh"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("20 Oct 2026<span class='sub'>09:05:44 IST</span>", "<div class='identity'><span class='avatar sm'>RS</span><div><div class='identity-name'>Ritika Sen</div><div class='identity-sub'>Nurse</div></div></div>", badge("Vaccination recorded", "success"), "V-10942", "Aarav Sharma · NCC-2026-00418", "Local → queued", badge("Pending sync", "info", "refresh"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("20 Oct 2026<span class='sub'>08:58:02 IST</span>", "<div class='identity'><span class='avatar sm'>KI</span><div><div class='identity-name'>Kavya Iyer</div><div class='identity-sub'>Receptionist</div></div></div>", badge("Receipt printed", "info"), "NCC-R-004196", "Diya Menon · NCC-2026-00502", "Desktop print bridge", badge("Synced", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("20 Oct 2026<span class='sub'>08:51:10 IST</span>", "<div class='identity'><span class='avatar sm'>RS</span><div><div class='identity-name'>Ritika Sen</div><div class='identity-sub'>Nurse</div></div></div>", badge("Sign in", "neutral"), "SESSION-8821", "No patient data", "Supabase Auth", badge("Success", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("20 Oct 2026<span class='sub'>08:44:31 IST</span>", "<div class='identity'><span class='avatar sm'>AR</span><div><div class='identity-name'>Ananya Rao</div><div class='identity-sub'>Admin</div></div></div>", badge("Stock adjusted", "warning"), "ADJ-2044", "PCV-2411 · batch", "Local → conflict", badge("Conflict", "danger", "alert-triangle"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("19 Oct 2026<span class='sub'>17:12:44 IST</span>", "<div class='identity'><span class='avatar sm'>MN</span><div><div class='identity-name'>Dr. Meera Nair</div><div class='identity-sub'>Doctor</div></div></div>", badge("Consultation deleted", "danger"), "C-2074", "Vivaan Nair · NCC-2025-01102", "Local → synced", badge("Synced", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("19 Oct 2026<span class='sub'>16:42:10 IST</span>", "<div class='identity'><span class='avatar sm'>AR</span><div><div class='identity-name'>Ananya Rao</div><div class='identity-sub'>Admin</div></div></div>", badge("Patient merged", "warning"), "MERGE-0091", "Aarav S. → Aarav Sharma", "Local → synced", badge("Synced", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
    ]
    content = f'''{page_head("Administration · governance", "Audit log", "Append-only record of sensitive actions. Actor identity is derived from the authenticated session, never from this UI.", btn("Export redacted extract", "secondary", "download"))}
    <div class="row tight" style="margin-bottom:12px">
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Events today</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700">128</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Sensitive actions</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700">12</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Sync unresolved</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700;color:var(--danger-700)">2</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Retention</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700">90 days <span class="small muted" style="font-weight:500">policy</span></div></div>
    </div>
    <div style="margin-bottom:10px">{tabs([("All events", "1,284"), ("Sensitive", "86"), ("Conflicts", "2"), ("Auth", "42"), ("Sync", "18")], 0, extra=f'<span class="spacer" style="flex:1"></span><span class="small muted">{icon("lock", 12)} Admin read · append-only</span>')}</div>
    <div class="toolbar">{search_input("Search actor, action, entity or patient ID")}<span class="spacer"></span><span class="toolbar-select">Today {icon("chevron-down", 12)}</span><span class="toolbar-select">All actors {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
    <div class="table-card">{table(["Time", "Actor", "Action", "Entity", "Patient / subject", "Source", "Status", ""], rows, widths=["w-date", "w-name", "w-status", "w-date", "", "w-date", "w-status", "w-actions"])}{pagination("1–8 of 1,284 events", ("‹", "1", "2", "3", "…", "161", "›"))}</div>
    <div class="alert warning mt-12">{icon("alert-triangle", 15)}<div><strong>Two audit events are unresolved.</strong> One stock adjustment conflict and one receipt event need review before export. Audit rows cannot be edited or deleted.</div></div>'''
    return content


def audit_list():
    return shell_page("AUD-001", "Audit log", USER_ADMIN, audit_list_content(), status="Online")


def audit_detail_drawer():
    base = audit_list_content()
    payload = '''{
  "batch": "PCV-2411",
  "delta": -2,
  "reason": "vial_breakage",
  "local_before": 34,
  "local_after": 32,
  "server_version": 31,
  "conflict": "stock_version_mismatch"
}'''
    drawer = f'''<div class="drawer wide" role="dialog" aria-modal="true" aria-labelledby="audit-detail-title">
      <div class="drawer-head"><div><div class="drawer-title" id="audit-detail-title">Audit event</div><div class="drawer-sub">EVT-9F3A-2044 · append-only</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="drawer-body">
        <div class="row tight" style="align-items:center"><span class="badge danger">Conflict</span><span class="badge neutral">Stock adjustment</span><span class="spacer" style="flex:1"></span><span class="small muted">20 Oct 2026 · 08:44:31 IST</span></div>
        <div class="card standalone mt-12"><div class="card-head"><div><div class="card-title">Actor (server-derived)</div><div class="card-sub">Not supplied by the renderer</div></div><span class="badge success">{icon("shield", 10)} Verified session</span></div><div class="card-body"><div class="identity"><span class="avatar">AR</span><div><div class="identity-name">Ananya Rao</div><div class="identity-sub">Admin · user 4a9c…e21b · session S-8821</div></div></div></div></div>
        <div class="grid-2 mt-12"><div class="card"><div class="card-head"><div class="card-title">Event</div></div><div class="card-body" style="padding-top:8px">{kv_list([("Action", "stock.adjust"), ("Entity", "inventory_batches"), ("Entity ID", "PCV-2411"), ("Operation", "decrement · 2 doses"), ("Source", "local outbox"), ("Status", "conflict")])}</div></div><div class="card"><div class="card-head"><div class="card-title">Integrity</div></div><div class="card-body" style="padding-top:8px">{kv_list([("Event ID", "EVT-9F3A-2044"), ("Hash", "sha256:8f2a…91c0"), ("Synced", "No · conflict"), ("Immutable", "Yes")])}</div></div></div>
        <div class="divider"></div>
        <div class="label">Payload (redacted preview)</div>
        <div class="code-block mt-8">{payload}</div>
        <div class="alert warning mt-12">{icon("alert-triangle", 15)}<div><strong>No PHI in the payload.</strong> Clinical identifiers are referenced by stable ID; patient names are not written to general audit payloads.</div></div>
        <div class="divider"></div>
        <div class="label">Related records</div>
        <div class="mt-8">{kv_list([("Batch", "PCV-2411 · PCV"), ("Open conflict", "SYNC-CONFLICT-12"), ("Actor session", "S-8821 · current"), ("Audit previous event", "EVT-9F3A-2039")])}</div>
        <div class="divider"></div>
        <div class="label">Event history</div>
        {timeline([{"title": "Business action committed", "time": "08:44:30", "body": "Local adjustment + audit intent in one transaction", "tone": "success"}, {"title": "Outbox upload attempted", "time": "08:44:31", "body": "Server stock version changed; hard conflict", "tone": "danger"}, {"title": "Conflict surfaced", "time": "08:44:32", "body": "No retry spawned; no silent overwrite", "tone": "warning"}])}
      </div>
      <div class="drawer-foot"><span class="small muted">Audit records cannot be edited or deleted</span><div class="spacer"></div><button class="btn" type="button">Close</button><button class="btn secondary" type="button">Open sync conflict</button></div>
    </div>'''
    return drawer_overlay(base, "AUD-001", "Audit log", USER_ADMIN, drawer)


add(id="AUD-001", name="Audit log", slug="audit-log", section="Administration", feature="Audit Logging",
    source="21-Audit-Logging.md", purpose="Provide a paged, filtered, append-only audit view for sensitive actions with actor and source visible.",
    users="Admin only for read/export; system writes on behalf of authenticated actors", permissions="Admin read/export. No renderer write path. Policy §7 roles.",
    entry="Sidebar Audit log, admin only.", navigation="Open event detail; filter; export redacted extract (approval pending).",
    layout=["Page header", "Event summary strip", "Category tabs", "Search/filter toolbar", "Audit table", "Unresolved warning"],
    components=["Summary cards", "Tabs", "Table", "Action/status badges", "Row actions"],
    data=["128 events today", "12 sensitive", "2 unresolved", "8 fictional events"],
    actions=["Export redacted extract", "Filter", "Open event"],
    forms=["Search", "Date", "Actor", "Action/entity filters"],
    states=["Loading", "Empty", "Ready", "Permission denied", "Stale/pending", "Audit write failure", "Export denied"],
    offline="Audit intent is local with the business transaction; read view shows pending. Failed sensitive audit must roll back or flag.",
    keyboard="/ search; table rows open; filters accessible; no edit affordances.",
    a11y="Time values explicit with timezone; actor role text; status not color-only; table headers.",
    deps="AUD-001–005; all sensitive modules; sync; export policy.",
    open="Retention, redaction rules, export approval, audit-write failure UX and PHI minimization.",
    notes="This is a business record, not a debug log. No update/delete affordance exists.",
    html=audit_list())


add(id="AUD-002", name="Audit event detail", slug="audit-event-detail", section="Administration", feature="Audit Logging",
    source="21-Audit-Logging.md", purpose="Show one append-only event with server-derived actor, redacted payload, integrity and linked conflict.",
    users="Admin only", permissions="Admin read; no mutation.",
    entry="Audit log row.", navigation="Open linked conflict; close. No edit/delete.",
    layout=["Audit list behind scrim", "Wide right drawer", "Actor card", "Event/integrity cards", "Redacted payload", "Event history"],
    components=["Drawer", "Key-values", "Code block", "Timeline", "Status badges"],
    data=["EVT-9F3A-2044", "Stock adjustment conflict", "PCV-2411", "Admin actor", "Redacted payload"],
    actions=["Close", "Open sync conflict"],
    forms=[],
    states=["Ready", "Payload redacted", "Integrity failure", "Permission denied", "Linked event unavailable"],
    offline="Local audit event read; unresolved sync shown.",
    keyboard="Focus enters drawer; Escape closes; code block scrollable with keyboard.",
    a11y="Code block has accessible label; hash/event ID readable; timeline ordered.",
    deps="AUD-001; audit schema; sync conflict; export.",
    open="What payload fields are lawful/appropriate for audit? Hash verification implementation.",
    notes="The payload contains no patient name; the UI shows only a redacted preview.",
    html=audit_detail_drawer())


# ---------------------------------------------------------------------------
# System: sync, recovery, updates, backup
# ---------------------------------------------------------------------------

def sync_center_content():
    rows = [
        ("Vaccination visit", "Aarav Sharma · V-10942", "Local group · 4 rows", "2 min", "1", badge("Pending", "info", "refresh"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("Stock adjustment", "PCV-2411 · ADJ-2044", "Local group · 2 rows", "8 min", "3", badge("Conflict", "danger", "alert-triangle"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("Payment", "Aarav Sharma · PAY-40871", "Dependent on visit", "2 min", "0", badge("Queued", "warning"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("Patient edit", "Aarav Sharma · PAT-004", "Profile update", "18 min", "1", badge("Pending", "info", "refresh"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("Wastage record", "AV-2409 · WAS-0031", "Local group · 2 rows", "1 h", "0", badge("Pending", "info", "refresh"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("Audit row", "EVT-9F3A-2044", "Append-only", "8 min", "0", badge("Blocked", "danger", "lock"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
    ]
    content = f'''{page_head("System · sync", "Sync center", "Local-first writes upload in dependency order. A group is acknowledged only when every required member is acknowledged.", btn("Sync now", "primary", "refresh") + btn("Pause", "secondary", "pause") + icon_btn("settings", "Sync settings"))}
    <div class="row tight" style="margin-bottom:12px">
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Pending writes</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700">3</div><div class="tiny muted">in 2 groups</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Conflicts</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700;color:var(--danger-700)">1</div><div class="tiny muted">stock · needs review</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Last successful sync</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700">2 min</div><div class="tiny muted">09:34 IST · 18 rows</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Outbox age</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700">1 h 8 m</div><div class="tiny muted">oldest pending row</div></div>
    </div>
    <div class="row" style="height:390px">
      <div class="card grow" style="display:flex;flex-direction:column">
        <div class="card-head"><div><div class="card-title">Outbox</div><div class="card-sub">Upload groups preserve dependencies · retries use the same identity</div></div><span class="badge warning">3 pending</span></div>
        <div style="padding:0 12px"><div class="tab-bar"><div class="tabs" style="border-bottom:0"><span class="tab active">All <span class="count">6</span></span><span class="tab">Pending <span class="count">3</span></span><span class="tab">Conflicts <span class="count">1</span></span><span class="tab">Failed <span class="count">0</span></span></div></div></div>
        <div class="card-body" style="padding:0;flex:1">{table(["Type", "Reference", "Group", "Age", "Attempts", "Status", ""], rows, widths=["", "", "", "w-date", "w-money", "w-status", "w-actions"])}</div>
        <div class="card-foot" style="display:flex;align-items:center;gap:8px"><span class="small muted">{icon("lock", 12)} Outbox is encrypted with the local DB</span><span class="spacer" style="flex:1"></span><span class="small muted">Next retry in 30 s</span></div>
      </div>
      <div class="col tight w-side">
        <div class="card"><div class="card-head"><div class="card-title">Connection</div><span class="badge success">Online</span></div><div class="card-body" style="padding-top:8px"><div class="stat-line"><span>Supabase</span><span class="spacer" style="flex:1"></span><strong>Reachable</strong></div><div class="stat-line"><span>API latency</span><span class="spacer" style="flex:1"></span><strong>128 ms</strong></div><div class="stat-line"><span>Auth</span><span class="spacer" style="flex:1"></span><strong>Valid · 41 min</strong></div><div class="stat-line"><span>Cursor</span><span class="spacer" style="flex:1"></span><strong class="mono">18,204</strong></div><div class="stat-line"><span>Timezone</span><span class="spacer" style="flex:1"></span><strong>IST</strong></div></div></div>
        <div class="card"><div class="card-head"><div class="card-title">Sync actions</div></div><div class="card-body" style="display:flex;flex-direction:column;gap:6px">{btn("Sync now", "primary", "refresh", size="sm")} {btn("Review conflict", "secondary", "alert-triangle", size="sm")} {btn("Pull latest", "ghost", "download", size="sm")} {btn("Open local data", "ghost", "database", size="sm")}</div></div>
        {alert("A retry never spawns a new ID. Receipt and stock conflicts are hard errors, not last-write-wins.", "warning", "info")}
      </div>
    </div>'''
    return content


def sync_center():
    return shell_page("SYS-001", "Sync center", USER_ADMIN, sync_center_content(), status="Syncing", status_tone="syncing", attention=6)


def conflict_content():
    content = f'''{page_head("System · sync conflict", "Resolve a sync conflict", "Stock and receipt conflicts are hard errors. Both sides stay visible; this is not last-write-wins and the physical ledger decides.", btn("Back to sync center", "ghost", "arrow-left", href="SYS-001.html") + btn("Open audit event", "secondary", "clipboard", href="AUD-002.html"))}
    <div class="card">
      <div class="card-head"><div><div class="card-title">Side-by-side comparison</div><div class="card-sub">Same batch changed on two devices within two minutes</div></div><div style="display:flex;gap:6px"><span class="badge danger">1 of 1</span><span class="badge warning">No auto-retry</span></div><span class="badge danger">Unresolved</span></div>
      <div class="card-body" style="padding:0">{table(["Field", "This device", "Shared record", "Interpretation"], [["Batch version", "v18", "v19", badge("Server is newer", "warning")], ["On hand", "34 → 32", "31", badge("Both changes are real", "danger")], ["Movement", "−2 · Ananya · 08:44", "−1 · Ishaan · 08:43", badge("Net effect −3", "warning")]], widths=["w-name", "", "", ""])}</div>
    </div>
    <div class="card mt-12">
      <div class="card-head"><div><div class="card-title">Resolution</div><div class="card-sub">Choose a deliberate path. Every path is audited; no silent overwrite.</div></div></div>
      <div class="card-body"><div class="grid-2"><div class="choice-card" style="border-color:var(--brand-300);background:var(--brand-50)"><div class="strong" style="display:flex;justify-content:space-between;align-items:center">Reapply local against v19 {badge("Audited", "neutral")}</div><div class="small muted mt-4">Recalculate the exact adjustment from both movements.</div></div><div class="choice-card"><div class="strong" style="display:flex;justify-content:space-between;align-items:center">Discard local adjustment {badge("Reason required", "warning")}</div><div class="small muted mt-4">Keep server v19; archive local intent.</div></div></div><div class="field mt-12"><label>Resolution note <span class="req">*</span></label><div class="textarea" style="min-height:40px"><span class="placeholder">Explain the physical count and chosen resolution</span></div></div></div>
      <div class="card-foot" style="display:flex;align-items:center;gap:8px"><span class="small muted">{icon("alert-triangle", 12)} The physical ledger decides, not the timestamp.</span><span class="spacer" style="flex:1"></span><button class="btn ghost" type="button">Cancel</button><button class="btn secondary" type="button">Discard local</button><button class="btn primary" type="button">Resolve & reapply</button></div>
    </div>'''
    return content


def conflict_resolution():
    return shell_page("SYS-001", "Sync conflict", USER_ADMIN, conflict_content(), status="Sync conflict", status_tone="attention")


def local_data_content():
    content = f'''{page_head("System · local data", "Local data & recovery", "The encrypted local database is the working copy. The Go core owns access; the renderer never receives raw rows.", btn("Run integrity check", "secondary", "shield") + btn("Create backup", "primary", "database", href="SYS-006.html"))}
    <div class="row tight" style="margin-bottom:12px">
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Encryption</div><div style="font-family:var(--font-display);font-size:18px;font-weight:700">SQLCipher</div><div class="tiny muted">OS keychain · unlocked</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Schema</div><div style="font-family:var(--font-display);font-size:18px;font-weight:700">v14</div><div class="tiny muted">latest · checked 09:20</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Database size</div><div style="font-family:var(--font-display);font-size:18px;font-weight:700">184 MB</div><div class="tiny muted">disk free 2.4 GB</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Last verified</div><div style="font-family:var(--font-display);font-size:18px;font-weight:700">2 hours</div><div class="tiny muted">integrity check passed</div></div>
    </div>
    <div class="row top">
      <div class="grow col">
        <div class="card"><div class="card-head"><div><div class="card-title">Local database</div><div class="card-sub">This device · clinic binding verified</div></div><span class="badge success">Healthy</span></div><div class="card-body">{kv_list([("Location", "Encrypted app data directory (path hidden in preview)"), ("Key protection", "OS keychain · key not exportable"), ("Schema version", "14 · forward-only migrations"), ("Clinic binding", "Neo Child Clinic · Indiranagar"), ("Last migration", "3 Oct 2026 · succeeded"), ("Writer", "Single Go core process")])}<div class="mt-12">{btn("Run integrity check", "secondary", "shield", size="sm")} {btn("Open migration history", "ghost", "list", size="sm")}</div></div></div>
        <div class="card"><div class="card-head"><div><div class="card-title">Recovery</div><div class="card-sub">Failures are surfaced; success is never assumed from a partial write.</div></div></div><div class="card-body"><div class="stat-line">{icon("check-circle", 13)}<span>Crash recovery journal</span><span class="spacer" style="flex:1"></span><strong>Ready</strong></div><div class="stat-line">{icon("check-circle", 13)}<span>Pre-restore safety snapshot</span><span class="spacer" style="flex:1"></span><strong>Required</strong></div><div class="stat-line">{icon("alert-circle", 13)}<span>Corruption repair</span><span class="spacer" style="flex:1"></span><strong>Manual / audited</strong></div><div class="stat-line">{icon("lock", 13)}<span>Clear local PHI</span><span class="spacer" style="flex:1"></span><strong>Lock / sign-out policy</strong></div></div></div>
        <div class="alert warning">{icon("alert-triangle", 15)}<div><strong>No destructive reset button here.</strong> Clearing local PHI is an admin recovery action with a passphrase and an approved procedure. The final sign-out/idle-lock policy is unresolved.</div></div>
      </div>
      <div class="col tight w-side">
        <div class="card"><div class="card-head"><div class="card-title">Checks</div><span class="badge success">All passed</span></div><div class="card-body" style="padding-top:8px"><div class="stat-line">{icon("check", 13)}<span>Encryption key present</span></div><div class="stat-line">{icon("check", 13)}<span>Schema current</span></div><div class="stat-line">{icon("check", 13)}<span>Foreign keys valid</span></div><div class="stat-line">{icon("check", 13)}<span>Outbox readable</span></div><div class="stat-line">{icon("check", 13)}<span>Disk space adequate</span></div></div></div>
        <div class="card"><div class="card-head"><div class="card-title">Related system pages</div></div><div class="card-body" style="display:flex;flex-direction:column;gap:6px">{btn("Sync center", "secondary", "refresh", size="sm", href="SYS-001.html")} {btn("Backups", "ghost", "database", size="sm", href="SYS-005.html")} {btn("Restore a backup", "ghost", "upload", size="sm", href="SYS-007.html")}</div></div>
        {alert("A local commit is not a cloud acknowledgement. The UI must not call it synced.", "info", "info")}
      </div>
    </div>'''
    return content


def local_data():
    return shell_page("SYS-001", "Local data & recovery", USER_ADMIN, local_data_content(), status="Online")


def update_content():
    content = f'''{page_head("System · updates", "Application updates", "Signed updates install only with explicit consent and never during an active local transaction or unsynced write.", btn("Check for updates", "secondary", "refresh") + btn("Install update", "primary", "download"))}
    <div class="row top">
      <div class="grow col">
        <div class="card"><div class="card-head"><div><div class="card-title">Version 0.2.0 available</div><div class="card-sub">Current 0.1.0-preview · released 18 Oct 2026</div></div><span class="badge success">{icon("shield", 10)} Signature verified</span></div><div class="card-body"><div class="row tight"><div class="grow"><div class="tiny muted">CURRENT VERSION</div><div class="mono" style="font-size:16px;font-weight:700">0.1.0-preview</div></div><div class="grow"><div class="tiny muted">NEW VERSION</div><div class="mono" style="font-size:16px;font-weight:700">0.2.0</div></div><div class="grow"><div class="tiny muted">DOWNLOAD</div><div class="strong">84.2 MB</div></div><div class="grow"><div class="tiny muted">CHANNEL</div><div class="strong">Stable</div></div></div><div class="divider"></div><div class="strong">Release notes</div><ul class="small muted" style="margin:6px 0 0 18px;line-height:1.7"><li>Faster local patient search and clearer sync conflict review.</li><li>Receipt preview now labels provisional numbers explicitly.</li><li>Fixes calendar date handling for IST due boundaries.</li></ul></div></div>
        <div class="card"><div class="card-head"><div><div class="card-title">Install readiness</div><div class="card-sub">The app must be safe to restart</div></div><span class="badge warning">Blocked</span></div><div class="card-body"><div class="stat-line">{icon("check-circle", 13)}<span>Signature verified</span><span class="spacer" style="flex:1"></span><strong>Yes</strong></div><div class="stat-line">{icon("check-circle", 13)}<span>Supported OS / architecture</span><span class="spacer" style="flex:1"></span><strong>Yes</strong></div><div class="stat-line">{icon("check-circle", 13)}<span>Disk space</span><span class="spacer" style="flex:1"></span><strong>2.4 GB free</strong></div><div class="stat-line">{icon("alert-circle", 13)}<span>Pending writes</span><span class="spacer" style="flex:1"></span><strong>3</strong></div><div class="stat-line">{icon("alert-circle", 13)}<span>Local transaction</span><span class="spacer" style="flex:1"></span><strong>None active</strong></div><div class="alert warning mt-12">{icon("alert-triangle", 15)}<div><strong>Sync before installing.</strong> This update will not start while 3 writes are pending. Open the sync center and resolve them first.</div></div></div></div>
        <div class="card"><div class="card-head"><div><div class="card-title">Rollback</div><div class="card-sub">Previous installed version</div></div><span class="badge neutral">Available</span></div><div class="card-body"><div class="row tight"><div class="grow">{kv_list([("Retained version", "0.1.0-preview"), ("Reason to keep", "Recovery if update fails"), ("Artifact", "Signed local installer")])}</div><div>{btn("View rollback details", "ghost", "history", size="sm")}</div></div></div></div>
      </div>
      <div class="col tight w-side">
        <div class="card"><div class="card-head"><div class="card-title">Update policy</div></div><div class="card-body" style="padding-top:8px"><div class="stat-line">{icon("lock", 13)}<span>Signed + verified</span></div><div class="stat-line">{icon("lock", 13)}<span>No downgrade</span></div><div class="stat-line">{icon("lock", 13)}<span>No silent install</span></div><div class="stat-line">{icon("lock", 13)}<span>No telemetry PHI</span></div><div class="stat-line">{icon("check", 13)}<span>Rollback retained</span></div></div></div>
        <div class="card"><div class="card-head"><div class="card-title">Current install</div></div><div class="card-body">{kv_list([("Version", "0.1.0-preview"), ("Channel", "Stable"), ("Installed", "12 Oct 2026"), ("Auto-check", "Weekly"), ("Admin deploy", "Ananya Rao")])}</div></div>
        {alert("Update checks fail gracefully offline; the current version keeps working.", "info", "wifi-off")}
      </div>
    </div>'''
    return content


def updates():
    return shell_page("SYS-001", "Application updates", USER_ADMIN, update_content(), status="Online")


def backups_content():
    rows = [
        ("20 Oct · 03:00", "Automatic", "184 MB", "AES-256", badge("Verified", "success"), "External", f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("19 Oct · 03:00", "Scheduled", "182 MB", "AES-256", badge("Verified", "success"), "External", f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("18 Oct · 03:00", "Scheduled", "181 MB", "AES-256", badge("Verified", "success"), "External", f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("17 Oct · 16:42", "Manual", "180 MB", "AES-256", badge("Verified", "success"), "External", f"<span class='row-action'>{icon('more', 16)}</span>"),
    ]
    content = f'''{page_head("System · backup & recovery", "Backups", "Encrypted local backups for disaster recovery. No automatic cloud upload and no secrets in the archive.", btn("Create backup", "primary", "database", href="SYS-006.html") + btn("Restore from file", "secondary", "upload", href="SYS-007.html"))}
    <div class="row tight" style="margin-bottom:12px">
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Last backup</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700">6 h ago</div><div class="tiny muted">20 Oct 2026 · 03:00</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Verified copies</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700">4</div><div class="tiny muted">checksums passed</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Next scheduled</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700">Tomorrow</div><div class="tiny muted">03:00 IST</div></div>
      <div class="card" style="flex:1;padding:10px 12px"><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Destination</div><div style="font-family:var(--font-display);font-size:18px;font-weight:700">External drive</div><div class="tiny muted">not cloud</div></div>
    </div>
    <div class="row top">
      <div class="grow col">
        <div class="card"><div class="card-head"><div><div class="card-title">Backup history</div><div class="card-sub">Manifest + checksum · restore requires preview and passphrase</div></div><span class="badge success">4 verified</span></div><div class="card-body" style="padding:0">{table(["Created", "Type", "Size", "Protection", "Status", "Location", ""], rows, widths=["w-created", "w-type", "w-size", "w-protect", "w-status", "", "w-actions"])}</div></div>
        <div class="alert info" style="padding:8px 12px">{icon("info", 15)}<div><strong>Backups are PHI.</strong> Store them on an approved encrypted drive. Restore requires a safety snapshot and passphrase.</div></div>
      </div>
      <div class="col tight w-side">
        <div class="card"><div class="card-head"><div><div class="card-title">Backup settings</div><div class="card-sub">Admin-only · audited</div></div></div><div class="card-body">{select_field("Schedule", "Daily · 03:00 IST", width="full")}<div class="mt-8">{select_field("Destination", "External drive · E:", width="full")}</div><div class="mt-8">{field("Retention", "14 days", width="full", help_text="Range validation required.")}</div><div class="mt-8">{checkbox("Require passphrase for every export", checked=True)}{checkbox("Verify checksum after write", checked=True)}</div><div class="mt-12">{btn("Save backup settings", "secondary", "check", size="sm")}</div></div></div>
      </div>
    </div>'''
    return content


def backups():
    return shell_page("SYS-001", "Backups", USER_ADMIN, backups_content(), status="Online")


def backup_export_content():
    content = f'''{page_head("System · backup", "Create encrypted backup", "Export a passphrase-protected local backup. No plaintext PHI may remain in temporary files.", btn("Cancel", "ghost", href="SYS-005.html") + btn("Create encrypted backup", "primary", "lock"))}
    <div class="row top">
      <div class="grow col">
        <div class="card"><div class="card-head"><div><div class="card-title">What will be included</div><div class="card-sub">Local backup contents</div></div></div><div class="card-body"><div class="grid-2"><div class="small"><strong>Included:</strong> patients and clinical history, vaccinations and stock ledger, payments and receipts, audit events.</div><div class="small"><strong>Excluded:</strong> Auth tokens, service keys, renderer caches. Temp files are shredded after write.</div></div><div class="row tight mt-8" style="justify-content:flex-start">{badge("Encrypted", "success")}{badge("Authenticated manifest", "info")}{badge("Clinic bound", "outline")}</div></div></div>
        <div class="form-section"><div class="form-section-head">{icon("lock", 15)}<div class="form-section-title">Passphrase</div><span class="badge warning">Required</span></div><div class="form-section-body"><div class="grid-2 pass-grid">{field("Passphrase", "", required=True, icon_name="lock", help_text="Strong passphrase; never stored in settings or logs.")}{field("Confirm passphrase", "", required=True, icon_name="lock")}</div><div class="mt-8">{field("Destination", "External drive · E:\\NeoClinic\\Backups", required=True, width="full", icon_name="folder", help_text="Choose an approved encrypted destination.")}</div><div class="mt-8">{checkbox("I understand that losing this passphrase makes the backup unrecoverable.", checked=False)}</div><div class="help mt-8">{icon("alert-triangle", 12)} Backups are PHI. Do not save them to a shared or unencrypted folder.</div></div></div>
      </div>
      <div class="col tight w-side">
        <div class="card"><div class="card-head"><div class="card-title">Backup preview</div></div><div class="card-body"><div class="summary-line"><span>Estimated size</span><strong>184 MB</strong></div><div class="summary-line"><span>Destination free</span><strong>1.2 TB</strong></div><div class="summary-line"><span>Schema</span><strong>v14</strong></div><div class="summary-line"><span>App</span><strong>0.1.0-preview</strong></div><div class="summary-line total-line"><span>File</span><strong class="mono">ncc-2026-10-20.nccb</strong></div><div class="help mt-8">Filename is a preview; the final path is chosen locally.</div></div></div>
        <div class="card"><div class="card-head"><div class="card-title">Process</div></div><div class="card-body" style="padding-top:8px"><div class="stat-line">{icon("check-circle", 13)}<span>Quiesce local writes</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Snapshot database</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Encrypt + manifest</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Verify checksum</span></div><div class="stat-line">{icon("alert-circle", 13)}<span>Disk full or interruption</span></div></div></div>
        {alert("No automatic cloud upload. This action is local and audited.", "info", "wifi-off")}
      </div>
    </div>'''
    return content


def backup_export():
    return shell_page("SYS-001", "Create backup", USER_ADMIN, backup_export_content(), status="Online")


def restore_preview_content():
    content = f'''{page_head("System · restore", "Restore preview", "Restore is destructive and admin-only. Preview the manifest, verify compatibility, then create a safety snapshot before writing.", btn("Cancel", "ghost", href="SYS-005.html") + btn("Restore local data", "primary", "upload"))}
    <div class="alert danger" style="margin-bottom:12px;padding:8px 12px">{icon("alert-triangle", 15)}<div><strong>Destructive action.</strong> Current local data is replaced only after a safety snapshot. A failed restore must leave the current data intact.</div></div>
    <div class="row top">
      <div class="grow col">
        <div class="card"><div class="card-head"><div><div class="card-title">Backup manifest & compatibility</div><div class="card-sub">ncc-2026-10-20.nccb · 184 MB · checksum verified</div></div><span class="badge success">5 of 6 checks</span></div><div class="card-body"><div class="grid-2"><div><div class="label">Manifest</div>{kv_list([("Created", "20 Oct 2026 · 03:00"), ("Schema", "v14"), ("App", "0.1.0-preview"), ("Clinic", "Neo Child Clinic"), ("Encryption", "AES-256")])}</div><div><div class="label">Compatibility & safety</div><div class="stat-line">{icon("check-circle", 13)}<span>Passphrase correct</span><span class="spacer" style="flex:1"></span><strong>Yes</strong></div><div class="stat-line">{icon("check-circle", 13)}<span>Checksum / manifest</span><span class="spacer" style="flex:1"></span><strong>Verified</strong></div><div class="stat-line">{icon("check-circle", 13)}<span>Schema compatible</span><span class="spacer" style="flex:1"></span><strong>v14 = v14</strong></div><div class="stat-line">{icon("alert-circle", 13)}<span>Safety snapshot</span><span class="spacer" style="flex:1"></span><strong>Not yet created</strong></div><div class="mt-8">{btn("Create safety snapshot", "secondary", "shield", size="sm")}</div></div></div><div class="help mt-8">Clinic binding matches · disk space sufficient · patients 2,418 · visits 8,942.</div></div></div>
      </div>
      <div class="col tight w-side">
        <div class="card"><div class="card-head"><div class="card-title">What happens</div></div><div class="card-body" style="padding-top:8px"><div class="stat-line">1<span>Quiesce writes</span></div><div class="stat-line">2<span>Safety snapshot</span></div><div class="stat-line">3<span>Atomic replace</span></div><div class="stat-line">4<span>Reconcile sync</span></div><div class="stat-line">5<span>Audit restore</span></div></div></div>
        <div class="card"><div class="card-head"><div class="card-title">Confirm restore</div><span class="badge warning">Required</span></div><div class="card-body">{field("Passphrase", "", required=True, icon_name="lock")}<div class="mt-8">{field("Type RESTORE to confirm", "", required=True, placeholder="RESTORE")}</div><div class="mt-8">{checkbox("I understand local data will be replaced.", checked=False)}</div><div class="help mt-8">{icon("alert-triangle", 12)} Post-restore reconciliation is required.</div></div></div>
      </div>
    </div>'''
    return content


def restore_preview():
    return shell_page("SYS-001", "Restore preview", USER_ADMIN, restore_preview_content(), status="Attention", status_tone="attention")


add(id="SYS-001", name="Sync center", slug="sync-center", section="System", feature="Supabase Synchronization",
    source="17-Supabase-Sync.md", purpose="Make local-first sync observable: pending groups, conflicts, retries and connection state without false acknowledgement.",
    users="All staff; admin for conflict resolution", permissions="Own writes visible; admin can review/resolve conflicts. No raw server credentials.",
    entry="Sidebar Sync center; status pill; pending badges; failed writes.", navigation="Review conflict; pull latest; open local data; pause/resume sync.",
    layout=["Page header", "Four health metrics", "Outbox table with status tabs", "Connection rail", "Sync actions", "Warning"],
    components=["Metric cards", "Tabs", "Outbox table", "Connection key-values", "Status badges", "Actions"],
    data=["3 pending writes", "1 conflict", "2 min last sync", "1 h 8 m oldest", "Fictional groups"],
    actions=["Sync now", "Pause", "Review conflict", "Pull latest", "Open local data"],
    forms=[], states=["Online/synced", "Syncing", "Offline", "Auth expired", "Conflict", "Retry/backoff", "Group failure", "Paused"],
    offline="Shows offline and preserves outbox. No new server acknowledgement is inferred. Retry after re-auth.",
    keyboard="Actions reachable; table rows open; sync status announced without polling noise.",
    a11y="Status text and counts; progress not spinner-only; timestamps include timezone.",
    deps="SYNC-001–007; OFF; local outbox; auth; audit.",
    open="Deletion/absence contract (NCC-023), conflict taxonomy, retry limits, pause semantics and live Supabase status.",
    notes="This preview does not connect to Supabase. The UI must not claim success for a partial group.",
    html=sync_center())


add(id="SYS-002", name="Resolve sync conflict", slug="resolve-sync-conflict", section="System", feature="Supabase Synchronization",
    source="17-Supabase-Sync.md", purpose="Compare local and server versions of a high-risk stock conflict and resolve deliberately, with audit and no last-write-wins.",
    users="Admin (proposed), with domain input", permissions="Admin review; stock/money/clinical conflicts never auto-resolve.",
    entry="Sync center conflict row; audit event linked conflict.", navigation="Resolve and reapply; discard local; cancel; open audit.",
    layout=["Page header", "Conflict summary strip", "Danger alert", "Local vs server cards", "Comparison table", "Resolution choice", "Why-blocked rail"],
    components=["Comparison cards", "Diff table", "Resolution cards", "Reason field", "Warning alerts"],
    data=["PCV-2411", "Local −2 · server −1", "v18 → v19", "Physical count not verified"],
    actions=["Resolve & reapply", "Discard local", "Cancel", "Open audit event"],
    forms=["Resolution choice (required)", "Resolution note (required)"],
    states=["Unresolved", "Resolving", "Reapply conflict", "Discarded", "Permission denied", "Server changed again"],
    offline="Conflict resolution requires a current server version; cannot be done offline.",
    keyboard="Choice cards keyboard selectable; destructive/discard separated; reason required.",
    a11y="Both sides labelled; interpretation text; no color-only conflict; table headers.",
    deps="SYS-001; INV; audit; sync conflict engine.",
    open="Exact resolution math, admin authority, physical-count verification, reapply semantics, receipt conflicts.",
    notes="The UI deliberately avoids a simple 'Keep mine/Keep theirs' timestamp choice.",
    html=conflict_resolution())


add(id="SYS-003", name="Local data & recovery", slug="local-data-recovery", section="System", feature="Local Persistence and Offline Operation",
    source="16-Local-Persistence-and-Offline-Operation.md", purpose="Expose local database health, encryption, schema, disk and recovery posture without raw data access.",
    users="Admin/support with approved procedure; all staff may see health", permissions="No raw DB access from renderer. Destructive recovery admin-only.",
    entry="Sync center Open local data; system health.", navigation="Run integrity check; backup; restore; migration history.",
    layout=["Page header", "Four health metrics", "Database details", "Recovery card", "Warning", "Checks rail", "Related system pages"],
    components=["Metric cards", "Key-values", "Status checks", "Actions", "Warnings"],
    data=["SQLCipher", "schema v14", "184 MB", "2.4 GB free", "integrity passed"],
    actions=["Run integrity check", "Create backup", "Open migration history", "Restore a backup"],
    forms=[], states=["Healthy", "Checking", "Migration failed", "Disk full", "Corrupt", "Keychain locked", "Unsupported schema"],
    offline="This page is local. Recovery operations must not claim success without verification.",
    keyboard="Actions reachable; progress text; no raw paths exposed in this preview.",
    a11y="Health checks text; pass/fail not color-only; disk values labelled.",
    deps="OFF-001–006; BAK; local core; keychain; audit.",
    open="Idle/lock policy, support access, corruption repair procedure, migration rollback UX, path disclosure policy.",
    notes="No destructive reset is offered here; final policy is unresolved.",
    html=local_data())


add(id="SYS-004", name="Application update", slug="application-update", section="System", feature="Application Updates",
    source="22-Application-Updates.md", purpose="Show a signed update, release notes and install readiness without interrupting active clinical work or unsynced writes.",
    users="All staff may check; admin deployment policy", permissions="Install may require admin; no unsigned/silent install.",
    entry="Settings/about/updates; scheduled check notification.", navigation="Check again; install when safe; rollback details.",
    layout=["Page header", "Version card", "Release notes", "Install readiness", "Rollback card", "Policy and current install rails"],
    components=["Version summary", "Readiness checklist", "Warnings", "Actions", "Policy list"],
    data=["Current 0.1.0-preview", "New 0.2.0", "84.2 MB", "3 pending writes", "signature verified"],
    actions=["Check for updates", "Install update (blocked)", "View rollback details"],
    forms=[], states=["Checking", "Up to date", "Update available", "Downloading", "Signature invalid", "Blocked by unsynced writes", "Installing", "Failed", "Rollback available"],
    offline="Check fails gracefully; current version continues. Downloaded update waits.",
    keyboard="Install blocked state explained; actions labelled; release notes readable.",
    a11y="Status textual; checks list; no countdown auto-install.",
    deps="UPD-001–005; sync; local transaction; installer.",
    open="Update channel policy, admin install rights, signature implementation, rollback procedure, telemetry scope.",
    notes="This preview cannot install anything; the block is intentional.",
    html=updates())


add(id="SYS-005", name="Backups", slug="backups", section="System", feature="Backup and Recovery",
    source="18-Backup-and-Recovery.md", purpose="Review encrypted backup history, verification, destination and restore entry points without cloud assumptions.",
    users="Admin only", permissions="Admin only; audited export/restore.",
    entry="Sidebar system or settings backup; system health.", navigation="Create backup; restore from file; save backup settings.",
    layout=["Page header", "Four backup metrics", "Backup history", "PHI warning", "Backup settings", "Safety snapshot rail"],
    components=["Metric cards", "Table", "Settings form", "Warnings", "Status badges"],
    data=["4 verified backups", "184 MB", "external drive", "daily 03:00 IST", "14-day retention"],
    actions=["Create backup", "Restore from file", "Save backup settings"],
    forms=["Schedule", "Destination", "Retention", "Passphrase requirement", "Checksum verification", "Cloud upload (off by default)"],
    states=["No backups", "Ready", "Verifying", "Failed checksum", "Disk full", "Restore in progress", "Permission denied"],
    offline="Export/restore local. No automatic cloud upload.",
    keyboard="Table and settings accessible; destructive restore separate.",
    a11y="Backup status textual; passphrase requirement explicit; retention range help.",
    deps="BAK-001–006; OFF; audit; settings.",
    open="Approved destination policy, encryption implementation, retention enforcement and support role.",
    notes="Backups contain PHI. The preview filenames and sizes are fictional.",
    html=backups())


add(id="SYS-006", name="Create encrypted backup", slug="create-encrypted-backup", section="System", feature="Backup and Recovery",
    source="18-Backup-and-Recovery.md", purpose="Create a passphrase-protected, authenticated local backup with an explicit include/exclude boundary.",
    users="Admin only", permissions="Admin only; audited.",
    entry="Backups Create backup.", navigation="Create → backup history. Cancel → backups.",
    layout=["Page header", "Included/excluded card", "Passphrase form", "Destination", "PHI warning", "Backup preview rail", "Process rail"],
    components=["Key-values", "Password fields", "Destination picker", "Checkboxes", "Preview", "Warnings"],
    data=["184 MB estimate", "1.2 TB free", "schema v14", "no secrets"],
    actions=["Create encrypted backup", "Cancel"],
    forms=["Passphrase (required)", "Confirm passphrase", "Destination (required)", "Passphrase-loss acknowledgement"],
    states=["Ready", "Creating", "Weak passphrase", "Destination unavailable", "Disk full", "Interrupted", "Permission denied"],
    offline="Local operation; no cloud upload. Temp files must not contain plaintext PHI.",
    keyboard="Passphrase fields labelled; destination picker accessible; progress announced.",
    a11y="Passphrase guidance; include/exclude lists; no color-only errors.",
    deps="BAK-001–006; OFF; audit.",
    open="Passphrase strength policy, destination allowlist, temp-file shredding, large-backup UX.",
    notes="No real passphrase is shown. The destination is a fictional preview path.",
    html=backup_export())


add(id="SYS-007", name="Restore backup preview", slug="restore-backup-preview", section="System", feature="Backup and Recovery",
    source="18-Backup-and-Recovery.md", purpose="Preview a backup, verify compatibility and require passphrase, safety snapshot and destructive confirmation before restore.",
    users="Admin only", permissions="Admin only; audited; destructive.",
    entry="Backups Restore from file.", navigation="Create safety snapshot; restore; cancel. Failure must leave current data intact.",
    layout=["Page header", "Danger alert", "Backup manifest", "Compatibility checklist", "Confirm restore form", "What happens rail", "Current copy rail"],
    components=["Manifest key-values", "Checks list", "Passphrase and typed confirmation", "Acknowledgement", "Warnings"],
    data=["ncc-2026-10-20.nccb", "2,418 patients", "schema v14", "5 of 6 checks", "3 pending writes"],
    actions=["Create safety snapshot", "Restore local data", "Cancel"],
    forms=["Passphrase (required)", "Type RESTORE (required)", "Loss acknowledgement (required)"],
    states=["Preview", "Checks pass", "Checks fail", "Snapshotting", "Restoring", "Interrupted", "Rolled back", "Reconciliation conflict"],
    offline="Local restore; sync reconciliation happens after restore.",
    keyboard="Typed confirmation; destructive action requires explicit focus/acknowledgement; no auto-submit.",
    a11y="Destructive consequence text; checklist text; passphrase error; no color-only.",
    deps="BAK-001–006; OFF; SYNC; audit.",
    open="Account binding checks, rollback trigger, reconciliation ownership, unsynced-write preservation.",
    notes="Restore is shown as blocked until a safety snapshot exists. This prototype performs no restore.",
    html=restore_preview())


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

def appearance_content():
    themes = f'''<div class="theme-grid">
      <div class="theme-choice active"><div class="theme-swatch light"><span></span><span></span><span></span></div><div class="theme-meta"><strong>Light</strong><span>Calm, high-contrast daylight workspace</span></div><span class="radio-dot checked"></span></div>
      <div class="theme-choice"><div class="theme-swatch dark"><span></span><span></span><span></span></div><div class="theme-meta"><strong>Dark</strong><span>Reduced-luminance evening workspace</span></div><span class="radio-dot"></span></div>
    </div>'''
    density = f'''<div class="segmented" style="font-size:11px"><span class="active">Comfortable</span><span>Compact</span></div><div class="help mt-8">Comfortable is the default at 1366×768. Compact is intended for larger displays and high-volume front-desk work.</div>'''
    content = f'''{page_head("Settings · this device", "Appearance", "Personal display preferences are stored on this device and never change clinic policy.", "")}
    <div class="settings-section"><div class="settings-section-head"><div><div class="settings-section-title">Theme</div><div class="settings-section-sub">Use the same accessible tokens across light and dark.</div></div></div><div class="settings-section-body">{themes}<div class="help mt-8">Theme is a device preference; clinical status colors and focus rings stay the same in both themes.</div></div></div>
    <div class="settings-section"><div class="settings-section-head"><div><div class="settings-section-title">Density</div><div class="settings-section-sub">Adjust table and form spacing, not font size below readable minimums.</div></div></div><div class="settings-section-body">{density}</div></div>
    <div class="settings-section"><div class="settings-section-head"><div><div class="settings-section-title">Workspace defaults</div><div class="settings-section-sub">Personal landing route and table page size.</div></div></div><div class="settings-section-body"><div class="grid-4">{select_field("Landing page", "Dashboard")}{select_field("Rows per table", "8 rows")}{select_field("Sidebar", "Expanded")}{select_field("Currency display", "INR · ₹")}</div></div></div>
    <div class="settings-actions"><span class="small muted">{icon("info", 12)} Changes apply after save.</span><div class="spacer"></div><button class="btn" type="button">Reset to defaults</button><button class="btn primary" type="button">Save preferences</button></div>'''
    return content


def appearance():
    return settings_page("SET-001", "Appearance", "Calm, accessible defaults for a 1366×768 desktop workspace.", appearance_content())


def notifications_content():
    content = f'''{page_head("Settings · this device", "Notifications", "Desktop notifications use IST and hide patient names by default. Due list remains the source of truth.", btn("Send test", "secondary", "bell", size="sm") + btn("OS settings", "ghost", "settings", size="sm") + btn("Save preferences", "primary", "check", size="sm"))}
    <div class="settings-section"><div class="settings-section-head"><div><div class="settings-section-title">Desktop notifications</div><div class="settings-section-sub">Operating-system permission state must be visible.</div></div><span class="badge success">Allowed</span></div><div class="settings-section-body"><div class="stat-line" style="padding:4px 0"><span>Windows notifications</span><span class="spacer" style="flex:1"></span><span class="status-pill"><span class="status-dot"></span>Allowed in OS settings</span></div><div class="mt-12"><label class="check-row"><span class="checkbox checked">{icon("check", 10)}</span><span class="check-text">Enable vaccination due and personal reminder notifications</span></label><label class="check-row"><span class="checkbox"></span><span class="check-text">Play a sound for due reminders</span></label></div></div></div>
    <div class="settings-section"><div class="settings-section-head"><div><div class="settings-section-title">Privacy on the lock screen</div><div class="settings-section-sub">Default: no patient names in OS previews.</div></div><span class="badge brand">Privacy-safe</span></div><div class="settings-section-body"><label class="check-row"><span class="checkbox checked">{icon("check", 10)}</span><span class="check-text">Hide patient names and clinical details in notification previews</span></label><div class="help mt-4">When hidden, a notification reads “Vaccination reminder due · open clinic workspace” rather than a child's name. Showing a name is a deliberate, logged override and is not offered here.</div></div></div>
    <div class="settings-section"><div class="settings-section-head"><div><div class="settings-section-title">Quiet hours & timing</div><div class="settings-section-sub">IST boundaries; no duplicate per reminder/day.</div></div></div><div class="settings-section-body"><div class="grid-4">{field("Due reminder time", "08:00", icon_name="clock")}{field("Quiet hours start", "20:00", icon_name="moon")}{field("Quiet hours end", "08:00", icon_name="sun")}{select_field("Behavior", "Queue until quiet hours end")}</div><div class="help mt-8">Quiet hours do not move the clinical due date. A reminder due at 20:30 remains due on that IST calendar day.</div></div></div>
'''
    return content


def notifications():
    return settings_page("SET-002", "Notifications", "Privacy-safe desktop reminders with IST due semantics.", notifications_content())


def security_content():
    content = f'''{page_head("Settings · this device", "Security & sessions", "Device preferences are separate from clinic-enforced security. Sign-out is blocked while writes are pending; sync or resolve first.", btn("Lock now", "secondary", "lock", size="sm") + btn("Sign out", "ghost", "logout", size="sm"))}
    <div class="settings-section"><div class="settings-section-head"><div><div class="settings-section-title">Current session</div><div class="settings-section-sub">Supabase Auth · refresh handled by the Go core</div></div><span class="badge success">Active</span></div><div class="settings-section-body">{kv_list([("Signed in as", "Ananya Rao · Admin"), ("Device", "This desktop · Windows"), ("Expires", "12 hours · 20:40 IST")])}</div></div>
    <div class="settings-section"><div class="settings-section-head"><div><div class="settings-section-title">Idle lock</div><div class="settings-section-sub">Clinic policy controls the maximum idle interval.</div></div><span class="badge neutral">Admin policy</span></div><div class="settings-section-body"><div class="grid-3">{select_field("Lock after inactivity", "10 minutes")}{select_field("Lock behavior", "Hide PHI · keep local session")}{field("Maximum allowed", "30 minutes", help_text="Clinic policy; cannot be set higher on this device.")}</div><div class="check-row mt-8"><span class="checkbox checked">{icon("check", 10)}</span><span class="check-text">Lock immediately when the OS session is locked</span></div></div></div>
    <div class="help mt-8">{icon("shield", 12)} Local database uses SQLCipher with the key in the OS keychain; backups require a passphrase. Renderer storage has no tokens or PHI. <a href="SYS-003.html">Open local data status</a>.</div>
    <div class="settings-actions"><span class="small muted">{icon("info", 12)} Security defaults are admin-managed and audited.</span><div class="spacer"></div><button class="btn primary" type="button">Save device preferences</button></div>'''
    return content


def security():
    return settings_page("SET-003", "Security & sessions", "Clear boundaries between device preferences and clinic security policy.", security_content())


def clinic_settings_content():
    content = f'''{page_head("Settings · clinic-wide", "Clinic & safety", "Admin-only policy for clinic identity, stock thresholds, backup and update behavior. Changes are audited.", badge("Admin-only · online-only", "warning") + btn("Discard", "ghost", size="sm") + btn("Save clinic settings", "primary", "check", size="sm"))}
    <div class="settings-section"><div class="settings-section-head"><div><div class="settings-section-title">Clinic identity</div><div class="settings-section-sub">Used on receipts and reports.</div></div><span class="badge neutral">Required</span></div><div class="settings-section-body"><div class="grid-3">{field("Clinic name", "Neo Child Clinic", required=True)}{field("Phone", "+91 80 4123 7788", icon_name="phone")}{field("GSTIN", "29ABCDE1234F1Z5", help_text="Receipt policy must confirm this.")}</div><div class="mt-8">{textarea("Address", "12, 4th Cross, Indiranagar, Bengaluru 560038", width="full")}</div></div></div>
    <table class="settings-two-col"><tr><td><div class="settings-section"><div class="settings-section-head"><div><div class="settings-section-title">Stock safety defaults</div><div class="settings-section-sub">Thresholds alert only; they do not change stock.</div></div></div><div class="settings-section-body"><div class="grid-2">{field("Low-stock threshold", "10 doses", suffix="doses")}{field("Expiry warning", "30 days", suffix="days")}</div><div class="grid-2 mt-8">{select_field("FEFO behavior", "Suggest, do not force")}{select_field("Adjustment approval", "Admin only")}</div><div class="help mt-8">FEFO and adjustment approval remain design proposals, not accepted policy.</div></div></div>
      </td><td><div class="settings-section"><div class="settings-section-head"><div><div class="settings-section-title">Backup & update policy</div><div class="settings-section-sub">Installs only with no pending writes; passphrases required.</div></div></div><div class="settings-section-body"><div class="grid-2">{select_field("Backup schedule", "Daily · 03:00 IST")}{select_field("Destination", "External drive · E:")}</div><div class="grid-2 mt-8">{field("Retention", "14 days")}{select_field("Update channel", "Stable")}</div><div class="mt-8">{checkbox("Require passphrase for every manual backup", checked=True)}</div></div></div>
    </td></tr></table>
    <div class="help mt-8">{icon("lock", 12)} Online-only and audited · v0.1.0-preview · schema v14</div>'''
    return content


def clinic_settings():
    return settings_page("SET-004", "Clinic & safety", "Admin-only clinic identity, stock safety, backup and update policy.", clinic_settings_content())


add(id="SET-001", name="Appearance settings", slug="appearance-settings", section="Settings", feature="Settings",
    source="20-Settings.md", purpose="Set personal theme, density and workspace display defaults without changing clinic policy.",
    users="All staff", permissions="Device preference only; no PHI and no secrets.",
    entry="Sidebar Settings; user menu.", navigation="Notifications; security; clinic settings; save preferences.",
    layout=["Page header", "Settings secondary nav", "Theme cards", "Density control", "Workspace defaults", "Save row"],
    components=["Secondary nav", "Theme choice cards", "Segmented control", "Select fields", "Save/reset"],
    data=["Light/dark themes", "Comfortable density", "Dashboard landing", "8 rows", "INR"],
    actions=["Select theme", "Select density", "Save preferences", "Reset to defaults"],
    forms=["Theme", "Density", "Landing page", "Rows per table", "Sidebar mode", "Currency display"],
    states=["Ready", "Saving", "Invalid/corrupt preference", "Theme preview", "Permission not applicable"],
    offline="Local device preferences work offline. Corrupt values fall back to safe defaults.",
    keyboard="Theme cards and segmented control keyboard accessible; focus visible; save reachable.",
    a11y="Theme choices not color-only (labels/descriptions); density does not reduce text below minimum; contrast maintained.",
    deps="SET-001–005; design tokens; local settings.",
    open="Is system theme supported? Density policy? Locale/currency beyond INR?",
    notes="Theme is device-local and does not alter clinical semantics.",
    html=appearance(), dark_variant=True)


add(id="SET-002", name="Notification settings", slug="notification-settings", section="Settings", feature="Settings",
    source="20-Settings.md; 19-Desktop-Notifications.md", purpose="Expose OS permission, privacy-safe previews, quiet hours and clinic defaults for notifications.",
    users="All staff; admin clinic defaults", permissions="Personal preferences self-service; clinic defaults admin-only.",
    entry="Settings Notifications; permission prompt link.", navigation="Appearance; security; clinic settings; test notification.",
    layout=["Page header", "Settings nav", "Permission card", "Privacy card", "Quiet hours form", "Clinic defaults", "Save row"],
    components=["Status pill", "Toggles/checkboxes", "Time fields", "Selects", "Test action", "Admin badge"],
    data=["Permission allowed", "Hide names default", "Quiet hours 20:00–08:00", "08:00 due time"],
    actions=["Test notification", "Open OS settings", "Save preferences"],
    forms=["Enable notifications", "Sound", "Hide preview names", "Due reminder time", "Quiet hours start/end", "Behavior", "Clinic defaults"],
    states=["Permission allowed", "Denied", "Quiet hours", "Test sent", "Invalid time range", "Offline"],
    offline="Local scheduling works offline; due list is source of truth. Permission denial must be visible, not silent.",
    keyboard="Toggles and time fields keyboard accessible; test result announced.",
    a11y="Privacy default explained; permission state textual; no PHI in preview examples.",
    deps="NOT-001–005; REM; SET; OS notification bridge.",
    open="Clinic preview policy, quiet-hours override, sound defaults, notification retention.",
    notes="No SMS/WhatsApp is implied. OS preview hides names by default.",
    html=notifications())


add(id="SET-003", name="Security & sessions", slug="security-sessions", section="Settings", feature="Settings",
    source="20-Settings.md; 02-Authentication-and-Session.md", purpose="Explain session, idle-lock and local-data protections while separating device preferences from clinic policy.",
    users="All staff; admin policy", permissions="Session actions self-service; security policy admin-only; no secrets in settings.",
    entry="Settings Security & sessions.", navigation="Local data status; lock now; sign out.",
    layout=["Page header", "Settings nav", "Current session card", "Idle lock policy", "Local data protection", "Recent sessions", "Save row"],
    components=["Session key-values", "Status badges", "Policy fields", "Checklist", "Session table"],
    data=["Admin current session", "12-hour expiry", "10-minute idle lock", "SQLCipher", "2 sessions"],
    actions=["Lock now", "Sign out", "Open local data status", "Save device preferences"],
    forms=["Lock inactivity", "Lock behavior", "OS-lock behavior", "Maximum allowed (policy)"],
    states=["Active", "Expiring", "Idle/locked", "Sign-out blocked by pending writes", "Keychain locked", "Permission denied"],
    offline="Idle lock and local protection are local. Authentication/session changes may require connectivity.",
    keyboard="Lock/sign out reachable; dialogs for blocked sign-out; focus return.",
    a11y="Security states textual; no secret displayed; lock behavior explained.",
    deps="AUTH; OFF; SET; STF; audit.",
    open="Final idle-lock/offline unlock policy, clipboard policy, session revoke API, last-admin guard.",
    notes="No token or key is displayed. The mockup flags unresolved security policy rather than inventing it.",
    html=security())


add(id="SET-004", name="Clinic & safety settings", slug="clinic-safety-settings", section="Settings", feature="Settings",
    source="20-Settings.md", purpose="Let admins manage clinic identity, stock safety defaults, backup/update policy and view about/support information.",
    users="Admin only", permissions="Admin-only, enforced server-side; changes audited; no secrets.",
    entry="Settings Clinic & safety.", navigation="Appearance; notifications; security; save clinic settings.",
    layout=["Page header", "Admin warning", "Settings nav", "Clinic identity", "Stock safety defaults", "Backup/update policy", "About/support", "Save row"],
    components=["Form grids", "Selects/checkboxes", "Key-values", "Warnings", "Save/discard"],
    data=["Neo Child Clinic", "GSTIN placeholder", "10-dose threshold", "30-day expiry", "daily backup", "stable channel"],
    actions=["Save clinic settings", "Discard"],
    forms=["Clinic name/phone/GSTIN/address", "Low-stock threshold", "Expiry warning window", "FEFO behavior", "Adjustment approval", "Backup schedule/destination/retention", "Update channel/install timing", "Backup passphrase requirement"],
    states=["Ready", "Saving", "Validation", "Permission denied", "Offline disabled", "Conflict", "Audit write failure"],
    offline="Clinic-wide changes require connectivity; personal preferences remain local.",
    keyboard="Form order; save/discard labelled; errors linked.",
    a11y="Admin boundary explicit; ranges explained; no color-only warning; receipt identity fields labelled.",
    deps="SET-001–005; STF; BAK; UPD; INV; RCP; audit.",
    open="Official clinic identity, receipt legal fields, stock thresholds/FEFO policy, backup destination allowlist, update channel.",
    notes="Clinic details are fictional. The screen distinguishes policy proposals from accepted settings.",
    html=clinic_settings())
