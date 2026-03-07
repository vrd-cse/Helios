import numpy as np

def detect_peak(predicted_demand, current_demand, threshold=5):
    """
    Detect if peak demand is coming
    """

    demand_increase = predicted_demand - current_demand

    if demand_increase > threshold:
        return True
    else:
        return False