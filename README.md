# DB-ChatBot Assistant

Ein intelligenter Chatbot, der natürliche Spracheingaben entgegennimmt und automatisch passende SQL-Abfragen generiert. Das System ermöglicht es Nutzer\*innen, Fragen zu verschiedenen Datenbanken zu stellen, ohne SQL-Kenntnisse zu benötigen.

---

## Funktionsweise

Der DB-ChatBot Assistant nutzt ein KI-Modell von OpenAI, um Benutzereingaben in SQL umzuwandeln. Das System unterstützt aktuell **nur `SELECT`-Abfragen**, um Daten zu analysieren oder abzufragen. Die Abfragen werden dann an eine ausgewählte Datenbank weitergeleitet, und das Ergebnis wird in Tabellenform zurückgegeben.

---

## Unterstützte Datenbanken

- **SQLite**: Hochschule (z. B. Studierende, Dozenten, Prüfungen)
- **MySQL**: Einkaufssystem (z. B. Artikel, Kategorien, Bestellungen)
- **PostgreSQL**: Finanzdaten (z. B. Kunden, Konten, Transaktionen)

---

## Technologie-Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML + Tailwind CSS
- **KI**: OpenAI API (GPT)
- **SQL**: Unterstützung für mehrere SQL-Dialekte (sqlite3, MySQL, PostgreSQL)

---

## Installation

1. Klone das Repository:

   ```bash
   git clone git@github.com:NabilDaoud96/Smart-Chatbot.git
   cd db-chatbot
   python setup_database_SQLite.py
   pip install -r requirements.txt

   ```

2. Konfiguration vornehmen:

   Öffne die Datei config.py und trage dort deine Verbindungsdaten für MySQL und PostgreSQL ein.
   Öffne chatbot.py und füge deinen OpenAI API Key ein (openai.api_key = "dein_api_key").

3. python app.py
   Rufe den ChatBot im Browser auf: http://localhost:5000

## Beispiel-Use-Cases

"Welche Vorlesungen mit SWS werden von Professor Sokrates gelesen?" Hochschule

"Welche Rechnungen sind noch nicht bezahlt? Zeigen Sie auch Rechnungsdatum und Gesamtbetrag?" Einkaufssystem

"Welche Transaktionen wurden im März 2024 durchgeführt?" Finanzdaten
