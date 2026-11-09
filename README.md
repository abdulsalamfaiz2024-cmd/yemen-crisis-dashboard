# Yemen Monitor — Humanitarian and Weather Dashboards

A Flask dashboard for Yemen with **two distinct data classes**:

1. **Weather:** Current modeled weather and recent hourly model history from [Open-Meteo](https://open-meteo.com/en/docs). No API key. Results are refreshed with a short cache and show their valid time and timezone. They are **model output, not ground-station observations**.
2. **Health, education, economy:** **Published snapshots** from OCHA, WHO, UNICEF, IMF, FAO, Save the Children and the UN. Each indicator includes its scope, source, and reference period. These are **not live counters**.

## Pages
- `/` — Weather and regional temperature map.
- `/health` — Health service needs, facility functionality, nutrition statistics.
- `/education` — National UNICEF statistics and a separate local Save the Children study.
- `/economy` — IMF 2026 outlook, FAO prices and IPC partial-area projections.

All pages work in Arabic and English. See `verified_data.py` for the source registry and the exact reporting scope of each indicator. All sector API endpoints carry `mode: PUBLISHED_SNAPSHOT`.

## Map attribution and usage
Basemap tiles are sourced from OpenStreetMap. The page displays required OSM attribution. See [Tile Usage Policy](https://operations.osmfoundation.org/policies/tiles/). For high-volume or commercial deployments, use an appropriately licensed tile provider or self-hosted tiles.

## Data policy
- No invented live exchange-rate quotes, fabricated school attendance series, simulated hospital facility counts or synthetic disease deaths.
- A projection is labeled as a projection; sample survey rates are not presented as national rates.
- Figures from different regions, definitions or reporting dates are not directly treated as comparable time series.
- A temporary failure of Open-Meteo shows data unavailable rather than displaying the bundled 2025 weather database as current.
- Source figures are static until **explicitly updated and independently verified**; a fresh page load does not mean a new statistical observation.

## Architecture
- Flask backend: `app.py`
- Source metadata and published statistics: `verified_data.py`
- Model weather and interactive Leaflet map: `dashboard.html`
- Source-aware sector dashboard template: `sector.html`
- Historical ETL and SQLite work in older repository files remains reference material and is **not** part of the published sector statistics or current weather API.

## Local development
```bash
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

Published through Vercel's Python/Flask runtime.
