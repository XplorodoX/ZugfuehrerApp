# AUTHOR: Marius Mühleck

from flask import Flask, request
from flask_restx import Api, Resource, fields
from datetime import datetime as dt
import requests
import logging
import sys


app = Flask(__name__)
stored_data = {}

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout
)
logger = logging.getLogger()

# Swagger Integration
api = Api(app, version='1.0', title='Backend APIs', description='API endpoints that provide interface react with the necessary information from the other container.')

@api.route('/delays_submit', methods=['POST'])
class DelaysSubmitResource(Resource):
    @api.doc(description='This endpoint accepts json formatted delay data and processes it.')
    @api.response(200, description='Success')
    @api.expect(
        api.model('Delay',{
            'line_id': fields.String(required=False, description='Line ID of the train'),
            'datetime': fields.DateTime(required=False, description='Date and time of the delay'),
        }))
    def post(self):
        data = request.get_json()

        line_id = data.get('line_id')
        datetime = data.get('datetime')

        # if line_id was provided search for the specific line
        if line_id:
            # try to fetch data from endpoint
            try:
                logger.info(f'http://192.168.0.4:5005/avg_delay_at/n/{line_id}')
                # Send a GET request to the server
                response = requests.get(f'http://192.168.0.4:5005/avg_delay_at/n/{line_id}')

                # Check response status code
                if response.status_code == 200:
                    logger.info("Got data from Data Analyzer")
                    data = response.json()
                    logger.info(data)

                    return data

                else:
                    logger.error("Failed to get data from Data Controller")
                    return {
                        "message": f'Failed to connect with status_code {response.status_code}'
                    }

            except Exception as e:
                logger.critical(f'Exception: {e}')
                return {
                        "message": f'Exception: {e}'
                    }
        # if no line_id was given, search general
        else:
            try:
                logger.info(f'http://192.168.0.4:5005/avg_delay_at')
                # Send a GET request to the server
                response = requests.get(f'http://192.168.0.4:5005/avg_delay_at')

                # Check response status code
                if response.status_code == 200:
                    logger.info("Got data from Data Analyzer")
                    data = response.json()
                    logger.info(data)

                    return data

                else:
                    logger.error("Failed to get data from Data Controller")
                    return {
                        "message": f'Failed to connect with status_code {response.status_code}'
                    }

            except Exception as e:
                logger.critical(f'Exception: {e}')
                return {
                        "message": f'Exception: {e}'
                }

@api.route('/delays_submit_specific_line', methods=['POST'])
class DelaysSubmitSpecificLineResource(Resource):
    @api.doc(description='This endpoint accepts line_id and returns the average delay for the specific line.')
    @api.response(200, description='Success')
    @api.expect(
        api.model('SpecificLine', {
            'line_id': fields.String(required=True, description='Line ID of a specific train'),
        }), validate=True) 
    def post(self):
        data = request.get_json()

        line_id = data.get('line_id')
        try:
            logger.info(f'http://192.168.0.4:5005/average_delay_at/{line_id}')
            # Send a GET request to the server
            response = requests.get(f'http://192.168.0.4:5005/average_delay_at/{line_id}')

            # Check response status code
            if response.status_code == 200:
                logger.info("Got data from Data Analyzer")
                data = response.json()
                logger.info(data)

                return data

            else:
                logger.error("Failed to get data from Data Controller")
                return {
                    "message": f'Failed to connect with status_code {response.status_code}'
                }

        except Exception as e:
            logger.critical(f'Exception: {e}')
            return {
                    "message": f'Exception: {e}'
                }

@api.route('/timetable_submit', methods=['POST'])
class TimetableFormProcessingResource(Resource):
    @api.doc(description='This endpoint accepts start, destination stations, and datetime and returns the appropriate connections with detailed stops along the route.')
    @api.response(200, description='Success')
    @api.expect(
        api.model('TimetableData', {
            'start_station': fields.String(required=True, description='Start station of the journey'),
            'destination_station': fields.String(required=False, description='Destination station of the journey'),
            'datetime': fields.DateTime(required=True, description='Date and time of the journey'),
        }), validate=True)
    def post(self):
        data = request.get_json()

        start_station = data.get('start_station')
        destination_station = data.get('destination_station')
        datetime = data.get('datetime')

        departure_start = None
        arrival_destination = None
        train_numbers = []

        train_stations = {
            'Aalen Hbf': 8000002,
            'Schwäbisch Gmünd': 8000329,
            'Heidenheim': 8002689,
            'Langenau(Württ)': 8003525,
            'Ulm Hbf': 8000170,
            'Schorndorf': 8005424,
            'Stuttgart Hbf': 8000096,
            'Nürnberg Hbf': 8000284,
            'Ellwangen': 8001751,
            'Donauwörth': 784839,
            'Waiblingen': 8000180,
            'Crailsheim': 8000067,
            'Karlsruhe Hbf': 8000191,
            'Pforzheim Hbf': 8000299,
            'Nördlingen': 8000280,
            'Oberkochen': 8004549,
            'München Hbf': 8000261,
            'Augsburg Hbf': 8000013,
        }
        # retrieve trainstation_id with given string
        trainstation_id = train_stations.get(start_station)

        if not trainstation_id:
            logger.error("No matching station found")
            return {
                "message": f'Failed to get station_id for {start_station}'
            } 

        date = datetime.split("T")[0]

        hour = datetime.split("T")[1].split(":")[0]

        try:
            logger.info(f'http://192.168.0.6:5001/timetable/{trainstation_id}/{date}/{hour}')
            # Send a GET request to the server
            response = requests.get(f'http://192.168.0.6:5001/timetable/{trainstation_id}/{date}/{hour}')

            # Check response status code
            if response.status_code == 200:
                logger.info("Got data from Data Controller")
                data = response.json()
                # logger.debug(data)

                # turn the destinations into a proper list
                for connection in data:
                    destinations = connection.get('planned').get('ppth').split('|')
                    connection['planned']['ppth'] = destinations

                # check if there is a destination set, if yes only return connections stopping at the desired destination
                connections_with_destination = []
                if len(destination_station) > 0:
                    for connection in data:
                        # just take the connections with the wanted destination_station in the path
                        if destination_station in connection.get('planned').get('ppth'):
                            # logger.info(f'possible connection:\n{connection}')
                            if connection.get('planned').get('dp_time'):
                                logger.info(f'Found possible connection to {destination_station}')
                                # logger.debug(connection)
                                train_number = connection.get('@n')
                                stations = []
                                done_station_ids = []

                                # prevent having duplicate trains inside
                                if train_number in train_numbers:
                                    continue

                                try:
                                    logger.info(f'http://192.168.0.6:5001/destination/{train_number}')
                                    # Send a GET request to the server
                                    response = requests.get(f'http://192.168.0.6:5001/destination/{train_number}')

                                    # Check response status code
                                    if response.status_code == 200:
                                        logger.info(f"Got destinations for {train_number} from Data Controller")
                                        destination_data = response.json()
                                        logger.debug(f'Destination data:\n{destination_data}')

                                        # These are used to check if the destination comes before the start station (trains that travel in the opposite direction)
                                        found_start = False
                                        found_destination = False
                                        wrong_direction = False

                                        for station in destination_data:
                                            # remove duplicate trains
                                            if station.get('train_number') in done_station_ids:
                                                continue
                                            # checks if destination comes before the start (trains going in opposite direction) and filters them out
                                            if station.get('destination').lower() == start_station.lower():
                                                found_start = True
                                            if station.get('destination').lower() == destination_station.lower():
                                                found_destination = True
                                            if not found_start and found_destination:
                                                wrong_direction = True
                                                break
                                            # set several fields for the connection, like arrival_time, departure_time (if delayed write delay time in brackets behind planned time)
                                            arrival_time = station.get('arrival_time')
                                            departure_time = station.get('departure_time')
                                            if station.get('arrival_time') and station.get('deleay_arrival_time'):
                                                if station.get('arrival_time') != station.get('deleay_arrival_time'):
                                                    arrival_time = f"{station.get('arrival_time')} ({station.get('deleay_arrival_time')})"
                                            if station.get('departure_time') and station.get('deleay_departure_time'):
                                                if station.get('departure_time') != station.get('deleay_departure_time'):
                                                    departure_time = f"{station.get('departure_time')} ({station.get('deleay_departure_time')})"

                                            if station.get('destination').lower() == start_station.lower():
                                                departure_start = station.get('departure_time')

                                            if station.get('destination').lower() == destination_station.lower():
                                                arrival_destination = station.get('arrival_time')

                                            if not arrival_time:
                                                arrival_time = station.get('departure_time') + ' (+0)'
                                            else:
                                                arrival_time += ' (+0)'
                                            if not departure_time:
                                                departure_time = station.get('arrival_time') + ' (+0)'
                                            else:
                                                departure_time += ' (+0)'
                                            # create dictionary with created values
                                            dic = {
                                                'station_id': station.get('train_number'),
                                                'destination': station.get('destination'),
                                                'arrival_time': arrival_time,
                                                'departure_time': departure_time,
                                            }
                                            # append all in the lists
                                            stations.append(dic)
                                            done_station_ids.append(station.get('train_number'))

                                        if wrong_direction:
                                            logger.info(f'Wrong direction for train {train_number}')
                                            continue

                                except Exception as e:
                                    logger.critical(f'Exception: {e}')
                                    return {
                                            "message": f'Exception: {e}'
                                        }
                                # calculate driving duration if possible
                                if departure_start and arrival_destination:
                                    # Convert the time strings to datetime.time objects
                                    time1 = dt.strptime(departure_start, "%H:%M:%S").time()
                                    time2 = dt.strptime(arrival_destination, "%H:%M:%S").time()

                                    # Combine the time objects with a dummy date to allow timedelta calculation
                                    dummy_date = dt(1900, 1, 1)
                                    dt1 = dt.combine(dummy_date, time1)
                                    dt2 = dt.combine(dummy_date, time2)

                                    # Calculate the time difference
                                    time_difference = dt2 - dt1

                                    # Extract hours and minutes from the time difference
                                    hours, remainder = divmod(time_difference.seconds, 3600)
                                    minutes, _ = divmod(remainder, 60)
                                    duration = f'{hours}:{minutes:2}'
                                else:
                                    duration = None
                                
                                # update the connection with the new values
                                connection.update([('stations', stations)])
                                connection.update([('departure_start', departure_start[:5] if departure_start else None)])
                                connection.update([('arrival_destination', arrival_destination[:5] if arrival_destination else None)])
                                connection.update([('duration', duration)])
                                connection.update([('train_type', connection.get('@train_type'))])
                                connection.update([('plattform', connection.get('planned').get('pl'))])

                                logger.debug(f'Updated connection: {connection}')
                                # append the train to the lists
                                connections_with_destination.append(connection)
                                train_numbers.append(train_number)
                
                    resp = {
                            "connections": connections_with_destination if connections_with_destination else None,
                            "start": start_station if start_station else None,
                            "destination": destination_station if destination_station else None,
                        }
                    
                else:
                    resp = {
                        "connections": data if data else None,
                        "start": start_station if start_station else None,
                    }

                #logger.debug(resp)
                return resp

            else:
                logger.error("Failed to get data from Data Controller")
                return {
                    "message": f'Failed to connect with status_code {response.status_code}'
                }

        except Exception as e:
            logger.critical(f'Exception: {e}')
            return {
                    "message": f'Exception: {e}'
                }

@api.route('/prices_submit', methods=['POST'])
class PricesSubmitResource(Resource):
    @api.doc(description='This endpoint accepts start station and destination station, and returns price plots from the Web Crawler.')
    @api.response(200, description='Success')
    @api.expect(
        api.model('Prices', {
            'start_station': fields.String(required=True, description='Start station for the journey'), 
            'destination_station': fields.String(required=True, description='Destination station for the journey')
        }), validate=True)
    
    def post(self):
        data = request.get_json()

        start_station = data.get('start_station')
        destination_station = data.get('destination_station')

        body = {
            'startbahnhof': start_station,
            'endbahnhof': destination_station
        }

        try:
            # Send a GET request to the server
            response = requests.post('http://192.168.0.9:5002/plot', json=body)

            # Check response status code
            if response.status_code == 200:
                logger.info("Got data from Web Crawler")
                data = response.json()
                logger.info(data)

                return data

            else:
                logger.error("Failed to get data from Web Crawler")
                return {
                    "message": f'Failed to connect with status_code {response.status_code}'
                }

        except Exception as e:
            logger.critical(f'Exception: {e}')
            return {
                    "message": f'Exception: {e}'
                }

@api.route('/price_wish', methods=['POST'])
class PriceWishResource(Resource):
    @api.doc(description='This endpoint accepts budget, time slots and destination, and returns travel options fitting the constraints, as analyzed by the Web Crawler.')
    @api.response(200, description='Success')
    @api.expect(
        api.model('PriceWish', {
            'budget': fields.Float(required=True, description='Budget for the journey'),
            'time_slot_start': fields.String(required=True, description='Start of the desired time slot for travel'),
            'time_slot_end': fields.String(required=True, description='End of the desired time slot for travel'),
            'destination': fields.String(required=True, description='Destination station for the journey')
        }), validate=True)
    def post(self):
    
        data = request.get_json()

        budget = float(data.get('budget'))
        time_slot_start = data.get('time_slot_start')
        time_slot_end = data.get('time_slot_end')
        destination = data.get('destination')


        try:
            # Send a GET request to the server
            response = requests.get(f'http://192.168.0.13:5011/budget/{budget}/{time_slot_start}/{time_slot_end}/{destination}')

            # Check response status code
            if response.status_code == 200:
                logger.info("Got price wish from Web Crawler Analysis")
                data = response.json()
                logger.debug(data)



                return data

            else:
                logger.error("Failed to get data from Web Crawler")
                return {
                    "message": f'Failed to connect with status_code {response.status_code}'
                }

        except Exception as e:
            logger.critical(f'Exception: {e}')
            return {
                    "message": f'Exception: {e}'
                }

@api.route('/metrics', methods=['POST'])
class MetricsResource(Resource):
    @api.doc(description='This endpoint accepts destination name and returns the metrics related to it')
    @api.response(200, description='Success')
    @api.expect(
        api.model('Metrics', {
            'metrics_destination': fields.String(required=True, description='Destination name'),
        }), validate=True)
    def post(self):
    
        data = request.get_json()

        metrics_destination = data.get('metrics_destination')


        try:
            # Send a GET request to the server
            response = requests.get(f'http://192.168.0.13:5011/metrics/{metrics_destination}')

            # Check response status code
            if response.status_code == 200:
                logger.info("Got destination metrics from Web Crawler Analysis")
                data = response.json()
                logger.debug(data)

                return data

            else:
                logger.error("Failed to get data from Web Crawler")
                return {
                    "message": f'Failed to connect with status_code {response.status_code}'
                }

        except Exception as e:
            logger.critical(f'Exception: {e}')
            return {
                    "message": f'Exception: {e}'
                }

@api.route('/trends', methods=['POST'])
class TrendsResource(Resource):
    @api.doc(description='This endpoint accepts destination name and retrieves its corresponding trends')
    @api.response(200, description='Success')
    @api.expect(
        api.model('Trends', {
            'metrics_destination': fields.String(required=True, description='Destination name'),
        }), validate=True)
    def post(self):
    
        data = request.get_json()

        metrics_destination = data.get('metrics_destination')


        try:
            # Send a GET request to the server
            response = requests.get(f'http://192.168.0.13:5011/preistrend/{metrics_destination}')

            # Check response status code
            if response.status_code == 200:
                logger.info("Got destination trends from Web Crawler Analysis")
                data = response.json()
                logger.debug(data)

                return data

            else:
                logger.error("Failed to get data from Web Crawler")
                return {
                    "message": f'Failed to connect with status_code {response.status_code}'
                }

        except Exception as e:
            logger.critical(f'Exception: {e}')
            return {
                    "message": f'Exception: {e}'
                }

@api.route('/increases', methods=['POST'])
class IncreasesResource(Resource):
    @api.doc(description='This endpoint accepts destination name and retrieves its corresponding increases')
    @api.response(200, description='Success')
    @api.expect(
        api.model('Increases', {
            'metrics_destination': fields.String(required=True, description='Destination name'),
        }), validate=True)
    def post(self):
    
        data = request.get_json()

        metrics_destination = data.get('metrics_destination')


        try:
            # Send a GET request to the server
            response = requests.get(f'http://192.168.0.13:5011/preisanstiege/{metrics_destination}')

            # Check response status code
            if response.status_code == 200:
                logger.info("Got destination increases from Web Crawler Analysis")
                data = response.json()
                logger.debug(data)

                return data

            else:
                logger.error("Failed to get data from Web Crawler")
                return {
                    "message": f'Failed to connect with status_code {response.status_code}'
                }

        except Exception as e:
            logger.critical(f'Exception: {e}')
            return {
                    "message": f'Exception: {e}'
                }

@api.route('/price_trend_all', methods=['GET'])
class PriceTrendsResource(Resource):
    @api.doc(description='This endpoint retrieves all price trends')
    @api.response(200, description='Success')
    def get(self):

        try:
            # Send a GET request to the server
            response = requests.get('http://192.168.0.13:5011/preistrend_alle')

            # Check response status code
            if response.status_code == 200:
                logger.info("Got price trends from Web Crawler Analysis")
                data = response.json()
                # logger.debug(data)

                return data

            else:
                logger.error("Failed to get data from Web Crawler")
                return {
                    "message": f'Failed to connect with status_code {response.status_code}'
                }

        except Exception as e:
            logger.critical(f'Exception: {e}')
            return {
                    "message": f'Exception: {e}'
                }
    
@api.route('/price_increase_all', methods=['GET'])
class PriceIncreasesResource(Resource):
    @api.doc(description='This endpoint retrieves all price increases')
    @api.response(200, 'Success')
    def get(self):

        try:
            # Send a GET request to the server
            response = requests.get('http://192.168.0.13:5011/preisanstiege_alle')

            # Check response status code
            if response.status_code == 200:
                logger.info("Got price increases from Web Crawler Analysis")
                data = response.json()
                # logger.debug(data)

                return data

            else:
                logger.error("Failed to get data from Web Crawler")
                return {
                    "message": f'Failed to connect with status_code {response.status_code}'
                }

        except Exception as e:
            logger.critical(f'Exception: {e}')
            return {
                    "message": f'Exception: {e}'
                }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
