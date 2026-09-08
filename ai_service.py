import pandas as pd
import joblib
from pathlib import Path


# ============================================================
# TRUCKGUARD AI SERVICE
# ============================================================

# Location of the trained model
MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "truckguard_model.pkl"
)


# Exact 16 features used when training the model
FEATURE_COLUMNS = [
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


def load_model():
    """
    Load the trained TruckGuard Random Forest model.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "TruckGuard AI model was not found."
        )

    model = joblib.load(MODEL_PATH)

    return model


def predict_sensor_risk(sensor_data):
    """
    Predict risk using the trained Random Forest model.

    Parameters:
        sensor_data: pandas DataFrame containing
                     the 16 required sensor features.

    Returns:
        prediction
        high_risk_probability
        risk_level
    """

    # Make sure all required features exist
    missing_features = [
        feature
        for feature in FEATURE_COLUMNS
        if feature not in sensor_data.columns
    ]

    if missing_features:
        raise ValueError(
            f"Missing sensor features: {missing_features}"
        )

    # Select only the features used by the model
    input_data = sensor_data[FEATURE_COLUMNS]

    # Load trained model
    model = load_model()

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Get prediction probabilities
    probabilities = model.predict_proba(input_data)[0]

    # Find probability for class 1 (high risk)
    high_risk_probability = 0.0

    for index, class_value in enumerate(model.classes_):

        if class_value == 1:
            high_risk_probability = (
                probabilities[index] * 100
            )

    # Determine risk level
    if high_risk_probability < 40:

        risk_level = "LOW"

    elif high_risk_probability < 70:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    return {
        "prediction": int(prediction),
        "high_risk_probability": float(
            high_risk_probability
        ),
        "risk_level": risk_level
    }