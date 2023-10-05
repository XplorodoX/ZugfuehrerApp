# Author: Marc Nebel
# Beschreibung: Modul für das erstmalige Initialiseren der Data Analyzer Datenbank beim ersten Start. Sollten die Tabellen 
# bereits existieren wird deren Erstellung übesprungen.

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Boolean
from sqlalchemy_utils import database_exists, create_database

# Postgres Verbindungs Daten
p_user = "p_user"
p_pass = "secretpwlel2341"
p_host = "192.168.0.8"
p_port = "5432"
p_db = "data"

# sqlalchemy engine Definition
connection_url = f'postgresql://{p_user}:{p_pass}@{p_host}:{p_port}/{p_db}'
engine = create_engine(connection_url)

# Prüfen ob die Tabelle bereits existiert
if not database_exists(engine.url):
    create_database(engine.url)

# In dieser Tabelle werden alle Verzögerungen und Basiskennwerte für weitere Berechnungen gespeichert. Diese Tabelle ist 
# nicht für die Verwendung außerhalb dieses Dienstes vorgesehen.
metadata = MetaData()
table1 = Table(
    'delay',
    metadata,
    Column('date', Date, primary_key=True),
    Column('n', Integer, primary_key=True),
    Column('station', String, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String),
    Column('first_station', Boolean),
    Column('final_station', Boolean),
    Column('destination', String),
    Column('time', Integer)
)

# Durchschnittliche Verzögerung aller vorhandenen Verzögerungen, die zu verschiedenen Zeitpunkten berechnet wurden.
table2 = Table(
    'avg_delay_at_over_time',
    metadata,
    Column('n', Integer, primary_key=True),
    Column('c_date', Date, primary_key=True),
    Column('station', String, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Durchschnittliche Verzögerung aller vorhandenen Verzögerungen
table3 = Table(
    'avg_delay_at',
    metadata,
    Column('n', Integer, primary_key=True),
    Column('station', String, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Durchschnittliche Verzögerung des Starts und des Ziels einer gegebenen Strecke
table4 = Table(
    'avg_delay_at_final',
    metadata,
    Column('n', Integer, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Durchschnittliche tägliche Verzögerung pro Linie. Beachten Sie, dass Linien pro Tag eindeutig sind, daher 
# ist diese Tabelle derzeit identisch mit der "delay"-Tabelle.
table5 = Table(
    'avg_delay_st_daily',
    metadata,
    Column('n', Integer, primary_key=True),
    Column('date', Date, primary_key=True),
    Column('station', String, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Durchschnittliche tägliche Verzögerung pro Linie am Start- und Zielpunkt der Fahrt
table6 = Table(
    'avg_delay_st_daily_final',
    metadata,
    Column('n', Integer, primary_key=True),
    Column('date', Date, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Das Gleiche wie oben, aber wöchentlich
table7 = Table(
    'avg_delay_st_weekly',
    metadata,
    Column('n', Integer, primary_key=True),
    Column('date', Date, primary_key=True),
    Column('station', String, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Das Gleiche wie oben, aber wöchentlich am Start- und Zielpunkt der Fahrt
table8 = Table(
    'avg_delay_st_weekly_final',
    metadata,
    Column('n', Integer, primary_key=True),
    Column('date', Date, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Das Gleiche wie oben, aber per monat
table9 = Table(
    'avg_delay_st_monthly',
    metadata,
    Column('n', Integer, primary_key=True),
    Column('date', Date, primary_key=True),
    Column('station', String, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Das Gleiche wie oben, aber per monat am Start- und Zielpunkt der Fahrt
table10 = Table(
    'avg_delay_st_monthly_final',
    metadata,
    Column('n', Integer, primary_key=True),
    Column('date', Date, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Durchschnittliche Verzögerungen des Starts und des Ziels einer gesamten Strecke (z. B. AA -> Ulm)
table11 = Table(
    'avg_delay_destination_final',
    metadata,
    Column('destination', String, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Das Gleiche wie oben, aber über verschiedene Zeitpunkte berechnet
table12 = Table(
    'avg_delay_destination_final_over_time',
    metadata,
    Column('destination', String, primary_key=True),
    Column('c_date', Date, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Verzögerung pro Station pro gesamte Strecke, etwas redundant, aber wichtig für Stationen mit mehreren Zielen
table13 = Table(
    'avg_delay_destination',
    metadata,
    Column('destination', String, primary_key=True),
    Column('station', String, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Das Gleiche wie oben, aber über Zeit
table14 = Table(
    'avg_delay_destination_over_time',
    metadata,
    Column('destination', String, primary_key=True),
    Column('station', String, primary_key=True),
    Column('c_date', Date, primary_key=True),
    Column('ar_time_diff', String),
    Column('dp_time_diff', String)
)

# Commiten der Änderungen an der Datenbank und löschen des engine objektes
metadata.create_all(engine)
engine.dispose()
