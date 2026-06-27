import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tkinter
from tkinter import simpledialog, messagebox

TITLE = "Popular Unserved Flight Routes"

class UnservedFlightRoutesAnalyzer:
    def __init__(self, db1b_path, t100_path):
        # Set up DB1B and T-100 attributes
        self.DB1B_df = pd.DataFrame()
        self.T100_df = pd.DataFrame()
        self.DB1B_path = db1b_path
        self.T100_path = t100_path

        # Create new Tkinter window then withdraw it
        self.window = tkinter.Tk()
        self.window.withdraw()

        # Set attributes for original airport and final dataframe
        self.origin_airport = None
        self.final_df = None

    # Method to get and validate airport code from user
    def get_origin_airport(self):
        # Ask user for airport code
        origin_airport = simpledialog.askstring(title = TITLE, prompt = "Enter a three-character IATA airport code\n"
                                                                        "for an airport in the U.S.:")

        if origin_airport:
            # Convert user input to uppercase
            origin_airport = origin_airport.upper()

            # Read CSVs
            self.DB1B_df = pd.read_csv(self.DB1B_path)
            self.T100_df = pd.read_csv(self.T100_path)

            # Get a set of valid origin airport codes
            valid_origin_airports = set(self.DB1B_df["ORIGIN"].unique())

            # Validate user-entered origin airport
            if origin_airport in valid_origin_airports: # Valid airport
                # Set origin_airport attribute to result
                self.origin_airport = origin_airport

                return True
            else: # Invalid airport
                # Display message box for error message
                messagebox.showerror(message = "Airport is nonexistent, does not have scheduled commercial passenger "
                                               "air service, or is not in the U.S.", title = TITLE)
                return False
        else:
            return False

    # Method to analyze data tables
    def analyze_data_tables(self):
        # First, clean T-100 table

        # Drop NA values
        self.T100_df.dropna(inplace=True)

        # Filter T-100 so that DEPARTURES_SCHEDULED > 0 (exclude diversions, etc.)
        self.T100_df = self.T100_df[self.T100_df["DEPARTURES_SCHEDULED"] > 0]

        # Filter T-100 so that CLASS is "F" (Scheduled Passenger/ Cargo Service F) (exclude non-scheduled flights)
        self.T100_df = self.T100_df[self.T100_df["CLASS"] == "F"]

        # Filter T-100 so that PASSENGERS > 0 (exclude cargo)
        self.T100_df = self.T100_df[self.T100_df["PASSENGERS"] > 0]

        # Keep only the ORIGIN and DEST columns in T-100
        self.T100_df = self.T100_df[["ORIGIN", "DEST"]].copy()

        # Filter T100_df down to rows where ORIGIN is same as user input
        self.T100_df = self.T100_df[self.T100_df["ORIGIN"] == self.origin_airport]

        # Remove duplicate rows (same routes)
        self.T100_df.drop_duplicates(inplace=True)

        # Second, clean DB1B table

        # Drop NA values
        self.DB1B_df.dropna(inplace = True)

        # Filter DB1B_df down to rows where origin airport is same as user input
        self.DB1B_df = self.DB1B_df[self.DB1B_df["ORIGIN"] == self.origin_airport].copy()

        # Create new column that multiplies passenger counts by 10, as DB1B is a 10% sample of tickets
        self.DB1B_df["PASSENGERS_TIMES_10"] = self.DB1B_df["PASSENGERS"] * 10

        # Create new column that calculates the passengers daily by dividing the PASSENGERS_TIMES_100 column by 365 and
        # round to 2 decimal places
        self.DB1B_df["PASSENGERS_DAILY"] = (self.DB1B_df["PASSENGERS_TIMES_10"] / 365).round(2)

        # Sort the df by passenger counts, highest to lowest, using merge sort
        self.DB1B_df.sort_values(by="PASSENGERS_TIMES_10", ascending=False, inplace=True, kind="mergesort")

        # Create a new column of boolean values in self.DB1B_df that indicates whether a route has a nonstop
        # flight by cross-checking with T100_df, which indicates whether a nonstop flight exists
        self.DB1B_df["HAS_NONSTOP_FLIGHT"] = self.DB1B_df["DEST"].isin(self.T100_df["DEST"])

        # Now do the magic

        # Filter to routes without nonstop flights
        self.DB1B_df = self.DB1B_df[self.DB1B_df["HAS_NONSTOP_FLIGHT"] == False]

        # Grab first 10 rows
        self.DB1B_df = self.DB1B_df.head(10)

        # Deal with edge case where filtered df might be empty
        if not self.DB1B_df.empty:
            self.final_df = self.DB1B_df
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
        if not self.get_origin_airport():
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