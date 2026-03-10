# Global Conflict Intelligence Dashboard

A hybrid conflict-monitoring dashboard built with **Python**, **Streamlit**, **GDELT**, and **GitHub Actions** to track recent war-related media signals and structured conflict patterns.

This project combines:
- a **Recent War News Pulse** powered by GDELT
- a **Structured Conflict Dashboard** powered by historical ACLED data
- an automated refresh pipeline that updates the processed datasets on a schedule

---

## Project Overview

The goal of this project is to build a visually polished and analytically useful dashboard for monitoring global conflict-related developments.

The dashboard is designed to support:
- recent war/news monitoring
- conflict topic tracking
- media-source analysis
- geographic conflict visualization
- historical structured conflict exploration

This project was built as a portfolio project connecting interests in:
- international studies
- data analytics
- Python development
- dashboard design
- automation workflows

---

## Key Features

### Recent War News Pulse
This section uses **GDELT** to monitor recent conflict-related media coverage.

Features include:
- recent article count
- top source countries
- top domains
- language distribution
- conflict topic breakdown
- latest headlines table
- automatically generated summary insight box

### Structured Conflict Dashboard
This section uses cleaned **ACLED** data for structured conflict analysis.

Features include:
- conflict event KPIs
- fatalities summary
- interactive conflict map
- event type breakdown
- daily event trend
- fatalities by region
- recent events table

### Automation
The project includes an automated refresh workflow using **GitHub Actions**.

Automation covers:
- fetching new GDELT data
- cleaning and processing the raw file
- updating processed CSV files
- committing refreshed data back to the repository

---

## Screenshots
- Recent War News Pulse tab
<img width="1704" height="1286" alt="Recent_war1" src="https://github.com/user-attachments/assets/e6696a39-288e-4b00-9067-1701561d0b51" />
<img width="1658" height="1251" alt="Recent_war2" src="https://github.com/user-attachments/assets/dc138889-00c0-4b3f-954e-ad2292821381" />
- Structured Conflict Dashboard tab
<img width="2532" height="1171" alt="Structured_conflict1" src="https://github.com/user-attachments/assets/39f54aa7-6cd8-401b-ba2c-8f3d9755e5ac" />
<img width="2470" height="1158" alt="Structured_conflict2" src="https://github.com/user-attachments/assets/070cbfa7-efdd-4d27-a208-c1ac3352d620" />





## Tech Stack

- **Python**
- **Pandas**
- **Streamlit**
- **Plotly**
- **PyDeck**
- **GDELT DOC 2.0 API**
- **ACLED** (historical structured conflict layer)
- **GitHub Actions**

---

## Project Structure

```text
global-conflict-intelligence-dashboard/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── fetch_data.py
│   ├── clean_data.py
│   ├── fetch_gdelt.py
│   ├── clean_gdelt.py
│   └── run_refresh_pipeline.py
│
├── .github/
│   └── workflows/
│       └── refresh_data.yml
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```
## Data Sources

### 1. GDELT
GDELT is used for the **recent war-news pulse layer**.

It provides:
- article metadata
- source country
- language
- domain
- headline-level recent media coverage

This powers the recent/news-oriented side of the dashboard.

### 2. ACLED
ACLED is used for the **structured conflict analysis layer**.

It provides:
- conflict event records
- event types
- locations
- fatalities
- actors
- regional trends

In this project, ACLED is used primarily for historical structured exploration because recent detailed access depends on account access level.

---

## How the Dashboard Works

The dashboard is split into two tabs:

### Tab 1 — Recent War News Pulse
This tab focuses on recent conflict-related media signals and includes:
- summary insight box
- recent article metrics
- topic breakdown
- top source countries
- language distribution
- top domains
- latest headlines

### Tab 2 — Structured Conflict Dashboard
This tab focuses on conflict-event analytics and includes:
- event KPIs
- interactive map
- conflict event trends
- regional fatalities
- recent structured events

---

## Automation Workflow

The project includes a GitHub Actions workflow that refreshes the processed data automatically.

The refresh pipeline:
1. fetches recent GDELT war-news data
2. cleans and filters the raw data
3. saves processed CSV files
4. commits updated processed files back to the repository

This turns the project from a static dashboard into a lightweight monitoring system.

---

## How to Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/Vireen555/global-conflict-intelligence-dashboard.git
cd global-conflict-intelligence-dashboard
```

### 2. Create and activate a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

MAC/Linux

```bash
python -m venv venv
source venv/bin/activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the data pipeline manually

```bash
python src/fetch_gdelt.py
python src/clean_gdelt.py
```

If needed, you can also run:

```bash
python src/run_refresh_pipeline.py
```

### 5. Start the Streamlit app

```bash
streamlit run app.py
```
## Current Capabilities

- recent conflict-news monitoring
- topic-based war-news analysis
- media-source distribution analysis
- automated processed-data refresh pipeline
- minimal glass-style dashboard UI
  
## Limitations

- GDELT provides article/news metadata, not fully structured conflict-event records
- conflict topic detection is currently rule-based and can still include some noise
- ACLED recent detailed access depends on account access level
- article-level geolocation is not yet implemented in the recent news tab

These limitations also create future improvement opportunities.

## Future Improvements
Planned and possible improvements include:
- more advanced topic classification
- better false-positive filtering
- sentiment or tone analysis
- clickable article cards
- region-based filtering for GDELT articles
- improved summary generation
- deployment on Streamlit Community Cloud
- optional React-based frontend version in the future

## Why I Built This
I wanted to build a project that sits at the intersection of:

- global affairs
- international studies
- data analytics
- Python
- automation
- visual storytelling
The idea was to create something that is not just technically functional, but also relevant to real-world ongoing events and useful as a portfolio showcase.
## Author
**Vireen Chowdary Vesangi**


If you found this project interesting, feel free to connect or explore the repository.


[Linkedin](www.linkedin.com/in/vireenchowdaryvesangi)

