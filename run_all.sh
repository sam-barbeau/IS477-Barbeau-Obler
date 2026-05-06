#!/usr/bin/env bash

set -e

if [ ! -f fredapi.txt ]; then
    echo "ERROR: fredapi.txt not found. Get a free key at https://fred.stlouisfed.org/docs/api/api_key.html"
    echo "and save it to fredapi.txt before running."
    exit 1
fi

echo "Step 1: acquire data from FRED"
python scripts/acquire_data.py

echo
echo "Step 2: profile raw data"
python scripts/profile_data.py

echo
echo "Step 3: integrate (merge) datasets"
python scripts/integrate_data.py

echo
echo "Step 4: analyze and generate figures"
python scripts/analyze_data.py
