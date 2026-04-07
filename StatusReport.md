# Status Report: Federal Interest Rates and Residential Building Permits

## Overview

It's been about a month since we submitted our project plan, and we've made solid progress. We've completed the data acquisition, profiling, and integration phases, plus we got a head start on the exploratory analysis. The core question we're exploring (how the federal funds rate relates to monthly building permits) has already shown some interesting patterns.

This report walks through what we've done, what we've found, and what's left to do.

---

## Task Updates

### Task 1: Data Acquisition Scripts

**Status: Complete**

We built a Python script ([scripts/acquire_data.py](scripts/acquire_data.py)) that pulls both datasets from the FRED API:

- **FEDFUNDS**: The effective federal funds rate (monthly average)
- **PERMIT**: New private housing units authorized by building permits (thousands of units, seasonally adjusted annual rate)

The script fetches 72 monthly observations for each series (January 2019 through December 2024), saves them as CSV files, and computes SHA-256 checksums for reproducibility. The checksums are stored in [data/checksums.json](data/checksums.json).

**Output files:**
- `data/fedfunds_raw.csv` — 72 rows, no missing values
- `data/permit_raw.csv` — 72 rows, no missing values

We stored our FRED API key locally (not committed to the repo) and the script handles API errors gracefully.

### Task 2: Data Profiling & Cleaning

**Status: Complete**

We wrote a profiling script ([scripts/profile_data.py](scripts/profile_data.py)) that checks both raw datasets for quality issues. Here's what we found:

**Federal Funds Rate:**
- 72 complete monthly observations
- No missing values or gaps
- Range: 0.05% (pandemic low) to 5.33% (2023 peak)
- Mean: 2.41%

**Building Permits:**
- 72 complete monthly observations
- No missing values or gaps
- Range: 1,076K to 1,920K units
- Mean: 1,546K units

**Good news:** Both datasets came in clean from FRED. No transformations or imputations were needed. Move straight to integration.

### Task 3: Data Integration

**Status: Complete**

The integration script ([scripts/integrate_data.py](scripts/integrate_data.py)) merges the two datasets on their shared `date` column. The result is a single dataframe with 72 rows where each month has:
- The federal funds rate
- The building permits count
- Some derived columns we added for analysis: `year`, `month`, `rate_change`, `permit_pct_change`, and a `period` label (Pre-COVID, Pandemic, Rate Hikes, 2024)

**Output file:**
- `data/integrated_data.csv` — the merged dataset with all columns
- SHA-256 checksum recorded in `data/checksums.json`

The merge was straightforward since both series use the same monthly date format from FRED.

### Task 4: Exploratory Analysis & Visualization

**Status: In Progress (Ahead of Schedule)**

We got started on the analysis earlier than planned because we were curious to see what the data showed. The analysis script ([scripts/analyze_data.py](scripts/analyze_data.py)) generates four visualizations and runs statistical tests.

**Visualizations created:**

1. **Time Series Overview** ([output/fig1_timeseries.png](output/fig1_timeseries.png))
   - Dual-axis plot showing both series over time
   - Includes shading for the pandemic period and rate hike period
   - You can clearly see rates crash to near-zero in 2020, then spike starting in 2022

2. **Scatter Plot with Correlation** ([output/fig2_scatter.png](output/fig2_scatter.png))
   - Points colored by period (Pre-COVID, Pandemic, Rate Hikes, 2024)
   - Includes the regression line with r = -0.41 and p < 0.001
   - Shows the inverse relationship isn't perfectly linear, but it's there

3. **Cross-Correlation Analysis** ([output/fig3_crosscorr.png](output/fig3_crosscorr.png))
   - Shows correlation at different lag values (±12 months)
   - Strongest inverse correlation at lag = -2 months
   - This suggests permits respond to rate changes with about a 2-month delay

4. **Period Comparison Box Plots** ([output/fig4_periods.png](output/fig4_periods.png))
   - Side-by-side distributions of rates and permits by economic period
   - Highlights how different the pandemic period was from the others

**Key statistical findings:**

| Metric | Value |
|--------|-------|
| Pearson correlation | r = -0.41 (p < 0.001) |
| Spearman correlation | ρ = -0.43 (p < 0.001) |
| Best lag | -2 months (r = -0.42) |

**Correlation by period:**
- Pre-COVID: r = -0.83 (strong inverse)
- Pandemic: r = -0.26 (weak, disrupted)
- Rate Hikes: r = -0.86 (strong inverse)
- 2024: r = 0.01 (no correlation—rates flat, permits fluctuating)

This is really interesting. The normal pattern (higher rates → fewer permits) was strong before COVID and during the rate hikes, but the pandemic period broke that pattern. During 2020-2021, permits actually surged despite rates being near zero—probably because of the remote-work housing boom and stimulus effects. That's exactly what we hypothesized in our project plan.

---

## Updated Timeline

| Target Date | Task | Status | Owner |
|------------|------|--------|-------|
| Week 1 | Project plan finalized | Complete | Sam & Everett |
| Week 2 | Data acquisition scripts | Complete | Sam |
| Week 3 | Data profiling & cleaning | Complete | Everett |
| Week 4 | Data integration | Complete | Sam |
| Week 5 | Exploratory analysis & visualization | In Progress (80%) | Everett |
| Week 6 | Statistical modeling (if needed) | Complete? | Sam |
| Week 7 | Final report writing | Pending | Sam & Everett |
| Week 8 | Review, polish, and submit | Pending | Sam & Everett |

We're actually ahead of schedule. The exploratory analysis that was planned for Week 5 is mostly done, and we've already got preliminary statistical results.

---

## Changes to Project Plan

Based on Milestone 2 feedback ("Great work. Don't forget to fill the rest of the timelines"), we've expanded the timeline to include Weeks 6-8 with specific tasks and owners.

**Other changes:**
- We decided to use Matplotlib and Seaborn for visualizations instead of Plotly. Matplotlib gave us better control over dual-axis plots and was simpler to set up for static images.
- We added a `period` labeling system to the integrated data that wasn't in the original plan. This made it much easier to compare behavior across different economic eras.
- We haven't added mortgage rate data (MORTGAGE30US) yet. We'll revisit this in Week 6 if we have time, but the core rate-to-permits analysis is working well without it.

---

## Challenges and Solutions

### Challenge 1: API Key Management

**Problem:** We needed to use the FRED API key without committing it to the repo.

**Solution:** For reproducibility, anyone running the code would need to supply their own FRED API key (it's free to get one from the FRED website). We documented this in the README.

### Challenge 2: Pandemic Period Distorting Correlation

**Problem:** When we first ran the overall correlation, it seemed weaker than expected (r = -0.41). We thought the relationship should be stronger based on economic theory.

**Solution:** We broke the analysis down by period and discovered the pandemic years (2020-2021) were muddying the relationship. During that time, rates were near zero but permits were all over the place due to supply chain chaos and the remote-work housing boom. When we look at just the pre-COVID or rate-hike periods, the correlation is much stronger (r = -0.83 to -0.86). This is actually a more interesting finding than a simple overall correlation.

### Challenge 3: Choosing the Right Lag for Cross-Correlation

**Problem:** We wanted to know if there's a delay between rate changes and permit changes, but there are different ways to calculate cross-correlation.

**Solution:** We computed the correlation at every lag from -12 to +12 months. The strongest inverse correlation was at lag = -2 months, meaning building permits respond most strongly to rate changes about 2 months later. This makes intuitive sense—it takes time for rate changes to affect mortgage rates, for buyers to adjust, and for permit applications to reflect those changes.

---

## Individual Contributions

### Sam's Contributions

For this milestone, I focused on the data engineering side of the project:

- Wrote the `acquire_data.py` script that pulls data from the FRED API, handles errors, and saves raw CSVs with SHA-256 checksums
- Built the `integrate_data.py` script that merges the two datasets and adds derived columns for analysis
- Set up the project directory structure (`scripts/`, `data/`, `output/`)
- Created the `requirements.txt` file listing all Python dependencies
- Helped debug the cross-correlation calculation in the analysis script

I spent roughly 6 hours on coding and testing, plus another hour or two reviewing analysis work and documenting.

### Everett's Contributions

I handled most of the data quality and visualization work:

- Wrote the `profile_data.py` script to check both datasets for missing values, outliers, and data type issues
- Built most of the `analyze_data.py` script, including all four visualizations and the statistical tests
- Discovered the period-by-period correlation pattern that explains why the overall correlation seemed weaker than expected
- Documented the analysis findings in `output/analysis_summary.txt`
- Started drafting sections of this status report

I spent about 7 hours on the analysis and visualizations, plus another 2 hours on documentation.

---

## Next Steps

1. **Finish exploratory analysis** — Add a few more summary tables and possibly an interactive time slider if we have time
2. **Consider regression modeling** — We might fit a simple lagged regression to quantify how much a 1% rate increase affects permits after 2 months
3. **Write the final report** — Pull together findings, limitations, and conclusions
4. **Clean up documentation** — Make sure the README has full setup instructions and the code is well-commented

We're feeling good about where the project stands. The core analysis is done and showing interesting results, and we have a clear path to completion.

