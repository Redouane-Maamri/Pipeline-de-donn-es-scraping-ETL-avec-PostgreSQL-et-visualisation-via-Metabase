import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0"
}

# 1️⃣ Get article links
def get_article_links():
    url = "https://www.hespress.com/"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    links = []

    for a in soup.find_all("a", href=True):
        link = a["href"]

        # Keep only article links
        if "hespress.com" in link and link.endswith(".html"):
            links.append(link)

    # remove duplicates + limit
    links = list(set(links))
    return links[:10]  # take 10 articles


# 2️⃣ Scrape one article
def scrape_article(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No title"

    paragraphs = soup.find_all("p")
    content = " ".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

    return {
        "title": title,
        "content": content,
        "url": url,
        "source": "hespress"
    }


# 3️⃣ Main scrape
def scrape():
    articles = []

    links = get_article_links()
    print(f"Found {len(links)} links")

    for link in links:
        try:
            article = scrape_article(link)
            articles.append(article)
            print(f"✔ Scraped: {link}")
        except:
            print(f"❌ Failed: {link}")

    with open("data/bronze/articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print("All articles saved ✅")