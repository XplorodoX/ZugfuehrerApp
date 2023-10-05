# Author: Maximilian Müller

import time
import datetime
from sqlalchemy import create_engine
from app import crawler
from dataHandler import polishData
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler


def save_crawler_to_db():
    p_pass = "example"  # Passwort für die PostgreSQL-Datenbank
    p_user = "postgres"  # Benutzername für die PostgreSQL-Datenbank
    p_host = "192.168.0.11"  # Hostname der PostgreSQL-Datenbank
    p_port = "5432"  # Port der PostgreSQL-Datenbank
    p_db = "postgres"  # Name der PostgreSQL-Datenbank

    connection_url = f'postgresql://{p_user}:{p_pass}@{p_host}:{p_port}/{p_db}'
    engine = create_engine(connection_url)

    final = pd.DataFrame()  # Leeres DataFrame für die endgültigen Daten

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Aktueller Zeitstempel

    startbahnhoefe = ["Aalen Hbf"]  # Liste der Startbahnhöfe
    endbahnhoefe = ["Berlin Hbf", "Hamburg Hbf", "München Hbf", "Dortmund Hbf", "Frankfurt(Main)Hbf"]  # Liste der Endbahnhöfe

    for d in startbahnhoefe:
        for s in endbahnhoefe:
            dicttemp = crawler(d, s, 7, 5)  # Daten von Crawler-Funktion abrufen
            temp = polishData(dicttemp, d, s, timestamp)  # Daten polieren und in temporäres DataFrame speichern
            final = pd.concat([final, temp])  # Temporäres DataFrame an das endgültige DataFrame anhängen
            print(f"Verarbeitete Daten für {d} nach {s}:")
            print(temp)  # Temporäres DataFrame anzeigen

    try:
        final.to_sql('your_table', engine, if_exists='append', index=False)  # Daten in die Datenbank einfügen
        print("Daten erfolgreich in die Datenbank eingefügt.")
    except Exception as error:
        print("Fehler beim Einfügen der Daten in die Datenbank:", error)

# Automatisierte ausführung des Crawlers in einem definierten Zeitintervall
def run_scheduler():
    scheduler = BackgroundScheduler(max_instances=2)

    save_crawler_to_db()  # Speichern der Crawler-Daten in der Datenbank

    scheduler.add_job(save_crawler_to_db, 'interval', minutes=20)  # Hinzufügen des geplanten Tasks

    try:
        scheduler.start()
        print("Scheduler gestartet. Drücken Sie Strg+C zum Beenden.")
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        scheduler.shutdown()

# Beispielcode, falls jede volle Stunde gecrawlt werden soll

# def run_scheduler():
#     scheduler = BackgroundScheduler()

#     save_crawler_to_db()

#     scheduler.add_job(save_crawler_to_db, 'cron', minute=0)

#     try:
#         scheduler.start()
#         print("Scheduler started. Press Ctrl+C to exit.")
#         while True:
#             time.sleep(2)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         scheduler.shutdown()


if __name__ == '__main__':
    run_scheduler()
