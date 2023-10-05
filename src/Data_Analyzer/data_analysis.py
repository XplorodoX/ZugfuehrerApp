# Author: Marc Nebel
# Beschreibung: Ausführendes Modul, welches die Funktionen des compute Moduls einsetzt und die Funktionen mit Daten aus der API Datenbank speißt

import time
import compute
import schedule
from datetime import datetime, timedelta
import db_connect

import requests
import schedule

import compute

# Liste der derzeitig nutzbaren Station IDs. Sollte die App jemals auf einem höheren Preismodell laufen wird diese Liste erweitert.
# "Aalen Hbf", "Schwäbisch Gmünd", "Heidenheim", "Langenau(Württ)", "Ulm Hbf", "Schorndorf", "Stuttgart Hbf", "Nürnberg Hbf", "Ellwangen", "Donauwörth", "Waiblingen", "Crailsheim", "Karlsruhe Hbf", "Pforzheim Hbf", "Nördlingen", "Oberkochen", "München Hbf", "Augsburg Hbf"
STATIONS = ["8000002","8000329", "8002689", "8003525", "8000170", "8005424", "8000096", "8000284", "8001751", "784839", "8000180", "8000067", "8000191", "8000299", "8000280", "8004549", "8000261", "8000013"]

ip = "192.168.0.6"  
port = "5001"

# Funktion welche Daten von der API Datenbank liest, die Daten über die to_pandas Funktion in einen DF flach konvertiert um dann anschließlich die Werte über die delay
# Funktion in die Datenbank zu speißen. Anschließend werden die einzelnen compute Module hintereinander ausgeführt.
def get_train_data(trainstation, date, hour):
    url = f"http://{ip}:{port}/timetable/{trainstation}/{date}/{hour}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if not data:
                print(f"Recieved no data for station {trainstation} at {date} {hour}")
                return 1
            data = compute.to_pandas(data)
            compute.delay(data)
            compute.average_delay_all_time()
            compute.average_delay_destination()
            compute.average_delay_daily(datetime.now().strftime("%Y-%m-%d"))
            compute.average_delay_weekly(datetime.now().strftime("%Y-%m-%d"))
            compute.average_delay_monthly(datetime.now().strftime("%Y-%m-%d"))
            print(f"Computed data for station {trainstation} at {date} {hour}")

        else:
            print(f'FEHLER: Anfrage fehlgeschlagen. Statuscode: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'FEHLER: Fehler bei der Anfrage an {url}.')
        print(f'Fehlermeldung: {str(e)}')

# Funktion welche alle 59 Sekunden die aktuellen Daten über die get_train_data Funktion für jeden Bahnhof aktualisiert.
def refresh_data():
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_hour = (datetime.now() + timedelta(hours=2)).strftime("%H")
    for station in STATIONS:
        get_train_data(station, current_date, current_hour)
schedule.every(59).seconds.do(refresh_data)

# Haupt Programm Schleife welche den Scheduler mit einer Verzögerung von einer Sekunde immer erneut ausführt.
while True:
    schedule.run_pending()
    time.sleep(1)

# Testfunktion für das schnelle Auffüllen der Verspätungsdatenbank, sollten Daten von mehreren vergangenen Tagen in der API Datenbank liegen
def test():
    current_date = datetime.now()
    current_hour = (datetime.now() + timedelta(hours=2)) #TODO

    for station in STATIONS:
        for i in reversed(range(3)):
            for s in reversed(range(24)):
                get_train_data(station,  (current_date - timedelta(days=i)).strftime("%Y-%m-%d"), (current_hour - timedelta(hours=s)).strftime("%H"))

#test()
