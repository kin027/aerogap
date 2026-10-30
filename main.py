from unserved_market_analyzer import UnservedMarketAnalyzer

def main():
    # Create analyzer object
    analyzer = UnservedMarketAnalyzer(db1c_path="final_db1c.csv", t100_path="final_t100.csv")

    # Call analyzer run method
    analyzer.run()


if __name__ == "__main__":
    main()
