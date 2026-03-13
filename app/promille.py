from flask import Flask, render_template, request, redirect, url_for, send_file
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import time
from datetime import datetime

app = Flask(__name__)

# Enkel database i minnet (forsvinner ved restart)
data = {
    'drikker': [],
    'vekt': 80,
    'kjonn': 'm'
}

def beregn_promille(sjekk_tid):
    if not data['drikker']:
        return 0.0
    
    r = 0.68 if data['kjonn'] == 'm' else 0.55
    start_tid = data['drikker'][0]['tid']
    
    total_gram = sum(d['gram'] for d in data['drikker'] if d['tid'] <= sjekk_tid)
    timer_gatt = (sjekk_tid - start_tid) / 3600
    
    promille = (total_gram / (data['vekt'] * r)) - (0.15 * timer_gatt)
    return max(0, promille)

@app.route('/')
def index():
    na_promille = beregn_promille(time.time())
    return f"""
    <h1>🍺 Promillemåler</h1>
    <p>Nåværende promille: <b>{na_promille:.2f}</b></p>
    <form action="/legg_til/12" method="post"><button>Drukket 0.33l (4.5%)</button></form>
    <form action="/legg_til/18" method="post"><button>Drukket 0.5l (4.5%)</button></form>
    <br>
    <img src="/graf.png?{time.time()}" style="max-width:100%">
    <br><br>
    <form action="/nullstill" method="post"><button>Nullstill alt</button></form>
    """

@app.route('/legg_til/<int:gram>', methods=['POST'])
def legg_til(gram):
    data['drikker'].append({'tid': time.time(), 'gram': gram})
    return redirect('/')

@app.route('/nullstill', methods=['POST'])
def nullstill():
    data['drikker'] = []
    return redirect('/')

@app.route('/graf.png')
def graf():
    if not data['drikker']:
        # Returner tom graf hvis ingen data
        plt.figure(figsize=(8, 4))
        plt.text(0.5, 0.5, 'Ingen data registrert ennå', ha='center')
    else:
        start_tid = data['drikker'][0]['tid']
        tidslinje = [start_tid + i * 900 for i in range(48)]
        promiller = [beregn_promille(t) for t in tidslinje]
        tidsstempler = [datetime.fromtimestamp(t) for t in tidslinje]
        
        plt.figure(figsize=(10, 5))
        plt.plot(tidsstempler, promiller, color='orange', linewidth=2)
        plt.fill_between(tidsstempler, promiller, color='orange', alpha=0.2)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        plt.grid(True, alpha=0.2)
        plt.ylabel("Promille")

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    # Intern løsning krever ofte port 8080 eller 5000
    app.run(host='0.0.0.0', port=8080)
