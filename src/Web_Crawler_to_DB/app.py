# Author: Maximilian Müller

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome, ChromeOptions
import selenium
import datetime
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
                slot = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f'#tbpSlot_{i}')))
                price = slot.find_element(By.CSS_SELECTOR, 'div.tbpSlotPrice')
                start_time = slot.find_element(By.CSS_SELECTOR, 'div.tbpSlotTimes > div.tbpSlotTimeStart')
                end_time = slot.find_element(By.CSS_SELECTOR, 'div.tbpSlotTimes > div.tbpSlotTimeEnd')

                output = f"Slot {i+1}:\nPreis: {price.text.replace(',', '.').replace(' ', '')}\nStart time: {start_time.text}\nEnd time: {end_time.text}"
                output_dict = {}
                output_dict[formatiertesDatum] = output
                output_list.append(output_dict)
            except Exception as e:
                print(f"Error occurred for Slot {i+1}: {str(e)}")
                continue

    # Lösche alle Cookies
    driver.quit()

    return output_list
    