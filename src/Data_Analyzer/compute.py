# Author: Marc Nebel
# Beschreibung: Hauptmodul welches alle Funktionen für die Berechnungen der verschiedenen Verspätungsdaten enthält.

import pandas as pd
import db_connect
from datetime import datetime, timedelta
import warnings

# Verstecken einer spezifischen Pandas Warnung, welche beim Parsen von None Datums Werten erzeugt wird. (Für das Reinhalten des Docker Log)
warnings.filterwarnings("ignore", message=".*Could not infer format, so each element will be parsed individually.*")

# Funktion für das Abflachen und Parsen eines JSON Objekts in einen Pandas Dataframe 
def to_pandas(data):
    flattened_data = []
    for item in data:
        flattened_item = {}
        for idx, value in item.items():
            if isinstance(value, dict):
                for i, s in value.items():
                    flattened_item[i] = s
            else:
                flattened_item[idx] = value
        flattened_data.append(flattened_item)

    data = pd.DataFrame(flattened_data)
    return data

# Funktion für das Gruppieren von Werten des Input DF. Die Verspätungen werden dabei als Durchschnitt aller vorhandenen Verspätungen gespeichert.
# Letztendliche Kovertierung in einen Minuten Time Delta Wert
def average_delay(data):
    data['ar_time_diff'] = pd.to_timedelta(data['ar_time_diff'])
    data['dp_time_diff'] = pd.to_timedelta(data['dp_time_diff'])

    data = data.groupby(['n', 'station', 'destination']).agg({'ar_time_diff': 'mean', 'dp_time_diff': 'mean'})
    data.reset_index(inplace=True)

    data['ar_time_diff'] = pd.to_timedelta(data['ar_time_diff'])/pd.Timedelta('60s')
    data['dp_time_diff'] = pd.to_timedelta(data['dp_time_diff'])/pd.Timedelta('60s')

    return data

# Funktion für das Gruppieren von Werten des Input DF, welche ein Start- oder ein Zielbahnhof sind. 
# Die Verspätungen werden dabei als Durchschnitt aller vorhandenen Verspätungen bei Start- oder Zielbahnhöfen gespeichert. 
# Dannach werden die Werte in ein Minuten Time Delta konvertiert.
def average_delay_final(data):
    data['ar_time_diff'] = pd.to_timedelta(data['ar_time_diff'])
    data['dp_time_diff'] = pd.to_timedelta(data['dp_time_diff'])

    data1 = data[data['first_station']]
    data2 = data[data['final_station']]

    data1 = data1.groupby(['n', 'destination']).agg({'dp_time_diff': 'mean'})
    data2 = data2.groupby('n').agg({'ar_time_diff': 'mean'})
    
    data1.reset_index(inplace=True)
    data2.reset_index(inplace=True)

    data = pd.merge(data1, data2, on=['n'])

    data['ar_time_diff'] = pd.to_timedelta(data['ar_time_diff'])/pd.Timedelta('60s')
    data['dp_time_diff'] = pd.to_timedelta(data['dp_time_diff'])/pd.Timedelta('60s')

    return data

# Funktion für das Berechnen der durchschnitlichen Verspätungen über alle vorhandenen Verspätungsdaten. Jeweilige Berechung der Verspätungen
# pro Zuglinie sowie Start und Zielbahnhof einer Zuglinie. Zusätzlich werden die Zuglinienverspätungen in eine seperate Tabelle mit Berechungs-
# zeitpunkten gespeichert um einen Trend der Änderungen zu speichern
def average_delay_all_time():
    data = db_connect.get_table('delay')
    
    data_final = average_delay_final(data)
    data = average_delay(data)
    #Is needed as destination can vary but n stays the same
    data = data.drop_duplicates(subset=['n', 'station'])

    db_connect.store_data("avg_delay_at_final", data_final[['n', 'ar_time_diff', 'dp_time_diff']])

    db_connect.store_data("avg_delay_at", data[['n', 'station', 'ar_time_diff', 'dp_time_diff']])
    
    data.insert(0, 'c_date', pd.Timestamp.today().date())
    
    db_connect.store_data("avg_delay_at_over_time", data[['n', 'c_date', 'station', 'ar_time_diff', 'dp_time_diff']])

    return 0

# Funktion für das Berechnen eines Durschnitsverspätungswert über eine gegebene Zeitspanne mit einem entsprechden Startdatum. Inkludiert 
# Verspätungen per Zuglinie sowie Start und Zielbahnhof einer Zuglinie.
def average_delay_specific_time(date, timespan):
    data = db_connect.get_table('delay')

    new_date = date - timespan

    data['date'] = pd.to_datetime(data['date'])

    data = data[data['date'] > new_date]

    data_final = average_delay_final(data)
    data = average_delay(data)
    
    return data, data_final

    
# Funktion für die Berechnung von Durschnitsverspätungswerten über eine Woche. Gespeichert werden Verspätungen per Zuglinie sowie Start und
# Zielbahnhof einer Zuglinie. Duplikate werden entfernt falls die Bahn das Ziel einer Bahnverbindung ändert was wiederum zu Duplikaten in den
# Daten führen kann.
def average_delay_weekly(date):
    date = pd.to_datetime(date)
    data, data_final = average_delay_specific_time(date, timedelta(days=7))

    data.insert(0, 'date', date)
    data_final.insert(0, 'date', date)

    db_connect.store_data("avg_delay_st_weekly_final", data_final[['n', 'date', 'ar_time_diff', 'dp_time_diff']])

    data = data.drop_duplicates(subset=['n', 'station'])
    db_connect.store_data("avg_delay_st_weekly", data[['n', 'date', 'station', 'ar_time_diff', 'dp_time_diff']])

    return 0

# Funktion für die Berechnung von Durschnitsverspätungswerten über einen Monat. Gespeichert werden Verspätungen per Zuglinie sowie Start und
# Zielbahnhof einer Zuglinie. Duplikate werden entfernt falls die Bahn das Ziel einer Bahnverbindung ändert was wiederum zu Duplikaten in den
# Daten führen kann.
def average_delay_monthly(date):
    date = pd.to_datetime(date)
    data, data_final = average_delay_specific_time(date, timedelta(days=31))

    data.insert(0, 'date', date)
    data_final.insert(0, 'date', date)

    db_connect.store_data("avg_delay_st_monthly_final", data_final[['n', 'date', 'ar_time_diff', 'dp_time_diff']])

    data = data.drop_duplicates(subset=['n', 'station'])
    db_connect.store_data("avg_delay_st_monthly", data[['n', 'date', 'station', 'ar_time_diff', 'dp_time_diff']])

    return 0

# Funktion für die Berechnung von Durschnitsverspätungswerten über einen Tag. Gespeichert werden Verspätungen per Zuglinie sowie Start und
# Zielbahnhof einer Zuglinie. Duplikate werden entfernt falls die Bahn das Ziel einer Bahnverbindung ändert was wiederum zu Duplikaten in den
# Daten führen kann. Funktion ist derzeit Redundant da Bahnverbindungen einzigartig per Tag sind. Sollte sich dies ändern wird diese Funktion 
# relevant.
def average_delay_daily(date):
    date = pd.to_datetime(date)
    data, data_final = average_delay_specific_time(date, timedelta(days=1))

    data.insert(0, 'date', date)
    data_final.insert(0, 'date', date)

    db_connect.store_data("avg_delay_st_daily_final", data_final[['n', 'date', 'ar_time_diff', 'dp_time_diff']])

    data = data.drop_duplicates(subset=['n', 'station'])
    db_connect.store_data("avg_delay_st_daily", data[['n', 'date', 'station', 'ar_time_diff', 'dp_time_diff']])

    return 0

# Funktion für das Erzeugen von Durchschnittsverspätungen einer Bahnlinie (z.B. Aalen nach Ulm). Gespeichert werden die Verspätungen der Bahnlinie
# sowie die finalen Verspätungen beim ersten sowie letzten Bahnhof der Bahnlinie. Parallel werden die Werte seperat mit jeweiligem Berechnungsdatum
# in eine seperate Tabelle gespeichert um einen Trend der Änderungen der Verspätungen zu speichern.
def average_delay_destination():
    data = db_connect.get_table('delay')

    data_final = average_delay_final(data)
    data = average_delay(data)
    
    data_final = data_final.groupby('destination').agg({'ar_time_diff': 'mean', 'dp_time_diff': 'mean'})
    data_final.reset_index(inplace=True)
    data = data.groupby(['destination', 'station']).agg({'ar_time_diff': 'mean', 'dp_time_diff': 'mean'})
    data.reset_index(inplace=True)

    db_connect.store_data("avg_delay_destination_final", data_final[['destination', 'ar_time_diff', 'dp_time_diff']])
    db_connect.store_data("avg_delay_destination", data[['destination', 'station', 'ar_time_diff', 'dp_time_diff']])

    data_final.insert(0, 'c_date', pd.Timestamp.today().date())
    data.insert(0, 'c_date', pd.Timestamp.today().date())
    data_final['c_date'] = pd.to_datetime(data_final['c_date'])
    db_connect.store_data("avg_delay_destination_final_over_time", data_final[['destination', 'c_date', 'ar_time_diff', 'dp_time_diff']])
    db_connect.store_data("avg_delay_destination_over_time", data[['destination', 'station', 'c_date', 'ar_time_diff', 'dp_time_diff']])


# Funktion für das Berechnen und die Konvertierung der Verspätungen aus den geänderten Arrivale und Departure Werten. Umbennen der Felder
# in einfachere Spaltennamen. Detektieren und speichern der Start- und Endbahnhöfe. Detektieren und speichern des Zielbahnhofs. Speichern
# der ursprüglichen Abfahrtszeit einer Zugverbindung (Für die einfachere Nutzung im Frontend). Diese Funktion versorgt alle anderen Funktionen
# mit Daten und ist die Grundtabelle aus denen alle Durchschnitte errechnet werden.
def delay(data):
    data['ar_time_diff'] = pd.to_datetime(data['n_ar_time']) - pd.to_datetime(data['ar_time'])
    data['dp_time_diff'] = pd.to_datetime(data['n_dp_time']) - pd.to_datetime(data['dp_time'])
    data['ar_time_diff'].fillna(pd.Timedelta(0), inplace = True)
    data['dp_time_diff'].fillna(pd.Timedelta(0), inplace = True)
    data['ar_time_diff'] = data['ar_time_diff'].astype(str)
    data['dp_time_diff'] = data['dp_time_diff'].astype(str)

    data = data.rename(columns={'@n': 'n'})
    data = data.rename(columns={'@date': 'date'})
    data = data.rename(columns={'@station': 'station'})

    data['date'] = pd.to_datetime(data['date'])

    data['first_station'] = data['ar_time'].isnull()
    data['final_station'] = data['dp_time'].isnull()

    data['destination'] = data['ppth'].str.split('|').str[-1]

    valid_dp_time = data['dp_time'].dropna()
    data['time'] = pd.to_datetime(valid_dp_time).dt.hour.astype(int)
    data['time'] = data['time'].reindex(data.index).fillna(-1).astype(int)
    
    db_connect.store_data("delay", data[['date', 'n', 'station', 'ar_time_diff', 'dp_time_diff','first_station', 'final_station', 'destination', 'time']])

    return 0