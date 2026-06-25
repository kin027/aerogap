# Class for analyzing
import pandas as pd
import matplotlib.pyplot as plt
import tkinter
from tkinter import simpledialog
from tkinter import messagebox

TITLE = "Popular Unserved Flight Routes"

class UnservedRoutesAnalyzer:
    def __init__(self, db1b_path, t100_path):
        # Read both DB1B and T-100 CSVs first
        self.DB1B_df = pd.read_csv(db1b_path)
        self.T100_df = pd.read_csv(t100_path)

        # Get a set of valid origin airport codes
        self.origin_airports_set = set(self.DB1B_df.ORIGIN)

    # Method to get airport code from user
    def get_origin_airport(self):
        # Create new Tkinter window then withdraw it
        window = tkinter.Tk()
        window.withdraw()

        # Ask user for airport code
        origin_airport = simpledialog.askstring(title = TITLE, prompt = "Enter a three-character IATA airport code:")

        if origin_airport is not None:
            # Convert user input to uppercase
            origin_airport = origin_airport.upper()

            # Call method to validate origin airport
            self.check_valid_origin_airport(origin_airport)
        else: # User hit the cancel button
            # End program
            return

    # Method to validate user-entered origin airport
    def check_valid_origin_airport(self, origin_airport):
        if origin_airport in self.origin_airports_set: # Valid airport
            # Call method to analyze data tables
            self.analyze_unserved_routes(origin_airport)
        else: # Invalid airport
            # Display message box for error message
            messagebox.showerror(message = "Airport nonexistent, does not have scheduled commercial air service, or is "
                                           "not in the U.S.", title = TITLE)

            # End the program
            return

    # Method to analyze data tables
    def analyze_unserved_routes(self, origin_airport):
        # Clean datasets by dropping N/A values (shouldn't be there anyway but double-check)
        self.DB1B_df.dropna(inplace = True)
        self.T100_df.dropna(inplace = True)

        # Filter DB1B_df down to rows where origin airport is same as user input
        filtered_DB1B_df = self.DB1B_df[self.DB1B_df.ORIGIN == origin_airport].copy()

        # Create new column that multiplies passenger counts by 10, as DB1B is a 10% sample of tickets
        filtered_DB1B_df["PASSENGERS_TIMES_10"] = filtered_DB1B_df["PASSENGERS"] * 10

        # Create new column that calculates the passengers daily by dividing the passengers_times_10 column by 365 and
        # round to 2 decimal places
        filtered_DB1B_df["PASSENGERS_DAILY"] = (filtered_DB1B_df["PASSENGERS_TIMES_10"] / 365).round(2)

        # Sort the df by passenger counts, highest to lowest, using merge sort
        filtered_DB1B_df.sort_values(by="PASSENGERS_TIMES_10", ascending=False, inplace=True, kind="mergesort")

        # Filter T100_df down to rows where origin airport is same as user input and passengers > 0 (as T100 contains
        # cargo flights)
        filtered_T100_df = self.T100_df[(self.T100_df.ORIGIN == origin_airport) & (self.T100_df.PASSENGERS > 0)]

        # Create a new column of boolean values in filtered_DB1B_df that indicates whether a route has a nonstop
        # flight by cross-checking with T100_df, which indicates whether a nonstop flight exists
        filtered_DB1B_df["HAS_NONSTOP_FLIGHT"] = filtered_DB1B_df["DEST"].isin(filtered_T100_df["DEST"])

        # Filter to routes without nonstop flights
        filtered_DB1B_df = filtered_DB1B_df[filtered_DB1B_df["HAS_NONSTOP_FLIGHT"] == False]

        # Grab first 10 rows
        filtered_DB1B_df = filtered_DB1B_df.head(10)

        # Call create_bar_graph method
        self.create_bar_graph(filtered_DB1B_df, origin_airport)

    def create_bar_graph(self, df, origin_airport):
        try:
            # Format graph
            fig, ax = plt.subplots(figsize = (12, 8))

            # Title
            ax.text(0, 1.18, f"Most popular unserved flight routes from {origin_airport} in 2024",
                    transform = ax.transAxes, fontsize = 24, va = 'top')

            # Subtitle
            ax.text(0, 1.04, "Based on Bureau of Transportation Statistics (BTS) 2024 DB1B tables.\nIn parentheses under"
                             " each count is the average daily passenger count. A Boeing 737-800 seats around 160 "
                             "passengers.",
                    transform = ax.transAxes, fontsize = 12, color = '#a7a9ac', va = 'bottom')

            # Labels and scale
            plt.xlabel("Destination Airport", labelpad = 20, fontsize = 18)
            plt.ylabel("Passengers", labelpad = 20, fontsize=18)
            plt.xticks(fontsize = 12)
            plt.yticks(fontsize = 12)
            plt.ylim(0, df["PASSENGERS_TIMES_10"].max() * 1.1)

            # Remove top and right borders
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            # Change window title
            fig.canvas.manager.set_window_title(TITLE)

            # Create graph
            graph = plt.bar(df.DEST, df.PASSENGERS_TIMES_10, color='#0039a6')
            bar_labels = df["PASSENGERS_TIMES_10"].astype(str).str.cat("\n(" + df["PASSENGERS_DAILY"].astype(str) + ")")
            plt.bar_label(graph, df.PASSENGERS_TIMES_10.map(int).astype(str) + "\n(" +
                          df.PASSENGERS_DAILY.map(float).astype(str) + ")", label_type="center", padding=2,
                          color="w", fontsize=12)
        except ValueError:
            # Display message box for error message
            messagebox.showerror(
                message=f"No passengers traveled from {origin_airport} to any other airport without connecting. (This i"
                        f"s common with airports served exclusively by budget airlines that do not sell connections.)",
                title=TITLE)
        else:
            # Show graph
            plt.tight_layout()
            plt.show()