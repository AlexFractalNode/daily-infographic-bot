import requests
import pandas as pd
from datetime import datetime

def get_weather_data(city="Berlin", lat=52.52, lon=13.41, days=30):
    """
    Holt die tägliche Höchsttemperatur der letzten 30 Tage.
    Nutzt Open-Meteo (welches u.a. DWD-Daten verwendet) für perfekt formatierte historische Daten.
    Kein API-Key notwendig!
    """
    print(f"🌡️ Lade Wetter-Daten (Max. Temperatur) für {city} der letzten {days} Tage...")
    
    # Open-Meteo API für historische und aktuelle Tagesdaten
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max&past_days={days}&forecast_days=0&timezone=Europe%2FBerlin"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            daily_data = data.get("daily", {})
            
            dates = daily_data.get("time", [])
            temps = daily_data.get("temperature_2m_max", [])
            
            if not dates or not temps:
                print("❌ Keine Wetterdaten erhalten.")
                return None
                
            # Daten für unseren DataFrame verpacken
            df = pd.DataFrame({
                'timestamp': pd.to_datetime(dates).dt.date,
                'Aufrufe': temps  # Intern nennen wir es 'Aufrufe', damit der Plotter glücklich ist!
            })
            
            # Die Open-Meteo API liefert manchmal den heutigen Tag doppelt oder unvollständig
            df = df.drop_duplicates(subset=['timestamp'], keep='first')
            
            print(f"✅ Wetter-Daten erfolgreich geladen! (Aktuell: {df['Aufrufe'].iloc[-1]}°C)")
            return df
            
        else:
            print(f"⚠️ Wetter API Fehler: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Fehler bei der Wetter API-Abfrage: {e}")
        return None
