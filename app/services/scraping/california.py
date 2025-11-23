import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Dict, Tuple            
import re
import time

BASE_URL = "https://apps.calbar.ca.gov/attorney/LicenseeSearch/AdvancedSearch"
DETAIL_URL = "https://apps.calbar.ca.gov/attorney/LicenseeSearch/Detail/{}"
features = [
    "Name",
    "Bar Number",
    "License Status",
    "Address",
    "Phone",
    "Email",
    "Additional Languages spoken",
    "Law School",
    "Date Admitted to Bar",
    "Certified Legal Specialty",
    "Practice Areas (self)"
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def clean_str(raw: str):
    if not raw:
        return ""
    cleaned = raw.strip().lstrip(":").strip()
    cleaned = " ".join(cleaned.split()) # collapse spaces
    return cleaned

def extract_website_and_email_fields(soup) -> Tuple[str, str]:
    email_pattern = re.compile(rf"{"Email"}:", re.IGNORECASE)
    website_pattern = re.compile(rf"{"Website"}:", re.IGNORECASE)
    email_nodes   = soup.find_all(string=lambda t: t and email_pattern.search(t) is not None)
    website_nodes = soup.find_all(string=lambda t: t and website_pattern.search(t) is not None)
    
    website = ""
    for node in website_nodes: # only be 1
        element = node.parent
        if not element: 
            continue
        for child in element.children:
            if child.name == "span":
                continue
            print(child)
            website = child.get_text(" ", strip=True)
            break
    if not website:
        return "", ""
    # find email with website... TBD

    return "", ""

def extract_field(
        soup, 
        label: str, 
        field_length: int = 0, 
        parent: str = "",
        skip_tags: list[str] = None
    ) -> str:

    """
    For Label-Based Fields 
    soup.findall(string=<>) will search all text nodes. 

    label:        Address, Email, etc. Data to be found
    field_length: Optional, for fields w/ specified length (phone, fax)
    parent:       Optional, for levereging find_parent
    skip_tags:    Optional, tags to skip
    """
    skip_tags = skip_tags or []
    pattern = re.compile(rf"{re.escape(label)}.", re.IGNORECASE)

    candidates = soup.find_all(string=lambda t: t and pattern.search(t) is not None)
    for node in candidates:
        if parent:
            element = node.find_parent(parent) # finds nearest element w/ specified parent (div, p, etc.)
        else:
            element = node.parent # goes one step up to fetch the entire element
        if not element:
            continue

        text, texts = "", []
        for child in element.children:
            if child.name in skip_tags:
                continue
            texts.append(child.get_text(", ", strip=True))

        text = " ".join(texts)
        text = clean_str(text)
        if field_length > 0:
            return text[len(label)+1:len(label)+1+field_length].strip()

        return text[len(label)+1:].strip()

    return ""

def parse_overview_page(html) -> Dict[str, str]:
    soup = BeautifulSoup(html, "lxml")
    results = []

    for link in soup.select("a[href^='/attorney/Licensee/Detail/']"):
        name = link.get_text(strip=True)
        bar_number = link["href"].split("/")[-1]

        results.append({
            "name": name,
            "bar_number": bar_number
        })

    return results

def parse_detail_page(html, bar_number):
    soup = BeautifulSoup(html, "lxml")
    details = {"bar_number": bar_number}
    details["source"] = f"https://apps.calbar.ca.gov/attorney/Licensee/Detail/{bar_number}"

    # Name, Bar Number
    name_block = soup.find("div", style="margin-top:1em;")
    if name_block:
        b_tag = name_block.find("b")
        if b_tag:
            # Extract name
            full_text = b_tag.get_text(" ", strip=True)
            # Name is before the #
            if "#" in full_text:
                name_text, bar_num = full_text.split("#", 1)
                details["name"] = name_text.strip()
                details["bar_number"] = bar_num.strip()
            else:
                details["name"] = full_text.strip()

    # Date Admitted to Bar
    date_tag = soup.find("strong", string=lambda t: t and "/" in t)
    if date_tag:
        details["date_admitted"] = date_tag.get_text(strip=True)
        
    # Label-based fields
    details["license_status"]  = extract_field(soup, "License Status")
    details["address"]         = extract_field(soup, "Address")
    details["phone"]           = extract_field(soup, "Phone", 12) # phone is len = 12
    details["languages_self"]  = extract_field(soup, "By the attorney")
    details["languages_staff"] = extract_field(soup, "By Staff")
    details["law_school"]      = extract_field(soup, "Law School", 0, parent="p")
    details["practice_areas"]  = extract_field(soup, "Self-Reported Practice Areas", 0, parent="div", skip_tags=["div"])
    return details

def fetch_overview_page(
        session,
        state_code: str = "CA", 
        city: str = "", 
        practice_area: str = "", 
    ):

    params = {
        "LastNameOption": "b",
        "LastName": "",
        "FirstNameOption": "b",
        "FirstName": "",
        "MiddleNameOption": "b",
        "MiddleName": "",
        "FirmNameOption": "b",
        "FirmName": "",
        "CityOption": "e",
        "City": city if city else "",
        "State": state_code, # CA
        "Zip": "",
        "District": "",
        "County": "",
        "LegalSpecialty": "",
        "LanguageSpoken": "",
        "PracticeArea": practice_area if practice_area else "" # 51 = Personal Injury
    }

    resp = session.get(
        BASE_URL,
        params=params,
        headers=HEADERS
    )
    return resp.text

def fetch_detail_page(session, detail_href):
    url = urljoin(BASE_URL, detail_href)
    resp = session.get(url, headers=HEADERS)
    resp.raise_for_status()

    # STEP 2: POST request to load expanded attorney details
    post_payload = {
        "v": "2",
        "tid": "G-CJSS797DVD",
        "gtm": "45je5bi1v886304780za200zd886304780",
        "_p": "1763856279791",
        "gcd": "13l3l3l3l1l1",
        "npa": "0",
        "dma": "0",
        "cid": "506327324.1762633773",
        "ul": "en-us",
        "sr": "1920x1080",
        "uaa": "x86",
        "uab": "64",
        "uafvl": "Chromium;142.0.7444.135|Google%20Chrome;142.0.7444.135|Not_A%20Brand;99.0.0.0",
        "uamb": "0",
        "uam": "uap",
        "uapv": "19.0.0",
        "uaw": "0",
        "are": "1",
        "frm": "0",
        "pscdl": "noapi",
        "_eu": "AAAAAAQ",
        "_s": "1",
        "tag_exp": "103116026~103200004~104527907~104528500~104684208~104684211~105322302~115583767~115938466~115938468~116184927~116184929~116217636~116217638~116474637",
        "sid": "1763856276",
        "sct": "10",
        "seg": "1",
        "dl": url,
        "dr": "https://apps.calbar.ca.gov/attorney/LicenseeSearch/AdvancedSearch?LastNameOption=b&LastName=&FirstNameOption=b&FirstName=&MiddleNameOption=b&MiddleName=&FirmNameOption=b&FirmName=&CityOption=b&City=Los+Angeles&State=CA&Zip=&District=&County=&LegalSpecialty=&LanguageSpoken=&PracticeArea=51",
        "dt": "Joel Fredrick Citron # 35879 - Attorney Licensee Search",
        "en": "page_view",
        "_ee": "1",
        "tfd": "5938"
    }

    post_resp = session.post(url, headers=HEADERS, data=post_payload)
    post_resp.raise_for_status()
    print(f"POST Response: {post_resp.status_code}, {post_resp.url}")
    with open("attorney_35879.html", "w", encoding="utf-8") as f:
        f.write(post_resp.text)
    return post_resp.text

def scrape_state(
        session,
        state_code: str, 
        overview_pages: int,
        city: str = "", 
        practice_area: str = ""
    ):

    all_attorneys = []
    for page in range(overview_pages):
        print(f"Fetching page {page + 1}...")
        overview_html = fetch_overview_page(session, state_code, city, practice_area)
        overview_data = parse_overview_page(overview_html)
        if not overview_data:
            print("No more results.")
            break

        for res in overview_data[:10]:
            if not res.get("bar_number"):
                continue
            detail_html = fetch_detail_page(session, f"/attorney/Licensee/Detail/{res.get("bar_number")}")
            detail_data = parse_detail_page(detail_html, res.get("bar_number"))
            detail_data["jurisdiction"] = state_code
            all_attorneys.append(detail_data)
            time.sleep(1.5)

    return all_attorneys

