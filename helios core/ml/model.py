import joblib
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from ml.data import prepare_ml_data
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "helios_model.pkl")
os.makedirs("ml", exist_ok=True)



def train_ml_model(df):
    X, y, df = prepare_ml_data(df)

    split_index = int(len(X) * 0.8)

    X_train = X[:split_index]
    X_test = X[split_index:]
    y_train = y[:split_index]
    y_test = y[split_index:]

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=None,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)

    # saving the trained model
    joblib.dump(model, MODEL_PATH)

    # print("Demand Forecast MAE:", round(mae, 3))

    # importance = pd.Series(
    #     model.feature_importances_,
    #     index=X.columns
    # )

    # print("\nFeature Importance:")
    # print(importance.sort_values(ascending=False))

    return model, mae

def load_trained_model():
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        return model
    else:
        return None