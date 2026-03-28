"""
Energy Profile Generation Module
=================================
Generates realistic solar generation and energy demand profiles.
"""

import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import TOTAL_HOURS, RANDOM_SEED

np.random.seed(RANDOM_SEED)


def generate_profiles():
    """
    Generate 24-hour solar and demand profiles.

    Solar: Sinusoidal curve peaking at noon (hour 12)
    Demand: Base load with evening peak

    Returns:
        hours: Array of hour indices
        solar: Solar generation array (kWh)
        demand: Energy demand array (kWh)
    """
    hours = np.arange(TOTAL_HOURS)

    # Solar generation: peaks at midday, zero at night
    solar = np.maximum(0, 25 * np.sin((hours - 6) * np.pi / 12))

    # Demand: base + sinusoidal variation + noise
    demand = 20 + 10 * np.sin((hours - 18) * np.pi / 12) + 10 * np.random.rand(TOTAL_HOURS)

    return hours, solar, demand
