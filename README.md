# Yemen Crisis Analytics & Monitoring Command Center

A geospatial data monitoring and analytics dashboard developed to compile, model, and display atmospheric, demographic, and humanitarian metrics across 11 key governorates in Yemen.

The system features automated background scripts, a performance-optimized SQLite database, and an interactive frontend dashboard with cartographic overlays.

---

## Core Features & System Architecture

### 1. Geospatial Overlays
*   **Regional Color Shading**: Maps the administrative governorate boundaries of Yemen, dynamically adjusting the fill color of each region based on live temperature values stored in the database.
*   **Wind Flow Simulation**: A custom HTML5 Canvas overlays the map to animate wind particle vectors dynamically. The wind particles adjust their velocity and direction in real time based on the database observations for each governorate.
*   **Regional Summaries**: Interactive hover tooltips provide localized statistics including current weather observations, estimated hospital pressure index, and regional risk metrics.

### 2. Data Pipelines (ETL)
*   **Weather Ingestion Script (`weather_fetcher.py`)**: Runs in the background, making requests every 5 minutes to the Open-Meteo API. It collects 14 atmospheric variables (including temperature, relative humidity, apparent temperature, UV index, cloud cover, and solar radiation) for 11 key cities and governorates.
*   **ReliefWeb (OCHA) Integration**: Fetches recent humanitarian logs and field reports filtered by country (Yemen) and sectors (Health and Education) using OCHA's ReliefWeb API.
*   **Demographic Estimates**: Combines historical census information with public population datasets to display live demographic trends.
*   **Historical Indicators Store**: Caches multi-year development indicators (such as World Bank historical datasets) locally as optimized JSON records, allowing fast parsing and frontend plotting.

### 3. Analytics Dashboard
*   **Atmospheric Parameter Radar**: Graphs temperature, wind velocity, humidity, cloud cover, and UV intensity side-by-side using Chart.js.
*   **Historical Trendlines**: Renders time-series charts displaying temperature and pressure trends over the preceding 24 hours.
*   **Caseload and Hospital Pressure Charts**: Models regional healthcare capacity and projects trends based on historical WHO report indicators.
*   **Education Deficit Simulator**: Calculates and projects school attendance trends based on estimated teacher salaries, regional risks, and historical literacy baselines.

---

## Technologies Used

*   **Backend**: Python, Flask (Web routing and API endpoints)
*   **Frontend**: HTML, CSS, JavaScript (ES6)
*   **Geospatial**: Leaflet.js, Custom HTML5 Canvas (Particle animation)
*   **Data Visualization**: Chart.js
*   **Database**: SQLite

---

## Database Design

The database `weather.db` maintains structural integrity through four primary tables:
*   `locations`: Coordinates and metadata for the 11 Yemeni Governorates.
*   `current_weather`: Stores live meteorological observations, using a unique location constraint to guarantee fast dashboard lookups.
*   `weather_history`: Retains temporal logs to feed the historical charts.
*   `health_indicators`: Caches World Bank historical metrics as JSON strings for fast dashboard parsing.

---

## System Verification

The system includes automated diagnostic tools to audit data and connectivity:
*   `verify_weather.py`: Audits current SQLite table records against live API endpoints, validating schema integrity and checking for data drift.
*   `verify_system.py`: Performs end-to-end checks on database health, API access, and file system paths.

---

## Getting Started

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
4.  **Run the Telemetry Ingestion Script**:
    ```bash
    python weather_fetcher.py
    ```
5.  **Start the Web Server**:
    ```bash
    python app.py
    ```
6.  **Access the App**:
    Navigate to `http://127.0.0.1:5000` in your web browser.
