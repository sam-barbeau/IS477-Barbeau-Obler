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

## Timeline



| Target Date | Task | Description | Owner |

|------------|------|-------------|-------|

| Week 1 | Project plan finalized | Complete and submit ProjectPlan.md; create `project-plan` tag/release | Sam & Everett |

| Week 2 | Data acquisition scripts | Write Python scripts to pull FEDFUNDS and PERMIT data via FRED API, save as CSV, and compute SHA-256 checksums | Sam |

| Week 3 | Data profiling & cleaning | Profile raw data (check for missing values, data types, outliers), clean and document any transformations | Everett |

| Week 4 | Data integration | Merge the two datasets on `date`, validate the joined dataframe, export integrated dataset | Sam |

| Week 5 | Exploratory analysis & visualization | Time-series plots, summary statistics, distribution analysis, scatter plots of rate vs. permits | Everett |

| Week 6 | ... | ... | ... |



## Constraints



- **National data only:** Both series are national-level, so we can't look at regional differences (e.g., Sun Belt vs. Midwest) unless we find reliable state-level permit data, which has been hard to access programmatically from the Census API.

- **Correlation is not causation:** Interest rates aren't the only thing driving building permits. Lumber prices, labor shortages, supply chain issues, and local zoning all matter too. We can find patterns and associations, but we can't prove the rate directly caused a change in permits.

- **Seasonality:** The PERMIT data is already seasonally adjusted, but the FEDFUNDS data isn't (rate decisions don't follow seasonal patterns, so it doesn't need to be). We'll need to be careful about any seasonal quirks in the relationship.

- **Pandemic effects:** The 2020–2021 period had stimulus checks, remote-work housing booms, and supply chain chaos — all of which could muddy the rate-to-permits relationship. We'll call this out in our analysis rather than drop the data.

- **API rate limits:** FRED allows 120 requests per minute, which is plenty for us, but our scripts should still handle errors gracefully.

- **Data licensing:** FRED data is free and public. The underlying data comes from the Federal Reserve and Census Bureau, which are U.S. government sources and not copyrighted.



## Gaps



- **State-level data:** We haven't found a reliable way to pull monthly state-level building permit data programmatically. If we do, we could extend the analysis to compare different regions.

- **Mortgage rates as a middle step:** The fed funds rate really affects housing through mortgage rates. Adding 30-year mortgage rate data (FRED series MORTGAGE30US) as a third variable could make the analysis stronger. We'll decide whether to include it once the main pipeline is working.

- **Visualization tools:** We haven't picked between Matplotlib/Seaborn and Plotly yet. We'll figure this out during Week 5 based on what works best for showing time-series data.
