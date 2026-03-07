from ml.features import build_features, FEATURE_COLUMNS

def prepare_ml_data(df):
    df = build_features(df)
    df = df.dropna()
    

    X = df[FEATURE_COLUMNS]
    y = df["Demand"]
    
    return X, y, df