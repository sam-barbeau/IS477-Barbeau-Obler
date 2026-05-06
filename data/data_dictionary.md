# Data Dictionary

This file describes every column in the datasets in `data/`. All three CSVs are monthly observations from January 2019 through December 2024 (72 rows each).

## `fedfunds_raw.csv`

Pulled directly from the FRED API (series `FEDFUNDS`).

| Column | Type | Units | Description |
|--------|------|-------|-------------|
| `date` | date (YYYY-MM-DD) | — | First day of the month the observation refers to |
| `fedfunds` | float | percent | Monthly average effective federal funds rate |

## `permit_raw.csv`

Pulled directly from the FRED API (series `PERMIT`).

| Column | Type | Units | Description |
|--------|------|-------|-------------|
| `date` | date (YYYY-MM-DD) | — | First day of the month the observation refers to |
| `permit` | float | thousands of units, seasonally adjusted annual rate (SAAR) | New privately-owned housing units authorized by building permits |

## `integrated_data.csv`

Built by `scripts/integrate_data.py`. Joins `fedfunds_raw.csv` and `permit_raw.csv` on `date` and adds a few derived columns we use for analysis.

| Column | Type | Units | Description |
|--------|------|-------|-------------|
| `date` | date (YYYY-MM-DD) | — | First day of the month |
| `fedfunds` | float | percent | Same as in `fedfunds_raw.csv` |
| `permit` | float | thousands (SAAR) | Same as in `permit_raw.csv` |
| `year` | int | — | Calendar year extracted from `date` |
| `month` | int | 1–12 | Calendar month extracted from `date` |
| `rate_change` | float | percentage points | Month-over-month change in `fedfunds` (NaN for the first row) |
| `permit_pct_change` | float | percent | Month-over-month percent change in `permit` (NaN for the first row) |
| `period` | string | — | One of: `Pre-COVID` (2019), `Pandemic` (2020–2021), `Rate Hikes` (2022–2023), `2024` |

## `checksums.json`

SHA-256 checksums for the three CSVs above, written by the acquisition and integration scripts. Used to verify reproducibility — anyone re-running the pipeline should get identical hashes for `fedfunds_raw.csv`, `permit_raw.csv`, and `integrated_data.csv`.
