import pandas as pd
import numpy as np
from ml.features import FEATURE_COLUMNS

def predict_next_demand(model, demand, t):

    if model is None or t < 3:
        return demand[t]

    row = {
        "Hour_of_Day": t % 24,
        "Demand_lag_1": demand[t-1],
        "Demand_lag_2": demand[t-2],
        "Demand_lag_3": demand[t-3],
        "Demand_roll3": np.mean(demand[t-3:t])
    }

    features = pd.DataFrame([row])[FEATURE_COLUMNS]

    return model.predict(features)[0]