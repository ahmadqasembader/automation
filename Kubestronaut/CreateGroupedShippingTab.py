import argparse
import os
import re
from datetime import datetime
from typing import Dict, Iterable, List, Optional

import pygsheets
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build


SERVICE_FILE = "kubestronauts-handling-service-file.json"
DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]
SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def compact_country_name(country: str) -> str:
    return re.sub(r"\s+", "", (country or "").strip())


def normalize_country_key(country: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (country or "").strip().lower())


def build_shipment_title(country: str, year_suffix: str, shipment_number: int) -> str:
    return f"{compact_country_name(country)}-{year_suffix}-{shipment_number}"


def matching_shipment_numbers(worksheet_titles: Iterable[str], country: str, year_suffix: str) -> List[int]:
    wanted_key = normalize_country_key(country)
    matches: List[int] = []
    pattern = re.compile(r"^(?P<country>.+)-(?P<year>\d{2})-(?P<number>\d+)$")

    for title in worksheet_titles:
        match = pattern.match((title or "").strip())
        if not match:
            continue
        if match.group("year") != year_suffix:
            continue
        if normalize_country_key(match.group("country")) != wanted_key:
            continue
        matches.append(int(match.group("number")))
    return sorted(matches)


def build_drive_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_FILE,
        scopes=DRIVE_SCOPES,
    )
    return build("drive", "v3", credentials=creds)


def build_sheets_client():
    return pygsheets.authorize(service_file=SERVICE_FILE)


def get_file_metadata(service, file_id: str) -> Dict:
    return service.files().get(
        fileId=file_id,
        fields="id,name,parents,owners(emailAddress,displayName),permissions(id,type,role,emailAddress,domain,allowFileDiscovery)",
        supportsAllDrives=True,
    ).execute()


def copy_template_spreadsheet(service, template_id: str, new_name: str) -> Dict:
    template_meta = get_file_metadata(service, template_id)
    body = {"name": new_name}
    if template_meta.get("parents"):
        body["parents"] = template_meta["parents"]

    copied = service.files().copy(
        fileId=template_id,
        body=body,
        supportsAllDrives=True,
        fields="id,name,webViewLink",
    ).execute()

    replicate_sharing_permissions(service, template_meta, copied["id"])
    return copied


def replicate_sharing_permissions(service, source_meta: Dict, target_file_id: str) -> None:
    service_account_email = None
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_FILE)
        service_account_email = creds.service_account_email
    except Exception:
        service_account_email = None

    owner_emails = {
        owner.get("emailAddress", "")
        for owner in source_meta.get("owners", [])
        if owner.get("emailAddress")
    }

    # The copied file is typically owned by the copier; explicitly share it back to the human owner(s).
    for owner_email in sorted(owner_emails):
        service.permissions().create(
            fileId=target_file_id,
            body={
                "type": "user",
                "role": "writer",
                "emailAddress": owner_email,
            },
            sendNotificationEmail=False,
            supportsAllDrives=True,
        ).execute()

    for permission in source_meta.get("permissions", []):
        perm_type = permission.get("type")
        role = permission.get("role")
        email = permission.get("emailAddress", "")
        domain = permission.get("domain", "")

        if role == "owner":
            continue
        if service_account_email and email == service_account_email:
            continue
        if owner_emails and email in owner_emails:
            continue

        body = {
            "type": perm_type,
            "role": role,
        }
        if perm_type == "user" and email:
            body["emailAddress"] = email
        if perm_type == "domain" and domain:
            body["domain"] = domain
        if "allowFileDiscovery" in permission:
            body["allowFileDiscovery"] = permission["allowFileDiscovery"]

        service.permissions().create(
            fileId=target_file_id,
            body=body,
            sendNotificationEmail=False,
            supportsAllDrives=True,
        ).execute()


def insert_grouped_shipping_tab(
    spreadsheet,
    title: str,
    volunteer_name: str,
    volunteer_email: str,
    linked_spreadsheet_url: str,
    group_label: str,
    to_be_confirmed: bool,
):
    worksheets = spreadsheet.worksheets()
    volunteer_indices = [idx for idx, ws in enumerate(worksheets) if ws.title == "VOLUNTEER"]
    if not volunteer_indices:
        raise ValueError("Worksheet 'VOLUNTEER' not found in grouped shipping reference spreadsheet.")

    insert_index = volunteer_indices[0] + 1
    worksheet = spreadsheet.add_worksheet(title=title, rows=100, cols=26, index=insert_index)
    worksheet.update_value("A10", group_label)
    worksheet.update_value("C15", volunteer_name)
    worksheet.update_value("C16", volunteer_email)
    worksheet.update_value("E10", f'=HYPERLINK("{linked_spreadsheet_url}", "{title}")')

    if to_be_confirmed:
        worksheet.apply_format(
            "C15:C16",
            {
                "backgroundColor": {
                    "red": 1.0,
                    "green": 0.95,
                    "blue": 0.4,
                }
            },
        )

    return worksheet


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a grouped shipping tab and a copied grouped shipping spreadsheet."
    )
    parser.add_argument("country", help="Country name used for the grouped shipment.")
    parser.add_argument("volunteer_name", help="Volunteer full name.")
    parser.add_argument("volunteer_email", help="Volunteer email.")
    parser.add_argument(
        "--to-be-confirmed",
        action="store_true",
        help="Highlight the volunteer name and email in yellow.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Compute names and positions without creating anything.",
    )
    args = parser.parse_args()

    load_dotenv(".env")
    ref_id = os.getenv("KUBESTRONAUT_GROUPED_SHIPPING_REF")
    template_id = os.getenv("KUBESTRONAUT_GROUPED_SHIPPING_TEMPLATE")
    if not ref_id or not template_id:
        raise ValueError("Missing KUBESTRONAUT_GROUPED_SHIPPING_REF or KUBESTRONAUT_GROUPED_SHIPPING_TEMPLATE in .env")

    year_suffix = f"{datetime.now().year % 100:02d}"
    country_display = compact_country_name(args.country)

    gc = build_sheets_client()
    ref_sheet = gc.open_by_key(ref_id)
    existing_titles = [ws.title for ws in ref_sheet.worksheets()]
    existing_numbers = matching_shipment_numbers(existing_titles, args.country, year_suffix)
    shipment_number = (max(existing_numbers) if existing_numbers else 0) + 1
    shipment_title = build_shipment_title(args.country, year_suffix, shipment_number)
    group_label = f"Grouped-{country_display}-{year_suffix}-{shipment_number}"

    if shipment_title in existing_titles:
        raise ValueError(f"Worksheet '{shipment_title}' already exists.")

    if args.dry_run:
        volunteer_indices = [idx for idx, ws in enumerate(ref_sheet.worksheets()) if ws.title == "VOLUNTEER"]
        insert_index = volunteer_indices[0] + 1 if volunteer_indices else None
        print("Grouped shipping reference spreadsheet:")
        print(f"https://docs.google.com/spreadsheets/d/{ref_id}")
        print("Planned worksheet title:")
        print(shipment_title)
        print("Planned insert index:")
        print(insert_index)
        print("Planned grouped label:")
        print(group_label)
        print("Volunteer:")
        print(f"{args.volunteer_name} <{args.volunteer_email}>")
        return

    drive_service = build_drive_service()
    copied_spreadsheet = copy_template_spreadsheet(drive_service, template_id, shipment_title)
    copied_url = copied_spreadsheet["webViewLink"]

    worksheet = None
    try:
        worksheet = insert_grouped_shipping_tab(
            spreadsheet=ref_sheet,
            title=shipment_title,
            volunteer_name=args.volunteer_name,
            volunteer_email=args.volunteer_email,
            linked_spreadsheet_url=copied_url,
            group_label=group_label,
            to_be_confirmed=args.to_be_confirmed,
        )
    except Exception:
        try:
            drive_service.files().delete(fileId=copied_spreadsheet["id"], supportsAllDrives=True).execute()
        except Exception:
            pass
        raise

    print("Grouped shipping reference spreadsheet:")
    print(f"https://docs.google.com/spreadsheets/d/{ref_id}")
    print("Created worksheet:")
    print(shipment_title)
    print("Worksheet gid:")
    print(worksheet.id)
    print("Copied spreadsheet:")
    print(copied_url)
    print("Grouped label:")
    print(group_label)


if __name__ == "__main__":
    main()
