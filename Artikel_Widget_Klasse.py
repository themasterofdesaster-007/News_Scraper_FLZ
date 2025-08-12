import math
import webbrowser
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from Bilder_Scraper_Klasse import ImageScraper


# 📰 **Artikel-Widget**
class NewsWidget(QWidget):
    def __init__(self, title, link, img_url):
        super().__init__()

        # **Lange Titel kürzen**
        if len(title) > 50:
            title = title[:50] + "..."

        self.setStyleSheet("""
            QWidget {
                background-color: black;
                border: 2px solid white;
                border-radius: 10px;
                padding: 10px;
                margin: 10px;  /* Mehr Abstand zwischen den Artikeln */
                transition: background-color 0.3s ease-in-out;
            }
            QWidget:hover {
                background-color: #222;  /* Hover-Effekt */
            }
        """)

        layout = QVBoxLayout(self)

        # Falls kein Bild vorhanden ist (Platzhalter)
        if img_url:
            img_pixmap = ImageScraper.load_and_prepare_image(img_url)
            img_pixmap = img_pixmap.scaled(250, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            img_label = QLabel()
            img_label.setPixmap(img_pixmap)
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(img_label)
        else:
            img_label = QLabel("Kein Artikel verfügbar")
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            img_label.setStyleSheet("font-size: 14px; color: gray;")
            layout.addWidget(img_label)

        # Artikel-Button (Falls Platzhalter, kein klickbares Event)
        button = QPushButton(title)
        if link != "#":
            button.clicked.connect(lambda: webbrowser.open(link))
        button.setStyleSheet("""
            QPushButton {
                text-align: center;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                background-color: #444;
                color: white;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        layout.addWidget(button)

