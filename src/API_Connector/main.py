# Autor: Florian Merlau
# Das ist die main Methode, die die Aufgaben plant und ausführt
# Die Aufgaben werden in der API_Connector-Klasse ausgeführt
# Die Aufgaben werden täglich um 0:01 Uhr und alle 30 Sekunden ausgeführt

import time
from datetime import datetime, timedelta
import schedule
from API_Connector import API_Connector

# Methode erstellt eine task Instanz und ruft die Methoden get_timetable() und get_known_changes() auf
def task():
    # Erstelle eine Instanz der API_Connector-Klasse
    change = API_Connector()
    print("get Timetable")
    # Rufe die Methode get_timetable() auf, um den Fahrplan abzurufen
    change.get_timetable()
    print("get known changes")
    # Rufe die Methode get_known_changes() auf, um bekannte Änderungen abzurufen
    change.get_known_changes()

# Methode erstellt eine task Instanz und ruft die Methode get_recent_changes() auf
def get_recent_changes_task():
    # Erstelle eine Instanz der API_Connector-Klasse
    change = API_Connector()
    print("get recent changes")
    # Rufe die Methode get_recent_changes() auf, um kürzlich vorgenommene Änderungen abzurufen
    change.get_recent_changes()

# Methode plant die Aufgaben, die täglich um 0 Uhr und die andere alle 30 Sekunden ausgeführt werden sollen
def run_scheduler():
    # Setze die anfängliche geplante Zeit für den nächsten Tag um 0:01 Uhr
    scheduled_time = datetime.now().replace(hour=0, minute=1) + timedelta(days=1)

    # Plane die Aufgabe, täglich um 0:01 Uhr ausgeführt zu werden
    schedule.every().day.at(scheduled_time.strftime("%H:%M")).do(task)

    # Plane die Aufgabe, alle 30 Sekunden ausgeführt zu werden
    schedule.every(30).seconds.do(get_recent_changes_task)

    # Führe die geplanten Aufgaben aus
    while True:
        schedule.run_pending()
        time.sleep(1)

# Starte die main-Methode, wenn das Skript direkt ausgeführt wird
if __name__ == '__main__':
    print("Starting initial task")
    # Führe die Aufgabe einmalig aus, um die anfänglichen Daten zu erhalten
    task()

    print("Starting scheduler")
    # Starte den Scheduler, um die geplanten Aufgaben auszuführen
    run_scheduler()
