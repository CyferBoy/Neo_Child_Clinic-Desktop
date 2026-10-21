#!/usr/bin/env python3
"""Prepare, validate and collect the screenshot review for this design package.

The review is deliberately split into small, isolated AI requests.  A request
must never contain more than ``MAX_IMAGES`` image parts, and a screen with
several screenshots consumes several slots.

Commands (run from anywhere)::

    python docs/UI_Design/review/review.py prepare
    python docs/UI_Design/review/review.py check
    python docs/UI_Design/review/review.py collect
    python docs/UI_Design/review/review.py status

``prepare`` performs the automated image checks (existence, readability,
dimensions, non-blank content), then writes:

* ``review_manifest.json`` and ``review_manifest.csv``
* ``batches/batch-NNN.json`` (every batch has at most 10 images)
* ``prompts/batch-NNN.md`` (file paths only; no embedded image data)

``collect`` merges the per-batch result files in ``results/`` into the
manifest and writes ``Screenshot-Review.md``.

This script never modifies a mockup, an HTML page or production code.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # docs/UI_Design
REVIEW = ROOT / "review"
SHOTS = ROOT / "screenshots"
SOURCE_MANIFEST = SHOTS / "manifest.json"
MANIFEST = REVIEW / "review_manifest.json"
MANIFEST_CSV = REVIEW / "review_manifest.csv"
BATCH_DIR = REVIEW / "batches"
PROMPT_DIR = REVIEW / "prompts"
RESULT_DIR = REVIEW / "results"
REQUEST_AUDIT = REVIEW / "request-audit.json"
REPORT = ROOT / "Screenshot-Review.md"
MAX_IMAGES = 10

# Pillow is installed in the isolated design tooling directory on this machine.
DEPS = Path("/data/data/com.termux/files/usr/tmp/opencode/uideps")
if DEPS.exists():
    sys.path.insert(0, str(DEPS))

EXPECTED_DIMENSIONS = {
    "base": (1366, 768),
    "dark": (1366, 768),
    "wide": (1920, 1080),
}

VERDICT_STATUS = {
    "pass": "reviewed_pass",
    "pass_with_notes": "reviewed_pass_with_notes",
    "fail": "reviewed_fail",
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_check(path: Path, kind: str) -> dict:
    """Check existence, readability, dimensions and that the image is not blank."""
    expected = EXPECTED_DIMENSIONS[kind]
    result = {
        "path": rel(path),
        "kind": kind,
        "exists": path.is_file(),
        "readable": False,
        "width": None,
        "height": None,
        "expected_width": expected[0],
        "expected_height": expected[1],
        "dimension_ok": False,
        "blank": None,
        "bytes": path.stat().st_size if path.is_file() else 0,
        "sha256": None,
        "error": None,
    }
    if not path.is_file():
        result["error"] = "file does not exist"
        return result
    if result["bytes"] == 0:
        result["error"] = "file is empty"
        return result

    try:
        from PIL import Image, ImageStat
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Pillow is required for image checks: {exc}")

    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            result["width"], result["height"] = image.size
            result["readable"] = True
            result["dimension_ok"] = image.size == expected
            rgb = image.convert("RGB")
            stat = ImageStat.Stat(rgb)
            # A completely blank PNG has a standard deviation of zero in all bands.
            result["blank"] = max(stat.stddev) < 0.5
        result["sha256"] = sha256(path)
    except Exception as exc:  # noqa: BLE001
        result["error"] = f"cannot read image: {exc}"
    return result


def load_json(path: Path, default=None):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}")


def bundle_sha(images: list[dict]) -> str:
    """Hash every screenshot in a screen bundle so any variant change resets review."""
    material = "|".join(
        f"{image.get('path')}:{image.get('sha256')}" for image in images
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def existing_reviews() -> dict:
    """Preserve prior review data only when every screenshot in the bundle is unchanged."""
    if not MANIFEST.exists():
        return {}
    data = load_json(MANIFEST, {})
    preserved = {}
    for screen in data.get("screens", []):
        screenshots = screen.get("screenshots", [])
        preserved[(screen.get("screen_id"), screen.get("screenshots", [{}])[0].get("path"))] = {
            "review_status": screen.get("review_status"),
            "verdict": screen.get("verdict"),
            "summary": screen.get("summary"),
            "issues": screen.get("issues", []),
            "reviewed_at": screen.get("reviewed_at"),
            "bundle_sha256": screen.get("bundle_sha256") or bundle_sha(screenshots),
        }
    return preserved


def spec_for(screen_id: str) -> str | None:
    matches = sorted((ROOT / "Screens").glob(f"{screen_id}-*.md"))
    return rel(matches[0]) if matches else None


def build_screens(previous: dict) -> tuple[list[dict], list[str]]:
    source = load_json(SOURCE_MANIFEST, None)
    if not isinstance(source, list):
        raise SystemExit(f"missing or invalid source manifest: {SOURCE_MANIFEST}")

    screens = []
    errors = []
    for item in source:
        screen_id = item["id"]
        shots = [("base", item["png"])]
        if item.get("dark"):
            shots.append(("dark", item["dark"]))
        if item.get("wide"):
            shots.append(("wide", item["wide"]))

        checked = []
        for kind, relative in shots:
            path = ROOT / relative
            check = image_check(path, kind)
            if not check["exists"]:
                errors.append(f"{screen_id}: missing {relative}")
            elif check["error"]:
                errors.append(f"{screen_id}: {relative}: {check['error']}")
            elif not check["dimension_ok"]:
                errors.append(
                    f"{screen_id}: {relative}: expected "
                    f"{check['expected_width']}x{check['expected_height']}, "
                    f"got {check['width']}x{check['height']}"
                )
            elif check["blank"]:
                errors.append(f"{screen_id}: {relative}: image appears blank")
            checked.append(check)

        prior = previous.get((screen_id, item["png"]))
        bundle = bundle_sha(checked)
        status = "pending"
        verdict = None
        summary = None
        issues = []
        reviewed_at = None
        if prior and prior.get("bundle_sha256") == bundle:
            status = prior.get("review_status") or "pending"
            verdict = prior.get("verdict")
            summary = prior.get("summary")
            issues = prior.get("issues") or []
            reviewed_at = prior.get("reviewed_at")

        screens.append(
            {
                "screen_id": screen_id,
                "name": item.get("name", ""),
                "section": item.get("section", ""),
                "feature": item.get("feature", ""),
                "spec": spec_for(screen_id),
                "html": item.get("html"),
                "screenshots": checked,
                "bundle_sha256": bundle,
                "review_status": status,
                "verdict": verdict,
                "summary": summary,
                "issues": issues,
                "batch_id": None,
                "reviewed_at": reviewed_at,
            }
        )
    return screens, errors


def build_batches(screens: list[dict]) -> list[dict]:
    """Pack whole screens into batches without splitting their screenshot bundle."""
    batches = []
    current: list[dict] = []
    current_count = 0

    def flush() -> None:
        nonlocal current, current_count
        if not current:
            return
        batch_id = f"batch-{len(batches) + 1:03d}"
        images = []
        for screen in current:
            for image in screen["screenshots"]:
                images.append(
                    {
                        "screen_id": screen["screen_id"],
                        "screen_name": screen["name"],
                        "path": image["path"],
                        "kind": image["kind"],
                        "width": image["width"],
                        "height": image["height"],
                        "sha256": image["sha256"],
                    }
                )
            screen["batch_id"] = batch_id
        batches.append(
            {
                "batch_id": batch_id,
                "image_count": current_count,
                "max_images": MAX_IMAGES,
                "screen_ids": [screen["screen_id"] for screen in current],
                "images": images,
                "prompt": f"review/prompts/{batch_id}.md",
                "result": f"review/results/{batch_id}.json",
                "status": "complete" if (RESULT_DIR / f"{batch_id}.json").exists() else "pending",
            }
        )
        current = []
        current_count = 0

    for screen in screens:
        count = len(screen["screenshots"])
        if count > MAX_IMAGES:
            raise SystemExit(
                f"{screen['screen_id']} needs {count} screenshots, "
                f"which exceeds the {MAX_IMAGES}-image request limit"
            )
        if current and current_count + count > MAX_IMAGES:
            flush()
        current.append(screen)
        current_count += count
    flush()
    return batches


def prompt_text(batch: dict) -> str:
    lines = [
        f"# Screenshot review — {batch['batch_id']}",
        "",
        "Review the rendered Neo Child Clinic Desktop screenshots in this batch.",
        "This is a design-package review only. Do not edit mockups, HTML, specs or",
        "production code.",
        "",
        "## Hard request limits",
        "",
        f"- This batch contains exactly **{batch['image_count']} images** (limit {MAX_IMAGES}).",
        "- Read every assigned image in **one assistant turn** using parallel `read`",
        "  calls. Do not read any other image before or after that turn.",
        "- Do not open a different batch. Do not paste images into your reply. The",
        "  batch JSON contains paths only; it contains no image data.",
        "- Use a fresh session for this batch. Never review a second batch in the",
        "  same conversation, because earlier images remain attached to later requests.",
        "",
        "## Inputs",
        "",
        "All paths below are relative to the repository root.",
        "",
        f"- Batch JSON: `docs/UI_Design/review/batches/{batch['batch_id']}.json`",
        "  (paths inside that JSON are relative to `docs/UI_Design/`)",
        f"- Result file to create: `docs/UI_Design/review/results/{batch['batch_id']}.json`",
        "",
        "Images (read these exact paths):",
        "",
    ]
    for image in batch["images"]:
        lines.append(
            f"- `docs/UI_Design/{image['path']}` — {image['screen_id']} ({image['kind']})"
        )
    lines += [
        "",
        "Automated checks already passed for every path above: the file exists,",
        "is readable, is not blank, and has the expected dimensions. If you cannot",
        "read an image, record that as a `fail` issue instead of guessing.",
        "",
        "## Review criteria",
        "",
        "For each screen, check:",
        "",
        "1. The image is a complete viewport, not cropped, blank or a browser error.",
        "2. No overlapping, clipped or off-screen text, controls or table columns.",
        "3. Typography is legible at 1366×768 (or the stated wide size).",
        "4. The shell, navigation, spacing, colours and component variants are",
        "   consistent with the design package.",
        "5. Tables, forms, dialogs and empty/error states look purposeful and do not",
        "   show `undefined`, `NaN`, raw template markers or obviously broken data.",
        "6. Any visible patient data is fictional; no real personal or clinical data.",
        "",
        "Use `pass` when the screen is fit for design review. Use",
        "`pass_with_notes` for cosmetic or non-blocking issues. Use `fail` for a",
        "blocking visual defect (unreadable content, missing core region, severe",
        "clipping, or an image that is not the intended screen).",
        "",
        "## Required output",
        "",
        "Write valid JSON only to the result path. Do not wrap it in Markdown fences.",
        "Use this shape:",
        "",
        "```json",
        "{",
        f'  "batch_id": "{batch["batch_id"]}",',
        f'  "images_reviewed": {batch["image_count"]},',
        '  "reviewed_at": "ISO-8601 timestamp",',
        '  "notes": "one or two sentences about the batch as a whole",',
        '  "screens": [',
        "    {",
        '      "screen_id": "AUTH-001",',
        '      "verdict": "pass",',
        '      "summary": "Concise finding for this screen.",',
        '      "issues": [',
        '        {"image": "screenshots/AUTH-001.png", "severity": "minor", "observation": "..."}',
        "      ]",
        "    }",
        "  ]",
        "}",
        "```",
        "",
        f"Include every one of these screen IDs exactly once: {', '.join(batch['screen_ids'])}.",
        "",
        "Keep each summary under 40 words. Do not include base64 or image data in the",
        "result. Finish after writing the result file.",
        "",
    ]
    return "\n".join(lines)


def write_manifest(screens: list[dict], batches: list[dict]) -> dict:
    counts = {"reviewed_pass": 0, "reviewed_pass_with_notes": 0, "reviewed_fail": 0,
              "pending": 0, "unreviewed": 0, "blocked_automated_checks": 0}
    for screen in screens:
        counts[screen["review_status"]] = counts.get(screen["review_status"], 0) + 1
    data = {
        "schema_version": 1,
        "generated_at": now(),
        "package": "Neo Child Clinic Desktop UI/UX design package",
        "max_images_per_request": MAX_IMAGES,
        "policy": (
            "One fresh AI session per batch. A screen's variants stay in the same "
            "batch and every image counts toward the limit."
        ),
        "totals": {
            "screens": len(screens),
            "screenshots": sum(len(s["screenshots"]) for s in screens),
            "batches": len(batches),
            "reviewed": counts["reviewed_pass"] + counts["reviewed_pass_with_notes"] + counts["reviewed_fail"],
            "pending": counts["pending"],
            "unreviewed": counts["unreviewed"],
            "failed": counts["reviewed_fail"],
        },
        "status_counts": counts,
        "screens": screens,
        "batches": batches,
    }
    REVIEW.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    write_csv(screens)
    return data


def write_csv(screens: list[dict]) -> None:
    fields = [
        "screen_id", "name", "section", "spec", "html", "base_png", "dark_png",
        "wide_png", "review_status", "verdict", "batch_id", "summary",
    ]
    with MANIFEST_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for screen in screens:
            by_kind = {image["kind"]: image["path"] for image in screen["screenshots"]}
            writer.writerow(
                {
                    "screen_id": screen["screen_id"],
                    "name": screen["name"],
                    "section": screen["section"],
                    "spec": screen["spec"] or "",
                    "html": screen["html"] or "",
                    "base_png": by_kind.get("base", ""),
                    "dark_png": by_kind.get("dark", ""),
                    "wide_png": by_kind.get("wide", ""),
                    "review_status": screen["review_status"],
                    "verdict": screen["verdict"] or "",
                    "batch_id": screen["batch_id"] or "",
                    "summary": screen["summary"] or "",
                }
            )


def write_batches(batches: list[dict]) -> None:
    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)
    for old in list(BATCH_DIR.glob("batch-*.json")) + list(PROMPT_DIR.glob("batch-*.md")):
        old.unlink()
    for batch in batches:
        (BATCH_DIR / f"{batch['batch_id']}.json").write_text(
            json.dumps(batch, indent=2) + "\n", encoding="utf-8"
        )
        (PROMPT_DIR / f"{batch['batch_id']}.md").write_text(
            prompt_text(batch), encoding="utf-8"
        )


def print_checks(data: dict, batches: list[dict], screens: list[dict], errors: list[str]) -> None:
    print(f"Screens: {len(screens)}")
    print(f"Screenshots: {sum(len(s['screenshots']) for s in screens)}")
    print(f"Batches: {len(batches)}")
    print(f"Largest batch: {max((b['image_count'] for b in batches), default=0)} images")
    print(f"Limit per request: {MAX_IMAGES}")
    if errors:
        print(f"FAIL: {len(errors)} automated image issue(s)")
        for error in errors[:40]:
            print(f"  - {error}")
    else:
        print("PASS: every screenshot exists, is readable, is not blank and has the expected dimensions.")


def command_prepare(_args) -> int:
    previous = existing_reviews()
    screens, errors = build_screens(previous)
    if errors:
        write_manifest(screens, [])
        print_checks({}, [], screens, errors)
        print("No batches were written because the automated image checks failed.")
        return 1
    batches = build_batches(screens)
    data = write_manifest(screens, batches)
    write_batches(batches)
    print_checks(data, batches, screens, errors)
    print(f"Wrote {rel(MANIFEST)} and {len(batches)} batch file(s).")
    return 0


def command_check(_args) -> int:
    data = load_json(MANIFEST, None)
    if not isinstance(data, dict):
        print("FAIL: review_manifest.json is missing; run `prepare` first.")
        return 1
    screens = data.get("screens", [])
    batches = data.get("batches", [])
    errors: list[str] = []

    if data.get("max_images_per_request") != MAX_IMAGES:
        errors.append(f"manifest max_images_per_request is not {MAX_IMAGES}")

    seen_paths: set[str] = set()
    seen_screens: set[str] = set()
    for batch in batches:
        images = batch.get("images", [])
        count = len(images)
        if count > MAX_IMAGES:
            errors.append(f"{batch.get('batch_id')}: {count} images exceeds {MAX_IMAGES}")
        if batch.get("image_count") != count:
            errors.append(f"{batch.get('batch_id')}: image_count does not match images")
        ids = [image.get("screen_id") for image in images]
        if set(ids) != set(batch.get("screen_ids", [])):
            errors.append(f"{batch.get('batch_id')}: screen_ids do not match images")
        manifest_screens = {screen["screen_id"]: screen for screen in screens}
        for screen_id in batch.get("screen_ids", []):
            expected = {
                image["path"]
                for image in manifest_screens.get(screen_id, {}).get("screenshots", [])
            }
            actual = {
                image["path"] for image in images if image.get("screen_id") == screen_id
            }
            if actual != expected:
                errors.append(
                    f"{batch.get('batch_id')}: variants for {screen_id} are split or incomplete"
                )
        prompt_path = ROOT / batch.get("prompt", "")
        if not prompt_path.is_file():
            errors.append(f"{batch.get('batch_id')}: prompt file is missing")
        else:
            prompt = prompt_path.read_text(encoding="utf-8")
            if "data:image" in prompt:
                errors.append(f"{batch.get('batch_id')}: prompt embeds image data")
            prompt_paths = set(re.findall(r"docs/UI_Design/(screenshots/[^\s`]+\.png)", prompt))
            if prompt_paths != {image["path"] for image in images}:
                errors.append(f"{batch.get('batch_id')}: prompt image list does not match batch")
            expected_line = f"This batch contains exactly **{count} images**"
            if expected_line not in prompt:
                errors.append(f"{batch.get('batch_id')}: prompt does not state the image count")
        for image in images:
            path = image.get("path")
            if path in seen_paths:
                errors.append(f"duplicate screenshot in batches: {path}")
            seen_paths.add(path)
            if not (ROOT / path).is_file():
                errors.append(f"{batch.get('batch_id')}: missing {path}")
            check = image_check(ROOT / path, image.get("kind", "base"))
            if not check["readable"]:
                errors.append(f"{batch.get('batch_id')}: unreadable {path}")
            elif not check["dimension_ok"]:
                errors.append(f"{batch.get('batch_id')}: wrong dimensions for {path}")
            elif check["blank"]:
                errors.append(f"{batch.get('batch_id')}: blank image {path}")
        for screen_id in batch.get("screen_ids", []):
            if screen_id in seen_screens:
                errors.append(f"screen split across batches: {screen_id}")
            seen_screens.add(screen_id)

    manifest_paths = {
        image["path"]
        for screen in screens
        for image in screen.get("screenshots", [])
    }
    if seen_paths != manifest_paths:
        missing = sorted(manifest_paths - seen_paths)
        extra = sorted(seen_paths - manifest_paths)
        if missing:
            errors.append(f"batches miss {len(missing)} screenshot(s): {missing[:5]}")
        if extra:
            errors.append(f"batches contain {len(extra)} unknown screenshot(s): {extra[:5]}")
    if len(screens) != 68:
        errors.append(f"expected 68 screens, found {len(screens)}")
    if len(seen_screens) != len(screens):
        errors.append(f"batches cover {len(seen_screens)} screens, manifest has {len(screens)}")

    # Result files must also respect the limit and correspond to a real batch.
    batch_ids = {batch["batch_id"]: batch for batch in batches}
    for result_path in sorted(RESULT_DIR.glob("batch-*.json")):
        result = load_json(result_path, {})
        if result.get("images_reviewed", 0) > MAX_IMAGES:
            errors.append(f"{result_path.name}: images_reviewed exceeds {MAX_IMAGES}")
        if result.get("batch_id") not in batch_ids:
            errors.append(f"{result_path.name}: unknown batch_id")
        else:
            expected = batch_ids[result["batch_id"]]["image_count"]
            if result.get("images_reviewed") != expected:
                errors.append(
                    f"{result_path.name}: images_reviewed is "
                    f"{result.get('images_reviewed')}, expected {expected}"
                )

    # Optional runtime audit of the isolated reviewer sessions.
    audit = load_json(REQUEST_AUDIT, None)
    if isinstance(audit, dict):
        if audit.get("max_allowed") != MAX_IMAGES:
            errors.append("request audit max_allowed is not 10")
        if audit.get("max_observed", 0) > MAX_IMAGES:
            errors.append("request audit max_observed exceeds 10")
        audited = {item.get("batch_id") for item in audit.get("sessions", [])}
        if audited != set(batch_ids):
            errors.append("request audit does not cover every batch exactly once")
        for item in audit.get("sessions", []):
            if item.get("max_images_in_request", 0) > MAX_IMAGES:
                errors.append(f"{item.get('batch_id')}: audited request exceeds 10 images")
            if item.get("images_total", 0) > MAX_IMAGES:
                errors.append(f"{item.get('batch_id')}: audited total exceeds 10 images")

    print(f"Screens: {len(screens)}")
    print(f"Screenshots: {len(manifest_paths)}")
    print(f"Batches: {len(batches)}")
    print(f"Largest batch: {max((len(b.get('images', [])) for b in batches), default=0)} images")
    print(f"Limit per request: {MAX_IMAGES}")
    if errors:
        print(f"FAIL: {len(errors)} issue(s)")
        for error in errors[:60]:
            print(f"  - {error}")
        return 1
    print("PASS: every batch is <= 10 images, every screenshot is covered, and no screen is split.")
    return 0


def normalize_result(result: dict, batch: dict) -> tuple[dict, list[str]]:
    errors = []
    if result.get("batch_id") != batch["batch_id"]:
        errors.append("batch_id does not match")
    if result.get("images_reviewed") != batch["image_count"]:
        errors.append(
            f"images_reviewed is {result.get('images_reviewed')}, expected {batch['image_count']}"
        )
    screens = result.get("screens")
    if not isinstance(screens, list):
        errors.append("missing screens array")
        return {}, errors
    by_id = {}
    for item in screens:
        if not isinstance(item, dict):
            errors.append("screen entry is not an object")
            continue
        screen_id = item.get("screen_id")
        if screen_id not in batch["screen_ids"]:
            errors.append(f"unexpected screen {screen_id}")
            continue
        if screen_id in by_id:
            errors.append(f"duplicate screen {screen_id}")
            continue
        verdict = item.get("verdict")
        if verdict not in VERDICT_STATUS:
            errors.append(f"{screen_id}: invalid verdict {verdict!r}")
            continue
        by_id[screen_id] = {
            "verdict": verdict,
            "summary": str(item.get("summary") or "").strip(),
            "issues": item.get("issues") if isinstance(item.get("issues"), list) else [],
        }
    return by_id, errors


def command_collect(_args) -> int:
    data = load_json(MANIFEST, None)
    if not isinstance(data, dict):
        print("FAIL: review_manifest.json is missing; run `prepare` first.")
        return 1
    screens = data["screens"]
    batches = data["batches"]
    screen_by_id = {screen["screen_id"]: screen for screen in screens}
    collect_errors = []
    batch_status = {}

    for batch in batches:
        result_path = RESULT_DIR / f"{batch['batch_id']}.json"
        for screen_id in batch["screen_ids"]:
            screen = screen_by_id[screen_id]
            screen["review_status"] = "unreviewed"
            screen["verdict"] = None
            screen["summary"] = None
            screen["issues"] = []
            screen["reviewed_at"] = None
        if not result_path.exists():
            batch["status"] = "no_result"
            batch_status[batch["batch_id"]] = "no_result"
            continue
        result = load_json(result_path, {})
        by_id, errors = normalize_result(result, batch)
        if errors:
            collect_errors.extend(f"{batch['batch_id']}: {error}" for error in errors)
            batch["status"] = "invalid_result"
            batch_status[batch["batch_id"]] = "invalid_result"
            continue
        missing = [sid for sid in batch["screen_ids"] if sid not in by_id]
        if missing:
            collect_errors.append(f"{batch['batch_id']}: no result for {', '.join(missing)}")
            batch["status"] = "partial"
            batch_status[batch["batch_id"]] = "partial"
        else:
            batch["status"] = "complete"
            batch_status[batch["batch_id"]] = "complete"
        for screen_id, review in by_id.items():
            screen = screen_by_id[screen_id]
            screen["review_status"] = VERDICT_STATUS[review["verdict"]]
            screen["verdict"] = review["verdict"]
            screen["summary"] = review["summary"]
            screen["issues"] = review["issues"]
            screen["reviewed_at"] = result.get("reviewed_at") or now()

    total = len(screens)
    pass_count = sum(1 for s in screens if s["review_status"] == "reviewed_pass")
    note_count = sum(1 for s in screens if s["review_status"] == "reviewed_pass_with_notes")
    fail_count = sum(1 for s in screens if s["review_status"] == "reviewed_fail")
    unreviewed = total - pass_count - note_count - fail_count
    data["generated_at"] = now()
    data["totals"] = {
        "screens": total,
        "screenshots": sum(len(s["screenshots"]) for s in screens),
        "batches": len(batches),
        "reviewed": pass_count + note_count + fail_count,
        "pending": 0,
        "unreviewed": unreviewed,
        "failed": fail_count,
    }
    data["status_counts"] = {
        "reviewed_pass": pass_count,
        "reviewed_pass_with_notes": note_count,
        "reviewed_fail": fail_count,
        "pending": 0,
        "unreviewed": unreviewed,
        "blocked_automated_checks": 0,
    }
    MANIFEST.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    write_csv(screens)
    write_report(data, screens, batches, batch_status, collect_errors)
    print(f"Reviewed: {pass_count + note_count + fail_count}/{total}")
    print(f"  pass: {pass_count}")
    print(f"  pass_with_notes: {note_count}")
    print(f"  fail: {fail_count}")
    print(f"  unreviewed: {unreviewed}")
    print(f"Largest batch: {max((b['image_count'] for b in batches), default=0)} images")
    if collect_errors:
        print(f"WARN: {len(collect_errors)} batch/result issue(s)")
        for error in collect_errors[:40]:
            print(f"  - {error}")
    return 0 if not collect_errors else 1


def write_report(data: dict, screens: list[dict], batches: list[dict],
                 batch_status: dict, collect_errors: list[str]) -> None:
    totals = data["totals"]
    max_batch = max((b["image_count"] for b in batches), default=0)
    lines = [
        "# Screenshot Review",
        "",
        "**Scope:** design-package verification only. No mockup, HTML page, production",
        "application file or database object was regenerated or modified.",
        "",
        "## Result",
        "",
        f"- Screens: **{totals['screens']}**",
        f"- Screenshots: **{totals['screenshots']}** (base + dark/wide variants)",
        f"- Batches: **{totals['batches']}** (largest batch **{max_batch}** images)",
        f"- Reviewed: **{totals['reviewed']}** of **{totals['screens']}** screens",
        f"- Failed review: **{totals['failed']}**",
        f"- Unreviewed: **{totals['unreviewed']}**",
        "",
        "Every batch was limited to 10 images. A screen with dark or wide variants",
        "occupies multiple slots in its batch, and the variants are never split from",
        "the base screen.",
        "",
        "## Batch results",
        "",
        "| Batch | Images | Screens | Status |",
        "|---|---:|---:|---|",
    ]
    for batch in batches:
        lines.append(
            f"| `{batch['batch_id']}` | {batch['image_count']} | "
            f"{len(batch['screen_ids'])} | {batch_status.get(batch['batch_id'], 'pending')} |"
        )
    lines += [
        "",
        "## Screens needing attention",
        "",
    ]
    attention = [s for s in screens if s["review_status"] in ("reviewed_fail", "reviewed_pass_with_notes")]
    if attention:
        lines += ["| Screen | Status | Summary |", "|---|---|---|"]
        for screen in attention:
            summary = (screen.get("summary") or "").replace("|", "\\|")
            lines.append(f"| `{screen['screen_id']}` | {screen['review_status']} | {summary} |")
    else:
        lines.append("None. Every reviewed screen passed without notes.")

    lines += ["", "## Unreviewed screens", ""]
    missing = [s for s in screens if s["review_status"] in ("unreviewed", "pending")]
    if missing:
        lines += ["| Screen | Screenshot(s) | Batch |", "|---|---|---|"]
        for screen in missing:
            paths = ", ".join(f"`{image['path']}`" for image in screen["screenshots"])
            lines.append(f"| `{screen['screen_id']}` | {paths} | `{screen['batch_id']}` |")
    else:
        lines.append("None. Every screen has a review result.")

    lines += [
        "",
        "## Method and safeguards",
        "",
        "1. `review/review.py prepare` checked every PNG for existence, non-zero size,",
        "   readability, non-blank content and expected dimensions before any visual",
        "   review was requested.",
        "2. Screens were packed into batches of at most 10 images. All variants of one",
        "   screen stay in the same batch and count toward that batch's limit.",
        "3. Each batch was reviewed in a fresh AI session with only that batch's image",
        "   paths. No batch inherited earlier images, and concise per-screen summaries",
        "   plus the manifest carried context between batches.",
        "4. The batch prompts contain file paths only; they do not embed image data.",
        "5. Failed or missing batch results stay `unreviewed` and are listed above.",
        "",
    ]
    audit = load_json(REQUEST_AUDIT, None)
    if isinstance(audit, dict):
        lines += [
            "## Request-size audit",
            "",
            "Observed image parts in each isolated reviewer session. The count is the",
            "maximum number of image parts present in a model request in that session.",
            "",
            "| Batch | Reviewer session | Images | Max in request |",
            "|---|---|---:|---:|",
        ]
        for item in audit.get("sessions", []):
            lines.append(
                f"| `{item['batch_id']}` | `{item['session_id']}` | "
                f"{item['images_total']} | {item['max_images_in_request']} |"
            )
        lines += [
            "",
            f"Maximum observed: **{audit.get('max_observed')} / {audit.get('max_allowed', MAX_IMAGES)}**.",
            f"Violations: **{len(audit.get('violations', []))}**.",
            "",
        ]
    lines += [
        "## Validation",
        "",
        f"- `python docs/UI_Design/review/review.py check` must pass.",
        f"- Maximum images in any batch: **{max_batch} / 10**.",
        f"- Screenshot coverage: **{totals['screenshots']}** images across "
        f"**{totals['screens']}** screens.",
        "",
    ]
    if collect_errors:
        lines += ["### Collection warnings", ""]
        lines += [f"- {error}" for error in collect_errors]
        lines.append("")
    REPORT.write_text("\n".join(lines), encoding="utf-8")


def command_status(_args) -> int:
    data = load_json(MANIFEST, None)
    if not isinstance(data, dict):
        print("No review manifest yet. Run `prepare`.")
        return 1
    print(json.dumps({"totals": data.get("totals"), "status_counts": data.get("status_counts")}, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "check", "collect", "status"])
    args = parser.parse_args()
    return {
        "prepare": command_prepare,
        "check": command_check,
        "collect": command_collect,
        "status": command_status,
    }[args.command](args)


if __name__ == "__main__":
    raise SystemExit(main())
