import pandas as pd
from scipy import stats
import os

# Pfad dynamisch bestimmen, damit das Skript von überall ausgeführt werden kann
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'data', 'experiment_results.csv')

# 1. Daten laden
df = pd.read_csv(csv_path, sep=';')

# 2. Datenbereinigung: Testläufe entfernen
df_clean = df[df['Proband_ID'] != 'UNKNOWN-PROBAND'].copy()

# Sicherstellen, dass Guardrail_Active als Boolean interpretiert wird
if df_clean['Guardrail_Active'].dtype == object:
    df_clean['Guardrail_Active'] = df_clean['Guardrail_Active'].astype(str).str.lower() == 'true'

# 3. Gruppen trennen
group_experiment = df_clean[df_clean['Guardrail_Active'] == True]['Time_Taken_Seconds']
group_control = df_clean[df_clean['Guardrail_Active'] == False]['Time_Taken_Seconds']

# 4. Deskriptive Statistik
mean_exp = group_experiment.mean()
mean_ctrl = group_control.mean()
n_exp = len(group_experiment)
n_ctrl = len(group_control)

print(f"--- Deskriptive Statistik ---")
print(f"Experimentalgruppe (Guardrail=True): n={n_exp}, Mittelwert = {mean_exp:.2f} s")
print(f"Kontrollgruppe (Guardrail=False): n={n_ctrl}, Mittelwert = {mean_ctrl:.2f} s")

# 5. Inferenzstatistik: Welch-Test (equal_var=False)
# Da H1 postuliert: mu_Experiment > mu_Kontrolle, nutzen wir alternative='greater'
if n_exp < 2 or n_ctrl < 2:
    print("\n[!] Nicht genug Daten (mindestens 2 pro Gruppe erforderlich), um den Welch-Test durchzuführen.")
else:
    t_stat, p_val = stats.ttest_ind(group_experiment, group_control, equal_var=False, alternative='greater')

    print(f"\n--- Inferenzstatistik (Welch-Test) ---")
    print(f"t-Statistik: {t_stat:.4f}")
    print(f"p-Wert (einseitig): {p_val:.4e}")

    # 6. Hypothesenentscheidung (Alpha = 0.05)
    if p_val < 0.05:
        print("\nErgebnis: H0 wird verworfen. Das Guardrail erhöht die Dwell Time signifikant.")
    else:
        print("\nErgebnis: H0 wird beibehalten. Kein signifikanter Effekt nachgewiesen.")
