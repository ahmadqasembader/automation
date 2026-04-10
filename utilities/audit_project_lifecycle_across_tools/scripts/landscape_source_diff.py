#!/usr/bin/env python3
"""
Compare vendored landscape.yml to PCC and CLOMonitor snapshots in datasources/.

Canonical truth: PCC + CLOMonitor (when both agree). When they disagree, the
report calls that out alongside landscape drift.
"""

from __future__ import annotations

import importlib.util
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
PCC_PATH = os.path.join(AUDIT_ROOT, "datasources", "pcc_projects.yaml")
CLOMONITOR_PATH = os.path.join(AUDIT_ROOT, "datasources", "clomonitor.yaml")
OUTPUT_DIR = os.path.join(AUDIT_ROOT, "audit", "landscape_data_integrity_audit")

_ldi_path = os.path.join(SCRIPT_DIR, "landscape_data_integrity_audit.py")
_spec = importlib.util.spec_from_file_location("_ldi", _ldi_path)
if _spec is None or _spec.loader is None:
    print(
        f"Failed to load helper module from: {_ldi_path}",
        file=sys.stderr,
    )
    sys.exit(2)
_ldi = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ldi)

iter_landscape_items = _ldi.iter_landscape_items
get_extra = _ldi.get_extra
effective_project = _ldi.effective_project
present = _ldi.present
SCOPE_MATURITIES = _ldi.SCOPE_MATURITIES


def normalize_slug(s: Any) -> str:
    return str(s or "").strip().lower().replace("_", "-")


def normalize_key(name: str) -> str:
    return " ".join(str(name or "").lower().split())


def normalize_url(u: str) -> str:
    u = str(u or "").strip().rstrip("/")
    if u.endswith(".git"):
        u = u[:-4]
    if u.startswith("https://github.com/"):
        rest = u[19:].lower().rstrip("/")
        return f"https://github.com/{rest}"
    return u.lower().rstrip("/")


def normalize_date(s: Any) -> str:
    if s is None:
        return ""
    t = str(s).strip().strip("'\"")
    if "T" in t:
        t = t.split("T", 1)[0]
    return t[:10] if len(t) >= 10 else t


def pcc_maturity_from_row(tier: str, row: Dict[str, Any]) -> str:
    t = (tier or "").strip()
    if t == "Archived":
        return "archived"
    m = {
        "Graduated": "graduated",
        "Incubating": "incubating",
        "Sandbox": "sandbox",
    }.get(t, "")
    if not m and row.get("status") == "Archived":
        return "archived"
    return m


def clo_maturity(raw: Any) -> str:
    s = str(raw or "").strip().lower()
    if s in ("graduated", "incubating", "sandbox", "archived"):
        return s
    return s


def clo_primary_repo(entry: Dict[str, Any]) -> str:
    repos = entry.get("repositories") or []
    if not isinstance(repos, list) or not repos:
        return ""
    r0 = repos[0]
    if isinstance(r0, dict):
        return str(r0.get("url") or "").strip()
    return ""


def load_pcc_indexes(path: str) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    """by_slug, by_normalized_project_name"""
    by_slug: Dict[str, Dict[str, Any]] = {}
    by_name: Dict[str, Dict[str, Any]] = {}
    if not os.path.isfile(path):
        return by_slug, by_name
    with open(path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f.read()) or {}
    categories = doc.get("categories") or {}
    for tier in ("Graduated", "Incubating", "Sandbox"):
        for row in categories.get(tier) or []:
            if not isinstance(row, dict):
                continue
            slug = normalize_slug(row.get("slug"))
            enriched = {**row, "_pcc_tier": tier}
            if slug:
                by_slug[slug] = enriched
            nk = normalize_key(row.get("name") or "")
            if nk and nk not in by_name:
                by_name[nk] = enriched
    for row in doc.get("archived_projects") or []:
        if not isinstance(row, dict):
            continue
        slug = normalize_slug(row.get("slug"))
        enriched = {**row, "_pcc_tier": "Archived"}
        if slug:
            by_slug[slug] = enriched
        nk = normalize_key(row.get("name") or "")
        if nk and nk not in by_name:
            by_name[nk] = enriched
    return by_slug, by_name


def load_clomonitor_indexes(path: str) -> Dict[str, Dict[str, Any]]:
    """by project `name` (slug)"""
    by_name: Dict[str, Dict[str, Any]] = {}
    if not os.path.isfile(path):
        return by_name
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f.read())
    if not isinstance(data, list):
        return by_name
    for entry in data:
        if not isinstance(entry, dict):
            continue
        k = normalize_slug(entry.get("name"))
        if k:
            by_name[k] = entry
    return by_name


def resolve_pcc_clo(
    item: Dict[str, Any],
    pcc_by_slug: Dict[str, Dict[str, Any]],
    pcc_by_name: Dict[str, Dict[str, Any]],
    clo_by_name: Dict[str, Dict[str, Any]],
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], str]:
    """Returns (pcc_row, clo_entry, match_note)."""
    extra = get_extra(item)
    name = str(item.get("name") or "").strip()
    pcc: Optional[Dict[str, Any]] = None
    clo: Optional[Dict[str, Any]] = None
    notes: List[str] = []

    ck = normalize_slug(extra.get("clomonitor_name"))
    if ck and ck in clo_by_name:
        clo = clo_by_name[ck]
        notes.append("clomonitor_name")

    sk = normalize_slug(extra.get("lfx_slug"))
    if sk and sk in pcc_by_slug:
        pcc = pcc_by_slug[sk]
        notes.append("lfx_slug")

    if clo and not pcc:
        nk = normalize_slug(clo.get("name"))
        if nk in pcc_by_slug:
            pcc = pcc_by_slug[nk]
            notes.append("pcc_via_clo_name")

    if not pcc and not clo:
        nk = normalize_key(name)
        if nk in pcc_by_name:
            pcc = pcc_by_name[nk]
            notes.append("pcc_name")
        guess = normalize_slug(name.replace(" ", "-").replace("(", "").replace(")", ""))
        if guess in clo_by_name:
            clo = clo_by_name[guess]
            notes.append("clo_slug_guess")

    if pcc and not clo:
        nk = normalize_slug(pcc.get("slug"))
        if nk in clo_by_name:
            clo = clo_by_name[nk]
            notes.append("clo_via_pcc_slug")

    return pcc, clo, "+".join(sorted(set(notes))) if notes else "none"


def compare_field(
    field_label: str,
    land_raw: Any,
    pcc_raw: Any,
    clo_raw: Any,
    normalize_fn,
) -> Optional[Dict[str, Any]]:
    """
    Emit a finding when landscape is out of sync with either source, or PCC and CLOMonitor disagree.
    """

    def norm(x: Any) -> str:
        if not present(x):
            return ""
        return normalize_fn(str(x).strip())

    lv, pv, cv = norm(land_raw), norm(pcc_raw), norm(clo_raw)
    has_l, has_p, has_c = bool(lv), bool(pv), bool(cv)

    if not has_p and not has_c:
        return None

    sources_agree = True
    if has_p and has_c:
        sources_agree = pv == cv

    land_ok_p = not has_p or (has_l and lv == pv)
    land_ok_c = not has_c or (has_l and lv == cv)

    if sources_agree and land_ok_p and land_ok_c:
        return None

    msgs: List[str] = []
    if has_p and has_c and not sources_agree:
        msgs.append(f"PCC ({pcc_raw!r}) and CLOMonitor ({clo_raw!r}) disagree.")
    if has_p and not land_ok_p:
        if has_l:
            msgs.append(f"Landscape ({land_raw!r}) ≠ PCC ({pcc_raw!r}).")
        else:
            msgs.append(f"Landscape missing; PCC has {pcc_raw!r}.")
    if has_c and not land_ok_c:
        if has_l:
            msgs.append(f"Landscape ({land_raw!r}) ≠ CLOMonitor ({clo_raw!r}).")
        else:
            msgs.append(f"Landscape missing; CLOMonitor has {clo_raw!r}.")

    return {
        "field": field_label,
        "landscape": land_raw if present(land_raw) else None,
        "pcc": pcc_raw if present(pcc_raw) else None,
        "clomonitor": clo_raw if present(clo_raw) else None,
        "pcc_clomonitor_agree": sources_agree if (has_p and has_c) else None,
        "message": " ".join(msgs),
    }


def slug_identity_conflict(pcc: Optional[Dict[str, Any]], clo: Optional[Dict[str, Any]]) -> Optional[str]:
    if not pcc or not clo:
        return None
    ps = normalize_slug(pcc.get("slug"))
    cn = normalize_slug(clo.get("name"))
    if ps and cn and ps != cn:
        return f"PCC slug {pcc.get('slug')!r} vs CLOMonitor name {clo.get('name')!r} (normalized identifiers differ)."
    return None


def build_report() -> Dict[str, Any]:
    with open(LANDSCAPE_PATH, "r", encoding="utf-8") as f:
        land_doc = yaml.safe_load(f.read()) or {}

    pcc_by_slug, pcc_by_name = load_pcc_indexes(PCC_PATH)
    clo_by_name = load_clomonitor_indexes(CLOMONITOR_PATH)

    projects_out: List[Dict[str, Any]] = []

    for cat_name, sub_name, item in iter_landscape_items(land_doc):
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        eff = effective_project(item)
        if eff not in SCOPE_MATURITIES:
            continue

        extra = get_extra(item)
        path = f"{cat_name} / {sub_name}" if cat_name or sub_name else ""
        pcc, clo, match_note = resolve_pcc_clo(item, pcc_by_slug, pcc_by_name, clo_by_name)

        land_repo = str(item.get("repo_url") or "").strip()
        land_slug = str(extra.get("lfx_slug") or "").strip()
        land_clomon = str(extra.get("clomonitor_name") or "").strip()
        land_dev = str(extra.get("dev_stats_url") or "").strip()
        land_acc = str(extra.get("accepted") or "").strip()

        pcc_repo = str(pcc.get("repository_url") or "").strip() if pcc else ""
        clo_repo = clo_primary_repo(clo) if clo else ""
        pcc_slug = str(pcc.get("slug") or "").strip() if pcc else ""
        clo_name = str(clo.get("name") or "").strip() if clo else ""
        clo_dev = str(clo.get("devstats_url") or "").strip() if clo else ""
        clo_acc = str(clo.get("accepted_at") or "").strip() if clo else ""

        pcc_mat = ""
        if pcc:
            pcc_mat = pcc_maturity_from_row(str(pcc.get("_pcc_tier") or ""), pcc)
        clo_mat = clo_maturity(clo.get("maturity")) if clo else ""

        findings: List[Dict[str, Any]] = []

        idc = slug_identity_conflict(pcc, clo)
        if idc:
            findings.append(
                {
                    "field": "identifiers",
                    "landscape": None,
                    "pcc": pcc_slug,
                    "clomonitor": clo_name,
                    "pcc_clomonitor_agree": False,
                    "message": idc,
                }
            )

        f1 = compare_field("repo_url", land_repo, pcc_repo, clo_repo, normalize_url)
        if f1:
            findings.append(f1)

        f2 = compare_field(
            "extra.lfx_slug",
            land_slug,
            pcc_slug,
            clo_name,
            normalize_slug,
        )
        if f2:
            findings.append(f2)

        f3 = compare_field(
            "extra.clomonitor_name",
            land_clomon,
            None,
            clo_name,
            normalize_slug,
        )
        if f3:
            findings.append(f3)

        f4 = compare_field("extra.dev_stats_url", land_dev, None, clo_dev, normalize_url)
        if f4:
            findings.append(f4)

        f5 = compare_field(
            "extra.accepted",
            land_acc,
            None,
            clo_acc,
            lambda x: normalize_date(x),
        )
        if f5:
            findings.append(f5)

        if pcc_mat or clo_mat:
            f6 = compare_field(
                "project (maturity)",
                eff,
                pcc_mat,
                clo_mat,
                normalize_slug,
            )
            if f6:
                findings.append(f6)

        projects_out.append(
            {
                "name": name,
                "path": path,
                "maturity": eff,
                "match_note": match_note,
                "matched_pcc": pcc is not None,
                "matched_clomonitor": clo is not None,
                "findings": findings,
            }
        )

    return {
        "source": "datasources vs landscape.yml",
        "projects": projects_out,
    }


def fmt_val(v: Any) -> str:
    if v is None:
        return "—"
    s = str(v).replace("|", "\\|")
    if len(s) > 60:
        return s[:57] + "…"
    return s


def render_markdown(data: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Landscape vs datasources diff")
    lines.append("")
    lines.append("**Canonical:** `datasources/pcc_projects.yaml` and `datasources/clomonitor.yaml`. ")
    lines.append("When those two disagree, that is called out. **`landscape.yml` should be updated** to match the agreed sources (or you must reconcile PCC vs CLOMonitor first).")
    lines.append("")

    projects = data["projects"]
    with_findings = [p for p in projects if p["findings"]]
    unmatched = [p for p in projects if not p["matched_pcc"] and not p["matched_clomonitor"]]
    pcc_clo_only = [
        f
        for p in projects
        for f in p["findings"]
        if f.get("pcc_clomonitor_agree") is False
    ]

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **CNCF landscape items in scope:** {len(projects)}")
    lines.append(f"- **With at least one drift / conflict row:** {len(with_findings)}")
    lines.append(f"- **Findings where PCC and CLOMonitor disagree:** {len(pcc_clo_only)}")
    lines.append(f"- **No PCC and no CLOMonitor match:** {len(unmatched)}")
    lines.append("")

    lines.append("## Per-project: landscape vs sources")
    lines.append("")
    for p in sorted(with_findings, key=lambda x: (x["maturity"], x["name"].lower())):
        lines.append(f"### {p['name']} ({p['maturity']})")
        lines.append("")
        lines.append(f"- **Path:** {p['path']}")
        lines.append(
            f"- **Matched:** PCC={p['matched_pcc']}, CLOMonitor={p['matched_clomonitor']} ({p['match_note']})"
        )
        lines.append("")
        lines.append("| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |")
        lines.append("|-------|-----------|-----|------------|---------|------|")
        for f in p["findings"]:
            agree = f.get("pcc_clomonitor_agree")
            agree_s = "—" if agree is None else ("Yes" if agree else "**No**")
            lines.append(
                f"| {f['field']} | {fmt_val(f.get('landscape'))} | {fmt_val(f.get('pcc'))} | "
                f"{fmt_val(f.get('clomonitor'))} | {agree_s} | {fmt_val(f.get('message', ''))} |"
            )
        lines.append("")

    lines.append("## No datasource match")
    lines.append("")
    if not unmatched:
        lines.append("_All in-scope items resolved to at least PCC or CLOMonitor._")
    else:
        lines.append("| Project | Maturity | Path |")
        lines.append("|---------|----------|------|")
        for p in sorted(unmatched, key=lambda x: (x["maturity"], x["name"].lower())):
            lines.append(f"| {p['name']} | {p['maturity']} | {p['path']} |")

    return "\n".join(lines)


def main() -> int:
    if not os.path.isfile(LANDSCAPE_PATH):
        print(f"Missing {LANDSCAPE_PATH}", file=sys.stderr)
        return 1

    data = build_report()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    md_path = os.path.join(OUTPUT_DIR, "landscape_source_diff.md")
    json_path = os.path.join(OUTPUT_DIR, "landscape_source_diff.json")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(render_markdown(data))

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
