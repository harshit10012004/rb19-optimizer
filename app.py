import gradio as gr
import sys
sys.path.append('src')
from physics_model import RB19Physics
from lap_simulation import simulate_miami
import numpy as np
import pandas as pd
from plotly import graph_objects as go
import plotly.utils
import json

rb19 = RB19Physics()

def analyze_setup(rake_mm, laps):
    """Main RB19 optimizer function"""
    # Physics calculation
    cd = rb19.drag_coefficient(rake_mm)
    gain = rb19.lap_time_gain(rake_mm)
    
    # Lap simulation
    baseline = simulate_miami(40, int(laps))
    fixed = simulate_miami(rake_mm, int(laps))
    
    # Results table
    df = pd.DataFrame({
        'Lap': range(1, int(laps)+1),
        'Baseline': baseline.round(2),
        'Optimized': fixed.round(2),
        'Gain': (baseline - fixed).round(2)
    })
    
    # Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Lap'], y=df['Baseline'], name='Baseline 40mm', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df['Lap'], y=df['Optimized'], name=f'Optimized {rake_mm}mm', line=dict(color='green')))
    fig.update_layout(
        title=f'RB19 Miami: {rake_mm}mm Rake vs Baseline',
        xaxis_title='Lap Number',
        yaxis_title='Lap Time (s)'
    )
    
    # JSON export
    setup = {
        "rake_mm": float(rake_mm),
        "cd": float(cd),
        "lap_gain": float(gain),
        "total_stint_gain": float((baseline - fixed).sum())
    }
    
    return df.to_html(), fig.to_html(), json.dumps(setup, indent=2)

# Gradio Interface
with gr.Blocks(title="Ì∂Å RB19 Lap Optimizer", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Ì∂Å RB19 Lap Optimizer")
    gr.Markdown("**Red Bull 2023 Floor Fix Physics: 40mm ‚Üí 35mm = 0.8s Miami gain**")
    
    with gr.Row():
        rake_slider = gr.Slider(30, 45, value=35, step=0.5, label="Rake Height (mm)")
        laps_slider = gr.Slider(5, 20, value=10, step=1, label="Race Laps")
    
    with gr.Row():
        table_output = gr.HTML()
        plot_output = gr.HTML()
        json_output = gr.JSON()
    
    analyze_btn = gr.Button("Ì¥¨ Optimize Setup", variant="primary", size="lg")
    
    analyze_btn.click(
        fn=analyze_setup,
        inputs=[rake_slider, laps_slider],
        outputs=[table_output, plot_output, json_output]
    )
    
    gr.Markdown("---")
    gr.Markdown("**Ì≥± Copy JSON ‚Üí iRacing setup file** | **Portfolio ready**")

if __name__ == "__main__":
    demo.launch()
