import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    INITIAL_SOC, BATTERY_CAPACITY, MIN_SOC, MAX_CHARGE_RATE,
    MAX_DISCHARGE_RATE, EFFICIENCY, CYCLE_COST_PER_KWH,
    GRID_EXPORT_LIMIT, EXPORT_PRICE, TOTAL_HOURS, PEAK_THRESHOLD,
    get_tariff
)
from simulation.profiles import generate_profiles
from ml.predictor import predict_next_demand
from ml.peak_detector import detect_peak


def run_simulation(model=None, verbose=False):
    """
    Run 60-day energy simulation with optional ML model.

    Args:
        model: Trained ML model for demand prediction (optional)
        verbose: Whether to print progress

    Returns:
        result: DataFrame with simulation results
        baseline_cost: Cost without optimization
        helios_cost: Cost with Helios optimization
    """
    hours, solar, demand = generate_profiles()
    tariff = get_tariff()

    if verbose:
        print(f"Running {len(hours)}-hour simulation...")

    soc = INITIAL_SOC
    soc_history = []

    solar_used = []
    battery_charged = []

    battery_used = []
    grid_used = []
    exported = []

    total_import_cost = 0
    total_export_revenue = 0
    total_battery_cycle_cost = 0

    for t in range(TOTAL_HOURS):
        available_solar =solar[t]
        predicted_demand = predict_next_demand(model, demand, t)
        peak_expected = detect_peak(predicted_demand, demand[t], PEAK_THRESHOLD)

        # solar to demand
        solar_to_demand = min(available_solar, demand[t])
        remaining_demand = demand[t] - solar_to_demand
        available_solar -= solar_to_demand

        # solar surplus
        solar_surplus = available_solar

        # charge battery from surplus solar
        battery_charge = 0
        if solar_surplus > 0 and soc < BATTERY_CAPACITY:
            available_capacity = (BATTERY_CAPACITY - soc)/EFFICIENCY
            charge_possible = min(solar_surplus, MAX_CHARGE_RATE, available_capacity)
            battery_charge = charge_possible
            soc += battery_charge * EFFICIENCY
            solar_surplus -= battery_charge

        # export remaining solar
        export = min(solar_surplus, GRID_EXPORT_LIMIT)

        # ---------------- Discharge Logic ----------------

        discharge = 0
        battery_to_load = 0

        if remaining_demand > 0 and soc > MIN_SOC :
            if peak_expected:
                discharge = min(
                    remaining_demand / EFFICIENCY,
                    MAX_DISCHARGE_RATE,
                    soc - MIN_SOC
                )
            else:
                # mild discharge during normal hours
                discharge = min(
                    remaining_demand / EFFICIENCY,
                    MAX_DISCHARGE_RATE * 0.5,
                    soc - MIN_SOC
                )

            battery_to_load = discharge * EFFICIENCY
            soc -= discharge
            remaining_demand -= battery_to_load
            total_battery_cycle_cost += discharge * CYCLE_COST_PER_KWH

        # grid usage
        grid = max(0, remaining_demand)

        # cost and revenue
        total_import_cost += grid*tariff[t % 24]
        total_export_revenue += export * EXPORT_PRICE

        # store history
        soc_history.append(soc)
        solar_used.append(solar_to_demand)
        battery_charged.append(battery_charge)
        battery_used.append(battery_to_load)
        grid_used.append(grid)
        exported.append(export)

    baseline_cost = 0
    for t in range(TOTAL_HOURS):
        baseline_cost += demand[t] * tariff[t % 24]

    helios_cost = total_import_cost - total_export_revenue + total_battery_cycle_cost

    result = pd.DataFrame({
        "Hours" :hours,
        "Solar" : solar,
        "Demand" : demand,
        "Solar_used": solar_used,
        "Battery_charged" : battery_charged,
        "Battery_Discharged" : battery_used,
        "Grid_used" : grid_used,
        "Exported" : exported,
        "SOC" : soc_history,
    })

    return result, baseline_cost, helios_cost

