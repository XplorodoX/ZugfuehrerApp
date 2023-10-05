# Author: Maximilian Müller

import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np
from analysis import basispreise

import logging
import sys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout
)
logger = logging.getLogger()

def plot_metrics(data):
    df = parse_json_response_metrics(data)
    df_list = []

    # Erstellt separate DataFrames für jeden Slot
    for i in range(1, 7):
        temp = df[df['Slots'].str.endswith(f'_slot{i}')].reset_index(drop=True)
        df_list.append(temp)

    # Ermittelt die Anzahl der Subplots
    num_subplots = len(df_list)

    # Berechnet die Anzahl der Zeilen für die Subplots
    num_rows = (num_subplots + 2) // 3

    # Erstellt die Subplots
    fig, axes = plt.subplots(num_rows, 3, figsize=(15, num_rows * 5), facecolor='#ddd7c5')

    # Zeichnet die Metrikdaten für jeden Slot in einen eigenen Subplot
    for i, df in enumerate(df_list):

        # Berechnet den Zeilenindex
        row = i // 3

        # Berechnet den Spaltenindex
        col = i % 3

        # Holt den entsprechenden Subplot
        ax = axes[row, col]

        values = ["+1T", "+1W", "+2W", "+3W", "+4W"]

        minimum = df['Minimum']
        mean = df['Mittelwert']
        maximum = df['Maximum']

        # Zeichnet die Linie für das Minimum
        ax.plot(values, minimum, label='Minimum')

        # Zeichnet die Linie für den Mittelwert
        ax.plot(values, mean, label='Mittelwert')

        # Zeichnet die Linie für das Maximum
        ax.plot(values, maximum, label='Maximum')

        # Achsenbeschriftungen & Legende
        ax.set_facecolor('#ddd7c5')
        ax.set_xlabel('Schritte')
        ax.set_ylabel('Preis')
        
        # Titel
        if i == 0:
            ax.set_title('0 - 7 Uhr')
        elif i == 1:
            ax.set_title('7 - 10 Uhr')
        elif i == 2:
            ax.set_title('10 - 13 Uhr')
        elif i == 3:
            ax.set_title('13 - 16 Uhr')
        elif i == 4:
            ax.set_title('16 - 19 Uhr')
        elif i == 5:
            ax.set_title('19 - 24 Uhr')
        else:
            ax.set_title('Unknown')

        ax.legend()

    # Entfernt leere Subplots, falls die Anzahl der Subplots nicht durch 3 teilbar ist
    if num_subplots % 3 != 0:
        for i in range(num_subplots, num_rows * 3):
            row = i // 3
            col = i % 3
            fig.delaxes(axes[row, col])

    plt.suptitle('Preismetriken')  # Setze den Titel für den gesamten Plot
    plt.tight_layout()
    return plt



def parse_json_response_metrics(json_response):
    # JSON in Python-Objekt umwandeln
    data = json.loads(json_response)

    # DataFrame für Minimum erstellen
    df_min = pd.DataFrame.from_dict(data["Minimum"], orient="index", columns=["Minimum"])

    # DataFrame für Mean erstellen, falls der Schlüssel vorhanden ist
    df_mean = pd.DataFrame.from_dict(data["Mean"], orient="index", columns=["Mittelwert"])

    # DataFrame für Maximum erstellen
    df_max = pd.DataFrame.from_dict(data["Maximum"], orient="index", columns=["Maximum"])

    # DataFrame für alle Slots erstellen
    df_slots = pd.DataFrame.from_dict(data["Column"], orient="index", columns=["Slots"])

    # DataFrame für alle Slots zusammenführen
    df = pd.concat([df_slots, df_min, df_mean, df_max], axis=1)

    return df

def plot_preisanstiege(data):
    plt.figure(figsize=(10, 6), facecolor='#ddd7c5')
    
    if sum(data.iloc[0] > 0):
        # Alle 0 Werte entfernen
        data = data.drop(columns=data.columns[data.eq(0).any()])

        # Farbverlauf von Blau zu Orange erstellen
        colors = plt.cm.coolwarm(np.linspace(0, 1, len(data.columns)))[::-1]

        # Pie-Chart erstellen mit Farbverlauf
        plt.pie(data.iloc[0], labels=data.columns, autopct='%1.1f%%', colors=colors)
    # Für lokales Testing
    else:
        # Farbverlauf von Blau zu Orange erstellen
        colors = plt.cm.coolwarm(np.linspace(0, 1, len(data.columns)))[::-1]

        data.iloc[0] = 1
        # Einzelnes Segment mit blauer Farbe erstellen
        plt.pie(data.iloc[0], labels=data.columns, autopct='%1.1f%%', colors=colors)
    
    # Achsentitel festlegen
    plt.title("Preisänderung nach Tagesstunden")
    plt.xlabel("Stunden")
    
    plt.tight_layout()
    
    return plt

def plot_preistrend_all(data, endbahnhof=None):

    data = json.loads(data)
    # Daten als DataFrame
    df = pd.DataFrame.from_dict(data)

    df_list = []

    for i in range(1, 7):
        columns_to_extract = [col for col in df.columns if col.endswith(f'_slot{i}')]

        # Erstelle ein neues DataFrame mit den extrahierten Spalten
        df_extracted = df[columns_to_extract].copy()
        df_list.append(df_extracted)

    # Listen für die resultierenden DataFrames
    df_dif_proz_list = []
    df_dif_real_list = []

    # Iteriere über jedes DataFrame in der Liste
    for df in df_list:
        # Extrahiere Spalten mit "dif_proz"
        df_dif_proz = df[[col for col in df.columns if 'dif_proz' in col]].copy()
        df_dif_proz_list.append(df_dif_proz)

        # Extrahiere Spalten mit "dif_real"
        df_dif_real = df[[col for col in df.columns if 'dif_real' in col]].copy()
        df_dif_real_list.append(df_dif_real)

    # Werte für die x-Achse
    x_values = ["1T->7Tage", "7T->14T", "14T->21T", "21T->28T"]

    # Erstelle eine Abbildung (Figure) und Subplots mit 3x2 Layout
    fig, axes = plt.subplots(3, 2, figsize=(12, 12), facecolor='#ddd7c5')
    fig.suptitle('Preistrend', fontsize=16)

    # Iteriere über jedes DataFrame in den Listen
    for idx, (df_dif_proz, df_dif_real) in enumerate(zip(df_dif_proz_list, df_dif_real_list)):
        # Berechne die Position des Subplots
        row = idx // 2
        col = idx % 2

        # Plot für dif_real
        ax_real = axes[row, col]
        ax_real.plot(x_values, df_dif_real.iloc[0].values, marker='o', label='dif_real')
        for i, val in enumerate(df_dif_real.iloc[0].values):
            if val != 0:
                ax_real.text(i, val, f"{round(val, 2)} €", ha='center', va='bottom')

        # Plot für dif_proz (als durchsichtige Balken mit Farben und Beschriftung)
        ax_proz = ax_real.twinx()
        for i, val in enumerate(df_dif_proz.iloc[0].values):
            if val != 0:
                color = 'orange' if val > 0 else 'blue'
                ax_proz.bar(i, val, align='center', alpha=0.5, color=color)
                if val > 0:
                    ax_proz.text(i, val/2, f"+{round(val, 2)}%", ha='center', va='center')
                else:
                    ax_proz.text(i, val/2, f"{round(val, 2)}%", ha='center', va='center')

        # Achsenbeschriftung
        ax_real.set_xlabel('Zeitschritte')
        ax_real.set_ylabel('Werte (€)')
        ax_proz.set_ylabel('Werte (%)')

        base_price_check = False

        if endbahnhof:
            base_price_check = True
            result_json = basispreise(endbahnhof=endbahnhof).to_json(orient='columns')

            base_price_json = json.loads(result_json)

            logger.info(base_price_json)
            logger.info(type(base_price_json))
            
            # extrahiere Preise und speichere sie in Variablen
            for k, v in base_price_json.items():
                if k == '1_1':
                    base_price_0 = v.get("0")
                elif k == '1_2':
                    base_price_1 = v.get("0")
                elif k == '1_3':
                    base_price_2 = v.get("0")
                elif k == '1_4':
                    base_price_3 = v.get("0")
                elif k == '1_5':
                    base_price_4 = v.get("0")
                elif k == '1_6':
                    base_price_5 = v.get("0")


        # Titel mit ermittelten Variablen
        if idx == 0:
            ax_real.set_title(f'0 bis 7 Uhr - Basispreis: {base_price_0:.2f}€' if base_price_check else '0 bis 7 Uhr')
        elif idx == 1:
            ax_real.set_title(f'7 bis 10 Uhr - Basispreis: {base_price_1:.2f}€' if base_price_check else '7 bis 10 Uhr')
        elif idx == 2:
            ax_real.set_title(f'10 bis 13 Uhr - Basispreis: {base_price_2:.2f}€' if base_price_check else '10 bis 13 Uhr')
        elif idx == 3:
            ax_real.set_title(f'13 bis 16 Uhr - Basispreis: {base_price_3:.2f}€' if base_price_check else '13 bis 16 Uhr')
        elif idx == 4:
            ax_real.set_title(f'16 bis 19 Uhr - Basispreis: {base_price_4:.2f}€' if base_price_check else '16 bis 19 Uhr')
        elif idx == 5:
            ax_real.set_title(f'19 bis 24 Uhr - Basispreis: {base_price_5:.2f}€' if base_price_check else '19 bis 24 Uhr')
        else:
            ax_real.set_title('Unknown')

        # Legende
        ax_real.legend(loc='upper left')

        # Setze den Hintergrundfarbe des Subplots
        ax_real.set_facecolor('#ddd7c5')
        ax_proz.set_facecolor('#ddd7c5')

    # Entferne überflüssige Subplots
    if len(df_dif_proz_list) < 6:
        for idx in range(len(df_dif_proz_list), 6):
            row = idx // 2
            col = idx % 2
            fig.delaxes(axes[row, col])

    # Passt den Layout an
    fig.tight_layout(rect=[0, 0, 1, 0.95])

    return fig
