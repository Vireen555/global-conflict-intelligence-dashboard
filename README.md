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
git clone <your-repo-url>
cd global-conflict-intelligence-dashboard
