import requests
import pandas as pd
from datetime import datetime, timedelta

def get_exchange_rate_data(base="EUR", target="USD", days=30):
    """
    Holt die historischen Wechselkurse der Europäischen Zentralbank (EZB).
    Nutzt die quelloffene Frankfurter API (kein API-Key notwendig).
    """
    print(f"💶 Lade Wechselkurse ({base} zu {target}) der letzten {days} Tage...")
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    
    # Frankfurter API Endpoint für Zeitreihen
    url = f"https://api.frankfurter.app/{start_str}..{end_str}?from={base}&to={target}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", {})
            
            if not rates:
                print("❌ Keine Wechselkursdaten erhalten.")
                return None
                
            all_data = []
            # Die API gibt ein Dictionary zurück (Datum -> {Währung: Kurs})
            for date_str, rate_info in rates.items():
                val = rate_info.get(target)
                if val:
                    all_data.append({'timestamp': pd.to_datetime(date_str).date(), 'Aufrufe': val})
                    
            df = pd.DataFrame(all_data)
            
            # Sortieren, um sicherzugehen, dass die Zeitachse im Plotter stimmt
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            print(f"✅ Wechselkurs-Daten erfolgreich geladen! (Aktuell: {df['Aufrufe'].iloc[-1]:.4f} {target})")
            return df
            
        else:
            print(f"⚠️ EZB API Fehler: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Fehler bei der Wechselkurs API-Abfrage: {e}")
        return None
