import pandas as pd
import glob
import os

# Get the absolute path of the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Find files in that same folder
file_pattern = os.path.join(script_dir, "*.parquet")
file_list = glob.glob(file_pattern)

db1c_list = []
target_column_list = ["SchFlYear", "SchFlMonth", "Origin", "Dest", "Passengers"]

for file in file_list:
    print(f"Processing {os.path.basename(file)}...")

    # Convert to a DataFrame
    single_df = pd.read_parquet(file, columns=target_column_list)

    # Append to array
    db1c_list.append(single_df)

# Concatenate each df in the db1c_list array
db1c_df = pd.concat(db1c_list)

# Sum up passenger counts for a unique route again due duplication of routes within and between months
db1c_df = (
    db1c_df.groupby(["SchFlYear", "SchFlMonth", "Origin", "Dest"])["Passengers"]
    .sum()
    .reset_index()
)

# Set the output path for the final csv
output_path = os.path.join(script_dir, "..", "final_db1c.csv")

# Output final_db1c.csv
db1c_df.to_csv(output_path, index=False)
