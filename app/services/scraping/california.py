import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Dict            
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

def parse_search_results(html) -> Dict[str, str]:
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

def parse_attorney_detail(html, bar_number):
    soup = BeautifulSoup(html, "lxml")
    details = {"bar_number": bar_number}

    # -------------------------
    # Name, Bar Number, License Status
    # -------------------------
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

        # License Status
        license_tag = name_block.find("p", class_="nostyle")
        if license_tag:
            status_b = license_tag.find("b")
            if status_b:
                status_text = status_b.get_text(strip=True)
                # Remove label if present
                if "License Status:" in status_text:
                    status_text = status_text.replace("License Status:", "").strip()
                details["license_status"] = status_text

    # -------------------------
    # Address
    # -------------------------
    addr_tag = soup.find("p", string=lambda t: t and t.startswith("Address:"))
    if addr_tag:
        details["address"] = addr_tag.get_text(strip=True).replace("Address:", "").strip()

    # -------------------------
    # Phone
    # -------------------------
    phone_tag = soup.find("p", string=lambda t: t and t.startswith("Phone:"))
    if phone_tag:
        details["phone"] = phone_tag.get_text(" ", strip=True).replace("Phone:", "").strip()

    # -------------------------
    # Additional Languages Spoken
    # -------------------------
    lang_div = soup.find("div", string=lambda t: t and "Additional Languages Spoken:" in t)
    if lang_div:
        # Parent div contains <ul><li>By the attorney / By staff</li></ul>
        ul_tag = lang_div.find_parent("div").find("ul")
        if ul_tag:
            for li in ul_tag.find_all("li"):
                label = li.get_text(":", strip=True).split(":")[0].lower().replace(" ", "_")
                value = li.find("span").get_text(strip=True)
                details[label] = value

    # -------------------------
    # Law School
    # -------------------------
    law_school_tag = soup.find("p", string=lambda t: t and "Law School:" in t)
    if law_school_tag:
        details["law_school"] = law_school_tag.get_text(strip=True).replace("Law School:", "").strip()

    # -------------------------
    # Date Admitted to Bar
    # -------------------------
    date_tag = soup.find("strong", string=lambda t: t and "/" in t)
    if date_tag:
        details["date_admitted"] = date_tag.get_text(strip=True)

    # -------------------------
    # Certified Legal Specialty
    # -------------------------
    cls_div = soup.find("a", href="http://californiaspecialist.org/")
    if cls_div:
        # The sibling div contains the specialty text
        sibling_div = cls_div.find_parent("div").find_all("div")[1]
        details["certified_legal_specialty"] = sibling_div.get_text(" ", strip=True)

    # -------------------------
    # Practice Areas (self)
    # -------------------------
    practice_ul = soup.find("p", string=lambda t: t and "Self-Reported Practice Areas:" in t)
    if practice_ul:
        ul_tag = practice_ul.find_next_sibling("div").find("ul")
        if ul_tag:
            details["practice_areas"] = [li.get_text(strip=True) for li in ul_tag.find_all("li")]
    return details

def fetch_city_page(city, session):
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
        "City": city,
        "State": "",
        "Zip": "",
        "District": "",
        "County": "",
        "LegalSpecialty": "",
        "LanguageSpoken": "",
        "PracticeArea": ""
    }

    resp = session.get(
        BASE_URL,
        params=params,
        headers=HEADERS
    )
    return resp.text

def fetch_attorney_detail(session, detail_href):
    url = urljoin(BASE_URL, detail_href)
    resp = session.get(url, headers=HEADERS)
    resp.raise_for_status()
    print(f"Details Response: {resp.status_code}, {resp.url}")
    return resp.text

def scrape_city(city, overview_pages):
    session = requests.Session()
    all_attorneys = []
    for page in range(overview_pages):
        print(f"Fetching {city}, page {page + 1}...")
        html = fetch_city_page(city, session)
        results = parse_search_results(html)
        if not results:
            print("No more results.")
            break

        for res in results[:5]:
            print(f"Attorney Details: {res.get("name", "")}")
            if not res.get("bar_number"):
                continue
            detail_html = fetch_attorney_detail(session, f"/attorney/Licensee/Detail/{res.get("bar_number")}")
            detail_data = parse_attorney_detail(detail_html, res.get("bar_number"))
            all_attorneys.append(detail_data)
            time.sleep(1.5)

    return all_attorneys

def main():
    cities = ["Los Angeles"]
    pages = 5

    for city in cities:
        data = scrape_city(city, pages)
    
    print(data)

if __name__ == "__main__":
    main()