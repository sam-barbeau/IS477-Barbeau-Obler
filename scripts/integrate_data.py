import pandas as pd
import hashlib
import json
from pathlib import Path

data_dir = Path("data")

print("Loading raw datasets...")
fedfunds = pd.read_csv(data_dir / "fedfunds_raw.csv", parse_dates=["date"])
permit = pd.read_csv(data_dir / "permit_raw.csv", parse_dates=["date"])

print(f"FEDFUNDS: {len(fedfunds)} rows")
print(f"PERMIT: {len(permit)} rows")

# Merge on date (inner join - only keep dates in both)
print("\nMerging datasets on date...")
merged = pd.merge(fedfunds, permit, on="date", how="inner")

print(f"Merged dataset: {len(merged)} rows")
print(f"Date range: {merged['date'].min().date()} to {merged['date'].max().date()}")

# Validate - should have 72 rows (6 years * 12 months)
expected_rows = 72
if len(merged) == expected_rows:
    print(f"Row count matches expected ({expected_rows} months)")
else:
    print(f"WARNING: Expected {expected_rows} rows, got {len(merged)}")

# Check for any missing values after merge
if merged.isnull().sum().sum() == 0:
    print("No missing values in merged dataset")
else:
    print("WARNING: Missing values found:")
    print(merged.isnull().sum())

# Add some computed columns that might be useful for analysis
print("\nAdding derived columns...")

# Year and month for potential grouping
merged["year"] = merged["date"].dt.year
merged["month"] = merged["date"].dt.month

# Rate change from previous month
merged["rate_change"] = merged["fedfunds"].diff()

# Percent change in permits from previous month
merged["permit_pct_change"] = merged["permit"].pct_change() * 100

# Label the periods for easier analysis
def label_period(date):
    if date.year == 2019:
        return "Pre-COVID"
    elif date.year in [2020, 2021]:
        return "Pandemic"
    elif date.year in [2022, 2023]:
        return "Rate Hikes"
    else:
        return "2024"

merged["period"] = merged["date"].apply(label_period)

print("Added columns: year, month, rate_change, permit_pct_change, period")

# Save integrated dataset
output_path = data_dir / "integrated_data.csv"
merged.to_csv(output_path, index=False)

# Compute checksum
sha256 = hashlib.sha256()
with open(output_path, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        sha256.update(chunk)
checksum = sha256.hexdigest()

print(f"\nSaved integrated dataset to {output_path}")
print(f"SHA-256: {checksum}")

# Update checksums file
checksums_path = data_dir / "checksums.json"
with open(checksums_path, "r") as f:
    checksums = json.load(f)
checksums["integrated"] = checksum
with open(checksums_path, "w") as f:
    json.dump(checksums, f, indent=2)

# Preview the data
print("\n--- First 10 rows of integrated data ---")
print(merged.head(10).to_string())

print("\n--- Summary by period ---")
print(merged.groupby("period")[["fedfunds", "permit"]].agg(["mean", "min", "max"]).round(2))
