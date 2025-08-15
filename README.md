# 📰 News Scraper FLZ

![Titelbild](A_digital_graphic_design_for_a_software_applicatio.png)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?logo=qt)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-yellow)

Der **News Scraper FLZ** ist eine Python-Anwendung mit moderner PyQt6-Oberfläche, die automatisch aktuelle Nachrichten von **20 Minuten** abruft, übersichtlich darstellt und dauerhaft in einer **SQLite-Datenbank** speichert.  
Ziel des Projekts ist es, Web-Scraping, Datenbankdesign und GUI-Entwicklung praxisnah zu verbinden.

---

## 🚀 Features

- **Automatisches Scraping** von Artikeln inkl. Titel, Link, Datum, Bild & Vorschau-Text
- **PyQt6 GUI** im Dark Mode
- **Suchfunktion** nach Schlagworten
- **Speicherung in SQLite** (keine Duplikate durch `INSERT OR IGNORE`)
- **Export** in verschiedene Formate (SQL, XLSX)
- **Crow’s Foot Diagramme** für IST- und SOLL-Datenmodell

---

## 📸 Screenshots

> Hier kannst du Screenshots deiner Anwendung einfügen  
> Beispiel: GUI-Ansicht, gespeicherte Artikel, Suchfunktion, Exportfunktion

---

## 🗂 Projektstruktur

```plaintext
News_Scraper_FLZ/
├── main.py                     # Startpunkt der Anwendung
├── News_Scraper.py             # Logik zum Abrufen von Artikeln
├── Artikel_Widget_Klasse.py    # Widget-Klasse für Artikelanzeige
├── articles.db                  # SQLite-Datenbank (wird automatisch erstellt)
├── requirements.txt             # Abhängigkeiten
└── README.md
Installation

Installation

Repository klonen
git clone https://github.com/themasterofdesaster-007/News_Scraper_FLZ.git
cd News_Scraper_FLZ

Virtuelle Umgebung erstellen
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

Abhängigkeiten installieren
pip install -r requirements.txt

Anwendung starten
python main.py

Datenbank

Die Anwendung erstellt beim ersten Start eine articles.db mit folgender Struktur (SOLL-Version, normalisiert):

sources – Nachrichtenquellen

authors – Autoren (optional)

tags – Schlagwörter

articles – Haupttabelle für Artikel

article_tag – Zuordnungstabelle für m:n-Beziehung

Crow’s Foot Diagramm (IST)

(Hier Bild erd_news_scraper_IST.png einfügen)

Crow’s Foot Diagramm (SOLL)

(Hier Bild erd_news_scraper_SOLL.png einfügen)


Wenn du willst, kann ich dir auch gleich **Platzhalter-Screenshots** und **Diagramm-Bilder** mit dem richtigen Namen erstellen,  
damit GitHub sie direkt im README anzeigt, sobald du sie in den Ordner legst.  
Willst du, dass ich das gleich mitmache?
