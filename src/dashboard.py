import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import yaml
import sys
sys.path.append('src')
from data_pipeline import load_rb19_miami

# Page config (F1 aesthetic)
st.set_page_config(
    page_title="Ì∂Å RB19 Lap Optimizer",
    page_icon="ÌøÅ",
    layout="wide"
)

st.title("Ì∂Å RB19 Lap Optimizer")
st.markdown("**Validating Red Bull's 2023 flexi-floor fix: 0.8s/lap Miami gains**")

# Load RB19 specs
with open('data/rb19_specs.yaml', 'r') as f:
    specs = yaml.safe_load(f)

# Sidebar: Car/Track info
with st.sidebar:
    st.header("Ì≥ã RB19 Baseline")
    st.json(specs['car'])
    st.json(specs['track'])

# Main dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ì≥à RB19 Miami Q3 Telemetry")
    df = load_rb19_miami()
    st.dataframe(df.head(10), use_container_width=True)

with col2:
    st.subheader("Ì¥• Tire Degradation")
    fig_deg = px.scatter(df, x='LapNumber', y='LapTime', 
                        color='TyreLife',
                        title="RB19 Tire Wear Curve",
                        color_continuous_scale='RdYlBu_r')
    st.plotly_chart(fig_deg, use_container_width=True)

# Lap time delta analysis
st.subheader("‚è±Ô∏è Lap Time Analysis")
best_lap = df['LapTime'].min()
avg_lap = df['LapTime'].mean()
st.metric("Best Lap", best_lap)
st.metric("Avg Lap", avg_lap, delta=f"{avg_lap-best_lap:.3f}")

# Throttle trace (key for floor fix validation)
fig_throttle = px.line(df, x='LapNumber', y='Throttle',
                      title="RB19 Throttle Trace (Flexi-floor issues)")
st.plotly_chart(fig_throttle, use_container_width=True)

# Export button
st.download_button(
    label="Ì≥• Download RB19 Data",
    data=df.to_csv(index=False),
    file_name="rb19_miami_q3.csv",
    mime="text/csv"
)
