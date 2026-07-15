import pandas as pd
import glob
import os

# Get absolute path of the folder where this script lives
script_dir = os.path.dirname(os.path.abspath(__file__))

# Find files in that same folder
file_pattern = os.path.join(script_dir, "*.parquet")
file_list = glob.glob(file_pattern)

# Fill db1c_list
target_column_list = ["SchFlYear", "SchFlMonth", "Origin", "Dest", "Passengers"]
db1c_list = [pd.read_parquet(file, columns=target_column_list) for file in file_list]

# Concatenate each df in db1c_list
db1c_df = pd.concat(db1c_list)

# Sum up passenger counts for a unique route
db1c_df = (
    db1c_df.groupby(["SchFlYear", "SchFlMonth", "Origin", "Dest"])["Passengers"]
    .sum()
    .reset_index()
)

# Convert floats to int64 data type
db1c_df[["SchFlYear", "SchFlMonth", "Passengers"]] = db1c_df[
    ["SchFlYear", "SchFlMonth", "Passengers"]
].astype("int64")

# Set the output path for the final csv
output_path = os.path.join(script_dir, "..", "final_db1c.csv")

# Output final_db1c.csv
db1c_df.to_csv(output_path, index=False)
