import os
import time
import requests
import pandas as pd
from datetime import datetime, timedelta

def get_nasa_neo_data(days=30):
    """
    Holt die Anzahl der erdnahen Asteroiden (NEOs) pro Tag von der NASA API.
    Da die NASA API max. 7 Tage pro Anfrage erlaubt, stückeln wir die Abfrage.
    """
    print(f"☄️ Lade NASA Asteroiden-Daten für die letzten {days} Tage...")
    
    # Key aus den Secrets laden (oder DEMO_KEY als Notfall-Fallback)
    api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    current_end = end_date
    all_data = []
    
    # In 7-Tage-Schritten rückwärts durch die Zeit gehen
    while current_end > start_date:
        # Der Startpunkt des aktuellen Häppchens
        current_start = max(current_end - timedelta(days=7), start_date)
        
        start_str = current_start.strftime('%Y-%m-%d')
        end_str = current_end.strftime('%Y-%m-%d')
        
        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_str}&end_date={end_str}&api_key={api_key}"
        
        try:
            print(f"   -> Lade Zeitraum: {start_str} bis {end_str}...")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                near_earth_objects = data.get('near_earth_objects', {})
                
                # Daten auspacken und zählen
                for date_key, asteroids in near_earth_objects.items():
                    # Wir zählen, wie viele Asteroiden an diesem Tag vorbeiflogen
                    count = len(asteroids)
                    all_data.append({'timestamp': pd.to_datetime(date_key).date(), 'Wert': count})
            
            elif response.status_code == 429:
                print("⚠️ NASA API Rate Limit erreicht. Breche Schleife ab.")
                break
            else:
                print(f"⚠️ NASA API Fehler: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Fehler bei der NASA API-Abfrage: {e}")
            
        # Den Zeitraum für den nächsten Schleifendurchlauf verschieben
        current_end = current_start - timedelta(days=1)
        
        # Kurze Pause, um die NASA-Server nicht zu spammen
        time.sleep(1.5) 
        
    if not all_data:
        print("❌ Keine NASA-Daten gefunden.")
        return None
        
    df = pd.DataFrame(all_data)
    
    # Nach Datum sortieren (da wir rückwärts in der Zeit gereist sind)
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    # WICHTIGER TRICK: Wir benennen die Spalte vorerst in 'Aufrufe' um, 
    # damit unsere plotter.py Datei das Diagramm ohne Absturz zeichnen kann!
    df = df.rename(columns={'Wert': 'Aufrufe'})
    
    print(f"✅ NASA-Daten erfolgreich geladen! ({len(df)} Tage verarbeitet)")
    return df
