import pandas as pd
import calendar
import glob
import os

# Get absolute path of the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Find files in that same folder
file_pattern = os.path.join(script_dir, "*.parquet")
file_list = glob.glob(file_pattern)

target_column_list = ["SchFlYear", "SchFlMonth", "Origin", "OriginCityMarketID", "Dest",
                      "DestCityMarketID",
                      "Passengers", "MktAmount"]

# Hint that processed_chunks holds DataFrames
processed_chunks: list[pd.DataFrame] = []

# Process each parquet file individually
for file in file_list:
    monthly_db1c_df = pd.read_parquet(file, columns=target_column_list).rename(
        columns={
            "SchFlYear": "YEAR",
            "SchFlMonth": "MONTH",
            "Origin": "ORIGIN",
            "OriginCityMarketID": "ORIGIN_MARKET_ID",
            "Dest": "DEST",
            "DestCityMarketID": "DEST_MARKET_ID",
            "Passengers": "PASSENGERS",
            "MktAmount": "MKT_AMOUNT"
        }
    )

    # Drop rows missing at least one value
    monthly_db1c_df = monthly_db1c_df.dropna()

    # Drop rows outside of date range
    date_filter = (
            ((monthly_db1c_df["YEAR"] == 2026) & (monthly_db1c_df["MONTH"] <= 7)) |
            ((monthly_db1c_df["YEAR"] == 2025) & (monthly_db1c_df["MONTH"] >= 7))
    )
    monthly_db1c_df = monthly_db1c_df[date_filter]

    # Drop coterminals
    monthly_db1c_df = monthly_db1c_df[
        monthly_db1c_df["ORIGIN_MARKET_ID"] != monthly_db1c_df["DEST_MARKET_ID"]]

    # Convert all numeric columns to type int32
    numeric_cols = monthly_db1c_df.select_dtypes(include="number").columns
    monthly_db1c_df[numeric_cols] = monthly_db1c_df[numeric_cols].astype("int32")

    # Append each df into processed_chunks
    processed_chunks.append(monthly_db1c_df)

# Concatenate chunks
db1c_df = pd.concat(processed_chunks, ignore_index=True)

# Sum up passenger counts for a market pair (doing this here or else the final file
# would be huge)
db1c_df = db1c_df.groupby(["YEAR", "MONTH", "ORIGIN_MARKET_ID", "DEST_MARKET_ID"]).agg(
    PASSENGERS=("PASSENGERS", "sum"),
    ORIGIN_MARKET_AIRPORTS=("ORIGIN", lambda x: ", ".join(sorted(set(x)))),
    DEST_MARKET_AIRPORTS=("DEST", lambda x: ", ".join(sorted(set(x))))
).reset_index()

# Read market ID lookup CSV
markets_df = \
    pd.read_csv(os.path.join(script_dir, "..", "L_CITY_MARKET_ID.csv")).set_index(
        "Code")[
        "Description"]

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

# Create new MONTH_NAME column for month name
db1c_df["MONTH_NAME"] = db1c_df["MONTH"].map(
    lambda x: calendar.month_name[x]
)

# Create new SCALED_PASSENGERS column that multiplies passenger counts by 2.5,
# as DB1C is a 40% sample of tickets
db1c_df["SCALED_PASSENGERS"] = (db1c_df["PASSENGERS"] * 2.5).round().astype("int32")

# Get number of days in a month
days_in_month = pd.to_datetime(
    db1c_df[["YEAR", "MONTH"]].assign(DAY=1)
).dt.days_in_month

# Create new PASSENGERS_DAILY column
db1c_df["PASSENGERS_DAILY"] = (db1c_df["SCALED_PASSENGERS"] / days_in_month).round(2)

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
