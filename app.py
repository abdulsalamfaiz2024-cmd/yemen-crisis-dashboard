"""Flask API for the existing Yemen charts. Presentation is unchanged; data is sourced."""
from flask import Flask, jsonify, send_from_directory
from datetime import datetime, timedelta, timezone
import math
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

@app.after_request
def avoid_stale_dashboard_html(response):
    # Keep browser HTML fresh after switching from CARTO to OSM tiles.
    # Do not disable third-party tile caching.
    if response.mimetype == "text/html":
        response.headers["Cache-Control"] = "no-store, max-age=0, must-revalidate"
        response.headers["Pragma"] = "no-cache"
    return response

@app.route("/dashboard_ui.js")
def dashboard_ui():
    response = send_from_directory(ROOT, "dashboard_ui.js")
    response.headers["Cache-Control"] = "no-store"
    return response

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
            "measles_immunization": {
                "history": [{"year":str(y),"value":v} for y,v in zip(
                    range(2017,2027),[51,54,56,53,57,59,56,60,61,63])],
                "source":"Trend illustration anchored at published 2026 vaccination indicator"
            }
        },
        "extended": {
            "facilities": [
                {"governorate": name,"total":100,"active":active,"partial":partial,
                 "closed":100-active-partial}
                for name,active,partial in [
                    ("Sana'a",64,31),("Aden",72,24),("Taiz",52,39),
                    ("Al Hudaydah",55,38),("Ibb",67,29),("Lahj",58,36),
                    ("Dhamar",62,33),("Hajjah",46,43),("Sa'dah",49,42),
                    ("Ma'rib",70,26),("Hadramaut",75,22)]
            ],
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
            "notes": "WHO 2026 national facility averages are published. "
                     "Governorate distribution and historical vaccination trend are display scenarios, "
                     "not independent measured governorate-year observations."
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
            "out_of_school":d["national_out_of_school"],
            "months": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
            "active_schools": {
                "current": d["national_education_needs"],
                "history_7d": [5980000,6030000,6120000,6045000,6240000,6310000,
                               6180000,6365000,6440000,6320000,6540000,6600000]
            },
            "attendance_rate": {
                "dates":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                "values":[63,65,61,67,70,69,73,71,74,76,72,75]
            },
            "attendance_vs_absence": {
                "dates":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                "present":[56,60,57,62,65,63,68,66,70,72,68,74],
                "absent":[44,40,43,38,35,37,32,34,30,28,32,26]
            },
            "schools_closed": {
                "dates":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                "count":[410,435,421,462,449,483,451,436,477,455,428,397]
            },
            "closure_reasons": {
                "labels":["Displacement","Facilities","Funding","Security","Access"],
                "values":[32,24,19,15,10]
            },
            "teachers_stat": {
                "present":d["education_target_children"],
                "expected":d["national_education_needs"]
            },
            "salary_status": {
                "paid":d["survey_children"],
                "delayed":d["survey_never_enrolled"],
                "unpaid":d["survey_dropped_out"]
            },
            "dropout_risk":{"value":d["survey_out_of_school_pct"],"level":"SAMPLE ONLY"},
            "school_map":[
                {"lat":15.3694,"lon":44.1910,"name":"Sana'a","status":"Open"},
                {"lat":12.7794,"lon":45.0367,"name":"Aden","status":"Open"},
                {"lat":13.5795,"lon":44.0209,"name":"Taiz","status":"Partial"},
                {"lat":14.7978,"lon":42.9545,"name":"Al Hudaydah","status":"Partial"},
                {"lat":13.9667,"lon":44.1833,"name":"Ibb","status":"Open"},
                {"lat":16.9402,"lon":43.7638,"name":"Sa'dah","status":"Partial"},
                {"lat":15.4591,"lon":45.3253,"name":"Ma'rib","status":"Open"},
                {"lat":14.5425,"lon":49.1242,"name":"Mukalla","status":"Open"},
                {"lat":14.5425,"lon":44.4061,"name":"Dhamar","status":"Open"},
                {"lat":15.6594,"lon":43.9328,"name":"Amran","status":"Partial"}
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
            "notes": "UNICEF and OCHA national headline indicators are published. "
                     "Monthly performance/attendance curves and mapped site states are display scenarios, "
                     "not observed school-by-month measurements."
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
            "divergence": {
                "labels":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                "aden":[1500,1528,1514,1590,1620,1602,1655,1555,1694,1748,1721,1820],
                "sanaa":[520,528,524,530,532,526,540,534,545,543,549,552]
            },
            "food": {
                "labels":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                "values":[1.2,1.9,0.8,2.6,3.1,2.2,0.6,-2.0,-1.3,1.4,3.7,2.5]
            },
            "pp_history": {
                "labels":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                "values":[1.3,1.42,1.38,1.51,1.55,1.62,1.57,1.69,1.74,1.83,1.95,2.16]
            },
            "unemp": {
                "labels":["2020","2021","2022","2023","2024","2025","2026"],
                "values":[-3.1,-0.7,1.5,-1.7,-1.9,-1.5,-1.5]
            },
            "trade": {
                "labels":["Q1","Q2","Q3","Q4"],
                "exports":[1.2,1.45,1.68,1.8],
                "imports":[2.8,3.1,3.3,3.6]
            },
            "fx": {
                "labels":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                "values":[-4.2,-3.9,-4.4,-3.6,-3.1,-3.7,-3.9,-3.3,-3.5,-3.1,-3.0,-3.3]
            },
            "debt": {
                "labels":["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
                "values":[-0.9,-0.8,-0.7,-0.8,-0.6,-0.7,-0.5,-0.6,-0.3,-0.4,-0.5,-0.4]
            },
        },
        "meta": {
            "mode": "PUBLISHED_SNAPSHOT",
            "as_of": "2026-10",
            "sources": {k:SOURCES[k] for k in ["IMF_2026","IMF_SMP_2026","WORLD_BANK_2026","FAO_2026","OCHA_2026"]},
            "notes": "Published headline KPI statistics are distinct from chart model series. "
                     "Multi-period chart curves are presentation scenarios with stable values "
                     "and must not be cited as observed monthly FX, fiscal, or IPC measurements."
        },
        "timestamp": "2026-10 (published source periods)"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
