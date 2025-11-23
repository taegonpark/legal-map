import requests
from app.services.scraping.california import scrape_state
from app.services.persistence import save_to_csv
from app.services.persistence import load_attorney_details_from_csv, load_attorneys_from_csv

def main():
    session = requests.Session()

    # state_code = "CA"
    # city = "Los Angeles"
    # practice_area = "51"
    # overview_pages = 1

    # attorneys = scrape_state(
    #     session,
    #     state_code, 
    #     overview_pages, 
    #     city, 
    #     practice_area
    # )

    # save_to_csv(attorneys, "data/attorneys.csv")

    # load_attorneys_from_csv(csv_file_path="data/attorneys.csv")
    # load_attorney_details_from_csv(csv_file_path="data/attorneys.csv")




if __name__ == "__main__":
    main()