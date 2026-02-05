import numpy as np
import matplotlib.pyplot as plt
battery_capacity = 100 #kWh
battery_SOC = 50 #kWh
grid_cost = np.zeros(24)
for t in range(24):
    if 18 <= t < 24:
        grid_cost[t] = 8
    else:
        grid_cost[t] = 4
total_cost = 0

hours = np.arange(24)

solar = np.maximum(0,50 * np.sin((hours - 6) * np.pi / 12))

demand = 30 + 10*np.sin((hours - 8) * np.pi/12) + 10

solar_used = np.zeros(24)
battery_used = np.zeros(24)
battery_charge = np.zeros(24)
grid_used = np.zeros(24)
soc = np.zeros(24)

baseline_cost = np.sum(demand * grid_cost)
print("Baseline Cost (Grid Only): ₹", round(baseline_cost, 2))


for t in range(24):
    # Use solar for demand first
    solar_used[t] = min(solar[t], demand[t])
    remaining_demand = demand[t] - solar_used[t]

    if remaining_demand > 0:
        # Discharge battery
        battery_used[t] = min(battery_SOC, remaining_demand)
        battery_SOC -= battery_used[t]
        grid_used[t] = remaining_demand - battery_used[t]
        total_cost += grid_used[t] * grid_cost[t]
    else:
        # Charge battery with excess solar
        excess_solar = solar[t] - demand[t]
        available_space = battery_capacity - battery_SOC
        battery_charge[t] = min(excess_solar, available_space)
        battery_SOC += battery_charge[t]

    soc[t] = battery_SOC

plt.figure(figsize=(10,5))
plt.plot(hours, solar_used, label="Solar Used")
plt.plot(hours, battery_used, label="Battery Used")
plt.plot(hours, grid_used, label="Grid Used")
plt.xlabel("Hour")
plt.ylabel("Energy (kWh)")
plt.legend()
plt.title("Helios Energy Source Usage")
plt.show()

plt.figure(figsize=(10,4))
plt.plot(hours, soc, label="Battery SoC")
plt.bar(hours, battery_charge, alpha=0.3, label="Battery Charging")
plt.xlabel("Hour")
plt.ylabel("Energy (kWh)")
plt.legend()
plt.title("Battery State of Charge")
plt.show()

print("Total Grid Energy Cost: ₹", round(total_cost, 2))


