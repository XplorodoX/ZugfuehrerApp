# Autor: Florian Merlau
# Definiere die Klasse TrainChanges

class TrainChanges:
    # Konstruktor der TrainChanges-Klasse
    def __init__(self):
        # Initialisiere die Attribute der TrainChanges-Klasse
        self.departure = None  # Abfahrtszeit
        self.arrival = None  # Ankunftszeit
        self.platform = None  # Bahnsteig
        self.stations = None  # Liste der Stationen
        self.passed_stations = None  # Liste der bereits passierten Stationen