#!/usr/bin/env python3
"""
landscape-guard checker

Compares base and PR versions of landscape.yml to detect direct modifications
to fields managed by dot-project (.project) repos. For each affected project,
checks GitHub for a .project repo. If one exists, the change should have been
made there instead.

The dot-project is still rolling out and not yet been adapted
by the majority of the CNCF Projects, therefore if the project
has a .project repo, that means it should adhere to the gaurd
and refere all meta data changes to the .project repo
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

import yaml

# Fields managed by the landscape-updater (from updateItemFields in main.go)
MANAGED_FIELDS = {"homepage_url", "description", "twitter"}
MANAGED_EXTRA_FIELDS = {"slack_url", "linkedin_url", "youtube_url"}

# Bot accounts that should bypass the check (landscape-updater automation)
BYPASS_AUTHORS = {
    "cncf-ci",
    "cncf-automation",
    "github-actions[bot]",
    "cncf-ci[bot]",
}


def parse_landscape_items(path: str) -> dict:
    """Parse landscape.yml and return a dict of item_name -> item_data.

    Each item_data is a dict with the managed fields + extra fields + repo_url.
    Key is (name, repo_url) to handle duplicate names across subcategories.
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    items = {}
    if not data or "landscape" not in data:
        return items

    for category in data["landscape"]:
        for subcategory in category.get("subcategories", []):
            for item in subcategory.get("items", []):
                name = item.get("name", "")
                repo_url = item.get("repo_url", "")
                if not name:
                    continue

                key = (name, repo_url)
                entry = {}

                # Collect managed top-level fields
                for field in MANAGED_FIELDS:
                    if field in item:
                        entry[field] = item[field]

                # Collect managed extra fields
                extra = item.get("extra", {})
                if isinstance(extra, dict):
                    for field in MANAGED_EXTRA_FIELDS:
                        if field in extra:
                            entry[f"extra.{field}"] = extra[field]

                entry["_repo_url"] = repo_url
                items[key] = entry

    return items


def find_changed_items(base_items: dict, pr_items: dict) -> list:
    """Compare base and PR items, return list of (name, repo_url, changed_fields)."""
    violations = []

    for key, pr_entry in pr_items.items():
        base_entry = base_items.get(key, {})
        name, repo_url = key

        changed_fields = []
        for field in list(MANAGED_FIELDS) + [f"extra.{f}" for f in MANAGED_EXTRA_FIELDS]:
            base_val = base_entry.get(field)
            pr_val = pr_entry.get(field)
            if base_val != pr_val:
                changed_fields.append(field)

        if changed_fields:
            violations.append((name, repo_url, changed_fields))

    return violations


def extract_org_from_repo_url(repo_url: str) -> str | None:
    """Extract GitHub org from a repo URL like https://github.com/kumahq/kuma."""
    if not repo_url:
        return None
    parts = repo_url.rstrip("/").split("/")
    # Expect: ['https:', '', 'github.com', 'org', 'repo']
    if len(parts) >= 4 and "github.com" in parts[2]:
        return parts[3]
    return None


def has_dot_project_repo(org: str, token: str) -> bool:
    """Check if <org>/.project exists on GitHub."""
    url = f"https://api.github.com/repos/{org}/.project"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    try:
        urllib.request.urlopen(req)
        return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        # For rate limits or other errors, assume no .project repo (fail open)
        print(f"::warning::GitHub API returned {e.code} checking {org}/.project")
        return False
    except Exception as e:
        print(f"::warning::Error checking {org}/.project: {e}")
        return False


def main():
    base_path = os.environ.get("LANDSCAPE_BASE", "")
    pr_path = os.environ.get("LANDSCAPE_PR", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    pr_author = os.environ.get("PR_AUTHOR", "")
    fail_on_violation = os.environ.get("FAIL_ON_VIOLATION", "false").lower() == "true"

    if not base_path or not pr_path:
        print("::error::LANDSCAPE_BASE and LANDSCAPE_PR must be set")
        sys.exit(1)

    # Bypass for automation bots
    if pr_author in BYPASS_AUTHORS:
        print(f"Skipping check: PR author '{pr_author}' is a known automation bot")
        sys.exit(0)

    # Parse both versions
    base_items = parse_landscape_items(base_path)
    pr_items = parse_landscape_items(pr_path)

    # Find changes to managed fields
    changed = find_changed_items(base_items, pr_items)
    if not changed:
        print("No managed field changes detected. All clear.")
        sys.exit(0)

    # For each changed item, check if a .project repo exists
    # Cache org lookups to avoid duplicate API calls
    org_cache: dict[str, bool] = {}
    guarded_violations = []

    for name, repo_url, changed_fields in changed:
        org = extract_org_from_repo_url(repo_url)
        if not org:
            continue

        if org not in org_cache:
            org_cache[org] = has_dot_project_repo(org, token)

        if org_cache[org]:
            guarded_violations.append((name, org, changed_fields))

    if not guarded_violations:
        print("Changed items don't have .project repos. No action needed.")
        sys.exit(0)

    # Build warning message
    lines = [
        "## ⚠️ Landscape Guard: managed fields modified directly\n",
        "The following project(s) have a `.project` repository that manages "
        "these fields automatically. Please submit your changes there instead:\n",
        "| Project | Changed Fields | Where to make changes |",
        "|---------|---------------|----------------------|",
    ]

    for name, org, changed_fields in guarded_violations:
        fields_str = ", ".join(f"`{f}`" for f in changed_fields)
        repo_link = f"[`{org}/.project`](https://github.com/{org}/.project)"
        lines.append(f"| **{name}** | {fields_str} | {repo_link} |")

    lines.append("")
    lines.append(
        "> **Why?** These fields are synced from the project's `.project` repository. "
        "Direct changes here will be overwritten on the next sync. "
        "See [dot-project docs](https://github.com/cncf/automation/tree/main/utilities/dot-project) for details."
    )

    comment_body = "\n".join(lines)

    # Write comment file for the action to post
    Path("/tmp/landscape-guard-comment.md").write_text(comment_body)

    # Write step summary
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(comment_body + "\n")

    # Set output so the action knows to post a comment
    output_path = os.environ.get("GITHUB_OUTPUT", "")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as f:
            f.write("comment=true\n")

    # Print to logs
    print(comment_body)

    n = len(guarded_violations)
    print(f"\n::warning::Found {n} project(s) with direct changes to managed fields")

    if fail_on_violation:
        print("::error::Failing check due to managed field violations (fail-on-violation=true)")
        sys.exit(1)


if __name__ == "__main__":
    main()

