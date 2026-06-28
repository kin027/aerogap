from unserved_market_identifier import UnservedMarketIdentifier

# Set global constants for paths of files
DB1B_PATH = "final_tables/DB1B_2024_consolidated.csv"
T100_PATH = "final_tables/T_T100_SEGMENT_ALL_CARRIER_2024.csv"


def main():
    # Create data object
    analyzer = UnservedMarketIdentifier(DB1B_PATH, T100_PATH)

    # Call analyzer run method
    analyzer.run()


main()
