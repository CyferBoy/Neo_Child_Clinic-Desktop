"""Shared HTML component helpers for the Neo Child Clinic Desktop design preview."""
from __future__ import annotations

import html
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # tools -> prototype -> docs/UI_Design
PROTOTYPE = ROOT / "prototype"
SCREENS_DIR = PROTOTYPE / "screens"
SCREENSHOTS = ROOT / "screenshots"
SPECS = ROOT / "Screens"

# Lucide-compatible, hand-maintained 24x24 stroke paths. No emoji or icon font.
PATHS = {
    "logo": '<path d="M12 3.5c1.2 2.3 3.1 3.7 5.4 4.2v4.7c0 3.5-2.2 6.3-5.4 7.8-3.2-1.5-5.4-4.3-5.4-7.8V7.7c2.3-.5 4.2-1.9 5.4-4.2Z"/><path d="M12 8.4v6.2M8.9 11.5h6.2"/>',
    "dashboard": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "user": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "user-plus": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M19 8v6M22 11h-6"/>',
    "user-x": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m17 8 5 5M22 8l-5 5"/>',
    "syringe": '<path d="m18 2 4 4M17 7 7 17M3 21l4-4M14 4l6 6M9 9l6 6M5 13l6 6"/>',
    "stethoscope": '<path d="M4 3v6a4 4 0 0 0 8 0V3M8 13v3a5 5 0 0 0 10 0v-2"/><circle cx="18" cy="12" r="2"/>',
    "package": '<path d="m7.5 4.3 9 5.2M12 22V12M3 7l9-4 9 4v10l-9 4-9-4V7Z"/><path d="M3 7l9 5 9-5"/>',
    "boxes": '<path d="m7.5 4.3 9 5.2M12 22V12M3 7l9-4 9 4v10l-9 4-9-4V7Z"/><path d="M3 7l9 5 9-5"/>',
    "trash": '<path d="M3 6h18M8 6V4h8v2M19 6l-1 15H6L5 6M10 11v6M14 11v6"/>',
    "repeat": '<path d="m17 1 4 4-4 4M3 11V9a4 4 0 0 1 4-4h14M7 23l-4-4 4-4M21 13v2a4 4 0 0 1-4 4H3"/>',
    "bell": '<path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M13.7 21a2 2 0 0 1-3.4 0"/>',
    "wallet": '<path d="M20 7V5a2 2 0 0 0-2-2H5a3 3 0 0 0 0 6h15v12H5a3 3 0 0 1-3-3V6"/><path d="M16 13h2"/>',
    "receipt": '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1-2-1Z"/><path d="M8 7h8M8 11h8M8 15h5"/>',
    "chart": '<path d="M3 3v18h18M7 16v-5M12 16V7M17 16v-8"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
    "shield-alert": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="M12 8v4M12 16h.01"/>',
    "settings": '<path d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.1 2.1-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6v.2h-3v-.2a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1L6.6 17l.1-.1a1.7 1.7 0 0 0 .3-1.9 1.7 1.7 0 0 0-1.6-1H5v-3h.4a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9L6.6 8l2.1-2.1.1.1a1.7 1.7 0 0 0 1.9.3 1.7 1.7 0 0 0 1-1.6V4h3v.7a1.7 1.7 0 0 0 1 1.6 1.7 1.7 0 0 0 1.9-.3l.1-.1L20.8 8l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.6 1h.4v3H22a1.7 1.7 0 0 0-1.6 1Z"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
    "filter": '<path d="M3 5h18l-7 8v6l-4 2v-8L3 5Z"/>',
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "chevron-up": '<path d="m18 15-6-6-6 6"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "chevron-left": '<path d="m15 18-6-6 6-6"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "calendar-clock": '<path d="M21 7H3M8 2v4M16 2v4M6 21h6M16 14v3l2 1"/><path d="M21 3H3v18h8"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "alert-triangle": '<path d="m10.3 3.9-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3.1l-8-14a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4M12 17h.01"/>',
    "alert-circle": '<circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01"/>',
    "check": '<path d="m20 6-11 11-5-5"/>',
    "check-circle": '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
    "x-circle": '<circle cx="12" cy="12" r="9"/><path d="m15 9-6 6M9 9l6 6"/>',
    "printer": '<path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
    "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>',
    "lock": '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5 19 11M18 5l3 3"/>',
    "wifi-off": '<path d="m2 2 20 20M8.5 8.5a10.5 10.5 0 0 1 12 1.5M5 12.5a10.5 10.5 0 0 1 3-1.5M8.5 16.5a5.5 5.5 0 0 1 7 0M12 20h.01"/>',
    "refresh": '<path d="M20 7h-5V2M4 17h5v5"/><path d="M4.7 9A8 8 0 0 1 19 7l1 1M19.3 15A8 8 0 0 1 5 17l-1-1"/>',
    "cloud-off": '<path d="m2 2 20 20M5.8 5.8A7 7 0 0 0 7 19h9a5 5 0 0 0 4.2-2.4M9.9 5.1A7 7 0 0 1 19 11h1a4 4 0 0 1 .8 2.3"/>',
    "cloud": '<path d="M17.5 19H6a4 4 0 0 1-.5-8A6.5 6.5 0 0 1 18 9.5h.5a4.5 4.5 0 0 1-.9 9.5Z"/>',
    "help": '<circle cx="12" cy="12" r="9"/><path d="M9.1 9a3 3 0 1 1 4.4 2.7c-.9.4-1.5 1.2-1.5 2.3M12 17h.01"/>',
    "arrow-right": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-left": '<path d="M19 12H5M11 18l-6-6 6-6"/>',
    "arrow-up-right": '<path d="M7 17 17 7M7 7h10v10"/>',
    "external-link": '<path d="M15 3h6v6M10 14 21 3M21 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h6"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
    "edit": '<path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5Z"/>',
    "more": '<circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>',
    "home": '<path d="m3 11 9-8 9 8M5 10v10h14V10"/>',
    "clipboard": '<rect x="5" y="4" width="14" height="18" rx="2"/><path d="M9 4V2h6v2M9 9h6M9 13h6M9 17h4"/>',
    "activity": '<path d="M3 12h4l2-7 4 14 2-7h6"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M8 13h8M8 17h8"/>',
    "credit-card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20M6 15h3"/>',
    "banknote": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2"/><path d="M6 10h.01M18 14h.01"/>',
    "trending-up": '<path d="m3 17 6-6 4 4 8-8M15 7h6v6"/>',
    "trending-down": '<path d="m3 7 6 6 4-4 8 8M15 17h6v-6"/>',
    "log-out": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>',
    "logout": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>',
    "folder": '<path d="M3 7a2 2 0 0 1 2-2h5l2 2h7a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7Z"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>',
    "hard-drive": '<path d="M22 12H2M5.5 5h13L22 12v5a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-5l3.5-7Z"/><path d="M6 16h.01M10 16h.01"/>',
    "rotate": '<path d="M3 12a9 9 0 1 0 3-6.7L3 8M3 3v5h5"/>',
    "save": '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2Z"/><path d="M17 21v-8H7v8M7 3v5h8"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4 20-7Z"/><path d="M22 2 11 13"/>',
    "message": '<path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4v8Z"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    "map-pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    "cake": '<path d="M20 21H4a1 1 0 0 1-1-1v-5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v5a1 1 0 0 1-1 1ZM3 14h18M7 14V9M12 14V9M17 14V9"/><path d="M7 6c0-1 1-1.5 1-2.5S7 2 7 2M12 6c0-1 1-1.5 1-2.5S12 2 12 2M17 6c0-1 1-1.5 1-2.5S17 2 17 2"/>',
    "baby": '<path d="M9 12h.01M15 12h.01M10 16c1.3 1 2.7 1 4 0"/><path d="M5 9a7 7 0 0 1 14 0v6a4 4 0 0 1-4 4h-6a4 4 0 0 1-4-4V9Z"/><path d="M9 2c0 2-1 2-1 3M15 2c0 2 1 2 1 3"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8l1.1 1.1L12 21l7.8-7.5 1.1-1.1a5.5 5.5 0 0 0-.1-7.8Z"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M2 13h20"/>',
    "list": '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    "columns": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M12 3v18"/>',
    "sliders": '<path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6"/>',
    "tag": '<path d="M20.6 13.4 12 22l-9-9V3h10l7.6 7.6a2 2 0 0 1 0 2.8Z"/><circle cx="7.5" cy="7.5" r="1"/>',
    "truck": '<path d="M14 18V6H2v12h12ZM14 9h4l4 4v5h-8"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="18" r="2"/>',
    "archive": '<path d="M21 8v13H3V8M1 3h22v5H1zM10 12h4"/>',
    "undo": '<path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 0 12h-3"/>',
    "pause": '<rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/>',
    "play": '<path d="m7 4 13 8-13 8V4Z"/>',
    "loader": '<path d="M12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M2 12h4M18 12h4M4.9 19.1l2.8-2.8M16.3 7.7l2.8-2.8"/>',
    "copy": '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    "qr": '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3h-3zM20 14v3M14 20h3M20 20h1"/>',
    "file-check": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M8 15l2 2 4-4"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M12 6h.01M16 6h.01M8 10h.01M12 10h.01M16 10h.01M8 14h.01M12 14h.01M16 14h.01"/>',
    "moon": '<path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8Z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "command": '<path d="M18 3a3 3 0 0 0-3 3v12a3 3 0 1 0 3-3H6a3 3 0 1 0 3 3V6a3 3 0 1 0-3 3h12a3 3 0 0 0 0-6Z"/>',
    "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8-6.2-3.3L5.8 21l1.2-6.8-5-4.9 6.9-1L12 2Z"/>',
    "circle": '<circle cx="12" cy="12" r="9"/>',
    "ellipsis": '<circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>',
}


def icon(name: str, size: int = 16, cls: str = "") -> str:
    path = PATHS.get(name, PATHS["circle"])
    return (
        f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true">{path}</svg>'
    )


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def initials(name: str) -> str:
    parts = [p for p in name.replace(".", " ").split() if p]
    return "".join(p[0] for p in parts[:2]).upper()


def avatar(name: str, cls: str = "") -> str:
    return f'<span class="avatar {cls}" aria-hidden="true">{esc(initials(name))}</span>'


def badge(label: str, tone: str = "neutral", icon_name: str | None = None) -> str:
    ic = icon(icon_name, 11) if icon_name else ""
    return f'<span class="badge {tone}">{ic}{esc(label)}</span>'


def btn(label: str, variant: str = "", icon_name: str | None = None, size: str = "", href: str | None = None) -> str:
    classes = "btn"
    if variant:
        classes += f" {variant}"
    if size:
        classes += f" {size}"
    ic = icon(icon_name, 15) if icon_name else ""
    if href:
        return f'<a class="{classes}" href="{esc(href)}">{ic}{esc(label)}</a>'
    return f'<button class="{classes}" type="button">{ic}{esc(label)}</button>'


def icon_btn(icon_name: str, label: str, bordered: bool = False, dot: bool = False) -> str:
    cls = "icon-btn bordered" if bordered else "icon-btn"
    dot_html = '<span class="dot"></span>' if dot else ""
    return f'<button class="{cls}" type="button" title="{esc(label)}" aria-label="{esc(label)}">{icon(icon_name, 17)}{dot_html}</button>'


def status_pill(label: str, tone: str = "", icon_name: str | None = None) -> str:
    ic = icon(icon_name, 13) if icon_name else ""
    return f'<span class="status-pill">{ic}<span class="status-dot {tone}"></span>{esc(label)}</span>'


def field(label: str, value: str = "", required: bool = False, help_text: str = "", error: str = "",
          placeholder: str = "", type: str = "text", width: str = "", icon_name: str | None = None,
          focus: bool = False, suffix: str = "") -> str:
    req = '<span class="req">*</span>' if required else ""
    cls = "input"
    if error:
        cls += " error"
    if focus:
        cls += " focus"
    ic = icon(icon_name, 14) if icon_name else ""
    content = f'<span>{esc(value)}</span>' if value else f'<span class="placeholder">{esc(placeholder or " ")}</span>'
    suffix_html = f'<span class="muted small">{esc(suffix)}</span>' if suffix else ""
    help_html = f'<div class="help">{esc(help_text)}</div>' if help_text else ""
    err_html = f'<div class="error-text">{icon("alert-circle", 12)}{esc(error)}</div>' if error else ""
    width_cls = f" {width}" if width else ""
    if icon_name:
        return f'''<div class="field{width_cls}"><div class="label-row"><label>{esc(label)} {req}</label></div><div class="{cls}">{ic}{content}{suffix_html}</div>{help_html}{err_html}</div>'''
    return f'''<div class="field{width_cls}"><div class="label-row"><label>{esc(label)} {req}</label></div><div class="{cls}">{content}{suffix_html}</div>{help_html}{err_html}</div>'''


def select_field(label: str, value: str, required: bool = False, help_text: str = "", width: str = "", focus: bool = False) -> str:
    req = '<span class="req">*</span>' if required else ""
    cls = "select focus" if focus else "select"
    help_html = f'<div class="help">{esc(help_text)}</div>' if help_text else ""
    width_cls = f" {width}" if width else ""
    return f'''<div class="field{width_cls}"><div class="label-row"><label>{esc(label)} {req}</label></div><div class="{cls}"><span>{esc(value)}</span>{icon("chevron-down", 14, "chevron")}</div>{help_html}</div>'''


def textarea(label: str, value: str = "", required: bool = False, help_text: str = "", placeholder: str = "", width: str = "full", error: str = "") -> str:
    req = '<span class="req">*</span>' if required else ""
    help_html = f'<div class="help">{esc(help_text)}</div>' if help_text else ""
    err_html = f'<div class="error-text">{icon("alert-circle", 12)}{esc(error)}</div>' if error else ""
    content = f'<span>{esc(value)}</span>' if value else f'<span class="placeholder">{esc(placeholder)}</span>'
    return f'''<div class="field {width}"><div class="label-row"><label>{esc(label)} {req}</label></div><div class="textarea">{content}</div>{help_html}{err_html}</div>'''


def checkbox(label_html: str, checked: bool = False) -> str:
    box = f'<span class="checkbox checked">{icon("check", 11)}</span>' if checked else '<span class="checkbox"></span>'
    return f'<div class="check-row">{box}<span class="check-text">{label_html}</span></div>'


def toggle(label_html: str, on: bool = True) -> str:
    return f'<div class="check-row"><span class="toggle {"on" if on else ""}"></span><span class="check-text">{label_html}</span></div>'


def metric(label: str, value: str, foot: str = "", icon_name: str | None = None, variant: str = "", hint: str = "") -> str:
    ic = icon(icon_name, 16) if icon_name else ""
    hint_html = f'<span class="badge {hint.split(":")[0] if ":" in hint else "neutral"}">{esc(hint.split(":")[1] if ":" in hint else hint)}</span>' if hint else ""
    return f'''<div class="metric-card {variant}"><div class="metric-top"><div class="metric-label">{esc(label)}</div><div class="metric-icon">{ic}</div></div><div class="metric-value">{value}</div><div class="metric-foot">{hint_html}<span>{esc(foot)}</span></div></div>'''


def search_input(placeholder: str = "Search patients by name, clinic ID or phone") -> str:
    return f'<div class="search-input">{icon("search", 14)}<div class="input"><span class="placeholder">{esc(placeholder)}</span><span class="kbd" style="margin-left:auto">/</span></div></div>'


def table(headers, rows, widths=None, selected: int | None = None, actions: bool = True) -> str:
    widths = widths or []
    head = []
    for i, h in enumerate(headers):
        w = f' class="{widths[i]}"' if i < len(widths) else ""
        head.append(f"<th{w}>{h}</th>")
    body = []
    for r_idx, row in enumerate(rows):
        tr_cls = ' class="selected"' if selected is not None and r_idx == selected else ""
        cells = []
        for i, cell in enumerate(row):
            w = f' class="{widths[i]}"' if i < len(widths) else ""
            if isinstance(cell, tuple):
                val, extra = cell
                if extra:
                    w = f' class="{extra}"'
            else:
                val = cell
            cells.append(f"<td{w}>{val}</td>")
        body.append(f"<tr{tr_cls}>{''.join(cells)}</tr>")
    return f'<table class="table"><thead><tr>{"".join(head)}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def pagination(total: str = "1–10 of 126", pages=("‹", "1", "2", "3", "…", "13", "›")) -> str:
    buttons = []
    for p in pages:
        cls = "page-btn active" if p == "1" else "page-btn"
        buttons.append(f'<span class="{cls}">{esc(p)}</span>')
    return f'<div class="pagination"><span>{esc(total)}</span><span class="spacer"></span>{"".join(buttons)}</div>'


def tabs(items, active: int = 0, extra: str = "") -> str:
    out = []
    for i, (label, count) in enumerate(items):
        cls = "tab active" if i == active else "tab"
        count_html = f'<span class="count">{count}</span>' if count is not None else ""
        out.append(f'<span class="{cls}">{esc(label)}{count_html}</span>')
    return f'<div class="tab-bar"><div class="tabs">{"".join(out)}</div>{extra}</div>'


def timeline(items) -> str:
    out = []
    for item in items:
        tone = item.get("tone", "")
        title = item["title"]
        time = item.get("time", "")
        body = item.get("body", "")
        meta = item.get("meta", "")
        out.append(f'''<div class="tl-item"><span class="tl-dot {tone}"></span><div class="tl-head"><div class="tl-title">{title}</div><div class="tl-time">{time}</div></div><div class="tl-body">{body}</div>{f'<div class="tl-meta">{meta}</div>' if meta else ''}</div>''')
    return f'<div class="timeline">{"".join(out)}</div>'


def mini_bars(values, labels=None, alt_every: bool = False) -> str:
    max_v = max(values) if values else 1
    bars = []
    for i, v in enumerate(values):
        h = max(3, round((v / max_v) * 78))
        cls = "bar alt" if alt_every and i % 2 else "bar"
        bars.append(f'<div class="bar-col"><div class="{cls}" style="height:{h}px"></div><div class="bar-label">{esc(labels[i]) if labels else ""}</div></div>')
    return f'<div class="bars">{"".join(bars)}</div>'


def line_chart(values, labels=None, height: int = 150, width: int = 500, color: str = "var(--chart-1)", fill: str = "rgba(15,93,100,.08)") -> str:
    if not values:
        return ""
    max_v = max(values)
    min_v = min(values)
    rng = max(1, max_v - min_v)
    pad_x, pad_top, pad_bottom = 20, 16, 26
    pts = []
    for i, v in enumerate(values):
        x = pad_x + (width - 2 * pad_x) * (i / max(1, len(values) - 1))
        y = pad_top + (height - pad_top - pad_bottom) * (1 - (v - min_v) / rng)
        pts.append((x, y))
    point_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{pad_x},{height-pad_bottom} {point_str} {width-pad_x},{height-pad_bottom}"
    label_html = ""
    if labels:
        for i, lab in enumerate(labels):
            x = pad_x + (width - 2 * pad_x) * (i / max(1, len(labels) - 1))
            label_html += f'<text x="{x:.1f}" y="{height-7}" font-size="9" fill="#6b7d80" text-anchor="middle" font-family="Noto Sans">{esc(lab)}</text>'
    grid = "".join(f'<line x1="{pad_x}" y1="{pad_top + i * (height-pad_top-pad_bottom)/4:.1f}" x2="{width-pad_x}" y2="{pad_top + i * (height-pad_top-pad_bottom)/4:.1f}" stroke="#e7eeec" stroke-width="1"/>' for i in range(5))
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#fff" stroke="{color}" stroke-width="2"/>' for x, y in pts)
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Trend chart"><rect width="{width}" height="{height}" fill="transparent"/>{grid}<polygon points="{area}" fill="{fill}"/><polyline points="{point_str}" fill="none" stroke="{color}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>{dots}{label_html}</svg>'''


def donut(parts, center_value: str = "", center_label: str = "") -> str:
    # parts: list of (value, color)
    total = sum(v for v, _ in parts) or 1
    circumference = 2 * math.pi * 35
    offset = 0
    segments = []
    for value, color in parts:
        length = circumference * (value / total)
        segments.append(f'<circle cx="46" cy="46" r="35" fill="none" stroke="{color}" stroke-width="11" stroke-dasharray="{length:.1f} {circumference - length:.1f}" stroke-dashoffset="{-offset:.1f}" transform="rotate(-90 46 46)"/>')
        offset += length
    return f'''<div class="donut-center"><svg width="92" height="92" viewBox="0 0 92 92" role="img" aria-label="Distribution">{"".join(segments)}</svg><div class="donut-label"><strong>{esc(center_value)}</strong><span>{esc(center_label)}</span></div></div>'''


def alert(text: str, tone: str = "info", icon_name: str = "info") -> str:
    return f'<div class="alert {tone}">{icon(icon_name, 15)}<div>{text}</div></div>'


def kv_list(items) -> str:
    return "".join(f'<div class="kv"><dt>{esc(k)}</dt><dd>{v}</dd></div>' for k, v in items)


NAV = [
    ("Workspace", [
        ("dashboard", "Dashboard", "DASH-001"),
        ("users", "Patients", "PAT-001"),
        ("syringe", "Vaccinations", "VAC-001"),
        ("stethoscope", "Consultations", "CON-001"),
    ]),
    ("Inventory", [
        ("package", "Inventory", "INV-001"),
        ("trash", "Wastage", "WAS-001"),
        ("repeat", "Borrow & return", "BRW-001"),
    ]),
    ("Follow-up", [
        ("bell", "Due vaccinations", "REM-001"),
        ("calendar", "Personal reminders", "REM-003"),
    ]),
    ("Business", [
        ("wallet", "Finance", "FIN-001"),
        ("receipt", "Receipts", "RCP-001"),
        ("chart", "Reports", "RPT-001"),
    ]),
    ("Administration", [
        ("user-plus", "Staff", "STF-001"),
        ("clipboard", "Audit log", "AUD-001"),
        ("refresh", "Sync center", "SYS-001"),
        ("settings", "Settings", "SET-001"),
    ]),
]

USER_ADMIN = {"name": "Ananya Rao", "role": "Admin", "initials": "AR"}
USER_DOCTOR = {"name": "Dr. Meera Nair", "role": "Doctor", "initials": "MN"}
USER_NURSE = {"name": "Ritika Sen", "role": "Nurse", "initials": "RS"}
USER_RECEPTION = {"name": "Kavya Iyer", "role": "Receptionist", "initials": "KI"}
USER_INVENTORY = {"name": "Arjun Patel", "role": "Inventory manager", "initials": "AP"}


def sidebar(active_id: str, user: dict, attention: int = 0) -> str:
    groups = []
    for label, items in NAV:
        links = []
        for ic, name, target in items:
            cls = "nav-item active" if target == active_id else "nav-item"
            count = ""
            if target == "REM-001" and attention:
                count = f'<span class="nav-count">{attention}</span>'
            elif target == "SYS-001":
                count = '<span class="nav-count">2</span>'
            links.append(f'<a class="{cls}" href="{target}.html" title="{esc(name)}">{icon(ic, 17)}<span>{esc(name)}</span>{count}</a>')
        groups.append(f'<div class="nav-group"><div class="nav-label">{esc(label)}</div>{"".join(links)}</div>')
    return f'''<aside class="sidebar">
  <div class="brand"><div class="brand-mark">{icon("logo", 18)}</div><div class="brand-text"><div class="brand-name">Neo Child Clinic</div><div class="brand-sub">Desktop workspace</div></div></div>
  <div class="sidebar-scroll">{"".join(groups)}</div>
  <div class="sidebar-foot"><div class="sidebar-user">{avatar(user["name"])}<div><div class="sidebar-user-name">{esc(user["name"])}</div><div class="sidebar-user-role">{esc(user["role"])}</div></div><div class="sidebar-user-more">{icon("more", 15)}</div></div></div>
</aside>'''


def topbar(crumb: str, user: dict, status: str = "Online", status_tone: str = "", search: str = "Search patients, invoices, batches…") -> str:
    return f'''<header class="topbar">
  <div class="crumbs"><strong>{esc(crumb)}</strong></div>
  <div class="search-shell">{icon("search", 15)}<span>{esc(search)}</span><span class="kbd">⌘K</span></div>
  {status_pill(status, status_tone, "cloud" if status == "Online" else ("refresh" if status == "Syncing" else "wifi-off"))}
  <span class="demo-pill"><span class="status-dot" style="background:var(--apricot-500)"></span>Design preview · fictional data</span>
  {icon_btn("bell", "Notifications", dot=True)}
  {icon_btn("help", "Help and keyboard shortcuts")}
  <span class="vdivider"></span>
  <div class="user-chip">{avatar(user["name"])}<div><div class="user-chip-name">{esc(user["name"])}</div><div class="user-chip-role">{esc(user["role"])}</div></div>{icon("chevron-down", 12)}</div>
</header>'''


def page_head(eyebrow: str, title: str, subtitle: str = "", actions: str = "", meta: str = "") -> str:
    return f'''<div class="page-head"><div class="page-head-main"><div class="eyebrow">{esc(eyebrow)}</div><h1 class="page-title">{title}</h1>{f'<div class="page-sub">{subtitle}</div>' if subtitle else ''}{f'<div class="page-meta">{meta}</div>' if meta else ''}</div>{f'<div class="page-actions">{actions}</div>' if actions else ''}</div>'''


def shell_inner(active_id: str, crumb: str, user: dict, content: str, status: str = "Online", status_tone: str = "", attention: int = 0) -> str:
    return f'{sidebar(active_id, user, attention)}<div class="main">{topbar(crumb, user, status, status_tone)}<section class="workspace">{content}</section></div>'


def shell_page(active_id: str, crumb: str, user: dict, content: str, status: str = "Online", status_tone: str = "", attention: int = 0) -> str:
    return f'<div class="app">{shell_inner(active_id, crumb, user, content, status, status_tone, attention)}</div>'


def document(title: str, body: str, extra_css: str = "") -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Neo Child Clinic Desktop</title>
<link rel="stylesheet" href="../assets/app.css">
{extra_css}
</head>
<body>
{body}
<script src="../assets/prototype.js"></script>
</body>
</html>'''


def standalone(body: str, title: str) -> str:
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Neo Child Clinic Desktop</title>
<link rel="stylesheet" href="../assets/app.css">
</head>
<body>{body}<script src="../assets/prototype.js"></script></body>
</html>'''


def modal_overlay(base_content: str, active_id: str, crumb: str, user: dict, modal: str, status: str = "Online", status_tone: str = "", soft: bool = False) -> str:
    shell = shell_inner(active_id, crumb, user, base_content, status, status_tone)
    return f'<div class="app">{shell}<div class="scrim {"soft" if soft else ""}"></div>{modal}</div>'


def drawer_overlay(base_content: str, active_id: str, crumb: str, user: dict, drawer: str, status: str = "Online", status_tone: str = "", soft: bool = False) -> str:
    shell = shell_inner(active_id, crumb, user, base_content, status, status_tone)
    return f'<div class="app">{shell}<div class="scrim {"soft" if soft else ""}"></div>{drawer}</div>'
