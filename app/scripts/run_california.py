from app.services.scraping.california import scrape_city
from app.services.persistence import save_to_csv

def main():
    cities = ["Los Angeles"]
    attorneys = scrape_city(cities, overview_pages=1)
    save_to_csv(attorneys, "data/california.csv")

if __name__ == "__main__":
    main()