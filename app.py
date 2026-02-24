import modal
import sys
sys.path.append("src")
from physics_model import RB19Physics
import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# Define Modal App
app = modal.App("rb19-optimizer")
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "fastapi==0.115.0",
    "uvicorn[standard]==0.30.6",
    "pandas==2.2.3",
    "numpy==1.26.4",
    "fastf1==3.8.1"
)

rb19 = RB19Physics()

# FastAPI web server
web_app = FastAPI()

@web_app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🦁 RB19 Lap Optimizer</title>
        <style>
            body { font-family: Arial; max-width: 1000px; margin: 50px auto; padding: 20px; }
            .container { display: flex; gap: 20px; }
            .controls { flex: 1; }
            .results { flex: 2; border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
            table { width: 100%; border-collapse: collapse; }
            th, td { padding: 8px; text-align: left; border-bottom: 1px solid #eee; }
            th { background: #f5f5f5; }
            button { background: #ff4444; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; }
            button:hover { background: #cc3333; }
            .metric { font-size: 24px; font-weight: bold; color: #ff4444; }
        </style>
    </head>
    <body>
        <h1>🦁 RB19 Lap Optimizer</h1>
        <p><strong>Red Bull 2023 Floor Fix Physics</strong> | 40mm → 35mm = <strong>0.8s Miami gain</strong></p>
        
        <div class="container">
            <div class="controls">
                <label>Rake Height (mm): <span id="rake-val">35</span></label><br>
                <input type="range" id="rake" min="30" max="45" value="35" step="0.5">
                <br><br>
                <label>Race Laps: <span id="laps-val">10</span></label><br>
                <input type="range" id="laps" min="5" max="20" value="10" step="1">
                <br><br>
                <button onclick="optimize()">🔬 OPTIMIZE SETUP</button>
            </div>
            <div class="results">
                <div id="metrics"></div>
                <table id="results">
                    <thead><tr><th>Lap</th><th>Baseline</th><th>Optimized</th><th>Gain</th></tr></thead>
                    <tbody></tbody>
                </table>
            </div>
        </div>

        <script>
        async function optimize() {
            const rake = document.getElementById('rake').value;
            const laps = document.getElementById('laps').value;
            
            const response = await fetch(`/optimize?rake=${rake}&laps=${laps}`);
            const data = await response.json();
            
            document.getElementById('rake-val').textContent = rake;
            document.getElementById('laps-val').textContent = laps;
            
            document.getElementById('metrics').innerHTML = 
                `<strong>Results:</strong><br>
                 Rake: <span class="metric">${rake}mm</span><br>
                 Lap Gain: <span class="metric">${data.lap_gain.toFixed(2)}s</span><br>
                 Stint Gain: <span class="metric">${data.stint_gain.toFixed(1)}s</span>`;
            
            let tbody = '';
            data.laps.forEach((row, i) => {
                tbody += `<tr>
                    <td>${row.lap}</td>
                    <td>${row.baseline.toFixed(2)}s</td>
                    <td>${row.optimized.toFixed(2)}s</td>
                    <td style="color: green">${row.gain.toFixed(2)}s</td>
                </tr>`;
            });
            document.getElementById('results').querySelector('tbody').innerHTML = tbody;
        }
        
        document.getElementById('rake').oninput = () => document.getElementById('rake-val').textContent = document.getElementById('rake').value;
        document.getElementById('laps').oninput = () => document.getElementById('laps-val').textContent = document.getElementById('laps').value;
        </script>
    </body>
    </html>
    """

@web_app.get("/optimize")
async def optimize(rake: float, laps: int):
    cd = rb19.drag_coefficient(rake)
    gain = rb19.lap_time_gain(rake)
    
    baseline = 79.8 * np.array([1 + 0.005*i for i in range(1, laps+1)])
    optimized = (79.8 - gain) * np.array([1 + 0.004*i for i in range(1, laps+1)])
    
    lap_data = []
    for i in range(laps):
        lap_data.append({
            "lap": i+1,
            "baseline": float(baseline[i]),
            "optimized": float(optimized[i]),
            "gain": float(baseline[i] - optimized[i])
        })
    
    return {
        "rake": rake,
        "cd": float(cd),
        "lap_gain": float(gain),
        "stint_gain": float((baseline - optimized).sum()),
        "laps": lap_data
    }

@app.function(image=image, timeout=60)
@modal.asgi_app()
def fastapi_app():
    return web_app
