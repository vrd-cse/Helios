"""
Helios Configuration Module
============================
Central configuration for all system parameters.

This module contains all constants and settings used across:
- Simulation engine (simulation/engines.py)
- ML pipeline (ml/*.py)
- Main orchestrator (main.py)
"""

import numpy as np

# =============================================================================
# BATTERY SPECIFICATIONS
# =============================================================================

BATTERY_CAPACITY = 10.0        # Total capacity in kWh
INITIAL_SOC = 5.0              # Initial state of charge in kWh (50%)
MIN_SOC = 1.0                  # Minimum state of charge in kWh
MAX_SOC = 9.5                  # Maximum state of charge in kWh (95% for longevity)
MAX_CHARGE_RATE = 3.0          # Maximum charge rate in kW
MAX_DISCHARGE_RATE = 3.0       # Maximum discharge rate in kW
EFFICIENCY = 0.90              # Round-trip efficiency (charge + discharge)
CYCLE_COST_PER_KWH = 0.10      # Battery degradation cost per kWh cycled

# =============================================================================
# GRID & EXPORT SETTINGS
# =============================================================================

GRID_EXPORT_LIMIT = 10.0       # Maximum export to grid in kW
EXPORT_PRICE = 3.0             # Price received for exports (₹/kWh or $/kWh)

# =============================================================================
# TIME-OF-USE TARIFF (₹/kWh or $/kWh)
# =============================================================================
# Returns array of 24 hourly rates
def get_tariff():
    """
    Generate time-of-use tariff array for 24 hours.

    Rate structure:
    - Off-peak (00:00-05:00, 22:00-24:00): 5
    - Mid-peak (05:00-17:00): 6
    - Peak (17:00-22:00): 9
    """
    tariff = np.zeros(24)
    for t in range(24):
        if 0 <= t < 5:
            tariff[t] = 5
        elif 5 <= t < 17:
            tariff[t] = 6
        elif 17 <= t < 22:
            tariff[t] = 9
        else:
            tariff[t] = 6
    return tariff


# =============================================================================
# SIMULATION SETTINGS
# =============================================================================

DAYS = 60                      # Number of days to simulate
TOTAL_HOURS = 24 * DAYS        # Total simulation hours (1440 for 60 days)
SIMULATION_HOURS = 24          # Default for standalone simulation
RANDOM_SEED = 42               # For reproducibility

# =============================================================================
# ML FEATURE COLUMNS
# =============================================================================

FEATURE_COLUMNS = [
    "Hour_of_Day",
    "Demand_lag_1",
    "Demand_lag_2",
    "Demand_lag_3",
    "Demand_roll3",
]

# =============================================================================
# PEAK DETECTION SETTINGS
# =============================================================================

PEAK_THRESHOLD = 5             # Demand increase threshold for peak detection (kW)
