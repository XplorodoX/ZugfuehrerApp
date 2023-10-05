
# Author: Florian Merlau

---

# API-Endpoint Data Controller

## Timetable

- **Pfad:** `/timetable/{trainstation}/{date}/{hour}`
- **Methoden:** GET
- **Beschreibung:** Ruft den Fahrplan für eine bestimmte Bahnhofsstation ab, basierend auf dem angegebenen Datum und der Stunde.
- **Parameter:**
  - `{trainstation}`: Der Name der Bahnhofsstation (String)
  - `{date}`: Das Datum im Format "YYYY-MM-DD" (String)
  - `{hour}`: Die Stunde im Format "HH:MM" (String)

## Timetable_Date

- **Pfad:** `/timetable/{trainstation}/{date}`
- **Methoden:** GET
- **Beschreibung:** Ruft den Fahrplan für eine bestimmte Bahnhofsstation ab, basierend auf dem angegebenen Datum.
- **Parameter:**
  - `{trainstation}`: Der Name der Bahnhofsstation (String)
  - `{date}`: Das Datum im Format "YYYY-MM-DD" (String)

## train_number

- **Pfad:** `/destination/{train_number}`
- **Methoden:** GET
- **Beschreibung:** Ruft Informationen zu einem bestimmten Zug basierend auf der Zugnummer ab.
- **Parameter:**
  - `{train_number}`: Die Zugnummer (String)

## input_data

- **Pfad:** `/data`
- **Methoden:** POST
- **Beschreibung:** Sendet Eingabedaten für den Fahrplan.
- **Parameter:** Keine zusätzlichen Parameter erforderlich. Die Daten sollten im Anforderungskörper als JSON-Objekt gesendet werden.

## input_delay_data

- **Pfad:** `/delay_data`
- **Methoden:** POST
- **Beschreibung:** Sendet Eingabedaten für Zugverspätungen.
- **Parameter:** Keine zusätzlichen Parameter erforderlich. Die Daten sollten im Anforderungskörper als JSON-Objekt gesendet werden.

## get_all

- **Pfad:** `/get_all`
- **Methoden:** GET
- **Beschreibung:** Ruft alle verfügbaren Daten ab.
- **Parameter:** Keine zusätzlichen Parameter erforderlich.

---

# API-Endpoint Data Analyses

## get_all
- **Pfad:** `/table_name/param1/value1/param2/value2/param3/value3`
- **Methoden:** GET
- **Beschreibung:** Dieser Endpunkt ermöglicht die Durchführung von Datenanalysen, indem nach bestimmten Parametern in der angegebenen Tabelle gesucht wird. Es können bis zu drei Parameter-Wert-Paare angegeben werden, um die Suche einzuschränken.
- **Parameter:**
  - `<table_name>` (Pfad-Parameter): Der Name der Tabelle, in der die Suche durchgeführt werden soll.
  - `<param1>` (Pfad-Parameter): Der Name des ersten Parameters, nach dem gesucht werden soll.
  - `<value1>` (Pfad-Parameter): Der Wert des ersten Parameters, nach dem gesucht werden soll.
  - `<param2>` (Pfad-Parameter): Der Name des zweiten Parameters, nach dem gesucht werden soll.
  - `<value2>` (Pfad-Parameter): Der Wert des zweiten Parameters, nach dem gesucht werden soll.
  - `<param3>` (Pfad-Parameter): Der Name des dritten Parameters, nach dem gesucht werden soll.
  - `<value3>` (Pfad-Parameter): Der Wert des dritten Parameters, nach dem gesucht werden soll.


- **Pfad:** `/table_name/param1/value1/param2/value2`
  - **Methoden:** GET
  - **Beschreibung:** Dieser Endpunkt ermöglicht die Suche mit zwei Parametern und ihren entsprechenden Werten in der angegebenen Tabelle.


- **Pfad:** `/table_name/param1/value1`
  - **Methoden:** GET
    - **Beschreibung:** Dieser Endpunkt ermöglicht die Suche mit einem Parameter und seinem Wert in der angegebenen Tabelle.

- **Pfad:** `/table_name/`
  - **Methoden:** GET
  - **Beschreibung:** Dieser Endpunkt gibt alle Einträge in der angegebenen Tabelle zurück, ohne Einschränkung durch spezifische Parameter.

---

# API-Endpoint Web_Crawler_Analyser

1. **Pfad:** `/metrics/<endbahnhof>`
   - **Methode:** GET
   - **Beschreibung:** Diese API-Schnittstelle liefert den Durchschnittspreis, den Höchstpreis und den Mindestpreis für einen bestimmten Endbahnhof in Schritten.

2. **Pfad:** `/budget/float:<budget>/int:<vonUhrzeit>/int:<bisUhrzeit>/<endbahnhof>`
   - **Methode:** GET
   - **Beschreibung:** Diese API-Schnittstelle gibt die Preise für einen bestimmten Endbahnhof zurück, basierend auf einem bestimmten Budget, einer Uhrzeit von und bis. Das Budget wird als Fließkommazahl (float) und die Uhrzeiten als Ganzzahlen (int) angegeben.

3. **Pfad:** `/preisanstiege/<endbahnhof>`
   - **Methode:** GET
   - **Beschreibung:** Diese API-Schnittstelle gibt die Preisanstiege für den gewählten Endbahnhof zurück.

4. **Pfad:** `/preisanstiege_alle`
   - **Methode:** GET
   - **Beschreibung:** Diese API-Schnittstelle gibt alle Preisanstiege zurück.

5. **Pfad:** `/preistrend/<endbahnhof>`
   - **Methode:** GET
   - **Beschreibung:** Diese API-Schnittstelle liefert den Preistrend für den gewählten Endbahnhof zurück.

6. **Pfad:** `/basispreise/<endbahnhof>`
   - **Methode:** GET
   - **Beschreibung:** Diese API-Schnittstelle gibt die Basispreise für den gewählten Endbahnhof zurück.
---

# API-Endpoint Web Crawler Analyses

**POST '/plot'**
- **Methode:** POST
- **Beschreibung:** Über diese API-Schnittstelle erhält man ein JSON mit einem Base64-codierten Bild, das für das geplottete Diagramm des Web-Crawlers steht.

Ein Benutzer kann eine POST-Anfrage an diesen Endpunkt senden und erhält als Antwort ein JSON-Objekt, das das Base64-codierte Bild des geplotteten Diagramms des Web-Crawlers enthält. Dieses Bild kann dann in einem Webbrowser oder einer Anwendung angezeigt werden.

Das JSON-Objekt enthält das Bild im Base64-Format, was bedeutet, dass es als Zeichenkette codiert ist und leicht in ein Bild umgewandelt werden kann.

Beispielantwort:
```
{
  "image": "data:image/png;base64,iVBORw0KG..."
}
```

Das Frontend kann die empfangene Base64-Zeichenkette verwenden, um das Bild darzustellen oder für weitere Verarbeitungszwecke zu verwenden.
---