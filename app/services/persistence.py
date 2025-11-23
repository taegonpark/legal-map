import csv
from datetime import datetime
from app.db.models import Attorney, AttorneyDetail
from app.db.session import SessionLocal

LIST_COLUMNS = {
    "languages_self": "Language (Self)",
    "languages_staff": "Language (Staff)",
    "practice_areas": "Practice Area"
}

def load_attorney_details_from_csv(csv_file_path: str):
    db = SessionLocal()
    try:
        with open(csv_file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                attorney = db.query(Attorney).filter(Attorney.bar == int(row["bar_number"])).first()
                # get attorney, using bar code.
                if not attorney:
                    continue  

                for csv_col, detail_type in LIST_COLUMNS.items():
                    if row.get(csv_col):
                        # each details row is comma delimited
                        items = [i.strip() for i in row[csv_col].split(",") if i.strip()]
                        for item in items:
                            detail = AttorneyDetail(
                                attorney_id=attorney.id,
                                detail_type=detail_type,
                                detail=item
                            )
                            db.add(detail)
            db.commit()
    finally:
        db.close()

def load_attorneys_from_csv(csv_file_path: str):
    db = SessionLocal()  # get a DB session
    try:
        with open(csv_file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert date string to datetime if needed
                date_admitted = None
                if row.get("date_admitted"):
                    date_str = row["date_admitted"]
                    date_admitted = datetime.strptime(date_str, "%m/%d/%Y")

                attorney = Attorney(
                    jurisdiction=row.get("jurisdiction", "US"),  # default if missing
                    source=row.get("source"),
                    name=row.get("name"),
                    bar=int(row["bar_number"]) if row.get("bar_number") else None,
                    phone=row.get("phone"),
                    address=row.get("address"),
                    date_admitted=date_admitted,
                    law_school=row.get("law_school"),
                    rating=row.get("license_status")  # map license_status to rating
                )

                db.add(attorney)
            db.commit()
    finally:
        db.close()

def save_to_csv(attorneys, filepath="data/attorneys.csv"):
    fieldnames = attorneys[0].keys()

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(attorneys)

