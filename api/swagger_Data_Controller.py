# Autor: Florian Merlau
# Beschreibung:
# Dies soll dazu dienen die Data Controller API zu dokumentieren

# Importieren der benötigten Module
from datetime import datetime, timedelta
import psycopg2
from flask import Flask, request
from flask_restx import Namespace, Api, Resource, fields
from src.Data_Controller.timetable_train import Train_Timetable

# Erstellen einer Flask-App und eines Flask-RESTX-APIs
app = Flask(__name__)
api = Api(app)

# Creating the Namespace
ns = Namespace('timetable', description='Timetable operations')

# Define model for API documentation
# This is a generic model, please adapt it to fit your actual data model
timetable_model = ns.model('Timetable', {
    's_id': fields.String(required=True, description='ID of the trainstation'),
    'station': fields.String(required=True, description='Name of the trainstation'),
    'train_type': fields.String(required=True, description='Type of the train'),
    'date': fields.String(required=True, description='Date of the timetable'),
    'n': fields.String(required=True, description='Train number'),
    'planned': fields.Nested(ns.model('Planned', {
        'ar_time': fields.String(description='Planned arrival time'),
        'dp_time': fields.String(description='Planned departure time'),
        'pl': fields.String(description='Planned platform'),
        'ppth': fields.String(description='Destination'),
    })),
    'changend': fields.Nested(ns.model('Changend', {
        'n_ar_time': fields.String(description='Changed arrival time'),
        'n_dp_time': fields.String(description='Changed departure time'),
        'n_pl': fields.String(description='Changed platform'),
    })),
})

train_number_model = ns.model('TrainNumber', {
    'train_number': fields.String(description='Train number'),
    'destination': fields.String(description='Destination'),
    'arrival_time': fields.String(description='Planned arrival time'),
    'train_type': fields.String(description='Type of the train'),
    'departure_time': fields.String(description='Planned departure time'),
    'delay_arrival_time': fields.String(description='Changed arrival time'),
    'delay_departure_time': fields.String(description='Changed departure time'),
})

# Verbinde mit der Datenbank
def connect_to_database():
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="example"
    )
    return conn

# Find the trainstation id in the CSV file
def find_trainstation_id(trainstation):
    with open('../src/Data_Controller/D_Bahnhof_2020_alle.CSV') as file:
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

@ns.route('/get_all')
class get_all(Resource):
    @ns.doc('get_all')
    @ns.doc(description='Get all train timetables')
    @ns.marshal_list_with(timetable_model)
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
@ns.route('/destination/<string:train_number>')
@ns.response(404, 'Entry not found')
@ns.response(500, 'Internal server error')
class train_number(Resource):
    @ns.doc('get_train_number')
    @api.doc(description='get information about a train by train number')
    @ns.marshal_list_with(train_number_model)
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
@ns.route('/timetable/<string:trainstation>/<string:date>/<string:hour>')
@ns.response(404, 'Entry not found')
@ns.response(500, 'Internal server error')
class Timetable(Resource):
    @ns.doc('get_timetable')
    @ns.doc(description='Get train timetables for a specific train station, date and hour')
    @ns.marshal_list_with(timetable_model)
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
@ns.route('/timetable/<string:trainstation>/<string:date>')
class Timetable_Date(Resource):
    @ns.doc(description='Get train timetables for a specific train station and date')
    @ns.marshal_list_with(timetable_model)
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
@ns.route('/data')
@ns.response(500, 'Internal server error')
class input_data(Resource):
    @ns.doc('post_input_data')
    @ns.doc(description='Post input data timetable to the database')
    @ns.expect(ns.model('InputDataPayload', {
        'timetable': fields.Nested(ns.model('TimetableData', {
            '@station': fields.String(required=True, description='Name of the trainstation'),
            's': fields.List(fields.Nested(ns.model('ScheduleData', {
                '@id': fields.String(required=True, description='ID of the schedule'),
                'tl': fields.Nested(ns.model('TrainData', {
                    '@t': fields.String(required=True, description='Train type'),
                    '@o': fields.String(required=True, description='Train origin'),
                    '@c': fields.String(required=True, description='Train category'),
                    '@n': fields.String(required=True, description='Train number'),
                }), required=True, description='Train details'),
                'ar': fields.Nested(ns.model('ArrivalData', {
                    '@pt': fields.String(required=True, description='Planned arrival time'),
                    '@pp': fields.String(required=True, description='Planned arrival platform'),
                    '@l': fields.String(required=True, description='Arrival platform track'),
                    '@ppth': fields.String(required=True, description='Arrival platform path'),
                }), required=True, description='Arrival details'),
                'dp': fields.Nested(ns.model('DepartureData', {
                    '@pt': fields.String(required=True, description='Planned departure time'),
                    '@pp': fields.String(required=True, description='Planned departure platform'),
                    '@l': fields.String(required=True, description='Departure platform track'),
                    '@ppth': fields.String(required=True, description='Departure platform path'),
                }), required=True, description='Departure details'),
            })), required=True, description='List of schedule data')
        }), required=True, description='Timetable data')
    }))
    def post(self):
        trainstationid = 0
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
@ns.route('/delay_data')
@ns.response(500, 'Internal server error')
class input_delay_data(Resource):
    @ns.doc('post_input_delay_data')
    @ns.doc(description='Post input delay data timetable to the database')
    @ns.expect(ns.model('InputDelayDataPayload', {
        'timetable': fields.List(fields.Raw, required=True, description='List of timetable changes')
    }))

    def post(self):
        trainstationid = 0
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

# add Namespace to API
api.add_namespace(ns)

# start the flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
