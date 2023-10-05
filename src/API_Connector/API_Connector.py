# Autor: Florian Merlau
# Beschreibung:
# Dieses Modul stellt die Klasse API_Connector zur Verfügung,
# welche die Verbindung zur DB-API herstellt und die Daten holt und an den DataController weiterleitet

# Importieren der benötigten Module
import datetime
import http.client
import json
import time
import requests
import xmltodict

# Station IDs
# "Aalen Hbf", "Schwäbisch Gmünd", "Heidenheim", "Langenau(Württ)", "Ulm Hbf", "Schorndorf", "Stuttgart Hbf", "Nürnberg Hbf", "Ellwangen", "Donauwörth", "Waiblingen", "Crailsheim", "Karlsruhe Hbf", "Pforzheim Hbf", "Nördlingen", "Oberkochen", "München Hbf", "Augsburg Hbf"
STATIONS = ["8000002","8000329", "8002689", "8003525", "8000170", "8005424", "8000096", "8000284", "8001751", "8000180", "8000067", "8000191", "8000299", "8000280", "8004549", "8000261", "8000013"]

# Herstellen einer Verbindung zur Deutschen Bahn API
conn = http.client.HTTPSConnection("apis.deutschebahn.com")

# Festlegen der erforderlichen Header für die API-Anfrage
headers = {
    "DB-Client-Id": "70b868be8702277c035ff6345c68c5d0",
    "DB-Api-Key": "5cbf3b674b3eb4ce5e5d15a82da8abeb",
    "Accept": "application/xml",
}

# Klasse zum Herstellen einer Verbindung zur Deutschen Bahn API
class API_Connector:

    # Methode zum Abrufen des Fahrplans
    @staticmethod
    def process_data(url, data):
        try:
            # Sende eine POST-Anfrage an die angegebene URL mit den übergebenen Daten
            response = requests.post(url, json=data)
            response.raise_for_status()  # Überprüfe den Statuscode der Antwort

            # Überprüfe den Statuscode der Antwort und gib eine entsprechende Meldung aus
            if response.status_code == 200:
                print("Daten erfolgreich gesendet!")
            elif response.status_code == 400:
                print("Fehler")
            else:
                print("Fehler beim Senden der Daten")
        except requests.exceptions.RequestException as e:
            # Behandle Ausnahmen, die während des Anfrageprozesses auftreten können
            print(f"Fehler beim Senden der Daten: {str(e)}")

    # Methode zum Abrufen des Fahrplans der gewussten Änderungen
    def get_known_changes(self):
        try:
            # Iteriere über jede Bahnhofs-ID in der STATIONS-Liste
            for id in STATIONS:
                # Sende eine GET-Anfrage an die Deutsche Bahn API, um Änderungen für den aktuellen Bahnhof abzurufen
                conn.request("GET", f"/db-api-marketplace/apis/timetables/v1/fchg/{id}", headers=headers)
                res = conn.getresponse()

                # Überprüfe den Statuscode der Antwort und führe entsprechende Aktionen aus
                if res.status == 200:
                    # Lese die Antwortdaten und konvertiere sie von XML zu JSON
                    data = res.read()
                    data = xmltodict.parse(data)
                    data = json.loads(json.dumps(data))
                    # Verarbeite die erhaltenen Daten und sende sie an eine bestimmte URL
                    self.process_data(f"http://192.168.0.6:5001/delay_data", data)
                elif res.status == 410:
                    # Der Statuscode 410 bedeutet, dass keine Änderungen für den aktuellen Bahnhof vorhanden sind
                    print(f"Keine Änderungen für ID {id}")
                    res.close()
                    continue
                else:
                    # Bei anderen Statuscodes wird ein Verbindungsfehler oder ein Problem mit der Anfrage angezeigt
                    print(f"Verbindungsfehler für ID {id}: {res.status} {res.reason}")
                    res.close()
                    continue
                res.close()
        except Exception as e:
            # Behandle allgemeine Ausnahmen, die während des Prozesses auftreten können
            print(f"Ein Fehler ist aufgetreten: {str(e)}")

    # Methode zum Abrufen des akutellen Fahrplans
    def get_timetable(self):
        try:
            # Aktuelles Datum im Format "YYMMDD" erhalten
            datum = datetime.date.today().strftime("%y%m%d")

            # Iteriere über jede Bahnhofs-ID in der STATIONS-Liste
            for id in STATIONS:
                # Schleife über die Stunden von 0 bis 23
                for stunde in range(13, 23):
                    # Sende eine GET-Anfrage an die Deutsche Bahn API, um den Fahrplan für den aktuellen Bahnhof und die aktuelle Stunde abzurufen
                    conn.request("GET", f"/db-api-marketplace/apis/timetables/v1/plan/{id}/{datum}/{stunde:02}",
                                 headers=headers)
                    res = conn.getresponse()

                    # Überprüfe den Statuscode der Antwort und führe entsprechende Aktionen aus
                    if res.status == 200:
                        # Lese die Antwortdaten und konvertiere sie von XML zu JSON
                        data = res.read()
                        data = xmltodict.parse(data)
                        data = json.loads(json.dumps(data))
                        # Verarbeite die erhaltenen Daten und sende sie an eine bestimmte URL
                        self.process_data(f"http://192.168.0.6:5001/data", data)
                    elif res.status == 410:
                        # Der Statuscode 410 bedeutet, dass für die aktuelle Stunde keine Fahrplaninformationen vorhanden sind
                        print(f"Error 410 for ID {id}, hour {stunde}. Skipping to the next hour.")
                        res.close()
                        continue
                    else:
                        # Bei anderen Statuscodes wird ein Fehler bei der Anfrage angezeigt
                        print(f"Request failed for ID {id}, hour {stunde}. Status code: {res.status}")
                        res.close()
                        continue

                    # Eine kurze Pause einlegen, um den Server nicht zu überlasten
                    time.sleep(2)
                    res.close()
        except Exception as e:
            # Behandle allgemeine Ausnahmen, die während des Prozesses auftreten können
            print("An error occurred while getting the timetable:", str(e))

    # Methode zum Abrufen der kürzlich vorgenommenen Änderungen
    def get_recent_changes(self):
        try:
            # Iteriere über jede Bahnhofs-ID in der STATIONS-Liste
            for id in STATIONS:
                # Sende eine GET-Anfrage an die Deutsche Bahn API, um kürzlich vorgenommene Änderungen für den aktuellen Bahnhof abzurufen
                conn.request("GET", f"/db-api-marketplace/apis/timetables/v1/rchg/{id}", headers=headers)
                res = conn.getresponse()

                # Überprüfe den Statuscode der Antwort und führe entsprechende Aktionen aus
                if res.status == 200:
                    # Lese die Antwortdaten und konvertiere sie von XML zu JSON
                    data = res.read()
                    data = xmltodict.parse(data)
                    data = json.loads(json.dumps(data))
                    # Verarbeite die erhaltenen Daten und sende sie an eine bestimmte URL
                    self.process_data(f"http://192.168.0.6:5001/delay_data", data)
                elif res.status == 410:
                    # Der Statuscode 410 bedeutet, dass für den aktuellen Bahnhof keine kürzlichen Änderungen vorhanden sind
                    print(f"Error 410 for ID {id}. Skipping to the next station.")
                    res.close()
                    continue
                else:
                    # Bei anderen Statuscodes wird ein Verbindungsfehler oder ein Problem mit der Anfrage angezeigt
                    print(f"Verbindungsfehler: {res.status} {res.reason}")
                    res.close()
                    continue
                res.close()
        except Exception as e:
            # Behandle allgemeine Ausnahmen, die während des Prozesses auftreten können
            print(f"Ein Fehler ist aufgetreten: {str(e)}")
