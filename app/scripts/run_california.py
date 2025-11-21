from services.scraping.california import scrape_california
from services.persistence import save_to_csv

def main():
    print("runs cali scraper")
    # attorneys = scrape_california()
    # save_to_csv(attorneys, "data/california.csv")

if __name__ == "__main__":
    main()