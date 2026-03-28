"""
ML Predictor Module
====================
Runtime demand prediction using trained ML model.
"""

import pandas as pd
import numpy as np

# Import feature columns from sibling module
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml.features import FEATURE_COLUMNS


def predict_next_demand(model, demand: list, t: int) -> float:
    """
    Predict next demand value using ML model.

    Args:
        model: Trained sklearn model (or None for fallback)
        demand: List of historical demand values
        t: Current time index

    Returns:
        Predicted demand value
    """
    # Fallback to actual demand if no model or insufficient history
    if model is None or t < 3:
        return demand[t]

    # Build feature row
    row = {
        "Hour_of_Day": t % 24,
        "Demand_lag_1": demand[t-1],
        "Demand_lag_2": demand[t-2],
        "Demand_lag_3": demand[t-3],
        "Demand_roll3": np.mean(demand[t-3:t])
    }

    # Create DataFrame and predict
    features = pd.DataFrame([row])[FEATURE_COLUMNS]

    return model.predict(features)[0]