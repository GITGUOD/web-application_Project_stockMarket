from Backend.Database import Database
from Backend.API.MarketData import MarketData

def main():
    db = Database()
    market_data = MarketData(db)
    market_data.load_sample_tickers()
    db.close()

if __name__ == "__main__":
    main()
