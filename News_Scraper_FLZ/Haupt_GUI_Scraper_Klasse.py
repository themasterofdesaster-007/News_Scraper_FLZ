import csv
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QScrollArea, QGridLayout, QApplication, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, QSize
from News_Scraper import NewsScraper
from Artikel_Widget_Klasse import NewsWidget


# 🖥️ **Haupt-GUI-Klasse**
class NewsScraperGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.articles = []  # Liste für die gespeicherten Artikel
        self.initUI()

    def initUI(self):
        # **Dunkles Design für das Hauptfenster**
        self.setStyleSheet("background-color: black; color: white;")

        # Hauptlayout
        self.layout = QVBoxLayout(self)

        # Suchfeld
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Thema eingeben und Enter drücken...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                font-size: 14px;
                padding: 5px;
                border-radius: 5px;
            }
        """)
        self.search_input.returnPressed.connect(self.scrape_news)
        self.layout.addWidget(self.search_input)

        # Scrollbare Ansicht für News
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)

        # Grid-Layout für die Artikel
        self.news_layout = QGridLayout(self.content_widget)
        self.news_layout.setSpacing(15)

        # CSV-Button zum Speichern
        self.save_button = QPushButton("Als CSV speichern", self)
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                font-size: 14px;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.save_button.clicked.connect(self.save_articles_to_csv)
        self.layout.addWidget(self.save_button)

        # Starte das erste Laden
        self.scrape_news()

    def scrape_news(self):
        """ Holt Nachrichten & speichert sie für den CSV-Export """
        search_term = self.search_input.text().strip().lower()
        scraper = NewsScraper()

        if search_term:
            self.articles = scraper.get_articles(search_term, max_results=12)
        else:
            self.articles = scraper.get_articles("", max_results=12)
            while len(self.articles) < 12:
                self.articles.append({"title": "Platzhalter", "link": "#", "img_url": None})

        # Altes Layout leeren
        for i in reversed(range(self.news_layout.count())):
            widget = self.news_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Dynamische Anzahl von Artikeln
        cols = 3
        row, col = 0, 0

        for article in self.articles:
            if search_term and article["title"] == "Platzhalter":
                continue

            news_widget = NewsWidget(article["title"], article["link"], article["img_url"])
            news_widget.setMinimumSize(QSize(300, 200))
            self.news_layout.addWidget(news_widget, row, col)

            col += 1
            if col >= cols:
                col = 0
                row += 1

    import os
    import csv
    import requests
    from PyQt6.QtWidgets import QFileDialog

    def save_articles_to_csv(self):
        """Speichert die gescrapten Artikel, lädt die Bilder herunter und erstellt zusätzlich eine HTML-Vorschau."""
        if not self.articles:
            print("⚠️ Keine Artikel zum Speichern gefunden.")
            return

        # Benutzer wählt den Speicherort für die CSV-Datei
        file_path, _ = QFileDialog.getSaveFileName(self, "Speichern unter", "news_scraper_output.csv",
                                                   "CSV-Dateien (*.csv)")

        if not file_path:
            return

        # Ordner für Bilder erstellen
        img_folder = os.path.join(os.path.dirname(file_path), "images")
        os.makedirs(img_folder, exist_ok=True)

        # CSV-Datei mit UTF-8-SIG speichern
        with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(["Titel", "Link", "Bild-URL", "Bild-Pfad", "Bild-Link in Excel"])  # Spaltenüberschriften

            html_content = ["<html><head><meta charset='utf-8'><title>News Scraper Ergebnisse</title></head><body>"]
            html_content.append(
                "<h1>Gescrapte Artikel</h1><table border='1'><tr><th>Titel</th><th>Link</th><th>Bild</th></tr>")

            for article in self.articles:
                img_url = article["img_url"]
                img_filename = ""
                img_excel_link = ""

                # Bild speichern, falls vorhanden
                if img_url:
                    try:
                        response = requests.get(img_url, stream=True, timeout=5)
                        response.raise_for_status()

                        # Bildname aus der URL extrahieren und speichern
                        img_filename = os.path.join(img_folder, os.path.basename(img_url.split("?")[0]))
                        with open(img_filename, "wb") as img_file:
                            img_file.write(response.content)

                        img_excel_link = f'=HYPERLINK("{img_filename}", "📷 Bild öffnen")'

                    except Exception as e:
                        print(f"⚠️ Fehler beim Speichern des Bildes {img_url}: {e}")
                        img_filename = "Fehler beim Speichern"
                        img_excel_link = "Kein Bild"

                writer.writerow([article["title"], article["link"], img_url, img_filename, img_excel_link])

                # HTML-Vorschau hinzufügen
                html_content.append(
                    f"<tr><td>{article['title']}</td><td><a href='{article['link']}'>{article['link']}</a></td>")
                if img_url:
                    html_content.append(f"<td><img src='{img_filename}' width='150'></td></tr>")
                else:
                    html_content.append("<td>Kein Bild</td></tr>")

            html_content.append("</table></body></html>")

        # HTML-Datei speichern
        html_file_path = file_path.replace(".csv", ".html")
        with open(html_file_path, "w", encoding="utf-8") as html_file:
            html_file.write("\n".join(html_content))

        print(f"✅ Daten wurden in {file_path} gespeichert. Bilder liegen in {img_folder}.")
        print(f"✅ HTML-Vorschau gespeichert unter {html_file_path}")
