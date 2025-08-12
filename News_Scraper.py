# =============================================================================
# File............: News_Scraper.py
# Project.........: News Scraper FLZ
# Version.........: 0.2 (Stub)
# Author..........: Florian Zingg
# Description.....: Platzhalter fuer den eigentlichen Web-Scraper. Liefert
#                   strukturierte Artikel-Dicts, damit GUI/DB laufen.
# Licence.........: MIT
# =============================================================================
import csv
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Bilder_Scraper_Klasse import ImageScraper


# 📰 **Artikel-Scraper-Klasse**
class NewsScraper:

    def __init__(self, url="https://www.20min.ch/schweiz"):
        self.url = url

    def get_articles(self, search_term="", max_results=10):
        """ Holt die Artikel von 20 Minuten & gibt sie als Liste von Dicts zurück """
        print(f"🔍 Scraping {self.url} ({search_term})")

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(self.url)

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
        except Exception as e:
            print(f"⚠️ Fehler: Keine Artikel gefunden! {e}")
            driver.quit()
            return []

        articles = driver.find_elements(By.TAG_NAME, "article")
        print(f"🔍 Gefundene Artikel: {len(articles)}")

        results = []
        count = 0

        for article in articles:
            if count >= max_results:
                break

            try:
                title_tag = article.find_element(By.TAG_NAME, "h2")
                title = title_tag.text.strip()

                try:
                    link_tag = article.find_element(By.TAG_NAME, "a")
                    link = link_tag.get_attribute("href")
                except:
                    link = self.url

                img_url = ImageScraper.extract_best_image(article)
                if img_url and not img_url.startswith("http"):
                    img_url = urllib.parse.urljoin("https://www.20min.ch", img_url)

                if search_term and search_term.lower() not in title.lower():
                    continue

                results.append({"title": title, "link": link, "img_url": img_url})
                count += 1

            except Exception as e:
                print(f"⚠️ Fehler beim Verarbeiten eines Artikels: {e}")

        driver.quit()
        return results
