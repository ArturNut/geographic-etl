#!/usr/bin/env python3
"""
Downloads countries.csv from an open repository.
Source: https://github.com/dr5hn/countries-states-cities-database
"""

import requests
from pathlib import Path

URL = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/csv/countries.csv"

SCRIPT_DIR = Path(__file__).parent
RAW_DATA_DIR = SCRIPT_DIR.parent / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = RAW_DATA_DIR / "countries.csv"

def download_data():
    print(f"Downloads: {URL}")
    response = requests.get(URL)
    response.raise_for_status()

    with open(OUTPUT_FILE, "wb") as f:
        f.write(response.content)
    print(f"Saved: {OUTPUT_FILE}")

if __name__ == "__main__":
    download_data()