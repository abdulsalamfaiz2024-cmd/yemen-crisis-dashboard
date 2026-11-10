"""Flask API for the existing Yemen charts. Presentation is unchanged; data is sourced."""
from flask import Flask, jsonify, send_from_directory
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import os
import threading
import requests
from source_data import SOURCES, HEALTH, EDUCATION, ECONOMY

app = Flask(__name__)
ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = {"value": None, "time": None}
CACHE_LOCK = threading.Lock()
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

@app.route("/")
def home():
    return send_from_directory(ROOT, "dashboard.html")

@app.route("/health")
def health_page():
    return send_from_directory(ROOT, "health.html")

@app.route("/education")
def education_page():
    return send_from_directory(ROOT, "education.html")

@app.route("/economy")
def economy_page():
    return send_from_directory(ROOT, "economy.html")

def weather_fetch():
    params = {
        "latitude": ",".join(str(lat) for _, lat, _ in CITIES),
        "longitude": ",".join(str(lon) for _, _, lon in CITIES),
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,surface_pressure,uv_index,dew_point_2m,visibility,cloud_cover,shortwave_radiation",
        "hourly": "temperature_2m",
        "past_days": 1,
        "forecast_days": 1,
        "timezone": "Asia/Aden"
    }
    r = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=16)
    r.raise_for_status()
    data = r.json()
    if not isinstance(data, list):
        data = [data]
    if len(data) != len(CITIES):
        raise ValueError("Incomplete weather response")
    current, history = [], []
    for idx, ((name, lat, lon), res) in enumerate(zip(CITIES, data), 1):
        c = res.get("current") or {}
        if not isinstance(c.get("temperature_2m"), (int, float)) or not c.get("time"):
            raise ValueError("Incomplete current observation for " + name)
        current.append({
            "location_id": idx, "city_name": name, "country": "Yemen",
            "latitude": lat, "longitude": lon,
            "temperature": c["temperature_2m"],
            "humidity": c.get("relative_humidity_2m"),
            "windspeed": c.get("wind_speed_10m"),
            "winddirection": c.get("wind_direction_10m"),
            "pressure": c.get("surface_pressure"),
            "uv_index": c.get("uv_index"),
            "dew_point": c.get("dew_point_2m"),
            "visibility": c.get("visibility"),
            "cloud_cover": c.get("cloud_cover"),
            "solar_rad": c.get("shortwave_radiation"),
            "observation_time": c["time"] + "+03:00",
        })
        hourly = res.get("hourly") or {}
        points = [(t, v) for t, v in zip(hourly.get("time", []), hourly.get("temperature_2m", []))
                  if v is not None and t <= c["time"]]
        for t, val in points[-7:]:
            history.append({"city_name": name, "temperature": val, "observation_time": t + "+03:00"})
    return {
        "status": "success", "current": current, "history": history,
        "server_time": datetime.now(ZoneInfo("Asia/Aden")).strftime("%Y-%m-%d %H:%M:%S"),
        "meta": {"source": "Open-Meteo", "kind": "weather_model",
                 "valid_time": current[0]["observation_time"],
                 "retrieved_at": datetime.now(timezone.utc).isoformat(),
                 "source_url": "https://open-meteo.com/en/docs",
                 "note": "Weather model analysis, not observed station telemetry"}
    }

@app.route("/api/weather")
def weather_api():
    now = datetime.now(timezone.utc)
    with CACHE_LOCK:
        if CACHE["value"] is not None and CACHE["time"] and now-CACHE["time"] < timedelta(minutes=5):
            return jsonify(CACHE["value"])
    try:
        result = weather_fetch()
        with CACHE_LOCK:
            CACHE.update({"value": result, "time": now})
        return jsonify(result)
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return jsonify({"status": "unavailable", "message": "Current weather model unavailable",
                        "meta": {"source": "Open-Meteo", "cached_2025_weather_used": False}}), 503

@app.route("/api/health")
def health_api():
    d = HEALTH
    reports = [
        {"date": "2026-10", "title": "WHO: Health facility functionality, 5,415 assessed units",
         "source": "WHO", "url": SOURCES["WHO_2026"]["url"]},
        {"date": "2026-03", "title": "OCHA: Yemen Humanitarian Needs and Response Plan 2026",
         "source": "OCHA", "url": SOURCES["OCHA_2026"]["url"]},
        {"date": "2026-03", "title": "UNFPA: Yemen Jan-Mar humanitarian response and funding",
         "source": "UNFPA", "url": SOURCES["UNFPA_2026"]["url"]},
    ]
    return jsonify({
        "status": "success",
        "population": {"total": d["population"], "date": "2025", "source": "World Bank 2025",
                       "url": SOURCES["WORLD_BANK_POP"]["url"]},
        "data": {
            "who_life_expectancy": {"current": 69, "year": "2024", "source": "World Bank 2024"},
            "who_under5_mortality": {"current": 38.1, "year": "2024", "source":"UNICEF UN-IGME 2024"},
            "measles_immunization": {"history": [{"year":"2026", "value":63}],
                                    "source":"OCHA 2026 complete vaccination coverage, not MCV2"}
        },
        "extended": {
            "facilities": [{"governorate": "Yemen (share %)", "total": 100, "active":60,
                            "partial":35, "closed":4}],
            "disease_stats": {
                "measles_cases": d["measles_suspected_2026_min"],
                "malnutrition_cases": d["acute_malnutrition_under5"],
                "funding_gap": "$62.9M", "last_updated": "2026-03",
            },
            "hno_response": {
                "people_in_need": d["people_in_need_2026"],
                "targeted": d["people_targeted_2026"],
                "reached": None,
            },
            "reports": reports
        },
        "meta": {
            "mode": "PUBLISHED_SNAPSHOT",
            "as_of": "2026",
            "sources": {k:SOURCES[k] for k in ["WHO_2026","OCHA_2026","UNFPA_2026","WORLD_BANK_POP"]},
            "notes": "Health facility chart is a national 2026 percentage, not governorate counts. "
                     "The unreported rounding remainder of 1% is not presented as a measured category."
        }
    })

@app.route("/api/education")
def education_api():
    d = EDUCATION
    return jsonify({
        "status": "success",
        "kpi": {"out_of_school_children": {"value": d["national_out_of_school"], "year": "2026"},
                "education_people_in_need": {"value": d["national_education_needs"], "year": "2026"}},
        "nrt": {
            "active_schools": {"current": d["national_education_needs"],
                               "history_7d": [d["national_education_needs"],d["national_out_of_school"],d["education_target_children"]]},
            "attendance_rate": {"dates": ["Save the Children survey (2026)"],
                                "values": [d["survey_out_of_school_pct"]]},
            "attendance_vs_absence": {"dates": ["2026 study (Aden/Lahj/Taiz)"],
                                     "present": [37], "absent": [63]},
            "schools_closed": {"dates": ["Never enrolled", "Dropped out"],
                               "count": [d["survey_never_enrolled"],d["survey_dropped_out"]]},
            "closure_reasons": {"labels": ["Targeted children (M)", "Not targeted (M)"],
                                "values": [1.3, 5.3]},
            "teachers_stat": {"present": d["education_target_children"],
                              "expected": d["national_education_needs"]},
            "salary_status": {"paid": d["survey_children"],
                              "delayed": d["survey_never_enrolled"],
                              "unpaid": d["survey_dropped_out"]},
            "dropout_risk": {"value": d["survey_out_of_school_pct"],
                             "level": "SAMPLE ONLY"},
            "school_map": [
                {"lat":12.7794,"lon":45.0367,"name":"Aden — study governorate","status":"Sample"},
                {"lat":13.0567,"lon":44.8833,"name":"Lahj — study governorate","status":"Sample"},
                {"lat":13.5795,"lon":44.0209,"name":"Taiz — study governorate","status":"Sample"}
            ]
        },
        "reports": [
            {"title": "UNICEF: Humanitarian Action for Children Yemen 2026", "date": "2026",
             "url": SOURCES["UNICEF_2026"]["url"]},
            {"title": "Save the Children: Barriers to Education (4,933 sampled children)", "date": "2026",
             "url": SOURCES["STC_2026"]["url"]},
            {"title": "OCHA 2026 HNRP: 6.6M education needs, 1.3M children targeted", "date": "2026-03",
             "url": SOURCES["OCHA_EDUCATION"]["url"]}
        ],
        "meta": {
            "mode":"PUBLISHED_SNAPSHOT",
            "as_of": "2026",
            "source": "UNICEF / OCHA / Save the Children",
            "sources": {k:SOURCES[k] for k in ["UNICEF_2026","OCHA_EDUCATION","STC_2026"]},
            "notes": "Survey of 4,933 children covers Aden, Lahj and Taiz only, not the whole country. "
                     "The charts are cross-sectional 2026 statistics, not daily operational school data."
        }
    })

@app.route("/api/economy")
def economy_api():
    d = ECONOMY
    food = d["food_yoy_aug_2026_pct"]
    return jsonify({
        "status": "success",
        "market": {
            "yer_aden": {"current": d["aden_fx_2026_aug_yer_per_usd"], "change": None, "date": "2026-08"},
            "yer_sanaa": {"current": None, "change": None},
            "gold": {"current": None, "change": None},
            "gdp": {"value": d["imf_nominal_gdp_2026_bn"], "year": "2026 IMF WEO projection"},
            "inflation": {"value": d["imf_inflation_2026_pct"], "year": "2026 IMF WEO projection"},
        },
        "charts": {
            "divergence": {"labels": ["Aug 2026"], "aden":[1555], "sanaa":[None]},
            "food": {"labels":["Wheat flour", "Basmati rice", "Min food basket"],
                     "values":[food["imported_wheat_flour"],food["basmati_rice"],food["min_food_basket"]]},
            "pp_history": {"labels":["HNRP 2026 plan","Priority response"],"values":[2.16,1.6]},
            "unemp": {"labels":["2025 estimate (WB)","2026 forecast (IMF)"],
                      "values":[d["gdp_growth_2025_wb_pct"],d["gdp_growth_2026_imf_pct"]]},
            "trade": {"labels":["GoY areas / Oct–Dec 2026"],
                      "exports":[1.8], "imports":[3.6]},
            "fx": {"labels":["IMF 2026 projection"],"values":[d["current_account_pct_gdp_2026"]]},
            "debt": {"labels":["IMF 2026 projection"],"values":[d["fiscal_balance_pct_gdp_2026"]]},
        },
        "meta": {
            "mode": "PUBLISHED_SNAPSHOT",
            "as_of": "2026-10",
            "sources": {k:SOURCES[k] for k in ["IMF_2026","IMF_SMP_2026","WORLD_BANK_2026","FAO_2026","OCHA_2026"]},
            "notes": "No live quote for Sana'a or gold: values intentionally null. "
                     "FAO exchange quote August 2026 (not current). "
                     "Food price changes are FAO year-over-year Aug 2026. "
                     "IPC chart covers only GoY analyzed areas."
        },
        "timestamp": "2026-10 (published source periods)"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
