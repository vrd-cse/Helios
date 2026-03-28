"""
Peak Demand Detection Module
=============================
Detects upcoming peak demand periods for battery discharge optimization.
"""


def detect_peak(predicted_demand: float, current_demand: float, threshold: float = 5.0) -> bool:
    """
    Detect if a peak demand period is expected.

    Args:
        predicted_demand: Predicted future demand value
        current_demand: Current demand value
        threshold: Minimum increase to consider as peak (kW)

    Returns:
        True if peak is expected, False otherwise
    """
    demand_increase = predicted_demand - current_demand
    return demand_increase > threshold