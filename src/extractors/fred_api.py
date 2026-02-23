import os
import requests
import pandas as pd
from datetime import datetime, timedelta

def get_fred_data(series_id="DGS10", days=30):
    """
    Holt makroökonomische Daten von der FRED API der US-Notenbank.
    Standard: DGS10 (10-Year Treasury Constant Maturity Rate - Tägliche US-Zinsen).
    """
    print(f"🏦 Lade FRED Makro-Daten (Serie: {series_id}) der letzten {days} Tage...")
    
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        print("❌ Fehler: FRED_API_KEY fehlt in den GitHub Secrets!")
        return None

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    # FRED API Endpoint
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={api_key}&file_type=json&observation_start={start_str}&observation_end={end_str}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            observations = data.get("observations", [])
            
            if not observations:
                print("❌ Keine FRED-Daten gefunden.")
                return None
                
            all_data = []
            for obs in observations:
                val = obs.get("value")
                # Feiertage (gekennzeichnet mit ".") überspringen
                if val != ".":
                    all_data.append({
                        'timestamp': pd.to_datetime(obs.get("date")).date(),
                        'Aufrufe': float(val)  # Wir nutzen wieder 'Aufrufe' für den Plotter
                    })
                    
            df = pd.DataFrame(all_data)
            print(f"✅ FRED-Daten erfolgreich geladen! (Aktuell: {df['Aufrufe'].iloc[-1]:.2f}%)")
            return df
            
        else:
            print(f"⚠️ FRED API Fehler: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Fehler bei der FRED API-Abfrage: {e}")
        return None
