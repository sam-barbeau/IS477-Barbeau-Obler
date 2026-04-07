import requests
import pandas as pd
import hashlib
import json
from pathlib import Path

# FRED API configuration - read key from local file (not committed to repo)
with open("fredapi.txt", "r") as f:
    API_KEY = f.read().strip()
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

# Date range for our analysis
START_DATE = "2019-01-01"
END_DATE = "2024-12-31"

# Series we're pulling
SERIES_INFO = {
    "FEDFUNDS": {
        "name": "Federal Funds Rate",
        "description": "Effective Federal Funds Rate, monthly average"
    },
    "PERMIT": {
        "name": "Building Permits",
        "description": "New Private Housing Units Authorized by Building Permits (thousands, SAAR)"
    }
}

def fetch_fred_series(series_id):
    """Fetch a single series from FRED API and return as DataFrame"""
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "observation_start": START_DATE,
        "observation_end": END_DATE
    }
    
    print(f"Fetching {series_id} from FRED...")
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    
    data = response.json()
    observations = data["observations"]
    
    # Convert to DataFrame
    df = pd.DataFrame(observations)
    df = df[["date", "value"]]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    
    # Rename value column to something meaningful
    df = df.rename(columns={"value": series_id.lower()})
    
    print(f"  Retrieved {len(df)} observations from {df['date'].min()} to {df['date'].max()}")
    
    return df

def compute_sha256(filepath):
    """Compute SHA-256 hash of a file"""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def save_with_checksum(df, filepath, description):
    """Save DataFrame to CSV and compute checksum"""
    df.to_csv(filepath, index=False)
    checksum = compute_sha256(filepath)
    print(f"  Saved to {filepath}")
    print(f"  SHA-256: {checksum}")
    return checksum

# Set up paths
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Fetch both series
fedfunds_df = fetch_fred_series("FEDFUNDS")
permit_df = fetch_fred_series("PERMIT")

# Save raw data
checksums = {}
checksums["fedfunds"] = save_with_checksum(
    fedfunds_df, 
    data_dir / "fedfunds_raw.csv",
    "Federal Funds Rate raw data"
)
checksums["permit"] = save_with_checksum(
    permit_df,
    data_dir / "permit_raw.csv", 
    "Building Permits raw data"
)

# Save checksums to a JSON file for reproducibility
with open(data_dir / "checksums.json", "w") as f:
    json.dump(checksums, f, indent=2)
print(f"\nChecksums saved to {data_dir / 'checksums.json'}")

# Quick data summary
print("\n--- Data Summary ---")
print(f"Federal Funds Rate: {len(fedfunds_df)} months, range {fedfunds_df['fedfunds'].min():.2f}% to {fedfunds_df['fedfunds'].max():.2f}%")
print(f"Building Permits: {len(permit_df)} months, range {permit_df['permit'].min():.0f}K to {permit_df['permit'].max():.0f}K units")
