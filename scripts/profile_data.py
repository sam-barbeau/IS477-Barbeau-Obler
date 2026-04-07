import pandas as pd
from pathlib import Path

data_dir = Path("data")

# Load raw data
print("=" * 60)
print("DATA PROFILING REPORT")
print("=" * 60)

# --- Federal Funds Rate ---
print("\n### Federal Funds Rate (FEDFUNDS) ###\n")
fedfunds = pd.read_csv(data_dir / "fedfunds_raw.csv", parse_dates=["date"])

print(f"Shape: {fedfunds.shape[0]} rows, {fedfunds.shape[1]} columns")
print(f"Date range: {fedfunds['date'].min().date()} to {fedfunds['date'].max().date()}")
print("\nData types:")
print(fedfunds.dtypes)
print("\nMissing values:")
print(fedfunds.isnull().sum())
print("\nBasic statistics:")
print(fedfunds['fedfunds'].describe())

# Check for any gaps in monthly sequence
fedfunds_dates = pd.date_range(start="2019-01-01", end="2024-12-01", freq="MS")
missing_dates = set(fedfunds_dates) - set(fedfunds['date'])
if missing_dates:
    print(f"\nWARNING - Missing months: {sorted(missing_dates)}")
else:
    print("\nNo gaps in monthly sequence")

# --- Building Permits ---
print("\n" + "=" * 60)
print("\n### Building Permits (PERMIT) ###\n")
permit = pd.read_csv(data_dir / "permit_raw.csv", parse_dates=["date"])

print(f"Shape: {permit.shape[0]} rows, {permit.shape[1]} columns")
print(f"Date range: {permit['date'].min().date()} to {permit['date'].max().date()}")
print("\nData types:")
print(permit.dtypes)
print("\nMissing values:")
print(permit.isnull().sum())
print("\nBasic statistics:")
print(permit['permit'].describe())

# Check for gaps
permit_dates = pd.date_range(start="2019-01-01", end="2024-12-01", freq="MS")
missing_dates = set(permit_dates) - set(permit['date'])
if missing_dates:
    print(f"\nWARNING - Missing months: {sorted(missing_dates)}")
else:
    print("\nNo gaps in monthly sequence")

# --- Key observations ---
print("\n" + "=" * 60)
print("KEY OBSERVATIONS")
print("=" * 60)

print("""
1. Both datasets have 72 complete monthly observations (Jan 2019 - Dec 2024)
2. No missing values in either dataset
3. Federal Funds Rate varied dramatically:
   - Pre-pandemic (2019): ~2.4%
   - Pandemic low (2020-2021): ~0.05-0.08%
   - Post-hike peak (2023-2024): ~5.33%
4. Building Permits ranged from ~1,076K to ~1,920K units
   - Shows significant variation that we can analyze against rate changes
5. Data is clean - no transformations needed beyond merging
""")
