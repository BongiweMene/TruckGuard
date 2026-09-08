import requests

OSIRIS_BASE_URL = "https://www.osirisai.live"


def get_weather_data():
    try:
        response = requests.get(
            f"{OSIRIS_BASE_URL}/api/weather",
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        return {
            "error": f"Weather API error: {e}"
        }


def get_radar_data():
    try:
        response = requests.get(
            f"{OSIRIS_BASE_URL}/api/radar",
            timeout=10
        )

        response.raise_for_status()
        return response.json()

    except requests.RequestException as e:
        return {
            "error": f"Radar API error: {e}"
        }