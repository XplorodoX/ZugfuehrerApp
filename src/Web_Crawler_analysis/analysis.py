from dataGathering import  get_data_by_endbahnhof
import pandas as pd

# Berechnung min, mean, und max für jeden Step
def calculate_price_statistics(endbahnhof):

    data = get_data_by_endbahnhof(endbahnhof)

    if data.empty:
        print("No data available in the database.")
        return
    
    # Entferne unerwünschte Spalten
    columns_to_exclude = ['timestamp', 'startbahnhof', 'endbahnhof', 'id']
    data = data.drop(columns=columns_to_exclude)
    
    # Berechne die Statistiken für jede Spalte
    statistics = {
        'Column': [],
        'Minimum': [],
        'Mean': [],
        'Maximum': []
    }
    
    for column in data.columns:
        minimum = data[column].min()
        mean = data[column].mean()
        maximum = data[column].max()
        
        statistics['Column'].append(column)
        statistics['Minimum'].append(minimum)
        statistics['Mean'].append(mean)
        statistics['Maximum'].append(maximum)
    
    # Erstelle ein DataFrame aus den Statistiken
    statistics_df = pd.DataFrame(statistics)
    
    return statistics_df

# Berechne aus start und Endzeit die zugehörigen Slots
def get_slots_in_time_range(start_hour, end_hour):
    slots = {
        1: (0, 7),
        2: (7, 10),
        3: (10, 13),
        4: (13, 16),
        5: (16, 19),
        6: (19, 0)
    }
    
    selected_slots = []

    for slot, (start, end) in slots.items():
        if start_hour <= end_hour:
            if start <= start_hour < end or start < end_hour <= end:
                selected_slots.append(slot)
        else:
            if start <= start_hour <= 23 or 0 <= end_hour < end:
                selected_slots.append(slot)
    
    return selected_slots

# Gebe alle Reisen aus, welche die Parameter erfüllen
def budget(budget, vonUhrzeit, bisUhrzeit, endbahnhof):
    data = get_data_by_endbahnhof(endbahnhof)

    if data.empty:
        print("No data available in the database.")
        return None

    # Sortiere die Daten nach dem Timestamp in absteigender Reihenfolge
    data.sort_values(by='timestamp', ascending=False, inplace=True)

    # Behalte nur die jüngste Zeile
    data = data.head(1)

    # Definiere die Zeitintervalle für die einzelnen Slots
    selected_slots = get_slots_in_time_range(vonUhrzeit, bisUhrzeit)

    step_slots_list = []
    for num in selected_slots:
        for step in range(1, 6):
            step_slots_list.append(f"step{step}_slot{num}")
    
    filtered_df = data.filter(items=step_slots_list)

    columns_to_drop = []
    
    for col in filtered_df.columns:
        if filtered_df[col].min() >= budget:
            columns_to_drop.append(col)

    # Entferne die ausgewählten Spalten
    filtered_df = filtered_df.drop(columns=columns_to_drop)

    return filtered_df

# Gibt Preisanstiege (kurzfristig) aus, sprich zählt für jede Tagesstunde, wie oft sich Preise erhöht haben
def preisanstiege(endbahnhof):
    data = get_data_by_endbahnhof(endbahnhof)
    
    if data.empty:
        print("No data available in the database.")
        return
    
    # Entferne unerwünschte Spalten
    columns_to_exclude = ['startbahnhof', 'endbahnhof', 'id']
    data = data.drop(columns=columns_to_exclude)
    
    # Erstelle ein defaultdict für die Preisanstiegszählung pro Stunde
    df = pd.DataFrame(columns=range(24))
    df.loc[0]=0
    
    # Durchlaufe die Datenpunkte
    for i in range(len(data) - 1):  # Iteriere bis zur vorletzten Zeile
        current_row = data.iloc[i]  # Aktuelle Datenpunkt-Zeile
        next_row = data.iloc[i + 1]  # Nächste Datenpunkt-Zeile
        
        # Überprüfe die Preisanstiege für jeden Slot in Step 1
        for slot in range(1, 6):
            current_price = current_row[f'step1_slot{slot}']
            next_price = next_row[f'step1_slot{slot}']
            
            # Überprüfe, ob der nächste Preis größer ist als der aktuelle
            if next_price > current_price:
                timestamp = current_row['timestamp']
                hour = pd.to_datetime(timestamp).hour
                df.loc[0, hour] += 1

    return df

# iteriere über Preisanstiege
def preisanstiege_alle():
    endbahnhöfe = ["Berlin Hbf", "Hamburg Hbf", "München Hbf", "Dortmund Hbf", "Frankfurt(Main)Hbf"]
    result = pd.DataFrame(columns=range(24))
    result.loc[0]=0

    for endbahnhof in endbahnhöfe:
        temp_df = preisanstiege(endbahnhof)
        for i in range(24):
            result.loc[0,i]+= temp_df.loc[0,i]
    
    return result

# Ermittle Basispreise (Abreisezeitpunkt = Buchungstag + 1) für jeden Slot
def basispreise (endbahnhof):
    data = get_data_by_endbahnhof(endbahnhof)

    if data.empty:
        print("No data available in the database.")
        return
    
    # Entferne unerwünschte Spalten
    columns_to_exclude = ['startbahnhof', 'endbahnhof', 'id', 'timestamp']
    data = data.drop(columns=columns_to_exclude)

    # Berechne die Mittelwerte der Preise über Steps und Slots
    mean_prices = data.mean()
    mean_prices.round(2)
    # Erstelle ein leeres Dictionary für die Ergebnisse
    result_dict = {}

    # Speichere den Preis für Step 1 für jeden Slot
    for slot in range(1, 7):
        step1_price = mean_prices[f'step1_slot{slot}']
        result_dict[f'1_{slot}'] = step1_price
    
    # Erstelle ein DataFrame aus dem result_dict
    result_df = pd.DataFrame(result_dict, index=[0])
    return result_df

# Es werden prozentuale und reale Differenzen zwischen den Steps innerhalb der Slots ermittelt
def preistrend(endbahnhof):
    data = get_data_by_endbahnhof(endbahnhof)

    if data.empty:
        print("No data available in the database.")
        return
    
    # Entferne unerwünschte Spalten
    columns_to_exclude = ['startbahnhof', 'endbahnhof', 'id', 'timestamp']
    data = data.drop(columns=columns_to_exclude)
    
    # Berechne die Mittelwerte der Preise über Steps und Slots
    mean_prices = data.mean()
    
    # Erstelle ein leeres Dictionary für die Ergebnisse
    result_dict = {}
    
    # Speichere den Preis für Step 1 für jeden Slot
    for slot in range(1, 7):
        step1_price = mean_prices[f'step1_slot{slot}']
        result_dict[f'1_{slot}'] = step1_price
    
    # Berechne die prozentualen und absoluten Unterschiede zwischen den Slots über die Steps
    for step in range(1, 5):
        for slot in range(1, 7):
            current_price = mean_prices[f'step{step}_slot{slot}']
            next_price = mean_prices[f'step{step+1}_slot{slot}']
            
            dif_proz = (next_price - current_price) / current_price * 100
            dif_real = next_price - current_price
            
            result_dict[f'dif_proz_step{step}_step{step+1}_slot{slot}'] = dif_proz
            result_dict[f'dif_real_step{step}_step{step+1}_slot{slot}'] = dif_real
    
    # Erstelle ein DataFrame aus dem result_dict
    result_df = pd.DataFrame(result_dict, index=[0])
    
    return result_df

# Iteriere über preistrend und bilde Mittelwert
def preistrend_alle():
    endbahnhöfe = ["Berlin Hbf", "Hamburg Hbf", "München Hbf", "Dortmund Hbf", "Frankfurt(Main)Hbf"]
    result = pd.DataFrame(columns=range(1, 21))
    
    for endbahnhof in endbahnhöfe:
        trend_df = preistrend(endbahnhof)
        result = pd.concat([result, trend_df], ignore_index=True)
    
    # Berechne den Durchschnitt der Preisänderungen über alle Endbahnhöfe
    result_mean = result.mean()
    
    # Erstelle ein leeres DataFrame für die formatierte Ausgabe
    output_df = pd.DataFrame(columns=result.columns)
    
    # Füge den Durchschnitt der Preisänderungen als Zeile zum Ausgabedatenrahmen hinzu
    output_df.loc[0] = result_mean
    
    return output_df
