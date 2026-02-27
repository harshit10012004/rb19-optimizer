import json
from datetime import datetime

class IRacingSetup:
    def __init__(self, rake_mm, lap_gain, track="Miami"):
        self.rake_mm = rake_mm
        self.lap_gain = lap_gain
        self.track = track
        self.timestamp = datetime.now().strftime("%Y%m%d")
    
    def generate_sto(self):
        """Generate iRacing .sto format"""
        sto_content = f"""[HEADER]
VERSION 1
DATE {self.timestamp}
DRIVER RB19_Optimizer
SETUPNAME {self.track}_Q3_Rake{self.rake_mm}mm

[BASELINE]
RAKE_MM 40.0
CD_BASELINE 0.900
LAP_TIME 79.80s

[FLOOR_FIX]
RAKE_MM {self.rake_mm:.1f}
CD_FIXED 0.855
LAP_GAIN {self.lap_gain:.2f}s

[IRACING]
WING_FLAP 12.5
ARB_FRONT 8.2
ARB_REAR 6.8
"""
        return sto_content
    
    def generate_json(self):
        return {
            "rake_mm": self.rake_mm,
            "lap_gain": self.lap_gain,
            "track": self.track,
            "cd": 0.855,
            "stint_gain": self.lap_gain * 10
        }
