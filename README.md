# 🇾🇪 Yemen Crisis Analytics & Intelligence Command Center

An advanced, production-grade geospatial data intelligence platform and analytics command center designed to monitor, model, and visualize real-time atmospheric, demographic, and humanitarian crisis conditions across Yemen's 11 key governorates. 

The system operates a three-tier high-availability architecture that orchestrates background ETL data pipelines, stores records in a performance-optimized SQLite engine, and serves interactive analytics panels and animated cartographic overlays.

---

## 🚀 Key Capabilities & Core Architecture

### 1. Geospatial Intelligence & Dynamic Overlays (Leaflet.js & Canvas)
*   **Thermal Governorate Shading**: Parses high-precision ADM1 geographic boundaries of Yemen. It dynamically adjusts regional fill colors based on live temperature telemetry, shifting from soothing cool tones to deep warning reds as temperatures rise.
*   **Animated Wind Vector Particle Flow**: A custom HTML5 Canvas overlays the Leaflet map. It spawns hundreds of independent vector particles that move in real time according to the **exact wind speed and direction** stored in the database, constrained specifically within governorate boundaries.
*   **Interactive Regional Info-Cards**: Dynamic tooltips show localized stats for each governorate, including live weather, hospital capacity forecasts, and humanitarian risk indexes.

### 2. Autonomous Ingestion Pipelines (ETL)
*   **Atmospheric Sensor Bot (`weather_fetcher.py`)**: Runs daemonized every 300 seconds. It connects to the Open-Meteo V1 API to extract 14 distinct atmospheric telemetry variables (including heat index, apparent temperature, relative humidity, UV index, cloud cover, visibility, and solar radiation) for Sana'a, Aden, Taiz, Ibb, Dhamar, Al Hudaydah, Mukalla, Amran, Sa'dah, Marib, and Al Mahrah.
*   **ReliefWeb (OCHA) Scraper**: Feeds real-time humanitarian field logs and situational reports into the dashboard, filtered by country (`Yemen`) and sector (`Health` & `Education`).
*   **Demographic API Pipeline**: Integrates live population projections using API wrappers (UN DESA data) to render live-updating population meters.
*   **Strategic Indicator Database**: Stores historical indicators (such as World Bank demographic profiles) as optimized JSON structures, permitting dynamic multi-year graphing without complex relational overhead.

### 3. Dashboard Analytical Engine (Flask & Chart.js)
*   **Multi-Dimensional Atmospheric Radar**: Evaluates and graphs five key parameters (Temperature, Wind Velocity, Humidity, Sky Density, and UV Intensity) to signal extreme climate events.
*   **Temporal Gradient Tracker**: Generates historical trendlines showing the thermal gradient and pressure variance over preceding hours using local database logs.
*   **Epidemiological Caseload Matrix**: Projects hospital occupancy and regional epidemic pressure (e.g., Cholera caseloads) using an aggregation of static WHO datasets, live reports, and deterministic simulation algorithms.
*   **Predictive Education Modeler**: Uses complex regional metrics (including unpaid teacher salary estimates, systemic local risk, and historical literacy ratios) to simulate and project current school attendance anomalies and structural deficits.

---

## 🛠️ Technology Stack

*   **Backend**: Python 3.10+ / Flask (REST APIs, routing, and data integration)
*   **Frontend**: HTML5, Vanilla CSS3 (Tactical Dark UI), JavaScript (ES6)
*   **Geospatial**: Leaflet.js (Interactive mapping), Custom HTML5 Canvas (Particle physics)
*   **Visualizations**: Chart.js (Radar, Line, Bar, and Doughnut charts)
*   **Database**: SQLite 3 (Performance-indexed tables with JSON blobs)
*   **Data Sources**: Open-Meteo API, UN DESA (Population.io), OCHA ReliefWeb API

---

## 📊 Database Schema Blueprint

The database `weather.db` maintains structural integrity through four primary relational tables:
*   `locations`: Stores precise latitude, longitude, and metadata for the 11 audited Yemeni Governorates.
*   `current_weather`: Uses a `UNIQUE(location_id)` constraint to guarantee $O(1)$ lookup complexity for real-time dashboard fetches.
*   `weather_history`: Holds high-volume historic records used to calculate temporal trendlines.
*   `health_indicators`: Caches World Bank historical metrics as JSON blobs, optimizing frontend retrieval and parsing speeds.

---

## 🧪 System Diagnostics & Data Quality

The architecture includes a comprehensive suite of verification utilities to guarantee data quality and system availability:
*   `verify_weather.py`: Audits current SQLite table records against live API endpoints, calculating variance tolerances and validating schema integrity.
*   `verify_system.py`: Runs end-to-end integration diagnostics for API connectivity, local cache health, background ETL status, and file system observers.

---

## 🚦 Getting Started

### Prerequisites
*   Python 3.10 or higher
*   Pip package manager

### Installation
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/abdulsalamfaiz2024-cmd/yemen-crisis-dashboard.git
    cd yemen-crisis-dashboard
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Initialize the Database**:
    ```bash
    python setup_db.py
    ```
4.  **Launch the Telemetry Ingestion Bot**:
    ```bash
    python weather_fetcher.py
    ```
5.  **Run the Flask Analytics Application**:
    ```bash
    python app.py
    ```
6.  **Access the Dashboard**:
    Open your browser and navigate to `http://127.0.0.1:5000` to interact with the command center interface.
