# Author: Marc Nebel
# Beschreibung: Flask REST Modul welches die Daten der Data_Analyzer DB für das Frontend 
# bereitstellt.

from flask import Flask, jsonify
from flask_cors import CORS
from manual import manual
import db_connect

# Initialisieren des Flask Objektes mit CORS Richtlinie um direkten Frontendzugriff zu erlauben
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Definieren der Standard Route. Diese gibt eine Liste der Tabellen und Spalten als JSON Objekt 
# mit Beschreibungen pro Tablle zurück
#TODO
@app.route('/')
def man():
    return jsonify(manual)

# Errorhandler welcher bei Fehler Statuscode 500 und den Fehler zurückgibt
@app.errorhandler(Exception)
def handle_error(error):
    response = jsonify({'error': str(error)})
    response.status_code = 500
    return response

# Route für das Ausgeben einer gesammten SQL Tabelle. Unsichere Lösung aber einfache Lösung
@app.route('/<table_name>/')
def get_data(table_name):
    try:
        data = db_connect.get_table(table_name)
        data = data.to_json(orient='records')
        return data
    except Exception:
        raise Exception("Error: Table does not exist")
    
# Route für das Ausgeben einer gesammten SQL Tabelle mit einem Suchparameter. So lassen sich z.B.
# Alle Daten zur Zugverbidnung(n) mit der Nummer 19456 anzeigen
@app.route('/<table_name>/<param1>/<value1>')
def get_data_with_param1(table_name, param1, value1):
    try:
        data = db_connect.get_table_specific(table_name, param1, value1)
        data = data.to_json(orient='records')
        return data
    except Exception:
        raise Exception("Either wrong table or param name")

# Route für das Ausgeben einer gesammten SQL Tabelle mit zwei Suchparametern. Ermöglicht spezifischere
# Filterung von Daten
@app.route('/<table_name>/<param1>/<value1>/<param2>/<value2>')
def get_data_with_param2(table_name, param1, value1, param2, value2):
    try:
        data = db_connect.get_table_specific2(table_name, param1, value1, param2, value2)
        data = data.to_json(orient='records')
        return data
    except Exception:
        raise Exception("Either wrong table or param name")

# Route für das Ausgeben einer gesammten SQL Tabelle mit drei Suchparametern. Ermöglicht noch 
# spezifischere Filterung von Daten
@app.route('/<table_name>/<param1>/<value1>/<param2>/<value2>/<param3>/<value3>')
def get_data_with_param3(table_name, param1, value1, param2, value2, param3, value3):
    try:
        data = db_connect.get_table_specific3(table_name, param1, value1, param2, value2, param3, value3)
        data = data.to_json(orient='records')
        return data
    except Exception:
        raise Exception("Either wrong table or param name")

# Starten des Flask Servers
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)