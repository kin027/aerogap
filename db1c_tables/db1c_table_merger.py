import pandas as pd
import calendar
import glob
import os

# Get absolute path of the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Find files in that same folder
file_pattern = os.path.join(script_dir, "*.parquet")
file_list = glob.glob(file_pattern)

target_column_list = ["SchFlYear", "SchFlMonth", "Origin", "OriginCityMarketID", "Dest", "DestCityMarketID", "Passengers"]

processed_chunks = []
db1c_df = pd.DataFrame()

# Process each parquet file individually
for file in file_list:
    df = pd.read_parquet(file, columns=target_column_list).rename(
            columns={
                "SchFlYear": "YEAR",
                "SchFlMonth": "MONTH",
                "Origin": "ORIGIN",
                "OriginCityMarketID": "ORIGIN_MARKET_ID",
                "Dest": "DEST",
                "DestCityMarketID": "DEST_MARKET_ID",
                "Passengers": "PASSENGERS",
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

    # Append each df into processed_chunks
    processed_chunks.append(df)

if processed_chunks:
    db1c_df = pd.concat(processed_chunks, ignore_index=True)
else:
    db1c_df = pd.DataFrame(columns=target_column_list)

# Sum up passenger counts for a market pair (doing this here or else the final file would be huge)
db1c_df = db1c_df.groupby(["YEAR", "MONTH", "ORIGIN_MARKET_ID", "DEST_MARKET_ID"]).agg(
    PASSENGERS=("PASSENGERS", "sum"),
    ORIGIN_MARKET_AIRPORTS=("ORIGIN", lambda x: ", ".join(sorted(set(x)))),
    DEST_MARKET_AIRPORTS=("DEST", lambda x: ", ".join(sorted(set(x))))
).reset_index()

# Drop NA values
db1c_df = db1c_df.dropna()

# CREATE NEW COLUMNS

# Read market ID lookup CSV
markets_df = pd.read_csv(os.path.join(script_dir, "..", "L_CITY_MARKET_ID.csv")).set_index("Code")["Description"]

# Create new ORIGIN_MARKET_NAME column
db1c_df["ORIGIN_MARKET_NAME"] = (
    db1c_df["ORIGIN_MARKET_ID"]
    .map(markets_df)
    .fillna("")
    .astype(str)
    .replace(to_replace=r" \(Metropolitan Area\)", value="", regex=True)
)

# Create new DEST_MARKET_NAME column
db1c_df["DEST_MARKET_NAME"] = (
    db1c_df["DEST_MARKET_ID"]
    .map(markets_df)
    .fillna("")
    .astype(str)
    .replace(to_replace=r" \(Metropolitan Area\)", value="", regex=True)
)

# Convert floats to int64 data type
db1c_df[["YEAR", "MONTH"]] = db1c_df[["YEAR", "MONTH"]].astype("int64")

# Create new MONTH_NAME column for month name
db1c_df["MONTH_NAME"] = db1c_df["MONTH"].map(
    lambda x: calendar.month_name[x]
)

# Create new SCALED_PASSENGERS column that multiplies passenger counts by 2.5, as DB1C is a 40% sample of tickets
db1c_df["SCALED_PASSENGERS"] = (db1c_df["PASSENGERS"] * 2.5).round()

# Get number of days in a month
days_in_month = pd.to_datetime(
    db1c_df[["YEAR", "MONTH"]].assign(DAY=1)
).dt.days_in_month

# Create new PASSENGERS_DAILY column
db1c_df["PASSENGERS_DAILY"] = (db1c_df["SCALED_PASSENGERS"] / days_in_month).round(2)

# Convert floats to int64 data type
db1c_df[["PASSENGERS", "SCALED_PASSENGERS", "ORIGIN_MARKET_ID", "DEST_MARKET_ID"]] = db1c_df[["PASSENGERS", "SCALED_PASSENGERS", "ORIGIN_MARKET_ID", "DEST_MARKET_ID"]].astype("int64")

# Create new BAR_TEXT column
db1c_df["BAR_TEXT"] = (
            db1c_df["SCALED_PASSENGERS"].astype(str)
            + "<br>("
            + db1c_df["PASSENGERS_DAILY"].astype(str)
            + ")"
        )

# Sort by passenger counts
db1c_df = db1c_df.sort_values(
    by="SCALED_PASSENGERS", ascending=False
)

# Set the output path for the final csv
output_path = os.path.join(script_dir, "..", "final_db1c.csv")

# Output final_db1c.csv
db1c_df.to_csv(output_path, index=False)
