# setup_database.py
import os
import sqlite3


# Alte Datenbank löschen, falls vorhanden
if os.path.exists("database/hochschule.db"):
    os.remove("database/hochschule.db")

# Verbindung zur Datenbank (wird erstellt, wenn sie nicht existiert)
conn = sqlite3.connect("database/hochschule.db")
cursor = conn.cursor()

# Tabellen erstellen
cursor.execute("DROP TABLE IF EXISTS pruefen;")
cursor.execute("DROP TABLE IF EXISTS hoeren;")
cursor.execute("DROP TABLE IF EXISTS voraussetzen;")
cursor.execute("DROP TABLE IF EXISTS Studenten;")
cursor.execute("DROP TABLE IF EXISTS Assistenten;")
cursor.execute("DROP TABLE IF EXISTS Vorlesungen;")
cursor.execute("DROP TABLE IF EXISTS Professoren;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Studenten (
    MatrNr INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Semester INTEGER,
    GebDatum TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Professoren (
    PersNr INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Rang TEXT,
    Raum INTEGER UNIQUE,
    Gebdatum TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Assistenten (
    PersNr INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Fachgebiet TEXT,
    Boss INTEGER,
    GebDatum TEXT,
    FOREIGN KEY (Boss) REFERENCES Professoren (PersNr)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Vorlesungen (
    VorlNr INTEGER PRIMARY KEY,
    Titel TEXT,
    SWS INTEGER,
    gelesenVon INTEGER,
    FOREIGN KEY (gelesenVon) REFERENCES Professoren (PersNr)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS hoeren (
    MatrNr INTEGER,
    VorlNr INTEGER,
    PRIMARY KEY (MatrNr, VorlNr),
    FOREIGN KEY (MatrNr) REFERENCES Studenten (MatrNr),
    FOREIGN KEY (VorlNr) REFERENCES Vorlesungen (VorlNr)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS voraussetzen (
    Vorgaenger INTEGER,
    Nachfolger INTEGER,
    PRIMARY KEY (Vorgaenger, Nachfolger),
    FOREIGN KEY (Vorgaenger) REFERENCES Vorlesungen (VorlNr),
    FOREIGN KEY (Nachfolger) REFERENCES Vorlesungen (VorlNr)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pruefen (
    MatrNr INTEGER,
    VorlNr INTEGER,
    PersNr INTEGER,
    Note REAL CHECK (Note BETWEEN 0.7 AND 5.0),
    PRIMARY KEY (MatrNr, VorlNr),
    FOREIGN KEY (MatrNr) REFERENCES Studenten (MatrNr),
    FOREIGN KEY (VorlNr) REFERENCES Vorlesungen (VorlNr),
    FOREIGN KEY (PersNr) REFERENCES Professoren (PersNr)
);
""")

# Daten einfügen – Studenten
cursor.executemany("""
INSERT INTO Studenten (MatrNr, Name, Semester, GebDatum) VALUES (?, ?, ?, ?);
""", [
    (24002, 'Xenokrates', 9, '1975-10-23'),
    (25403, 'Jonas', 1, '1973-09-18'),
    (26120, 'Fichte', 3, '1967-12-04'),
    (26830, 'Aristoxenos', 5, '1943-08-05'),
    (27550, 'Schopenhauer', 1, '1954-06-22'),
    (28106, 'Carnap', 3, '1979-10-02'),
    (29120, 'Theophrastos', 7, '1948-04-19'),
    (29555, 'Feuerbach', 1, '1961-02-12'),
    (27123, 'Kessler', 3, '1978-11-11'),
    (29917, 'Erlebach', 1, '1981-05-20')
])

# Professoren
cursor.executemany("""
INSERT INTO Professoren (PersNr, Name, Rang, Raum, Gebdatum) VALUES (?, ?, ?, ?, ?);
""", [
    (2125, 'Sokrates', 'C4', 226, '1923-08-23'),
    (2126, 'Russel', 'W2', 232, '1934-07-10'),
    (2127, 'Kopernikus', 'C3', 310, '1962-03-12'),
    (2133, 'Popper', 'C3', 52, '1949-09-03'),
    (2134, 'Augustinus', 'W2', 309, '1939-04-21'),
    (2136, 'Curie', 'C4', 36, '1929-05-10'),
    (2137, 'Kant', 'C4', 7, '1950-04-04'),
    (4711, 'Newton', 'C4', 339, '1951-03-24'),
    (4712, 'Möbius', 'W3', 222, '1962-09-18')
])

# Assistenten
cursor.executemany("""
INSERT INTO Assistenten (PersNr, Name, Fachgebiet, Boss, GebDatum) VALUES (?, ?, ?, ?, ?);
""", [
    (3002, 'Platon', 'Ideenlehre', 2125, '1966-08-14'),
    (3003, 'Aristoteles', 'Syllogistik', 2125, '1970-12-23'),
    (3004, 'Wittgenstein', 'Sprachtheorie', 2126, '1968-08-02'),
    (3005, 'Rhetikus', 'Planetenbewegung', 2127, '1967-06-09'),
    (3006, 'Newton', 'Keplersche Gesetze', 2127, '1961-11-10'),
    (3007, 'Spinoza', 'Gott und Natur', 2134, '1963-02-08')
])

# Vorlesungen
cursor.executemany("""
INSERT INTO Vorlesungen (VorlNr, Titel, SWS, gelesenVon) VALUES (?, ?, ?, ?);
""", [
    (4052, 'Logik', 4, 2125),
    (4630, 'Die 3 Kritiken', 4, 2137),
    (5001, 'Grundzuege', 4, 2137),
    (5022, 'Glaube und Wissen', 2, 2134),
    (5041, 'Ethik', 4, 2125),
    (5043, 'Erkenntnistheorie', 3, 2126),
    (5049, 'Mäeutik', 2, 2125),
    (5052, 'Wissenschaftstheorie', 3, 2126),
    (5216, 'Bioethik', 2, 2126),
    (5259, 'Der Wiener Kreis', 2, 2133)
])

# hoeren
cursor.executemany("""
INSERT INTO hoeren (MatrNr, VorlNr) VALUES (?, ?);
""", [
    (25403, 5022),
    (26120, 5001),
    (27550, 4052),
    (27550, 4630),
    (27550, 5001),
    (27550, 5041),
    (27550, 5259),
    (28106, 4052),
    (28106, 5216),
    (28106, 5259),
    (29120, 5041),
    (29120, 5049),
    (29555, 5001),
    (29555, 5022)
])

# voraussetzen
cursor.executemany("""
INSERT INTO voraussetzen (Vorgaenger, Nachfolger) VALUES (?, ?);
""", [
    (5001, 5041),
    (5001, 5043),
    (5001, 5049),
    (5041, 5052),
    (5041, 5216),
    (5043, 5052),
    (5052, 5259)
])

# pruefen
cursor.executemany("""
INSERT INTO pruefen (MatrNr, VorlNr, PersNr, Note) VALUES (?, ?, ?, ?);
""", [
    (25403, 5041, 2125, 2.0),
    (27550, 4630, 2137, 2.0),
    (29917, 5001, 2127, 0.7),
    (28106, 5001, 2126, 1.0),
    (27550, 5001, 2126, 2.3),
    (27123, 4052, 4712, 3.7)
])
# Speichern & Verbindung schließen
conn.commit()
conn.close()

print("Datenbank erfolgreich erstellt & mit Daten befüllt.")
