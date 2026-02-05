import numpy as np
import matplotlib.pyplot as plt

evening_start = 18
moring_end = 8

battery_capacity = 100 #kWh
battery_SOC = 50 #kWh
max_charge_rate = 5 #kW
max_discharge_rate = 5 #kW

battery_soc_history = []
battery_charged = np.zeros(24)
battery_used = np.zeros(24)
grid_used = np.zeros(24)
solar_used = np.zeros(24)

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
    solar_available = solar[t]
    remaining_demand = demand[t]

    solar_used[t] = min(solar_available, remaining_demand) 
    remaining_demand -= solar_used[t]
    solar_available -= solar_used[t]

    # charge battery if battery is surplus exists
    if solar_available > 0 and battery_SOC < battery_capacity:
        charge = min(solar_available, max_charge_rate, battery_capacity - battery_SOC)
        battery_SOC += charge
        battery_charged[t] = charge
        solar_available -= charge

    # decide if battery can be used 
    if (t >= 18 or t <= 8) and battery_SOC> 0:
        discharge = min(
            remaining_demand,
            battery_SOC,
            max_discharge_rate
        )
        battery_used[t] = discharge
        battery_SOC -= discharge
        remaining_demand -= discharge
    # grid supplies remaining demand
    grid_used[t] = remaining_demand

    battery_soc_history.append(battery_SOC)

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


