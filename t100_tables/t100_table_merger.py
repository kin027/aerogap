import pandas as pd
import glob
import os

# Get absolute path of the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Find files in that same folder
file_pattern = os.path.join(script_dir, "*.csv")
file_list = glob.glob(file_pattern)

# Hint that processed_chunks holds DataFrames
processed_chunks: list[pd.DataFrame] = []

# Process each parquet file individually
for file in file_list:
    monthly_t100_df = pd.read_csv(file).rename(
        columns={
            "ORIGIN_CITY_MARKET_ID": "ORIGIN_MARKET_ID",
            "DEST_CITY_MARKET_ID": "DEST_MARKET_ID",
        }
    )

    # Drop rows missing at least one value
    monthly_t100_df = monthly_t100_df.dropna()

    # Drop rows outside of date range
    date_filter = (
            ((monthly_t100_df["YEAR"] == 2026) & (monthly_t100_df["MONTH"] <= 7)) |
            ((monthly_t100_df["YEAR"] == 2025) & (monthly_t100_df["MONTH"] >= 7))
    )
    monthly_t100_df = monthly_t100_df[date_filter]

    # Drop coterminals
    monthly_t100_df = monthly_t100_df[monthly_t100_df["ORIGIN_MARKET_ID"] != monthly_t100_df["DEST_MARKET_ID"]]

    # Convert all numeric columns to type int32
    numeric_cols = monthly_t100_df.select_dtypes(include="number").columns
    monthly_t100_df[numeric_cols] = monthly_t100_df[numeric_cols].astype("int32")

    # Drop unscheduled departures such as diversions
    monthly_t100_df = monthly_t100_df[
        monthly_t100_df["DEPARTURES_SCHEDULED"] > 0
        ]

    # Drop non-passenger flights
    monthly_t100_df = monthly_t100_df[
        monthly_t100_df["SEATS"] > 0
        ]

    # Drop non-scheduled flights (Scheduled Passenger/ Cargo Service is F)
    monthly_t100_df = monthly_t100_df[
        monthly_t100_df["CLASS"] == "F"
        ]

    # Append each df into processed_chunks
    processed_chunks.append(monthly_t100_df)

# Concatenate chunks
t100_df = pd.concat(processed_chunks, ignore_index=True)

# Keep only important columns
t100_df = t100_df[["YEAR", "MONTH", "ORIGIN", "ORIGIN_MARKET_ID", "DEST", "DEST_MARKET_ID"]]

# Drop duplicate rows
t100_df = t100_df.drop_duplicates(subset=["YEAR", "MONTH", "ORIGIN", "DEST"])

# Set the output path for the final csv
output_path = os.path.join(script_dir, "..", "final_t100.csv")

# Output final_t100.csv
t100_df.to_csv(output_path, index=False)
