"""Clinical screens: vaccination and consultation records."""
from __future__ import annotations

from components import (
    alert, avatar, badge, btn, checkbox, field, icon, icon_btn, kv_list,
    modal_overlay, page_head, pagination, search_input, select_field,
    shell_page, table, tabs, textarea, timeline, USER_DOCTOR, USER_NURSE,
)

SCREENS = []


def add(**kwargs):
    kwargs.setdefault("dark_variant", False)
    kwargs.setdefault("wide_variant", False)
    SCREENS.append(kwargs)


def patient_ribbon_vaccination():
    return f'''<div class="patient-ribbon"><div class="identity"><span class="avatar lg">AS</span><div><div class="identity-name" style="font-size:15px">Aarav Sharma</div><div class="identity-sub">NCC-2026-00418 · 2y 4m · Male · +91 98450 11223</div></div></div><span class="badge warning">{icon("clock", 10)} Due: Pentavalent dose 3</span><span class="spacer" style="flex:1"></span><span class="small muted">No recorded allergy alert in this preview</span></div>'''


# ---------------------------------------------------------------------------
# Vaccinations
# ---------------------------------------------------------------------------

def vaccination_list_content():
    rows = [
        ("<div class='identity'><span class='avatar'>AS</span><div class='identity-main'><div class='identity-name'>Aarav Sharma</div><div class='identity-sub'>NCC-2026-00418 · 2y 4m</div></div></div>", "20 Oct 2026<span class='sub'>09:04</span>", "Pentavalent dose 3", "AV-2409", "₹850", badge("Cash", "neutral"), "<span class='mono' style='font-size:10.5px'>Provisional</span>", badge("Pending sync", "info", "refresh"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar apricot'>DM</span><div class='identity-main'><div class='identity-name'>Diya Menon</div><div class='identity-sub'>NCC-2026-00502 · 8m</div></div></div>", "20 Oct 2026<span class='sub'>09:38</span>", "Rotavirus dose 2", "RV-2408", "₹1,200", badge("Online", "info"), "<span class='mono' style='font-size:10.5px'>NCC-R-004196</span>", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar info'>IG</span><div class='identity-main'><div class='identity-name'>Ishaan Gupta</div><div class='identity-sub'>NCC-2026-00488 · 1y 2m</div></div></div>", "19 Oct 2026<span class='sub'>15:12</span>", "PCV booster", "PCV-2411", "₹1,450", badge("Mixed", "neutral"), "<span class='mono' style='font-size:10.5px'>NCC-R-004191</span>", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar success'>SK</span><div class='identity-main'><div class='identity-name'>Sara Khan</div><div class='identity-sub'>NCC-2025-00987 · 5y 2m</div></div></div>", "18 Oct 2026<span class='sub'>11:20</span>", "MMR dose 2", "MMR-2404", "₹0", badge("Free dose", "success"), "<span class='mono' style='font-size:10.5px'>NCC-R-004182</span>", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar info'>VN</span><div class='identity-main'><div class='identity-name'>Vivaan Nair</div><div class='identity-sub'>NCC-2025-01102 · 3y 7m</div></div></div>", "16 Oct 2026<span class='sub'>10:08</span>", "Varicella dose 1", "VAR-2407", "₹1,800", badge("Cash", "neutral"), "<span class='mono' style='font-size:10.5px'>NCC-R-004163</span>", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar'>AR</span><div class='identity-main'><div class='identity-name'>Anaya Reddy</div><div class='identity-sub'>NCC-2026-00323 · 4y 1m</div></div></div>", "2 Sep 2026<span class='sub'>16:42</span>", "Tdap booster", "TD-2402", "₹950", badge("Online", "info"), "<span class='mono' style='font-size:10.5px'>NCC-R-004088</span>", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
    ]
    content = f'''{page_head("Clinical records · vaccinations", "Vaccination visits", "One atomic visit groups vaccine items, stock movements, payment and the next due reminder.", btn("Record vaccination", "primary", "syringe", href="VAC-002.html") + btn("Export", "secondary", "download"))}
    <div class="row tight" style="margin-bottom:12px">
      {metric_strip("Today", "18", "doses recorded", "syringe")}
      {metric_strip("Pending sync", "2", "visits waiting", "refresh", "info")}
      {metric_strip("Provisional receipts", "1", "server number pending", "receipt", "warning")}
      {metric_strip("Next due (7 days)", "23", "reminders queued", "bell", "neutral")}
    </div>
    <div class="row tight" style="margin-bottom:10px"><span class="chip active">{icon("list", 12)} All visits</span><span class="chip">{icon("refresh", 12)} Pending sync <span class="badge info">2</span></span><span class="chip">{icon("receipt", 12)} Provisional receipts</span><span class="chip">{icon("edit", 12)} Corrected</span><span class="spacer" style="flex:1"></span><span class="small muted">Local-first · receipt numbers from server</span></div>
    <div class="toolbar">{search_input("Search by patient, clinic ID or receipt")}<span class="spacer"></span><span class="toolbar-select">Last 30 days {icon("chevron-down", 12)}</span><span class="toolbar-select">All vaccines {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
    <div class="table-card">{table(["Patient", "Visit", "Vaccine", "Batch", "Amount", "Payment", "Receipt", "Status", ""], rows, widths=["w-name", "w-date", "", "w-date", "w-money", "w-status", "w-date", "w-status", "w-actions"])}{pagination("1–6 of 1,284 visits", ("‹","1","2","3","…","161","›"))}</div>'''
    return content


def metric_strip(label, value, foot, ic, tone=""):
    border = "var(--border)" if not tone else f"var(--{tone}-100)"
    return f'''<div class="card" style="flex:1;padding:10px 12px;display:flex;align-items:center;gap:10px"><span style="width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;background:var(--surface-3);color:var(--ink-600)">{icon(ic, 15)}</span><div><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">{label}</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700;line-height:1.1">{value} <span class="small muted" style="font-family:var(--font-body);font-weight:500">{foot}</span></div></div></div>'''


def vaccination_list():
    return shell_page("VAC-001", "Vaccinations", USER_NURSE, vaccination_list_content(), status="Syncing", status_tone="syncing", attention=6)


def vaccination_form_content():
    line_rows = [
        ("Pentavalent dose 3", "<span class='mono'>AV-2409</span> · exp 30 Jun 27 · 48", "1", "₹850", "₹850"),
        ("Rotavirus dose 2", "<span class='mono'>RV-2408</span> · exp 12 Feb 27 · 21", "1", "₹1,200", "₹1,200"),
    ]
    line_html = "".join(f'''<tr><td class="primary-cell">{v}</td><td>{batch}</td><td><span class="input" style="height:30px;width:54px;justify-content:center">{q}</span></td><td class="money">{price}</td><td class="money">{price}</td><td class="actions"><span class="btn-link danger" style="font-size:10px">Remove</span></td></tr>''' for v, batch, q, price, tot in line_rows)
    right = f'''<div class="col tight w-side">
      <div class="sticky-summary"><div class="small muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">Visit total</div><div class="total mt-4">₹2,050.00</div><div class="summary-line"><span>Vaccines (2)</span><strong>₹2,050</strong></div><div class="summary-line"><span>Discount</span><strong>₹0</strong></div><div class="summary-line total-line"><span>Amount due</span><strong>₹2,050</strong></div><div class="mt-12">{field("Cash", "₹1,500", icon_name="banknote")}{field("Online", "₹550", icon_name="credit-card")}</div><div class="summary-line total-line"><span>Balance</span><strong class="amount-positive">₹0</strong></div><div class="mt-12">{btn("Save & print", "secondary", "printer", size="sm")}</div><div class="help mt-8">{icon("shield", 12)} Stock valid · receipt number provisional until sync.</div></div>
    </div>'''
    content = f'''{page_head("Vaccinations · new visit", "Record vaccination", "One visit, one atomic local commit: stock, reminders, payment and receipt link.", btn("Cancel", "ghost", href="VAC-001.html") + btn("Save visit", "primary", "check"))}
    {patient_ribbon_vaccination()}
    <div class="row top mt-12">
      <div class="grow col">
        <div class="form-section"><div class="form-section-head">{icon("syringe", 15)}<div class="form-section-title">Vaccine items</div><span class="badge neutral">2 items</span><span class="badge success">{icon("check", 10)} Stock valid</span><span class="spacer" style="flex:1"></span><button class="btn-link" type="button">{icon("plus", 13)} Add vaccine</button></div>
          <div class="form-section-body" style="padding:0"><table class="table"><thead><tr><th style="padding-left:14px;width:190px">Vaccine</th><th style="width:200px">Batch</th><th style="width:60px">Qty</th><th style="width:90px">Unit price</th><th style="width:90px">Line total</th><th style="width:70px"></th></tr></thead><tbody>{line_html}</tbody></table></div>
          <div class="card-foot" style="display:flex;align-items:center;gap:8px"><span class="small muted">FEFO preference is visible, but the selected batch remains explicit.</span><span class="spacer" style="flex:1"></span><span class="small">Total <strong class="mono">₹2,050</strong></span></div>
        </div>
        <div class="form-section"><div class="form-section-head">{icon("calendar", 15)}<div class="form-section-title">Visit details & next reminder</div><span class="badge neutral">IST dates</span></div><div class="form-section-body"><div class="form-grid">{field("Visit date", "20 Oct 2026", required=True, icon_name="calendar")}{select_field("Given by", "Dr. Meera Nair", required=True)}{select_field("Batch selection", "AV-2409 · Pentavalent")}{field("Next due date", "20 Nov 2026", icon_name="calendar")}{checkbox("Create a vaccination reminder for this visit", checked=True)}</div></div>
      </div>
      {right}
    </div>'''
    return content


def vaccination_form():
    return shell_page("VAC-002", "Vaccinations", USER_NURSE, vaccination_form_content(), status="Online")


def vaccination_batch_dialog():
    base = vaccination_form_content()
    modal = f'''<div class="dialog wide" role="dialog" aria-modal="true" aria-labelledby="batch-title">
      <div class="dialog-head"><div class="dialog-icon">{icon("package", 18)}</div><div><div class="dialog-title" id="batch-title">Select a batch</div><div class="dialog-sub">Pentavalent · quantity 1 · visit 20 Oct 2026</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        <div class="row tight" style="margin-bottom:10px">{search_input("Search batch")}<span class="toolbar-select" style="width:130px">All locations {icon("chevron-down", 12)}</span></div>
        <div class="table-card standalone">{table(["Batch", "Expiry", "On hand", "Net rate", "Use"], [["AV-2409<span class='sub'>Received 12 Sep 2026</span>", "30 Jun 2027", "48", "₹760", badge("FEFO · selected", "brand")], ["AV-2408<span class='sub'>Received 4 Aug 2026</span>", "31 Dec 2026", "12", "₹760", badge("Use first", "warning")], ["AV-2410<span class='sub'>Received 2 Oct 2026</span>", "12 Aug 2027", "60", "₹775", badge("Available", "success")], ["AV-2312<span class='sub'>Expired · blocked</span>", "30 Sep 2026", "4", "₹755", badge("Expired", "danger", "x")]], widths=["w-name", "w-date", "w-money", "w-money", "w-status"])}</div>
        <div class="alert info mt-12">{icon("info", 15)}<div>Batch AV-2408 expires first but has only 12 doses. The ledger will reject a quantity above availability at commit.</div></div>
      </div>
      <div class="dialog-foot"><span class="small muted">Selected: AV-2409</span><div class="spacer"></div><button class="btn" type="button">Cancel</button><button class="btn primary" type="button">Use selected batch</button></div>
    </div>'''
    return modal_overlay(base, "VAC-001", "Vaccinations", USER_NURSE, modal)


def vaccination_detail_content():
    lines = f'''<div class="table-card standalone">{table(["Vaccine", "Batch", "Qty", "Unit price", "Line total"], [["Pentavalent dose 3<span class='sub'>DTwP-HepB-Hib</span>", "AV-2409<span class='sub'>exp 30 Jun 2027</span>", "1", "₹850.00", "₹850.00"], ["Rotavirus dose 2<span class='sub'>Oral</span>", "RV-2408<span class='sub'>exp 12 Feb 2027</span>", "1", "₹1,200.00", "₹1,200.00"]], widths=["w-name", "w-name", "w-money", "w-money", "w-money"])}</div>'''
    stock = f'''<div class="timeline" style="padding-left:20px"><div class="tl-item"><span class="tl-dot warning"></span><div class="tl-head"><div class="tl-title">Stock movement queued</div><div class="tl-time">09:04</div></div><div class="tl-body">-1 AV-2409 · -1 RV-2408 · linked to visit V-10942</div></div><div class="tl-item"><span class="tl-dot success"></span><div class="tl-head"><div class="tl-title">Reminder created</div><div class="tl-time">09:04</div></div><div class="tl-body">Pentavalent dose 4 · due 20 Nov 2026 · IST</div></div><div class="tl-item"><span class="tl-dot neutral"></span><div class="tl-head"><div class="tl-title">Payment recorded</div><div class="tl-time">09:05</div></div><div class="tl-body">Cash ₹1,500 · Online ₹550 · total ₹2,050</div></div><div class="tl-item"><span class="tl-dot neutral"></span><div class="tl-head"><div class="tl-title">Audit entry</div><div class="tl-time">09:05</div></div><div class="tl-body">Recorded by Nurse Ritika Sen · pending sync</div></div></div>'''
    content = f'''{page_head("Vaccination visit · V-10942", "Vaccination visit", "Aarav Sharma · 20 Oct 2026 · recorded by Nurse Ritika Sen", btn("Print receipt", "secondary", "printer", href="RCP-001.html") + btn("Correct visit", "secondary", "edit") + icon_btn("more", "More visit actions"))}
    {patient_ribbon_vaccination()}
    <div class="row top mt-12">
      <div class="grow col">
        <div class="card"><div class="card-head"><div><div class="card-title">Vaccine items</div><div class="card-sub">One logical visit · two stock movements</div></div><span class="badge info">Pending sync</span></div><div class="card-body" style="padding:0">{lines}</div><div class="card-foot" style="display:flex"><span class="small muted">Receipt: provisional</span><span style="flex:1"></span><strong class="mono">₹2,050.00</strong></div></div>
        <div class="row tight">
          <div class="card grow"><div class="card-head"><div class="card-title">Payment</div><span class="badge success">Paid</span></div><div class="card-body">{kv_list([("Total", "₹2,050.00"), ("Cash", "₹1,500.00"), ("Online", "₹550.00"), ("Balance", "₹0.00")])}</div></div>
          <div class="card grow"><div class="card-head"><div class="card-title">Next reminder</div><span class="badge warning">Due 20 Nov</span></div><div class="card-body"><div class="strong">Pentavalent · dose 4</div><div class="small muted mt-4">Created locally with this visit. Shows in the due list immediately.</div><div class="mt-8">{btn("Open reminder", "ghost sm", "bell", href="REM-001.html")}</div></div></div>
        </div>
        <div class="card"><div class="card-head"><div><div class="card-title">Commit trail</div><div class="card-sub">The local group is uploaded in dependency order</div></div></div><div class="card-body">{stock}</div></div>
      </div>
      <div class="col tight w-side">
        <div class="card"><div class="card-head"><div class="card-title">Visit details</div></div><div class="card-body" style="padding-top:8px">{kv_list([("Visit", "V-10942"), ("Date", "20 Oct 2026 · 09:04 IST"), ("Given by", "Dr. Meera Nair"), ("Recorded by", "Ritika Sen"), ("Location", "Consult room 2"), ("Receipt", "<span class='mono'>Provisional</span>")])}</div></div>
        <div class="card"><div class="card-head"><div class="card-title">Validation</div></div><div class="card-body" style="padding-top:8px"><div class="stat-line">{icon("check-circle", 13)}<span>Patient linked</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Batches valid on visit date</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Stock ledger queued</span></div><div class="stat-line">{icon("alert-circle", 13)}<span>Receipt awaits server</span></div></div></div>
        {alert("Do not edit the batch quantity directly. A correction is a linked diff that reverses and re-deducts stock exactly once.", "warning", "alert-triangle")}
      </div>
    </div>'''
    return content


def vaccination_detail():
    return shell_page("VAC-001", "Vaccination visit", USER_NURSE, vaccination_detail_content(), status="Syncing", status_tone="syncing")


def vaccination_correct_delete():
    base = vaccination_detail_content()
    modal = f'''<div class="dialog wide" role="dialog" aria-modal="true" aria-labelledby="correct-title">
      <div class="dialog-head"><div class="dialog-icon warning">{icon("edit", 18)}</div><div><div class="dialog-title" id="correct-title">Correct or delete this visit?</div><div class="dialog-sub">V-10942 · Aarav Sharma · 20 Oct 2026</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        {alert("A correction is a linked diff and reverses stock exactly once. A deletion is audited and must not orphan the payment or reminder.", "warning", "alert-triangle")}
        <div class="grid-2 mt-12">
          <div class="card" style="border-color:var(--brand-200);background:var(--brand-50)"><div class="card-body"><div class="strong">Correct the visit</div><div class="small muted mt-4">Change a vaccine, batch, quantity, amount or note. The original is preserved in audit.</div><div class="mt-8">{badge("Recommended", "brand")} {badge("Admin / doctor", "outline")}</div></div></div>
          <div class="card"><div class="card-body"><div class="strong">Delete and reverse</div><div class="small muted mt-4">Reverse stock and payment, cancel the reminder, and keep the audit entry. Receipt status is checked first.</div><div class="mt-8">{badge("High risk", "danger")} {badge("Admin / doctor", "outline")}</div></div></div>
        </div>
        <div class="field mt-12"><label>Reason <span class="req">*</span></label><div class="textarea"><span class="placeholder">e.g. Wrong batch selected; vaccine not administered</span></div></div>
        <div class="field mt-12"><label>What needs to change?</label><div class="select"><span>Select a correction type</span>{icon("chevron-down", 14)}</div></div>
      </div>
      <div class="dialog-foot"><button class="btn ghost" type="button">Cancel</button><div class="spacer"></div><button class="btn danger-ghost" type="button">Delete with reversal</button><button class="btn primary" type="button">Continue to correction</button></div>
    </div>'''
    return modal_overlay(base, "VAC-001", "Vaccination visit", USER_DOCTOR, modal)


add(id="VAC-001", name="Vaccination visits", slug="vaccination-visits", section="Vaccinations", feature="Vaccination Management",
    source="05-Vaccination-Management.md", purpose="Review vaccination visits, payment state, batch usage, receipt status and pending local commits.",
    users="Admin, doctor, nurse; inventory manager may view stock only", permissions="Recording proposed for admin/doctor/nurse; deletion/correction requires admin/doctor confirmation.",
    entry="Sidebar Vaccinations; patient profile; dashboard due list.", navigation="Open visit; record vaccination; filter pending/corrected; print receipt.",
    layout=["Page header", "Summary strip", "Saved status filters", "Search/filter toolbar", "Visit table", "Pagination"],
    components=["Summary cards", "Search", "Status chips", "Table", "Receipt status", "Pagination"],
    data=["18 doses today", "2 pending visits", "1 provisional receipt", "Fictional patients and amounts"],
    actions=["Record vaccination", "Export", "Open visit", "Filter"],
    forms=["Search", "Date range", "Vaccine filter"],
    states=["Loading", "Empty", "Ready", "Pending sync", "Provisional receipt", "Corrected/audit state", "Offline"],
    offline="Local visits remain visible; pending and provisional badges are explicit; no silent receipt numbering.",
    keyboard="/ focuses search; results are keyboard navigable; row actions named with patient/visit.",
    a11y="Receipt and sync status have text; money uses tabular numerals; table headers scoped.",
    deps="VAC-001–007; INV; REM; FIN; RCP; sync.",
    open="Correction vs reversal semantics and who may delete after a receipt are unresolved.",
    notes="The list does not compute receipt numbers. A provisional receipt is deliberately marked.",
    html=vaccination_list())

add(id="VAC-002", name="Record vaccination", slug="record-vaccination", section="Vaccinations", feature="Vaccination Management",
    source="05-Vaccination-Management.md", purpose="Record a vaccination visit as one atomic local transaction with vaccine items, stock, reminder, payment and receipt link.",
    users="Admin, doctor, nurse (proposed)", permissions="Inventory manager may view but not record unless approved.",
    entry="Vaccination list; patient profile; dashboard; patient due list.", navigation="Save → visit detail. Save & print → provisional receipt. Cancel → prior screen.",
    layout=["Page header", "Patient identity ribbon", "Vaccine items table", "Visit details and reminder", "Visit note", "Sticky totals and stock rail"],
    components=["Line-item table", "Batch subtext", "Payment inputs", "Reminder controls", "Validation rail", "Atomic-save actions"],
    data=["Fictional patient Aarav Sharma", "Pentavalent AV-2409 and Rotavirus RV-2408", "₹2,050 total", "Cash/online split"],
    actions=["Add vaccine", "Remove line", "Save visit", "Save & print", "Cancel"],
    forms=["Visit date (required)", "Given by", "Vaccine item (required)", "Batch (required, not expired)", "Quantity (1+, ≤ available)", "Price (non-negative)", "Cash + online = total", "Reminder type/date"],
    states=["Ready", "Saving/local commit", "Insufficient stock", "Expired batch", "Payment mismatch", "Offline/provisional receipt", "Partial group failure"],
    offline="Fully local commit; group uploads in dependency order; receipt remains provisional until the server assigns it.",
    keyboard="Logical form order; add/remove line actions keyboard accessible; Ctrl/Cmd+Enter saves in implementation.",
    a11y="Line table has headers; stock warnings in text; totals associated with payment fields; errors linked to inputs.",
    deps="VAC-001–007; inventory ledger; reminders; finance; receipts; local transaction.",
    open="FEFO mandatory vs default, correction semantics, mixed visit scope and deletion permissions remain open.",
    notes="No receipt number is computed in the renderer. Stock quantity is never edited directly.",
    html=vaccination_form())

add(id="VAC-003", name="Batch selection", slug="batch-selection", section="Vaccinations", feature="Vaccination Management",
    source="05-Vaccination-Management.md", purpose="Choose an explicit, valid batch and make expiry and availability visible before commit.",
    users="Admin, doctor, nurse", permissions="Record vaccination; inventory visibility per role.",
    entry="Record vaccination batch selector.", navigation="Use selected batch → form. Cancel → form unchanged.",
    layout=["Form context behind scrim", "Wide batch dialog", "Search/filter", "Batch comparison table", "FEFO note"],
    components=["Batch table", "Expiry", "On-hand", "Net rate", "Status badges", "Selection acknowledgement"],
    data=["AV-2409 (48)", "AV-2408 (12, expiring first)", "AV-2410 (60)", "Expired AV-2312 blocked"],
    actions=["Use selected batch", "Cancel", "Search batch"],
    forms=["Batch selection (required)"],
    states=["Ready", "Selected", "Expired disabled", "Insufficient stock", "Batch changed since load"],
    offline="Uses local stock; selection is revalidated at commit because another device may consume the last dose.",
    keyboard="Table rows selectable with keyboard; Enter confirms; Escape closes.",
    a11y="Expiry and stock numbers are text; expired rows not color-only; selection announced.",
    deps="VAC-004; inventory batches; FEFO policy.",
    open="Whether FEFO is mandatory or only a default is unresolved.",
    notes="The dialog makes FEFO visible but not silent. Manual selection remains explicit.",
    html=vaccination_batch_dialog())

add(id="VAC-004", name="Vaccination visit detail", slug="vaccination-visit-detail", section="Vaccinations", feature="Vaccination Management",
    source="05-Vaccination-Management.md", purpose="Show the atomic visit, its stock and reminder effects, payment, receipt status and audit trail.",
    users="Admin, doctor, nurse", permissions="Read role-scoped; correction/deletion role-gated.",
    entry="Vaccination list; patient timeline.", navigation="Print receipt; correct; return to list; open reminder.",
    layout=["Page header", "Patient ribbon", "Vaccine items", "Payment and reminder cards", "Commit trail", "Details/validation rail"],
    components=["Line table", "Status badges", "Key-value details", "Timeline", "Correct/delete actions"],
    data=["Visit V-10942", "₹2,050 paid", "Two stock movements", "Provisional receipt"],
    actions=["Print receipt", "Correct visit", "Delete/correct", "Open reminder"],
    forms=[],
    states=["Ready", "Pending sync", "Receipt conflict", "Partial group failure", "Corrected", "Deleted/reversed"],
    offline="Local commit visible; provisional receipt; conflict must block blind retry.",
    keyboard="All actions reachable; destructive action requires confirmation.",
    a11y="Audit trail ordered; monetary values have labels; status not color-only.",
    deps="VAC-005/006/007; inventory; finance; receipts; audit.",
    open="Receipt reprint after correction and block scope are unresolved.",
    notes="The page does not imply that the server receipt number already exists.",
    html=vaccination_detail())

add(id="VAC-005", name="Correct or delete vaccination", slug="correct-delete-vaccination", section="Vaccinations", feature="Vaccination Management",
    source="05-Vaccination-Management.md", purpose="Offer a safe correction diff or an audited delete with stock/payment reversal.",
    users="Admin, doctor (confirmation)", permissions="Admin/doctor confirmation; nurse may request correction but not delete.",
    entry="Vaccination detail Correct visit or more menu.", navigation="Continue to correction → editable diff. Delete with reversal → confirmation and audit.",
    layout=["Visit detail behind scrim", "Wide decision dialog", "Two consequence cards", "Reason field", "Correction type"],
    components=["Decision dialog", "Warning", "Risk badges", "Reason textarea", "Correction type"],
    data=["Fictional visit", "Stock and receipt implications"],
    actions=["Continue to correction", "Delete with reversal", "Cancel"],
    forms=["Reason (required)", "Correction type"],
    states=["Ready", "Receipt exists", "Payment already reconciled", "Conflict", "Permission denied"],
    offline="Correction can be local; deletion may be blocked by sync policy. Policy is unresolved.",
    keyboard="Focus trap; destructive action clearly separated; Escape cancel.",
    a11y="Consequences in text; destructive button labelled with action, not color alone.",
    deps="VAC-004; AUD; stock ledger; finance.",
    open="Who may delete after a receipt, and whether corrections are edits or linked reversal events?",
    notes="This screen intentionally does not perform deletion directly; it opens a reviewed path.",
    html=vaccination_correct_delete())


# ---------------------------------------------------------------------------
# Consultations
# ---------------------------------------------------------------------------

def consultation_list_content():
    rows = [
        ("<div class='identity'><span class='avatar'>AS</span><div class='identity-main'><div class='identity-name'>Aarav Sharma</div><div class='identity-sub'>NCC-2026-00418 · 2y 4m</div></div></div>", "20 Oct 2026<span class='sub'>10:32</span>", "Dr. Meera Nair", "Mild viral fever", "27 Oct 2026", "₹500", badge("Paid", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar apricot'>DM</span><div class='identity-main'><div class='identity-name'>Diya Menon</div><div class='identity-sub'>NCC-2026-00502 · 8m</div></div></div>", "18 Oct 2026<span class='sub'>11:20</span>", "Dr. Nikhil Verma", "Feeding review", "—", "₹500", badge("Paid", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar success'>SK</span><div class='identity-main'><div class='identity-name'>Sara Khan</div><div class='identity-sub'>NCC-2025-00987 · 5y 2m</div></div></div>", "16 Oct 2026<span class='sub'>16:42</span>", "Dr. Meera Nair", "Ear pain", "—", "₹500", badge("Paid", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar info'>VN</span><div class='identity-main'><div class='identity-name'>Vivaan Nair</div><div class='identity-sub'>NCC-2025-01102 · 3y 7m</div></div></div>", "12 Oct 2026<span class='sub'>09:50</span>", "Dr. Nikhil Verma", "Skin rash", "19 Oct 2026", "₹500", badge("Pending sync", "info", "refresh"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("<div class='identity'><span class='avatar apricot'>AR</span><div class='identity-main'><div class='identity-name'>Anaya Reddy</div><div class='identity-sub'>NCC-2026-00323 · 4y 1m</div></div></div>", "2 Sep 2026<span class='sub'>16:40</span>", "Dr. Meera Nair", "Seasonal allergy", "—", "₹500", badge("Paid", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
    ]
    content = f'''{page_head("Clinical records · consultations", "Consultations", "Doctor notes, follow-up dates and linked payments without orphaned visits.", btn("New consultation", "primary", "stethoscope", href="CON-002.html") + btn("Export", "secondary", "download"))}
    <div class="row tight" style="margin-bottom:12px">{metric_strip("Today", "6", "consultations", "stethoscope")}{metric_strip("Follow-ups (7 days)", "9", "scheduled", "calendar", "info")}{metric_strip("Pending sync", "1", "note waiting", "refresh", "warning")}{metric_strip("Notes hidden", "0", "role-scoped", "lock", "neutral")}</div>
    <div class="toolbar">{search_input("Search by patient, doctor or problem")}<span class="spacer"></span><span class="toolbar-select">All doctors {icon("chevron-down", 12)}</span><span class="toolbar-select">Last 30 days {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
    <div class="table-card">{table(["Patient", "Date", "Doctor", "Problem / note", "Follow-up", "Amount", "Payment", ""], rows, widths=["w-name", "w-date", "", "", "w-date", "w-money", "w-status", "w-actions"])}{pagination("1–7 of 428 consultations", ("‹","1","2","3","…","62","›"))}</div>
    <div class="alert info mt-12">{icon("lock", 15)}<div><strong>Clinical notes are role-scoped.</strong> Reception can schedule a visit but cannot open consultation notes. Financial columns require finance permission.</div></div>'''
    return content


def consultation_list():
    return shell_page("CON-001", "Consultations", USER_DOCTOR, consultation_list_content(), status="Online")


def consultation_form_content():
    right = f'''<div class="col tight w-side">
      <div class="card"><div class="card-head"><div class="card-title">Patient context</div></div><div class="card-body" style="padding-top:8px"><div class="identity"><span class="avatar">AS</span><div><div class="identity-name">Aarav Sharma</div><div class="identity-sub">2y 4m · NCC-2026-00418</div></div></div><div class="mt-12">{kv_list([("Last visit", "12 Aug 2026"), ("Recent problem", "Mild viral fever"), ("Next vaccination", "Today · Pentavalent dose 3"), ("Balance", "₹0")])}</div></div></div>
      <div class="card"><div class="card-head"><div class="card-title">Linked visit</div><span class="badge brand">V-10943</span></div><div class="card-body"><div class="small muted">The consultation belongs to this visit. Changing payment reconciles to the same identity.</div><div class="stat-line mt-8">{icon("check-circle", 13)}<span>Patient linked</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Doctor assigned</span></div><div class="stat-line">{icon("alert-circle", 13)}<span>Payment not yet saved</span></div><div class="help mt-8">{icon("shield", 12)} Sync conflicts preserve both versions for review; notes are never silently overwritten.</div></div></div>
    </div>'''
    content = f'''{page_head("Consultations · new", "New consultation", "Capture the clinical note and payment against one visit; follow-up appears on the patient timeline.", btn("Cancel", "ghost", href="CON-001.html") + btn("Save consultation", "primary", "check"))}
    <div class="patient-ribbon"><div class="identity"><span class="avatar lg">AS</span><div><div class="identity-name" style="font-size:15px">Aarav Sharma</div><div class="identity-sub">NCC-2026-00418 · 2y 4m · Male · +91 98450 11223</div></div></div><span class="badge warning">{icon("clock", 10)} Visit today · 10:32</span><span class="spacer" style="flex:1"></span><span class="small muted">Dr. Meera Nair</span></div>
    <div class="row top mt-12">
      <div class="grow col">
        <div class="form-section"><div class="form-section-head">{icon("stethoscope", 15)}<div class="form-section-title">Consultation</div><span class="badge neutral">IST</span></div><div class="form-section-body">
          <table class="form-table"><colgroup><col style="width:50%"><col style="width:50%"></colgroup><tbody>
            <tr><td>{field("Date & time", "20 Oct 2026 · 10:32", required=True, icon_name="calendar-clock")}</td><td>{select_field("Doctor", "Dr. Meera Nair", required=True)}</td></tr>
            <tr><td colspan="2">{field("Problem / reason", "Mild viral fever", required=True)}</td></tr>
            <tr><td colspan="2">{textarea("Clinical notes", "Fever since yesterday evening, maximum 100.4°F. Feeding and urine output adequate. No breathing difficulty. Advised fluids and paracetamol as needed; return if fever persists beyond 48 hours.")}</td></tr>
            <tr><td>{field("Follow-up date", "27 Oct 2026", icon_name="calendar")}</td><td>{select_field("Follow-up type", "In person")}</td></tr>
          </tbody></table>
          <div class="summary-line mt-8"><span>Payment</span><strong>₹500 · Paid · Cash</strong></div>
        </div></div>
      </div>
      {right}
    </div>'''
    return content


def consultation_form():
    return shell_page("CON-001", "Consultations", USER_DOCTOR, consultation_form_content(), status="Online")


def consultation_detail_content():
    content = f'''{page_head("Consultation · C-2084", "Consultation detail", "Aarav Sharma · 20 Oct 2026 · Dr. Meera Nair", btn("Edit consultation", "secondary", "edit") + btn("Print receipt", "secondary", "printer", href="RCP-001.html") + icon_btn("more", "More consultation actions"))}
    <div class="patient-ribbon"><div class="identity"><span class="avatar lg">AS</span><div><div class="identity-name" style="font-size:15px">Aarav Sharma</div><div class="identity-sub">NCC-2026-00418 · 2y 4m · linked visit V-10943</div></div></div><span class="badge success">Paid</span><span class="badge success">Synced</span><span class="spacer" style="flex:1"></span><span class="small muted">Updated 20 Oct 2026 · 10:36</span></div>
    <div class="row top mt-12">
      <div class="grow col">
        <div class="card"><div class="card-head"><div><div class="card-title">Clinical note</div><div class="card-sub">Role-scoped · visible to doctor and admin</div></div><span class="badge warning">Follow-up 27 Oct</span></div><div class="card-body"><div class="strong">Mild viral fever</div><p class="muted mt-8" style="font-size:12px;line-height:1.65">Fever since yesterday evening, maximum 100.4°F. Feeding and urine output adequate. No breathing difficulty. Advised fluids and paracetamol as needed; return if fever persists beyond 48 hours.</p><div class="divider"></div><div class="row tight"><div><div class="tiny muted">DOCTOR</div><div class="strong">Dr. Meera Nair</div></div><div><div class="tiny muted">CONSULTATION TIME</div><div class="strong">20 Oct 2026 · 10:32 IST</div></div><div><div class="tiny muted">FOLLOW-UP</div><div class="strong">27 Oct 2026</div></div></div></div></div>
        <div class="row tight">
          <div class="card grow"><div class="card-head"><div class="card-title">Payment</div><span class="badge success">Paid</span></div><div class="card-body">{kv_list([("Consultation fee", "₹500.00"), ("Cash", "₹500.00"), ("Online", "₹0.00"), ("Receipt", "NCC-R-004197")])}</div></div>
          <div class="card grow"><div class="card-head"><div class="card-title">Follow-up</div><span class="badge info">In 7 days</span></div><div class="card-body"><div class="strong">27 Oct 2026 · In person</div><div class="small muted mt-4">Added to the patient timeline and follow-up list.</div><div class="mt-8">{btn("Add to personal reminders", "ghost sm", "bell")}</div></div></div>
        </div>
      </div>
      <div class="col tight w-side">
        <div class="card"><div class="card-head"><div class="card-title">Audit</div></div><div class="card-body">{timeline([{"title":"Consultation created","time":"10:36","body":"Dr. Meera Nair · local commit","tone":"success"},{"title":"Payment linked","time":"10:36","body":"₹500 · receipt NCC-R-004197","tone":"neutral"},{"title":"Synced","time":"10:38","body":"Server acknowledged visit group","tone":"success"}])}</div></div>
        <div class="card"><div class="card-head"><div class="card-title">Record actions</div></div><div class="card-body" style="display:flex;flex-direction:column;gap:6px">{btn("Edit note", "secondary", "edit", size="sm")} {btn("Add addendum", "ghost", "message", size="sm")} {btn("Delete / cancel", "ghost", "trash", size="sm")}</div></div>
        <div class="alert warning">{icon("alert-triangle", 15)}<div><strong>Deleting this consultation</strong> leaves the visit and payment intact. A reason and audit entry are required.</div></div>
      </div>
    </div>'''
    return content


def consultation_detail():
    return shell_page("CON-001", "Consultation detail", USER_DOCTOR, consultation_detail_content(), status="Online")


def consultation_delete_dialog():
    base = consultation_detail_content()
    modal = f'''<div class="dialog narrow" role="dialog" aria-modal="true" aria-labelledby="delete-consult-title">
      <div class="dialog-head"><div class="dialog-icon danger">{icon("trash", 18)}</div><div><div class="dialog-title" id="delete-consult-title">Delete this consultation?</div><div class="dialog-sub">C-2084 · linked visit V-10943 · receipt exists</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        {alert("The visit and its payment will remain. The receipt is not deleted or renumbered. This action is audited.", "warning", "alert-triangle")}
        <div class="mt-12">{kv_list([("Consultation", "C-2084 · Mild viral fever"), ("Doctor", "Dr. Meera Nair"), ("Payment", "₹500 · Paid"), ("Receipt", "NCC-R-004197")])}</div>
        <div class="field mt-12"><label>Reason for deletion <span class="req">*</span></label><div class="textarea"><span class="placeholder">e.g. Created against the wrong visit</span></div></div>
        <div class="check-row mt-8"><span class="checkbox"></span><span class="check-text">I understand the audit trail and the payment will remain.</span></div>
      </div>
      <div class="dialog-foot"><button class="btn ghost" type="button">Cancel</button><div class="spacer"></div><button class="btn danger" type="button">Delete consultation</button></div>
    </div>'''
    return modal_overlay(base, "CON-001", "Consultation detail", USER_DOCTOR, modal)


add(id="CON-001", name="Consultations", slug="consultations", section="Consultations", feature="Consultation Management",
    source="06-Consultation-Management.md", purpose="Review consultations, linked payments, follow-ups and pending notes without exposing notes to non-clinical roles.",
    users="Admin, doctor; reception may schedule but not write clinical notes", permissions="Clinical notes admin/doctor; payment columns finance-permitted roles.",
    entry="Sidebar Consultations; patient profile; dashboard.", navigation="New consultation; open detail; filter by doctor/date; export.",
    layout=["Page header", "Summary strip", "Search/filter toolbar", "Consultation table", "Role-scope note"],
    components=["Summary cards", "Table", "Status badges", "Search", "Filters"],
    data=["6 consultations today", "9 follow-ups in 7 days", "1 pending note", "Fictional patients and amounts"],
    actions=["New consultation", "Export", "Open consultation"],
    forms=["Search", "Doctor filter", "Date range"],
    states=["Loading", "Empty", "Ready", "Pending sync", "Permission denied", "Offline"],
    offline="Local reads; pending note badge; clinical notes remain local until sync.",
    keyboard="/ focuses search; table rows and actions keyboard accessible.",
    a11y="Role-scoped columns explained; statuses textual; clinical note column not shown to unauthorized roles.",
    deps="CON-001–005; patients; finance; receipts.",
    open="Can receptionists create a consultation shell? Addenda vs edits? One consultation per visit?",
    notes="Clinical notes are deliberately absent from the list preview beyond the problem label.",
    html=consultation_list())

add(id="CON-002", name="New consultation", slug="new-consultation", section="Consultations", feature="Consultation Management",
    source="06-Consultation-Management.md", purpose="Capture a doctor consultation linked to a patient, visit, doctor, date, follow-up and payment.",
    users="Admin, doctor", permissions="Receptionist may schedule but must not write clinical notes.",
    entry="Consultation list; patient profile; dashboard.", navigation="Save → consultation detail. Cancel → prior screen.",
    layout=["Page header", "Patient ribbon", "Consultation form", "Payment section", "Patient context rail", "Linked visit rail"],
    components=["Clinical text fields", "Follow-up date", "Payment split", "Role warnings"],
    data=["Fictional Aarav Sharma", "Mild viral fever", "₹500 paid", "Follow-up 27 Oct"],
    actions=["Save consultation", "Cancel"],
    forms=["Patient (via context)", "Doctor (required)", "Date/time (required)", "Problem (required)", "Clinical notes", "Follow-up date", "Fee", "Cash + online = total", "Payment reconciliation acknowledgement"],
    states=["Ready", "Saving", "Validation error", "Missing visit", "Payment mismatch", "Offline", "Conflict"],
    offline="Local commit and outbox; conflict preserves both versions rather than overwriting notes.",
    keyboard="Form order; date controls keyboard accessible; save shortcut documented in implementation.",
    a11y="Labels visible; error text linked; note length bounded; no PHI in placeholders.",
    deps="CON-003–005; patients; finance; receipts; audit.",
    open="Payment categories, addenda policy and one-consultation-per-visit rule are unresolved.",
    notes="The note shown is fictional clinical content for layout testing only.",
    html=consultation_form())

add(id="CON-003", name="Consultation detail", slug="consultation-detail", section="Consultations", feature="Consultation Management",
    source="06-Consultation-Management.md", purpose="Read the consultation, its payment and follow-up, and review the audit trail.",
    users="Admin, doctor", permissions="Clinical notes role-scoped; delete requires confirmation and audit.",
    entry="Consultation list; patient timeline.", navigation="Edit; print receipt; add addendum; delete/cancel; open patient.",
    layout=["Page header", "Patient ribbon", "Clinical note card", "Payment and follow-up cards", "Audit rail", "Delete warning"],
    components=["Clinical note", "Key-value blocks", "Audit timeline", "Action list"],
    data=["C-2084", "Mild viral fever note", "₹500 paid", "Receipt NCC-R-004197", "Follow-up 27 Oct"],
    actions=["Edit", "Print receipt", "Add addendum", "Delete/cancel"],
    forms=[],
    states=["Ready", "Pending sync", "Conflict", "Corrected", "Deleted/cancelled", "Permission denied"],
    offline="Local read; pending state visible; receipt state explicit.",
    keyboard="Actions reachable in logical order; delete opens confirmation.",
    a11y="Note heading; payment labels; audit ordered; no color-only follow-up status.",
    deps="CON-002/004; RCP; audit; finance.",
    open="Addendum behavior and deletion with receipt are unresolved.",
    notes="Deletion does not delete the visit or payment; this is stated in the UI.",
    html=consultation_detail())

add(id="CON-004", name="Delete consultation", slug="delete-consultation", section="Consultations", feature="Consultation Management",
    source="06-Consultation-Management.md", purpose="Delete or cancel a consultation with a reason while preserving the linked visit, payment and audit.",
    users="Admin, doctor (confirmation)", permissions="Deletion requires confirmation and audit.",
    entry="Consultation detail Delete / cancel.", navigation="Delete → detail/list with audit. Cancel → detail.",
    layout=["Detail context behind scrim", "Narrow destructive dialog", "Linked payment warning", "Reason", "Confirmation"],
    components=["Destructive dialog", "Context summary", "Reason field", "Required acknowledgement"],
    data=["C-2084", "₹500 paid", "Receipt NCC-R-004197"],
    actions=["Delete consultation", "Cancel"],
    forms=["Reason (required)", "Acknowledgement (required)"],
    states=["Ready", "Validation error", "Deleting", "Conflict", "Permission denied"],
    offline="Delete is audit-required; offline policy for deletion is unresolved at the sync boundary.",
    keyboard="Focus trapped; Escape cancels; delete requires explicit acknowledgement.",
    a11y="Destructive action clearly labelled; consequence text; no timeout.",
    deps="CON-003; AUD; finance; receipts; sync deletion contract.",
    open="What happens to a receipt when a consultation is deleted? Is cancellation distinct from deletion?",
    notes="This mockup preserves the visit and payment; that is proposed, not implemented.",
    html=consultation_delete_dialog())