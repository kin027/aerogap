import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import tkinter
from tkinter import simpledialog, messagebox

TITLE = "AeroGap"


class UnservedMarketAnalyzer:
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
        origin_airport = simpledialog.askstring(
            title=TITLE,
            prompt="Enter a three-character IATA airport code\n"
            "for an airport in the U.S.:",
        )

        if origin_airport:
            # Convert user input to uppercase
            origin_airport = origin_airport.upper()

            # Read CSVs
            self.DB1B_df = pd.read_csv(self.DB1B_path)
            self.T100_df = pd.read_csv(self.T100_path)

            # Get a set of valid origin airport codes
            valid_origin_airports = set(self.DB1B_df["ORIGIN"].unique())

            # Validate user-entered origin airport
            if origin_airport in valid_origin_airports:  # Valid airport
                # Set origin_airport attribute to result
                self.origin_airport = origin_airport

                return True
            else:  # Invalid airport
                # Display message box for error message
                messagebox.showerror(
                    message="Airport is nonexistent, does not have scheduled commercial passenger "
                    "air service, or is not in the U.S.",
                    title=TITLE,
                )
                return False
        else:
            return False

    # Method to analyze data tables
    def analyze_data_tables(self):
        # First, clean T-100 table

        # Drop NA values
        self.T100_df = self.T100_df.dropna()

        # Filter T-100 so that DEPARTURES_SCHEDULED > 0 (exclude diversions, etc.)
        self.T100_df = self.T100_df[self.T100_df["DEPARTURES_SCHEDULED"] > 0]

        # Filter T-100 so that PASSENGERS > 0 (exclude cargo)
        self.T100_df = self.T100_df[self.T100_df["PASSENGERS"] > 0]

        # Filter T-100 so that CLASS is "F" (Scheduled Passenger/ Cargo Service F) (exclude non-scheduled flights)
        self.T100_df = self.T100_df[self.T100_df["CLASS"] == "F"]

        # Keep only the ORIGIN and DEST columns in T-100
        self.T100_df = self.T100_df[["ORIGIN", "DEST"]].copy()

        # Filter T100_df down to rows where ORIGIN is same as user input
        self.T100_df = self.T100_df[self.T100_df["ORIGIN"] == self.origin_airport]

        # Remove duplicate rows (same routes)
        self.T100_df = self.T100_df.drop_duplicates()

        # Second, clean DB1B table

        # Drop NA values
        self.DB1B_df = self.DB1B_df.dropna()

        # Filter DB1B_df down to rows where origin airport is same as user input
        self.DB1B_df = self.DB1B_df[
            self.DB1B_df["ORIGIN"] == self.origin_airport
        ].copy()

        # Create new column that multiplies passenger counts by 10, as DB1B is a 10% sample of tickets
        self.DB1B_df["PASSENGERS_TIMES_10"] = self.DB1B_df["PASSENGERS"] * 10

        # Create new column that calculates the passengers daily by dividing the PASSENGERS_TIMES_100 column by 365 and
        # round to 2 decimal places
        self.DB1B_df["PASSENGERS_DAILY"] = (
            self.DB1B_df["PASSENGERS_TIMES_10"] / 365
        ).round(2)

        # Sort the df by passenger counts, highest to lowest, using merge sort
        self.DB1B_df = self.DB1B_df.sort_values(
            by="PASSENGERS_TIMES_10", ascending=False, kind="mergesort"
        )

        # Create a new column of boolean values in self.DB1B_df that indicates whether a route has a nonstop
        # flight by cross-checking with T100_df, which indicates whether a nonstop flight exists
        self.DB1B_df["HAS_NONSTOP_FLIGHT"] = self.DB1B_df["DEST"].isin(
            self.T100_df["DEST"]
        )

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
            messagebox.showerror(
                message=f"No passengers from {self.origin_airport} connected to an onward flight.\n\n(This "
                f"is common with airports served exclusively by a budget airline that does "
                f"not sell connecting itineraries.)",
                title=TITLE,
            )
            return False

    # Method to create and show the graph
    def create_graph(self):
        # Constants for graph
        GRAPH_TITLE = f"Top Domestic Unserved Markets from {self.origin_airport} by Passenger Volume (2024)"
        SMALL_FONT_SIZE = 12
        MEDIUM_FONT_SIZE = 16
        LARGE_FONT_SIZE = 20
        FONT = "Helvetica"

        # Graph size
        plt.figure(num=GRAPH_TITLE, figsize=(12, 8))

        # Create graph
        graph = plt.bar(
            x=self.final_df.DEST,
            height=self.final_df.PASSENGERS_TIMES_10,
            color="#0039a6",
        )

        # Format graph

        # Title

        plt.title(
            label=GRAPH_TITLE,
            pad=20,
            loc="left",
            fontfamily=FONT,
            fontsize=LARGE_FONT_SIZE,
            fontweight="bold",
            color="#000",
            wrap=True,
        )

        # In-bar labels
        plt.bar_label(
            container=graph,
            labels=self.final_df.PASSENGERS_TIMES_10.map(int).astype(str)
            + "\n("
            + self.final_df.PASSENGERS_DAILY.map(float).astype(str)
            + ")",
            label_type="center",
            padding=2,
            color="#fff",
            fontsize=SMALL_FONT_SIZE,
            fontfamily=FONT,
        )

        # x-axis
        plt.xlabel(
            "Destination Airport",
            labelpad=20,
            loc="center",
            fontsize=MEDIUM_FONT_SIZE,
            fontfamily=FONT,
            wrap=True,
        )
        plt.xticks(fontsize=SMALL_FONT_SIZE, fontfamily=FONT)
        plt.tick_params(axis="x", which="both", length=0, pad=8)

        # y-axis
        plt.ylabel(
            "Estimated Annual Passengers (Scaled 10% Sample)",
            labelpad=20,
            loc="center",
            fontsize=MEDIUM_FONT_SIZE,
            fontfamily=FONT,
            wrap=True,
        )
        plt.yticks(fontsize=SMALL_FONT_SIZE, fontfamily=FONT)
        plt.tick_params(axis="y", which="both", pad=4)
        plt.ylim(0, self.final_df["PASSENGERS_TIMES_10"].max() * 1.05)

        # Bottom text
        plt.figtext(
            x=0.01,
            y=0.01,
            s="Based on Bureau of Transportation Statistics (BTS) 2024 DB1B tables.\nValues in parentheses represent average daily passengers. An Embraer E175LR seats around 76 passengers.",
            ha="left",
            fontfamily=FONT,
            fontsize=SMALL_FONT_SIZE,
            fontweight="normal",
            color="#A7A9AC",
            wrap=True,
        )

        # Borders
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)

        # Show graph
        plt.tight_layout()
        plt.gcf().subplots_adjust(bottom=0.15)
        plt.show()

    def run(self):
        # Call get_origin_airport method
        if self.get_origin_airport():

            # Call analyze_data_tables method
            if self.analyze_data_tables():

                # Call create_graph method
                self.create_graph()

        # Destroy the window
        self.window.destroy()
