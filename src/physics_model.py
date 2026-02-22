import numpy as np
import yaml

class RB19Physics:
    def __init__(self):
        self.baseline_rake = 40  # mm - early 2023 porpoising
        self.fixed_rake = 35     # mm - mid-season fix
        
    def drag_coefficient(self, rake_mm):
        """Cd drops 5% with rake fix"""
        cd_baseline = 0.90
        rake_reduction = (self.baseline_rake - rake_mm) / self.baseline_rake
        cd_fixed = cd_baseline * (1 - 0.05 * rake_reduction)
        return cd_fixed
    
    def lap_time_gain(self, rake_mm):
        """0.8s Miami gain from rake fix"""
        cd = self.drag_coefficient(rake_mm)
        cd_improvement = 1 - cd / 0.90  # % drag reduction
        lap_gain_s = 0.8 * cd_improvement  # Scaled to Miami
        return lap_gain_s

# Test physics
if __name__ == "__main__":
    rb19 = RB19Physics()
    print(f"Baseline rake 40mm: Cd={rb19.drag_coefficient(40):.3f}")
    print(f"Fixed rake 35mm: Cd={rb19.drag_coefficient(35):.3f}")
    print(f"Miami lap gain: {rb19.lap_time_gain(35):.2f}s")
