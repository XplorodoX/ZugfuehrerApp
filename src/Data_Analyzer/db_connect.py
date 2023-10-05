# Author: Marc Nebel
# Beschreibung: Datenbankmodul, welches sich mit der PostgreSQL Datenbank des Data_Analyzer Service verbindet. Speichert und aktualisiert Daten und
# macht diese einfach zugänglich

import pandas as pd
from sqlalchemy import create_engine, exc, text

# Postgres Verbindungs Daten
p_user = "p_user"
p_pass = "secretpwlel2341"
p_host = "192.168.0.8"
p_port = "5432"
p_db = "data"

# sqlalchemy engine Definition
connection_url = f'postgresql://{p_user}:{p_pass}@{p_host}:{p_port}/{p_db}'
engine = create_engine(connection_url)


# Funktion für das Speichern und aktualieren von Daten. Die Input Daten sind Pandas Dataframes. Da es der Pandas to_sql Methode nicht möglich ist Daten
# zu updaten wird diese Funktion benötigt. Dabei wird der Datenframe in eine temporäre Tabelle gespeichert welche mit der Zieltabelle verglichen wird. 
# Sollten die Daten bereits existieren werden sie an den definierten key columns aktualisiert. 
# Diese Funktion besiert lose auf der Lösung dieses Threads: https://stackoverflow.com/questions/52188446/pandas-to-sql-to-update-unique-values-in-db
def store_data(t_name, data):
    data.to_sql('t_temp', engine, if_exists = 'replace', index = False)
    with engine.begin() as cn:
        column_names = data.columns.tolist()
        columns = ', '.join(column_names)
        if data.empty:
            return 0
        prim_keys = data.iloc[[0], :3]
        primary_key_columns = []
        if 'date' in prim_keys.columns:
            primary_key_columns.append('date')
        if 'c_date' in prim_keys.columns:
            primary_key_columns.append('c_date')
        if 'n' in prim_keys.columns:
            primary_key_columns.append('n')
        if 'station' in prim_keys.columns:
            primary_key_columns.append('station')
        if 'destination' in prim_keys.columns:
            primary_key_columns.append('destination')
        
        match_columns = ' AND '.join(f"t.{c} = f.{c}" for c in primary_key_columns)

        insert_sql = f"""INSERT INTO {t_name} ({columns})
                        SELECT {columns}
                        FROM t_temp t
                        WHERE NOT EXISTS 
                            (SELECT 1 FROM {t_name} f
                             WHERE {match_columns})"""
        cn.execute(text(insert_sql))

        update_assignments = ', '.join(f"{c} = t.{c}" for c in column_names if c not in primary_key_columns)

        if match_columns:
            update_sql = f"""UPDATE {t_name} f
                             SET {update_assignments}
                             FROM t_temp t
                             WHERE {match_columns}"""
            cn.execute(text(update_sql))

    with engine.begin() as cn:
        cn.execute(text("DROP TABLE IF EXISTS t_temp"))

    return 0

# Funktion für das Auslesen einer gesammten SQL Tabelle
def get_table(t_name):
    query = f"SELECT * FROM {t_name}"
    data = pd.read_sql(query, engine)
    return data

# Funktion für das Auslesen einer SQL Tabelle mit einem Suchparameter
def get_table_specific(t_name, c_name, value):
    query = f"SELECT * FROM {t_name} WHERE {c_name} = '{value}'"
    data = pd.read_sql(query, engine)
    return data

# Funktion für das Auslesen einer SQL Tabelle mit zwei Suchparametern
def get_table_specific2(t_name, c_name1, c_value1, c_name2, c_value2):
    query = f"SELECT * FROM {t_name} WHERE {c_name1} = '{c_value1}' AND {c_name2} = '{c_value2}'"
    data = pd.read_sql(query, engine)
    return data

# Funktion für das Auslesen einer SQL Tabelle mit drei Suchparametern
def get_table_specific3(t_name, c_name1, c_value1, c_name2, c_value2, c_name3, c_value3):
    query = f"SELECT * FROM {t_name} WHERE {c_name1} = '{c_value1}' AND {c_name2} = '{c_value2}' AND {c_name3} = '{c_value3}"
    data = pd.read_sql(query, engine)
    return data