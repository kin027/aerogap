from unserved_routes_analyzer import UnservedRoutesAnalyzer

# Set global constants for paths of files
DB1B_PATH = "final_datasets/DB1B_2024_consolidated.csv"
T100_PATH = "final_datasets/T100_2024.csv"

def main():
    # Create RoutesAnalyzer object
    analyzer = UnservedRoutesAnalyzer(DB1B_PATH, T100_PATH)

    # Call analyzer analyze_routes method
    analyzer.get_origin_airport()

main()