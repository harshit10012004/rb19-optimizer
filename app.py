import gradio as gr
import sys
sys.path.append('src')
from physics_model import RB19Physics
import numpy as np
import pandas as pd

rb19 = RB19Physics()

def optimize_setup(rake_mm, laps):
    """RB19 rake optimizer"""
    cd = rb19.drag_coefficient(rake_mm)
    gain = rb19.lap_time_gain(rake_mm)
    
    # Simple simulation
    baseline = 79.8 * np.array([1 + 0.005*i for i in range(1, int(laps)+1)])
    optimized = (79.8 - gain) * np.array([1 + 0.004*i for i in range(1, int(laps)+1)])
    
    df = pd.DataFrame({
        'Lap': range(1, int(laps)+1),
        'Baseline': baseline.round(2),
        'Optimized': optimized.round(2),
        'Gain': (baseline - optimized).round(2)
    }).to_html(index=False)
    
    total_gain = (baseline - optimized).sum()
    
    return (
        df,
        f"**🎯 RESULTS**<br/>"
        f"Rake: **{rake_mm}mm**<br/>"
        f"Drag Coeff: **{cd:.3f}** (was 0.900)<br/>"
        f"Lap Gain: **{gain:.2f}s**<br/>"
        f"Stint Gain: **{total_gain:.1f}s** ({laps} laps)<br/><br/>"
        f"**📱 Copy for iRacing:**<br/>"
        f"`rake_mm: {rake_mm}, cd: {cd:.3f}, gain: {gain:.2f}s`"
    )

# Gradio Interface
with gr.Blocks(title="🦁 RB19 Lap Optimizer") as demo:
    gr.Markdown("# 🦁 RB19 Lap Optimizer")
    gr.Markdown("**Red Bull 2023 Floor Fix: 40mm → 35mm = 0.8s Miami gain**")
    
    with gr.Row():
        rake = gr.Slider(30, 45, value=35, step=0.5, label="Rake Height (mm)")
        laps_input = gr.Slider(5, 20, value=10, step=1, label="Race Laps")
    
    with gr.Row():
        table = gr.HTML()
        metrics = gr.Markdown()
    
    gr.Button("🔬 OPTIMIZE SETUP", size="lg").click(
        optimize_setup, 
        inputs=[rake, laps_input], 
        outputs=[table, metrics]
    )
    
    gr.Markdown("**🏆 Portfolio ready | FSAE teams: Setup optimizer LIVE**")

if __name__ == "__main__":
    demo.launch()
