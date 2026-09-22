import requests

OSIRIS_BASE_URL = "https://osirisai.live"


def get_weather_data():
    """Fetch severe-weather/natural-event data from OSIRIS.

    OSIRIS documents /api/weather as a keyless GET endpoint backed by
    severe-weather/natural-event feeds. The function returns the raw JSON
    so the UI can remain flexible if the upstream schema changes.
    """
    try:
        response = requests.get(
            f"{OSIRIS_BASE_URL}/api/weather",
            timeout=10,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Weather API error: {e}"}


def get_radar_data():
    """Fetch OSIRIS radar/navigation-outage intelligence."""
    try:
        response = requests.get(
            f"{OSIRIS_BASE_URL}/api/radar",
            timeout=10,
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as e:
        return {"error": f"Radar API error: {e}"}


def normalize_weather_events(payload):
    """Convert common OSIRIS/GeoJSON weather payloads to table-friendly rows."""
    if not payload or isinstance(payload, dict) and payload.get("error"):
        return []

    if isinstance(payload, dict):
        if isinstance(payload.get("features"), list):
            raw_events = payload["features"]
        elif isinstance(payload.get("events"), list):
            raw_events = payload["events"]
        elif isinstance(payload.get("data"), list):
            raw_events = payload["data"]
        elif isinstance(payload.get("weather"), list):
            raw_events = payload["weather"]
        else:
            raw_events = []
    elif isinstance(payload, list):
        raw_events = payload
    else:
        raw_events = []

    rows = []
    for event in raw_events:
        if not isinstance(event, dict):
            continue

        properties = event.get("properties") or event
        geometry = event.get("geometry") or {}
        coordinates = geometry.get("coordinates")

        lat = None
        lon = None
        if isinstance(coordinates, (list, tuple)):
            # GeoJSON point = [longitude, latitude].
            if len(coordinates) >= 2 and all(
                isinstance(x, (int, float)) for x in coordinates[:2]
            ):
                lon, lat = coordinates[:2]
            elif coordinates and isinstance(coordinates[0], (list, tuple)):
                first = coordinates[0]
                if len(first) >= 2:
                    lon, lat = first[:2]

        def first_value(*keys):
            for key in keys:
                value = properties.get(key)
                if value not in (None, ""):
                    return value
            return "—"

        rows.append(
            {
                "Event": first_value("title", "name", "event", "type"),
                "Category": first_value("category", "categories", "event_type"),
                "Severity": first_value("severity", "severity_level", "alert_level"),
                "Location": first_value("location", "place", "description"),
                "Date": first_value("date", "datetime", "updated", "closed"),
                "Latitude": lat,
                "Longitude": lon,
            }
        )

    return rows
