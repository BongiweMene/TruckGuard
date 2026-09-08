import pandas as pd

from ai_service import predict_sensor_risk


# Load TruckGuard dataset
data = pd.read_csv(
    "data/truckguard_dataset.csv"
)


# Find an actual high-risk record
high_risk_data = data[
    data["risk"] == 1
]


# Take the first high-risk record
sample = high_risk_data.iloc[[0]]


# Send the sensor data to the AI service
result = predict_sensor_risk(sample)


print("\n==============================")
print("TRUCKGUARD HIGH-RISK TEST")
print("==============================")

print("\nActual Dataset Risk:")
print(sample["risk"].iloc[0])

print("\nAI Prediction:")
print(result["prediction"])

print("\nHigh-Risk Probability:")
print(
    f'{result["high_risk_probability"]:.2f}%'
)

print("\nRisk Level:")
print(result["risk_level"])

print("\nAI SERVICE TEST COMPLETE")