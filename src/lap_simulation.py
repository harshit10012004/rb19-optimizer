import numpy as np
from physics_model import RB19Physics

def simulate_miami(rake_mm=40, laps=10):
    """Miami Q3 simulation - 5.412km, 19 corners"""
    rb19 = RB19Physics()
    baseline = 79.8  # Verstappen pole 1:19.8
    
    lap_times = []
    for lap in range(1, laps+1):
        cd = rb19.drag_coefficient(rake_mm)
        tyre_deg = 1 + 0.005 * lap  # 0.5% deg/lap
        lap_time = baseline * tyre_deg * (cd / 0.85)
        lap_times.append(lap_time)
    
    return np.array(lap_times)

if __name__ == "__main__":
    print("BASELINE (40mm rake):")
    base = simulate_miami(40, 10)
    print(f"Lap 1: {base[0]:.2f}s, Lap 10: {base[9]:.2f}s")
    
    print("\nFIXED (35mm rake):")
    fixed = simulate_miami(35, 10)
    print(f"Lap 1: {fixed[0]:.2f}s, Lap 10: {fixed[9]:.2f}s")
    
    gain = base - fixed
    print(f"\nAverage gain: {np.mean(gain):.2f}s per lap")
