import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "Hour_of_Day",
    "Demand_lag_1",
    "Demand_lag_2",
    "Demand_lag_3",
    "Demand_roll3",
]


def add_time_features(df):
    df["Hour_of_Day"] = df["Hours"] % 24
    return df

def add_lag_features(df):
    df["Demand_lag_1"] = df["Demand"].shift(1)
    df["Demand_lag_2"] = df["Demand"].shift(2)
    df["Demand_lag_3"] = df["Demand"].shift(3)
    return df

def add_rolling_features(df):
    df["Demand_roll3"] = df["Demand"].rolling(window=3).mean()
    return df

def build_features(df):
    df = df.copy()
    df = add_time_features(df)
    df = add_lag_features(df)
    df = add_rolling_features(df)
    return df
