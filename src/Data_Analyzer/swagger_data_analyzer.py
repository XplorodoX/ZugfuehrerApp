# Author: Marc Nebel
# Beschreibung: Flask Server mit Swagger Integration. Funktioniert leider nicht mit dem Frontend. Daten können aber als Json über den Browser
# aufgerufen werden und entsprechend mit Swagger getestest werden. Kommentare sind deckungsgleich zu ursprünglichem Flask Server.

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource

from manual import manual
import db_connect

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

description = 'This is the API documentation for the data analytics REST service. '

api = Api(app, version='1.0', title='Data Analytics Service API Docs', description='API Documentation')


@api.route('/')
class Manual(Resource):
    @api.doc(description='Get the manual with all table and field names')
    def get(self):
        return jsonify(manual)


@api.route('/<table_name>/')
@api.doc(params={'table_name': 'The name of the table'})
class GetData(Resource):
    @api.doc(description='Get all data from a table')
    def get(self, table_name):
        try:
            data = db_connect.get_table(table_name)
            data = data.to_json(orient='records')
            return data
        except Exception:
            raise Exception("Error: Table does not exist")


@api.route('/<table_name>/<param1>/<value1>')
@api.doc(params={'table_name': 'The name of the table', 'param1': 'Description of param1', 'value1': 'Value for param1'})
class GetDataWithParam1(Resource):
    @api.doc(description='Get data from a table with a specific value for a column')
    def get(self, table_name, param1, value1):
        try:
            data = db_connect.get_table_specific(table_name, param1, value1)
            data = data.to_json(orient='records')
            return data
        except Exception:
            raise Exception("Either wrong table or param name")


@api.route('/<table_name>/<param1>/<value1>/<param2>/<value2>')
@api.doc(params={'table_name': 'The name of the table', 'param1': 'Description of param1', 'value1': 'Value for param1',
                 'param2': 'Description of param2', 'value2': 'Value for param2'})
class GetDataWithParam2(Resource):
    @api.doc(description='Get data from a table with two specific values for two different columns')
    def get(self, table_name, param1, value1, param2, value2):
        try:
            data = db_connect.get_table_specific2(table_name, param1, value1, param2, value2)
            data = data.to_json(orient='records')
            return data
        except Exception:
            raise Exception("Either wrong table or param name")


@api.route('/<table_name>/<param1>/<value1>/<param2>/<value2>/<param3>/<value3>')
@api.doc(params={'table_name': 'The name of the table', 'param1': 'Description of param1', 'value1': 'Value for param1',
                 'param2': 'Description of param2', 'value2': 'Value for param2',
                 'param3': 'Description of param3', 'value3': 'Value for param3'})
class GetDataWithParam3(Resource):
    @api.doc(description='Get data from a table with three specific values for three different columns')
    def get(self, table_name, param1, value1, param2, value2, param3, value3):
        try:
            data = db_connect.get_table_specific3(table_name, param1, value1, param2, value2, param3, value3)
            data = data.to_json(orient='records')
            return data
        except Exception:
            raise Exception("Either wrong table or param name")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
