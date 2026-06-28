from unserved_market_analyzer import UnservedMarketAnalyzer

# Set global constants for paths of files
DB1B_PATH = "final_tables/DB1B_2024_consolidated.csv"
T100_PATH = "final_tables/T_T100_SEGMENT_ALL_CARRIER_2024.csv"


def main():
    # Create data object
    analyzer = UnservedMarketAnalyzer(DB1B_PATH, T100_PATH)

    # Call analyzer run method
    analyzer.run()


main()
