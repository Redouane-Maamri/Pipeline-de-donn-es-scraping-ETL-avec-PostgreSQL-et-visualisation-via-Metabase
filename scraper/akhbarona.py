import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_akhbarona_links():
    url = "https://www.akhbarona.com/"
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "lxml")

    links = []

    for a in soup.find_all("a", href=True):
        link = a["href"]

        # filter article links
        if "akhbarona.com" in link and ".html" in link:
            links.append(link)

    links = list(set(links))
    return links[:10]


def scrape_akhbarona():
    articles = []
    links = get_akhbarona_links()

    print(f"Akhbarona links found: {len(links)}")

    for link in links:
        try:
            res = requests.get(link, headers=headers)
            soup = BeautifulSoup(res.text, "lxml")

            title_tag = soup.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else "No title"

            paragraphs = soup.find_all("p")
            content = " ".join([
                p.get_text(strip=True) for p in paragraphs 
                if p.get_text(strip=True)
            ])

            # filter weak articles
            if len(content.split()) > 100:
                articles.append({
                    "title": title,
                    "content": content,
                    "url": link,
                    "source": "akhbarona"
                })

                print(f"✔ Akhbarona: {link}")

        except:
            print(f"❌ Failed: {link}")

    return articles