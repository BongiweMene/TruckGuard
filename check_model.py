import pandas as pd
import joblib

# Load dataset
data = pd.read_csv("data/truckguard_dataset.csv")

# Load model
model = joblib.load("models/truckguard_model.pkl")

# The exact 16 features used by the model
features = [
    "accel_x",
    "accel_y",
    "accel_z",
    "linear_x",
    "linear_y",
    "linear_z",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "mag_x",
    "mag_y",
    "mag_z",
    "acceleration_magnitude",
    "linear_acceleration_magnitude",
    "gyro_magnitude",
    "magnetic_magnitude"
]

# Prepare input
X = data[features]

# Predictions
predictions = model.predict(X)

# Add predictions to a copy
results = data[["event", "risk"]].copy()
results["prediction"] = predictions

print("\n==============================")
print("TRUCKGUARD AI MODEL TEST")
print("==============================")

print("\nDataset rows:", len(data))

print("\nActual risk distribution:")
print(data["risk"].value_counts())

print("\nAI prediction distribution:")
print(pd.Series(predictions).value_counts())

print("\nActual vs AI prediction:")
print(
    pd.crosstab(
        results["risk"],
        results["prediction"],
        rownames=["Actual"],
        colnames=["AI Prediction"]
    )
)

print("\nSample predictions:")
print(results.head(20))