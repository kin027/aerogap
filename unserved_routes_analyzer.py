# Class for analyzing
import pandas as pd

class UnservedRoutesAnalyzer:
    def __init__(self, db1b_path, t100_path):
        # Read both DB1B and T-100 CSVs first
        self.DB1B_df = pd.read_csv(db1b_path)
        self.T100_df = pd.read_csv(t100_path)

        # Get a set of valid origin airport codes
        self.origin_airports_set = set(self.DB1B_df.ORIGIN)

    # Method to validate user-entered origin airport input
    def check_valid_origin_airport(self, origin_airport):
        if origin_airport in self.origin_airports_set:
            result = True
        else:
            result = False

        return result

    # "Main" analyzer method
    def analyze_unserved_routes(self, origin_airport):
        # Validate origin_airport
        validation_result = self.check_valid_origin_airport(origin_airport)
        if not validation_result: # Invalid airport
            # Print error message
            print("Airport not found, does not have scheduled commercial air service, or is not in the U.S.")

            # Stop method from proceeding
            return

        # Origin airport is validated, continue analyzing

        # Filter DB1B_df down to rows where origin airport is same as user input
        filtered_DB1B_df = self.DB1B_df[self.DB1B_df.ORIGIN == origin_airport].copy()

        # Create new column that multiplies passenger counts by 10, as DB1B is a 10% sample of tickets
        filtered_DB1B_df["passengers_times_10"] = filtered_DB1B_df["PASSENGERS"] * 10

        # Sort the df by passenger counts, highest to lowest, using merge sort
        filtered_DB1B_df.sort_values(by="passengers_times_10", ascending=False, inplace=True, kind="mergesort")

        # Filter T100_df down to rows where origin airport is same as user input and passengers > 0 (as T100 contains cargo
        # flights)
        filtered_T100_df = self.T100_df[(self.T100_df.ORIGIN == origin_airport) & (self.T100_df.PASSENGERS > 0)]

        # Create a new column of boolean values in filtered_DB1B_df that indicates whether a route has a nonstop flight
        # by cross-checking with T100_df, which indicates whether a nonstop flight exists
        filtered_DB1B_df["has_nonstop_flight"] = filtered_DB1B_df["DEST"].isin(filtered_T100_df["DEST"])

        # Filter filtered_DB1B_df down to rows where "has_nonstop_flight" is false
        filtered_DB1B_df_2 = filtered_DB1B_df[filtered_DB1B_df["has_nonstop_flight"] == False]

        # Print DB1B_df (for now)
        print(filtered_DB1B_df_2)

        # Done
        return

