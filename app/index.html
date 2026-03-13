<!DOCTYPE html>
<html lang="no">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Promille-kalkulator</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; background: #f4f4f4; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 500px; margin: auto; }
        button { padding: 10px 20px; margin: 5px; cursor: pointer; border: none; border-radius: 5px; background: #f39c12; color: white; font-weight: bold; }
        .reset { background: #e74c3c; margin-top: 20px; }
        #promille-verdi { font-size: 48px; color: #2c3e50; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🍺 Øl-Logg</h1>
        <p>Din estimerte promille er:</p>
        <div id="promille-verdi">0.00</div>
        
        <button onclick="leggTilDrikke(12)">Liten øl (0.33l)</button>
        <button onclick="leggTilDrikke(18)">Stor øl (0.5l)</button>
        
        <canvas id="promilleChart" style="margin-top:20px;"></canvas>
        
        <button class="reset" onclick="nullstill()">Nullstill alt</button>
    </div>

    <script>
        let drikker = JSON.parse(localStorage.getItem('drikker')) || [];
        const vekt = 80; // Standard
        const r = 0.68;  // Standard mann
        let chart;

        function leggTilDrikke(gram) {
            drikker.push({ tid: Date.now(), gram: gram });
            lagreOgOppdater();
        }

        function nullstill() {
            drikker = [];
            lagreOgOppdater();
        }

        function lagreOgOppdater() {
            localStorage.setItem('drikker', JSON.stringify(drikker));
            oppdaterVisning();
        }

        function beregnPromille(sjekkTid) {
            if (drikker.length === 0) return 0;
            const startTid = drikker[0].tid;
            const totalGram = drikker.filter(d => d.tid <= sjekkTid).reduce((sum, d) => sum + d.gram, 0);
            const timerGatt = (sjekkTid - startTid) / 3600000;
            const p = (totalGram / (vekt * r)) - (0.15 * timerGatt);
            return Math.max(0, p);
        }

        function oppdaterVisning() {
            const na = Date.now();
            document.getElementById('promille-verdi').innerText = beregnPromille(na).toFixed(2);
            oppdaterGraf();
        }

        function oppdaterGraf() {
            const ctx = document.getElementById('promilleChart').getContext('2d');
            const start = drikker.length > 0 ? drikker[0].tid : Date.now();
            const labels = [];
            const data = [];

            for (let i = 0; i < 48; i++) {
                const t = start + (i * 15 * 60000);
                labels.push(new Date(t).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}));
                data.push(beregnPromille(t));
            }

            if (chart) chart.destroy();
            chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{ label: 'Promille', data: data, borderColor: 'orange', fill: true }]
                },
                options: { scales: { y: { beginAtZero: true } } }
            });
        }

        setInterval(oppdaterVisning, 60000);
        oppdaterVisning();
    </script>
</body>
</html>
