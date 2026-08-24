import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
import joblib


# ==========================================
# TRUCKGUARD AI - MODEL TRAINING
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "truckguard_dataset.csv"
)

MODEL_DIR = BASE_DIR / "models"

MODEL_FILE = MODEL_DIR / "truckguard_model.pkl"


print("=" * 60)
print("TRUCKGUARD AI MODEL TRAINING")
print("=" * 60)


# ==========================================
# LOAD DATASET
# ==========================================

print("\nLoading dataset...")

df = pd.read_csv(DATA_FILE)

print(f"Dataset loaded successfully.")
print(f"Records: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# ==========================================
# SELECT FEATURES
# ==========================================

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


target = "risk"


# ==========================================
# CHECK FEATURES
# ==========================================

missing_features = [
    feature
    for feature in features
    if feature not in df.columns
]

if missing_features:

    print("\nERROR: Missing features:")

    for feature in missing_features:
        print(f"- {feature}")

    raise SystemExit


# ==========================================
# PREPARE X AND Y
# ==========================================

X = df[features]

y = df[target]


print("\nFeature matrix:")
print(f"X shape: {X.shape}")

print("\nTarget distribution:")
print(y.value_counts())


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training records: {len(X_train):,}")
print(f"Testing records: {len(X_test):,}")


# ==========================================
# CREATE RANDOM FOREST
# ==========================================

print("\nCreating Random Forest model...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced",
    n_jobs=-1
)


# ==========================================
# TRAIN MODEL
# ==========================================

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Model training completed.")


# ==========================================
# MAKE PREDICTIONS
# ==========================================

print("\nEvaluating model...")

y_pred = model.predict(X_test)


# ==========================================
# ACCURACY
# ==========================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n" + "=" * 60)
print("MODEL RESULTS")
print("=" * 60)

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)


# ==========================================
# CLASSIFICATION REPORT
# ==========================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Normal",
            "High Risk"
        ]
    )
)


# ==========================================
# CONFUSION MATRIX
# ==========================================

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ==========================================
# FEATURE IMPORTANCE
# ==========================================

print("\nFeature Importance:")

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print(
    importance.to_string(index=False)
)


# ==========================================
# SAVE MODEL
# ==========================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_FILE
)


print("\n" + "=" * 60)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 60)

print(
    f"\nModel saved to:\n{MODEL_FILE}"
)

print("\nTruckGuard AI training complete! 🚛🤖")