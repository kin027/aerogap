import pandas as pd

# Ask user for airport code
origin_airport = input("Enter a three-character IATA airport code: ")

# Convert user input to uppercase
origin_airport_upper = origin_airport.upper()

# Read consolidated DB1B CSV file with pandas
DB1B_df = pd.read_csv("final_datasets/DB1B_2024_consolidated.csv")

# Get all ORIGIN airports as a Series and drop duplicates
origin_airports_series = DB1B_df.ORIGIN.drop_duplicates()

# Convert this Series to a list
origin_airports_list = origin_airports_series.to_list()

# Perform input validation based on this list
if origin_airport_upper in origin_airports_list:
    # Create new df that filters down to rows where origin airport is user input
    filtered_DB1B_df = DB1B_df[DB1B_df.ORIGIN == origin_airport_upper]

    # Create new column that multiplies passenger counts by 10, as DB1B is a 10% sample of tickets
    filtered_DB1B_df["passengers_times_10"] = filtered_DB1B_df["PASSENGERS"] * 10

    # Sort the df by passenger counts, highest to lowest, using merge sort
    filtered_DB1B_df.sort_values(by = "passengers_times_10", ascending = False, inplace = True, kind = "mergesort")

    # Print df (for now)
    print(filtered_DB1B_df)

else: # Invalid airport
    # Print error message
    print("Airport not found, does not have scheduled commercial air service, or is not in the U.S.")