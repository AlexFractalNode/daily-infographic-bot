import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_trend_chart(df, topic, output_filename="output/trend_chart.png"):
    """Erstellt eine ansprechende Social-Media-Grafik aus den Wikipedia-Daten."""
    print("🎨 Generiere Grafik...")
    
    # Stelle sicher, dass der Output-Ordner existiert
    os.makedirs("output", exist_ok=True)
    
    # Styling Setup (Dark Mode für Social Media)
    plt.style.use('dark_background')
    
    # Figure erstellen (Hohe Auflösung, 16:9 Format)
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    
    # Hintergrundfarben anpassen (Ein modernes, dunkles Blaugrau)
    bg_color = '#1e1e2e'
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    # Daten plotten (Leuchtende Linie + gefüllte Fläche darunter)
    line_color = '#89b4fa' # Ein schönes Hellblau
    ax.plot(df.index, df['Aufrufe'], color=line_color, linewidth=2.5)
    ax.fill_between(df.index, df['Aufrufe'], color=line_color, alpha=0.2)
    
    # Grid und Achsen stylen
    ax.grid(color='#313244', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cdd6f4')
    ax.spines['bottom'].set_color('#cdd6f4')
    ax.tick_params(colors='#cdd6f4')
    
    # Titel und Labels (Thema aufräumen: Unterstriche zu Leerzeichen)
    topic_clean = topic.replace('_', ' ')
    plt.title(f'Wikipedia Trend: {topic_clean}', color='#cdd6f4', fontsize=18, fontweight='bold', pad=20)
    plt.suptitle('Tägliche Aufrufzahlen der letzten 30 Tage', color='#a6adc8', fontsize=12, y=0.92)
    plt.xlabel('')
    plt.ylabel('Aufrufe', color='#a6adc8')
    
    # Layout anpassen und speichern
    plt.tight_layout()
    plt.savefig(output_filename, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    
    print(f"✅ Grafik erfolgreich gespeichert unter: {output_filename}")
    return output_filename
