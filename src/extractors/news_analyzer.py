import os
import requests

# NEU: Wir fügen den Parameter test_mode=False hinzu
def get_news_and_analyze(thema, language="de", test_mode=False):
    """
    Sucht aktuelle Nachrichten zum Thema und lässt die Groq KI den Grund erklären.
    Im test_mode werden keine echten APIs aufgerufen.
    """
    print(f"📰 Suche nach dem 'Warum' für das Thema: {thema}...")
    
    # 🛑 TEST-MODUS ABFANGEN
    if test_mode:
        print("🛠️ TEST-MODUS AKTIV: Überspringe GNews und Groq APIs, um Tokens zu sparen!")
        return "🛠️ [TEST-MODUS] Dies ist ein Platzhalter. Hier würde normalerweise die KI erklären, warum das Thema trendet."
    
    # --- Ab hier läuft der normale, echte API-Code ---
    gnews_key = os.getenv("GNEWS_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    
    if not gnews_key or not groq_key:
        print("⚠️ Warnung: GNews oder Groq API Keys fehlen. Überspringe News-Analyse.")
        return ""
        
    query = thema.replace('_', ' ')
    gnews_url = f"https://gnews.io/api/v4/search?q={query}&lang={language}&max=3&apikey={gnews_key}"
    
    try:
        news_response = requests.get(gnews_url, timeout=10)
        news_data = news_response.json()
        
        articles = news_data.get('articles', [])
        if not articles:
            print("ℹ️ Keine aktuellen Nachrichten zu diesem Thema gefunden.")
            return ""
            
        news_context = ""
        for i, article in enumerate(articles):
            news_context += f"{i+1}. {article['title']} - {article['description']}\n"
            
        print("🧠 Lasse Groq KI (Llama 3.1) die Nachrichten analysieren...")
        
        groq_url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json"
        }
        
        prompt = (
            f"Du bist ein Social Media Redakteur. Das Thema '{query}' trendet gerade extrem auf Wikipedia. "
            f"Hier sind die aktuellsten Schlagzeilen dazu:\n\n{news_context}\n\n"
            f"Fasse basierend auf diesen Schlagzeilen in maximal 2 kurzen, knackigen Sätzen zusammen, WARUM das Thema gerade trendet. "
            f"Schreibe es so, dass es direkt in einen Social Media Post passt (gerne mit 1 Emoji). "
            f"Antworte NUR mit den zwei Sätzen, ohne Einleitung, ohne Grußformel."
        )
        
        payload = {
            "model": "llama-3.1-8b-instant", # Dein aktualisiertes Modell!
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 150
        }
        
        groq_response = requests.post(groq_url, headers=headers, json=payload, timeout=15)
        
        if groq_response.status_code == 200:
            groq_data = groq_response.json()
            ai_text = groq_data['choices'][0]['message']['content'].strip()
            
            if ai_text.startswith('"') and ai_text.endswith('"'):
                ai_text = ai_text[1:-1]
                
            print(f"✅ KI-Analyse erfolgreich abgeschlossen.")
            return ai_text
        else:
            print(f"⚠️ Groq API Fehler: {groq_response.text}")
            return ""
            
    except Exception as e:
        print(f"⚠️ Fehler bei der News-Analyse: {e}")
        return ""
