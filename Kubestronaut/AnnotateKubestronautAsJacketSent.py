import argparse
import os

import pygsheets
from dotenv import load_dotenv

from AckKubestronautAndGKSwagShipped import (
    FALLBACK_EMAIL_COLUMN,
    FALLBACK_KUBESTRONAUT_SENT_COLUMN,
    annotate_email,
    resolve_infos_columns,
)


parser = argparse.ArgumentParser(
    description="Annotate the Kubestronaut sheet to reflect shipping associated to a Kubestronauts email"
)
parser.add_argument("-a", "--annotation", help="", required=True)
parser.add_argument("-e", "--email", help="", required=True)
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
args = parser.parse_args()

load_dotenv()
kubestronauts_infos = os.getenv("KUBESTRONAUTS_INFOS")
if not kubestronauts_infos:
    raise ValueError("Missing KUBESTRONAUTS_INFOS in .env")

gc = pygsheets.authorize(service_file="kubestronauts-handling-service-file.json")
sh = gc.open_by_key(kubestronauts_infos)
wks = sh[0]

email_column, kubestronaut_sent_column, _ = resolve_infos_columns(
    wks,
    email_column=args.email_column.strip().upper(),
    kubestronaut_sent_column=args.kubestronaut_sent_column.strip().upper(),
    golden_sent_columns=tuple(),
)
print(
    "KUBESTRONAUTS_INFOS columns: "
    f"email={email_column}, kubestronaut_shipped={kubestronaut_sent_column}"
)

_, message = annotate_email(
    infos_worksheet=wks,
    email=args.email,
    annotation=args.annotation,
    email_column=email_column,
    target_columns=(kubestronaut_sent_column,),
    dry_run=False,
)
print(message)
