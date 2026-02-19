"""
RB19 Lap Optimizer - Red Bull 2023 flexi-floor fix simulator
"""
import fastf1
import os

# Enable persistent cache (speeds up 10x after first load)
fastf1.Cache.enable_cache('data/cache')
print("✅ FastF1 cache enabled: data/cache/")
