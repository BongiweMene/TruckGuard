import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================
# TRUCKGUARD - REAL DATASET PREPARATION
# ==========================================

# Project folders
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = (
    BASE_DIR
    / "data"
    / "driverBehaviorDataset"
    / "data"
)

OUTPUT_DIR = BASE_DIR / "data"
OUTPUT_FILE = OUTPUT_DIR / "truckguard_dataset.csv"


# ==========================================
# PROCESS ONE DRIVING SESSION
# ==========================================

def process_session(session_folder):

    print(f"\nProcessing session: {session_folder.name}")

    # Sensor files
    accelerometer_file = session_folder / "acelerometro_terra.csv"
    linear_acceleration_file = session_folder / "aceleracaoLinear_terra.csv"
    gyroscope_file = session_folder / "giroscopio_terra.csv"
    magnetometer_file = session_folder / "campoMagnetico_terra.csv"
    ground_truth_file = session_folder / "groundTruth.csv"

    # Check that required files exist
    required_files = [
        accelerometer_file,
        linear_acceleration_file,
        gyroscope_file,
        magnetometer_file,
        ground_truth_file
    ]

    for file in required_files:
        if not file.exists():
            print(f"WARNING: Missing file: {file.name}")
            return None

    # ==========================================
    # LOAD SENSOR DATA
    # ==========================================

    accelerometer = pd.read_csv(accelerometer_file)
    linear_acceleration = pd.read_csv(linear_acceleration_file)
    gyroscope = pd.read_csv(gyroscope_file)
    magnetometer = pd.read_csv(magnetometer_file)
    ground_truth = pd.read_csv(ground_truth_file)

    # Clean column names
    accelerometer.columns = accelerometer.columns.str.strip()
    linear_acceleration.columns = linear_acceleration.columns.str.strip()
    gyroscope.columns = gyroscope.columns.str.strip()
    magnetometer.columns = magnetometer.columns.str.strip()
    ground_truth.columns = ground_truth.columns.str.strip()

    print(f"Accelerometer records: {len(accelerometer)}")
    print(f"Linear acceleration records: {len(linear_acceleration)}")
    print(f"Gyroscope records: {len(gyroscope)}")
    print(f"Magnetometer records: {len(magnetometer)}")
    print(f"Ground truth events: {len(ground_truth)}")

    # ==========================================
    # KEEP USEFUL SENSOR FEATURES
    # ==========================================

    # Accelerometer
    accelerometer = accelerometer[
        ["uptimeNanos", "x", "y", "z"]
    ].copy()

    accelerometer.rename(
        columns={
            "x": "accel_x",
            "y": "accel_y",
            "z": "accel_z"
        },
        inplace=True
    )

    # Linear acceleration
    linear_acceleration = linear_acceleration[
        ["uptimeNanos", "x", "y", "z"]
    ].copy()

    linear_acceleration.rename(
        columns={
            "x": "linear_x",
            "y": "linear_y",
            "z": "linear_z"
        },
        inplace=True
    )

    # Gyroscope
    gyroscope = gyroscope[
        ["uptimeNanos", "x", "y", "z"]
    ].copy()

    gyroscope.rename(
        columns={
            "x": "gyro_x",
            "y": "gyro_y",
            "z": "gyro_z"
        },
        inplace=True
    )

    # Magnetometer
    magnetometer = magnetometer[
        ["uptimeNanos", "x", "y", "z"]
    ].copy()

    magnetometer.rename(
        columns={
            "x": "mag_x",
            "y": "mag_y",
            "z": "mag_z"
        },
        inplace=True
    )

    # ==========================================
    # CONVERT SENSOR TIME
    # ==========================================

    for dataframe in [
        accelerometer,
        linear_acceleration,
        gyroscope,
        magnetometer
    ]:

        dataframe["uptimeNanos"] = pd.to_numeric(
            dataframe["uptimeNanos"],
            errors="coerce"
        )

    # ==========================================
    # MERGE SENSOR DATA
    # ==========================================

    # Start with accelerometer data
    combined = accelerometer.copy()

    # Merge closest sensor readings based on sensor time
    combined = pd.merge_asof(
        combined.sort_values("uptimeNanos"),
        linear_acceleration.sort_values("uptimeNanos"),
        on="uptimeNanos",
        direction="nearest"
    )

    combined = pd.merge_asof(
        combined.sort_values("uptimeNanos"),
        gyroscope.sort_values("uptimeNanos"),
        on="uptimeNanos",
        direction="nearest"
    )

    combined = pd.merge_asof(
        combined.sort_values("uptimeNanos"),
        magnetometer.sort_values("uptimeNanos"),
        on="uptimeNanos",
        direction="nearest"
    )

    # ==========================================
    # CREATE MAGNITUDES
    # ==========================================

    combined["acceleration_magnitude"] = np.sqrt(
        combined["accel_x"] ** 2
        + combined["accel_y"] ** 2
        + combined["accel_z"] ** 2
    )

    combined["linear_acceleration_magnitude"] = np.sqrt(
        combined["linear_x"] ** 2
        + combined["linear_y"] ** 2
        + combined["linear_z"] ** 2
    )

    combined["gyro_magnitude"] = np.sqrt(
        combined["gyro_x"] ** 2
        + combined["gyro_y"] ** 2
        + combined["gyro_z"] ** 2
    )

    combined["magnetic_magnitude"] = np.sqrt(
        combined["mag_x"] ** 2
        + combined["mag_y"] ** 2
        + combined["mag_z"] ** 2
    )

    # ==========================================
    # CREATE EVENT TIME
    # ==========================================

    first_timestamp = combined["uptimeNanos"].min()

    combined["time_seconds"] = (
        combined["uptimeNanos"] - first_timestamp
    ) / 1_000_000_000

    # ==========================================
    # APPLY GROUND TRUTH LABELS
    # ==========================================

    ground_truth["inicio"] = pd.to_numeric(
        ground_truth["inicio"],
        errors="coerce"
    )

    ground_truth["fim"] = pd.to_numeric(
        ground_truth["fim"],
        errors="coerce"
    )

    combined["event"] = "evento_nao_agressivo"

    for _, event_row in ground_truth.iterrows():

        start = event_row["inicio"]
        end = event_row["fim"]
        event_name = event_row["evento"]

        if pd.isna(start) or pd.isna(end):
            continue

        mask = (
            (combined["time_seconds"] >= start)
            & (combined["time_seconds"] <= end)
        )

        combined.loc[mask, "event"] = event_name

    # ==========================================
    # CREATE MACHINE LEARNING TARGET
    # ==========================================

    aggressive_events = [
        "curva_direita_agressiva",
        "curva_esquerda_agressiva"
    ]

    combined["risk"] = combined["event"].isin(
        aggressive_events
    ).astype(int)

    # ==========================================
    # ADD SESSION ID
    # ==========================================

    combined["session_id"] = session_folder.name

    # ==========================================
    # REMOVE INVALID VALUES
    # ==========================================

    combined.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    combined.dropna(inplace=True)

    print(
        f"Processed records: {len(combined)}"
    )

    print(
        f"High-risk records: {combined['risk'].sum()}"
    )

    return combined


# ==========================================
# PROCESS ALL DATA SESSIONS
# ==========================================

def main():

    print("=" * 60)
    print("TRUCKGUARD DATASET PREPARATION")
    print("=" * 60)

    print(f"\nDataset location:")
    print(DATA_DIR)

    if not DATA_DIR.exists():

        print("\nERROR: Dataset folder was not found.")

        return

    sessions = [
        folder
        for folder in DATA_DIR.iterdir()
        if folder.is_dir()
    ]

    print(
        f"\nFound {len(sessions)} sessions."
    )

    all_sessions = []

    for session in sorted(sessions):

        result = process_session(session)

        if result is not None:
            all_sessions.append(result)

    # ==========================================
    # COMBINE ALL SESSIONS
    # ==========================================

    if not all_sessions:

        print(
            "\nERROR: No sessions were processed."
        )

        return

    final_dataset = pd.concat(
        all_sessions,
        ignore_index=True
    )

    # ==========================================
    # SAVE DATASET
    # ==========================================

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    final_dataset.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ==========================================
    # FINAL INFORMATION
    # ==========================================

    print("\n" + "=" * 60)
    print("DATASET CREATED SUCCESSFULLY")
    print("=" * 60)

    print(
        f"\nTotal records: {len(final_dataset):,}"
    )

    print(
        f"Total features: {len(final_dataset.columns)}"
    )

    print(
        f"High-risk records: "
        f"{final_dataset['risk'].sum():,}"
    )

    print(
        f"Normal records: "
        f"{(final_dataset['risk'] == 0).sum():,}"
    )

    print("\nEvent distribution:")

    print(
        final_dataset["event"].value_counts()
    )

    print(
        f"\nSaved to:\n{OUTPUT_FILE}"
    )


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    main()