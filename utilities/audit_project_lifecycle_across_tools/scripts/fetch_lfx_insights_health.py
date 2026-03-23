#!/usr/bin/env python3
"""
Fetch LFX Insights health tier (and optional numeric score) for CNCF projects listed in
datasources/pcc_projects.yaml.

Uses the public badge endpoint (302 to shields.io with message=<tier>) — no LFX_TOKEN.
Project keys match Insights `/project/{slug}` using the PCC `slug` field when present; when
absent, a slug is derived from the PCC `name` (same string shown in audit "Project" column).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, unquote, urlparse

import requests

try:
    import yaml  # type: ignore
except Exception:
    print("Missing dependency: PyYAML. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = os.getcwd()
DATASOURCES_DIR = os.path.join(REPO_ROOT, "datasources")
PCC_PATH = os.path.join(DATASOURCES_DIR, "pcc_projects.yaml")
OUTPUT_PATH = os.path.join(DATASOURCES_DIR, "lfx_insights_health.yaml")

BADGE_URL = "https://insights.linuxfoundation.org/api/badge/health-score"
PROJECT_PAGE_URL = "https://insights.linuxfoundation.org/project/{slug}"

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "cncf-automation/lfx-insights-health (+github actions)",
        "Accept": "text/html,application/json",
    }
)

OVERALL_SCORE_RE = re.compile(r'overall-score="(\d+)"')
SLEEP_SECONDS = 0.35


def slugify_from_name(name: str) -> str:
    """Fallback slug when PCC has no Slug (forming / some archived)."""
    s = re.sub(r"\([^)]*\)", "", name or "")
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def iter_pcc_projects(
    pcc: Dict[str, Any], max_projects: Optional[int] = None
) -> List[Tuple[str, Optional[str], str]]:
    """
    Yields (display_name, pcc_slug_or_none, origin) for each project row we try to match
    in Insights. Order: Graduated, Incubating, Sandbox, forming, archived.
    """
    out: List[Tuple[str, Optional[str], str]] = []
    categories = pcc.get("categories") or {}
    for cat in ("Graduated", "Incubating", "Sandbox"):
        for item in categories.get(cat) or []:
            name = (item.get("name") or "").strip()
            if not name:
                continue
            slug = item.get("slug")
            if isinstance(slug, str):
                slug = slug.strip() or None
            out.append((name, slug, f"category:{cat}"))
    for item in pcc.get("forming_projects") or []:
        name = (item.get("name") or "").strip()
        if not name:
            continue
        slug = item.get("slug")
        if isinstance(slug, str):
            slug = slug.strip() or None
        out.append((name, slug, "forming"))
    for item in pcc.get("archived_projects") or []:
        name = (item.get("name") or "").strip()
        if not name:
            continue
        slug = item.get("slug")
        if isinstance(slug, str):
            slug = slug.strip() or None
        out.append((name, slug, "archived"))
    if max_projects is not None:
        return out[: max(0, max_projects)]
    return out


def resolve_slugs_to_try(name: str, pcc_slug: Optional[str]) -> List[str]:
    """Insights is case-sensitive per project; try PCC slug first, then derived."""
    seen: set[str] = set()
    ordered: List[str] = []
    if pcc_slug:
        for s in (pcc_slug, pcc_slug.lower()):
            if s and s not in seen:
                seen.add(s)
                ordered.append(s)
    derived = slugify_from_name(name)
    if derived and derived not in seen:
        ordered.append(derived)
    return ordered


def tier_from_badge_head(slug: str) -> Tuple[Optional[str], int]:
    """
    Returns (tier_label, http_status) for the badge HEAD request.
    tier_label is parsed from shields redirect Location (message=...).
    """
    try:
        r = SESSION.head(
            BADGE_URL,
            params={"project": slug},
            allow_redirects=False,
            timeout=45,
        )
    except requests.RequestException as e:
        print(f"  badge HEAD error for slug={slug!r}: {e}", file=sys.stderr)
        return None, 0

    if r.status_code == 302 and r.headers.get("Location"):
        loc = r.headers["Location"]
        q = parse_qs(urlparse(loc).query)
        raw = (q.get("message") or [None])[0]
        if raw:
            return unquote(raw), r.status_code
    return None, r.status_code


def overall_score_from_project_page(slug: str) -> Optional[int]:
    """Fetch SSR project page and read overall-score=\"N\" if present."""
    url = PROJECT_PAGE_URL.format(slug=requests.utils.quote(slug, safe=""))
    try:
        r = SESSION.get(url, timeout=45)
    except requests.RequestException:
        return None
    if r.status_code != 200:
        return None
    m = OVERALL_SCORE_RE.search(r.text)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def fetch_one(name: str, pcc_slug: Optional[str]) -> Dict[str, Any]:
    slugs = resolve_slugs_to_try(name, pcc_slug)
    row: Dict[str, Any] = {
        "name": name,
        "pcc_slug": pcc_slug,
        "insights_slug_used": None,
        "health_tier": None,
        "overall_score": None,
        "error": None,
    }
    last_status: Optional[int] = None
    for slug in slugs:
        tier, status = tier_from_badge_head(slug)
        last_status = status
        if tier:
            row["insights_slug_used"] = slug
            row["health_tier"] = tier
            time.sleep(SLEEP_SECONDS)
            row["overall_score"] = overall_score_from_project_page(slug)
            return row
        time.sleep(SLEEP_SECONDS)

    row["error"] = "not_found"
    if last_status is not None:
        row["http_status_last"] = last_status
    return row


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch LFX Insights health scores from PCC project list.")
    parser.add_argument(
        "--max-projects",
        type=int,
        default=None,
        metavar="N",
        help="Only process the first N projects (for testing).",
    )
    args = parser.parse_args()

    os.makedirs(DATASOURCES_DIR, exist_ok=True)
    if not os.path.isfile(PCC_PATH):
        print(f"Error: {PCC_PATH} not found. Run PCC sync or checkout the repo with datasources.", file=sys.stderr)
        sys.exit(1)

    with open(PCC_PATH, "r", encoding="utf-8") as f:
        pcc = yaml.safe_load(f.read())

    projects_in = iter_pcc_projects(pcc, max_projects=args.max_projects)
    results: List[Dict[str, Any]] = []
    for i, (name, pcc_slug, _origin) in enumerate(projects_in):
        print(f"[{i + 1}/{len(projects_in)}] {name!r} ...", flush=True)
        results.append(fetch_one(name, pcc_slug))
        time.sleep(SLEEP_SECONDS)

    out_doc: Dict[str, Any] = {
        "source": "LFX Insights (badge API + project page SSR)",
        "pcc_source_file": "datasources/pcc_projects.yaml",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "projects": results,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        yaml.safe_dump(out_doc, f, sort_keys=False, allow_unicode=True)

    ok = sum(1 for r in results if r.get("health_tier"))
    missing = sum(1 for r in results if r.get("error") == "not_found")
    print(f"Wrote {OUTPUT_PATH} — {ok} with tier, {missing} not found, {len(results)} total")


if __name__ == "__main__":
    main()
