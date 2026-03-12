import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # <-- Ny import for å fikse klokkeslett
import time
from datetime import datetime

# Sett opp siden
st.set_page_config(page_title="Promille-Kalkulator", layout="centered")
st.title("🍺 Øl-Logg & Promillemåler")

# Brukerinput i sidebar
with st.sidebar:
    vekt = st.number_input("Vekt (kg)", min_value=40, max_value=200, value=80)
    kjonn = st.selectbox("Kjønn", ["Mann", "Kvinne"])
    r = 0.68 if kjonn == "Mann" else 0.55

# Initialiser session state
if 'drikker' not in st.session_state:
    st.session_state.drikker = []

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Legg til en Øl (0.33l)"):
        st.session_state.drikker.append({'tid': time.time(), 'gram': 12})
with col2:
    if st.button("➕ Legg til en Stor Øl (0.5l)"):
        st.session_state.drikker.append({'tid': time.time(), 'gram': 18})

if st.session_state.drikker:
    start_tid = st.session_state.drikker[0]['tid']
    na_tid = time.time()
    
    total_gram = sum(d['gram'] for d in st.session_state.drikker)
    timer_gatt = (na_tid - start_tid) / 3600
    na_promille = max(0, (total_gram / (vekt * r)) - (0.15 * timer_gatt))
    
    st.metric("Estimert Promille Nå", f"{na_promille:.2f}")

    # Lag tidslinje (12 timer frem i tid fra start)
    tidslinje = [start_tid + i * 600 for i in range(72)] # Hvert 10. minutt i 12 timer
    promiller = []
    for t in tidslinje:
        gram_hittil = sum(d['gram'] for d in st.session_state.drikker if d['tid'] <= t)
        timer = (t - start_tid) / 3600
        p = max(0, (gram_hittil / (vekt * r)) - (0.15 * timer))
        promiller.append(p)
    
    tidsstempler = [datetime.fromtimestamp(t) for t in tidslinje]
    
    fig, ax = plt.subplots()
    ax.plot(tidsstempler, promiller, color='orange', linewidth=2, label="Promille")
    ax.fill_between(tidsstempler, promiller, color='orange', alpha=0.2)
    ax.axhline(y=0.2, color='red', linestyle='--', label="Kjøregrense (0.2)")
    
    # --- HER ER FIKSEN FOR TIDEN ---
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M')) # Viser kun Time:Minutt
    plt.xticks(rotation=45)
    # -------------------------------
    
    ax.set_ylabel("Promille")
    ax.set_ylim(0, max(promiller) + 0.5 if promiller else 2)
    ax.legend()
    ax.grid(True, alpha=0.2)
    
    st.pyplot(fig)

    if st.button("Nullstill alt"):
        st.session_state.drikker = []
        st.rerun()
else:
    st.info("Registrer din første øl for å se grafen!")
