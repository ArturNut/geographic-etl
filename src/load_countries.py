import pandas as pd
import sqlite3
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJ_DIR = SCRIPT_DIR.parent

CSV = Path(f"{PROJ_DIR}/data/raw/countries.csv")
DB = Path(f"{PROJ_DIR}/data/geography.db")

df = pd.read_csv(CSV)
with sqlite3.connect(DB) as conn:
    df.to_sql("countries", conn, if_exists="replace", index=False)
print(f"Uploaded to {DB}")