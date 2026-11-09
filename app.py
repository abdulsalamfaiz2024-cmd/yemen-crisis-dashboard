"""Yemen humanitarian dashboards: model weather + cited published sector indicators."""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import os
import threading

import requests
from flask import Flask, jsonify, send_from_directory
from verified_data import SECTORS

app = Flask(__name__)
ROOT = os.path.dirname(os.path.abspath(__file__))
CITIES = [
    ("Sana'a", 15.3694, 44.1910),
    ("Aden", 12.7794, 45.0367),
    ("Taiz", 13.5795, 44.0209),
    ("Al Hudaydah", 14.7978, 42.9545),
    ("Ibb", 13.9667, 44.1833),
    ("Mukalla", 14.5425, 49.1242),
    ("Dhamar", 14.5425, 44.4061),
    ("Amran", 15.6594, 43.9328),
    ("Sa'dah", 16.9402, 43.7638),
    ("Ma'rib", 15.4591, 45.3253),
    ("Al Mahrah", 16.2167, 52.1667),
]
CACHE = {"at": None, "data": None}
CACHE_LOCK = threading.Lock()
MAX_AGE = timedelta(minutes=10)

@app.route("/")
def index():
    return send_from_directory(ROOT, "dashboard.html")

@app.route("/health")
@app.route("/education")
@app.route("/economy")
def sector_page():
    return send_from_directory(ROOT, "sector.html")

@app.route("/api/<sector>")
def published_sector(sector):
    if sector == "weather":
        return weather()
    if sector not in SECTORS:
        return jsonify({"status": "error", "message": "Unknown sector"}), 404
    return jsonify({
        "status": "success",
        "data": SECTORS[sector],
        "meta": {
            "mode": "PUBLISHED_SNAPSHOT",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "disclaimer": "Published indicators are not live counts; scope and date accompany each metric."
        }
    })

def _fetch_model_weather():
    params = {
        "latitude": ",".join(str(lat) for _, lat, _ in CITIES),
        "longitude": ",".join(str(lon) for _, _, lon in CITIES),
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,surface_pressure,uv_index,dew_point_2m,visibility,cloud_cover,shortwave_radiation",
        "hourly": "temperature_2m",
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "Asia/Aden"
    }
    response = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=18)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, list):
        payload = [payload]
    if len(payload) != len(CITIES):
        raise ValueError("Open-Meteo returned an incomplete location set")

    cities, history = [], []
    for i, ((name, latitude, longitude), place) in enumerate(zip(CITIES, payload), 1):
        current = place.get("current") or {}
        timestamp = current.get("time")
        if not timestamp or not isinstance(current.get("temperature_2m"), (int, float)):
            raise ValueError("Missing model temperature or timestamp for " + name)
        data = {
            "location_id": i, "city_name": name, "country": "Yemen",
            "latitude": latitude, "longitude": longitude,
            "temperature": current["temperature_2m"],
            "humidity": current.get("relative_humidity_2m"),
            "windspeed": current.get("wind_speed_10m"),
            "winddirection": current.get("wind_direction_10m"),
            "pressure": current.get("surface_pressure"),
            "uv_index": current.get("uv_index"),
            "dew_point": current.get("dew_point_2m"),
            "visibility": current.get("visibility"),
            "cloud_cover": current.get("cloud_cover"),
            "solar_rad": current.get("shortwave_radiation"),
            "observation_time": timestamp + "+03:00",
        }
        cities.append(data)
        times = (place.get("hourly") or {}).get("time", [])
        values = (place.get("hourly") or {}).get("temperature_2m", [])
        valid = [(t, v) for t, v in zip(times, values) if t <= timestamp and v is not None]
        for t, v in valid[-7:]:
            history.append({"city_name": name, "temperature": v, "observation_time": t + "+03:00"})

    return {
        "status": "success",
        "current": cities,
        "history": history,
        "observation_time": cities[0]["observation_time"],
        "server_time": datetime.now(ZoneInfo("Asia/Aden")).isoformat(timespec="seconds"),
        "meta": {"source": "Open-Meteo", "type": "weather_model", "timezone": "Asia/Aden",
                 "notice": "Current weather model analysis; not ground-station observations",
                 "source_url": "https://open-meteo.com/en/docs"}
    }

def weather():
    now = datetime.now(timezone.utc)
    with CACHE_LOCK:
        if CACHE["data"] is not None and CACHE["at"] and now - CACHE["at"] < MAX_AGE:
            return jsonify(CACHE["data"])
    try:
        fresh = _fetch_model_weather()
        with CACHE_LOCK:
            CACHE.update({"data": fresh, "at": now})
        return jsonify(fresh)
    except (requests.RequestException, ValueError, TypeError, KeyError) as err:
        # No misleading "live" data from the 2025 SQLite snapshot.
        return jsonify({"status": "unavailable",
                        "message": "Current weather model unavailable; historical cache is not shown as live",
                        "checked_at": now.isoformat(), "source": "Open-Meteo"}), 503

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
