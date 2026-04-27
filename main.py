from scraper.scraper import scrape
from etl.transform import transform
from db.load import load_to_db

if __name__ == "__main__":
    scrape()
    transform()
    load_to_db()
    print("Pipeline DONE 🚀")