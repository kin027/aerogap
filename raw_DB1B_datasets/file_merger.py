# This program combines the four quarterly DB1B datasets and aggregates passenger counts, but does NOT multiply the passenger counts by 10

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

# For loop for each quarter DB1B file
for file in file_list:
    print(f"Processing {os.path.basename(file)}...")

    # Convert to a DataFrame
    df = pd.read_csv(file)

    # Sum up passenger counts for a unique route
    quarter_summary = df.groupby(['ORIGIN', 'DEST'])['PASSENGERS'].sum().reset_index()

    # Append to summaries array
    summaries.append(quarter_summary)

# Combine and save to the 'datasets' folder (one level up from this script)
if summaries:
    # Concatenate each df in the summaries array
    annual_data = pd.concat(summaries)

    # Sum up passenger counts for a unique route again due duplication of routes between quarters
    final_total = annual_data.groupby(['ORIGIN', 'DEST'])['PASSENGERS'].sum().reset_index()

    # Set the output path for the final csv
    output_path = os.path.join(script_dir, "..", "datasets", "DB1B_2024_consolidated.csv")

    # Convert the final_total df to the final csv
    final_total.to_csv(output_path, index=False)
    print(f"Final file saved at {output_path}")