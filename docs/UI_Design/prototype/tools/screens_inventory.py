"""Inventory, wastage and borrow/return screens."""
from __future__ import annotations

from components import (
    alert, avatar, badge, btn, checkbox, drawer_overlay, field, icon, icon_btn, kv_list,
    mini_bars, modal_overlay, page_head, pagination, search_input, select_field,
    shell_page, table, tabs, textarea, timeline, USER_ADMIN, USER_INVENTORY,
    USER_NURSE,
)

SCREENS = []


def add(**kwargs):
    kwargs.setdefault("dark_variant", False)
    kwargs.setdefault("wide_variant", False)
    SCREENS.append(kwargs)


def strip(label, value, foot, ic, tone="neutral"):
    return f'''<div class="card" style="flex:1;padding:10px 12px;display:flex;align-items:center;gap:10px"><span style="width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;background:var(--surface-3);color:var(--ink-600)">{icon(ic, 15)}</span><div><div class="tiny muted" style="font-weight:700;text-transform:uppercase;letter-spacing:.4px">{label}</div><div style="font-family:var(--font-display);font-size:19px;font-weight:700;line-height:1.1">{value} <span class="small muted" style="font-family:var(--font-body);font-weight:500">{foot}</span></div></div></div>'''


# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------

def inventory_overview_content():
    rows = [
        ("<div class='identity'><span class='avatar' style='border-radius:8px'>P</span><div class='identity-main'><div class='identity-name'>Pentavalent</div><div class='identity-sub'>DTwP-HepB-Hib · 3 brands</div></div></div>", "7 batches", "126", "30 Jun 2027", "₹95,760", badge("Healthy", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("<div class='identity'><span class='avatar info' style='border-radius:8px'>PC</span><div class='identity-main'><div class='identity-name'>PCV</div><div class='identity-sub'>Pneumococcal conjugate · 2 brands</div></div></div>", "4 batches", "86", "12 Nov 2026", "₹1,24,700", badge("Expiring soon", "warning"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("<div class='identity'><span class='avatar apricot' style='border-radius:8px'>R</span><div class='identity-main'><div class='identity-name'>Rotavirus</div><div class='identity-sub'>Oral · 3 brands</div></div></div>", "3 batches", "21", "12 Feb 2027", "₹25,200", badge("Low stock", "warning"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("<div class='identity'><span class='avatar' style='border-radius:8px'>V</span><div class='identity-main'><div class='identity-name'>Varicella</div><div class='identity-sub'>Live attenuated</div></div></div>", "2 batches", "18", "18 Aug 2027", "₹32,400", badge("Healthy", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("<div class='identity'><span class='avatar info' style='border-radius:8px'>H</span><div class='identity-main'><div class='identity-name'>Hepatitis B</div><div class='identity-sub'>Adult and paediatric</div></div></div>", "3 batches", "74", "22 Jan 2027", "₹29,600", badge("Healthy", "success"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
        ("<div class='identity'><span class='avatar warning' style='border-radius:8px;background:var(--warning-100);color:var(--warning-700)'>I</span><div class='identity-main'><div class='identity-name'>Influenza</div><div class='identity-sub'>Annual · 2 brands</div></div></div>", "1 batch", "6", "31 Oct 2026", "₹6,600", badge("Low + expiring", "danger"), f"<span class='row-action'>{icon('chevron-right', 15)}</span>"),
    ]
    content = f'''{page_head("Inventory · stock control", "Inventory", "Batch-level stock with expiry, low-stock thresholds and a single auditable ledger.", btn("Receive stock", "primary", "package", href="INV-005.html") + btn("Stock adjustment", "secondary", "sliders", href="INV-006.html"))}
    <div class="row tight" style="margin-bottom:12px">{strip("Stock value", "₹4.28L", "at net rate", "wallet")}{strip("Low stock", "3", "vaccines below threshold", "alert-triangle")}{strip("Expiring ≤ 30 days", "2", "batches", "calendar", "warning")}{strip("Pending movements", "1", "awaiting sync", "refresh", "info")}</div>
    <div style="margin-bottom:10px">{tabs([("By vaccine", None), ("By batch", "23"), ("Ledger", None), ("Expired", "2")], 0, extra=f'<span class="spacer" style="flex:1"></span>{btn("Export stock", "ghost sm", "download")}')}</div>
    <div class="toolbar">{search_input("Search vaccine, brand or batch")}<span class="spacer"></span><span class="toolbar-select">All storage locations {icon("chevron-down", 12)}</span><span class="toolbar-select">Health: all {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
    <div class="table-card">{table(["Vaccine", "Batches", "On hand", "Nearest expiry", "Stock value", "Status", ""], rows, widths=["w-name", "w-date", "w-money", "w-date", "w-money", "w-status", "w-actions"])}{pagination("6 of 7 vaccine groups · 23 batches", ("‹","1","›"))}</div>
    <div class="help mt-8">{icon("alert-triangle", 12)} PCV-2411 expires in 12 days; 34 doses remain and FEFO should be used before newer PCV batches.</div>'''
    return content


def inventory_overview():
    return shell_page("INV-001", "Inventory", USER_INVENTORY, inventory_overview_content(), attention=6)


def catalog_content():
    rows = [
        ("Pentavalent", "<div class='strong'>Pentavac SD</div><div class='sub'>Serum Institute of India</div>", "DTwP-HepB-Hib", "Vaccine", "₹850", "₹760", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("Pentavalent", "<div class='strong'>Easyfive-TT</div><div class='sub'>Panacea Biotec</div>", "DTwP-HepB-Hib", "Vaccine", "₹820", "₹735", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("PCV", "<div class='strong'>Prevenar 13</div><div class='sub'>Pfizer</div>", "Pneumococcal conjugate", "Vaccine", "₹4,200", "₹3,850", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("Rotavirus", "<div class='strong'>Rotavac</div><div class='sub'>Bharat Biotech</div>", "Oral rotavirus", "Vaccine", "₹1,200", "₹1,050", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("MMR", "<div class='strong'>MMR II</div><div class='sub'>Merck</div>", "Measles, mumps, rubella", "Vaccine", "₹950", "₹840", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("Varicella", "<div class='strong'>Varilrix</div><div class='sub'>GlaxoSmithKline</div>", "Live attenuated", "Vaccine", "₹1,800", "₹1,620", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("Influenza", "<div class='strong'>Influvac Tetra</div><div class='sub'>Abbott</div>", "Seasonal influenza", "Vaccine", "₹1,100", "₹980", badge("Low stock", "warning"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("Hepatitis B", "<div class='strong'>Engerix-B</div><div class='sub'>GlaxoSmithKline</div>", "Hepatitis B", "Vaccine", "₹400", "₹340", badge("Active", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
    ]
    content = f'''{page_head("Inventory · catalogue", "Vaccine catalogue", "Brand, manufacturer, dose schedule, storage and pricing used by clinical and stock workflows.", btn("Add vaccine", "primary", "plus", href="INV-003.html") + btn("Import catalogue", "secondary", "upload"))}
    <div class="toolbar">{search_input("Search brand, type or manufacturer")}<span class="spacer"></span><span class="result-count">8 active catalogue items</span><span class="toolbar-select">All categories {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
    <div class="table-card">{table(["Type", "Brand / manufacturer", "Category", "Dose schedule", "MRP", "Net rate", "Status", ""], rows, widths=["w-date", "w-name", "", "", "w-money", "w-money", "w-status", "w-actions"])}{pagination("1–8 of 8 items", ("‹","1","›"))}</div>
    <div class="alert info mt-12">{icon("info", 15)}<div><strong>Catalog edits do not change historical prices.</strong> A batch keeps its own cost and selling price; old visits are not repriced.</div></div>'''
    return content


def catalog():
    return shell_page("INV-002", "Vaccine catalogue", USER_INVENTORY, catalog_content(), attention=6)


def catalog_form_drawer():
    base = catalog_content()
    drawer = f'''<div class="drawer wide" role="dialog" aria-modal="true" aria-labelledby="catalog-form-title">
      <div class="drawer-head"><div><div class="drawer-title" id="catalog-form-title">Edit vaccine</div><div class="drawer-sub">Rotavac · catalogue identity</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="drawer-body">
        <div class="alert info" style="margin-bottom:14px">{icon("info", 15)}<div>Changing catalogue details never reprices an existing batch or recorded visit.</div></div>
        <div class="form-grid">
          {field("Vaccine type", "Rotavirus", required=True, width="full", help_text="Group used for due schedules and stock summaries.")}
          {field("Brand name", "Rotavac", required=True)}
          {field("Manufacturer", "Bharat Biotech")}
          {field("Company / supplier", "Bharat Biotech", width="full")}
          {select_field("Category", "Vaccine")}
          {field("Dose schedule", "2-dose infant schedule")}
          {textarea("Storage details", "Store at 2–8°C. Do not freeze. Protect from light.", width="full")}
          {field("MRP", "₹1,200", icon_name="banknote")}
          {field("Net rate", "₹1,050", icon_name="banknote")}
        </div>
        <div class="divider"></div>
        <div class="label">Catalogue metadata</div><div class="mt-8">{kv_list([("Created", "12 Jan 2026"), ("Last updated", "2 Sep 2026 · Arjun Patel"), ("Catalog status", badge("Active", "success"))])}</div>
      </div>
      <div class="drawer-foot"><span class="small muted">Fields marked * are required</span><div class="spacer"></div><button class="btn" type="button">Cancel</button><button class="btn primary" type="button">Save vaccine</button></div>
    </div>'''
    return drawer_overlay(base, "INV-002", "Vaccine catalogue", USER_INVENTORY, drawer)


def batch_detail_content():
    ledger_rows = [
        ("20 Oct 2026 · 09:04", "Vaccination · V-10942", "−1", "28", "Aarav Sharma", badge("Pending sync", "info", "refresh")),
        ("19 Oct 2026 · 15:12", "Vaccination · V-10936", "−1", "29", "Ishaan Gupta", badge("Synced", "success")),
        ("18 Oct 2026 · 11:20", "Vaccination · V-10918", "−1", "30", "Sara Khan", badge("Synced", "success")),
        ("12 Oct 2026 · 10:00", "Stock receipt · GRN-2409", "+48", "31", "Supplier: Bharat Biotech", badge("Synced", "success")),
        ("12 Oct 2026 · 09:55", "Opening balance", "+0", "0", "Batch created", badge("Audit", "neutral")),
    ]
    content = f'''{page_head("Inventory · batch AV-2409", "Batch AV-2409", "Pentavalent · Pentavac SD · received 12 Sep 2026", btn("Receive more", "secondary", "package", href="INV-005.html") + btn("Adjust batch", "primary", "sliders", href="INV-006.html"))}
    <div class="row tight" style="margin-bottom:12px">{strip("On hand", "28", "doses", "package")}{strip("Available", "28", "not expired", "check-circle")}{strip("Expiry", "30 Jun 2027", "249 days", "calendar")}{strip("Stock value", "₹21,280", "at net ₹760", "wallet")}</div>
    <div class="row top">
      <div class="grow col">
        <div class="card"><div class="card-head"><div><div class="card-title">Stock ledger</div><div class="card-sub">Every movement is recorded once; batch remaining is derived from the ledger.</div></div><span class="badge warning">Reconcile after sync</span></div><div class="card-body" style="padding:0">{table(["Date", "Movement", "Delta", "Balance", "Reference", "Status"], ledger_rows, widths=["w-date", "", "w-money", "w-money", "", "w-status"])}</div></div>
        <div class="alert warning">{icon("alert-triangle", 15)}<div><strong>Do not edit the on-hand quantity.</strong> Adjustments and corrections must write a ledger movement with a reason and actor.</div></div>
      </div>
      <div class="col tight w-side">
        <div class="card"><div class="card-head"><div class="card-title">Batch details</div></div><div class="card-body" style="padding-top:8px">{kv_list([("Vaccine", "Pentavalent"), ("Brand", "Pentavac SD"), ("Batch number", "AV-2409"), ("Supplier", "Bharat Biotech"), ("Received", "12 Sep 2026"), ("Expiry", "30 Jun 2027"), ("Purchase price", "₹760 / dose"), ("Selling price", "₹850 / dose")])}</div></div>
        <div class="card"><div class="card-head"><div class="card-title">Batch controls</div></div><div class="card-body" style="display:flex;flex-direction:column;gap:6px">{btn("Adjust stock", "secondary", "sliders", size="sm")} {btn("View all batches", "ghost", "package", size="sm")} {btn("Open movement ledger", "ghost", "list", size="sm")}</div></div>
        {alert("FEFO suggests this batch before AV-2410. The batch remains selectable explicitly for clinical workflows.", "info", "info")}
      </div>
    </div>'''
    return content


def batch_detail():
    return shell_page("INV-001", "Batch AV-2409", USER_INVENTORY, batch_detail_content(), status="Syncing", status_tone="syncing")


def receive_stock_content():
    right = f'''<div class="col tight w-side">
      <div class="card"><div class="card-head"><div class="card-title">Receipt preview</div></div><div class="card-body"><div class="summary-line"><span>Quantity</span><strong>+48 doses</strong></div><div class="summary-line"><span>Purchase cost</span><strong>₹36,480</strong></div><div class="summary-line"><span>Selling value</span><strong>₹40,800</strong></div><div class="summary-line total-line"><span>Expected margin</span><strong class="amount-positive">₹4,320</strong></div><div class="help mt-8">Calculated from purchase price × quantity. This preview is not a financial posting.</div></div></div>
      <div class="card"><div class="card-head"><div class="card-title">Batch rules</div></div><div class="card-body" style="padding-top:8px"><div class="stat-line">{icon("check-circle", 13)}<span>Unique batch number</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Expiry after purchase date</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Quantity non-negative</span></div><div class="stat-line">{icon("alert-circle", 13)}<span>Cannot use expired stock clinically</span></div></div></div>
      {alert("Receiving stock writes a ledger movement. It does not overwrite the batch quantity outside the ledger.", "info", "info")}
    </div>'''
    content = f'''{page_head("Inventory · receive stock", "Receive a batch", "Create a batch and record its incoming stock movement in one local transaction.", btn("Cancel", "ghost", href="INV-001.html") + btn("Receive stock", "primary", "package"))}
    <div class="row top">
      <div class="grow col">
        <div class="form-section"><div class="form-section-head">{icon("package", 15)}<div class="form-section-title">Vaccine & supplier</div></div><div class="form-section-body"><div class="form-grid">{select_field("Vaccine", "Pentavalent · Pentavac SD", required=True)}{field("Batch number", "", required=True, placeholder="e.g. AV-2409")}{field("Supplier", "Bharat Biotech", required=True)}{field("Invoice / GRN", "GRN-2409")}</div></div></div>
        <div class="form-section"><div class="form-section-head">{icon("calendar", 15)}<div class="form-section-title">Dates & quantity</div></div><div class="form-section-body"><div class="form-grid">{field("Purchase date", "20 Oct 2026", icon_name="calendar", required=True)}{field("Expiry date", "30 Jun 2027", icon_name="calendar", required=True)}{field("Quantity received", "48", required=True, suffix="doses")}{field("Purchase price / dose", "₹760", required=True, icon_name="banknote")}{field("Selling price / dose", "₹850", icon_name="banknote")}{field("Storage location", "Cold room · rack 2", icon_name="map-pin")}</div></div></div>
      </div>
      {right}
    </div>'''
    return content


def receive_stock():
    return shell_page("INV-001", "Receive stock", USER_INVENTORY, receive_stock_content(), status="Online")


def adjust_stock_dialog():
    base = batch_detail_content()
    modal = f'''<div class="dialog" role="dialog" aria-modal="true" aria-labelledby="adjust-title">
      <div class="dialog-head"><div class="dialog-icon warning">{icon("sliders", 18)}</div><div><div class="dialog-title" id="adjust-title">Adjust batch stock</div><div class="dialog-sub">AV-2409 · 28 doses on hand</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        {alert("Adjustments are audited and require a reason. Direct quantity edits are not allowed.", "warning", "alert-triangle")}
        <div class="grid-2 mt-12"><div class="field"><label>Adjustment type <span class="req">*</span></label><div class="select"><span>Decrease</span>{icon("chevron-down", 14)}</div></div><div class="field"><label>Quantity <span class="req">*</span></label><div class="input"><span>2</span><span class="muted small" style="margin-left:auto">doses</span></div></div></div>
        <div class="field mt-12"><label>Reason <span class="req">*</span></label><div class="select"><span>Vial breakage</span>{icon("chevron-down", 14)}</div><div class="help">The approved reason taxonomy is not yet confirmed.</div></div>
        <div class="field mt-12"><label>Note</label><div class="textarea"><span class="placeholder">Optional explanation for the audit trail</span></div></div>
        <div class="sticky-summary mt-12"><div class="summary-line"><span>Current on hand</span><strong>28</strong></div><div class="summary-line"><span>Adjustment</span><strong class="amount-out">−2</strong></div><div class="summary-line total-line"><span>New on hand</span><strong>26</strong></div></div>
      </div>
      <div class="dialog-foot"><button class="btn ghost" type="button">Cancel</button><div class="spacer"></div><button class="btn primary" type="button">Record adjustment</button></div>
    </div>'''
    return modal_overlay(base, "INV-001", "Batch AV-2409", USER_INVENTORY, modal)


add(id="INV-001", name="Inventory overview", slug="inventory-overview", section="Inventory", feature="Vaccine and Batch Inventory",
    source="07-Vaccine-and-Batch-Inventory.md", purpose="Show batch-level stock, expiry risk, value and low-stock state without direct quantity editing.",
    users="All clinical roles read; inventory manager/admin manage", permissions="Catalog/batch/adjust admin/inventory manager; clinical roles read and consume.",
    entry="Sidebar Inventory; stock alerts on dashboard; vaccination batch selector.", navigation="By vaccine/batch/ledger/expired views; batch detail; receive stock; adjustment.",
    layout=["Page header", "Stock summary strip", "View tabs", "Search/filter toolbar", "Vaccine stock table", "Expiry callout"],
    components=["Summary cards", "Tabs", "Table", "Status badges", "Expiry alert"],
    data=["₹4.28L stock value", "3 low-stock vaccines", "2 batches expiring ≤30 days", "7 vaccine groups / 23 batches"],
    actions=["Receive stock", "Stock adjustment", "Open vaccine group", "Export", "Filter"],
    forms=["Search", "Storage filter", "Health filter"],
    states=["Loading", "Empty", "Ready", "Low stock", "Expiring", "Expired", "Pending movement", "Concurrent conflict"],
    offline="Local stock reads/writes with pending badges; expired batches excluded from clinical use but visible for waste.",
    keyboard="/ search; table rows open with Enter; filters accessible.",
    a11y="Status includes text; expiry typed; money tabular; table header scopes.",
    deps="INV-001–007; VAC; WAS; BRW; local ledger.",
    open="FEFO mandatory? Who approves adjustments? Is low-stock global or per vaccine?",
    notes="Stock totals are derived from batches/ledger, not a single mutable quantity.",
    html=inventory_overview())

add(id="INV-002", name="Vaccine catalogue", slug="vaccine-catalogue", section="Inventory", feature="Vaccine and Batch Inventory",
    source="07-Vaccine-and-Batch-Inventory.md", purpose="Maintain vaccine identity, brand, manufacturer, category, schedule, storage and reference prices.",
    users="Admin, inventory manager", permissions="Catalog edit admin/inventory manager; read all clinical roles.",
    entry="Inventory tabs or catalogue link.", navigation="Add/edit vaccine; return to stock.",
    layout=["Page header", "Search/filter toolbar", "Catalogue table", "Historical-price note"],
    components=["Table", "Status badges", "Add/edit actions", "Info alert"],
    data=["8 fictional catalogue items", "MRP and net rates", "Manufacturer and category"],
    actions=["Add vaccine", "Import catalogue", "Edit", "Filter"],
    forms=["Search", "Category filter"],
    states=["Loading", "Empty", "Ready", "Duplicate brand", "Archived catalog item"],
    offline="Local edit with outbox; conflict on catalog identity is surfaced.",
    keyboard="Search focus; edit actions labelled with brand.",
    a11y="MRP/net rate columns labelled; status text; table headers.",
    deps="INV-003; INV-007; vaccination pricing.",
    open="Catalog identity/uniqueness policy and supplier return handling remain unresolved.",
    notes="Editing a catalog item never reprices historical batches or visits.",
    html=catalog())

add(id="INV-003", name="Edit vaccine catalogue", slug="edit-vaccine-catalogue", section="Inventory", feature="Vaccine and Batch Inventory",
    source="07-Vaccine-and-Batch-Inventory.md", purpose="Edit catalogue identity and storage/pricing metadata without changing historical records.",
    users="Admin, inventory manager", permissions="Catalog edit admin/inventory manager.",
    entry="Vaccine catalogue row or Add vaccine.", navigation="Save → catalogue. Cancel → catalogue.",
    layout=["Catalogue context behind scrim", "Right drawer form", "Catalogue metadata", "Footer actions"],
    components=["Drawer", "Text/select fields", "Storage textarea", "Metadata"],
    data=["Rotavac", "Bharat Biotech", "2-dose infant schedule", "MRP/net rate"],
    actions=["Save vaccine", "Cancel"],
    forms=["Vaccine type (required)", "Brand (required)", "Manufacturer", "Company", "Category", "Dose schedule", "Storage details", "MRP", "Net rate"],
    states=["Ready", "Saving", "Validation", "Duplicate identity", "Conflict"],
    offline="Local edit and outbox; no historical repricing.",
    keyboard="Focus enters drawer; Escape cancel; labels visible.",
    a11y="Drawer dialog semantics; background inert; error association.",
    deps="INV-002; INV-007.",
    open="Whether catalog items can be archived rather than deleted is unresolved.",
    notes="No batch quantity is edited here.",
    html=catalog_form_drawer())

add(id="INV-004", name="Batch detail", slug="batch-detail", section="Inventory", feature="Vaccine and Batch Inventory",
    source="07-Vaccine-and-Batch-Inventory.md", purpose="Show batch identity, quantities, ledger, expiry and pricing, with auditable adjustment entry points.",
    users="Admin, inventory manager; clinical read", permissions="Adjust/receive admin/inventory manager.",
    entry="Inventory by batch; vaccine group.", navigation="Receive more; adjust; movement ledger; back to inventory.",
    layout=["Page header", "Batch summary strip", "Ledger table", "Batch details rail", "Controls and FEFO note"],
    components=["Summary cards", "Ledger table", "Key-value details", "Warning alert"],
    data=["AV-2409", "28 on hand", "expiry 30 Jun 2027", "₹21,280 value", "5 ledger movements"],
    actions=["Receive more", "Adjust batch", "View all batches", "Open ledger"],
    forms=[],
    states=["Ready", "Pending sync", "Reconciliation error", "Expired", "Zero stock", "Concurrent edit"],
    offline="Ledger reads local; pending movement visible; server trigger reconciliation is required after sync.",
    keyboard="Table and actions reachable; adjustment opens an audited dialog.",
    a11y="Balance derived from ledger; dates typed; status text; table headers.",
    deps="INV-005/006; VAC; WAS; sync reconciliation.",
    open="Server-side stock trigger reconciliation approach is still to be implemented and tested.",
    notes="Direct quantity edits are prohibited in this design.",
    html=batch_detail())

add(id="INV-005", name="Receive stock", slug="receive-stock", section="Inventory", feature="Vaccine and Batch Inventory",
    source="07-Vaccine-and-Batch-Inventory.md", purpose="Create a batch and one incoming stock movement transactionally.",
    users="Admin, inventory manager", permissions="Batch receive admin/inventory manager.",
    entry="Inventory Receive stock; batch detail Receive more.", navigation="Save → batch detail/inventory. Cancel → inventory.",
    layout=["Page header", "Vaccine/supplier form", "Dates/quantity form", "Receiving note", "Receipt preview rail", "Batch rules"],
    components=["Form sections", "Date/quantity fields", "Calculated preview", "Cold-chain acknowledgement"],
    data=["Pentavalent Pentavac SD", "48 doses", "₹760 purchase", "₹850 selling", "Expiry 30 Jun 2027"],
    actions=["Receive stock", "Cancel"],
    forms=["Vaccine (required)", "Batch number (required, unique)", "Supplier", "Invoice/GRN", "Purchase date", "Expiry date", "Quantity", "Purchase price", "Selling price", "Storage location", "Cold-chain acknowledgement"],
    states=["Ready", "Saving", "Duplicate batch", "Invalid expiry", "Negative quantity", "Offline", "Conflict"],
    offline="Local transaction and outbox; no partial batch write.",
    keyboard="Form order; calculated totals updated in implementation; date picker accessible.",
    a11y="Required fields; error text; calculated values labelled; no color-only warnings.",
    deps="INV-001–004; local ledger; sync.",
    open="Partial receipt, batch-number uniqueness across suppliers, and cold-chain evidence requirements remain unresolved.",
    notes="The receipt preview is not a financial posting.",
    html=receive_stock())

add(id="INV-006", name="Adjust stock", slug="adjust-stock", section="Inventory", feature="Vaccine and Batch Inventory",
    source="07-Vaccine-and-Batch-Inventory.md", purpose="Adjust stock through an audited ledger movement with reason and actor.",
    users="Admin, inventory manager (approval policy unresolved)", permissions="Adjust admin/inventory manager; approval for large write-offs unresolved.",
    entry="Batch detail Adjust batch; inventory Stock adjustment.", navigation="Record adjustment → batch detail/ledger. Cancel → batch.",
    layout=["Batch context behind scrim", "Dialog form", "New balance preview", "Reason and note"],
    components=["Adjustment type", "Quantity", "Reason", "Note", "Balance preview"],
    data=["AV-2409", "28 on hand", "−2", "new balance 26"],
    actions=["Record adjustment", "Cancel"],
    forms=["Type (increase/decrease)", "Quantity (required)", "Reason (required)", "Note"],
    states=["Ready", "Validation", "Insufficient stock", "Authorization needed", "Offline", "Conflict"],
    offline="Local movement with pending badge; server conflict is surfaced, not overwritten.",
    keyboard="Focus trap; quantity/type keyboard accessible; Escape cancel.",
    a11y="Reason taxonomy text; preview labels; destructive decrease not color-only.",
    deps="INV-004; audit; ledger; sync.",
    open="Who approves stock adjustments and the reason taxonomy are unresolved.",
    notes="This is an explicit movement, never a direct quantity edit.",
    html=adjust_stock_dialog())


# ---------------------------------------------------------------------------
# Wastage
# ---------------------------------------------------------------------------

def wastage_overview_content():
    rows = [
        ("20 Oct 2026", "<div class='strong'>Pentavalent · AV-2409</div><div class='sub'>Pentavac SD</div>", "2 doses", "<div class='strong'>Vial breakage</div><div class='sub'>During handling</div>", "₹1,520", "Ritika Sen", badge("Pending sync", "info", "refresh"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("18 Oct 2026", "<div class='strong'>PCV · PCV-2411</div><div class='sub'>Prevenar 13</div>", "1 dose", "<div class='strong'>Expired</div><div class='sub'>Removed from usable stock</div>", "₹3,850", "Arjun Patel", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("15 Oct 2026", "<div class='strong'>Rotavirus · RV-2408</div><div class='sub'>Rotavac</div>", "3 doses", "<div class='strong'>Cold-chain breach</div><div class='sub'>Temperature excursion</div>", "₹3,150", "Arjun Patel", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("11 Oct 2026", "<div class='strong'>Influenza · FLU-2405</div><div class='sub'>Influvac Tetra</div>", "2 doses", "<div class='strong'>Expired</div><div class='sub'>End of season</div>", "₹1,960", "Ritika Sen", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("4 Oct 2026", "<div class='strong'>MMR · MMR-2404</div><div class='sub'>MMR II</div>", "1 dose", "<div class='strong'>Vial breakage</div><div class='sub'>Dropped during preparation</div>", "₹840", "Ritika Sen", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("28 Sep 2026", "<div class='strong'>Hepatitis B · HB-2403</div><div class='sub'>Engerix-B</div>", "2 doses", "<div class='strong'>Other</div><div class='sub'>Clinic closure</div>", "₹680", "Arjun Patel", badge("Synced", "success"), f"<span class='row-action'>{icon('more', 16)}</span>"),
    ]
    content = f'''{page_head("Inventory · wastage", "Wastage", "Batch-linked write-offs reduce available stock exactly once and keep an auditable reason.", btn("Record wastage", "primary", "trash", href="WAS-002.html") + btn("Export", "secondary", "download"))}
    <div class="row tight" style="margin-bottom:12px">{strip("This month", "42 doses", "₹31,600 at net rate", "trash")}{strip("Wastage rate", "3.8%", "of doses handled", "trending-down", "warning")}{strip("Expired stock", "12 doses", "2 batches", "calendar")}{strip("Pending sync", "1", "record", "refresh", "info")}</div>
    <div class="row top">
      <div class="grow">
        <div class="toolbar">{search_input("Search vaccine, batch or reason")}<span class="spacer"></span><span class="toolbar-select">All reasons {icon("chevron-down", 12)}</span><span class="toolbar-select">This month {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
        <div class="table-card">{table(["Date", "Vaccine / batch", "Qty", "Reason", "Value", "Recorded by", "Status", ""], rows, widths=["w-date-sm", "w-vaccine", "w-qty", "w-reason", "w-money", "w-actor", "w-status", "w-actions"])}{pagination("1–6 of 31 records", ("‹","1","2","3","…","6","›"))}</div>
      </div>
      <div class="col tight w-side-sm">
        <div class="card"><div class="card-head"><div><div class="card-title">This month by reason</div><div class="card-sub">Doses, not cost</div></div></div><div class="card-body">{mini_bars([18, 9, 7, 5, 3], ["Expired","Breakage","Cold chain","Closure","Other"], alt_every=True)}</div></div>
        <div class="card"><div class="card-head"><div class="card-title">Watch</div><span class="badge warning">2</span></div><div class="card-body"><div class="stat-line"><span>Influenza FLU-2405</span><span class="spacer" style="flex:1"></span><strong>6 left</strong></div><div class="stat-line"><span>PCV-2411</span><span class="spacer" style="flex:1"></span><strong>Expires 12 Nov</strong></div><div class="help mt-8">Review expiring stock before it becomes wastage.</div>{btn("Review expiring stock", "ghost sm", "chevron-right", href="INV-001.html")}</div></div>
        {alert("Waste is never a direct quantity edit; it records a stock movement.", "info", "info")}
      </div>
    </div>'''
    return content


def wastage_overview():
    return shell_page("WAS-001", "Wastage", USER_INVENTORY, wastage_overview_content(), status="Syncing", status_tone="syncing")


def wastage_form_content():
    right = f'''<div class="col tight w-side">
      <div class="card"><div class="card-head"><div class="card-title">Stock after waste</div></div><div class="card-body"><div class="summary-line"><span>Batch on hand</span><strong>28 doses</strong></div><div class="summary-line"><span>Waste quantity</span><strong class="amount-out">−2 doses</strong></div><div class="summary-line total-line"><span>New on hand</span><strong>26 doses</strong></div><div class="help mt-8">The ledger posts the decrease once. Waste is also visible in stock history.</div></div></div>
      <div class="card"><div class="card-head"><div class="card-title">Batch context</div></div><div class="card-body" style="padding-top:8px">{kv_list([("Vaccine", "Pentavalent"), ("Batch", "AV-2409"), ("Expiry", "30 Jun 2027"), ("On hand", "28 doses"), ("Net rate", "₹760")])}</div></div>
      {alert("Expired stock may be wasted but must never be selected for a clinical vaccination.", "warning", "alert-triangle")}
    </div>'''
    content = f'''{page_head("Wastage · new record", "Record wastage", "Write off batch-linked stock with a reason; the ledger reduces availability exactly once.", btn("Cancel", "ghost", href="WAS-001.html") + btn("Record wastage", "primary", "trash"))}
    <div class="row top">
      <div class="grow col">
        <div class="form-section"><div class="form-section-head">{icon("package", 15)}<div class="form-section-title">Batch</div></div><div class="form-section-body"><div class="form-grid">{select_field("Vaccine", "Pentavalent · Pentavac SD", required=True)}{select_field("Batch", "AV-2409 · 28 available · exp 30 Jun 2027", required=True)}{field("Waste date", "20 Oct 2026", required=True, icon_name="calendar")}{field("Quantity", "2", required=True, suffix="doses", help_text="Positive and no more than the available quantity.")}</div></div></div>
        <div class="form-section"><div class="form-section-head">{icon("alert-triangle", 15)}<div class="form-section-title">Reason</div><span class="badge warning">Required</span></div><div class="form-section-body"><div class="form-grid">{select_field("Reason", "Vial breakage", required=True, width="full")}{textarea("Details", "Vial dropped during preparation; glass cracked before draw-up.", width="full", help_text="Visible to admin and inventory manager in audit.")}</div></div></div>
        <div class="help mt-8">{icon("shield", 12)} Recorded by Ritika Sen · Nurse · 20 Oct 2026 · 13:18 IST. The quantity and batch are confirmed against the physical write-off.</div>
      </div>
      {right}
    </div>'''
    return content


def wastage_form():
    return shell_page("WAS-001", "Record wastage", USER_NURSE, wastage_form_content(), status="Online")


add(id="WAS-001", name="Wastage overview", slug="wastage-overview", section="Wastage", feature="Wastage",
    source="08-Wastage.md", purpose="Review batch-linked wastage, reasons, value and stock impact; surface expiry risk before write-off.",
    users="Admin, nurse, inventory manager", permissions="Record proposed for admin/nurse/inventory manager; audit read admin.",
    entry="Sidebar Wastage; inventory expiry review.", navigation="Record wastage; filter by reason/date; review expiring stock.",
    layout=["Page header", "Summary strip", "Search/filter toolbar", "Waste table", "Reason chart and watch rail"],
    components=["Summary cards", "Table", "Bar chart", "Watch list", "Status badges"],
    data=["42 doses this month", "₹31,600", "3.8% rate", "6 fictional records"],
    actions=["Record wastage", "Export", "Filter", "Review expiring stock"],
    forms=["Search", "Reason filter", "Date range"],
    states=["Loading", "Empty", "Ready", "Pending sync", "Conflict", "No waste this month"],
    offline="Local read/write; pending record visible; batch availability rechecked at commit.",
    keyboard="/ search; chart has text alternative; table actions labelled.",
    a11y="Chart has a table/text alternative; reasons in text; quantities and money labelled.",
    deps="WAS-001–004; inventory; audit; reports.",
    open="Reason taxonomy, partial-vial tracking, and large write-off approval are unresolved.",
    notes="Wastage totals are illustrative and must not be treated as live clinic data.",
    html=wastage_overview())

add(id="WAS-002", name="Record wastage", slug="record-wastage", section="Wastage", feature="Wastage",
    source="08-Wastage.md", purpose="Record a positive, batch-linked waste quantity with a reason and actor, reducing stock exactly once.",
    users="Admin, nurse, inventory manager", permissions="Record proposed for these roles; approval thresholds unresolved.",
    entry="Wastage overview Record wastage; batch detail waste action.", navigation="Record → wastage overview. Cancel → back.",
    layout=["Page header", "Batch form", "Reason form", "Actor confirmation", "Before/after stock rail"],
    components=["Select fields", "Quantity", "Reason taxonomy", "Details textarea", "Confirmation checkboxes"],
    data=["Pentavalent AV-2409", "2 doses", "₹760 net rate", "26 remaining"],
    actions=["Record wastage", "Cancel"],
    forms=["Vaccine/batch (required)", "Date (required)", "Quantity (required, >0, ≤ available)", "Reason (required)", "Details", "Physical write-off and clinical-use confirmations"],
    states=["Ready", "Saving", "Insufficient stock", "Expired batch", "Offline", "Conflict"],
    offline="Local commit/outbox; server conflict visible.",
    keyboard="Form order; confirmation checkboxes before submit; focus ring.",
    a11y="Errors linked; stock preview text; no color-only warnings.",
    deps="WAS-001–004; inventory ledger; audit; sync.",
    open="Is a reason taxonomy required? Are partial vials tracked? Who approves large write-offs?",
    notes="Expired stock can be wasted but not used clinically.",
    html=wastage_form())


# ---------------------------------------------------------------------------
# Borrow / lend
# ---------------------------------------------------------------------------

def borrow_list_content():
    rows = [
        ("BR-1042", "<div class='strong'>City Care Clinic</div><div class='sub'>External clinic · Indiranagar</div>", badge("Lent out", "warning"), "Pentavalent · AV-2409", "10", "6", "4", "24 Oct 2026", badge("Partially returned", "warning"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("BR-1038", "<div class='strong'>Dr. Rohan Iyer</div><div class='sub'>Walk-in doctor</div>", badge("Borrowed in", "info"), "PCV · PCV-2410", "6", "0", "6", "22 Oct 2026", badge("Outstanding", "info"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("BR-1031", "<div class='strong'>Sunrise Pediatrics</div><div class='sub'>External clinic · Koramangala</div>", badge("Lent out", "warning"), "MMR · MMR-2404", "5", "5", "0", "18 Oct 2026", badge("Closed", "neutral"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("BR-1029", "<div class='strong'>Dr. Neha Shah</div><div class='sub'>Walk-in doctor</div>", badge("Lent out", "warning"), "Varicella · VAR-2407", "4", "2", "2", "27 Oct 2026", badge("Partially returned", "warning"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("BR-1024", "<div class='strong'>Green Cross Clinic</div><div class='sub'>External clinic · HSR Layout</div>", badge("Borrowed in", "info"), "Rotavirus · RV-2408", "8", "4", "4", "25 Oct 2026", badge("Partially returned", "warning"), f"<span class='row-action'>{icon('more', 16)}</span>"),
        ("BR-1019", "<div class='strong'>Dr. Anil Kumar</div><div class='sub'>Walk-in doctor</div>", badge("Lent out", "warning"), "Influenza · FLU-2405", "3", "3", "0", "12 Oct 2026", badge("Closed", "neutral"), f"<span class='row-action'>{icon('more', 16)}</span>"),
    ]
    content = f'''{page_head("Inventory · borrow & return", "Borrowed & lent vaccines", "Track batch-linked loans, partial returns and outstanding balances without treating a loan as a sale.", btn("Record borrow / lend", "primary", "repeat", href="BRW-002.html") + btn("Export", "secondary", "download"))}
    <div class="row tight" style="margin-bottom:12px">{strip("Open records", "4", "outstanding balances", "repeat")}{strip("Lent out", "16", "doses outstanding", "arrow-up-right", "warning")}{strip("Borrowed in", "10", "doses outstanding", "arrow-left", "info")}{strip("Overdue return", "1", "BR-1042 · 4 days", "clock", "danger")}</div>
    <div style="margin-bottom:10px">{tabs([("Open", "4"), ("Partially returned", "3"), ("Closed", "18"), ("All records", "25")], 0, extra=f'<span class="spacer" style="flex:1"></span><span class="small muted">Batch identity preserved · returns restore stock once</span>')}</div>
    <div class="toolbar">{search_input("Search counterparty, vaccine or batch")}<span class="spacer"></span><span class="toolbar-select">All directions {icon("chevron-down", 12)}</span><span class="toolbar-select">Due: all {icon("chevron-down", 12)}</span>{btn("Filters", "", "filter", size="sm")}</div>
    <div class="table-card">{table(["Record", "Counterparty", "Direction", "Vaccine / batch", "Qty", "Returned", "Outstanding", "Due", "Status", ""], rows, widths=["w-date", "w-name", "w-status", "w-name", "w-money", "w-money", "w-money", "w-date", "w-status", "w-actions"])}{pagination("1–6 of 25 records", ("‹","1","2","3","…","5","›"))}</div>
    <div class="alert warning mt-12">{icon("alert-triangle", 15)}<div><strong>One return is overdue.</strong> City Care Clinic has 4 Pentavalent doses outstanding from BR-1042. Review before the batch expires.</div></div>'''
    return content


def borrow_list():
    return shell_page("BRW-001", "Borrow & return", USER_INVENTORY, borrow_list_content(), attention=6)


def borrow_form_content():
    right = f'''<div class="col tight w-side">
      <div class="card"><div class="card-head"><div class="card-title">Stock effect</div></div><div class="card-body"><div class="summary-line"><span>Batch on hand</span><strong>28 doses</strong></div><div class="summary-line"><span>Loan quantity</span><strong>10 doses</strong></div><div class="summary-line total-line"><span>Available after</span><strong>18 doses</strong></div><div class="help mt-8">Lending reduces available stock once. The outstanding balance remains until returned or approved as lost.</div></div></div>
      <div class="card"><div class="card-head"><div class="card-title">Rules</div></div><div class="card-body" style="padding-top:8px"><div class="stat-line">{icon("check-circle", 13)}<span>Counterparty required</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Batch quantity must be available</span></div><div class="stat-line">{icon("check-circle", 13)}<span>Return cannot exceed outstanding</span></div><div class="stat-line">{icon("alert-circle", 13)}<span>Lost/damaged needs approval</span></div></div></div>
      {alert("A loan is not a sale. Do not create a receipt or finance transaction for this movement.", "info", "info")}
    </div>'''
    content = f'''{page_head("Borrow & return · new record", "Record borrow / lend", "Move a batch with an expected return; preserve the batch and an outstanding balance.", btn("Cancel", "ghost", href="BRW-001.html") + btn("Save record", "primary", "check"))}
    <div class="row top">
      <div class="grow col">
        <div class="form-section"><div class="form-section-head">{icon("repeat", 15)}<div class="form-section-title">Direction & counterparty</div></div><div class="form-section-body">
          <table class="form-table"><colgroup><col style="width:50%"><col style="width:50%"></colgroup><tbody>
            <tr><td><div class="field"><label>Direction <span class="req">*</span></label><div class="segmented"><span class="active">Lend out</span><span>Borrow in</span></div></div></td><td>{field("Counterparty", "City Care Clinic", required=True)}</td></tr>
            <tr><td>{field("Contact", "+91 80 4112 9000", icon_name="phone")}</td><td>{field("Record date", "20 Oct 2026", required=True, icon_name="calendar")}</td></tr>
            <tr><td>{field("Expected return", "24 Oct 2026", icon_name="calendar")}</td><td>{field("Reference", "BR-1043", help_text="Generated after save.")}</td></tr>
          </tbody></table>
        </div></div>
        <div class="form-section"><div class="form-section-head">{icon("package", 15)}<div class="form-section-title">Vaccine & quantity</div></div><div class="form-section-body"><div class="form-grid">{select_field("Vaccine", "Pentavalent · Pentavac SD", required=True)}{select_field("Batch", "AV-2409 · 28 available · exp 30 Jun 2027", required=True)}{field("Quantity", "10", required=True, suffix="doses")}{field("Net rate", "₹760", icon_name="banknote", help_text="Reference only; this is not a sale.")}</div></div></div>
      </div>
      {right}
    </div>'''
    return content


def borrow_form():
    return shell_page("BRW-001", "Record borrow / lend", USER_INVENTORY, borrow_form_content(), status="Online")


def borrow_return_dialog():
    base = borrow_list_content()
    modal = f'''<div class="dialog" role="dialog" aria-modal="true" aria-labelledby="return-title">
      <div class="dialog-head"><div class="dialog-icon">{icon("undo", 18)}</div><div><div class="dialog-title" id="return-title">Record a return</div><div class="dialog-sub">BR-1042 · City Care Clinic · Pentavalent AV-2409</div></div><span class="close-x">{icon("x", 16)}</span></div>
      <div class="dialog-body">
        <div class="grid-2"><div>{kv_list([("Outstanding", "4 doses"), ("Already returned", "6 of 10"), ("Due", "24 Oct 2026 · overdue")])}</div><div>{kv_list([("Batch", "AV-2409"), ("Expiry", "30 Jun 2027"), ("Status", badge("Partially returned", "warning"))])}</div></div>
        <div class="divider"></div>
        <div class="form-grid">{field("Return quantity", "4", required=True, suffix="doses", help_text="Maximum 4 outstanding.")}{field("Return date", "20 Oct 2026", required=True, icon_name="calendar")}{select_field("Condition", "Usable · return to stock")}{textarea("Note", "Returned in original cold-chain box; temperature log checked.", width="full")}</div>
        {alert("Returning the full outstanding quantity closes the record. A partial return keeps it open.", "info", "info")}
        <div class="check-row mt-8"><span class="checkbox"></span><span class="check-text">I verified the physical batch and quantity.</span></div>
      </div>
      <div class="dialog-foot"><span class="small muted">Remaining after: 0 doses</span><div class="spacer"></div><button class="btn ghost" type="button">Cancel</button><button class="btn primary" type="button">Record return</button></div>
    </div>'''
    return modal_overlay(base, "BRW-001", "Borrow & return", USER_INVENTORY, modal)


add(id="BRW-001", name="Borrow & return", slug="borrow-return", section="Borrow & Return", feature="Borrowed and Lent Vaccines",
    source="09-Borrowed-and-Lent-Vaccines.md", purpose="Track batch-linked loans, partial returns and outstanding quantities across counterparties.",
    users="Admin, nurse, inventory manager", permissions="Record proposed for these roles; write-off approval unresolved.",
    entry="Sidebar Borrow & return; inventory ledger.", navigation="Record borrow/lend; record return; filter open/closed; export.",
    layout=["Page header", "Summary strip", "Status tabs", "Search/filter toolbar", "Borrow table", "Overdue alert"],
    components=["Summary cards", "Tabs", "Table", "Progress text (returned/outstanding)", "Status badges"],
    data=["4 open records", "16 doses lent out", "10 borrowed in", "1 overdue", "6 fictional records"],
    actions=["Record borrow/lend", "Record return", "Export", "Filter"],
    forms=["Search", "Direction filter", "Due filter"],
    states=["Loading", "Empty", "Open", "Partially returned", "Closed", "Overdue", "Over-return blocked", "Pending sync"],
    offline="Local records/returns with pending badges; balance from local ledger; server conflict visible.",
    keyboard="/ search; return action labelled; tabs arrow-key semantics.",
    a11y="Outstanding not color-only; progress has text; status labels.",
    deps="BRW-001–005; inventory ledger; audit.",
    open="Cross-clinic borrowing, write-off authority, due-date reminders and batch split/merge policy are unresolved.",
    notes="Loans do not create receipts or finance transactions.",
    html=borrow_list())

add(id="BRW-002", name="Record borrow / lend", slug="record-borrow-lend", section="Borrow & Return", feature="Borrowed and Lent Vaccines",
    source="09-Borrowed-and-Lent-Vaccines.md", purpose="Record a directional, batch-linked loan and its expected return without treating it as a sale.",
    users="Admin, nurse, inventory manager", permissions="Record proposed for these roles.",
    entry="Borrow list Record borrow/lend.", navigation="Save → borrow list/detail. Cancel → list.",
    layout=["Page header", "Direction/counterparty form", "Vaccine/quantity form", "Stock effect rail", "Rules"],
    components=["Segmented direction", "Counterparty fields", "Batch selector", "Quantity", "Stock preview", "Info alert"],
    data=["City Care Clinic", "Pentavalent AV-2409", "10 doses", "Expected return 24 Oct"],
    actions=["Save record", "Cancel"],
    forms=["Direction (required)", "Counterparty (required)", "Contact", "Record date", "Expected return", "Reference", "Vaccine/batch (required)", "Quantity (required, ≤ available)", "Note"],
    states=["Ready", "Saving", "Insufficient stock", "Overdue date", "Offline", "Conflict"],
    offline="Local commit/outbox; batch availability checked locally and revalidated at commit.",
    keyboard="Direction toggle keyboard accessible; form order; save shortcut documented.",
    a11y="Direction labels not color-only; quantity errors linked; stock preview labelled.",
    deps="BRW-001/003; inventory; audit.",
    open="Who can write off a lost item and whether due dates create reminders.",
    notes="No receipt, payment or sale is created by this workflow.",
    html=borrow_form())

add(id="BRW-003", name="Record return", slug="record-return", section="Borrow & Return", feature="Borrowed and Lent Vaccines",
    source="09-Borrowed-and-Lent-Vaccines.md", purpose="Record a full or partial return without exceeding the outstanding balance or closing the record early.",
    users="Admin, nurse, inventory manager", permissions="Record return proposed for these roles.",
    entry="Borrow list open/partial record Return.", navigation="Record return → list/detail with updated balance. Cancel → list.",
    layout=["Borrow list behind scrim", "Return dialog", "Balance/context summary", "Return quantity and condition", "Confirmation"],
    components=["Dialog", "Balance summary", "Return fields", "Condition select", "Checkbox"],
    data=["BR-1042", "4 outstanding", "6 already returned", "AV-2409"],
    actions=["Record return", "Cancel"],
    forms=["Return quantity (required, ≤ outstanding)", "Return date", "Condition", "Note", "Physical verification"],
    states=["Ready", "Validation", "Over-return blocked", "Closed record", "Offline", "Conflict"],
    offline="Local return and outbox; server conflict surfaced; returns restore stock once.",
    keyboard="Focus trap; quantity focus; Escape cancel.",
    a11y="Outstanding and remaining balance in text; no color-only warning.",
    deps="BRW-001/002; inventory; audit; sync.",
    open="Closed-record behavior, condition taxonomy, and lost/damaged resolution path are unresolved.",
    notes="Partial returns keep the original record open.",
    html=borrow_return_dialog())