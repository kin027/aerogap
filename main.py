from unserved_market_analyzer import UnservedMarketAnalyzer

# Set global constants for paths of files
DB1C_PATH = "final_db1c.csv"
T100_PATH = "T_T100D_SEGMENT_ALL_CARRIER_2025.csv"
AIRPORTS_PATH = "airports.csv"


def main():
    # Create data object
    analyzer = UnservedMarketAnalyzer(DB1C_PATH, T100_PATH, AIRPORTS_PATH)

    # Call analyzer run method
    analyzer.run()


main()
