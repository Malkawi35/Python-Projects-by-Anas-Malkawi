# web_scraping.py
from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urljoin

class WebScraping:
    def print_beautified_website_content(self, url) -> None:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html5lib')
        print(soup.prettify())

    def saving_website_content(self, url: str, csv_path: str = "output.csv") -> None:
        # fetches the page
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.content, 'html5lib')

        rows = []
        seen = set()


        def add_row(field, value):
            f = (field or "").strip()
            v = (value or "").strip()
            if not f or not v:
                return
            key = (f.lower(), v)
            if key in seen:
                return
            rows.append([f, v])
            seen.add(key)

        # page title
        if soup.title and soup.title.string:
            add_row("Title", soup.title.string)


        for s in soup.stripped_strings:
            if ":" in s:
                k, v = s.split(":", 1)
                add_row(k, v)


        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"])
            text = a.get_text("", strip=True) or href
            add_row("Link", f"{text} | {href}")

        # write CSV file
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["field", "value"])
            w.writerows(rows)

if __name__ == '__main__':
    web_scraping_content = WebScraping()
    url = input("Enter URL: ").strip()
    csv_name = input("Enter CSV file name: ").strip()
    if not csv_name.lower().endswith(".csv"):
        csv_name += ".csv"
    web_scraping_content.saving_website_content(url, csv_name)
