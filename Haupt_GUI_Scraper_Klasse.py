# =============================================================================
# File............: news_scraper_gui.py
# Project.........: News Scraper FLZ – GUI
# Version.........: 1.1  (2025-07-02)
# Author..........: Florian Zingg  <florian.zingg@example.com>
# Description.....: PyQt6‑basierte Oberfläche für den News Scraper.
#                   Stellt Suche, Vorschau und dauerhafte Speicherung der
#                   Artikel in einer SQLite‑Datenbank bereit.
# Python version..: 3.11
# Dependencies....: PyQt6, requests, sqlite3, News_Scraper, Artikel_Widget_Klasse
# Licence.........: MIT
# -----------------------------------------------------------------------------
# Änderungsverlauf
#   * 1.0  (Initial)   – Grundlegendes GUI mit CSV‑Export
#   * 1.1  (2025-07-02) – Umstellung auf SQLite‑Persistenz, umfassende
#                      Dokumentation & Refactoring
# =============================================================================
import os
import requests
import sqlite3
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QScrollArea,
    QGridLayout, QPushButton
)
from PyQt6.QtCore import QSize
from News_Scraper import NewsScraper
from Artikel_Widget_Klasse import NewsWidget


class NewsScraperGUI(QWidget):
    """Hauptfenster des News‑Scraper‑Projekts.

    Responsibilities
    -----------------
    * stellt ein dunkles PyQt6‑GUI bereit (Suchfeld, Grid‑Layout, Button)
    * ruft *NewsScraper.get_articles* auf und rendert Ergebnisse
    * persistiert Artikel in einer SQLite‑Datenbank (``articles.db``)
    * akzeptiert Mehrfachstarts ohne Duplikate dank *INSERT OR IGNORE*

    Attributes
    ----------
    articles : list[dict]
        Zwischenspeicher der aktuell angezeigten Artikel.
    db_connection : sqlite3.Connection
        Verbindungsobjekt zur SQLite‑Datenbank.
    db_cursor : sqlite3.Cursor
        Cursor für wiederholte Inserts.
    """

    # ────────────────────────────────────────────────────────────────────
    # Konstruktor / Initialisierung
    # ────────────────────────────────────────────────────────────────────

    def __init__(self):
        super().__init__()
        self.articles = []
        self._init_db()
        self._init_ui()


    # ────────────────────────────────────────────────────────────────────
    # Datenbank‑Initialisierung
    # ────────────────────────────────────────────────────────────────────

    def _init_db(self) -> None:
        """Erzeugt die SQLite‑Datei sowie die Tabelle *articles* (idempotent)."""
        self.db_connection = sqlite3.connect("articles.db")
        self.db_cursor = self.db_connection.cursor()
        self.db_cursor.execute(
            """CREATE TABLE IF NOT EXISTS articles (
                    id         INTEGER PRIMARY KEY,
                    title      TEXT,
                    url        TEXT UNIQUE,
                    date       TEXT,
                    snippet    TEXT,
                    image_url  TEXT,
                    source     TEXT,
                    scraped_at TEXT
                )""")
        self.db_connection.commit()


    # ────────────────────────────────────────────────────────────────────
    # UI‑Aufbau
    # ────────────────────────────────────────────────────────────────────

    def _init_ui(self) -> None:
        """Erstellt und stylt alle Qt‑Widgets."""
        self.setWindowTitle("News Scraper FLZ")
        self.setStyleSheet("background-color: black; color: white;")

        self.layout = QVBoxLayout(self)

        # Suchfeld
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Thema eingeben und Enter drücken…")
        self.search_input.setStyleSheet(
            """QLineEdit {background-color: white; color: black;
                           font-size: 14px; padding: 5px; border-radius: 5px;}""")
        self.search_input.returnPressed.connect(self.scrape_news)
        self.layout.addWidget(self.search_input)

        # ScrollArea + Grid
        self.scroll_area = QScrollArea(self, widgetResizable=True)
        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)

        self.news_layout = QGridLayout(self.content_widget)
        self.news_layout.setSpacing(15)

        # Persist‑Button
        self.save_button = QPushButton("In Datenbank speichern", self)
        self.save_button.setStyleSheet(
            """QPushButton {background-color: #555; color: white; font-size: 14px;
                              padding: 8px; border-radius: 5px;}
               QPushButton:hover {background-color: #777;}""")
        self.save_button.clicked.connect(self.save_articles_to_db)
        self.layout.addWidget(self.save_button)

        # Initialer Abruf
        self.scrape_news()


    # ────────────────────────────────────────────────────────────────────
    # Scraping‑Workflow
    # ────────────────────────────────────────────────────────────────────

    def scrape_news(self) -> None:
        """Ruft den Scraper auf, leert das Grid und rendert neue Artikel."""
        search_term = self.search_input.text().strip().lower()
        scraper = NewsScraper()

        # Liste befüllen
        self.articles = scraper.get_articles(search_term or "", max_results=12)
        if not search_term:
            # Dummy‑Platzhalter, um das Grid voll zu halten
            while len(self.articles) < 12:
                self.articles.append({"title": "Platzhalter", "link": "#", "img_url": None})

        # Grid reset
        for i in reversed(range(self.news_layout.count())):
            widget = self.news_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Artikel‑Widgets (3 Spalten)
        cols, row, col = 3, 0, 0
        for art in self.articles:
            if search_term and art["title"] == "Platzhalter":
                continue
            item = NewsWidget(art["title"], art["link"], art["img_url"])
            item.setMinimumSize(QSize(300, 200))
            self.news_layout.addWidget(item, row, col)

            col = (col + 1) % cols
            row += 1 if col == 0 else 0


    # ────────────────────────────────────────────────────────────────────
    # Persistenz
    # ────────────────────────────────────────────────────────────────────

    def save_articles_to_db(self) -> None:
        """Schreibt alle aktuellen Artikel in die SQLite‑DB, dupes werden ignoriert."""
        if not self.articles:
            print("⚠️ Keine Artikel zum Speichern vorhanden.")
            return

        inserted, skipped = 0, 0
        for art in self.articles:
            try:
                self.db_cursor.execute(
                    """INSERT OR IGNORE INTO articles
                           (title, url, date, snippet, image_url,
                            source, scraped_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        art["title"],
                        art["link"],
                        art.get("date", ""),
                        art.get("snippet", ""),
                        art.get("img_url", ""),
                        "20Minuten",
                        datetime.now().isoformat(timespec="seconds")
                    ))
                if self.db_cursor.rowcount:
                    inserted += 1
                else:
                    skipped += 1
            except Exception as exc:
                print(f"⚠️ Fehler beim Einfügen: {exc}")

        self.db_connection.commit()
        print(f"✅ {inserted} Artikel gespeichert, {skipped} übersprungen (duplikat).")


    # ────────────────────────────────────────────────────────────────────
    # Aufräumen
    # ────────────────────────────────────────────────────────────────────

    def closeEvent(self, event) -> None:  # Qt‑Überschreibung
        """Schliesst die DB‑Verbindung sauber, bevor das Fenster schliesst."""
        if hasattr(self, "db_connection"):
            self.db_connection.close()
        event.accept()
