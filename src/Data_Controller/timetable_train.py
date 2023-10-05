# Author: Florian Merlau
# convert the data from the api to a timetable object
# the timetable object contains a list of trains and the station

# import the necessary modules
from datetime import datetime
from typing import Tuple
from train import Train
from trainchanges import TrainChanges
from trainstation import trainstation


class Train_Timetable:
    station: trainstation
    # Konstruktor der Klasse Train_Timetable
    def __init__(self):
        self.station = None  # Eine Instanz der Klasse trainstation wird als station-Attribut gespeichert
        self.trains = []  # Eine leere Liste zur Speicherung von Train-Objekten wird erstellt

    # Die Methode wandelt das Datum im Format '2304132237' in ein brauchbares Dateformat und eine Time für PostgreSQL um
    def convert_date(self, date: str) -> Tuple[datetime, datetime]:
        if date is None:
            return None, None
        dt = datetime.strptime(date, '%y%m%d%H%M')
        formatted_date = dt.strftime("%Y-%m-%d")
        formatted_time = dt.strftime("%H:%M:%S")
        return formatted_date, formatted_time

    # Die Methode verarbeitet die Daten, die von der API kommen und erstellt ein Train-Objekt
    def get_timetable_info(self, data) -> list[Train]:
        train_list: list[Train] = []  # Eine leere Liste zur Speicherung von Train-Objekten wird erstellt

        trains = data["timetable"]["s"]
        trainstation = data["timetable"]["@station"]

        # prüfe, ob trains ein dict oder eine Liste ist
        if isinstance(trains, dict):
            # `trains` enthält nur ein Element
            train_id = trains["@id"]
            train_label_object = trains.get("tl", None)
            arrival = trains.get("ar", None)
            departure = trains.get("dp", None)

            train_ob = Train()
            train_ob.train_id = train_id

            train_ob.arrival_time = None
            train_ob.departure_time = None

            # prüfen ob es ein tl-Objekt gibt
            if train_label_object:
                train_ob.train_type = train_label_object.get("@c", None)
                train_ob.train_number = train_label_object.get("@n", None)
                if "f" in train_label_object:
                    train_ob.passed_stations = train_label_object["f"]

            # prüfen ob es ein ar-Objekt gibt
            if arrival:
                train_ob.arrival = arrival.get("@pt", None)
                train_ob.train_off = arrival.get("@l", None)
                train_ob.arrival_date, train_ob.arrival_time = self.convert_date(train_ob.arrival)

            # prüfen ob es ein dp-Objekt gibt
            if departure:
                train_ob.platform = departure.get("@pp", None)
                train_ob.stations = departure.get("@ppth", None)
                train_ob.departure = departure.get("@pt", None)
                train_ob.train_off = arrival.get("@l", None)
                train_ob.departure_date, train_ob.departure_time = self.convert_date(train_ob.departure)

            # prüfen ob es ein ar-Objekt gibt
            if departure is None:
                train_ob.date = train_ob.arrival_date
                train_ob.platform = arrival.get("@pp", None)
                train_ob.train_off = arrival.get("@l", None)
                train_ob.stations = arrival.get("@ppth", None)
            else:
                train_ob.date = train_ob.departure_date

            # prüfen ob platform leer ist
            if train_ob.platform == "":
                train_ob.platform = None

            #füge das Train-Objekt der Liste hinzu
            train_list.append(train_ob)

            return train_list, trainstation
        else:
            # `trains` enthält eine Liste von Stationen
            for train in trains:
                # hole die Daten aus dem dict
                train_id = train["@id"]
                train_label_object = train.get("tl")
                arrival = train.get("ar")
                departure = train.get("dp")
                # Erstelle ein Train-Objekt
                train_ob = Train()
                train_ob.train_id = train_id
                train_ob.arrival_time = None
                train_ob.departure_time = None

                # prüfen ob es ein tl-Objekt gibt
                if train_label_object:
                    train_ob.train_type = train_label_object.get("@c", None)
                    train_ob.train_number = train_label_object.get("@n", None)
                    if "f" in train_label_object:
                        train_ob.passed_stations = train_label_object["f", None]
                # prüfen ob es ein ar-Objekt gibt
                if arrival:
                    train_ob.arrival = arrival.get("@pt", None)
                    train_ob.train_off = arrival.get("@l", None)
                    train_ob.arrival_date, train_ob.arrival_time = self.convert_date(train_ob.arrival)
                # prüfen ob es ein dp-Objekt gibt
                if departure:
                    train_ob.platform = departure.get("@pp", None)
                    train_ob.stations = departure.get("@ppth", None)
                    train_ob.departure = departure.get("@pt", None)
                    train_ob.train_off = departure.get("@l", None)
                    train_ob.departure_date, train_ob.departure_time = self.convert_date(train_ob.departure)
                    if "l" in departure:
                        train_ob.stations = departure["l"]
                # prüfen ob es ein ar-Objekt gibt
                if departure is None:
                    train_ob.date = train_ob.arrival_date
                    train_ob.platform = arrival.get("@pp", None)
                    train_ob.stations = arrival.get("@ppth", None)
                    train_ob.train_off = arrival.get("@l", None)
                else:
                    train_ob.date = train_ob.departure_date
                # prüfen ob platform leer ist
                if train_ob.platform == "":
                    train_ob.platform = None
                # füge das Train-Objekt der Liste hinzu
                train_list.append(train_ob)
            return train_list, trainstation

    # Methode zum Abrufen der Timetable änderungen
    def get_timetable_changes(self, data) -> list[TrainChanges]:
        train_changes_list: list[TrainChanges] = []

        trains = data["timetable"]["s"]
        trainstation = data["timetable"]["@eva"]

        #iteriuere über alle Züge
        for change_train in trains:
            #erstelle ein TrainChanges-Objekt
            train_changes = TrainChanges()
            train_changes.time_id = change_train.get("@id", None)

            arrival = change_train.get("ar", None)
            departure = change_train.get("dp", None)

            train_changes.arrival_time = None
            train_changes.departure_time = None

            #prüfen ob es ein dp-Objekt gibt
            if departure:
                train_changes.departure = departure.get("@ct", None)
                train_changes.departure_date, train_changes.departure_time = self.convert_date(train_changes.departure)
                train_changes.stations = departure.get("cpth", None)
                train_changes.platform = departure.get("cp", None)
                train_changes.date = train_changes.departure_date
            #prüfen ob es ein ar-Objekt gibt
            if arrival:
                train_changes.arrival = arrival.get("@ct", None)
                train_changes.arrival_date, train_changes.arrival_time = self.convert_date(train_changes.arrival)
                train_changes.passed_stations = arrival.get("cpth", None)
                train_changes.platform = arrival.get("@pp", None)
                train_changes.stations = arrival.get("@ppth", None)
                train_changes.date = train_changes.arrival_date
            #prüfen ob es ein ar-Objekt gibt
            if not departure and not arrival:
                train_changes.date = None
            #prüfen ob platform leer ist
            if train_changes.platform == "":
                train_changes.platform = None
            #füge das TrainChanges-Objekt der Liste hinzu
            train_changes_list.append(train_changes)

        return train_changes_list, trainstation