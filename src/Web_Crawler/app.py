# Author: Maximilian Müller

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome, ChromeOptions
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time

# Es wird immer eine Preisanalyse für Reisebeginn heutiger Tag+1 durchgeführt
# die Schrittweite definiert dann den Intervall für die Abfragen in der Zukunft
# bspwse. 7 Tage. Bei Eingabe "7" würde somit der Reiseantritt jeweils für die nächsten
# Schritte Wochen nach Preisen analysiert werden.

def crawler (startbahnhof, endbahnhof, schrittweite, schritte):


    output_list = []

    # Optionen für driver setzen

    options = ChromeOptions()
    
    # wenn Browser Window angzeigt werden soll die folgende Zeile auskommentieren

    options.add_argument('--headless')
    #options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    options.add_argument("--incognito")
    options.add_argument('--disable-application-cache')

    # Browser ausführen
    driver = Chrome("/usr/bin/chromedriver", options=options)

    # Lösche alle Cookies
    driver.delete_all_cookies()

    driver.get("https://reiseauskunft.bahn.de/bin/query.exe/dn?protocol=https:")

    # Seite vollständig Laden
    time.sleep(1)

    # Shadow DOM
    while True:
        try:

            shadow_host = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div:nth-child(1)'))
            )
            break
        except:
            pass

    # Javascript um Shadow root zu finden und Button zu clicken

    while True:
        try:
            driver.execute_script('''
                const shadowRoot = arguments[0].shadowRoot;
                const button = shadowRoot.querySelector('.js-accept-essential-cookies');
                button.click();
            ''', shadow_host)
            break
        except:
            pass

    for i in range(schritte):

        if i > 0:

            driver.get("https://reiseauskunft.bahn.de/bin/query.exe/dn?protocol=https:")

        # Start- und Zielort eingeben und Suche starten
        time.sleep(5)
        
        from_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "REQ0JourneyStopsS0G"))
        )
        from_input.clear()
        from_input.send_keys(startbahnhof)

        to_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "REQ0JourneyStopsZ0G"))
        )

        to_input.clear()
        to_input.send_keys(endbahnhof)
        
        # Suche Reisezeitpunkt +1 Tag

        if i==0:

            today = datetime.date.today()
            today = today + datetime.timedelta(days=1)
            formatiertesDatum = today.strftime("%d-%m-%y")
            driver.find_element(By.XPATH, '//*[@id="date0"]/span[2]').click()
            
        else:

            # Suche für definierte Schrittweite und Schritte

            today = datetime.date.today()
            futureDays = today + datetime.timedelta(days=schrittweite*i)
            formatiertesDatum = futureDays.strftime("%d-%m-%y")
            
            date_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="REQ0JourneyDate"]'))
            )

            date_input.clear()
            date_input.send_keys(formatiertesDatum)
        
        # bestpreise anzeigen
        time.sleep(1)
        element = driver.find_element(By.XPATH, '//*[@id="queryWrapper"]/div[5]/fieldset[2]/div/label/span[2]')
        element.click()
      
        # suche Starten

        driver.find_element(By.XPATH, '//*[@id="searchConnectionButton"]').click()

        wait = WebDriverWait(driver, 10)

        # Langstreckenreisen haben zusätzlich zu den Preisunterschieden abhängig
        # vom Buchungszeitpunkt zusätzlich noch verschiedene Preise zu verschiedenen
        # Abreisezeitpunkten über den Tag, hierbei wird in 6 Zeitslots unterschieden.
        # Slot 1 00:00 - 07:00 
        # Slot 2 bis 10:00
        # Slot 3 bis 13:00
        # Slot 4 bis 16:00
        # Slot 5 bis 19:00
        # Slot 6 bis 00:00

        for i in range(6):
            try:
                # Es wird über das Element #tbpSlot iteriert, so werden die Preise der einzelnen Slots 
                # gespeichert mit den zugehörigen Zeiten der Slots sowie dem Datum der Buchung.

                slot = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'#tbpSlot_{i}')))
                price = slot.find_element(By.CSS_SELECTOR, 'div.tbpSlotPrice')
                start_time = slot.find_element(By.CSS_SELECTOR, 'div.tbpSlotTimes > div.tbpSlotTimeStart')
                end_time = slot.find_element(By.CSS_SELECTOR, 'div.tbpSlotTimes > div.tbpSlotTimeEnd')

                output = f"Slot {i+1}:\nPreis: {price.text}\nStart time: {start_time.text}\nEnd time: {end_time.text}"
                output_dict = {}
                output_dict[formatiertesDatum] = output
                output_list.append(output_dict)
            except Exception as e:
                print(f"Error occurred for Slot {i+1}: {str(e)}")
                continue

    # Lösche alle Cookies
    driver.quit()

    return output_list

def toPicture(data):
    # Listen zur Speicherung der Daten für das Diagramm
    x_labels = []        # x-Achsenbeschriftungen (Datumsangaben)
    start_times = []     # Startzeiten der Slots
    end_times = []       # Endzeiten der Slots
    prices = []          # Preise der Slots
    slot_colors = []     # Farben der Slots

    for item in data:
        # Datum und Slot-Informationen aus dem Dictionary extrahieren
        date, slot_info = list(item.items())[0]

        # Startzeit, Endzeit und Preis aus den Slot-Informationen extrahieren
        start_time = slot_info.split('\n')[2].split(': ')[1]
        end_time = slot_info.split('\n')[3].split(': ')[1]
        price_str = slot_info.split('\n')[1].split('€')[0].split('ab ')[1]
        price = float(price_str.replace(',', '.'))
        slot = int(slot_info.split(':')[0].split('Slot ')[1])

        # Daten unique machen
        if date not in x_labels:
            x_labels.append(date)
        else:
            x_labels.append('')

        # Daten zu den entsprechenden Listen hinzufügen
        slot_colors.append(slot)
        start_times.append(start_time)
        end_times.append(end_time)
        prices.append(price)

    # Erstelle das Balkendiagramm
    fig, ax = plt.subplots(figsize=(10, 6))  # Größe des Diagramms anpassen
    fig.set_facecolor('#ddd7c5')
    bar_width = 1  # Breite der Balken anpassen

    index = range(len(x_labels))

    # Farbverlauf von Blau nach Orange erstellen
    color_map = plt.cm.get_cmap('coolwarm_r', max(slot_colors) + 1)

    # Balken erstellen und Farben entsprechend den Slots zuweisen
    bar1 = ax.bar(index, prices, bar_width, color=color_map(slot_colors))

    # Achsenbeschriftungen und Titel
    ax.set_xlabel('Datum')
    ax.set_ylabel('Preis in €')
    ax.set_title('Preise für Slots')

    # X-Achsenbeschriftungen auf Basis der Daten
    ax.set_xticks(index)
    ax.set_xticklabels(x_labels)

    # Y-Achsenbegrenzung
    ax.set_ylim([0, max(prices) + 50])

    # Legende für Slots
    slot_patches = []
    for slot, start_time, end_time in zip(range(1, max(slot_colors) + 1), start_times, end_times):
        slot_patch = mpatches.Patch(color=color_map(slot), label='Slot {}: {} - {}'.format(slot, start_time, end_time))
        slot_patches.append(slot_patch)
    ax.legend(handles=slot_patches)

    for rect in bar1:
        height = rect.get_height()
        width = rect.get_width()
        x = rect.get_x() + width / 2

        # Die Schriftgröße basierend auf der Breite des Balkens berechnen
        font_size = min(8, max(6, int(width * 5)))  # Die minimale und maximale Schriftgröße bei Bedarf anpassen

        # Die Position des Textes in der Mitte jedes Balkens festlegen
        text_x = x
        text_y = height / 2

        ax.text(text_x, text_y, '%.2f€' % height, ha='center', va='center', fontsize=font_size)
    
    ax.set_facecolor('#ddd7c5')

    # Anzeigen des Diagramms
    plt.tight_layout()
    plt.show()

    return plt



#if __name__ == '__main__':

    # Wir suchen nach den Preisen von Aalen Hbf nach Berlin Hbf bei heutiger Buchung für den nexten Tag,
    # sowie die Preise, wenn Reiseantritt in 1 Woche, 2 Wochen, ... , 4 Wochen wäre.
    # (7 ist schrittweite in Tagen und 5-1 ist die Anzahl an Schritten die gemacht werden sollen)

    #dictAalenBerlin = crawler("Crailsheim",'Hamburg Hbf',7 ,5)
    #toPicture(dictAalenBerlin)
    