import requests
from app.services.scraping.california import scrape_state
from app.services.persistence import save_to_csv


def main():
    session = requests.Session()

    state = "CA"
    city = "Los Angeles"
    practice_area = "51"
    overview_pages = 1

    attorneys = scrape_state(
        session,
        state, 
        overview_pages, 
        city, 
        practice_area
    )
    
    save_to_csv(attorneys, "data/attorneys.csv")

if __name__ == "__main__":
    main()