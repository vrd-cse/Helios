from data.database import load_data
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

df = load_data()

features = [
"solar_irradiance_wm2",
"temperature_c",
"cloud_cover",
"panel_efficiency",
"energy_demand_mw",
"battery_storage_mwh"
]

X = df[features]

y = df["solar_generation_mw"]

X_train,X_test,y_train,y_test = train_test_split(
X,y,test_size=0.2,random_state=42
)

model = RandomForestRegressor(n_estimators=100)

model.fit(X_train,y_train)

joblib.dump(model,"helios_model.pkl")

print("Helios model trained successfully")