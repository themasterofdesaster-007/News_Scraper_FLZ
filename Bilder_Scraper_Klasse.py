# =============================================================================
# File............: Bilder_Scraper_Klasse.py
# Project.........: News Scraper FLZ
# Version.........: 1.0
# Author..........: Florian Zingg
# Description.....: Extrahiert geeignete Bild-Quellen aus Artikel-DOMs und
#                   laedt Bilder robust als QPixmap.
# Licence.........: MIT
# =============================================================================
import requests
from io import BytesIO
from PIL import Image, ImageQt
from selenium.webdriver.common.by import By
from PyQt6.QtGui import QPixmap


# 🖼️ **Bild-Scraper-Klasse**
class ImageScraper:
    @staticmethod
    def extract_best_image(article):
        """ Extrahiert das beste Bild aus einem Artikel """
        try:
            # **1️⃣ Zuerst nach `<picture>`-Element suchen**
            picture_tag = article.find_element(By.TAG_NAME, "picture")
            if picture_tag:
                sources = picture_tag.find_elements(By.TAG_NAME, "source")
                for source in sources:
                    srcset = source.get_attribute("srcset")
                    if srcset:
                        img_url = srcset.split(" ")[0]  # Erstes Bild in `srcset`
                        return img_url  # Direkte Rückgabe

            # **2️⃣ Falls kein `<picture>`, nach `img` suchen**
            img_tag = article.find_element(By.TAG_NAME, "img")
            if img_tag:
                img_url = img_tag.get_attribute("src")
                return img_url

        except Exception as e:
            print(f"⚠️ Kein Bild gefunden: {e}")
            return None  # Kein Bild verfügbar

    @staticmethod
    def load_and_prepare_image(img_url):
        """ Lädt das Bild, konvertiert es & sichert es gegen Fehler ab """
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(img_url, headers=headers, stream=True, timeout=5)
            response.raise_for_status()

            # folgende 3 Zeilen hat Chrigu hinzugefügt (den Rest der Methode nach "return pixmap" braucht es nicht mehr):
            pixmap = QPixmap()
            pixmap.loadFromData(BytesIO(response.content).read())
            return pixmap

            image = Image.open(BytesIO(response.content))

            # **Falls WebP oder AVIF → Konvertiere in JPEG**
            if image.format in ["WEBP", "AVIF"]:
                image = image.convert("RGB")

            image = image.resize((180, 120))  # Größere & klarere Vorschau
            qt_image = QPixmap.fromImage(ImageQt.ImageQt(image))

            if qt_image.isNull():
                print(f"⚠️ QPixmap konnte das Bild nicht laden: {img_url}")
                return None

            return qt_image

        except Exception as e:
            print(f"⚠️ Fehler beim Laden des Bildes {img_url}: {e}")
            return None  # Fehler abfangen & GUI-Fehler verhindern

