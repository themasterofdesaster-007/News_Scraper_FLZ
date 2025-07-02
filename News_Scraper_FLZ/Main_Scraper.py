import sys
from PyQt6.QtWidgets import QApplication

# Eigene Klassen importieren
from News_Scraper import NewsScraper  # Artikel-Scraper
from Bilder_Scraper_Klasse import ImageScraper  # Bild-Scraper
from Artikel_Widget_Klasse import NewsWidget  # Widget für Artikel-Anzeige
from Haupt_GUI_Scraper_Klasse import NewsScraperGUI  # Haupt-GUI

# 🛠️ Fehler in PyQt sichtbar machen
def excepthook(exc_type, exc_value, traceback):
    print(f"🔴 Fehler: {exc_type.__name__}: {exc_value}")
    sys.__excepthook__(exc_type, exc_value, traceback)

sys.excepthook = excepthook

# 🖥️ **Startet das Programm**
app = QApplication(sys.argv)
window = NewsScraperGUI()
window.show()
sys.exit(app.exec())
