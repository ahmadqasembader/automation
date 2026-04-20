import argparse
import base64
import json
import os
import re
import unicodedata
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from typing import Dict, Iterable, List, Tuple
from urllib.parse import urlencode, urlparse

import pygsheets
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv


SERVICE_FILE = "kubestronauts-handling-service-file.json"
SHOP_DOMAIN = "https://store.cncf.io"
OUTPUT_WORKSHEET_TITLE = "Generated Cart"
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
DEFAULT_GMAIL_TEMPLATE_SUBJECT = "Confirmation of your shipping address for the Kubestronaut swags shipment and next steps"
STEP2_OPERATOR_EMAIL_ENV = "KUBESTRONAUT_STEP2_OPERATOR_EMAIL"
STEP2_BILLING_ADDRESS_ENV = "KUBESTRONAUT_STEP2_BILLING_ADDRESS"
SHOPIFY_VARIANT_IDS_FILE_ENV = "KUBESTRONAUT_SHOPIFY_VARIANT_IDS_FILE"
DEFAULT_SHOPIFY_VARIANT_IDS_FILE = "shopify-variant-ids.json"

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
SKU_RE = re.compile(r"^(CNCF-[A-Z0-9-]+)")


MEN_JACKET_SKU_PREFIX = "CNCF-10480"
WOMEN_JACKET_SKU_PREFIX = "CNCF-10479"
GOLDEN_BACKPACK_SKU = "CNCF-10598"
GOLDEN_BEANIE_SKU = "CNCF-10599"

SIZE_ALIASES = {
    "XS": "XS",
    "EXTRA SMALL": "XS",
    "S": "S",
    "SMALL": "S",
    "M": "M",
    "MEDIUM": "M",
    "L": "L",
    "LARGE": "L",
    "XL": "XL",
    "XLARGE": "XL",
    "X-LARGE": "XL",
    "EXTRALARGE": "XL",
    "EXTRA LARGE": "XL",
    "1XL": "XL",
    "2XL": "2XL",
    "2X": "2XL",
    "XXL": "2XL",
    "XX-LARGE": "2XL",
    "XX LARGE": "2XL",
    "2X-LARGE": "2XL",
    "2X LARGE": "2XL",
    "3XL": "3XL",
    "3X": "3XL",
    "XXXL": "3XL",
    "3X-LARGE": "3XL",
    "3X LARGE": "3XL",
    "4XL": "4XL",
    "4X": "4XL",
    "5XL": "5XL",
    "5X": "5XL",
}


@dataclass
class VolunteerInfo:
    first_name: str
    last_name: str
    full_name: str
    ascii_first_name: str
    ascii_last_name: str
    email: str
    phone: str
    street_number: str
    street_name: str
    address1: str
    address2: str
    ascii_address1: str
    ascii_address2: str
    city: str
    state: str
    postal_code: str
    country_code: str
    customs_code: str


@dataclass
class EmailDraftContent:
    subject: str
    body_text: str
    to_email: str
    from_name: str = ""
    mime_message: EmailMessage = None


def normalize_label(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").strip().lower())


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


def get_header_map(row: List[str]) -> Dict[str, int]:
    return {normalize_label(value): idx for idx, value in enumerate(row)}


def cell_value(row: List[str], header_map: Dict[str, int], header_name: str) -> str:
    idx = header_map.get(normalize_label(header_name))
    if idx is None or idx >= len(row):
        return ""
    return (row[idx] or "").strip()


def first_non_empty(*values: str) -> str:
    for value in values:
        if (value or "").strip():
            return value.strip()
    return ""


def load_shopify_variant_ids(path: str) -> Dict[str, int]:
    if not os.path.exists(path):
        raise ValueError(
            f"Missing Shopify variant ID file: {path}. "
            f"Set {SHOPIFY_VARIANT_IDS_FILE_ENV} or create {DEFAULT_SHOPIFY_VARIANT_IDS_FILE}."
        )

    with open(path, "r", encoding="utf-8") as fh:
        parsed = json.load(fh)

    if not isinstance(parsed, dict):
        raise ValueError(f"{path} must be a JSON object mapping SKU to Shopify variant ID.")

    variant_ids: Dict[str, int] = {}
    for sku, variant_id in parsed.items():
        sku = (sku or "").strip()
        try:
            variant_ids[sku] = int(variant_id)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid Shopify variant ID for SKU '{sku}': {variant_id}") from None

    return variant_ids


def load_country_code_map(worksheet) -> Dict[str, str]:
    country_map: Dict[str, str] = {}
    values = worksheet.get_all_values(
        returnas="matrix",
        include_tailing_empty=False,
        include_tailing_empty_rows=False,
    )
    for row in values:
        if len(row) < 2:
            continue
        code = (row[0] or "").strip().upper()
        definition = (row[1] or "").strip()
        if len(code) == 2 and definition:
            country_map[code] = definition
    return country_map


def load_volunteer_info(worksheet) -> VolunteerInfo:
    values = worksheet.get_all_values(
        returnas="matrix",
        include_tailing_empty=False,
        include_tailing_empty_rows=False,
    )
    if not values:
        raise ValueError("Volunteer_Info worksheet is empty.")

    header_map = get_header_map(values[0])
    matching_rows: List[VolunteerInfo] = []

    for row in values[1:]:
        email = cell_value(row, header_map, "Email")
        full_name = cell_value(row, header_map, "Full Name")
        street_number = cell_value(row, header_map, "Street Number")
        street_name = cell_value(row, header_map, "Street Name")
        legacy_address1 = cell_value(row, header_map, "Address Line 1")
        address1 = first_non_empty(
            " ".join(part for part in [street_number, street_name] if part).strip(),
            legacy_address1,
        )
        ascii_address1 = first_non_empty(
            cell_value(row, header_map, "ASCII Address Line 1"),
            sanitize_checkout_text(address1),
        )
        ascii_address2 = first_non_empty(
            cell_value(row, header_map, "ASCII Address Line 2"),
            sanitize_checkout_text(cell_value(row, header_map, "Address Line 2")),
        )
        first_name = cell_value(row, header_map, "Legal First Name")
        last_name = cell_value(row, header_map, "Legal Last Name")
        ascii_first_name = first_non_empty(
            cell_value(row, header_map, "ASCII First Name"),
            sanitize_checkout_text(first_name),
        )
        ascii_last_name = first_non_empty(
            cell_value(row, header_map, "ASCII Last Name"),
            sanitize_checkout_text(last_name),
        )
        if not full_name:
            full_name = " ".join(part for part in [first_name, last_name] if part).strip()
        if not any([email, full_name, address1]):
            continue
        matching_rows.append(
            VolunteerInfo(
                first_name=first_name,
                last_name=last_name,
                full_name=full_name,
                ascii_first_name=ascii_first_name,
                ascii_last_name=ascii_last_name,
                email=email,
                phone=cell_value(row, header_map, "Phone Number"),
                street_number=street_number,
                street_name=street_name,
                address1=address1,
                address2=cell_value(row, header_map, "Address Line 2"),
                ascii_address1=ascii_address1,
                ascii_address2=ascii_address2,
                city=cell_value(row, header_map, "City"),
                state=first_non_empty(
                    cell_value(row, header_map, "State / Province / Region"),
                    cell_value(row, header_map, "State"),
                ),
                postal_code=cell_value(row, header_map, "Postal Code"),
                country_code=cell_value(row, header_map, "Country Code").upper(),
                customs_code=cell_value(
                    row,
                    header_map,
                    "TAX ID/EORI/Personal Customs code (if applicable)",
                ),
            )
        )

    if not matching_rows:
        raise ValueError("Volunteer_Info does not contain a filled shipping row.")

    return matching_rows[0]


def extract_non_empty_column_values(worksheet, col: int = 1) -> List[str]:
    values = worksheet.get_col(col, include_tailing_empty=False)
    return [value.strip() for value in values if (value or "").strip()]


def normalize_size(value: str) -> str:
    raw = (value or "").strip().upper()
    raw = re.sub(r"\s+", " ", raw)
    raw = raw.replace("MEN'S", "MEN").replace("WOMEN'S", "WOMEN").replace("LADIES'", "LADIES")
    raw = raw.replace("LADIES", "").replace("WOMEN", "").replace("MEN", "")
    raw = raw.strip(" -")
    compact = raw.replace(" ", "")
    if compact in SIZE_ALIASES:
        return SIZE_ALIASES[compact]
    if raw in SIZE_ALIASES:
        return SIZE_ALIASES[raw]
    raise ValueError(f"Unsupported size label: '{value}'")


def gender_to_prefix(value: str) -> str:
    lowered = (value or "").strip().lower()
    if lowered in {"men", "mens", "men's", "male"}:
        return MEN_JACKET_SKU_PREFIX
    if lowered in {"women", "womens", "women's", "ladies", "lady", "female"}:
        return WOMEN_JACKET_SKU_PREFIX
    raise ValueError(f"Unsupported gender label: '{value}'")


def parse_kubestronaut_line(line: str) -> Tuple[str, str, str]:
    parts = [part.strip() for part in line.split(" - ") if part.strip()]
    if len(parts) < 4:
        raise ValueError(
            "Expected format similar to 'Name - email - Men/Women - Size - Address'"
        )

    email_idx = next((idx for idx, part in enumerate(parts) if EMAIL_RE.search(part)), None)
    if email_idx is None:
        raise ValueError(f"Could not find email in row: '{line}'")

    if email_idx + 2 >= len(parts):
        raise ValueError(f"Missing gender/size information in row: '{line}'")

    email = EMAIL_RE.search(parts[email_idx]).group(0).lower()
    gender = parts[email_idx + 1]
    size = parts[email_idx + 2]
    return email, gender, size


def build_quantities(kubestronaut_rows: Iterable[str], golden_rows: Iterable[str]) -> Counter:
    quantities: Counter = Counter()

    for line in kubestronaut_rows:
        _, gender, size = parse_kubestronaut_line(line)
        sku = f"{gender_to_prefix(gender)}-{normalize_size(size)}"
        quantities[sku] += 1

    golden_count = 0
    for line in golden_rows:
        if not EMAIL_RE.search(line):
            raise ValueError(f"Golden Kubestronaut row does not contain an email: '{line}'")
        golden_count += 1

    if golden_count:
        quantities[GOLDEN_BACKPACK_SKU] += golden_count
        quantities[GOLDEN_BEANIE_SKU] += golden_count

    return quantities


def build_variant_quantities(quantities: Counter, sku_to_variant_id: Dict[str, int]) -> List[Tuple[int, int]]:
    variant_quantities: List[Tuple[int, int]] = []

    for sku, quantity in sorted(quantities.items()):
        if quantity <= 0:
            continue

        if sku in sku_to_variant_id:
            variant_quantities.append((sku_to_variant_id[sku], quantity))
            continue

        raise ValueError(f"No Shopify variant ID configured for SKU '{sku}' in the Shopify variant ID JSON file.")

    return variant_quantities


def update_quantities_worksheet(worksheet, quantities: Counter) -> List[Tuple[str, int]]:
    values = worksheet.get_all_values(
        returnas="matrix",
        include_tailing_empty=False,
        include_tailing_empty_rows=False,
    )
    updated: List[Tuple[str, int]] = []

    for row_idx, row in enumerate(values[1:], start=2):
        sku_cell = (row[0] if row else "").strip()
        match = SKU_RE.match(sku_cell)
        if not match:
            continue

        sku = match.group(1)
        quantity = int(quantities.get(sku, 0))
        worksheet.update_value((row_idx, 2), str(quantity))
        updated.append((sku, quantity))

    return updated


def sanitize_checkout_text(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""

    replacements = {
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
    }
    for src, dst in replacements.items():
        value = value.replace(src, dst)

    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^A-Za-z0-9\s,./'#-]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def build_checkout_query(
    volunteer: VolunteerInfo,
    country_name: str,
    note: str,
    *,
    checkout_email: str,
    discount_code: str,
    ascii_safe: bool,
    include_shipping_address: bool,
) -> str:
    if ascii_safe:
        first_name = first_non_empty(volunteer.ascii_first_name, sanitize_checkout_text(volunteer.first_name))
        last_name = first_non_empty(volunteer.ascii_last_name, sanitize_checkout_text(volunteer.last_name))
        address1 = first_non_empty(volunteer.ascii_address1, sanitize_checkout_text(volunteer.address1))
        address2 = first_non_empty(volunteer.ascii_address2, sanitize_checkout_text(volunteer.address2))
        city = sanitize_checkout_text(volunteer.city)
        state = sanitize_checkout_text(volunteer.state)
        country = sanitize_checkout_text(country_name)
        note_value = sanitize_checkout_text(note)
        customs_value = sanitize_checkout_text(volunteer.customs_code)
    else:
        first_name = volunteer.first_name
        last_name = volunteer.last_name
        address1 = volunteer.address1
        address2 = volunteer.address2
        city = volunteer.city
        state = volunteer.state
        country = country_name
        note_value = note
        customs_value = volunteer.customs_code

    params = {
        "checkout[email]": checkout_email,
        "note": note_value,
    }
    if discount_code:
        params["discount"] = discount_code

    if customs_value:
        params["attributes[tax_id_eori]"] = customs_value
        params["attributes[customs_code]"] = customs_value

    if include_shipping_address:
        params.update(
            {
                "checkout[shipping_address][first_name]": first_name,
                "checkout[shipping_address][last_name]": last_name,
                "checkout[shipping_address][address1]": address1,
                "checkout[shipping_address][address2]": address2,
                "checkout[shipping_address][city]": city,
                "checkout[shipping_address][province]": state,
                "checkout[shipping_address][country]": country,
                "checkout[shipping_address][zip]": volunteer.postal_code,
            }
        )

    return urlencode({k: v for k, v in params.items() if v})


def build_note(spreadsheet_id: str, volunteer: VolunteerInfo, suffix: str = "") -> str:
    note = f"Kubestronaut volunteer spreadsheet {spreadsheet_id}"
    if suffix:
        note = f"{note} | {suffix}"
    if volunteer.customs_code:
        note = f"{note} | Customs: {volunteer.customs_code}"
    return note


def build_urls(
    variant_quantities: List[Tuple[int, int]],
    volunteer: VolunteerInfo,
    country_name: str,
    spreadsheet_id: str,
    step2_discount_code: str,
    step2_operator_email: str,
) -> Dict[str, str]:
    if not variant_quantities:
        raise ValueError("No products were derived from the spreadsheet.")

    cart_items = ",".join(f"{variant_id}:{quantity}" for variant_id, quantity in variant_quantities)
    base = f"{SHOP_DOMAIN}/cart/{cart_items}"
    validation_note = build_note(spreadsheet_id, volunteer, "Step 1 validation")
    payment_note = build_note(spreadsheet_id, volunteer, "Step 2 operator payment")

    validation_query = build_checkout_query(
        volunteer,
        country_name,
        validation_note,
        checkout_email=volunteer.email,
        discount_code="",
        ascii_safe=True,
        include_shipping_address=True,
    )

    recommended_query = build_checkout_query(
        volunteer,
        country_name,
        payment_note,
        checkout_email=step2_operator_email,
        discount_code=step2_discount_code,
        ascii_safe=True,
        include_shipping_address=True,
    )
    raw_query = build_checkout_query(
        volunteer,
        country_name,
        payment_note,
        checkout_email=step2_operator_email,
        discount_code=step2_discount_code,
        ascii_safe=False,
        include_shipping_address=True,
    )
    email_only_query = build_checkout_query(
        volunteer,
        country_name,
        payment_note,
        checkout_email=step2_operator_email,
        discount_code=step2_discount_code,
        ascii_safe=True,
        include_shipping_address=False,
    )

    return {
        "validation_checkout_url": f"{base}?{validation_query}",
        "validation_cart_url": f"{base}?{validation_query}&storefront=true",
        "recommended_checkout_url": f"{base}?{recommended_query}",
        "raw_checkout_url": f"{base}?{raw_query}",
        "cart_url": f"{base}?{recommended_query}&storefront=true",
        "email_only_checkout_url": f"{base}?{email_only_query}",
    }


def get_or_create_output_worksheet(spreadsheet, title: str = OUTPUT_WORKSHEET_TITLE):
    try:
        return spreadsheet.worksheet_by_title(title)
    except pygsheets.WorksheetNotFound:
        return spreadsheet.add_worksheet(title=title, rows=30, cols=2)


def render_summary_rows(
    spreadsheet_url: str,
    volunteer: VolunteerInfo,
    country_name: str,
    quantities: Counter,
    urls: Dict[str, str],
) -> List[List[str]]:
    volunteer_name = volunteer.full_name or f"{volunteer.first_name} {volunteer.last_name}".strip()
    address_summary = ", ".join(
        value
        for value in [
            volunteer.address1,
            volunteer.address2,
            volunteer.city,
            volunteer.state,
            volunteer.postal_code,
            volunteer.country_code,
        ]
        if value
    )
    rows: List[List[str]] = [
        ["Generated At (UTC)", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")],
        ["Volunteer", volunteer_name],
        ["Email", volunteer.email],
        ["Phone", volunteer.phone],
        ["", ""],
        ["Send This To Final User", ""],
        ["Validation Checkout URL", urls["validation_checkout_url"]],
        ["What They Must Send Back", "Confirmed or corrected shipping address + phone"],
        ["Step 1 Note", "Address from Volunteer_Info is prefilled when Shopify accepts it. User can edit it before sending the final version back."],
        ["", ""],
        ["SKU", "Quantity"],
    ]

    for sku in sorted(quantities):
        rows.append([sku, str(quantities[sku])])
    return rows


def update_grouped_shipping_reference_tab(
    gc,
    current_spreadsheet_title: str,
    volunteer_name: str,
    volunteer_email: str,
    recommended_checkout_url: str,
    phone: str,
    address_summary: str,
    discount_code: str,
    step2_operator_email: str,
    step2_billing_address: str,
) -> bool:
    ref_key = os.getenv("KUBESTRONAUT_GROUPED_SHIPPING_REF")
    if not ref_key:
        return False

    try:
        ref_sheet = gc.open_by_key(ref_key)
        ws = ref_sheet.worksheet_by_title(current_spreadsheet_title)
    except Exception:
        return False

    rows = [
        ["Step 2 - Use This Yourself After Address Validation", ""],
        ["Recommended Checkout URL", recommended_checkout_url],
        ["Step 2 Checkout Email", step2_operator_email],
        ["Phone To Type Manually", phone],
        ["Address To Keep In Volunteer_Info", address_summary],
        ["Billing Address To Use", step2_billing_address],
        ["Operator Note", "Shopify does not prefill phone, billing address, or the 'billing same as shipping' toggle from the permalink."],
    ]
    anchor_row = 0
    for pattern in [volunteer_name, volunteer_email]:
        if not pattern:
            continue
        try:
            matches = ws.find(pattern=pattern, matchEntireCell=False)
        except Exception:
            matches = []
        if matches:
            anchor_row = min(cell.row for cell in matches)
            break

    if not anchor_row:
        col_d_values = ws.get_col(4, include_tailing_empty=False)
        for idx, value in enumerate(col_d_values, start=1):
            if (value or "").strip():
                anchor_row = idx

    start_row = anchor_row + 3 if anchor_row else 3
    ws.update_values(f"G{start_row}", rows)
    return True


def build_step2_rows(
    recommended_checkout_url: str,
    phone: str,
    address_summary: str,
    discount_code: str,
    step2_operator_email: str,
    step2_billing_address: str,
) -> List[List[str]]:
    rows = [
        ["Step 2 - Use This Yourself After Address Validation", ""],
        ["Recommended Checkout URL", recommended_checkout_url],
        ["Step 2 Checkout Email", step2_operator_email],
        ["Phone To Type Manually", phone],
        ["Address To Keep In Volunteer_Info", address_summary],
        ["Billing Address To Use", step2_billing_address],
        ["Operator Note", "Shopify does not prefill phone, billing address, or the 'billing same as shipping' toggle from the permalink."],
    ]
    if discount_code:
        rows.append(["Step 2 Discount Code", discount_code])
    return rows


def build_email_placeholders(
    volunteer: VolunteerInfo,
    urls: Dict[str, str],
    quantities: Counter,
    spreadsheet_url: str,
) -> Dict[str, str]:
    quantity_lines = "\n".join(f"- {sku}: {quantities[sku]}" for sku in sorted(quantities))
    full_name = volunteer.full_name or f"{volunteer.first_name} {volunteer.last_name}".strip()
    return {
        "{{FIRST_NAME}}": volunteer.first_name,
        "{{LAST_NAME}}": volunteer.last_name,
        "{{FULL_NAME}}": full_name,
        "{{EMAIL}}": volunteer.email,
        "{{PHONE}}": volunteer.phone,
        "{{VALIDATION_CHECKOUT_URL}}": urls["validation_checkout_url"],
        "{{RECOMMENDED_CHECKOUT_URL}}": urls["recommended_checkout_url"],
        "{{VOLUNTEER_INFO_SPREADSHEET_URL}}": spreadsheet_url,
        "{{ITEMS}}": quantity_lines,
    }


def build_default_email_draft(
    volunteer: VolunteerInfo,
    urls: Dict[str, str],
    quantities: Counter,
    spreadsheet_url: str,
) -> EmailDraftContent:
    placeholders = build_email_placeholders(volunteer, urls, quantities, spreadsheet_url)
    subject = DEFAULT_GMAIL_TEMPLATE_SUBJECT
    body = (
        "Hello {{FIRST_NAME}},\n\n"
        "I am preparing your Kubestronaut shipment.\n\n"
        "Please open the link below and review the shipping information in Shopify:\n"
        "{{VALIDATION_CHECKOUT_URL}}\n\n"
        "What to do:\n"
        "1. Check the prefilled shipping address.\n"
        "2. Correct it if needed.\n"
        "3. Add your phone number if Shopify asks for it.\n"
        "4. Do not pay.\n"
        "5. Reply to this email with your final validated shipping address and phone number.\n\n"
        "Items in this shipment:\n"
        "{{ITEMS}}\n\n"
        "Thank you.\n"
    )
    for key, value in placeholders.items():
        body = body.replace(key, value or "")
        subject = subject.replace(key, value or "")
    message = EmailMessage()
    message["To"] = volunteer.email
    message["Subject"] = subject
    message.set_content(body)
    return EmailDraftContent(
        subject=subject,
        body_text=body,
        to_email=volunteer.email,
        mime_message=message,
    )


def extract_plain_text_from_message(message: EmailMessage) -> str:
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                continue
            disposition = (part.get_content_disposition() or "").lower()
            if disposition == "attachment" or part.get_filename():
                continue
            if part.get_content_type() == "text/plain":
                try:
                    return part.get_content()
                except Exception:
                    continue
    else:
        if message.get_content_type() == "text/plain":
            try:
                return message.get_content()
            except Exception:
                return ""
    return ""


def clone_message(message: EmailMessage) -> EmailMessage:
    return BytesParser(policy=policy.default).parsebytes(message.as_bytes())


def apply_placeholders_to_text(value: str, placeholders: Dict[str, str]) -> str:
    result = value or ""
    for key, replacement in placeholders.items():
        result = result.replace(key, replacement or "")
    return result


def apply_placeholders_to_mime_message(
    message: EmailMessage,
    placeholders: Dict[str, str],
    fallback_to_email: str,
    from_name: str = "",
) -> EmailMessage:
    message = clone_message(message)

    original_subject = message.get("Subject", "")
    if "Subject" in message:
        message.replace_header("Subject", apply_placeholders_to_text(original_subject, placeholders))
    else:
        message["Subject"] = apply_placeholders_to_text(original_subject, placeholders)

    original_to = message.get("To", "") or fallback_to_email
    replaced_to = apply_placeholders_to_text(original_to, placeholders) or fallback_to_email
    if "To" in message:
        message.replace_header("To", replaced_to)
    else:
        message["To"] = replaced_to

    if from_name:
        if "From" in message:
            del message["From"]
        message["From"] = from_name

    for part in message.walk():
        if part.is_multipart():
            continue
        disposition = (part.get_content_disposition() or "").lower()
        if disposition == "attachment" or part.get_filename():
            continue
        if part.get_content_maintype() != "text":
            continue

        try:
            original_content = part.get_content()
        except Exception:
            continue
        updated_content = apply_placeholders_to_text(original_content, placeholders)
        subtype = part.get_content_subtype()
        charset = part.get_content_charset() or "utf-8"
        content_disposition = part.get("Content-Disposition")
        content_id = part.get("Content-ID")

        part.set_content(updated_content, subtype=subtype, charset=charset)
        if content_disposition:
            part.replace_header("Content-Disposition", content_disposition)
        if content_id:
            if "Content-ID" in part:
                part.replace_header("Content-ID", content_id)
            else:
                part["Content-ID"] = content_id

    return message


def build_gmail_service(credentials_file: str, token_file: str):
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, GMAIL_SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, GMAIL_SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_file, "w", encoding="utf-8") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def load_gmail_template(service, draft_id: str = "", subject_query: str = "") -> EmailDraftContent:
    draft = None
    if draft_id:
        draft = service.users().drafts().get(userId="me", id=draft_id, format="raw").execute()
    elif subject_query:
        results = service.users().drafts().list(userId="me").execute()
        for item in results.get("drafts", []):
            candidate = service.users().drafts().get(userId="me", id=item["id"], format="raw").execute()
            raw = candidate.get("message", {}).get("raw", "")
            parsed = BytesParser(policy=policy.default).parsebytes(base64.urlsafe_b64decode(raw.encode("utf-8")))
            subject = parsed.get("Subject", "")
            if subject_query.lower() in subject.lower():
                draft = candidate
                break
    if not draft:
        raise ValueError("Could not find Gmail draft template.")

    raw = draft.get("message", {}).get("raw", "")
    parsed = BytesParser(policy=policy.default).parsebytes(base64.urlsafe_b64decode(raw.encode("utf-8")))
    subject = parsed.get("Subject", "")
    to_email = parsed.get("To", "")
    body_text = extract_plain_text_from_message(parsed)
    return EmailDraftContent(subject=subject, body_text=body_text, to_email=to_email, mime_message=parsed)


def apply_placeholders_to_email(template: EmailDraftContent, placeholders: Dict[str, str], fallback_to_email: str) -> EmailDraftContent:
    subject = template.subject
    body_text = template.body_text
    to_email = template.to_email or fallback_to_email
    for key, value in placeholders.items():
        subject = subject.replace(key, value or "")
        body_text = body_text.replace(key, value or "")
        to_email = to_email.replace(key, value or "")
    mime_message = None
    if template.mime_message is not None:
        mime_message = apply_placeholders_to_mime_message(
            template.mime_message,
            placeholders,
            fallback_to_email=fallback_to_email,
            from_name=template.from_name,
        )
        subject = mime_message.get("Subject", subject)
        to_email = mime_message.get("To", to_email)
        body_text = extract_plain_text_from_message(mime_message) or body_text
    return EmailDraftContent(
        subject=subject,
        body_text=body_text,
        to_email=to_email,
        from_name=template.from_name,
        mime_message=mime_message,
    )


def create_gmail_draft(service, draft: EmailDraftContent) -> str:
    message = clone_message(draft.mime_message) if draft.mime_message is not None else EmailMessage()
    if draft.mime_message is None:
        message["To"] = draft.to_email
        message["Subject"] = draft.subject
        message.set_content(draft.body_text)
    if draft.from_name:
        profile = service.users().getProfile(userId="me").execute()
        sender_email = profile.get("emailAddress", "")
        if sender_email:
            if "From" in message:
                del message["From"]
            message["From"] = f"{draft.from_name} <{sender_email}>"
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    created = service.users().drafts().create(
        userId="me",
        body={"message": {"raw": encoded_message}},
    ).execute()
    return created["id"]


def send_gmail_message(service, draft: EmailDraftContent) -> str:
    message = clone_message(draft.mime_message) if draft.mime_message is not None else EmailMessage()
    if draft.mime_message is None:
        message["To"] = draft.to_email
        message["Subject"] = draft.subject
        message.set_content(draft.body_text)
    if draft.from_name:
        profile = service.users().getProfile(userId="me").execute()
        sender_email = profile.get("emailAddress", "")
        if sender_email:
            if "From" in message:
                del message["From"]
            message["From"] = f"{draft.from_name} <{sender_email}>"
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    sent = service.users().messages().send(
        userId="me",
        body={"raw": encoded_message},
    ).execute()
    return sent["id"]


def update_output_worksheet(worksheet, rows: List[List[str]]) -> None:
    worksheet.clear()
    worksheet.update_values("A1", rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update Quantities and generate a Shopify cart/checkout permalink from a Google Spreadsheet."
    )
    parser.add_argument(
        "spreadsheet",
        help="Google Spreadsheet URL or spreadsheet key.",
    )
    parser.add_argument(
        "--service-file",
        default=SERVICE_FILE,
        help=f"Google service account JSON file (default: {SERVICE_FILE})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write changes back to the spreadsheet.",
    )
    parser.add_argument(
        "--recreate-step2",
        action="store_true",
        help="Recompute and print the Step 2 operator fields without writing anything.",
    )
    parser.add_argument(
        "--render-email",
        action="store_true",
        help="Render the email subject/body in stdout and Generated Cart.",
    )
    parser.add_argument(
        "--gmail-create-draft",
        action="store_true",
        help="Create a Gmail draft using OAuth credentials.",
    )
    parser.add_argument(
        "--gmail-send",
        action="store_true",
        help="Send the email directly with Gmail instead of creating a draft.",
    )
    parser.add_argument(
        "--gmail-credentials-file",
        default="credentials.json",
        help="OAuth client credentials JSON for Gmail draft creation.",
    )
    parser.add_argument(
        "--gmail-token-file",
        default="gmail-token.json",
        help="OAuth token JSON cache for Gmail draft creation.",
    )
    parser.add_argument(
        "--gmail-template-draft-id",
        default="",
        help="Existing Gmail draft id to use as a template.",
    )
    parser.add_argument(
        "--gmail-template-subject",
        default=DEFAULT_GMAIL_TEMPLATE_SUBJECT,
        help="Substring to search in Gmail draft subjects when selecting a template.",
    )
    parser.add_argument(
        "--from-name",
        default="",
        help="Display name to set in the From header for Gmail drafts/sends.",
    )
    args = parser.parse_args()

    if args.gmail_create_draft and args.gmail_send:
        parser.error("--gmail-create-draft and --gmail-send are mutually exclusive")
    if args.recreate_step2 and (args.gmail_create_draft or args.gmail_send):
        parser.error("--recreate-step2 cannot be combined with Gmail send/draft actions")

    spreadsheet_id = parse_spreadsheet_id(args.spreadsheet)
    spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"
    if args.recreate_step2:
        args.dry_run = True

    load_dotenv(".env")
    gc = pygsheets.authorize(service_file=args.service_file)
    sh = gc.open_by_key(spreadsheet_id)

    volunteer_ws = find_worksheet(sh, "Volunteer_Info", "Volunteer_info")
    kubestronauts_ws = find_worksheet(sh, "Kubestronauts")
    golden_ws = find_worksheet(sh, "Golden Kubestronauts", "GoldenKubestronauts")
    quantities_ws = find_worksheet(sh, "Quantities", "Quantitites")
    countries_ws = find_worksheet(sh, "ISO 2-Digit Alpha Country Code")

    volunteer = load_volunteer_info(volunteer_ws)
    country_map = load_country_code_map(countries_ws)
    country_name = country_map.get(volunteer.country_code, volunteer.country_code)
    address_summary = ", ".join(
        value
        for value in [
            volunteer.address1,
            volunteer.address2,
            volunteer.city,
            volunteer.state,
            volunteer.postal_code,
            volunteer.country_code,
        ]
        if value
    )
    step2_discount_code = (os.getenv("KUBESTRONAUT_SHIPPING_DISCOUNT") or "").strip()
    step2_operator_email = (os.getenv(STEP2_OPERATOR_EMAIL_ENV) or "").strip()
    if not step2_operator_email:
        raise ValueError(f"Missing {STEP2_OPERATOR_EMAIL_ENV} in .env")
    step2_billing_address = (os.getenv(STEP2_BILLING_ADDRESS_ENV) or "").strip()
    if not step2_billing_address:
        raise ValueError(f"Missing {STEP2_BILLING_ADDRESS_ENV} in .env")
    shopify_variant_ids_file = (
        os.getenv(SHOPIFY_VARIANT_IDS_FILE_ENV) or DEFAULT_SHOPIFY_VARIANT_IDS_FILE
    ).strip()
    sku_to_variant_id = load_shopify_variant_ids(shopify_variant_ids_file)

    kubestronaut_rows = extract_non_empty_column_values(kubestronauts_ws)
    golden_rows = extract_non_empty_column_values(golden_ws)
    quantities = build_quantities(kubestronaut_rows, golden_rows)
    variant_quantities = build_variant_quantities(quantities, sku_to_variant_id)
    urls = build_urls(
        variant_quantities,
        volunteer,
        country_name,
        spreadsheet_id,
        step2_discount_code,
        step2_operator_email,
    )
    email_draft = None
    gmail_draft_id = ""
    gmail_message_id = ""

    if args.render_email or args.gmail_create_draft or args.gmail_send:
        placeholders = build_email_placeholders(volunteer, urls, quantities, spreadsheet_url)
        if args.gmail_template_draft_id or args.gmail_template_subject:
            service = build_gmail_service(args.gmail_credentials_file, args.gmail_token_file)
            template = load_gmail_template(
                service,
                draft_id=args.gmail_template_draft_id,
                subject_query=args.gmail_template_subject,
            )
            email_draft = apply_placeholders_to_email(template, placeholders, volunteer.email)
        else:
            email_draft = build_default_email_draft(volunteer, urls, quantities, spreadsheet_url)

        if email_draft and args.from_name:
            email_draft.from_name = args.from_name

        if args.gmail_create_draft:
            service = service if "service" in locals() else build_gmail_service(args.gmail_credentials_file, args.gmail_token_file)
            gmail_draft_id = create_gmail_draft(service, email_draft)
        if args.gmail_send:
            service = service if "service" in locals() else build_gmail_service(args.gmail_credentials_file, args.gmail_token_file)
            gmail_message_id = send_gmail_message(service, email_draft)

    if not args.dry_run:
        update_quantities_worksheet(quantities_ws, quantities)
        output_ws = get_or_create_output_worksheet(sh)
        summary_rows = render_summary_rows(
            spreadsheet_url=spreadsheet_url,
            volunteer=volunteer,
            country_name=country_name,
            quantities=quantities,
            urls=urls,
        )
        update_output_worksheet(output_ws, summary_rows)
        update_grouped_shipping_reference_tab(
            gc=gc,
            current_spreadsheet_title=sh.title,
            volunteer_name=volunteer.full_name or f"{volunteer.first_name} {volunteer.last_name}".strip(),
            volunteer_email=volunteer.email,
            recommended_checkout_url=urls["recommended_checkout_url"],
            phone=volunteer.phone,
            address_summary=address_summary,
            discount_code=step2_discount_code,
            step2_operator_email=step2_operator_email,
            step2_billing_address=step2_billing_address,
        )

    print("Spreadsheet:", spreadsheet_url)
    print("Volunteer:", volunteer.full_name or f"{volunteer.first_name} {volunteer.last_name}".strip())
    print("Quantities:")
    for sku in sorted(quantities):
        print(f"  {sku}: {quantities[sku]}")
    print("Validation checkout URL:")
    print(urls["validation_checkout_url"])
    print("Recommended checkout URL:")
    print(urls["recommended_checkout_url"])
    print("Step 2 checkout email:")
    print(step2_operator_email)
    print("Step 2 discount code:")
    print(step2_discount_code or "[none]")
    print("Phone to enter manually at checkout:")
    print(volunteer.phone or "[missing phone number in Volunteer_Info]")
    step2_rows = build_step2_rows(
        recommended_checkout_url=urls["recommended_checkout_url"],
        phone=volunteer.phone,
        address_summary=address_summary,
        discount_code=step2_discount_code,
        step2_operator_email=step2_operator_email,
        step2_billing_address=step2_billing_address,
    )
    print("Step 2 rows:")
    for label, value in step2_rows:
        if value:
            print(f"  {label}: {value}")
        else:
            print(f"  {label}")
    if args.recreate_step2:
        print("Recreate Step 2 mode:")
        print("  No spreadsheet was modified.")
    if email_draft:
        print("Email subject:")
        print(email_draft.subject)
        print("Email to:")
        print(email_draft.to_email)
        if email_draft.from_name:
            print("Email from name:")
            print(email_draft.from_name)
        print("Email body:")
        print(email_draft.body_text)
    if gmail_draft_id:
        print("Gmail draft id:")
        print(gmail_draft_id)
    if gmail_message_id:
        print("Gmail message id:")
        print(gmail_message_id)


if __name__ == "__main__":
    main()
