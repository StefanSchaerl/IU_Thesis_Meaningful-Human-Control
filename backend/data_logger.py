import os
import pandas as pd
from datetime import datetime

# Definierter Speicherort für die Experiment-Logs
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'experiment_results.csv')

def log_experiment_data(
    proband_id: str, 
    guardrail_active: bool, 
    force_error: bool, 
    decision: str, 
    rationale: str,
    time_taken_seconds: float
) -> None:
    """
    Speichert die Ergebnisse eines Durchlaufs sauber in einer CSV-Datei für die ANOVA-Auswertung.
    
    Args:
        proband_id (str): Die eindeutige Kennung des Probanden.
        guardrail_active (bool): Unabhängige Variable 1 - War das Guardrail aktiv?
        force_error (bool): Unabhängige Variable 2 - Hat die KI absichtlich falsch geantwortet?
        decision (str): Abhängige Variable - Die finale Entscheidung (AKZEPTIERT/ABGELEHNT).
        rationale (str): Die fachliche Begründung (Qualitative Auswertung).
        time_taken_seconds (float): Reaktionszeit in Sekunden (für Kovarianzanalysen).
    """
    # Neuen Datensatz erstellen
    new_data = {
        'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        'Proband_ID': [proband_id],
        'Guardrail_Active': [guardrail_active],
        'Force_Error': [force_error],
        'Decision': [decision],
        'Time_Taken_Seconds': [round(time_taken_seconds, 2)],
        'Rationale': [rationale.strip() if rationale else ""]
    }
    
    df_new = pd.DataFrame(new_data)
    
    # CSV anhängen oder neu erstellen, falls sie nicht existiert
    if not os.path.isfile(LOG_FILE_PATH):
        df_new.to_csv(LOG_FILE_PATH, index=False, sep=';', encoding='utf-8')
    else:
        df_new.to_csv(LOG_FILE_PATH, mode='a', header=False, index=False, sep=';', encoding='utf-8')
