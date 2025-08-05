# chatbot.py

from openai import OpenAI
import sqlite3
import mysql.connector
import psycopg2
import re

from config import SQLITE_DB_PATH, MYSQL_CONFIG, POSTGRES_CONFIG

client = OpenAI(api_key="dein_api_key")

def hole_datenbankschema(datenbank_typ):
    if datenbank_typ == "sqlite":
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabellen = [row[0] for row in cursor.fetchall()]
        schema = []
        for tabelle in tabellen:
            cursor.execute(f"PRAGMA table_info({tabelle});")
            spalten = cursor.fetchall()
            spalten_info = ", ".join([f"{s[1]} ({s[2]})" for s in spalten])
            schema.append(f"- {tabelle}: {spalten_info}")
        conn.close()

    elif datenbank_typ == "mysql":
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tabellen = [row[0] for row in cursor.fetchall()]
        schema = []
        for tabelle in tabellen:
            cursor.execute(f"DESCRIBE {tabelle}")
            spalten = cursor.fetchall()
            spalten_info = ", ".join([f"{s[0]} ({s[1]})" for s in spalten])
            schema.append(f"- {tabelle}: {spalten_info}")
        conn.close()

    elif datenbank_typ == "postgresql":
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
        """)
        tabellen = [row[0] for row in cursor.fetchall()]
        schema = []
        for tabelle in tabellen:
            cursor.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{tabelle}'
            """)
            spalten = cursor.fetchall()
            spalten_info = ", ".join([f"{s[0]} ({s[1]})" for s in spalten])
            schema.append(f"- {tabelle}: {spalten_info}")
        conn.close()

    else:
        schema = ["Unbekannter Datenbanktyp"]
    
    return "\n".join(schema)


def frage_verarbeiten(frage, datenbank_typ):
    schema = hole_datenbankschema(datenbank_typ)

    hinweis = {
        "sqlite": "Verwende ausschließlich gültige SQLite-Syntax.",
        "mysql": "Verwende ausschließlich gültige MySQL-Syntax.",
        "postgresql": "Verwende ausschließlich gültige PostgreSQL-Syntax."
    }.get(datenbank_typ, "")

    prompt = f"""
    Du bist ein SQL-Experte. {hinweis}
    Erstelle eine gültige SELECT-Abfrage basierend auf folgender Frage und dem Datenbankschema.

    Frage:
    {frage}

    Datenbankschema:
    {schema}

    Hinweise:
    - Gib **nur** die reine SQL-Abfrage zurück (keine Erklärungen oder ```sql).
    - Nutze keine INSERT/UPDATE/DELETE.
    - Nutze nur Tabellen und Spalten aus dem Schema.
    - Verwende **nur Tabellen und Spalten, die exakt im bereitgestellten Schema enthalten sind**.
    - Wenn die Frage sich auf eine Tabelle oder Spalte bezieht, die **nicht im Schema enthalten** ist, gib stattdessen **den Text** zurück: 
        `FEHLER: Die angefragte Tabelle oder Spalte existiert nicht im aktuellen Schema.`
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher SQL-Assistent."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    sql_query = response.choices[0].message.content.strip()
    sql_query = re.sub(r"^```sql|```$", "", sql_query).strip()
    sql_query = re.sub(r"^sql", "", sql_query).strip()
    return sql_query


def sql_ausführen(query, datenbank_typ):
    try:
        if datenbank_typ == "sqlite":
            conn = sqlite3.connect(SQLITE_DB_PATH)
        elif datenbank_typ == "mysql":
            conn = mysql.connector.connect(**MYSQL_CONFIG)
        elif datenbank_typ == "postgresql":
            conn = psycopg2.connect(**POSTGRES_CONFIG)
        else:
            return [[f"Unbekannter Datenbanktyp: {datenbank_typ}"]]

        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        spalten = [desc[0] for desc in cursor.description]
        return [spalten] + rows
    except Exception as e:
        return [[f"Fehler bei SQL-Ausführung: {e}"]]
    finally:
        if 'conn' in locals():
            conn.close()
