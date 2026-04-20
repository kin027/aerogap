import pandas as pd

# Ask user for airport code
origin_airport = input("Enter a three-character IATA airport code: ")

# Convert user input to uppercase
origin_airport_upper = origin_airport.upper()

# Read consolidated DB1B CSV file with pandas
DB1B_df = pd.read_csv("final_datasets/DB1B_2024_consolidated.csv")

# Convert the series of origin airports to a set
origin_airports_list = set(DB1B_df.ORIGIN)

# Perform input validation based on this list
if origin_airport_upper in origin_airports_list:
    # Filter DB1B_df down to rows where origin airport is same as user input
    filtered_DB1B_df = DB1B_df[DB1B_df.ORIGIN == origin_airport_upper]

    # Create new column that multiplies passenger counts by 10, as DB1B is a 10% sample of tickets
    filtered_DB1B_df["passengers_times_10"] = filtered_DB1B_df["PASSENGERS"] * 10

    # Sort the df by passenger counts, highest to lowest, using merge sort
    filtered_DB1B_df.sort_values(by = "passengers_times_10", ascending = False, inplace = True, kind = "mergesort")

    # Read T-100 CSV file with pandas
    T100_df = pd.read_csv("final_datasets/T100_2024.csv")

    # Filter T100_df down to rows where origin airport is same as user input and passengers > 0 (as T100 contains cargo
    # flights)
    filtered_T100_df = T100_df[(T100_df.ORIGIN == origin_airport_upper) & (T100_df.PASSENGERS > 0)]

    # Create a new series of boolean values that indicate whether a route has a nonstop flight by cross-checking with
    # T100_df, which indicates whether a nonstop flight exists
    has_nonstop_series = filtered_DB1B_df["DEST"].isin(filtered_T100_df["DEST"])

    # Create new column in filtered_DB1B_df that pastes this series
    filtered_DB1B_df["has_nonstop_flight"] = has_nonstop_series

    # Filter filtered_DB1B_df down to rows where "has_nonstop_flight" is false
    filtered_DB1B_df_2 = filtered_DB1B_df[filtered_DB1B_df["has_nonstop_flight"] == False]

    # Print DB1B_df (for now)
    print(filtered_DB1B_df_2)

else: # Invalid airport
    # Print error message
    print("Airport not found, does not have scheduled commercial air service, or is not in the U.S.")