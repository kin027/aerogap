import pandas as pd
from tkinter import *
from tkinter import simpledialog, messagebox
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import webview
import threading

TITLE = "AeroGap"


class UnservedMarketAnalyzer:
    def __init__(self, db1c_path, t100_path):
        # Original data attributes
        self.original_db1c_df = pd.read_csv(db1c_path)
        self.original_t100_df = pd.read_csv(t100_path)

        # Attributes to be filled out in later methods
        self.origin_market_id = None
        self.origin_market_name = None
        self.copy_t100_df = None
        self.copy_db1c_df = None

        # Interactive graph
        self.app = Dash(__name__)
        self.register_callbacks()
        self.timeline = []

    # Method to get and validate airport code from user
    def get_origin_airport(self):
        # Create base tkinter window
        root = Tk()

        # Immediately hide window
        root.withdraw()

        # Ask user for airport code
        origin_airport = simpledialog.askstring(
            title=TITLE,
            prompt="Enter a three-character IATA airport code\n"
                   "for an airport in the U.S.:",
        )

        if origin_airport:
            # Convert user input to uppercase
            origin_airport = origin_airport.upper()

            # Get list of valid airports
            mask = [
                origin_airport in str(airports).split(", ")
                for airports in self.original_db1c_df["ORIGIN_MARKET_AIRPORTS"]
            ]

            valid_rows = self.original_db1c_df[mask]

            is_valid_airport = not valid_rows.empty

            # Validate user-entered origin airport
            if is_valid_airport:  # Valid airport
                # Set relevant attributes
                self.origin_market_id = valid_rows["ORIGIN_MARKET_ID"].iloc[0]
                self.origin_market_name = valid_rows["ORIGIN_MARKET_NAME"].iloc[0]

                result = "VALID"
            else:  # Invalid airport
                # Display message box for error message
                messagebox.showerror(
                    message="Airport is nonexistent, does not have scheduled "
                            "commercial passenger air service, or is not in the U.S.",
                    title=TITLE,
                )
                result = "INVALID"
        else:  # No response
            result = "EXIT"

        # Destroy window immediately before returning
        root.destroy()

        return result

    # Method to analyze routes
    def analyze_routes(self):
        # Create copies
        self.copy_db1c_df = self.original_db1c_df.copy()
        self.copy_t100_df = self.original_t100_df.copy()

        # Set self.timeline
        temp_df = self.original_db1c_df.drop_duplicates(subset=["YEAR", "MONTH"])
        temp_df = temp_df.sort_values(by=["YEAR", "MONTH"], ascending=True)
        self.timeline = [
            (row.YEAR, row.MONTH, row.MONTH_NAME) for row in temp_df.itertuples()
        ]

        # Filter both dfs to rows where ORIGIN is same as user input
        self.copy_t100_df = self.copy_t100_df[
            self.copy_t100_df["ORIGIN_MARKET_ID"] == self.origin_market_id
            ]
        self.copy_db1c_df = self.copy_db1c_df[
            self.copy_db1c_df["ORIGIN_MARKET_ID"] == self.origin_market_id
            ]

        # Keep rows in T-100 where DEST_MARKET_ID is not origin_market_id
        self.copy_t100_df = self.copy_t100_df[
            self.copy_t100_df["DEST_MARKET_ID"] != self.origin_market_id]

    # Method to construct and return layout tree
    def build_layout(self):
        return html.Div(
            # Overall style
            style={
                "display": "flex",
                "flexDirection": "column",
                "height": "98vh",
                "padding": "10px",
                "fontFamily": "Helvetica",
            },
            children=[
                # Div for graph
                html.Div(
                    dcc.Graph(
                        id="graph",
                        style={
                            "height": "100%",
                            "width": "100%",
                        },
                    ),
                    style={"flex": "3"},
                ),
                # Div for slider
                html.Div(
                    dcc.Slider(
                        min=0,
                        max=len(self.timeline) - 1,
                        step=1,
                        value=0,
                        marks={
                            i: f"{time[2]} {time[0]}"
                            for i, time in enumerate(self.timeline)
                        },
                        id="slider",
                        tooltip={"placement": "bottom", "always_visible": False},
                        updatemode="drag",
                        allow_direct_input=False,  # Hide input box
                        included=False,
                    ),
                    style={
                        "flex": "1",
                        "paddingLeft": "50px",
                        "paddingRight": "50px",
                        "marginTop": "50px",
                    },
                ),
                # Div for bottom data source note
                html.Div(
                    children=[
                        "Source: Bureau of Transportation Statistics (BTS).",
                        html.Br(),
                        "Below each monthly passenger count in parentheses is the "
                        "average daily passenger count. An Embraer E175LR typically "
                        "seats 76 passengers.",
                    ],
                    style={
                        "fontSize": "18px",
                        "color": "#A7A9AC",
                        "paddingBottom": "10px",
                        "paddingLeft": "10px",
                    },
                ),
            ],
        )

    # Method to update map whenever slider is moved
    def register_callbacks(self):
        @self.app.callback(
            Output("graph", "figure"),
            Input("slider", "value"),
        )
        def update(slider_val):
            return self.update_graph(slider_val)

    def update_graph(self, slider_position):
        # Constants for graph
        TYPEFACE = "Helvetica"
        HOVER_FONT_SIZE = 12
        BAR_FONT_SIZE = 18
        AXES_LABELS_FONT_SIZE = 12
        AXES_TITLE_FONT_SIZE = 24
        TITLE_FONT_SIZE = 36
        LINE_WIDTH = 1
        TITLE_COLOR = "#000000"
        BAR_COLOR = "#00933C"

        # Get year and month from timeline position
        target_year, target_month, target_month_name = self.timeline[slider_position]

        # Set graph title
        GRAPH_TITLE = (
            f"Top Domestic Unserved Airline O&D Markets from "
            f"{self.origin_market_name} in "
            f"{target_month_name} {target_year}")

        # Create temp_db1c_df, which is source of info for all tickets and is
        # filtered by month and year
        temp_db1c_df = self.copy_db1c_df[
            (self.copy_db1c_df["YEAR"] == target_year)
            & (self.copy_db1c_df["MONTH"] == target_month)
            ]

        # Create temp_t100_df, which is source of info for all routes and is filtered
        # by month and year
        temp_t100_df = self.copy_t100_df[
            (self.copy_t100_df["YEAR"] == target_year)
            & (self.copy_t100_df["MONTH"] == target_month)
            ]

        # Create new column of boolean values that indicates whether a route has a
        # nonstop flight by
        # cross-checking with t100_df, which indicates whether a nonstop flight exists
        temp_db1c_df["HAS_NONSTOP_FLIGHT"] = temp_db1c_df["DEST_MARKET_ID"].isin(
            temp_t100_df["DEST_MARKET_ID"]
        )

        # Filter to top 10 routes without nonstop flights
        temp_db1c_df = temp_db1c_df[temp_db1c_df["HAS_NONSTOP_FLIGHT"] == False].head(
            10
        )

        # If temp_db1c_df has data:
        if not temp_db1c_df.empty:
            # Create graph
            display_graph = px.bar(
                temp_db1c_df,
                x="DEST_MARKET_NAME",
                y="SCALED_PASSENGERS",
                labels={
                    "DEST_MARKET_NAME": "Destination Market",
                    "SCALED_PASSENGERS": "Passengers (Scaled 40% Sample)",
                },
                title=GRAPH_TITLE,
                hover_data=["DEST_MARKET_AIRPORTS"],
                color_discrete_sequence=[BAR_COLOR],
                text="BAR_TEXT",
            )

            # Change hover label text formatting
            display_graph.update_traces(
                hovertemplate="%{customdata[0]}<extra></extra>",
                textposition="inside",
                textfont=dict(
                    family=TYPEFACE,
                    size=BAR_FONT_SIZE,
                    color="#FFFFFF",  # Ensures readability inside colored bars
                ),
            )

            # Change general graph layout
            display_graph.update_layout(
                margin_l=200,
                plot_bgcolor="white",
                font=dict(family=TYPEFACE, color=TITLE_COLOR),
                title=dict(font=dict(size=TITLE_FONT_SIZE)),
                xaxis=dict(
                    ticks="",
                    title=dict(
                        font=dict(size=AXES_TITLE_FONT_SIZE),
                        standoff=AXES_TITLE_FONT_SIZE * 2,
                    ),
                    tickfont=dict(size=AXES_LABELS_FONT_SIZE),
                    showline=True,
                    linecolor=TITLE_COLOR,
                    linewidth=LINE_WIDTH,
                ),
                yaxis=dict(
                    title=dict(
                        font=dict(size=AXES_TITLE_FONT_SIZE),
                        standoff=AXES_TITLE_FONT_SIZE * 2,
                    ),
                    tickfont=dict(size=AXES_LABELS_FONT_SIZE),
                    ticks="outside",
                    tickcolor=TITLE_COLOR,
                    tickwidth=LINE_WIDTH,
                    showline=True,
                    linecolor=TITLE_COLOR,
                    linewidth=LINE_WIDTH,
                ),
                hovermode="closest",
                hoverdistance=30,
                hoverlabel=dict(
                    font=dict(
                        size=HOVER_FONT_SIZE,
                    )
                ),
                transition_duration=200,
                height=None,
            )

        else:  # No data, display message saying so instead
            display_graph = px.scatter(title=GRAPH_TITLE)

            display_graph.update_layout(
                font=dict(family=TYPEFACE, color=TITLE_COLOR),
                title=dict(font=dict(size=TITLE_FONT_SIZE)),
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                plot_bgcolor="#FFFFFF",
                transition_duration=200,
                annotations=[
                    dict(
                        text=f"No passengers from {self.origin_market_name} connected "
                             f"to an onward flight during {target_month_name} "
                             f"{target_year}.<br><br>(This is common with airports "
                             f"served exclusively by a<br>budget airline that does "
                             f"not sell connecting itineraries.)",
                        xref="paper",
                        yref="paper",
                        x=0.5,
                        y=0.5,
                        showarrow=False,
                        font=dict(
                            family=TYPEFACE,
                            size=TITLE_FONT_SIZE,
                            color=TITLE_COLOR,
                        ),
                        align="center",
                        xanchor="center",
                        yanchor="middle",
                    )
                ],
            )

        return display_graph

    # Method to show the graph
    def show_graph(self):
        # Open Dash server
        server_thread = threading.Thread(
            target=self.app.run,
            kwargs={"debug": False, "port": 8050, "use_reloader": False},
            daemon=True,
        )

        server_thread.start()

        # Show window for graph
        webview.create_window(title=TITLE, url="http://127.0.0.1:8050/", maximized=True)
        webview.start()

    # Method to run all previous methods
    def run(self):
        result = None

        # While the result of the function has something
        while result != "EXIT":
            # Get origin airport
            result = self.get_origin_airport()

            if result == "VALID":
                # Analyze routes
                self.analyze_routes()

                # Build map layout
                self.app.layout = self.build_layout()

                # Show map
                self.show_graph()
