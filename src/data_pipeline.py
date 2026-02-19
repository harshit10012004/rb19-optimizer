import fastf1
import pandas as pd
from pathlib import Path

def load_rb19_miami(year=2023, session_type='Q'):
    """Load Verstappen RB19 Miami Q3 laps (1:19.5 pole target)"""
    session = fastf1.get_session(year, 'Miami Grand Prix', session_type)
    session.load()
    
    # Verstappen RB19 only
    laps = session.laps.pick_driver('VER').pick_team('Red Bull')
    
    # Core telemetry columns
    columns = ['LapNumber', 'LapTime', 'TyreLife', 'Throttle', 
               'Brake', 'Speed', 'RPM']
    
    df = laps[columns].copy()
    df.to_csv('data/rb19_miami_q3.csv', index=False)
    
    print(f"✅ Loaded {len(df)} RB19 Miami laps")
    return df

if __name__ == "__main__":
    load_rb19_miami()
