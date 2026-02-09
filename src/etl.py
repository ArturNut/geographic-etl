#!/usr/bin/env python3

"""
ETL script: execute SQL → save to Parquet or CSV.

Usage:
    python3 etl.py <db_file> <sql_file> <output_file>
"""

import logging
import sys
from pathlib import Path
import sqlite3
import pandas as pd

# Determine the path to the "logs" folder
SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)  # create a folder if it doesn't exist
LOG_FILE = LOG_DIR / "etl.log"

# Setting up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()  # + output to terminal
    ]
)
logger = logging.getLogger(__name__)

def run_etl(db_file: Path, sql_file: Path, output_file: Path):
    
    # --- Checking the existence of a database, db_file ---
    if not db_file.exists():
        logger.error(f"Error: *.db file not found: {db_file}")
        return

    # --- Checking if an SQL file exists ---
    if not sql_file.exists():
        logger.error(f"Error: SQL file not found: {sql_file}")
        return

    # --- Reading an SQL file ---
    try:
        with open(sql_file, "r", encoding="utf-8") as f:
            query = f.read()
    except Exception as e:
        logger.error(f"Error reading SQL file: {e}")
        return

    # --- Executing a request ---
    try:
        with sqlite3.connect(db_file) as conn:
            df = pd.read_sql_query(query, conn)
    except Exception as e:
        logger.error(f"SQL execution error: {e}")
        return

    # --- Determine the target folder ---
    suffix = output_file.suffix.lower()
    if suffix == ".csv":
        target_dir = SCRIPT_DIR.parent / "output" / "csv"
        target_path = target_dir / output_file.name
    elif suffix == ".parquet":
        target_dir = SCRIPT_DIR.parent / "output" / "parquet"
        target_path = target_dir / output_file.name
    else:
        logger.info(f"Unsupported file format:: {suffix}. Use .csv or .parquet")
        return
    
    # Create the required folder
    target_dir.mkdir(parents=True, exist_ok=True)

    # --- Saving in the desired format ---
    try:
        if suffix == ".csv":
            df.to_csv(target_path, index=False, encoding="utf-8")
            logger.info(f"The result is saved in CSV: {target_path}")
        elif suffix == ".parquet":
            df.to_parquet(target_path, index=False)
            logger.info(f"The result is saved in Parquet: {target_path}")        
    except Exception as e:
        logger.error(f"Recording error: {e}")

def main():
    
    if len(sys.argv) != 4:
        logger.error("Use: python3 etl.py <db_file> <sql_file> <output_file>")
        logger.info("Example: python3 data/geography.db queries/canada_info.sql canada.parquet")
        sys.exit(1)
    
    db_file = Path(sys.argv[1])
    sql_path = Path(sys.argv[2])
    output_path = Path(sys.argv[3])

    run_etl(db_file, sql_path, output_path)

if __name__ == "__main__":
    main()