""" Helios Energy Management System
    Author : VRD
    objective :Stimulate 24 hour solar + battery + grid interaction
    with time of use pricing and export capabilities.
"""

from simulation.engines import run_simulation
from ml.model import train_ml_model , load_trained_model
from data.database import load_data, create_table, save_results
import matplotlib.pyplot as plt
import os 
os.makedirs("plot" , exist_ok=True)


create_table()

if __name__ == "__main__":
    print("\n========== HELIOS ENERGY REPORT ==========")

    df = load_data()

    model = load_trained_model()

# Train model only if it does not exist and enough data is available
    if model is None and len(df) > 100:
        model, mae = train_ml_model(df)
    if model:
        print("AI Model Loaded ✓")
    else:
        print("Running Rule-Based Optimization")

    # Rule based
    results, baseline, cost = run_simulation()
    print(f"Baseline Energy Cost (Without AI): ₹{round(cost,2)}")
    save_results(results)
    print("\nRunning energy optimization...")

    # ML simulation
    results_ml, baseline_ml, cost_ml = run_simulation(model)
    print(f"Optimized Energy Cost (Helios AI): ₹{round(cost_ml,2)}")
    print(f"Total Savings Today: ₹{round(cost - cost_ml,2)}")
    save_results(results_ml)
    solar_used = results_ml["Solar_used"].sum()
    battery_used = results_ml["Battery_Discharged"].sum()
    grid_used = results_ml["Grid_used"].sum()

    print("\nEnergy Usage Summary")
    print("----------------------")
    print(f"Solar Energy Used   : {round(solar_used,2)} kWh")
    print(f"Battery Energy Used : {round(battery_used,2)} kWh")
    print(f"Grid Energy Used    : {round(grid_used,2)} kWh")

    print("\nSystem Status: Energy optimized successfully")
    print("=============================================")


    results_ml.to_csv("helios_simulation_results.csv", index=False)
    subset = results_ml[results_ml["Hours"] < 48]
    subset.plot(x="Hours", y=["Solar", "Demand"] , figsize=(10,5))
    plt.title("Solar vs Demand (First 48 Hours)")
    plt.grid(True)
    plt.savefig("plots/solar_vs_demand.png")
    plt.close()
    subset.plot(x="Hours", y=["Grid_used", "Battery_Discharged", "Solar_used"] , figsize=(10,5))
    plt.title("Energy Allocation")
    plt.savefig("plots/energy_allocation.png")
    plt.grid(True)
    plt.close()
    subset.plot(x="Hours", y="SOC" , figsize=(10,5))
    plt.title("Battery SOC")
    plt.savefig("plots/battery_soc.png")
    plt.grid(True)
    plt.close()

