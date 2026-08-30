from unserved_market_analyzer import UnservedMarketAnalyzer

# Set global constants for paths of files
DB1C_PATH = "final_db1c.csv"
T100_PATH = "final_t100.csv"


def main():
    # Create data object
    analyzer = UnservedMarketAnalyzer(DB1C_PATH, T100_PATH)

    # Call analyzer run method
    analyzer.run()


main()
