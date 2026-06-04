# IU_Thesis_Meaningful-Human-Control

Technische Implementierung von 'Meaningful Human Control'-Mechanismen in LLM-gestützten Entscheidungssystemen zur Reduktion von Responsibility Gaps.

## Projektstruktur

Dieses Repository ist wie folgt modular aufgebaut:

- **`/backend`**: Die Schnittstelle zu unserer lokalen Ollama-Instanz zur Abfrage der LLM-Modelle.
- **`/middleware`**: Der Kern der Thesis. Hier wird die Guardrail-Logik implementiert, um Prompt-Manipulationen und Steuerungseingriffe durchzuführen.
- **`/frontend`**: Das Streamlit-basierte Benutzerinterface (UI), mit dem die Probanden interagieren.
- **`/data`**: Das Zielverzeichnis für alle generierten CSV- und JSON-Logs der Experimente.
- **`.gitignore`**: Schließt temporäre Dateien, Logdaten und die virtuelle Umgebung vom Repository aus.
- **`README.md`**: Dieses Dokument zur Übersicht und Dokumentation.

## Akademischer Kontext: Design Science Research (DSR)

Dieses Projekt ist das Kernartefakt meiner Thesis. Es untersucht das Konzept der **"Meaningful Human Control"** in LLM-gestützten Entscheidungssystemen. 
Das Ziel ist es, durch kognitive Guardrails (z.B. den Begründungszwang bei Entscheidungen) sogenannte "Responsibility Gaps" (Verantwortungslücken) zu reduzieren, die durch Automatisierung Bias und Blindes Vertrauen entstehen. Die gewonnenen Logging-Daten fließen direkt in die statistische ANOVA-Auswertung der Arbeit ein.

## Voraussetzungen

Um das Projekt auf einem fremden System zu starten, wird folgendes benötigt:
1. Eine laufende Instanz von **[Ollama](https://ollama.com/)**.
2. Das unzensierte Modell `dolphin-llama3` muss heruntergeladen sein:
   ```powershell
   ollama pull dolphin-llama3
   ```
3. Das Projekt bringt seine eigene portable Python-Umgebung im Verzeichnis `LocalPython` mit, es ist keine systemweite Python-Installation erforderlich.

## Experiment starten (Streamlit UI)

Das Benutzerinterface (Frontend) für die Probanden basiert auf Streamlit. Um die Anwendung zu starten, führen Sie im Wurzelverzeichnis des Projekts den folgenden Befehl aus:

```powershell
G:\VoramirGit\LocalPython\python.exe -m streamlit run frontend\app.py
```
Dies öffnet das Experiment im Standard-Webbrowser unter `http://localhost:8501`.
