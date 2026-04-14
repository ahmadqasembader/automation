#!/usr/bin/env python3
"""
Generate repo URL healthcheck markdown from landscape_source_diff.json.

Policy:
- Input candidates are repo_url findings from landscape_source_diff.json.
- If PCC and Landscape GitHub org/owner match, repo-level mismatch is ignored.
- Otherwise compare reachability and final redirect destination.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from urllib.parse import urlparse


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIT_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(AUDIT_ROOT, "audit", "landscape_data_integrity_audit")
DEFAULT_SOURCE_JSON = os.path.join(OUTPUT_DIR, "landscape_source_diff.json")
DEFAULT_OUTPUT_MD = os.path.join(OUTPUT_DIR, "repo_url_landscape.md")


@dataclass(frozen=True)
class RepoRow:
    project: str
    maturity: str
    pcc_url: str
    landscape_url: str


@dataclass(frozen=True)
class UrlCheck:
    input_url: str
    ok: bool
    status_text: str
    final_url: str


def _normalize_cell(value: Any) -> str:
    text = str(value or "").strip()
    return text if text else "—"


def load_repo_rows(source_json_path: str) -> List[RepoRow]:
    with open(source_json_path, "r", encoding="utf-8") as f:
        data: Dict[str, Any] = json.load(f)

    rows: List[RepoRow] = []
    seen: Set[Tuple[str, str, str, str]] = set()
    for project in data.get("projects", []):
        name = str(project.get("name") or "").strip()
        maturity = str(project.get("maturity") or "").strip()
        for finding in project.get("findings", []):
            if finding.get("field") != "repo_url":
                continue
            pcc_url = _normalize_cell(finding.get("pcc"))
            landscape_url = _normalize_cell(finding.get("landscape"))
            key = (name, maturity, pcc_url, landscape_url)
            if key in seen:
                continue
            seen.add(key)
            rows.append(
                RepoRow(
                    project=name,
                    maturity=maturity,
                    pcc_url=pcc_url,
                    landscape_url=landscape_url,
                )
            )

    rows.sort(key=lambda row: (row.project.lower(), row.maturity.lower()))
    return rows


def _github_owner(url: str) -> Optional[str]:
    if not url or url == "—":
        return None
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = (parsed.netloc or "").lower()
    if host not in {"github.com", "www.github.com"}:
        return None
    path = (parsed.path or "").strip("/")
    if not path:
        return None
    owner = path.split("/", 1)[0].strip().lower()
    return owner or None


def _normalize_url(url: str) -> str:
    if not url or url == "—":
        return "—"
    parsed = urlparse(url if "://" in url else f"https://{url}")
    scheme = (parsed.scheme or "https").lower()
    host = (parsed.netloc or "").lower()
    path = (parsed.path or "").rstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    if host in {"github.com", "www.github.com"}:
        path = path.lower()
    return f"{scheme}://{host}{path}"


def check_url(url: str, timeout_seconds: int = 20) -> UrlCheck:
    if url == "—":
        return UrlCheck(input_url=url, ok=False, status_text="❌ missing", final_url="—")
    cmd = [
        "curl",
        "-L",
        "-sS",
        "-o",
        "/dev/null",
        "-w",
        "%{http_code} %{url_effective}",
        "--max-time",
        str(timeout_seconds),
        url,
    ]
    try:
        cp = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return UrlCheck(input_url=url, ok=False, status_text="❌ curl_error", final_url="—")

    out = (cp.stdout or "").strip()
    if cp.returncode != 0 or not out:
        return UrlCheck(input_url=url, ok=False, status_text="❌ URLError", final_url="—")

    parts = out.split(" ", 1)
    code_raw = parts[0] if parts else "000"
    effective = parts[1].strip() if len(parts) > 1 else url

    try:
        code = int(code_raw)
    except ValueError:
        return UrlCheck(input_url=url, ok=False, status_text="❌ URLError", final_url="—")

    if 200 <= code < 400:
        marker = "✅" if code == 200 else "⚠️"
        return UrlCheck(
            input_url=url,
            ok=True,
            status_text=f"{marker} {code}",
            final_url=effective or url,
        )
    return UrlCheck(
        input_url=url,
        ok=False,
        status_text=f"❌ HTTP {code}",
        final_url=effective or "—",
    )


def render_markdown(rows: Iterable[RepoRow]) -> str:
    lines = [
        "# Repo URL health check (Landscape vs PCC)",
        "",
        "Generated from `landscape_source_diff.json` (`field = repo_url`) with `curl` URL checks.",
        "",
        "Rule: when both URLs are GitHub and org/owner matches, repo path differences are treated as aligned.",
        "",
        "| Project | Maturity | PCC URL | PCC | Landscape URL | Landscape | Org match | Same final destination | Result | Note |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    rendered_rows: List[Dict[str, str]] = []
    for row in rows:
        pcc = check_url(row.pcc_url)
        land = check_url(row.landscape_url)
        pcc_owner = _github_owner(row.pcc_url)
        land_owner = _github_owner(row.landscape_url)
        org_match = bool(pcc_owner and land_owner and pcc_owner == land_owner)

        pcc_final_norm = _normalize_url(pcc.final_url)
        land_final_norm = _normalize_url(land.final_url)
        same_final_value = "N/A"
        same_final_bool = False
        if pcc.ok and land.ok and pcc_final_norm != "—" and land_final_norm != "—":
            same_final_bool = pcc_final_norm == land_final_norm
            same_final_value = "Yes" if same_final_bool else "No"

        if row.pcc_url == "—" or row.landscape_url == "—":
            result = "Missing URL"
            note = "One side is missing."
        elif org_match:
            result = "Aligned (org match)"
            note = f"GitHub owner `{pcc_owner}` matches; repo path ignored."
        elif same_final_bool:
            result = "Aligned (same final URL)"
            note = "URLs converge to same effective destination."
        elif same_final_value == "No":
            result = "Mismatch"
            note = (
                "Different final destinations: "
                f"PCC `{pcc.final_url}` vs Landscape `{land.final_url}`."
            )
        else:
            result = "URL error"
            note = (
                "At least one URL is not reachable: "
                f"PCC `{pcc.status_text}`, Landscape `{land.status_text}`."
            )

        rendered_rows.append(
            {
                "project": row.project,
                "maturity": row.maturity,
                "pcc_url": row.pcc_url,
                "pcc_status": pcc.status_text,
                "landscape_url": row.landscape_url,
                "landscape_status": land.status_text,
                "org_match": "Yes" if org_match else "No",
                "same_final": same_final_value,
                "result": result,
                "note": note,
            }
        )

    # Keep "Same final destination = No" rows at the top, then N/A, then Yes.
    sort_rank = {"No": 0, "N/A": 1, "Yes": 2}
    rendered_rows.sort(key=lambda r: (sort_rank.get(r["same_final"], 3), r["project"].lower()))
    for r in rendered_rows:
        lines.append(
            f"| {r['project']} | {r['maturity']} | {r['pcc_url']} | {r['pcc_status']} | "
            f"{r['landscape_url']} | {r['landscape_status']} | {r['org_match']} | "
            f"{r['same_final']} | {r['result']} | {r['note']} |"
        )
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate repo_url_landscape.md from "
            "audit/landscape_data_integrity_audit/landscape_source_diff.json"
        )
    )
    parser.add_argument(
        "--source-json",
        default=DEFAULT_SOURCE_JSON,
        help="Path to landscape_source_diff.json",
    )
    parser.add_argument(
        "--output-md",
        default=DEFAULT_OUTPUT_MD,
        help="Path to output markdown report",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source_json = os.path.abspath(args.source_json)
    output_md = os.path.abspath(args.output_md)

    if not os.path.isfile(source_json):
        print(
            f"Missing source file: {source_json}\n"
            "Run scripts/landscape_source_diff.py first.",
            file=sys.stderr,
        )
        return 1

    rows = load_repo_rows(source_json)
    body = render_markdown(rows)
    os.makedirs(os.path.dirname(output_md), exist_ok=True)
    with open(output_md, "w", encoding="utf-8") as f:
        f.write(body)

    print(f"Wrote {output_md}")
    print(f"Rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
