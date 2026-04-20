import csv
import json
import gdown
import os
import re
from collections import OrderedDict
import argparse
import shutil
import pygsheets
from dotenv import load_dotenv

# In the same directory a file named Kubestronaut.tsv should contains the export
# of the Kubestronauts responses in tsv
# That script should access the people CNCF repo with the following path ../../people
parser = argparse.ArgumentParser(description='Add Kubestronaut to the people.json file')
parser.add_argument('-fl','--firstLine', help='First row number to be added from the tsv file', required=True)
parser.add_argument('-ll','--lastLine', help='Last row number to be added from the tsv file', required=True)
parser.add_argument('--force', action='store_true',
                    help='Force insertion for a single line even if the person already exists in people.json')
parser.add_argument('--manual-cache', default='Kubestronaut_manual_matching.json',
                    help='JSON file used to store manual email mappings for ACK')
parsed_args = parser.parse_args()
args = vars(parsed_args)

firstLineToBeInserted = int(args['firstLine'])
lastLineToBeInserted = int(args['lastLine'])
FORCE_INSERT = args['force']
MANUAL_CACHE_FILE = args['manual_cache']

if FORCE_INSERT and firstLineToBeInserted != lastLineToBeInserted:
    parser.error("--force only works for a single person, so --firstLine and --lastLine must be identical")


load_dotenv()
# Store credentials
KUBESTRONAUT_RECEIVERS = os.getenv('KUBESTRONAUT_RECEIVERS')

# Initialize the access to the GSheet to ACK Kubestronauts
gc = pygsheets.authorize(service_file='kubestronauts-handling-service-file.json')
#open the google spreadsheet
sh = gc.open_by_key(KUBESTRONAUT_RECEIVERS)
# Select the first sheet
issued = sh[0]
invited = sh.worksheet_by_title("Invited")
# Define elements used to ACK
NON_acked_Kubestronauts=[]
PENDING_manual_Kubestronauts=[]
SKIPPED_PEOPLE=[]
cell_f2 = issued.cell('F2')
bg_color_f2 = cell_f2.color
EMAIL_RE = re.compile(r'[\w.+-]+@[\w-]+\.[\w.-]+')


def norm_email(s):
    return (s or "").strip().lower()


def extract_emails(s):
    emails = [norm_email(e) for e in EMAIL_RE.findall(s or "")]
    dedup = []
    seen = set()
    for email in emails:
        if email and email not in seen:
            seen.add(email)
            dedup.append(email)
    return dedup


def load_manual_cache(cache_file):
    if not os.path.exists(cache_file):
        return {}
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)
        if isinstance(cache, dict):
            print(f"[INFO] Loaded {len(cache)} manual matches from cache: {cache_file}")
            return cache
        print(f"[WARN] Manual cache has invalid format in {cache_file}. Ignoring cache.")
    except Exception as e:
        print(f"[WARN] Could not load manual cache from {cache_file}: {e}")
    return {}


def save_manual_cache(cache, cache_file):
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        print(f"[INFO] Saved {len(cache)} manual matches to cache: {cache_file}")
    except Exception as e:
        print(f"[WARN] Could not save manual cache to {cache_file}: {e}")


def build_expanded_cache(cache):
    expanded = {}
    for raw_source, raw_target in cache.items():
        target = norm_email(raw_target)
        if not target:
            continue
        source_emails = extract_emails(raw_source)
        if not source_emails and "@" in (raw_source or ""):
            source_emails = [norm_email(raw_source)]
        for src in source_emails:
            if src:
                expanded[src] = target
    return expanded


def find_invited_cells(email):
    return invited.find(pattern=email, cols=(2,2), matchEntireCell=False)


def prompt_manual_match(source_email):
    print("\n" + "=" * 78)
    print(f"[MATCH] Email not found for ACK: {source_email}")
    print("Provide an email from the 'Invited' tab (column B) to continue.")
    print("Type 'skip' to leave this Kubestronaut as not ACKed for now.")
    print("-" * 78)

    while True:
        ans = input("Manual email (or 'skip'): ").strip()
        ans_lower = ans.lower()

        if ans_lower in ("", "skip", "s", "n", "no"):
            return None, None

        if "@" not in ans:
            print("Invalid email format. Try again or type 'skip'.")
            continue

        normalized = norm_email(ans)
        cells = find_invited_cells(normalized)
        if len(cells) == 1:
            return normalized, cells[0]
        if len(cells) == 0:
            print(f"Email '{normalized}' not found in Invited tab column B.")
        else:
            print(f"Email '{normalized}' matches multiple rows in Invited tab. Please provide a more specific email.")


manual_cache = load_manual_cache(MANUAL_CACHE_FILE)
expanded_manual_cache = build_expanded_cache(manual_cache)

class People:
    def __init__(self, name, bio, company, pronouns, location, linkedin, twitter, github, wechat, website, youtube, certdirectory, slack_id, image):
        self.name=name.strip().title()
        self.bio="<p>"+bio.replace("   ","<p/><p>")+"</p>"
        self.company=company
        self.pronouns=pronouns
        self.location=location

        if linkedin.startswith(("https","http")):
            self.linkedin=linkedin
        elif linkedin:
            if linkedin.startswith(("www")):
                self.linkedin="https://"+linkedin
            else:
                self.linkedin="https://www.linkedin.com/in/"+linkedin
        else:
            self.linkedin=""

        if twitter.startswith(("https","http")):
            self.twitter=twitter
        elif twitter :
            if twitter.startswith(("www")):
                self.twitter="https://"+twitter
            else:
                self.twitter="https://twitter.com/"+twitter
        else:
            self.twitter=""

        if github.startswith(("https","http")):
            self.github=github
        elif github:
            if github.startswith(("www")):
                self.github="https://"+github
            else:
                self.github="https://github.com/"+github
        else:
            self.github=""

        if wechat.startswith(("https","http")):
            self.wechat=wechat
        elif wechat:
            if wechat.startswith(("www")):
                self.wechat="https://"+wechat
            else:
                self.wechat="https://web.wechat.com/"+wechat
        else:
            self.wechat=""

        if website.startswith(("https","http")):
            self.website=website
        elif website:
            self.website="https://"+website
        else:
            self.website=""

        if youtube.startswith(("https","http")):
            self.youtube=youtube
        elif youtube:
            if youtube.startswith(("www")):
                self.youtube="https://"+youtube
            else:
                self.youtube="https://www.youtube.com/c/"+youtube
        else:
            self.youtube=""

        if certdirectory.startswith(("https","http")):
            self.certdirectory=certdirectory
        elif certdirectory :
            if certdirectory.startswith(("www")):
                self.certdirectory="https://"+certdirectory
            else:
                self.certdirectory="https://certdirectory.io/profile/"+certdirectory
        else:
            self.certdirectory=""

        self.category=["Kubestronaut"]
        self.slack_id=slack_id

        if (image) :
            url = image
            gdown.download(url, "imageTemp.jpg", fuzzy=True, quiet=False)
            output=name.lower().replace(" ","-")+".jpg"
        else :
            shutil.copy("phippy.jpg","imageTemp.jpg")
            output="phippy.jpg"
        self.image=output

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            indent=4)

def apply_ack(email_cell, ack_email, source_email):
    invited.update_value("G"+str(email_cell.row),"")
    cell=invited.cell("F"+str(email_cell.row))
    cell.color = bg_color_f2

    existing_emails = issued.get_col(2, include_tailing_empty=False)
    next_row = len(existing_emails) + 1
    # Insert a blank row before the next row
    issued.insert_rows(next_row - 1, number=1)

    # Add the email to column B in the newly inserted row
    issued.update_value(f"B{next_row}", ack_email)

    # Add the first name to column C and last name to column D
    issued.update_value(f"C{next_row}", invited.get_value("C"+str(email_cell.row)))
    issued.update_value(f"D{next_row}", invited.get_value("D"+str(email_cell.row)))

    # Set the background color of column F to green
    issued.cell(f"F{next_row}").color = (0, 1.0, 0.0)

    if norm_email(ack_email) == norm_email(source_email):
        print("Kubestronaut with email "+source_email+" : ACKed")
    else:
        print("Kubestronaut with email "+source_email+" : ACKed (matched as "+ack_email+")")


def ack_kubestronaut(raw_email):
    source_emails = extract_emails(raw_email)
    if not source_emails:
        normalized_raw = norm_email(raw_email)
        if normalized_raw:
            source_emails = [normalized_raw]

    candidates = []
    seen_candidates = set()

    for src in source_emails:
        if src not in seen_candidates:
            seen_candidates.add(src)
            candidates.append(src)

    for src in source_emails:
        cached = expanded_manual_cache.get(src)
        if cached and cached not in seen_candidates:
            seen_candidates.add(cached)
            candidates.append(cached)

    for candidate in candidates:
        list_kubestronauts_cells = find_invited_cells(candidate)
        number_matching_cells = len(list_kubestronauts_cells)

        if number_matching_cells == 1:
            apply_ack(list_kubestronauts_cells[0], candidate, raw_email)
            return

        if number_matching_cells > 1:
            print("Kubestronaut with email "+candidate+" found multiple times in Invited tab")

    # Not found with direct emails or cache -> queue for end-of-run manual matching
    print("Kubestronaut with email "+raw_email+" not found, queued for manual matching at end.")
    PENDING_manual_Kubestronauts.append(raw_email)


def process_pending_manual_matches():
    if not PENDING_manual_Kubestronauts:
        return

    print("\n\nManual matching required for the following Kubestronauts:")
    for email in PENDING_manual_Kubestronauts:
        print("\t"+email)

    for raw_email in PENDING_manual_Kubestronauts:
        source_emails = extract_emails(raw_email)
        if not source_emails:
            normalized_raw = norm_email(raw_email)
            if normalized_raw:
                source_emails = [normalized_raw]

        manual_email, manual_cell = prompt_manual_match(raw_email)
        if manual_email and manual_cell:
            apply_ack(manual_cell, manual_email, raw_email)
            for src in source_emails:
                manual_cache[src] = manual_email
                expanded_manual_cache[src] = manual_email
            save_manual_cache(manual_cache, MANUAL_CACHE_FILE)
            continue

        print("Kubestronaut with email "+raw_email+" not found !!")
        NON_acked_Kubestronauts.append(raw_email)


def record_skipped_person(line_number, person_name, reason, email=""):
    SKIPPED_PEOPLE.append({
        "line": line_number,
        "name": person_name,
        "email": email,
        "reason": reason,
    })


def print_skipped_people_summary():
    if not SKIPPED_PEOPLE:
        return

    print("\n\nSummary of skipped people:")
    for skipped in SKIPPED_PEOPLE:
        details = f"line {skipped['line']} - {skipped['name']}"
        if skipped["email"]:
            details += f" ({skipped['email']})"
        details += f" : {skipped['reason']}"
        print("\t"+details)


def cleanup_temp_image():
    if os.path.exists("imageTemp.jpg"):
        os.remove("imageTemp.jpg")



# Retrieve JSON data from the file
with open('../../people/people.json', "r+") as jsonfile:
#    print(jsonfile.read())
    data = json.load(jsonfile)


# Import CSV that needs to be treated
with open('Kubestronaut.tsv') as csv_file:
    lineCount = 1
    csv_reader = csv.reader(csv_file, delimiter='\t')
    
    for row in csv_reader:
        # Check if the current line is within the requested range
        if firstLineToBeInserted <= lineCount <= lastLineToBeInserted:
            if row[1]:
                print(f'\tProcessing line {lineCount}: {row[1]}')
                newPeople = People(name=row[1], bio=row[2], company=row[3], pronouns=row[4], location=row[5], linkedin=row[6], twitter=row[7], github=row[8], wechat=row[9], website=row[10], youtube=row[11], certdirectory=row[17], slack_id=row[13], image=row[14])
                
                print(newPeople.toJSON())

                # Check if person already exists
                name_exists = False
                for people in data:
                    if people["name"].lower() == newPeople.name.lower():
                        if FORCE_INSERT:
                            print(f"[WARN] {newPeople.name} already in people.json, but --force is enabled so the person will still be added.")
                        else:
                            print(f"[WARN] {newPeople.name} already in people.json, skipping...")
                        name_exists = True
                        break
                
                if name_exists and not FORCE_INSERT:
                    record_skipped_person(
                        line_number=lineCount,
                        person_name=newPeople.name,
                        reason="already exists in people.json",
                        email=row[12],
                    )
                    print(f"[INFO] Skipping people.json insert for {newPeople.name}, but continuing invited/issued processing.")
                    cleanup_temp_image()
                    ack_kubestronaut(row[12])
                    lineCount += 1
                    continue

                # If we reach here, name doesn't exist, so add it
                print('Adding '+newPeople.name)
                data.insert(0, json.JSONDecoder(object_pairs_hook=OrderedDict).decode(newPeople.toJSON()))
                # Move the downloaded image to the final destination
                final_image_path = "../../people/images/"+newPeople.image
                if os.path.exists("imageTemp.jpg"):
                    if os.path.exists(final_image_path):
                         os.remove(final_image_path)
                    os.rename("imageTemp.jpg", final_image_path)
                    
                ack_kubestronaut(row[12])

        lineCount += 1

# Sort the data before writing to maintain alphabetical order
process_pending_manual_matches()

sorted_people = sorted(data, key=lambda x: x['name'])

with open('../../people/people.json', "w", encoding='utf-8') as jsonfile:
    jsonfile.write(json.dumps(sorted_people, indent=4, ensure_ascii=False))

if NON_acked_Kubestronauts:
    print("\n\nList of Kubestroauts that were NOT ACKED:")
    for email_address in NON_acked_Kubestronauts:
        print("\t"+email_address)

print_skipped_people_summary()
