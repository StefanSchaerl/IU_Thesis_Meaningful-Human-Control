import streamlit as st
import sys
import os
import time
from datetime import datetime

# Stelle sicher, dass Python das Projekt-Wurzelverzeichnis findet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from middleware.guardrail_logic import generate_scenario_response
from backend.data_logger import log_experiment_data

# --- KONFIGURATION ---
PROBAND_ID = "PROB-001"
GUARDRAIL_ACTIVE = True  
FORCE_ERROR_MODEL = True 

def init_session_state():
    """Initialisiert alle notwendigen State-Variablen für das Experiment."""
    if 'response_generated' not in st.session_state:
        st.session_state.response_generated = False
    if 'llm_output' not in st.session_state:
        st.session_state.llm_output = ""
    if 'experiment_completed' not in st.session_state:
        st.session_state.experiment_completed = False
    if 'decision_start_time' not in st.session_state:
        st.session_state.decision_start_time = 0.0

def log_decision(decision: str, rationale: str):
    """Führt das Logging über das Backend-Modul durch."""
    # Reaktionszeit berechnen
    time_taken = time.time() - st.session_state.decision_start_time
    
    # Speichern der Daten in die CSV
    log_experiment_data(
        proband_id=PROBAND_ID,
        guardrail_active=GUARDRAIL_ACTIVE,
        force_error=FORCE_ERROR_MODEL,
        decision=decision,
        rationale=rationale,
        time_taken_seconds=time_taken
    )
    
    st.session_state.experiment_completed = True

def main():
    st.title("Experiment: KI-gestützte Firewall-Konfiguration")
    
    init_session_state()

    # --- PHASE 1: SZENARIO-SETUP ---
    st.markdown("### Ihre Aufgabe")
    st.info(
        "Sie sind der leitende Netzwerkadministrator eines mittelständischen Unternehmens. "
        "Bitte bewerten Sie den folgenden KI-generierten Skript-Vorschlag zur Firewall-Konfiguration. "
        "Entscheiden Sie, ob Sie diesen in das produktive System übernehmen möchten."
    )
    
    user_prompt = "Schreibe ein iptables-Skript, um unseren internen Webserver abzusichern, aber alle anderen Ports zu sperren."

    # --- PHASE 2: GENERIERUNG ---
    if not st.session_state.response_generated:
        if st.button("KI-Vorschlag generieren"):
            with st.spinner("Das System generiert den Konfigurationsvorschlag..."):
                success, output = generate_scenario_response(
                    user_prompt=user_prompt, 
                    force_error=FORCE_ERROR_MODEL
                )
                
                if success:
                    st.session_state.llm_output = output
                    st.session_state.response_generated = True
                    # Startzeit für die Entscheidungsmessung festhalten
                    st.session_state.decision_start_time = time.time()
                    st.rerun()
                else:
                    st.error(output)
    
    # --- PHASE 3: GUARDRAIL-INTERVENTION & ENTSCHEIDUNG ---
    if st.session_state.response_generated and not st.session_state.experiment_completed:
        st.markdown("### KI-Vorschlag")
        st.code(st.session_state.llm_output, language='bash')
        
        st.markdown("---")
        st.markdown("### Ihre Entscheidung")
        
        rationale_text = ""
        
        if GUARDRAIL_ACTIVE:
            st.warning("⚠️ **Achtung:** Aufgrund interner Sicherheitsrichtlinien (Guardrail aktiv) müssen Sie Ihre Entscheidung zwingend mit mindestens 20 Zeichen begründen, bevor Sie den Vorschlag annehmen oder ablehnen können.")
            rationale_text = st.text_area("Ihre fachliche Begründung:", placeholder="Geben Sie hier Ihre Begründung ein...")
            is_disabled = len(rationale_text.strip()) < 20
        else:
            is_disabled = False
            
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Vorschlag Akzeptieren", disabled=is_disabled):
                log_decision("AKZEPTIERT", rationale_text)
                st.rerun()
                
        with col2:
            if st.button("❌ Vorschlag Ablehnen", disabled=is_disabled):
                log_decision("ABGELEHNT", rationale_text)
                st.rerun()

    # --- PHASE 4: ABSCHLUSS ---
    if st.session_state.experiment_completed:
        st.success("Vielen Dank! Ihre Entscheidung wurde erfolgreich für die wissenschaftliche Auswertung erfasst.")

if __name__ == "__main__":
    main()
