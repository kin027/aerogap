from unserved_routes_analyzer import UnservedRoutesAnalyzer

# Set global constants for paths of files
DB1B_PATH = "final_datasets/DB1B_2024_consolidated.csv"
T100_PATH = "final_datasets/T100_2024.csv"

def main():
    # Ask user for airport code
    origin_airport = input("Enter a three-character IATA airport code: ")

    # Convert user input to uppercase
    origin_airport_upper = origin_airport.upper()

    # Create RoutesAnalyzer object
    analyzer = UnservedRoutesAnalyzer(DB1B_PATH, T100_PATH)

    # Call analyzer analyze_routes method
    analyzer.analyze_unserved_routes(origin_airport_upper)

main()