import time
import requests
import pandas as pd
from datetime import datetime

def get_crypto_data(coin_id="bitcoin", currency="usd", days=30):
    """
    Holt die historischen Preisdaten einer Kryptowährung von CoinGecko.
    Standardmäßig: Bitcoin in USD für die letzten 30 Tage.
    """
    print(f"🪙 Lade Krypto-Daten für {coin_id.capitalize()} der letzten {days} Tage...")
    
    # Die CoinGecko API für historische Marktdaten (kostenlos, kein API-Key nötig!)
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency={currency}&days={days}&interval=daily"
    
    headers = {
        "User-Agent": "DataZeitgeistBot/1.0",
        "Accept": "application/json"
    }
    
    try:
        # Kurze Pause, da CoinGecko bei der kostenlosen API auf Rate Limits achtet
        time.sleep(2)
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            prices = data.get("prices", [])
            
            if not prices:
                print("❌ Keine Preisdaten von CoinGecko erhalten.")
                return None
                
            all_data = []
            for item in prices:
                # CoinGecko liefert den Timestamp in Millisekunden, wir brauchen Sekunden
                timestamp_ms = item[0]
                price = item[1]
                
                date_obj = datetime.utcfromtimestamp(timestamp_ms / 1000).date()
                all_data.append({'timestamp': date_obj, 'Wert': price})
                
            df = pd.DataFrame(all_data)
            
            # WICHTIG: Damit unser standardisierter Plotter nicht abstürzt, 
            # benennen wir die Wert-Spalte intern wieder in 'Aufrufe' um.
            df = df.rename(columns={'Wert': 'Aufrufe'})
            
            # Manchmal gibt CoinGecko den aktuellsten Tag doppelt zurück, das bereinigen wir:
            df = df.drop_duplicates(subset=['timestamp'], keep='last')
            
            print(f"✅ Krypto-Daten erfolgreich geladen! (Aktueller Preis: ~${int(df['Aufrufe'].iloc[-1]):,})")
            return df
            
        else:
            print(f"⚠️ CoinGecko API Fehler: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Fehler bei der Krypto API-Abfrage: {e}")
        return None
