# Author: Maximilian Müller

from flask import Flask, request
import base64, io 
from app import crawler, toPicture
from flask_restx import Api, Resource


app = Flask(__name__)
api = Api(app, version='1.0', title='Cralwer plotted', description='Diese API bietet die Möglichkeit daten aus einem dynamisch angestoßenen Crawl-Vorgang zu erhalten.')

# Webcrawler
class PlotResource(Resource):
    def post(self):
        # JSON-Daten vom Frontend abrufen
        data = request.get_json()
        startbahnhof = data.get('startbahnhof', 'Variable nicht übergeben')
        endbahnhof = data.get('endbahnhof', 'Variable nicht übergeben')

        # Aufruf der crawler-Funktion, um die Daten zu sammeln
        dictAalenBerlin = crawler(startbahnhof, endbahnhof, 7, 5)

        # Aufruf der toPicture-Funktion, um das Diagramm zu generieren
        plt = toPicture(dictAalenBerlin)

        # Speichern des Diagrammbilds in einem Bytes-Puffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # Kodieren des Bilderpuffers als base64
        encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Rückgabe des kodierten Bildes als Antwort
        return {'plot': encoded_image}

api.add_resource(PlotResource, '/plot')

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5002)