import pandas as pd
import sys

if len(sys.argv) != 2:
        logger.error("Use: python3 read_full_parquet.py <parquet_file>")
        logger.info("Example: python3 read_full_parquet.py output/parquet/canada.parquet")
        sys.exit(1)
    
parquet_file = sys.argv[1]

# Full reading
print(pd.read_parquet(parquet_file))