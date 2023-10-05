# Autor: Florian Merlau
# Beschreibung:
# Dieses Modul stellt die Klasse Data_Controller zur Verfügung,
# welche die Daten vom API_Connector bekommt und Daten in die Datenbank schreibt

# Importieren der benötigten Module
from datetime import datetime, timedelta
import psycopg2
from flask import Flask, request
from flask_restx import Namespace, Api, Resource
from timetable_train import Train_Timetable

# Erstellen einer Flask-App und eines Flask-RESTX-APIs
app = Flask(__name__)
api = Api(app)

# Erstellen eines Flask-RESTX-Namespace
ns = Namespace('timetable', description='Timetable operations')
api.add_namespace(ns)

# Verbinde mit der Datenbank
def connect_to_database():
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        host="192.168.0.5",
        port="5432",
        database="postgres",
        user="postgres",
        password="example"
    )
    return conn

# Find the trainstation id in the CSV file
def find_trainstation_id(trainstation):
    with open('D_Bahnhof_2020_alle.CSV') as file:
        for line in file:
            if trainstation in line:
                trainstationid = line.split(';')[0]
                return trainstationid

# Konvertiert ein datetime-Objekt in einen String
def convert_time_to_sting(time):
    return time.strftime('%H:%M:%S') if time is not None else None

# Verarbeitet die Daten, die vom API_Connector kommen, gibt sie zurück
def process_data(row):
    date = row[2].strftime('%Y-%m-%d')
    name = row[3]
    arrival_time = convert_time_to_sting(row[4])
    departure_time = convert_time_to_sting(row[5])
    platform = row[6]
    train_number = row[7]
    train_type = row[8]
    destination = row[9]
    new_arrival_time = convert_time_to_sting(row[10])
    new_departure_time = convert_time_to_sting(row[11])
    new_platform = row[12]
    return date, name, arrival_time, departure_time, platform, train_number, train_type, destination, new_arrival_time, new_departure_time, new_platform

# gibt alle Einträge in der Datenbank aller Züge zurück
class get_all(Resource):
    def get(self):
        try:
            name = ""
            # Verbinde mit der Datenbank
            conn = connect_to_database()
            cur = conn.cursor()
            #SQL-Abfrage
            try:
                cur.execute("""
                                    SELECT t.*, c.new_arrival_time, c.new_departure_time, c.new_platform
                                   FROM timetable t
                                   LEFT JOIN changestimetable c ON t.timetable_id = c.timetable_id_new
                """, ())
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {str(e)}")

            #Holt alle Zeilen aus der Datenbank
            rows = cur.fetchall()
            data = []

            #iteriet durch alle Züge und fügt sie in die Liste data ein
            for row in rows:
                trainstation_id = row[1]

                date, name, arrival_time, departure_time, platform, train_number, train_type, destination, new_arrival_time, new_departure_time, new_platform = process_data(
                    row)
                # Fügt die Daten in die Liste data ein -> Json-Format
                data.append({
                    '@s_id': trainstation_id,
                    '@station': name,
                    '@train_type': train_type,
                    '@date': date,
                    '@n': train_number,
                    'planned': {
                        'ar_time': arrival_time,
                        'dp_time': departure_time,
                        'pl': platform,
                        'ppth': destination,
                    },
                    'changend': {
                        'n_ar_time': new_arrival_time,
                        'n_dp_time': new_departure_time,
                        'n_pl': new_platform
                    }
                })

            # Schließt die Verbindung zur Datenbank
            cur.close()
            conn.close()
            return data, 200
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {str(e)}")
            return None, 500

# gibt für eine Zugnummer alle Einträge in der Datenbank zurück
class train_number(Resource):
    def get(self, train_number):
        try:
            # Verbinde mit der Datenbank
            conn = connect_to_database()
            cur = conn.cursor()
            #SQL-Abfrage
            try:
                cur.execute("""
                    SELECT ts.trainstation_id, ts.name AS trainstation_name, tt.arrival_time, tt.train_type, tt.departure_time,
                           c.new_arrival_time, c.new_departure_time
                    FROM timetable tt
                    JOIN trainstation ts ON tt.trainstation_id = ts.trainstation_id
                    LEFT JOIN changestimetable c ON tt.timetable_id = c.timetable_id_new
                    WHERE tt.train_number = %s
                    ORDER BY tt.departure_time
                """, (train_number,))

            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {str(e)}")

            #Holt alle Zeilen aus der Datenbank
            rows = cur.fetchall()
            data = []
            # iteriet durch alle rows und fügt sie in die Liste data ein
            for row in rows:
                data.append({
                    'train_number': row[0],
                    'destination': row[1],
                    'arrival_time': convert_time_to_sting(row[2]),
                    'train_type': row[3],
                    'departure_time': convert_time_to_sting(row[4]),
                    'deleay_arrival_time': convert_time_to_sting(row[5]),
                    'deleay_departure_time': convert_time_to_sting(row[6]),
                })
            # Schließt die Verbindung zur Datenbank
            cur.close()
            conn.close()
            return data, 200
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {str(e)}")

# Erstellt eine Instanz der Klasse Train_Timetable und gibt die Daten von der Timetable zurück, dabei müssen die Parameter trainstation, date und hour angegeben werden
class Timetable(Resource):
    def get(self, trainstation,  date, hour):

        name = ""  # Standardwert für die Variable 'name'

        try:
            # Verbinde mit der Datenbank
            conn = connect_to_database()
            cur = conn.cursor()

            #Datum umwandeln
            datetime_str = date + ' ' + str(hour)
            datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H')

            #Endzeit berechnen
            end_time = datetime_obj + timedelta(hours=1)

            #SQL-Abfrage
            cur.execute("""
                            SELECT t.*, c.new_arrival_time, c.new_departure_time, c.new_platform
                            FROM timetable t
                            LEFT JOIN changestimetable c ON t.timetable_id = c.timetable_id_new
                            WHERE t.trainstation_id = %s AND t.date = %s AND t.departure_time >= %s AND t.departure_time < %s OR t.arrival_time >= %s AND t.arrival_time < %s
                        """, (trainstation, date, datetime_obj.time(), end_time.time(), datetime_obj.time(), end_time.time()))

            #Holt alle Zeilen aus der Datenbank
            rows = cur.fetchall()
            data = []

            # schließt die Verbindung zur Datenbank
            cur.close()
            conn.close()

            #iteriert durch alle rows und fügt sie in die Liste data ein
            for row in rows:
                trainstation_id = row[1]

                date, name, arrival_time, departure_time, platform, train_number, train_type, destination, new_arrival_time, new_departure_time, new_platform = process_data(row)

                # Fügt die Daten in die Liste data ein -> Json-Format
                data.append({
                    '@s_id': trainstation_id, #id of the trainstation
                    '@station': name, #name of the trainstation
                    '@train_type': train_type, #type of the train 'IC', 'ICE', 'RE', 'RB', 'S
                    '@date': date,  # date of the timetable
                    '@n': train_number,  # train number
                    'planned': {  # planed timetable
                        'ar_time': arrival_time,  # planed arrival time
                        'dp_time': departure_time,  # planed departure time
                        'pl': platform,  # planed platform
                        'ppth': destination,  # destination
                    },
                    'changend':{ #changed timetable
                        'n_ar_time': new_arrival_time, #changed arrival time
                        'n_dp_time': new_departure_time, #changed departure time
                        'n_pl': new_platform #changed platform
                    }
                })

            return data, 200
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {str(e)}")
            return str(e), 400

# Erstellt eine Instanz der Klasse Train_Timetable und gibt die Daten von der Timetable zurück, dabei müssen die Parameter trainstation, date angegeben werden
class Timetable_Date(Resource):
    def get(self, trainstation, date):
        try:
            name = ""  # Standardwert für die Variable 'name'

            # Verbinde mit der Datenbank
            conn = connect_to_database()
            cur = conn.cursor()

            #SQL-Abfrage
            try:
                cur.execute("""
                                    SELECT t.*, c.new_arrival_time, c.new_departure_time, c.new_platform
                                   FROM timetable t
                                   LEFT JOIN changestimetable c ON t.timetable_id = c.timetable_id_new
                                    WHERE t.trainstation_id = %s AND t.date = %s
                                """, (trainstation, date))

            except Exception as e:
                return str(e), 400

            # Holt alle Zeilen aus der Datenbank
            rows = cur.fetchall()
            data = []

            # schließt die Verbindung zur Datenbank
            for row in rows:
                trainstation_id = row[1]
                date, name, arrival_time, departure_time, platform, train_number, train_type, destination, new_arrival_time, new_departure_time, new_platform = process_data(row)

                # Fügt die Daten in die Liste data ein -> Json-Format
                data.append({
                    '@s_id': trainstation_id,
                    '@station': name,
                    '@train_type': train_type,
                    '@date': date,
                    '@n': train_number,
                    'planned': {
                        'ar_time': arrival_time,
                        'dp_time': departure_time,
                        'pl': platform,
                        'ppth': destination,
                    },
                    'changend': {
                        'n_ar_time': new_arrival_time,
                        'n_dp_time': new_departure_time,
                        'n_pl': new_platform
                    }
                })

            # schließt die Verbindung zur Datenbank
            cur.close()
            conn.close()
            return data, 200
        except Exception as e:
            return str(e), 400

# Bekommt Daten(Timetable Data) vom API Connector und verarbeitet diese und speichert sie in der Datenbank
class input_data(Resource):
    trainstationid = 0
    def post(self):
        try:
            # Json Daten werden aus dem Request geholt
            json_data = request.get_json()

            # Überprüft ob die Json Daten leer sind
            if json_data is None:
                return "Invalid JSON data", 401

            # Überprüft ob die Json Daten die richtigen Keys haben
            if json_data['timetable'] == None:
                return "No data", 430

            # Erstellt eine Instanz der Klasse Train_Timetable und bekommt die Daten von der Timetable
            timetable = Train_Timetable()
            train_list, trainstation = timetable.get_timetable_info(json_data)

            # Erstellt eine Instanz der Klasse Train_Timetable und bekommt die Daten von der Timetable
            trainstationid = find_trainstation_id(trainstation)

            # Verbinde mit der Datenbank
            conn = connect_to_database()
            cur = conn.cursor()

            # SQL-Abfrage für jeden Zug in der Liste train_list
            for train in train_list:
                try:
                    train_type = train.train_type + ' ' + train.train_off
                    cur.execute("INSERT INTO timetable (timetable_id, trainstation_id, date,name, arrival_time, departure_time, platform, train_number, train_type, destination) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                    (str(train.train_id), trainstationid, train.date, trainstation, train.arrival_time, train.departure_time, train.platform, train.train_number, train_type, train.stations))
                    conn.commit()
                except Exception as e:
                    pass

            # schließt die Verbindung zur Datenbank
            cur.close()
            conn.close()
            return True, 200
        except Exception as e:
             return str(e), 400

# Bekommt Daten (Verspätungen timetable) vom API Connector und verarbeitet diese und speichert sie in der Datenbank
class input_delay_data(Resource):
    trainstationid = 0

    def post(self):
        try:
            # Json Daten werden aus dem Request geholt
            json_data = request.get_json()

            # Überprüft ob die Json Daten leer sind
            if json_data is None:
                return "Invalid JSON data", 400

            # Überprüft ob die Json Daten die richtigen Keys haben
            timetable = Train_Timetable()
            train_list, trainstation = timetable.get_timetable_changes(json_data)

            # verbindet mit der Datenbank
            conn = connect_to_database()
            cur = conn.cursor()

            # SQL-Abfrage für jeden Zug in der Liste train_list
            for train in train_list:
                try:
                    cur.execute("""
                        INSERT INTO changestimetable (timetable_id_new, new_arrival_time, new_departure_time, new_platform)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (timetable_id_new) DO UPDATE
                        SET new_arrival_time = EXCLUDED.new_arrival_time,
                            new_departure_time = EXCLUDED.new_departure_time,
                            new_platform = EXCLUDED.new_platform
                    """, (str(train.time_id), train.arrival_time, train.departure_time, train.platform))
                    conn.commit()
                except Exception as e:
                    pass

            # schließt die Verbindung zur Datenbank
            cur.close()
            conn.close()
            return True, 200
        except Exception as e:
            return str(e), 400

# swagger documentation for the api endpoints
api.add_resource(Timetable, '/timetable/<string:trainstation>/<string:date>/<string:hour>')
api.add_resource(Timetable_Date, '/timetable/<string:trainstation>/<string:date>')
api.add_resource(train_number, '/destination/<string:train_number>')
api.add_resource(input_data, '/data')
api.add_resource(input_delay_data, '/delay_data')
api.add_resource(get_all, '/get_all')

# start the flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
