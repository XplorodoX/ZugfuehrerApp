# Author: Maximilian Müller

from flask import Flask, jsonify
from analysis import calculate_price_statistics, budget, preisanstiege, preisanstiege_alle, preistrend, preistrend_alle, basispreise
from plotting import plot_metrics, plot_preisanstiege, plot_preistrend_all
import base64, io 
import json
import logging
import sys
from flask_restx import Api, Resource

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout
)
logger = logging.getLogger()

app = Flask(__name__)

# Swagger Integration
api = Api(app, version='1.0', title='Web_Crawler_analysis API', description='Diese API ermöglicht es berechnete Preismetriken zu erhalten.')

class MetricsResource(Resource):
    @api.doc(params={'endbahnhof': 'Endbahnhof parameter'})
    @api.response(200, 'Success')
    def get(self, endbahnhof):
        """
        Get metrics for the specified endbahnhof.
        """
        # Metriken berechnen
        metrics = calculate_price_statistics(endbahnhof)

        # JSON-Formatierung der Metriken
        temp = metrics.to_json(orient='columns')

        # plot Funktion
        plot = plot_metrics(temp) 

        # Speichern des Diagrammbilds in einem Bytes-Puffer
        buffer1 = io.BytesIO()
        plot.savefig(buffer1, format='png')
        buffer1.seek(0)

        # Kodieren des Bilderpuffers als base64
        metrics_image = base64.b64encode(buffer1.getvalue()).decode('utf-8')
        buffer1.close()

        # Rückgabe des kodierten Bildes als Antwort
        return {'plot': metrics_image}

class BudgetResource(Resource):
    @api.doc(params={'b': 'Budget parameter', 'vonUhrzeit': 'VonUhrzeit parameter', 'bisUhrzeit': 'BisUhrzeit parameter', 'endbahnhof': 'Endbahnhof parameter'})
    @api.response(200, 'Success')
    def get(self, b, vonUhrzeit, bisUhrzeit, endbahnhof):

        # Budget berechnen
        budget_data = budget(b, vonUhrzeit, bisUhrzeit, endbahnhof)

        # JSON-Formatierung der Daten
        budget_json = json.loads(budget_data.to_json(orient='records'))[0]

        new_dict = {}
        # Dynamischer Ausgabe der gefundenen Reisen
        for key, value in budget_json.items():
            step, slot = key.split('_')

            time_string = ""

            if slot == "slot1":
                time_string = "zwischen 0 und 7 Uhr"
            elif slot == "slot2":
                time_string = "zwischen 7 und 10 Uhr"
            elif slot == "slot3":
                time_string = "zwischen 10 und 13 Uhr"
            elif slot == "slot4":
                time_string = "zwischen 13 und 16 Uhr"
            elif slot == "slot5":
                time_string = "zwischen 16 und 19 Uhr"
            elif slot == "slot6":
                time_string = "zwischen 19 und 24 Uhr"

            days_string = ""

            if step == "step1":
                days_string = "Reiseantritt Morgen"
            elif step == "step2":
                days_string = "Reiseantritt in einer Woche"
            elif step == "step3":
                days_string = "Reiseantritt in zwei Wochen"
            elif step == "step4":
                days_string = "Reiseantritt in drei Wochen"
            elif step == "step5":
                days_string = "Reiseantritt in vier Wochen"

            new_dict.update([(f"{days_string} {time_string}", value)])

        return new_dict

class PreisanstiegeResource(Resource):
    @api.doc(params={'endbahnhof': 'Endbahnhof parameter'})
    @api.response(200, 'Success')
    def get(self, endbahnhof):
        # Preisanstiege für einen bestimmten Endbahnhof berechnen
        preisanstiege_data = preisanstiege(endbahnhof)
        
        plot = plot_preisanstiege(preisanstiege_data)

        # Speichern des Diagrammbilds in einem Bytes-Puffer
        buffer2 = io.BytesIO()
        plot.savefig(buffer2, format='png')
        buffer2.seek(0)

        # Kodieren des Bilderpuffers als base64
        price_image = base64.b64encode(buffer2.getvalue()).decode('utf-8')
        buffer2.close()

        # Rückgabe des kodierten Bildes als Antwort
        return {'plot': price_image}

class PreisanstiegeAlleResource(Resource):
    @api.response(200, 'Success')
    def get(self):
        # Preisanstiege für alle Endbahnhöfe berechnen
        preisanstiege_data = preisanstiege_alle()

        plot = plot_preisanstiege(preisanstiege_data)

        # Speichern des Diagrammbilds in einem Bytes-Puffer
        buffer3 = io.BytesIO()
        plot.savefig(buffer3, format='png')
        buffer3.seek(0)

        # Kodieren des Bilderpuffers als base64
        price_all_image = base64.b64encode(buffer3.getvalue()).decode('utf-8')
        buffer3.close()

        # Rückgabe des kodierten Bildes als Antwort
        return {'plot': price_all_image}


class PreistrendResource(Resource):
    @api.doc(params={'endbahnhof': 'Endbahnhof parameter'})
    @api.response(200, 'Success')
    def get(self, endbahnhof):
        # Preistrend für einen bestimmten Endbahnhof berechnen
        preistrend_data = preistrend(endbahnhof)

        # JSON-Formatierung der Daten
        preistrend_json = preistrend_data.to_json(orient='columns')

        plot = plot_preistrend_all(preistrend_json, endbahnhof)

        # Speichern des Diagrammbilds in einem Bytes-Puffer
        buffer4 = io.BytesIO()
        
        plot.savefig(buffer4, format='png')
        buffer4.seek(0)

        # Kodieren des Bilderpuffers als base64
        trend_image = base64.b64encode(buffer4.getvalue()).decode('utf-8')
        buffer4.close()

        # Rückgabe des kodierten Bildes als Antwort
        return {'plot': trend_image}

class BasispreiseResource(Resource):
    @api.doc(params={'endbahnhof': 'Endbahnhof parameter'})
    @api.response(200, 'Success')
    def get(self, endbahnhof):
        # Basispreise für einen bestimmten Endbahnhof berechnen
        basispreise_data = basispreise(endbahnhof)

        # JSON-Formatierung der Daten
        basispreise_json = basispreise_data.to_json(orient='columns')

        # Rückgabe der JSON-Daten als Antwort
        return json.loads(basispreise_json)

   
class PreistrendAlleResource(Resource):
    @api.response(200, 'Success')
    def get(self):
        # Preistrend für alle Endbahnhöfe berechnen
        preistrend = preistrend_alle()

        # JSON-Formatierung der Daten
        preistrend_json = preistrend.to_json(orient='columns')

        plot = plot_preistrend_all(preistrend_json)

        # Speichern des Diagrammbilds in einem Bytes-Puffer
        buffer5 = io.BytesIO()
        plot.savefig(buffer5, format='png')
        buffer5.seek(0)

        # Kodieren des Bilderpuffers als base64
        trend_all_image = base64.b64encode(buffer5.getvalue()).decode('utf-8')
        buffer5.close()
        # Rückgabe des kodierten Bildes als Antwort
        return {'plot': trend_all_image}

api.add_resource(MetricsResource, '/metrics/<endbahnhof>')
api.add_resource(BudgetResource, '/budget/<float:b>/<int:vonUhrzeit>/<int:bisUhrzeit>/<endbahnhof>')
api.add_resource(PreisanstiegeResource, '/preisanstiege/<endbahnhof>')
api.add_resource(PreisanstiegeAlleResource, '/preisanstiege_alle')
api.add_resource(PreistrendResource, '/preistrend/<endbahnhof>')
api.add_resource(BasispreiseResource, '/basispreise/<endbahnhof>')
api.add_resource(PreistrendAlleResource, '/preistrend_alle')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011)
