import pandas as pd
from datetime import datetime


def get_test_gps_data():
    """
    Temporary GPS data for development.
    This will later be replaced or supplemented
    with real phone GPS and truck GPS API data.
    """

    gps_data = pd.DataFrame({
        "truck_id": [
            "TG-001",
            "TG-002",
            "TG-003",
            "TG-004"
        ],

        "driver": [
            "Driver 001",
            "Driver 002",
            "Driver 003",
            "Driver 004"
        ],

        "latitude": [
            -26.2041,
            -26.1951,
            -26.2105,
            -26.2200
        ],

        "longitude": [
            28.0473,
            28.0500,
            28.0350,
            28.0600
        ],

        "speed_kmh": [
            72,
            65,
            91,
            58
        ],

        "timestamp": [
            datetime.now(),
            datetime.now(),
            datetime.now(),
            datetime.now()
        ]
    })

    return gps_data