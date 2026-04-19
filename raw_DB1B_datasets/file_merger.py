# This file combines the four quarterly DB1B datasets and aggregates passenger counts

import pandas as pd
import glob
import os

# Get the absolute path of the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Find files in that same folder (raw_DB1B)
file_pattern = os.path.join(script_dir, "DB1B_2024_Q*.csv")
file_list = glob.glob(file_pattern)

print(f"Found {len(file_list)} files to process")

summaries = []

for file in file_list:
    print(f"Processing {os.path.basename(file)}...")

    df = pd.read_csv(file)

    # Aggregate passenger count of a quarter DB1B file
    quarter_summary = df.groupby(['ORIGIN', 'DEST'])['PASSENGERS'].sum().reset_index()
    summaries.append(quarter_summary)

# Combine and save to the 'datasets' folder (one level up from this script)
if summaries:
    annual_data = pd.concat(summaries)
    final_total = annual_data.groupby(['ORIGIN', 'DEST'])['PASSENGERS'].sum().reset_index()

    # Join path to go up one level, then into 'datasets'
    output_path = os.path.join(script_dir, "..", "datasets", "DB1B_2024_consolidated.csv")

    final_total.to_csv(output_path, index=False)
    print(f"Final file saved at {output_path}")