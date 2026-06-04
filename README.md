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

## Setup und Installation

### Python-Umgebung
Es wird ein isoliertes virtuelles Python-Environment im Wurzelverzeichnis verwendet:
```bash
python -m venv .venv
```

Aktivierung unter Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```
