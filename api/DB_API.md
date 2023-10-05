# Author: Florian Merlau

---

Deutsche Bahn API Timetable Information

**1. Abfrage des aktuellen Fahrplans für eine Station:**

API-Endpunkt:
```
GET https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/fchg/{evaNo}
```

Beschreibung:
Diese API gibt einen Fahrplan zurück, der alle bekannten Veränderungen für die angegebene Station (evaNo) enthält. Die Daten umfassen alle bekannten Veränderungen von jetzt bis in die unendliche Zukunft. Sobald Veränderungen veraltet sind (weil ihre Fahrt vom Bahnhof abfährt), werden sie aus dieser Ressource entfernt. Veränderungen können auch Nachrichten enthalten. Die vollständigen Veränderungen werden alle 30 Sekunden aktualisiert und sollten für diesen Zeitraum von Web-Caches zwischengespeichert werden.

**2. Abfrage des geplanten Fahrplans für eine Station innerhalb eines bestimmten Zeitfensters:**

API-Endpunkt:
```
GET https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/{evaNo}/{date}/{hour}
```

Beschreibung:
Diese API gibt einen Fahrplan zurück, der geplante Daten für die angegebene Station (evaNo) innerhalb des stündlichen Zeitfensters enthält, das durch Datum (Format YYMMDD) und Stunde (Format HH) definiert ist. Die Daten umfassen Haltestellen für alle Fahrten, die innerhalb dieses Zeitfensters ankommen oder abfahren. Es gibt eine kleine Überlappung zwischen den Zeitfenstern, da einige Fahrten in einem Zeitfenster ankommen und in einem anderen abfahren. Geplante Daten enthalten niemals Nachrichten. Die geplanten Daten enthalten die geplanten Attribute pt, pp, ps und ppth, während die veränderten Attribute ct, cp, cs und cpth fehlen.

**3. Abfrage der kürzlich eingetretenen Veränderungen für eine Station:**

API-Endpunkt:
```
GET https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/rchg/{evaNo}
```

Beschreibung:
Diese API gibt einen Fahrplan zurück, der alle kürzlich eingetretenen Veränderungen für die angegebene Station (evaNo) enthält. Kürzlich eingetretene Veränderungen sind immer eine Teilmenge der vollständigen Veränderungen. Sie können den vollständigen Veränderungen entsprechen, sind aber in der Regel viel kleiner. Die Daten enthalten nur die Veränderungen, die innerhalb der letzten 2 Minuten bekannt wurden. Ein Client, der seinen Zustand in Intervallen von weniger als 2 Minuten aktualisiert, sollte zuerst die vollständigen Veränderungen laden und dann regelmäßig nur die kürzlich eingetretenen Veränderungen laden, um Bandbreite zu sparen. Die kürzlich eingetretenen Veränderungen werden ebenfalls alle 30 Sekunden aktualisiert und sollten für diesen Zeitraum von Web-Caches zwischengespeichert werden.

Bei Verwendung dieser APIs müssen Sie Ihre Client-ID (DB-Client-Id) und Ihren API-Schlüssel (DB-Api-Key) im Header angeben. Die Antwort wird im XML-Format zurückgegeben.

Hier ist ein Beispielcode für die Verwendung der APIs mit Python und dem `http.client`-Modul:

```python
import http.client

conn = http.client.HTTP

SConnection("apis.deutschebahn.com")

headers = {
    'DB-Client-Id': "clientId",
    'DB-Api-Key': "clientSecret",
    'accept': "application/xml"
}

# Beispiel für die Abfrage des aktuellen Fahrplans für eine Station
conn.request("GET", "/db-api-marketplace/apis/timetables/v1/fchg/REPLACE_EVANO", headers=headers)

# Beispiel für die Abfrage des geplanten Fahrplans für eine Station innerhalb eines bestimmten Zeitfensters
conn.request("GET", "/db-api-marketplace/apis/timetables/v1/plan/REPLACE_EVANO/REPLACE_DATE/REPLACE_HOUR", headers=headers)

# Beispiel für die Abfrage der kürzlich eingetretenen Veränderungen für eine Station
conn.request("GET", "/db-api-marketplace/apis/timetables/v1/rchg/REPLACE_EVANO", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

Bitte beachten Sie, dass Sie die `clientId` und `clientSecret` durch Ihre eigenen gültigen Anmeldedaten für die Deutsche Bahn API ersetzen müssen. Außerdem sollten Sie die XML-Antwort entsprechend Ihrer Anwendungslogik verarbeiten.