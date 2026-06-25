# Class for analyzing
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tkinter
from tkinter import simpledialog, messagebox

TITLE = "Popular Unserved Flight Routes"

class UnservedFlightRoutesAnalyzer:
    def __init__(self, db1b_path, t100_path):
        # Read both DB1B and T-100 CSVs first
        self.DB1B_df = pd.read_csv(db1b_path)
        self.T100_df = pd.read_csv(t100_path)

        # Get a set of valid origin airport codes
        self.origin_airports_set = set(self.DB1B_df.ORIGIN)

        # Create new Tkinter window then withdraw it
        self.window = tkinter.Tk()
        self.window.withdraw()

        # Set attributes for original airport and final dataframe
        self.origin_airport = None
        self.final_df = None

    # Method to get airport code from user
    def get_origin_airport(self):
        # Ask user for airport code
        origin_airport = simpledialog.askstring(title = TITLE, prompt = "Enter a three-character IATA airport code:")

        if origin_airport:
            # Convert user input to uppercase
            origin_airport = origin_airport.upper()

            # Set origin_airport attribute to result
            self.origin_airport = origin_airport

    # Method to validate user-entered origin airport
    def validate_origin_airport(self):
        if self.origin_airport in self.origin_airports_set: # Valid airport
            return True
        else: # Invalid airport
            # Display message box for error message
            messagebox.showerror(message = "Airport is nonexistent, does not have scheduled commercial air service, or "
                                           "is not in the U.S.", title = TITLE)
            return False

    # Method to analyze data tables
    def analyze_data_tables(self):
        # Clean datasets by dropping N/A values (shouldn't be there anyway but double-check)
        self.DB1B_df.dropna(inplace = True)
        self.T100_df.dropna(inplace = True)

        # Filter DB1B_df down to rows where origin airport is same as user input
        filtered_DB1B_df = self.DB1B_df[self.DB1B_df.ORIGIN == self.origin_airport].copy()

        # Create new column that multiplies passenger counts by 10, as DB1B is a 10% sample of tickets
        filtered_DB1B_df["PASSENGERS_TIMES_10"] = filtered_DB1B_df["PASSENGERS"] * 10

        # Create new column that calculates the passengers daily by dividing the passengers_times_10 column by 365 and
        # round to 2 decimal places
        filtered_DB1B_df["PASSENGERS_DAILY"] = (filtered_DB1B_df["PASSENGERS_TIMES_10"] / 365).round(2)

        # Sort the df by passenger counts, highest to lowest, using merge sort
        filtered_DB1B_df.sort_values(by="PASSENGERS_TIMES_10", ascending=False, inplace=True, kind="mergesort")

        # Filter T100_df down to rows where origin airport is same as user input and passengers > 0 (as T100 contains
        # cargo flights)
        filtered_T100_df = self.T100_df[(self.T100_df.ORIGIN == self.origin_airport) & (self.T100_df.PASSENGERS > 0)]

        # Create a new column of boolean values in filtered_DB1B_df that indicates whether a route has a nonstop
        # flight by cross-checking with T100_df, which indicates whether a nonstop flight exists
        filtered_DB1B_df["HAS_NONSTOP_FLIGHT"] = filtered_DB1B_df["DEST"].isin(filtered_T100_df["DEST"])

        # Filter to routes without nonstop flights
        filtered_DB1B_df = filtered_DB1B_df[filtered_DB1B_df["HAS_NONSTOP_FLIGHT"] == False]

        # Grab first 10 rows
        filtered_DB1B_df = filtered_DB1B_df.head(10)

        # Deal with edge case where filtered df might be empty
        if not filtered_DB1B_df.empty:
            self.final_df = filtered_DB1B_df
            return True
        else:
            messagebox.showerror(message=f"Everyone who flew out of {self.origin_airport} took a nonstop flight. (This "
                                         f"is common with airports served exclusively by a budget airline that does "
                                         f"not sell connecting itineraries.)", title=TITLE)
            return False

    # Method to create and show the graph
    def create_bar_graph(self):
        # Format graph
        fig, ax = plt.subplots(figsize = (12, 8))

        # Title
        ax.text(0, 1.22, f"Most popular unserved flight routes from {self.origin_airport} in 2024",
                transform = ax.transAxes, fontsize = 24, va = 'top')

        # Subtitle
        ax.text(0, 1.04, "Based on Bureau of Transportation Statistics (BTS) 2024 DB1B tables.\nIn parentheses under"
                         " each count is the average daily passenger count.\nFor context, a Boeing 737-800 seats "
                         "around 160 passengers, and an Embraer E175LR seats around 76 passengers.",
                transform = ax.transAxes, fontsize = 12, color = '#a7a9ac', va = 'bottom')

        # Labels and scale
        plt.xlabel("Destination Airport", labelpad = 20, fontsize = 18)
        plt.ylabel("Passengers", labelpad = 20, fontsize=18)
        plt.xticks(fontsize = 12)
        plt.yticks(fontsize = 12)
        plt.ylim(0, self.final_df["PASSENGERS_TIMES_10"].max() * 1.1)

        # Remove top and right borders
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Change window title
        fig.canvas.manager.set_window_title(f"Most popular unserved flight routes from {self.origin_airport} in 2024")

        # Create graph
        graph = plt.bar(self.final_df.DEST, self.final_df.PASSENGERS_TIMES_10, color='#0039a6')
        bar_labels = self.final_df["PASSENGERS_TIMES_10"].astype(str).str.cat("\n(" +
                     self.final_df["PASSENGERS_DAILY"].astype(str) + ")")
        plt.bar_label(graph, self.final_df.PASSENGERS_TIMES_10.map(int).astype(str) + "\n(" +
                      self.final_df.PASSENGERS_DAILY.map(float).astype(str) + ")", label_type="center", padding=2,
                      color="w", fontsize=12)

        # Show graph
        plt.tight_layout()
        plt.show()

    def run(self):
        # Call method to get airport code from user
        self.get_origin_airport()

        if not self.origin_airport: # User hit the cancel button
            self.window.destroy()
            return

        # Call method to validate user-entered origin airport
        if not self.validate_origin_airport():
            self.window.destroy()
            return

        # Call method to analyze data tables
        if not self.analyze_data_tables():
            self.window.destroy()
            return

        # Call the method to create and show the graph
        self.create_bar_graph()

        # Destroy the window
        self.window.destroy()