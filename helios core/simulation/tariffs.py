import numpy as np

def get_tariff():
    tariff = np.zeros(24)
    for t in range(24):
        if 0 <= t < 5:
            tariff[t % 24] = 5
        elif 5 <= t < 17:
            tariff[t % 24] = 6
        elif 17 <= t < 22:
            tariff[t % 24] = 9
        else:
            tariff[t % 24] = 6
    return tariff
