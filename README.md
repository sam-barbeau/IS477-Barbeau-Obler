# Federal Interest Rates and Residential Building Permits

**IS 477 Final Project — Sam Barbeau & Everett Obler**

## What This Project Does

This project looks at how the Federal Reserve's interest rate policy (the federal funds rate) relates to residential building permits across the U.S. from 2019 to 2024. We pull data from the FRED API, merge the two series, and run statistical analysis to measure the correlation and check for time-lagged effects.

## Quick Start

1. **Clone the repo:**
   ```bash
   git clone https://github.com/your-repo/IS477-Barbeau-Obler.git
   cd IS477-Barbeau-Obler
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get a FRED API key** (free): https://fred.stlouisfed.org/docs/api/api_key.html

4. **Run the pipeline:**
   ```bash
   python scripts/acquire_data.py    # Pulls data from FRED
   python scripts/profile_data.py    # Checks data quality
   python scripts/integrate_data.py  # Merges datasets
   python scripts/analyze_data.py    # Generates visualizations and stats
   ```

## Key Findings

- **Significant negative correlation** (r = -0.41, p < 0.001) between fed funds rate and building permits
- **2-month lag effect**: Permits respond most strongly to rate changes about 2 months later
- **Pandemic disruption**: The 2020-2021 period broke the normal pattern due to remote-work housing demand and supply chain chaos

## Project Structure

```
├── scripts/           # Python scripts for data pipeline
├── data/              # Raw and processed datasets
├── output/            # Visualizations and analysis results
├── ProjectPlan.md     # Original project plan
├── StatusReport.md    # Progress report
└── requirements.txt   # Python dependencies
```

## Data Sources

- **Federal Funds Rate (FEDFUNDS)**: Board of Governors of the Federal Reserve System via FRED
- **Building Permits (PERMIT)**: U.S. Census Bureau via FRED

Both datasets are public domain U.S. government data.