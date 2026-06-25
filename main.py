from unserved_flight_routes_analyzer import UnservedFlightRoutesAnalyzer

# Set global constants for paths of files
DB1B_PATH = "final_datasets/DB1B_2024_consolidated.csv"
T100_PATH = "final_datasets/T100_2024.csv"

def main():
    # Create UnservedFlightRoutesAnalyzer object
    analyzer = UnservedFlightRoutesAnalyzer(DB1B_PATH, T100_PATH)

    # Call analyzer run method
    analyzer.run()

main()