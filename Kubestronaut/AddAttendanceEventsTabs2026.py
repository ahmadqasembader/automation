#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import re
from collections import OrderedDict
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Set, Tuple

import pygsheets
from dotenv import load_dotenv


EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
SHEET_FORBIDDEN_CHARS_RE = re.compile(r"[\[\]\*\?/\\:]")


@dataclass
class InfosEntry:
    email: str
    country: str
    name: str
    size: str
    jacket_sent: str


@dataclass
class EventParticipant:
    email: str
    name: str
    country: str
    size: str
    highlight_yellow: bool


def norm(s: str) -> str:
    return (s or "").strip().lower()


def compact_header(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def extract_emails(raw: str) -> List[str]:
    return [norm(e) for e in EMAIL_RE.findall(raw or "")]


def has_meaningful_value(raw: str) -> bool:
    return bool((raw or "").strip())


def is_green_color(color) -> bool:
    if not color:
        return False

    if isinstance(color, dict):
        raw_r = color.get("red")
        raw_g = color.get("green")
        raw_b = color.get("blue")
    elif hasattr(color, "red") and hasattr(color, "green") and hasattr(color, "blue"):
        raw_r = getattr(color, "red")
        raw_g = getattr(color, "green")
        raw_b = getattr(color, "blue")
    else:
        if len(color) < 3:
            return False
        raw_r, raw_g, raw_b = color[0], color[1], color[2]

    try:
        r = float(raw_r) if raw_r is not None else None
        g = float(raw_g) if raw_g is not None else None
        b = float(raw_b) if raw_b is not None else None
    except (TypeError, ValueError):
        return False

    if r is None or g is None or b is None:
        return False

    return g >= 0.55 and (g - r) >= 0.15 and (g - b) >= 0.15


def split_events(raw: str) -> List[str]:
    if not raw:
        return []
    parts = re.split(r"\n+|\s*;\s*|\s*,\s*", raw)
    out: List[str] = []
    for p in parts:
        ev = (p or "").strip()
        if not ev:
            continue
        if ev.lower() in {"none", "n/a", "na", "no"}:
            continue
        out.append(ev)
    return out


def load_excluded_events(file_path: str, cli_events: List[str]) -> Set[str]:
    excluded = {compact_header(ev) for ev in cli_events if compact_header(ev)}
    if not file_path or not os.path.exists(file_path):
        return excluded

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                raw = line.strip()
                if not raw or raw.startswith("#"):
                    continue
                excluded.add(compact_header(raw))
    except Exception as exc:
        print(f"[WARN] Failed to read excluded events file {file_path}: {exc}")

    return excluded


def load_events_to_manage(spreadsheet, tab_title: str) -> Set[str]:
    try:
        ws = spreadsheet.worksheet_by_title(tab_title)
    except pygsheets.WorksheetNotFound:
        raise RuntimeError(f"Worksheet '{tab_title}' not found in attendance spreadsheet.")

    values = ws.get_all_values(
        include_tailing_empty=False,
        include_tailing_empty_rows=False,
        returnas="matrix",
    )
    managed: Set[str] = set()
    for row in values:
        if not row:
            continue
        raw = (row[0] or "").strip()
        if not raw or raw.startswith("#"):
            continue
        header_like = compact_header(raw)
        if header_like in {"event", "events", "event to manage", "events to manage"}:
            continue
        managed.add(header_like)

    if not managed:
        raise RuntimeError(f"Worksheet '{tab_title}' is empty. Add at least one event to manage.")

    return managed


def sanitize_sheet_title(raw_title: str) -> str:
    title = SHEET_FORBIDDEN_CHARS_RE.sub(" ", raw_title or "")
    title = re.sub(r"\s+", " ", title).strip().strip("'")
    if not title:
        title = "Event"
    return title[:100]


def make_unique_titles(events: List[str]) -> Dict[str, str]:
    used = set()
    mapping: Dict[str, str] = {}

    for event in events:
        base = sanitize_sheet_title(event)
        title = base
        idx = 2
        while title in used:
            suffix = f" ({idx})"
            max_base_len = 100 - len(suffix)
            title = f"{base[:max_base_len]}{suffix}"
            idx += 1
        used.add(title)
        mapping[event] = title

    return mapping


def load_manual_cache(cache_file: str) -> Dict[str, str]:
    if not os.path.exists(cache_file):
        return {}
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            print(f"[WARN] Manual cache format invalid in {cache_file}, ignoring.")
            return {}
        return data
    except Exception as exc:
        print(f"[WARN] Failed to read manual cache {cache_file}: {exc}")
        return {}


def save_manual_cache(cache: Dict[str, str], cache_file: str):
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False)


def build_expanded_cache(cache: Dict[str, str]) -> Dict[str, str]:
    expanded: Dict[str, str] = {}
    for raw_source, raw_target in cache.items():
        target = norm(raw_target)
        if not target:
            continue

        source_emails = extract_emails(raw_source)
        if not source_emails and "@" in raw_source:
            source_emails = [norm(raw_source)]

        for src in source_emails:
            if src:
                expanded[src] = target
    return expanded


def detect_attendance_columns(headers: List[str]) -> Tuple[int, int, int, int]:
    normalized = [compact_header(h) for h in headers]

    email_idx = -1
    events_idx = -1
    timestamp_idx = -1
    swag_mention_idx = -1

    for i, h in enumerate(normalized):
        if h == "timestamp":
            timestamp_idx = i
        if h in {"email", "email address"} and email_idx < 0:
            email_idx = i

    if email_idx < 0:
        for i, h in enumerate(normalized):
            if "email" in h:
                email_idx = i
                break

    for i, h in enumerate(normalized):
        if "plan to attend" in h and ("kubecon" in h or "kcd" in h):
            events_idx = i
            break

    if events_idx < 0:
        for i, h in enumerate(normalized):
            if "select all that applies" in h:
                events_idx = i
                break

    for i, h in enumerate(normalized):
        if "if you have not received your swag" in h:
            swag_mention_idx = i
            break

    if email_idx < 0:
        raise RuntimeError("Could not find 'Email Address' column in attendance sheet.")
    if events_idx < 0:
        raise RuntimeError("Could not find events column in attendance sheet.")

    return email_idx, events_idx, timestamp_idx, swag_mention_idx


def detect_infos_columns(headers: List[str]) -> Tuple[int, int, int, int, int]:
    normalized = [compact_header(h) for h in headers]

    email_idx = -1
    country_idx = -1
    name_idx = -1
    size_idx = -1
    jacket_sent_idx = -1

    for i, h in enumerate(normalized):
        if h in {"email", "email address"} and email_idx < 0:
            email_idx = i
        if h == "country" and country_idx < 0:
            country_idx = i
        if (h == "name" or "what is your name" in h) and name_idx < 0:
            name_idx = i
        if ("t-shirt/jacket size" in h or "t-shirt/jacket sizes" in h or "jacket size" in h) and size_idx < 0:
            size_idx = i
        if "jacket sent" in h and jacket_sent_idx < 0:
            jacket_sent_idx = i

    if email_idx < 0:
        for i, h in enumerate(normalized):
            if "email" in h:
                email_idx = i
                break

    if country_idx < 0:
        for i, h in enumerate(normalized):
            if "country" in h:
                country_idx = i
                break

    if name_idx < 0:
        for i, h in enumerate(normalized):
            if "name" in h:
                name_idx = i
                break
    if size_idx < 0:
        for i, h in enumerate(normalized):
            if "size" in h and ("shirt" in h or "jacket" in h):
                size_idx = i
                break
    if jacket_sent_idx < 0:
        for i, h in enumerate(normalized):
            if "jacket sent" in h:
                jacket_sent_idx = i
                break

    if email_idx < 0:
        raise RuntimeError("Could not find email column in KUBESTRONAUTS_INFOS sheet.")
    if country_idx < 0:
        raise RuntimeError("Could not find 'Country' column in KUBESTRONAUTS_INFOS sheet.")
    if name_idx < 0:
        raise RuntimeError("Could not find 'What is your name?' column in KUBESTRONAUTS_INFOS sheet.")
    if size_idx < 0:
        raise RuntimeError("Could not find 'What is your t-shirt/jacket sizes?' column in KUBESTRONAUTS_INFOS sheet.")
    if jacket_sent_idx < 0:
        raise RuntimeError("Could not find 'Jacket Sent ?' column in KUBESTRONAUTS_INFOS sheet.")

    return email_idx, country_idx, name_idx, size_idx, jacket_sent_idx


def load_infos_index(infos_ws) -> Tuple[Dict[str, InfosEntry], List[InfosEntry]]:
    matrix = infos_ws.get_all_values(
        include_tailing_empty=False,
        include_tailing_empty_rows=False,
        returnas="matrix",
    )
    if not matrix or len(matrix) < 2:
        raise RuntimeError("KUBESTRONAUTS_INFOS appears empty.")

    headers = matrix[0]
    email_idx, country_idx, name_idx, size_idx, jacket_sent_idx = detect_infos_columns(headers)

    by_email: Dict[str, InfosEntry] = {}
    all_entries: List[InfosEntry] = []

    for row in matrix[1:]:
        email_cell = row[email_idx] if email_idx < len(row) else ""
        country = (row[country_idx].strip() if country_idx < len(row) and row[country_idx] else "")
        name = (row[name_idx].strip() if name_idx >= 0 and name_idx < len(row) and row[name_idx] else "")
        size = (row[size_idx].strip() if size_idx >= 0 and size_idx < len(row) and row[size_idx] else "")
        jacket_sent = (row[jacket_sent_idx].strip() if jacket_sent_idx >= 0 and jacket_sent_idx < len(row) and row[jacket_sent_idx] else "")

        for email in extract_emails(email_cell):
            if not email:
                continue
            entry = InfosEntry(email=email, country=country, name=name, size=size, jacket_sent=jacket_sent)
            if email not in by_email:
                by_email[email] = entry
            all_entries.append(entry)

    if not by_email:
        raise RuntimeError("No email found in KUBESTRONAUTS_INFOS.")

    return by_email, all_entries


def score_candidate(source_email: str, candidate_email: str) -> float:
    s = norm(source_email)
    c = norm(candidate_email)
    if not s or not c:
        return 0.0

    s_local, _, s_domain = s.partition("@")
    c_local, _, c_domain = c.partition("@")

    whole = SequenceMatcher(None, s, c).ratio()
    local = SequenceMatcher(None, s_local, c_local).ratio() if s_local and c_local else 0.0

    score = (0.45 * whole) + (0.45 * local)

    if s_domain and c_domain and s_domain == c_domain:
        score += 0.10
    elif s_domain and c_domain and (s_domain in c_domain or c_domain in s_domain):
        score += 0.05

    if s_local and c_local and (s_local.startswith(c_local[:4]) or c_local.startswith(s_local[:4])):
        score += 0.05

    return min(score, 1.0)


def propose_candidates(source_email: str, entries: List[InfosEntry], top_k: int) -> List[Tuple[InfosEntry, float]]:
    scored = []
    seen = set()
    for entry in entries:
        if entry.email in seen:
            continue
        seen.add(entry.email)
        scored.append((entry, score_candidate(source_email, entry.email)))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]


def prompt_manual_match(source_email: str, candidates: List[Tuple[InfosEntry, float]], infos_by_email: Dict[str, InfosEntry]) -> Optional[str]:
    print("\n" + "=" * 78)
    print(f"[MATCH] Attendance email not found in infos: {source_email}")
    if candidates:
        print("Top candidate emails:")
        for i, (entry, score) in enumerate(candidates, start=1):
            label = f"{entry.email} | country='{entry.country or 'UNKNOWN'}'"
            if entry.name:
                label += f" | name='{entry.name}'"
            label += f" | score={score:.3f}"
            print(f"  {i}. {label}")
    else:
        print("No candidates available.")

    print("Type one of:")
    print("  - Candidate number")
    print("  - Full email from KUBESTRONAUTS_INFOS")
    print("  - 'skip' to continue without country")

    while True:
        ans = input("Your choice: ").strip()
        ans_l = ans.lower()

        if ans_l in {"", "skip", "s", "n", "no"}:
            return None

        if ans.isdigit():
            idx = int(ans) - 1
            if 0 <= idx < len(candidates):
                return candidates[idx][0].email
            print("Invalid candidate number.")
            continue

        typed = norm(ans)
        if typed in infos_by_email:
            return typed

        print("Email not found in KUBESTRONAUTS_INFOS. Try again or type 'skip'.")


def get_or_create_worksheet(spreadsheet, title: str, rows: int = 200, cols: int = 3):
    try:
        return spreadsheet.worksheet_by_title(title)
    except pygsheets.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=title, rows=rows, cols=cols)


def read_managed_tabs(meta_ws) -> List[str]:
    values = meta_ws.get_all_values(
        include_tailing_empty=False,
        include_tailing_empty_rows=False,
        returnas="matrix",
    )
    if len(values) <= 1:
        return []
    tabs = []
    for row in values[1:]:
        if row and row[0].strip():
            tabs.append(row[0].strip())
    return tabs


def write_managed_tabs(meta_ws, tab_titles: List[str]):
    values = [["Managed Event Tabs"]] + [[title] for title in tab_titles]
    meta_ws.clear()
    meta_ws.resize(rows=max(50, len(values) + 10), cols=1)
    meta_ws.update_values("A1", values)


def load_green_locked_participants(spreadsheet, tab_title: str) -> "OrderedDict[str, EventParticipant]":
    locked: "OrderedDict[str, EventParticipant]" = OrderedDict()
    try:
        ws = spreadsheet.worksheet_by_title(tab_title)
    except pygsheets.WorksheetNotFound:
        return locked

    values = ws.get_all_values(
        include_tailing_empty=False,
        include_tailing_empty_rows=False,
        returnas="matrix",
    )
    if len(values) <= 1:
        return locked

    for row_idx in range(2, len(values) + 1):
        row = values[row_idx - 1]
        email = norm(row[0] if len(row) > 0 else "")
        if not email:
            continue

        try:
            size_color = ws.cell((row_idx, 4)).color
        except Exception:
            size_color = None

        if not is_green_color(size_color):
            continue

        locked[email] = EventParticipant(
            email=email,
            name=(row[1] if len(row) > 1 else ""),
            country=(row[2] if len(row) > 2 else ""),
            size=(row[3] if len(row) > 3 else ""),
            highlight_yellow=False,
        )

    return locked


def load_existing_event_emails(spreadsheet, tab_title: str) -> Set[str]:
    try:
        ws = spreadsheet.worksheet_by_title(tab_title)
    except pygsheets.WorksheetNotFound:
        return set()

    values = ws.get_col(1, include_tailing_empty=False)
    existing = set()
    for raw in values[1:]:
        email = norm(raw)
        if email:
            existing.add(email)
    return existing


def update_event_tab(
    spreadsheet,
    tab_title: str,
    participants: OrderedDict,
    dry_run: bool,
) -> Tuple[int, int]:
    existing_emails = load_existing_event_emails(spreadsheet, tab_title)
    rows_to_add: List[List[str]] = []
    yellow_rows_count = 0

    for participant in participants.values():
        if participant.email in existing_emails:
            continue
        rows_to_add.append([
            participant.email,
            participant.name or "",
            participant.country or "UNKNOWN",
            participant.size or "",
        ])
        if participant.highlight_yellow:
            yellow_rows_count += 1

    if dry_run:
        print(
            f"[DRY-RUN] Would append {len(rows_to_add)} participant(s) to '{tab_title}' "
            f"and preserve {len(existing_emails)} existing row(s)"
        )
        return yellow_rows_count, len(existing_emails)

    ws = get_or_create_worksheet(spreadsheet, tab_title, rows=200, cols=4)
    current_values = ws.get_all_values(
        include_tailing_empty=False,
        include_tailing_empty_rows=False,
        returnas="matrix",
    )
    if not current_values:
        ws.update_values("A1", [["Email", "Name", "Country", "Size"]])
        current_values = [["Email", "Name", "Country", "Size"]]

    if rows_to_add:
        start_row = len(current_values) + 1
        ws.update_values(f"A{start_row}", rows_to_add)
        for idx, participant in enumerate((p for p in participants.values() if p.email not in existing_emails), start=start_row):
            if participant.highlight_yellow:
                for col_idx in range(1, 5):
                    ws.cell((idx, col_idx)).color = (1.0, 1.0, 0.0)

    return yellow_rows_count, len(existing_emails)


def main():
    parser = argparse.ArgumentParser(
        description="Create one tab per attendance event with participant email and country."
    )
    parser.add_argument("--service-file", default="kubestronauts-handling-service-file.json",
                        help="Google service account file")
    parser.add_argument("--env-file", default=".env", help="Path to .env file")
    parser.add_argument("--attendance-env", default="KUBESTRONAUT_ATTENDANCE_EVENT_2026",
                        help="Env var containing attendance spreadsheet key")
    parser.add_argument("--infos-env", default="KUBESTRONAUTS_INFOS",
                        help="Env var containing infos spreadsheet key")
    parser.add_argument("--manual-cache", default="Kubestronaut_manual_matching.json",
                        help="JSON file storing manual email mappings")
    parser.add_argument("--events-to-manage-tab", default="Events_To_Manage",
                        help="Worksheet listing the only events that should be processed")
    parser.add_argument("--exclude-events-file", default="AttendanceEvents_excluded_2026.txt",
                        help="Text file with one event per line to exclude from processing")
    parser.add_argument("--exclude-event", action="append", default=[],
                        help="Event name to exclude from processing (can be repeated)")
    parser.add_argument("--meta-tab", default="_ATTENDANCE_EVENTS_META",
                        help="Internal worksheet title used to track managed tabs")
    parser.add_argument("--top-k", type=int, default=5,
                        help="Number of candidate emails proposed for manual matching")
    parser.add_argument("--non-interactive", action="store_true",
                        help="Skip manual prompts and leave unknown countries when no match is found")
    parser.add_argument("--delete-obsolete-tabs", action="store_true",
                        help="Delete managed tabs that are no longer in the active event list")
    parser.add_argument("--dry-run", action="store_true",
                        help="Do not write any sheet or cache changes")
    args = parser.parse_args()

    if args.env_file and os.path.exists(args.env_file):
        load_dotenv(args.env_file)
    else:
        load_dotenv()

    attendance_key = os.getenv(args.attendance_env)
    infos_key = os.getenv(args.infos_env)

    if not attendance_key:
        raise SystemExit(f"Missing env var: {args.attendance_env}")
    if not infos_key:
        raise SystemExit(f"Missing env var: {args.infos_env}")
    if not os.path.exists(args.service_file):
        raise SystemExit(f"Service file not found: {args.service_file}")

    gc = pygsheets.authorize(service_file=args.service_file)

    attendance_sh = gc.open_by_key(attendance_key)
    attendance_ws = attendance_sh.sheet1

    infos_sh = gc.open_by_key(infos_key)
    infos_ws = infos_sh.sheet1

    infos_by_email, infos_entries = load_infos_index(infos_ws)
    print(f"[INFO] Loaded {len(infos_by_email)} unique emails from infos sheet.")

    manual_cache = load_manual_cache(args.manual_cache)
    expanded_cache = build_expanded_cache(manual_cache)
    cache_modified = False
    managed_events = load_events_to_manage(attendance_sh, args.events_to_manage_tab)
    excluded_events = load_excluded_events(args.exclude_events_file, args.exclude_event)

    attendance_values = attendance_ws.get_all_values(
        include_tailing_empty=False,
        include_tailing_empty_rows=False,
        returnas="matrix",
    )

    if not attendance_values or len(attendance_values) < 2:
        print("[INFO] Attendance sheet is empty, nothing to do.")
        return

    headers = attendance_values[0]
    email_idx, events_idx, timestamp_idx, swag_mention_idx = detect_attendance_columns(headers)

    events_map: OrderedDict[str, OrderedDict[str, EventParticipant]] = OrderedDict()
    unresolved_count = 0

    local_resolution_cache: Dict[str, Tuple[Optional[str], Optional[InfosEntry]]] = {}

    def resolve_infos_entry(source_email: str) -> Tuple[Optional[str], Optional[InfosEntry]]:
        nonlocal cache_modified, unresolved_count

        src = norm(source_email)
        if not src:
            return None, None

        if src in local_resolution_cache:
            return local_resolution_cache[src]

        if src in infos_by_email:
            out = (src, infos_by_email[src])
            local_resolution_cache[src] = out
            return out

        cached_target = expanded_cache.get(src)
        if cached_target and cached_target in infos_by_email:
            out = (cached_target, infos_by_email[cached_target])
            local_resolution_cache[src] = out
            return out

        if cached_target and cached_target not in infos_by_email:
            print(f"[WARN] Cached mapping is invalid: {src} -> {cached_target}")

        if args.non_interactive:
            unresolved_count += 1
            out = (None, None)
            local_resolution_cache[src] = out
            return out

        candidates = propose_candidates(src, infos_entries, max(1, args.top_k))
        chosen = prompt_manual_match(src, candidates, infos_by_email)
        if chosen and chosen in infos_by_email:
            manual_cache[src] = chosen
            expanded_cache[src] = chosen
            cache_modified = True
            out = (chosen, infos_by_email[chosen])
            local_resolution_cache[src] = out
            return out

        unresolved_count += 1
        out = (None, None)
        local_resolution_cache[src] = out
        return out

    highlighted_rows_count = 0
    preserved_existing_rows_count = 0
    for row_num, row in enumerate(attendance_values[1:], start=2):
        raw_email = row[email_idx] if email_idx < len(row) else ""
        raw_events = row[events_idx] if events_idx < len(row) else ""
        raw_timestamp = row[timestamp_idx] if timestamp_idx >= 0 and timestamp_idx < len(row) else ""
        raw_swag_mention = row[swag_mention_idx] if swag_mention_idx >= 0 and swag_mention_idx < len(row) else ""

        emails = extract_emails(raw_email)
        events = split_events(raw_events)

        if not emails or not events:
            continue

        for email in emails:
            matched_email, infos_entry = resolve_infos_entry(email)
            if matched_email is None or infos_entry is None:
                print(f"[WARN] Could not resolve country for '{email}' (row {row_num}, ts='{raw_timestamp}')")
            highlight_yellow = bool(
                has_meaningful_value(raw_swag_mention)
                and infos_entry is not None
                and has_meaningful_value(infos_entry.jacket_sent)
            )
            participant = EventParticipant(
                email=email,
                name=(infos_entry.name if infos_entry else ""),
                country=(infos_entry.country if infos_entry else "UNKNOWN"),
                size=(infos_entry.size if infos_entry else ""),
                highlight_yellow=highlight_yellow,
            )
            for event in events:
                normalized_event = compact_header(event)
                if normalized_event not in managed_events:
                    continue
                if normalized_event in excluded_events:
                    continue
                if event not in events_map:
                    events_map[event] = OrderedDict()
                existing = events_map[event].get(email)
                if existing:
                    existing.highlight_yellow = existing.highlight_yellow or participant.highlight_yellow
                    if not existing.name and participant.name:
                        existing.name = participant.name
                    if (not existing.country or existing.country == "UNKNOWN") and participant.country:
                        existing.country = participant.country
                    if not existing.size and participant.size:
                        existing.size = participant.size
                else:
                    events_map[event][email] = participant

    if not events_map:
        print("[INFO] No event participants found in attendance sheet.")
        return

    ordered_events = list(events_map.keys())
    title_map = make_unique_titles(ordered_events)
    managed_titles = [title_map[event] for event in ordered_events]

    meta_ws = None
    if args.dry_run:
        try:
            meta_ws = attendance_sh.worksheet_by_title(args.meta_tab)
        except pygsheets.WorksheetNotFound:
            meta_ws = None
    else:
        meta_ws = get_or_create_worksheet(attendance_sh, args.meta_tab, rows=200, cols=1)

    previous_managed_titles = read_managed_tabs(meta_ws) if meta_ws else []

    if args.delete_obsolete_tabs:
        for old_title in previous_managed_titles:
            if old_title == args.meta_tab:
                continue
            if old_title not in managed_titles:
                if args.dry_run:
                    print(f"[DRY-RUN] Would delete obsolete tab '{old_title}'")
                    continue
                try:
                    old_ws = attendance_sh.worksheet_by_title(old_title)
                    attendance_sh.del_worksheet(old_ws)
                    print(f"[INFO] Deleted obsolete tab: {old_title}")
                except pygsheets.WorksheetNotFound:
                    pass

    # Update current event tabs.
    for event in ordered_events:
        tab_title = title_map[event]
        participants = events_map[event]
        yellow_count, preserved_count = update_event_tab(
            attendance_sh,
            tab_title,
            participants,
            args.dry_run,
        )
        highlighted_rows_count += yellow_count
        preserved_existing_rows_count += preserved_count

    if args.dry_run:
        print(f"[DRY-RUN] Would update meta tab '{args.meta_tab}' with {len(managed_titles)} managed tabs")
    else:
        write_managed_tabs(meta_ws, managed_titles)

    if cache_modified and not args.dry_run:
        save_manual_cache(manual_cache, args.manual_cache)
        print(f"[INFO] Manual cache updated: {args.manual_cache}")

    print("\n[SUMMARY]")
    print(f"Events created/updated: {len(managed_titles)}")
    print(f"Unique attendance participants processed: {len(local_resolution_cache)}")
    print(f"Unresolved emails: {unresolved_count}")
    print(f"Managed events: {len(managed_events)}")
    print(f"Excluded events: {len(excluded_events)}")
    print(f"Highlighted rows (yellow): {highlighted_rows_count}")
    print(f"Existing rows preserved: {preserved_existing_rows_count}")
    print(f"Attendance spreadsheet: {attendance_sh.url}")


if __name__ == "__main__":
    main()
