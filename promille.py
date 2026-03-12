import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def beregn_promille_ved_tid(vekt, kjonn, drikker, sjekk_tid, start_tid):
    """Beregner promille på et spesifikt tidspunkt."""
    r = 0.68 if kjonn == "m" else 0.55
    forbrenning_per_time = 0.15
    
    # Finn ut hvor mye alkohol som er drukket frem til sjekk_tid
    gram_drukket_hittil = sum(d['gram'] for d in drikker if d['tid'] <= sjekk_tid)
    
    if not gram_drukket_hittil:
        return 0.0
    
    timer_gatt = (sjekk_tid - start_tid) / 3600
    promille = (gram_drukket_hittil / (vekt * r)) - (forbrenning_per_time * timer_gatt)
    
    return max(0, promille)

def vis_graf(vekt, kjonn, drikker, start_tid):
    if not drikker:
        print("Ingen data å vise.")
        return

    na_tid = time.time()
    # Lag tidslinje fra start til 12 timer frem i tid for å se nedtrappingen
    tidslinje_sekunder = [start_tid + i * 300 for i in range(int((12 * 3600) / 300))]
    promille_verdier = [beregn_promille_ved_tid(vekt, kjonn, drikker, t, start_tid) for t in tidslinje_sekunder]
    
    tidsstempler = [datetime.fromtimestamp(t) for t in tidslinje_sekunder]
    
    plt.figure(figsize=(10, 5))
    plt.plot(tidsstempler, promille_verdier, label='Estimert Promille', color='orange', linewidth=2)
    plt.axhline(y=0.2, color='r', linestyle='--', label='Kjøregrense (0.2)')
    plt.axvline(x=datetime.fromtimestamp(na_tid), color='blue', linestyle=':', label='Nå')
    
    plt.title('Alkoholutvikling over tid')
    plt.xlabel('Klokkeslett')
    plt.ylabel('Promille')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.gcf().autofmt_xdate()
    
    print("Viser graf... (Lukk grafvinduet for å fortsette registrering)")
    plt.show()

def main():
    print("--- Øl-Logg med Graf ---")
    try:
        vekt = float(input("Oppgi vekt (kg): "))
        kjonn = input("Kjønn (m/k): ").lower()
    except ValueError:
        print("Feil inndata. Bruker standardverdier (80kg, mann).")
        vekt, kjonn = 80, "m"
    
    drikker = []
    start_tid = None
    
    print("\nKommandoer: 'øl' (0.33l), 'stor' (0.5l), 'graf', 'status', 'slutt'")
    
    while True:
        valg = input("\nHandling: ").lower()
        
        if valg in ['øl', 'stor']:
            na = time.time()
            if not drikker:
                start_tid = na
            
            gram = 12 if valg == 'øl' else 18
            drikker.append({'tid': na, 'gram': gram})
            
            p = beregn_promille_ved_tid(vekt, kjonn, drikker, na, start_tid)
            print(f"Registrert! Enheter: {len(drikker)}. Nåværende promille: {p:.2f}")
            
        elif valg == 'graf':
            vis_graf(vekt, kjonn, drikker, start_tid)
            
        elif valg == 'status':
            if not drikker:
                print("Ingen drikker registrert.")
                continue
            p = beregn_promille_ved_tid(vekt, kjonn, drikker, time.time(), start_tid)
            print(f"Status: {len(drikker)} enheter. Promille: {p:.2f}")
            
        elif valg == 'slutt':
            break

if __name__ == "__main__":
    main()
