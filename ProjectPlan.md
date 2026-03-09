# Project Plan: Federal Interest Rates and Residential Building Permits

## Overview

This project looks at how the federal funds rate (the Federal Reserve's main interest rate tool) relates to the number of new residential building permits issued each month across the U.S. When the Fed raises or lowers rates, borrowing gets more or less expensive, and housing is one of the first sectors to feel it. Our goal is to measure and visualize how strong this connection is, and whether there's a time delay, over the period from January 2019 to December 2024. This window covers the low rates before COVID, the near-zero rates during the pandemic, and the sharp rate hikes starting in 2022.

We'll pull both datasets through the FRED (Federal Reserve Economic Data) API, clean them up, align them on a shared monthly date index, and run exploratory and statistical analysis in Python. This includes time-series plots, cross-correlation to check for lagged effects (e.g., do permits drop a few months after a rate hike?), and if needed, a simple regression model. Every step (data acquisition, processing, and analysis) will be scripted so the whole project is reproducible, and everything will be version-controlled in Git.

## Team

| Member |Responsibilities |
|--------|-----------------|
| **Sam Barbeau** | Data acquisition scripts, API integration, data cleaning and merging pipeline, reproducibility infrastructure (hashing, environment setup), statistical analysis |
| **Everett Obler** | Exploratory data analysis, visualization, writing and editing documentation (README, project plan, final report), license and metadata management |


## Research Questions

1. **Primary:** Is there a correlation between the federal funds rate and the number of new residential building permits issued each month in the U.S. from 2019 to 2024?
2. **Secondary:** When the federal funds rate changes, how long does it take for building permit numbers to respond? Is there a noticeable delay?
3. **Exploratory:** Did the pandemic years (2020–2021) break the usual trend of interest rates and building permits?

## Datasets

### Dataset 1: Effective Federal Funds Rate (FEDFUNDS)

- **Source:** Board of Governors of the Federal Reserve System, accessed via the FRED API
- **URL:** https://fred.stlouisfed.org/series/FEDFUNDS
- **Format:** JSON (via API); will be converted to CSV
- **Temporal coverage:** Monthly observations, January 2019 – December 2024
- **Key fields:** `date` (first of month, YYYY-MM-DD), `value` (monthly average rate, percent)
- **Description:** The effective federal funds rate is the overnight lending rate between banks. It's the Fed's main lever for monetary policy and has a direct effect on mortgage rates, consumer loans, and business borrowing.

### Dataset 2: New Private Housing Units Authorized by Building Permits (PERMIT)

- **Source:** U.S. Census Bureau, Building Permits Survey; accessed via the FRED API
- **URL:** https://fred.stlouisfed.org/series/PERMIT
- **Format:** JSON (via API); will be converted to CSV
- **Temporal coverage:** Monthly observations, January 2019 – December 2024
- **Key fields:** `date` (first of month, YYYY-MM-DD), `value` (thousands of units, seasonally adjusted annual rate)
- **Description:** This series tracks how many new privately-owned housing units are approved via building permits each month, reported as a seasonally adjusted annual rate in thousands of units. It's a leading indicator of future construction activity and tends to react quickly to changes in financing conditions.

### Integration

Both datasets share a `date` field formatted as the first of each month (YYYY-MM-DD). We'll join them on this column, giving us a single dataframe with 72 monthly rows that each have the federal funds rate and the permit count side by side.

