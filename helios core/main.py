"""
Helios Energy Management System
================================
AI-powered energy optimization for solar + battery + grid systems.

This module simulates 24-hour energy flow with time-of-use pricing,
intelligent battery management, and export capabilities.

Author: VRD
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from datetime import datetime

# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

# Battery specifications
BATTERY_CAPACITY_KWH = 10.0      # Total capacity in kWh
BATTERY_MIN_SOC = 1.0            # Minimum state of charge (kWh)
BATTERY_MAX_SOC = 9.5            # Maximum state of charge (kWh)
BATTERY_CHARGE_RATE_MAX = 3.0    # Max charge rate (kW)
BATTERY_DISCHARGE_RATE_MAX = 3.0 # Max discharge rate (kW)
BATTERY_EFFICIENCY = 0.90        # Round-trip efficiency

# Grid & Export
GRID_EXPORT_LIMIT_KW = 5.0       # Max export to grid (kW)
EXPORT_TARIFF = 0.08             # $/kWh received for exports

# Time-of-Use Pricing ($/kWh)
# Peak: 17:00-22:00, Mid: 05:00-17:00, Off-peak: 22:00-05:00
TOU_RATES = {
    'off_peak': 0.12,  # 22:00 - 05:00
    'mid_peak': 0.18,  # 05:00 - 17:00
    'peak': 0.35       # 17:00 - 22:00
}

# Simulation settings
SIMULATION_HOURS = 24
RANDOM_SEED = 42


# =============================================================================
# DATA GENERATION
# =============================================================================

def generate_energy_data(hours: int = SIMULATION_HOURS) -> pd.DataFrame:
    """
    Generate realistic simulated energy data for the simulation period.

    Creates time-series data for:
    - Solar generation (sinusoidal, peaks at noon)
    - Energy demand (varies by time of day with morning/evening peaks)

    Args:
        hours: Number of hours to simulate

    Returns:
        DataFrame with columns: hour, solar_generation_kwh, demand_kwh
    """
    np.random.seed(RANDOM_SEED)

    # Time array
    hour_array = np.arange(hours)

    # Solar generation: bell curve centered at noon (hour 12)
    # Zero at night, peaks around 5-6 kW at midday
    solar_generation = np.maximum(
        0,
        6.0 * np.sin((hour_array - 6) * np.pi / 12)  # Peak at hour 12
    )
    # Add small variation for realism
    solar_generation += np.random.normal(0, 0.3, hours)
    solar_generation = np.clip(solar_generation, 0, None)

    # Energy demand: base load + morning peak + evening peak
    base_demand = 0.8  # Base load (kWh)

    # Morning peak (6-9 AM)
    morning_peak = 1.5 * np.exp(-((hour_array - 7.5) ** 2) / 4)

    # Evening peak (6-10 PM)
    evening_peak = 2.0 * np.exp(-((hour_array - 20) ** 2) / 6)

    # Daytime baseline (higher than night)
    daytime_baseline = 0.5 * ((np.sin((hour_array - 6) * np.pi / 12) + 1) / 2)

    demand_kwh = base_demand + morning_peak + evening_peak + daytime_baseline
    # Add realistic noise
    demand_kwh += np.random.normal(0, 0.2, hours)
    demand_kwh = np.clip(demand_kwh, 0.3, None)  # Minimum demand

    return pd.DataFrame({
        'hour': hour_array,
        'solar_generation_kwh': solar_generation,
        'demand_kwh': demand_kwh
    })


def get_tariff_rate(hour: int) -> float:
    """
    Get the time-of-use electricity rate for a given hour.

    Args:
        hour: Hour of day (0-23)

    Returns:
        Electricity rate in $/kWh
    """
    if 0 <= hour < 5 or 22 <= hour < 24:
        return TOU_RATES['off_peak']
    elif 5 <= hour < 17:
        return TOU_RATES['mid_peak']
    else:  # 17 <= hour < 22
        return TOU_RATES['peak']


# =============================================================================
# ENERGY OPTIMIZATION
# =============================================================================

def optimize_energy_flow(
    solar_kwh: float,
    demand_kwh: float,
    battery_soc: float,
    hour: int
) -> Dict[str, float]:
    """
    Optimize energy flow for a single time step.

    Priority order:
    1. Solar directly powers demand
    2. Excess solar charges battery
    3. Remaining excess exports to grid
    4. If solar insufficient, discharge battery
    5. Grid is last resort

    Args:
        solar_kwh: Solar energy available (kWh)
        demand_kwh: Energy demand (kWh)
        battery_soc: Current battery state of charge (kWh)
        hour: Current hour (for tariff calculation)

    Returns:
        Dictionary with energy flow values and new battery SOC
    """
    result = {
        'solar_used_direct': 0.0,
        'solar_to_battery': 0.0,
        'solar_exported': 0.0,
        'battery_discharged': 0.0,
        'grid_imported': 0.0,
        'battery_soc_new': battery_soc,
        'cost': 0.0,
        'export_revenue': 0.0
    }

    # Step 1: Use solar directly for demand
    solar_used_direct = min(solar_kwh, demand_kwh)
    result['solar_used_direct'] = solar_used_direct

    remaining_demand = demand_kwh - solar_used_direct
    remaining_solar = solar_kwh - solar_used_direct

    # Step 2: Charge battery with excess solar
    if remaining_solar > 0 and battery_soc < BATTERY_MAX_SOC:
        available_capacity = BATTERY_MAX_SOC - battery_soc
        charge_amount = min(
            remaining_solar,
            BATTERY_CHARGE_RATE_MAX,
            available_capacity / BATTERY_EFFICIENCY  # Account for charging losses
        )
        result['solar_to_battery'] = charge_amount
        result['battery_soc_new'] += charge_amount * BATTERY_EFFICIENCY
        remaining_solar -= charge_amount

    # Step 3: Export remaining solar to grid
    if remaining_solar > 0:
        export_amount = min(remaining_solar, GRID_EXPORT_LIMIT_KW)
        result['solar_exported'] = export_amount
        result['export_revenue'] = export_amount * EXPORT_TARIFF

    # Step 4: Use battery for remaining demand (especially during peak hours)
    tariff_rate = get_tariff_rate(hour)
    is_peak_hour = tariff_rate == TOU_RATES['peak']

    if remaining_demand > 0 and result['battery_soc_new'] > BATTERY_MIN_SOC:
        # More aggressive discharge during peak hours
        if is_peak_hour:
            discharge_limit = BATTERY_DISCHARGE_RATE_MAX
        else:
            discharge_limit = BATTERY_DISCHARGE_RATE_MAX * 0.5

        available_energy = result['battery_soc_new'] - BATTERY_MIN_SOC
        discharge_needed = remaining_demand / BATTERY_EFFICIENCY
        battery_discharged = min(discharge_needed, discharge_limit, available_energy)

        result['battery_discharged'] = battery_discharged
        result['battery_soc_new'] -= battery_discharged
        remaining_demand -= battery_discharged * BATTERY_EFFICIENCY

    # Step 5: Import from grid for any remaining demand
    if remaining_demand > 0:
        result['grid_imported'] = max(0, remaining_demand)
        result['cost'] = result['grid_imported'] * tariff_rate

    return result


# =============================================================================
# SIMULATION ENGINE
# =============================================================================

def run_simulation(
    data: Optional[pd.DataFrame] = None,
    verbose: bool = True
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Run the full energy optimization simulation.

    Processes each hour sequentially, tracking energy flows,
    costs, and battery state of charge.

    Args:
        data: Optional DataFrame with solar/demand data.
              If None, generates simulated data.
        verbose: Whether to print progress and summary

    Returns:
        Tuple of (results DataFrame, summary statistics dict)
    """
    # Generate or use provided data
    if data is None:
        data = generate_energy_data()

    # Initialize tracking arrays
    n_hours = len(data)

    results = {
        'hour': [],
        'solar_generation': [],
        'demand': [],
        'solar_used_direct': [],
        'solar_to_battery': [],
        'solar_exported': [],
        'battery_discharged': [],
        'grid_imported': [],
        'battery_soc': [],
        'hourly_cost': [],
        'hourly_revenue': [],
        'tariff_rate': []
    }

    # Initialize battery state
    battery_soc = BATTERY_CAPACITY_KWH * 0.5  # Start at 50%

    total_cost = 0.0
    total_revenue = 0.0

    if verbose:
        print("\n" + "=" * 60)
        print("HELIOS ENERGY OPTIMIZATION SIMULATION")
        print("=" * 60)
        print(f"Simulating {n_hours} hours...")

    # Process each hour
    for idx, row in data.iterrows():
        hour = int(row['hour'])
        solar = row['solar_generation_kwh']
        demand = row['demand_kwh']

        # Optimize energy flow for this hour
        flow = optimize_energy_flow(
            solar_kwh=solar,
            demand_kwh=demand,
            battery_soc=battery_soc,
            hour=hour
        )

        # Update battery state
        battery_soc = flow['battery_soc_new']

        # Accumulate costs/revenue
        total_cost += flow['cost']
        total_revenue += flow['export_revenue']

        # Record results
        results['hour'].append(hour)
        results['solar_generation'].append(solar)
        results['demand'].append(demand)
        results['solar_used_direct'].append(flow['solar_used_direct'])
        results['solar_to_battery'].append(flow['solar_to_battery'])
        results['solar_exported'].append(flow['solar_exported'])
        results['battery_discharged'].append(flow['battery_discharged'])
        results['grid_imported'].append(flow['grid_imported'])
        results['battery_soc'].append(battery_soc)
        results['hourly_cost'].append(flow['cost'])
        results['hourly_revenue'].append(flow['export_revenue'])
        results['tariff_rate'].append(get_tariff_rate(hour))

    # Create results DataFrame
    results_df = pd.DataFrame(results)

    # Calculate summary statistics
    summary = {
        'total_solar_generated': data['solar_generation_kwh'].sum(),
        'total_solar_used': results_df['solar_used_direct'].sum(),
        'total_solar_exported': results_df['solar_exported'].sum(),
        'total_battery_charged': results_df['solar_to_battery'].sum(),
        'total_battery_discharged': results_df['battery_discharged'].sum(),
        'total_grid_imported': results_df['grid_imported'].sum(),
        'total_demand': data['demand_kwh'].sum(),
        'total_energy_cost': total_cost,
        'total_export_revenue': total_revenue,
        'net_cost': total_cost - total_revenue,
        'solar_self_consumption_pct': (
            results_df['solar_used_direct'].sum() /
            data['solar_generation_kwh'].sum() * 100
        ) if data['solar_generation_kwh'].sum() > 0 else 0,
        'grid_independence_pct': (
            (results_df['solar_used_direct'].sum() +
             results_df['battery_discharged'].sum()) /
            data['demand_kwh'].sum() * 100
        ) if data['demand_kwh'].sum() > 0 else 0
    }

    if verbose:
        _print_summary(summary, results_df)

    return results_df, summary


def _print_summary(summary: Dict[str, float], results_df: pd.DataFrame) -> None:
    """Print a formatted summary of the simulation results."""

    print("\n" + "-" * 60)
    print("ENERGY SUMMARY")
    print("-" * 60)

    print(f"\nEnergy Generation & Consumption:")
    print(f"   Total Solar Generated:  {summary['total_solar_generated']:>8.2f} kWh")
    print(f"   Total Energy Demand:    {summary['total_demand']:>8.2f} kWh")

    print(f"\nSolar Energy Breakdown:")
    print(f"   Used Directly:          {summary['total_solar_used']:>8.2f} kWh")
    print(f"   Stored in Battery:      {summary['total_battery_charged']:>8.2f} kWh")
    print(f"   Exported to Grid:       {summary['total_solar_exported']:>8.2f} kWh")

    print(f"\nEnergy Sources for Demand:")
    print(f"   Solar (Direct):         {summary['total_solar_used']:>8.2f} kWh")
    print(f"   Battery (Discharged):   {summary['total_battery_discharged']:>8.2f} kWh")
    print(f"   Grid (Imported):        {summary['total_grid_imported']:>8.2f} kWh")

    print(f"\nCost Analysis:")
    print(f"   Grid Import Cost:       ${summary['total_energy_cost']:>8.2f}")
    print(f"   Export Revenue:         ${summary['total_export_revenue']:>8.2f}")
    print(f"   Net Cost:               ${summary['net_cost']:>8.2f}")

    print(f"\nEfficiency Metrics:")
    print(f"   Solar Self-Consumption: {summary['solar_self_consumption_pct']:>8.1f}%")
    print(f"   Grid Independence:      {summary['grid_independence_pct']:>8.1f}%")

    print("\n" + "=" * 60)
    print("Simulation completed successfully")
    print("=" * 60 + "\n")


# =============================================================================
# BASELINE COMPARISON
# =============================================================================

def run_baseline_simulation(data: Optional[pd.DataFrame] = None) -> Dict[str, float]:
    """
    Run a baseline simulation without optimization (grid-only).

    This represents a standard home without solar/battery system.

    Args:
        data: Optional DataFrame with demand data

    Returns:
        Summary statistics for baseline scenario
    """
    if data is None:
        data = generate_energy_data()

    total_cost = 0.0

    for _, row in data.iterrows():
        hour = int(row['hour'])
        demand = row['demand_kwh']
        tariff = get_tariff_rate(hour)
        total_cost += demand * tariff

    return {
        'total_demand': data['demand_kwh'].sum(),
        'total_grid_imported': data['demand_kwh'].sum(),
        'total_energy_cost': total_cost,
        'net_cost': total_cost
    }


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """
    Main entry point for the Helios Energy Management System.

    Runs the optimization simulation and compares against baseline.
    """
    print("\n" + "=" * 60)
    print("       HE LIOS  ENERGY  MANAGEMENT  SYSTEM")
    print("           AI-Powered Energy Optimization")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Run optimized simulation
    results_df, summary = run_simulation(verbose=True)

    # Run baseline (no solar/battery)
    print("\nRunning baseline comparison (grid-only scenario)...")
    baseline = run_baseline_simulation()

    # Compare results
    savings = baseline['net_cost'] - summary['net_cost']
    savings_pct = (savings / baseline['net_cost'] * 100) if baseline['net_cost'] > 0 else 0

    print("\n" + "-" * 60)
    print("COMPARISON: Helios vs Grid-Only")
    print("-" * 60)
    print(f"\n   Grid-Only Cost:      ${baseline['net_cost']:>8.2f}")
    print(f"   Helios Optimized:    ${summary['net_cost']:>8.2f}")
    print(f"   Total Savings:       ${savings:>8.2f} ({savings_pct:.1f}%)")
    print("\n" + "=" * 60)

    # Save results to CSV for further analysis
    results_df.to_csv('helios_simulation_results.csv', index=False)
    print(f"\nResults saved to: helios_simulation_results.csv")

    return results_df, summary, baseline


if __name__ == "__main__":
    main()
