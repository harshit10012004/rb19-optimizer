import numpy as np

class RB19Physics:
    def __init__(self):
        self.baseline_rake = 40
        self.fixed_rake = 35
        
    def drag_coefficient(self, rake_mm):
        cd_baseline = 0.90
        rake_pct = (self.baseline_rake - rake_mm) / self.baseline_rake
        return cd_baseline * (1 - 0.05 * rake_pct)
    
    def lap_time_gain(self, rake_mm):
        cd = self.drag_coefficient(rake_mm)
        return 0.8 * (1 - cd / 0.90)
