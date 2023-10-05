# Author: Maximilian Müller

from sqlalchemy import create_engine
import pandas as pd

# Diese Funktion stellt die Verbindung zur Datenbank her
def connect_to_db():
    p_pass = "example"  # Das Passwort für die Datenbankverbindung
    p_user = "postgres"  # Der Benutzername für die Datenbankverbindung
    p_host = "192.168.0.11"  # Die IP-Adresse des Datenbankservers
    p_port = "5432"  # Der Port für die Datenbankverbindung
    p_db = "postgres"  # Der Name der Datenbank

    # Erstellt die Verbindungs-URL zur PostgreSQL-Datenbank
    connection_url = f'postgresql://{p_user}:{p_pass}@{p_host}:{p_port}/{p_db}'

    # Erstellt den Datenbank-Engine
    engine = create_engine(connection_url)  

    return engine

# Die Funktion extrahiert alle dem übergebenen endbahnhof entsprechenden Datensätze aus der Datenbank
def get_data_by_endbahnhof(endbahnhof):

    # Verbindet mit der Datenbank
    engine = connect_to_db()  

    # Erstellt die SQL-Abfrage, um Daten mit dem gegebenen Endbahnhof abzurufen
    query = f"SELECT * FROM your_table WHERE endbahnhof = '{endbahnhof}'"

    try:
        # Führt die Abfrage aus und liest das Ergebnis in ein DataFrame ein
        df = pd.read_sql(query, engine)  
        return df
    except Exception as e:
        print("Fehler beim Abrufen der Datenbankdaten:", e)

# Alle Daten aus der Datenbank werden extrahiert
def get_all_data():

    # Verbindet mit der Datenbank
    engine = connect_to_db()  

    # Erstellt die SQL-Abfrage, um alle Daten aus der Tabelle abzurufen
    query = f"SELECT * FROM your_table"

    try:
        # Führt die Abfrage aus und liest das Ergebnis in ein DataFrame ein
        df = pd.read_sql(query, engine)  
        return df
    except Exception as e:
        print("Fehler beim Abrufen der Datenbankdaten:", e)

