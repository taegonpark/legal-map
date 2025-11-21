import csv

def save_to_csv(attorneys, filepath="data/attorneys.csv"):
    fieldnames = attorneys[0].keys()

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(attorneys)