import yfinance as yf # YFinance API, importing data
from .. import Database

#API Reference: https://ranaroussi.github.io/yfinance/reference/index.html


class MarketData:
    #Utilizing our initial database
    def __init__(self, db: Database):
        self.db = db

    def load_sample_tickers(self):
        # Adding tickers and fetching company data using yfinance API
        tickers = [("MSFT", "Microsoft Corporation"),
           ("AAPL", "Apple Inc."),
           ("GOOGL", "Alphabet Inc."),
           ("TSLA", "Tesla Inc."),
           ("NVDA", "Nvidia Corporation."),
           ("AMZN", "Amazon.com Inc.")
           ]
        
        for symbol in tickers:
            try:
                #Using all ticker objects in our vector and adding them to the database by fetching the method from our db class
                ticker = yf.Ticker(symbol)
                name = ticker.info.get("longName") or ticker.info.get("shortName") or "Unknown Company"
                self.db.insert_ticker(symbol, name)
            except Exception as e:
                print(f"Failed to insert {symbol}: {e}")
