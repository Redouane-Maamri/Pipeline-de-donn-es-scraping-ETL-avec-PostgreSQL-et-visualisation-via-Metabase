from scraper.scraper import scrape_hespress
from scraper.akhbarona import scrape_akhbarona
from etl.transform import transform
from db.load import load_to_db
import json

def scrape():
    all_articles = []

    # Scrape both sources
    all_articles += scrape_hespress()
    all_articles += scrape_akhbarona()

    # Save to Bronze
    with open("data/bronze/articles.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"Total articles scraped: {len(all_articles)} ✅")

if __name__ == "__main__":
    scrape()
    transform()
    load_to_db()
    print("Pipeline DONE 🚀")