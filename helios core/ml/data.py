import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.features import build_features, FEATURE_COLUMNS

def prepare_ml_data(df):
    """
    Prepare data for ML model training.

    Args:
        df: DataFrame with 'Hours' and 'Demand' columns

    Returns:
        X: Feature DataFrame
        y: Target Series
        df: DataFrame with added features
    """
    df = build_features(df)
    df = df.dropna()

    X = df[FEATURE_COLUMNS]
    y = df["Demand"]

    return X, y, df