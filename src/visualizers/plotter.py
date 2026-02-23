import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# ==========================================
# FUNKTION 1: STANDARD LINIENDIAGRAMM
# ==========================================
def create_trend_chart(df, thema, source_name="Wikipedia", y_label="Aufrufe"):
    """
    Erstellt ein ansprechendes Liniendiagramm mit Trendlinie und Höchstwert-Markierung.
    Wird für isolierte Datensätze (z.B. nur NASA oder nur Wetter) genutzt.
    """
    print(f"🎨 Generiere professionelle Grafik für {source_name}...")
    
    os.makedirs("output", exist_ok=True)
    chart_path = "output/trend_chart.png"
    
    try:
        # 1. Daten und Basis-Setup vorbereiten
        thema_clean = thema.replace('_', ' ')
        if 'timestamp' in df.columns:
            df = df.set_index('timestamp')
            
        df['Trend'] = df['Aufrufe'].rolling(window=7, min_periods=1).mean()
        
        max_views = df['Aufrufe'].max()
        max_date = df['Aufrufe'].idxmax()

        # 2. Design & Farben
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
        
        bg_color = '#15202b'
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        ax.grid(color='#38444d', linestyle='--', linewidth=0.5, alpha=0.7)

        # 3. Dynamische Y-Achse berechnen (damit kleine Schwankungen sichtbar werden)
        min_val = df['Aufrufe'].min()
        max_val = df['Aufrufe'].max()
        padding = (max_val - min_val) * 0.2 
        
        if padding == 0: padding = min_val * 0.05 
        
        lower_bound = min_val - padding
        upper_bound = max_val + padding
        ax.set_ylim(lower_bound, upper_bound)

        # 4. Linien und Flächen zeichnen
        ax.fill_between(df.index, df['Aufrufe'], lower_bound, color='#1DA1F2', alpha=0.2)
        ax.plot(df.index, df['Aufrufe'], color='#1DA1F2', linewidth=1.5, alpha=0.5, label=f'Tägliche {y_label}')
        ax.plot(df.index, df['Trend'], color='#FFD700', linewidth=3, label='7-Tage Trend')
        
        ax.legend(loc='upper left', facecolor=bg_color, edgecolor='#38444d', labelcolor='white')

        # 5. Den Höchstwert markieren (Pfeil & Text)
        if max_views < 10:
            max_views_str = f"{max_views:.4f}" 
        elif max_views < 100:
            max_views_str = f"{max_views:.1f}" 
        else:
            max_views_str = f"{int(max_views):,}".replace(',', '.') 
            
        # Die passende Einheit zum Modul finden
        unit = ""
        if source_name == "Makro/FRED": unit = "%"
        elif source_name == "Umwelt/DWD": unit = "°C"
        elif source_name in ["EZB", "Krypto"]: unit = " $"
            
        # Hänge die Einheit direkt an den Peak-String an
        ax.annotate(f'Peak: {max_views_str}{unit}',
                    xy=(max_date, max_views),
                    xytext=(10, 20), 
                    textcoords='offset points',
                    color='white',
                    fontweight='bold',
                    arrowprops=dict(arrowstyle="->", color='#FFD700', lw=1.5))

        # 6. Beschriftungen und Achsen formatieren
        plt.title(f'{source_name} Trend: {thema_clean}', color='white', fontsize=16, fontweight='bold', pad=15)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d. %b'))
        plt.xticks(rotation=45, color='#8899a6')
        plt.yticks(color='#8899a6')
        
        for spine in ax.spines.values():
            spine.set_color('#38444d')

        plt.tight_layout()
        plt.savefig(chart_path, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        
        print(f"✅ Grafik erfolgreich gespeichert unter: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ Fehler bei der Grafikerstellung: {e}")
        return None

# ==========================================
# FUNKTION 2: CROSSOVER DIAGRAMM (2 ACHSEN)
# ==========================================
def create_correlation_chart(df, title, label_1, label_2):
    """
    Erstellt ein Diagramm mit ZWEI Y-Achsen, um zwei Datensätze zu vergleichen.
    Erwartet einen DataFrame mit den Spalten 'timestamp', 'Wert1' und 'Wert2'.
    """
    print(f"🎨 Generiere Crossover-Grafik: {title}...")
    
    os.makedirs("output", exist_ok=True)
    chart_path = "output/correlation_chart.png"
    
    try:
        # 1. Basis-Setup
        if 'timestamp' in df.columns:
            df = df.set_index('timestamp')

        plt.style.use('dark_background')
        fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
        
        bg_color = '#15202b'
        fig.patch.set_facecolor(bg_color)
        ax1.set_facecolor(bg_color)
        ax1.grid(color='#38444d', linestyle='--', linewidth=0.5, alpha=0.7)

        # 2. ERSTE Y-ACHSE (Linke Seite, z.B. Bitcoin)
        color1 = '#1DA1F2' # Twitter-Blau
        ax1.set_ylabel(label_1, color=color1, fontweight='bold')
        line1 = ax1.plot(df.index, df['Wert1'], color=color1, linewidth=2.5, label=label_1)
        ax1.tick_params(axis='y', labelcolor=color1)

        # 3. ZWEITE Y-ACHSE (Rechte Seite, z.B. Zinsen)
        ax2 = ax1.twinx()  # Magie: Zweite Achse erstellen
        color2 = '#FFD700' # Gold
        ax2.set_ylabel(label_2, color=color2, fontweight='bold')
        line2 = ax2.plot(df.index, df['Wert2'], color=color2, linewidth=2.5, linestyle='-', label=label_2)
        ax2.tick_params(axis='y', labelcolor=color2)

        # 4. Design & Layout
        plt.title(title, color='white', fontsize=16, fontweight='bold', pad=15)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d. %b'))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, color='#8899a6')
        
        for spine in ax1.spines.values(): spine.set_color('#38444d')
        for spine in ax2.spines.values(): spine.set_color('#38444d')

        # 5. Legenden zusammenführen
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.15), 
                   ncol=2, facecolor=bg_color, edgecolor='#38444d', labelcolor='white')

        plt.tight_layout()
        plt.savefig(chart_path, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches="tight")
        plt.close()
        
        print(f"✅ Crossover-Grafik erfolgreich gespeichert unter: {chart_path}")
        return chart_path
        
    except Exception as e:
        print(f"❌ Fehler bei der Crossover-Grafikerstellung: {e}")
        return None
