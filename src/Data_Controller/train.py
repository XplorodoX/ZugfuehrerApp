# Author: Florian Merlau
# Definiere die Klasse Train
class Train:
    def __init__(self):
        # Initialisiere die Attribute der Zugklasse
        self.train_id = None  # ID des Zugs
        self.stop_id = None  # ID der Haltestelle
        self.train_type = None  # Art des Zugs (z.B. Regionalzug, Intercity)
        self.train_number = None  # Zugnummer
        self.train_off = None  # Offizielle Zugnummer
        self.stations = None  # Liste der Stationen, die der Zug bedient
        self.arrival = None  # Ankunftszeit an der aktuellen Station
        self.departure = None  # Abfahrtszeit von der aktuellen Station
        self.platform = None  # Bahnsteig, an dem der Zug hält
        self.passed_stations = None  # Liste der bereits passierten Stationen