import sys
import time # <--- WICHTIG: Das hier ganz oben zu den Imports packen!
import pandas as pd 
from extractors.wikipedia_api import get_wikipedia_data, get_top_wikipedia_trend, get_wikipedia_summary
from visualizers.plotter import create_trend_chart
from publishers.social_poster import post_to_telegram
from publishers.social_poster import post_to_twitter

# ... (Deine generate_smart_caption Funktion bleibt hier exakt so wie sie ist) ...

def main():
    print("🚀 Starte Daily Infographic Bot...")
    
    # Dynamisches Top-Thema holen
    thema = get_top_wikipedia_trend("de")
    
    # Kurzbeschreibung holen
    print("📚 Lade Kurzbeschreibung...")
    summary = get_wikipedia_summary(thema, "de")
    
    # NEU: Wir warten 2 Sekunden, damit Wikipedia uns nicht wegen Spam blockiert!
    print("⏳ Warte 2 Sekunden (Wikipedia Spam-Schutz)...")
    time.sleep(2)
    
    # Phase 1: Extraktion
    df = get_wikipedia_data(thema, days=30)
    
    # NEU: Genauere Fehlerausgabe
    if df is None:
        print("❌ Abbruch in Phase 1: get_wikipedia_data hat 'None' zurückgegeben (API hat evtl. blockiert).")
        return
    if df.empty:
        print("❌ Abbruch in Phase 1: Daten empfangen, aber die Tabelle ist leer.")
        return

    # Phase 2: Visualisierung
    chart_path = create_trend_chart(df, thema)
    if not chart_path:
        print("❌ Abbruch in Phase 2.")
        return
        
    # Phase 3: Publishing
    print("\n--- Generiere smarten Text ---")
    caption = generate_smart_caption(df, thema, summary)
    print(f"Generierter Text:\n{caption}\n")
    
    print("--- Starte Publishing-Phase ---")
    
    if ENABLE_TELEGRAM:
        post_to_telegram(chart_path, caption)
    else:
        print("⏭️ Telegram übersprungen.")

    if ENABLE_TWITTER:
        post_to_twitter(chart_path, caption)
    else:
        print("⏭️ Twitter übersprungen.")
        
    print("\n🎉 Pipeline erfolgreich komplett durchlaufen!")

if __name__ == "__main__":
    main()
