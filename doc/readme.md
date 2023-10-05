# Author: Florian Merlau

---

# Anleitung zur Ausführung unseres Dienstes in Docker.

## Voraussetzungen
Docker muss installiert sein.

## Ausführen des Dienstes
Clone das Repository und führe folgenden Befehl aus:
```
git clone git@bitbucket.org:roberhau/23s-cdc-teamg.git
```

Navigiere in den Ordner `23s-cdc-teamg7/src`.

Führe folgenden Befehl aus:
```
docker-compose up
```

Das nimmt jetzt ein paar Minuten in Anspruch, da die Images erstellt werden müssen.

Jetzt sollte der Dienst laufen und das Frontend unter http://localhost:80 erreichbar sein.

## Beenden des Dienstes
Die Container beenden:
```
docker-compose down
```

## Die Container beenden und die Images löschen:
```
docker-compose down --rmi all
```
## Mögliche Fehler und Lösungen
- Es kann zu einem Fehler im Api Connector kommen, wenn man ihn zu spät am Tag zum ersten Mal startet. Es wird empfohlen, den Api Connector morgens früh zu starten oder die Werte in der Schleife in der Datei API_Connector.py von 13 bis 23 Uhr anzupassen.
Leider war aus Zeitgründen keine Zeit mehr, um das Problem zu beheben.