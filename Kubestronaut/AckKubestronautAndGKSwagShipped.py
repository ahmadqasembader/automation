import argparse
import os
import re
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlparse

import pygsheets
from dotenv import load_dotenv


SERVICE_FILE = "kubestronauts-handling-service-file.json"
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
FALLBACK_EMAIL_COLUMN = "M"
FALLBACK_KUBESTRONAUT_SENT_COLUMN = "U"
FALLBACK_GOLDEN_SENT_COLUMNS = ("AB", "AC")


def normalize_label(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").strip().lower())


def normalize_header(value: str) -> str:
    return " ".join((value or "").strip().lower().split())


def parse_spreadsheet_id(spreadsheet_ref: str) -> str:
    parsed = urlparse(spreadsheet_ref)
    if parsed.scheme and parsed.netloc:
        match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", spreadsheet_ref)
        if not match:
            raise ValueError(f"Could not extract spreadsheet key from URL: {spreadsheet_ref}")
        return match.group(1)
    return spreadsheet_ref.strip()


def find_worksheet(spreadsheet, *candidate_titles: str):
    normalized_to_ws = {normalize_label(ws.title): ws for ws in spreadsheet.worksheets()}
    for candidate in candidate_titles:
        ws = normalized_to_ws.get(normalize_label(candidate))
        if ws:
            return ws
    raise pygsheets.WorksheetNotFound(
        f"Worksheet not found. Tried: {', '.join(candidate_titles)}"
    )


def extract_emails_from_first_column(worksheet) -> List[str]:
    rows = worksheet.get_col(1, include_tailing_empty=False)
    emails: List[str] = []
    seen = set()

    for row in rows:
        match = EMAIL_RE.search(row or "")
        if not match:
            continue
        email = match.group(0).strip()
        key = email.lower()
        if key in seen:
            continue
        seen.add(key)
        emails.append(email)

    return emails


def column_index_to_letter(index1: int) -> str:
    if index1 < 1:
        raise ValueError(f"Invalid 1-based column index: {index1}")

    value = index1
    output = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        output = chr(65 + remainder) + output
    return output


def column_letter_to_index(column_letter: str) -> int:
    value = 0
    for char in (column_letter or "").strip().upper():
        if char < "A" or char > "Z":
            raise ValueError(f"Invalid column letter: {column_letter}")
        value = value * 26 + (ord(char) - ord("A") + 1)
    if value < 1:
        raise ValueError(f"Invalid column letter: {column_letter}")
    return value


def parse_column_letters(value: str) -> List[str]:
    columns = [part.strip().upper() for part in (value or "").split(",") if part.strip()]
    for column in columns:
        column_letter_to_index(column)
    return columns


def get_header_row(worksheet) -> List[str]:
    values = worksheet.get_all_values(
        returnas="matrix",
        include_tailing_empty=False,
        include_tailing_empty_rows=False,
    )
    if not values:
        raise RuntimeError("KUBESTRONAUTS_INFOS appears empty.")
    return values[0]


def detect_infos_columns(headers: List[str]) -> Dict[str, Optional[str]]:
    normalized = [normalize_header(header) for header in headers]
    compacted = [normalize_label(header) for header in headers]
    columns: Dict[str, Optional[str]] = {
        "email": None,
        "kubestronaut_sent": None,
        "golden_beanie": None,
        "golden_backpack": None,
    }

    for index, header in enumerate(normalized):
        compact = compacted[index]
        column = column_index_to_letter(index + 1)

        if columns["email"] is None and (header == "email" or compact == "email"):
            columns["email"] = column

        if columns["email"] is None and (
            "preferred email address" in header
            and "kubestronaut communications" in header
        ):
            columns["email"] = column

        if columns["kubestronaut_sent"] is None and (
            compact == "jacketsent" or ("jacket" in header and "sent" in header)
        ):
            columns["kubestronaut_sent"] = column

        if columns["golden_beanie"] is None and (
            compact == "gkbeanie"
            or "gkbeanie" in compact
            or ("beanie" in header and ("gk" in header or "golden" in header))
        ):
            columns["golden_beanie"] = column

        if columns["golden_backpack"] is None and (
            compact == "gkbackpack"
            or "gkbackpack" in compact
            or ("backpack" in header and ("gk" in header or "golden" in header))
        ):
            columns["golden_backpack"] = column

    if columns["email"] is None:
        for index, header in enumerate(normalized):
            if "email" in header:
                columns["email"] = column_index_to_letter(index + 1)
                break

    return columns


def resolve_infos_columns(
    worksheet,
    email_column: str,
    kubestronaut_sent_column: str,
    golden_sent_columns: Tuple[str, str],
) -> Tuple[str, str, Tuple[str, str]]:
    headers = get_header_row(worksheet)
    detected = detect_infos_columns(headers)

    resolved_email = (email_column or detected["email"] or FALLBACK_EMAIL_COLUMN).upper()
    resolved_kubestronaut = (
        kubestronaut_sent_column
        or detected["kubestronaut_sent"]
        or FALLBACK_KUBESTRONAUT_SENT_COLUMN
    ).upper()

    detected_golden = [
        column
        for column in [detected["golden_beanie"], detected["golden_backpack"]]
        if column
    ]
    if golden_sent_columns:
        resolved_golden = golden_sent_columns
    elif len(detected_golden) == 2:
        resolved_golden = (detected_golden[0].upper(), detected_golden[1].upper())
    else:
        resolved_golden = FALLBACK_GOLDEN_SENT_COLUMNS

    return resolved_email, resolved_kubestronaut, resolved_golden


def annotate_email(
    infos_worksheet,
    email: str,
    annotation: str,
    email_column: str,
    target_columns: Iterable[str],
    dry_run: bool,
) -> Tuple[str, str]:
    email_column_index = column_letter_to_index(email_column)
    matching_cells = infos_worksheet.find(
        pattern=email,
        cols=(email_column_index, email_column_index),
        matchEntireCell=True,
    )
    number_matching_cells = len(matching_cells)

    if number_matching_cells == 1:
        email_cell = matching_cells[0]
        targets = [f"{col}{email_cell.row}" for col in target_columns]
        if not dry_run:
            for target in targets:
                infos_worksheet.update_value(target, annotation)
        return "ok", f"{email} : OK ({', '.join(targets)})"

    if number_matching_cells == 0:
        return "not_found", f"Kubestronaut with email {email} not found !!"

    return "multiple", f"Kubestronaut with email {email} found multiple times !!"


def annotate_batch(
    infos_worksheet,
    emails: List[str],
    annotation: str,
    email_column: str,
    target_columns: Iterable[str],
    label: str,
    dry_run: bool,
) -> Dict[str, List[str]]:
    results = {
        "ok": [],
        "not_found": [],
        "multiple": [],
    }
    print(f"\n{label}: {len(emails)} email(s) to annotate")

    for email in emails:
        status, message = annotate_email(
            infos_worksheet=infos_worksheet,
            email=email,
            annotation=annotation,
            email_column=email_column,
            target_columns=target_columns,
            dry_run=dry_run,
        )
        results[status].append(email)
        print(message)

    return results


def print_failures(results_by_label: Dict[str, Dict[str, List[str]]]) -> None:
    for label, results in results_by_label.items():
        failures = results["not_found"] + results["multiple"]
        if not failures:
            continue

        print(f"\nList of {label} that were NOT ACKED:")
        for email in failures:
            print(f"\t{email}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Annotate KUBESTRONAUTS_INFOS for shipped Kubestronaut jackets and "
            "Golden Kubestronaut swags from a grouped shipping spreadsheet."
        )
    )
    parser.add_argument(
        "spreadsheet",
        help="Grouped shipping spreadsheet URL or key, same input style as GenerateShopifyCartFromSpreadsheet.py.",
    )
    parser.add_argument(
        "annotation",
        help="Value to write in the shipped columns.",
    )
    parser.add_argument(
        "--service-file",
        default=SERVICE_FILE,
        help=f"Google service account JSON file (default: {SERVICE_FILE})",
    )
    parser.add_argument(
        "--infos-env",
        default="KUBESTRONAUTS_INFOS",
        help="Environment variable containing the KUBESTRONAUTS_INFOS spreadsheet key.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the updates that would be made without writing to KUBESTRONAUTS_INFOS.",
    )
    parser.add_argument(
        "--email-column",
        default="",
        help=f"Column containing emails in KUBESTRONAUTS_INFOS. Default: auto-detect, then {FALLBACK_EMAIL_COLUMN}.",
    )
    parser.add_argument(
        "--kubestronaut-sent-column",
        default="",
        help=(
            "Column to update for Kubestronaut jacket shipping. "
            f"Default: auto-detect, then {FALLBACK_KUBESTRONAUT_SENT_COLUMN}."
        ),
    )
    parser.add_argument(
        "--golden-sent-columns",
        default="",
        help=(
            "Comma-separated columns to update for Golden Kubestronaut swags. "
            f"Default: auto-detect, then {','.join(FALLBACK_GOLDEN_SENT_COLUMNS)}."
        ),
    )
    args = parser.parse_args()

    load_dotenv()
    infos_spreadsheet_id = os.getenv(args.infos_env)
    if not infos_spreadsheet_id:
        raise ValueError(f"Missing {args.infos_env} in .env")

    gc = pygsheets.authorize(service_file=args.service_file)
    source_spreadsheet_id = parse_spreadsheet_id(args.spreadsheet)
    source_sheet = gc.open_by_key(source_spreadsheet_id)
    infos_sheet = gc.open_by_key(infos_spreadsheet_id)
    infos_worksheet = infos_sheet[0]
    golden_sent_columns_arg = parse_column_letters(args.golden_sent_columns)
    if golden_sent_columns_arg and len(golden_sent_columns_arg) != 2:
        raise ValueError("--golden-sent-columns must contain exactly two columns, for example AB,AC")
    email_column, kubestronaut_sent_column, golden_sent_columns = resolve_infos_columns(
        infos_worksheet,
        email_column=args.email_column.strip().upper(),
        kubestronaut_sent_column=args.kubestronaut_sent_column.strip().upper(),
        golden_sent_columns=tuple(golden_sent_columns_arg),
    )

    kubestronauts_ws = find_worksheet(source_sheet, "Kubestronauts")
    golden_ws = find_worksheet(source_sheet, "Golden Kubestronauts", "GoldenKubestronauts")

    kubestronaut_emails = extract_emails_from_first_column(kubestronauts_ws)
    golden_emails = extract_emails_from_first_column(golden_ws)

    if args.dry_run:
        print("DRY RUN: no write will be made.")
    print(
        "KUBESTRONAUTS_INFOS columns: "
        f"email={email_column}, kubestronaut_shipped={kubestronaut_sent_column}, "
        f"golden_shipped={','.join(golden_sent_columns)}"
    )

    results_by_label = {
        "Kubestronauts": annotate_batch(
            infos_worksheet=infos_worksheet,
            emails=kubestronaut_emails,
            annotation=args.annotation,
            email_column=email_column,
            target_columns=(kubestronaut_sent_column,),
            label="Kubestronauts jacket shipped",
            dry_run=args.dry_run,
        ),
        "Golden Kubestronauts": annotate_batch(
            infos_worksheet=infos_worksheet,
            emails=golden_emails,
            annotation=args.annotation,
            email_column=email_column,
            target_columns=golden_sent_columns,
            label="Golden Kubestronauts swags shipped",
            dry_run=args.dry_run,
        ),
    }

    print_failures(results_by_label)

    total_ok = sum(len(results["ok"]) for results in results_by_label.values())
    total_failed = sum(
        len(results["not_found"]) + len(results["multiple"])
        for results in results_by_label.values()
    )
    print(f"\nSummary: {total_ok} ACKed, {total_failed} failed.")


if __name__ == "__main__":
    main()
