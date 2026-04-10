#!/usr/bin/env python3
"""
CNCF landscape.yml data integrity audit (local vendored copy only).

Reads datasources/landscape.yml and writes reports under
audit/landscape_data_integrity_audit/.

Reports (1) required lifecycle dates under extra: and (2) presence of fields that
can be filled or cross-checked from other files in datasources/ (PCC, CLOMonitor,
devstats.html, artwork.md).
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml  # type: ignore
except Exception:
    print("Missing dependency: PyYAML. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIT_ROOT = os.path.dirname(SCRIPT_DIR)
LANDSCAPE_PATH = os.path.join(AUDIT_ROOT, "datasources", "landscape.yml")
OUTPUT_DIR = os.path.join(AUDIT_ROOT, "audit", "landscape_data_integrity_audit")

SCOPE_MATURITIES = frozenset({"sandbox", "incubating", "graduated", "archived"})

# Markdown report: one table per maturity, top to bottom.
REPORT_SECTION_ORDER = ("graduated", "incubating", "sandbox", "archived")

# Generic CNCF landscape placeholder (hosted logo filename).
CNCF_PLACEHOLDER_LOGO_BASENAMES = frozenset({"cncf.svg"})


# (field_key in row["fields"], short column header, datasource hint for the legend)
FIXABLE_FIELDS: Tuple[Tuple[str, str, str], ...] = (
    ("extra.lfx_slug", "slug", "`pcc_projects.yaml` → `slug`"),
    ("repo_url", "repo", "`pcc_projects.yaml` → `repository_url`"),
    ("logo", "logo", "`pcc_projects.yaml` → `project_logo` (filename vs placeholder)"),
    ("extra.dev_stats_url", "devstats", "`clomonitor.yaml` → `devstats_url`; `devstats.html`"),
    ("extra.clomonitor_name", "clomon", "`clomonitor.yaml` → project `name`"),
    ("extra.accepted", "accepted", "`clomonitor.yaml` → `accepted_at`"),
    ("extra.artwork_url", "artwork", "`clomonitor.yaml` → `logo_url`; `artwork.md`"),
)


def present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, dict):
        return bool(value)
    if isinstance(value, list):
        return bool(value)
    if isinstance(value, bool):
        return True
    return str(value).strip() != ""


def logo_audit_value(item: Dict[str, Any]) -> str:
    """
    Item-level `logo` (hosted filename). Returns:
    - "Yes" — non-empty and not the CNCF placeholder asset
    - "cncf logo" — basename matches generic CNCF placeholder (e.g. cncf.svg)
    - "No" — missing or empty
    """
    raw = item.get("logo")
    if not present(raw):
        return "No"
    base = os.path.basename(str(raw).strip()).lower()
    if base in CNCF_PLACEHOLDER_LOGO_BASENAMES:
        return "cncf logo"
    return "Yes"


def get_extra(item: Dict[str, Any]) -> Dict[str, Any]:
    ex = item.get("extra")
    return ex if isinstance(ex, dict) else {}


def effective_project(item: Dict[str, Any]) -> str:
    extra = get_extra(item)
    p = extra.get("project")
    if p is None or (isinstance(p, str) and not p.strip()):
        p = item.get("project")
    if p is None:
        return ""
    return str(p).strip().lower()


def evaluate_lifecycle_dates(eff: str, extra: Dict[str, Any]) -> Tuple[str, str, List[str]]:
    """
    Returns (dates_ok, dates_detail, missing_keys).
    dates_ok: pass | fail | n/a
    """
    if eff not in SCOPE_MATURITIES:
        return "n/a", "out_of_scope", []

    def has(k: str) -> bool:
        return present(extra.get(k))

    if eff == "sandbox":
        required = ("accepted",)
    elif eff == "incubating":
        required = ("accepted", "incubating")
    elif eff == "graduated":
        required = ("accepted", "incubating", "graduated")
    else:  # archived
        required = ("accepted", "archived")

    missing = [k for k in required if not has(k)]
    if not missing:
        return "pass", "ok", []
    return "fail", "missing:" + ",".join(missing), missing


def _category_name(cat_entry: Dict[str, Any]) -> str:
    """Support nested `category: { name: ... }` and flat `category: null` + `name: ...`."""
    cat = cat_entry.get("category")
    if isinstance(cat, dict):
        n = str(cat.get("name") or "").strip()
        if n:
            return n
    if isinstance(cat, str) and cat.strip():
        return cat.strip()
    return str(cat_entry.get("name") or "").strip()


def _subcategory_name(sub_entry: Dict[str, Any]) -> str:
    sub = sub_entry.get("subcategory")
    if isinstance(sub, dict):
        n = str(sub.get("name") or "").strip()
        if n:
            return n
    if isinstance(sub, str) and sub.strip():
        return sub.strip()
    return str(sub_entry.get("name") or "").strip()


def _normalize_item_dict(it_wrap: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Landscape YAML may nest fields under `item:` or flatten them when `item` is null
    (PyYAML merges following keys onto the parent mapping).
    """
    inner = it_wrap.get("item")
    if isinstance(inner, dict):
        return inner
    # Flattened shape: `item:` null + name, project, extra, ... as siblings of `item`
    if inner is None:
        keys_skip = frozenset({"item"})
        if any(k not in keys_skip and it_wrap.get(k) is not None for k in it_wrap):
            return {k: v for k, v in it_wrap.items() if k not in keys_skip}
    return None


def iter_landscape_items(doc: Dict[str, Any]) -> List[Tuple[str, str, Dict[str, Any]]]:
    """Yield (category_name, subcategory_name, item_dict)."""
    out: List[Tuple[str, str, Dict[str, Any]]] = []
    root = doc.get("landscape")
    if root is None:
        root = doc.get("categories")
    if not isinstance(root, list):
        return out

    for cat_entry in root:
        if not isinstance(cat_entry, dict):
            continue
        cat_name = _category_name(cat_entry)
        subs = None
        cat = cat_entry.get("category")
        if isinstance(cat, dict):
            subs = cat.get("subcategories")
        if subs is None:
            subs = cat_entry.get("subcategories")
        if not isinstance(subs, list):
            continue

        for sub_entry in subs:
            if not isinstance(sub_entry, dict):
                continue
            sub_name = _subcategory_name(sub_entry)
            items = None
            sub = sub_entry.get("subcategory")
            if isinstance(sub, dict):
                items = sub.get("items")
            if items is None:
                items = sub_entry.get("items")
            if not isinstance(items, list):
                continue

            for it_wrap in items:
                if not isinstance(it_wrap, dict):
                    continue
                item = _normalize_item_dict(it_wrap)
                if not item:
                    continue
                out.append((cat_name, sub_name, item))
    return out


def yn(p: bool) -> str:
    return "Yes" if p else "No"


def build_rows(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for cat_name, sub_name, item in iter_landscape_items(doc):
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        eff = effective_project(item)
        if eff not in SCOPE_MATURITIES:
            continue

        extra = get_extra(item)
        dates_ok, dates_detail, missing_dates = evaluate_lifecycle_dates(eff, extra)
        path = f"{cat_name} / {sub_name}" if cat_name or sub_name else ""

        row: Dict[str, Any] = {
            "name": name,
            "path": path,
            "effective_project": eff,
            "dates_ok": dates_ok,
            "dates_detail": dates_detail,
            "missing_required_dates": missing_dates,
            "fields": {},
        }

        f = row["fields"]
        f["repo_url"] = present(item.get("repo_url"))
        f["logo"] = logo_audit_value(item)
        f["extra.lfx_slug"] = present(extra.get("lfx_slug"))
        f["extra.dev_stats_url"] = present(extra.get("dev_stats_url"))
        f["extra.clomonitor_name"] = present(extra.get("clomonitor_name"))
        f["extra.accepted"] = present(extra.get("accepted"))
        f["extra.artwork_url"] = present(extra.get("artwork_url"))

        rows.append(row)

    rows.sort(key=lambda r: (r["effective_project"], r["name"].lower()))
    return rows


def render_markdown(rows: List[Dict[str, Any]]) -> str:
    lines: List[str] = []
    lines.append("# Landscape data integrity audit")
    lines.append("")
    lines.append("Source: vendored `datasources/landscape.yml` in this repository.")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append(
        "CNCF items with `project` (or `extra.project`) in: "
        + ", ".join(sorted(SCOPE_MATURITIES))
        + "."
    )
    lines.append("")
    lines.append("## Lifecycle date rules")
    lines.append("")
    lines.append("| Maturity | Required `extra` date fields |")
    lines.append("|----------|-------------------------------|")
    lines.append("| sandbox | `accepted` |")
    lines.append("| incubating | `accepted`, `incubating` |")
    lines.append("| graduated | `accepted`, `incubating`, `graduated` |")
    lines.append("| archived | `accepted`, `archived` |")
    lines.append("")
    lines.append("## Legend")
    lines.append("")
    lines.append("- **dates_ok** / **dates_detail**: required lifecycle date keys under `extra:` for this maturity.")
    lines.append("- **Yes** / **No** (most columns): that landscape field is non-empty.")
    lines.append(
        "- **logo**: **Yes** = `logo:` set to a project asset (not the CNCF placeholder); "
        "**cncf logo** = generic `cncf.svg`; **No** = missing/empty."
    )
    lines.append("- **Datasource hints** (where we can source fixes later):")
    for _fk, short, hint in FIXABLE_FIELDS:
        lines.append(f"  - **{short}**: {hint}")
    lines.append("")
    lines.append(f"**Projects in scope:** {len(rows)}")
    lines.append("")

    fail_count = sum(1 for r in rows if r["dates_ok"] == "fail")
    lines.append(f"**Lifecycle date failures:** {fail_count}")
    lines.append("")

    section_headers = ["Project", "Path", "dates_ok", "dates_detail"] + [short for _fk, short, _h in FIXABLE_FIELDS]

    by_maturity: Dict[str, List[Dict[str, Any]]] = {m: [] for m in REPORT_SECTION_ORDER}
    for r in rows:
        m = r["effective_project"]
        if m in by_maturity:
            by_maturity[m].append(r)
    for m in REPORT_SECTION_ORDER:
        by_maturity[m].sort(key=lambda x: x["name"].lower())

    lines.append("## Matrix (by maturity)")
    lines.append("")
    for maturity in REPORT_SECTION_ORDER:
        sec_rows = by_maturity[maturity]
        title = maturity.capitalize()
        lines.append(f"### {title}")
        lines.append("")
        lines.append(f"**Count:** {len(sec_rows)}")
        lines.append("")
        if not sec_rows:
            lines.append("_No projects._")
            lines.append("")
            continue
        lines.append("| " + " | ".join(section_headers) + " |")
        lines.append("|" + "|".join(["---"] * len(section_headers)) + "|")
        for r in sec_rows:
            fld = r["fields"]
            cells = [r["name"], r["path"] or "-", r["dates_ok"], r["dates_detail"]]
            for fk, _short, _h in FIXABLE_FIELDS:
                if fk == "logo":
                    cells.append(fld[fk])
                else:
                    cells.append(yn(fld[fk]))
            lines.append("| " + " | ".join(str(c) for c in cells) + " |")
        lines.append("")

    lines.append("")
    lines.append("## Lifecycle date failures (detail)")
    lines.append("")
    failures = [r for r in rows if r["dates_ok"] == "fail"]
    if not failures:
        lines.append("None.")
    else:
        lines.append("| Project | Maturity | Missing |")
        lines.append("|---------|----------|---------|")
        for r in failures:
            miss = ", ".join(r["missing_required_dates"])
            lines.append(f"| {r['name']} | {r['effective_project']} | `{miss}` |")

    return "\n".join(lines)


def main() -> int:
    if not os.path.isfile(LANDSCAPE_PATH):
        print(f"Error: landscape not found at {LANDSCAPE_PATH}", file=sys.stderr)
        return 1

    with open(LANDSCAPE_PATH, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f.read()) or {}

    rows = build_rows(doc)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    md_path = os.path.join(OUTPUT_DIR, "landscape_data_integrity.md")
    json_path = os.path.join(OUTPUT_DIR, "landscape_data_integrity.json")

    md_body = render_markdown(rows)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_body)

    out_json = {
        "source": os.path.relpath(LANDSCAPE_PATH, AUDIT_ROOT),
        "scope_maturities": sorted(SCOPE_MATURITIES),
        "fixable_field_keys": [fk for fk, _s, _h in FIXABLE_FIELDS],
        "project_count": len(rows),
        "lifecycle_date_failures": sum(1 for r in rows if r["dates_ok"] == "fail"),
        "projects": rows,
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(out_json, f, indent=2, ensure_ascii=False)

    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
