import argparse
import os

import pygsheets
from dotenv import load_dotenv

from AckKubestronautAndGKSwagShipped import (
    FALLBACK_EMAIL_COLUMN,
    FALLBACK_GOLDEN_SENT_COLUMNS,
    annotate_email,
    parse_column_letters,
    resolve_infos_columns,
)


parser = argparse.ArgumentParser(
    description="Annotate the Kubestronaut sheet to reflect shipping associated to a Golden Kubestronauts email"
)
parser.add_argument("-a", "--annotation", help="", required=True)
parser.add_argument("-e", "--email", help="", required=True)
parser.add_argument(
    "--email-column",
    default="",
    help=f"Column containing emails in KUBESTRONAUTS_INFOS. Default: auto-detect, then {FALLBACK_EMAIL_COLUMN}.",
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
kubestronauts_infos = os.getenv("KUBESTRONAUTS_INFOS")
if not kubestronauts_infos:
    raise ValueError("Missing KUBESTRONAUTS_INFOS in .env")

golden_sent_columns_arg = parse_column_letters(args.golden_sent_columns)
if golden_sent_columns_arg and len(golden_sent_columns_arg) != 2:
    raise ValueError("--golden-sent-columns must contain exactly two columns, for example AB,AC")

gc = pygsheets.authorize(service_file="kubestronauts-handling-service-file.json")
sh = gc.open_by_key(kubestronauts_infos)
wks = sh[0]

email_column, _, golden_sent_columns = resolve_infos_columns(
    wks,
    email_column=args.email_column.strip().upper(),
    kubestronaut_sent_column="",
    golden_sent_columns=tuple(golden_sent_columns_arg),
)
print(
    "KUBESTRONAUTS_INFOS columns: "
    f"email={email_column}, golden_shipped={','.join(golden_sent_columns)}"
)

_, message = annotate_email(
    infos_worksheet=wks,
    email=args.email,
    annotation=args.annotation,
    email_column=email_column,
    target_columns=golden_sent_columns,
    dry_run=False,
)
print(message)
