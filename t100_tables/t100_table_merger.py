import pandas as pd
import glob
import os

# Get absolute path of the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Find files in that same folder
file_pattern = os.path.join(script_dir, "*.csv")
file_list = glob.glob(file_pattern)

processed_chunks = []
t100_df = pd.DataFrame()

# Process each parquet file individually
for file in file_list:
    df = pd.read_csv(file).rename(
        columns={
            "ORIGIN_CITY_MARKET_ID": "ORIGIN_MARKET_ID",
            "DEST_CITY_MARKET_ID": "DEST_MARKET_ID",
        }
    )

    # CLEAN DATA

    # Filter date range first (July 2025 to May 2026)
    date_filter = (
            ((df["YEAR"] == 2026) & (df["MONTH"] <= 5)) |
            ((df["YEAR"] == 2025) & (df["MONTH"] >= 7))
    )
    df = df[date_filter]

    # Drop coterminals
    df = df[df["ORIGIN_MARKET_ID"] != df["DEST_MARKET_ID"]]

    # Drop unscheduled departures such as diversions
    df = df[
        df["DEPARTURES_SCHEDULED"] > 0
        ]

    # Drop non-passenger flights
    df = df[
        df["SEATS"] > 0
        ]

    # Drop non-scheduled flights (Scheduled Passenger/ Cargo Service is F)
    df = df[
        df["CLASS"] == "F"
        ]

    # Append each df into processed_chunks
    processed_chunks.append(df)

if processed_chunks:
    t100_df = pd.concat(processed_chunks, ignore_index=True)
else:
    t100_df = pd.DataFrame()

# Keep only important columns
t100_df = t100_df[["YEAR", "MONTH", "ORIGIN", "ORIGIN_MARKET_ID", "DEST", "DEST_MARKET_ID"]]

# Drop NA values
t100_df = t100_df.dropna()

# Drop duplicate rows
t100_df = t100_df.drop_duplicates(subset=["YEAR", "MONTH", "ORIGIN", "DEST"])

# Set the output path for the final csv
output_path = os.path.join(script_dir, "..", "final_t100.csv")

# Output final_t100.csv
t100_df.to_csv(output_path, index=False)
