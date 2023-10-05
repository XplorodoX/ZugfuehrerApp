# Author: Maximilian Müller

import pandas as pd

# Datenaufbereitung
def polishData(data, startbahnhof, endbahnhof, Zeit):

    df = pd.DataFrame()

    for i, entry in enumerate(data):
        date = list(entry.keys())[0]
        price = entry[date].split('\n')[1].split(':')[1].strip().replace('ab', '').replace('€', '')

        column_name = f'step{i // 6 + 1}_slot{i % 6 + 1}'
        df[column_name] = [price]
    
    df['startbahnhof'] = startbahnhof  # Platzhalter für die Spalte "startbahnhof"
    df['endbahnhof'] = endbahnhof  # Platzhalter für die Spalte "endbahnhof"
    df['timestamp'] = Zeit  # Platzhalter für die Spalte "timestamp"

    return df
