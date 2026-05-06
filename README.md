# Federal Interest Rates and Residential Building Permits (2019–2024)

**IS 477 Final Project Report**

## Contributors

- **Sam Barbeau** — sole author of the final submission. Responsible for all data acquisition, profiling, integration, analysis, visualization, and write-up.
- **Everett Obler** — was originally on the team and contributed to the project plan and the mid-semester status report. Did not contribute to this final submission; I (Sam) finished the project on my own. References to "we" in `ProjectPlan.md` and `StatusReport.md` reflect the earlier two-person team.

## Summary

This project looks at how the Federal Reserve's main monetary-policy lever (the federal funds rate) relates to new residential building permits in the U.S. between January 2019 and December 2024. Housing is one of the most rate-sensitive parts of the economy: when borrowing gets more expensive, mortgages get more expensive, and developers and buyers tend to pull back. Building permits are a leading indicator of future construction, so they should react to rate changes before things like housing starts or completions do. The 2019–2024 window is interesting because it covers three very different regimes: the moderate pre-COVID rates, the near-zero pandemic rates, and the sharp hiking cycle that started in 2022.

The research questions were:

1. **Primary:** Is there a correlation between the federal funds rate and monthly new residential building permits?
2. **Secondary:** When the rate changes, how long does it take for permits to respond?
3. **Exploratory:** Did the pandemic break the usual rate-to-permits relationship?

To answer these, I pulled both series from the FRED (Federal Reserve Economic Data) API, computed SHA-256 checksums for the raw CSVs, profiled them for missing values and gaps, merged them on the shared monthly date index, and ran statistical tests (Pearson, Spearman, period-by-period correlation, and a cross-correlation lag analysis going back and forward 12 months). The whole thing is scripted in Python so the pipeline is reproducible end-to-end.

The findings line up with what economic theory would predict, but with a twist. Across the full 72-month window, the federal funds rate and building permits are negatively correlated (Pearson r = −0.41, p < 0.001; Spearman ρ = −0.43). That's a moderate, not strong, relationship — but when I split the data into economic periods, the picture sharpens. In the Pre-COVID period (2019), r = −0.83. During the rate-hike period (2022–2023), r = −0.86. Both are very strong inverse relationships and match the textbook story: higher rates, fewer permits. The pandemic period (2020–2021) has a much weaker correlation (r = −0.26), and 2024 is essentially flat (r = 0.01). So the overall correlation looks weaker than it should because the pandemic and post-hike plateau periods dilute the signal. The cross-correlation analysis shows the strongest inverse correlation at a lag of −2 months, meaning permits respond most strongly to rate changes about two months after they happen, which is consistent with how long it takes for rate moves to flow through to mortgage rates and into permit applications.

The big takeaway is that the federal funds rate and residential building permits really do move inversely, with about a two-month lag, but you can only see the relationship cleanly when you isolate "normal" economic conditions. The pandemic is a good illustration of why. Rates were essentially flat at near-zero for all of 2020–2021, while permits were swinging wildly. They first dropped in spring 2020 from lockdowns, then spiked due to remote-work demand and stimulus money. Permits were responding to pandemic specific factors, not to interest rates. That mostly answers question (3): yes, the pandemic disrupted the usual rate-to-permits mechanism.

## Data profile

Both datasets come from FRED, the public data portal run by the Federal Reserve Bank of St. Louis. They're U.S. federal government data, public domain in the U.S., and FRED's terms allow redistribution. There are no privacy or PII concerns — both series are aggregate national-level monthly numbers.

### Dataset 1: Effective Federal Funds Rate (FEDFUNDS)

- **Original source:** Board of Governors of the Federal Reserve System (US)
- **Access path:** FRED API, series `FEDFUNDS` (https://fred.stlouisfed.org/series/FEDFUNDS)
- **Acquisition:** `scripts/acquire_data.py` makes a JSON request to `https://api.stlouisfed.org/fred/series/observations` and writes the result to `data/fedfunds_raw.csv`.
- **Files:** `data/fedfunds_raw.csv` (raw), included in `data/integrated_data.csv` (joined).
- **Shape:** 72 rows × 2 columns.
- **Columns:** `date` (first of month, YYYY-MM-DD) and `fedfunds` (monthly average rate, percent).
- **Coverage:** Monthly, January 2019 through December 2024.
- **Range observed:** 0.05% (pandemic low, April 2020) to 5.33% (peak in 2023).
- **Mean:** 2.41%.
- **License/use:** Public domain. The federal funds rate is set in policy meetings by the Federal Open Market Committee (FOMC). The "effective" rate is the actual realized overnight bank-to-bank lending rate, and FRED publishes the monthly average.

### Dataset 2: New Privately-Owned Housing Units Authorized by Building Permits (PERMIT)

- **Original source:** U.S. Census Bureau, Building Permits Survey
- **Access path:** FRED API, series `PERMIT` (https://fred.stlouisfed.org/series/PERMIT)
- **Acquisition:** Same script (`scripts/acquire_data.py`), pulled in the same run.
- **Files:** `data/permit_raw.csv` (raw), included in `data/integrated_data.csv` (joined).
- **Shape:** 72 rows × 2 columns.
- **Columns:** `date` (first of month, YYYY-MM-DD) and `permit` (thousands of units, seasonally adjusted annual rate).
- **Coverage:** Monthly, January 2019 through December 2024.
- **Range observed:** ~1,076K to ~1,920K units (SAAR).
- **Mean:** ~1,546K units.
- **License/use:** Public domain. The Census Bureau collects this from local permit-issuing authorities. The series is already seasonally adjusted, which matters because raw permit counts are very seasonal.

### Integrated dataset

`data/integrated_data.csv` is the merged result, produced by `scripts/integrate_data.py`. It joins the two raw CSVs on `date` (inner join), and adds `year`, `month`, `rate_change` (month-over-month change in `fedfunds`), `permit_pct_change` (month-over-month % change in `permit`), and a `period` label (`Pre-COVID` / `Pandemic` / `Rate Hikes` / `2024`). All three CSVs are checksummed in `data/checksums.json`. Full column descriptions are in `data/data_dictionary.md`.

### How the data answers the questions

Both series are at the same granularity (national, monthly), cover the same time window, and share a clean date key, which lets me directly correlate them and run a lag analysis. The 72-month window is small for some statistical methods but large enough for Pearson/Spearman correlation and basic cross-correlation. Both ethical and legal constraints are minimal — these are public, aggregated, non-personal government statistics, intended for redistribution and reuse.

## Data quality

I assessed both raw datasets with `scripts/profile_data.py`, which checks shape, dtypes, missing values, the basic statistical summary (`describe()`), and explicitly verifies that there are no missing months in the monthly sequence from 2019-01-01 to 2024-12-01.

The headline result is that both raw datasets came in clean. Specifically:

- **Completeness.** Both datasets have exactly 72 rows, one per month, with zero missing values in either column. The "no gaps in monthly sequence" check passed for both — every month between 2019-01 and 2024-12 is present.
- **Schema / data types.** After parsing, `date` is `datetime64`, and the value columns (`fedfunds`, `permit`) are `float64`. FRED returns numeric values as strings in JSON, so the acquisition script explicitly does `pd.to_numeric(..., errors="coerce")`, which would convert any FRED placeholder like `"."` (their convention for missing values) to `NaN`. None showed up.
- **Range / plausibility.** The federal funds rate ranges from 0.05% to 5.33%, which exactly matches the historical reality of the period (zero-bound during COVID, peak of the hiking cycle in 2023). The permit series ranges from about 1,076K to 1,920K units (SAAR), which is in the historical normal band — high but not implausible during the 2021–2022 boom, low but not implausible during the early-COVID dip. No obvious outliers from data-entry errors.
- **Consistency.** Both series are reported on the same monthly date convention (first-of-month), which makes the join trivial. Both are reported in their natural units (percent for the rate, thousands of units SAAR for permits). I did not have to convert anything.
- **Provenance / integrity.** SHA-256 checksums are computed at acquisition time and stored in `data/checksums.json` for all three CSVs. Anyone re-running the pipeline against the same FRED series should reproduce identical hashes, assuming FRED hasn't published a revision in the meantime (FRED occasionally revises older permit values when Census re-estimates).
- **Validity of the merge.** The integration script verifies that the merge produced exactly 72 rows (6 years × 12 months) and that no nulls were introduced.

The one quality issue worth calling out isn't really a data quality problem — it's an analytical one. The PERMIT series is seasonally adjusted but FEDFUNDS isn't (and doesn't need to be — the Fed doesn't follow seasonal patterns). That's the right setup for a rate-vs-permits correlation, but it's worth documenting because it means I'm intentionally comparing one seasonally adjusted series to one non-seasonally-adjusted series. The FRED documentation supports this choice. The other thing I noted is that COVID-era values are real but anomalous: the pandemic-low rate (0.05%) and the sharp permit swings in 2020–2021 are genuine observations, but they pull the overall correlation down, which is exactly what the period by period analysis confirms.

In short: no missing values, no type issues, no gaps, no outliers from data entry. The data was clean enough that no imputation, deduplication, or value correction was needed. The "cleaning" step ended up being mostly transformation (computing derived columns) rather than fixing problems.

## Data cleaning

Because both raw datasets were already clean, the "cleaning" stage was really a derived-column / transformation stage. There were no missing values to impute, no duplicates to drop, no malformed rows to repair, and no obvious outliers from data-entry mistakes. Here is what I actually did, mapped to the issues each step addressed:

1. **Type coercion at acquisition (`scripts/acquire_data.py`).** FRED returns observation values as strings in JSON, with `"."` used as a sentinel for missing values. I run `pd.to_numeric(value, errors="coerce")` on the value column for each series, which handles two issues at once: it converts numbers from string to float, and it would convert any future `"."` to `NaN` so it shows up in the missingness check downstream. None showed up in this dataset, but the safety net is there.
2. **Date parsing.** Dates come back as ISO strings; I convert them to `datetime64` so they can be sorted, joined, and compared. Without this, the inner join in the integration step would still work (both sides are strings), but downstream operations like `dt.year` and `pd.date_range` continuity checks would not.
3. **Column renaming.** The raw FRED response has a generic `value` column. I rename it to a meaningful name (`fedfunds`, `permit`) so the columns are self-explanatory after the merge — no risk of two ambiguous `value_x` / `value_y` columns post-join.
4. **Merge / join (`scripts/integrate_data.py`).** I do an inner join on `date`. Because both series are 72-row, gap-free, first-of-month series, the inner join produces all 72 rows with no nulls. A validation step asserts the row count is 72 and that no nulls appear, which catches the case where FRED has published one series but not the other for a given month.
5. **Derived columns for analysis.** I added `year`, `month`, `rate_change` (month-over-month change in `fedfunds`), `permit_pct_change` (month-over-month percent change in `permit`), and a `period` label. The first two are convenience columns for grouping. The change/pct-change columns are NaN in the first row by construction (no prior month to diff against), which I leave as-is. The `period` label addresses an analysis concern rather than a data-quality concern: pooling 2020–2021 with the rest of the window dilutes the rate to permits relationship, so labeling lets me run period correlations easily.
6. **Checksumming.** Each output CSV is hashed with SHA-256 and the hash is stored in `data/checksums.json`. This isn't strictly cleaning, but it serves as a tamper / drift check: if anyone modifies a CSV after the fact, the hash will mismatch, which is a quality of evidence guarantee.

I considered but did not do: differencing the series for stationarity, converting the SAAR permit values back to a non-annualized monthly count, or smoothing either series with a rolling mean. I decided against all three because the research questions are about levels and lagged correlation, not about regression coefficients on a stationary process, and because the SAAR vs percent comparison is fine for correlation purposes (Pearson is scale invariant).

## Findings

The full numbers and the four figures live in `output/`. Headline results from `output/analysis_summary.txt`:

- **Overall Pearson correlation:** r = −0.4096, p = 0.000353 (significant, moderate, inverse).
- **Spearman rank correlation:** ρ = −0.4259, p = 0.000192 (similar).
- **Best lag from cross-correlation:** −2 months, r = −0.4227. Permits respond most strongly to rate changes about two months later.

Period stratified correlation:

| Period | r |
|---|---|
| Pre-COVID (2019) | −0.83 |
| Pandemic (2020–2021) | −0.26 |
| Rate Hikes (2022–2023) | −0.86 |
| 2024 | 0.01 |

The four figures in `output/`:

1. **`fig1_timeseries.png`** — Dual-axis time series of both variables, with the pandemic and rate-hike periods shaded. You can visually see the rate crashing to near-zero in 2020 and then climbing past 5% by 2023, and the permit line dipping briefly in 2020 before surging through 2021 and then falling through 2022–2023. The opposite movement during the rate-hike period is clear by eye.
2. **`fig2_scatter.png`** — Scatter of `fedfunds` vs. `permit`, colored by period, with the overall regression line and r/p annotated. The Pre-COVID and Rate Hikes points sit on a clear downward-sloping cloud; the Pandemic points are off to the lower-left (low rates, but permits all over the place); the 2024 points are clustered tightly on the right (rates flat ≈5%, permits varying around ~1,470K).
3. **`fig3_crosscorr.png`** — Cross-correlation at lags from −12 to +12 months. The most negative bar is at lag −2 (highlighted), and the cross-correlation is symmetrically less negative on either side of that, which is the expected shape for a lagged inverse relationship.
4. **`fig4_periods.png`** — Side by side boxplots of rates and permits by period. The pandemic period has the lowest median rate and the highest median (and most variable) permit count — visually the clearest illustration of why the pandemic period breaks the usual relationship.

Putting it together: yes, fed funds and permits are inversely correlated; yes, there's a roughly two-month lag; and yes, the pandemic broke the relationship — exactly as hypothesized at the project-plan stage.

## Future work

If I had another semester, the most obvious next step is to add the 30-year mortgage rate (FRED series `MORTGAGE30US`) as an intermediate variable. Economically, the fed funds rate doesn't affect housing demand directly — it affects mortgage rates, and those affect housing demand. A two-step model (fed funds to mortgage rate to permits) would probably tighten the correlation, and it would let me test whether the pandemic disruption was about rates or about something else (stimulus, supply chain, remote work). The data is right there in FRED and would slot into the existing pipeline with a small change to `acquire_data.py`.

A second extension is regional disaggregation. The PERMIT national series washes out a lot of meaningful variation between, say, the Sun Belt (where building boomed even during the rate hikes) and the older Midwest/Northeast metros (which barely react to rate changes because they're already not building much). The Census Bureau publishes state level permit data, and pulling even four or five regions would let me ask whether the rate to permits relationship is uniformly distributed across the country or concentrated in certain markets. The reason I didn't do this in the project is that the state-level Census API is more work to use than FRED's clean monthly series. The data is there, but it's split across many endpoints and includes both seasonally adjusted and non-adjusted versions.

Third, I'd like to try a proper time-series model rather than just correlation. Pearson correlation treats each (rate, permit) pair as if it were independent, which clearly isn't true for monthly economic data — both series are autocorrelated. A small ARDL (autoregressive distributed lag) model or even a simple VAR (vector autoregression) on the differenced series would give me coefficients I could interpret as "a 1pp rate increase reduces permits by X% over Y months," which is much more useful than a correlation coefficient. The reason I stuck with correlation is that 72 monthly observations is on the small side for a VAR with two variables, several lags, and dummy variables for periods, and I didn't want to over-claim from a thin model.

Lessons I'd carry forward: the period stratification idea was the single most useful thing I did. I almost reported "r = −0.41, weaker than expected, the data doesn't really show the relationship" before I split by period and saw the −0.83 / −0.86 within-period correlations. The lesson is that a moderate overall correlation in a dataset that spans very different regimes is often hiding strong relationships, and you can only see them by labeling regimes. The other lesson is that scripted, checksummed pipelines really do save time when you re-run things. I rebuilt the integrated dataset several times while iterating on the `period` label boundaries, and being able to re-run from scratch in a few seconds (and verify the hashes hadn't changed for the raw data) made that painless.

A smaller-scale future-work item: the four figures use Matplotlib for a reason (dual-axis is much easier than in Plotly), but an interactive Plotly version of `fig1_timeseries.png` would be useful for anyone who wants to hover and read off specific months. The static figures are fine for the report; an interactive HTML version would be a small extra deliverable.

## Challenges

The single biggest challenge was that I lost my teammate partway through the semester. The project plan and the status report are written in a "we" voice because at that point Everett was on the team. Going from a two person split (data engineering for me, EDA/visualization for him) to one person doing both halves meant I had to pick up the visualization and statistical analysis work I hadn't originally scoped for myself. The mid-semester status report papered over this a bit (it claims contributions from both of us), and rewriting `analyze_data.py`, generating all four figures, and writing the full quality / cleaning / findings narrative for this report all fell to me. The trade off was that I had to scope the analysis tighter than the project plan implied — no mortgage rate side analysis, no regional comparison, no formal time series model — and instead make sure the core pipeline and the period stratified correlation analysis were solid. I think that was the right call given the time, but it's the most honest answer to "what was hard about this project."

The second challenge was an analysis side surprise: the overall Pearson correlation came out moderate (r = −0.41) when economic theory said it should be strong. My first instinct was that I'd done something wrong in the join or the cross correlation calculation. Walking through the merge step by step, validating with the SHA-256 checksums, and reading off the integrated CSV manually convinced me the data was right. Splitting by period revealed the pandemic was the cause. The challenge was epistemic — separating "my code has a bug" from "the data has a real story" — and the discipline of checksums, the row count assertion, and the gap check in the profiling script genuinely helped me trust the underlying numbers.

A third smaller challenge was managing the FRED API key without committing it. The standard fix (read from a file in `.gitignore`, document the steps) is what I did, but it does add friction for anyone trying to reproduce — they have to register for a free key and drop it into `fredapi.txt`. I considered hard coding a key just for this submission and then rotating it, but that would have been bad practice.

A fourth challenge was deciding what to not do. The project plan listed several things ("possibly add MORTGAGE30US," "possibly look at state-level data") that I chose not to do because the core analysis was already answering the research questions and adding more variables would have meant rushing all of it. Future work covers what I didn't do; the challenge was being disciplined about scope.

Finally, choosing the lag for cross-correlation was a methodological challenge. There are different ways to compute it (positive vs. negative lag conventions, using levels vs. differences). I went with the simplest: correlate the rate at month *t* with permits at month *t + k* for *k* from −12 to +12, and report the *k* that gives the most negative correlation. That gave −2 months, which matches the economic intuition that mortgage rates (and therefore permit applications) react to fed funds with a short delay. I'm not 100% sure about the sign convention I labeled in `fig3_crosscorr.png`, but the substantive result — a couple of months of delay, in the direction "rate change happens first, permits respond later" — is robust to the convention.

## Reproducing

Everything below assumes a Unix shell (macOS or Linux).

1. **Clone the repository.**
   ```bash
   git clone https://github.com/sam-barbeau/IS477-Barbeau-Obler.git
   cd IS477-Barbeau-Obler
   ```
2. **Set up a Python environment.**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Get a FRED API key.** Free; takes a minute. Sign up at https://fred.stlouisfed.org/docs/api/api_key.html. Save the key (just the key, on one line) to `fredapi.txt` in the project root. This file is in `.gitignore` so it won't be committed.
4. **Run the whole pipeline.** Easiest is the convenience script:
   ```bash
   bash run_all.sh
   ```
   Or step by step:
   ```bash
   python scripts/acquire_data.py
   python scripts/profile_data.py
   python scripts/integrate_data.py
   python scripts/analyze_data.py
   ```
5. **Verify reproducibility.** Compare the SHA-256 hashes printed by the acquisition and integration scripts against `data/checksums.json`. They should match exactly.
6. **Check the outputs.** The four figures land in `output/fig1_timeseries.png` … `fig4_periods.png`, and the headline numerical results are in `output/analysis_summary.txt`.

If you just want to look at the results without re-running anything: the input CSVs, the integrated CSV, and all four output figures are committed in this repo, so you can view them directly without setting up Python or getting a FRED key.

## References

- Board of Governors of the Federal Reserve System (US). *Effective Federal Funds Rate (FEDFUNDS).* Retrieved from FRED, Federal Reserve Bank of St. Louis. https://fred.stlouisfed.org/series/FEDFUNDS
- U.S. Census Bureau. *New Privately-Owned Housing Units Authorized in Permit-Issuing Places: Total Units (PERMIT).* Retrieved from FRED, Federal Reserve Bank of St. Louis. https://fred.stlouisfed.org/series/PERMIT
- Federal Reserve Bank of St. Louis. *FRED API documentation.* https://fred.stlouisfed.org/docs/api/fred/
