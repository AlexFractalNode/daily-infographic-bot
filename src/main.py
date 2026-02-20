import sys
from extractors.wikipedia_api import get_wikipedia_data
from visualizers.plotter import create_trend_chart

def main():
    print("🚀 Starte Daily Infographic Bot...")
    
    # Phase 1: Daten extrahieren
    thema = "Künstliche_Intelligenz"
    df = get_wikipedia_data(thema, days=30)
    
    if df is not None:
        print("🎉 Phase 1 (Extraction) ist abgeschlossen!")
        
        # Phase 2: Visualisierung
        chart_path = create_trend_chart(df, thema)
        print("🎉 Phase 2 (Visualization) ist abgeschlossen!")
        
    else:
        print("❌ Pipeline abgebrochen, da keine Daten geladen wurden.")

if __name__ == "__main__":
    main()
