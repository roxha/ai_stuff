import streamlit as st
import matplotlib.pyplot as plt
import time
from datetime import datetime, timedelta

# Sett opp siden
st.set_page_config(page_title="Promille-Kalkulator", layout="centered")
st.title("🍺 Øl-Logg & Promillemåler")

# Brukerinput i sidebar
with st.sidebar:
    vekt = st.number_input("Vekt (kg)", min_value=40, max_value=200, value=80)
    kjonn = st.selectbox("Kjønn", ["Mann", "Kvinne"])
    r = 0.68 if kjonn == "Mann" else 0.55

# Initialiser session state for å lagre drikker
if 'drikker' not in st.session_state:
    st.session_state.drikker = []

# Knapper for å legge til drikke
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
    
    # Beregn nåværende promille
    total_gram = sum(d['gram'] for d in st.session_state.drikker)
    timer_gatt = (na_tid - start_tid) / 3600
    na_promille = max(0, (total_gram / (vekt * r)) - (0.15 * timer_gatt))
    
    st.metric("Estimert Promille Nå", f"{na_promille:.2f}")

    # Lag graf
    tidslinje = [start_tid + i * 900 for i in range(48)] # 12 timer frem
    promiller = []
    for t in tidslinje:
        gram_hittil = sum(d['gram'] for d in st.session_state.drikker if d['tid'] <= t)
        timer = (t - start_tid) / 3600
        p = max(0, (gram_hittil / (vekt * r)) - (0.15 * timer))
        promiller.append(p)
    
    tidsstempler = [datetime.fromtimestamp(t) for t in tidslinje]
    
    fig, ax = plt.subplots()
    ax.plot(tidsstempler, promiller, color='orange', label="Promille")
    ax.axhline(y=0.2, color='red', linestyle='--', label="Kjøregrense")
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

    if st.button("Nullstill alt"):
        st.session_state.drikker = []
        st.rerun()
else:
    st.info("Trykk på knappene over for å registrere din første øl!")
