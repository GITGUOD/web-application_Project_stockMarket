import yfinance as yf # YFinance API, importing data
#from .. import Database
from Backend.Database import Database


#API Reference: https://ranaroussi.github.io/yfinance/reference/index.html


class MarketData:
    #Utilizing our initial database
    def __init__(self, db: Database):
        self.db = db

    def load_sample_tickers(self):
        # Fetching company data using yfinance API
        
        tickers = self.get_samples()
        
        for symbol, _ in tickers: #Packing up each String as a tuple, without ', _' both MSFT and Microsoft Corporation would be treated one way which we don't want to
            try:
                #Using all ticker objects in our vector and adding them to the database by fetching the method from our db class
                ticker = yf.Ticker(symbol)
                name = ticker.info.get("longName") or ticker.info.get("shortName") or "Unknown Company"
                self.db.insert_ticker(symbol, name)
            except Exception as e:
                print(f"Failed to insert {symbol}: {e}")
    
    #Adding tickers
    def get_samples():
        tickers = [("MSFT", "Microsoft Corporation"),
           ("AAPL", "Apple Inc."),
           ("GOOGL", "Alphabet Inc."),
           ("TSLA", "Tesla Inc."),
           ("NVDA", "Nvidia Corporation."),
           ("AMZN", "Amazon.com Inc.")
           ]
        return tickers
        
    
    def load_stock_data(self, symbol):
        #Fetching historical price stock data from Yahoo Finance
        HistoricalPeriod = "5y" #You can adjust this time period depending on your needs
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=HistoricalPeriod)

            for date, row in data.iterrows():

                open_price = row['Open']
                high_price = row['High']
                low_price = row['Low']
                close_price = row['Close']
                volume = row['Volume']
                date_str = date.strftime('%Y-%m-%d')  # Convert to string (date format)

                # Insert into price table (assuming you have already inserted stock and ticket data)
                self.db.insert_price(symbol, "1d", date_str, open_price, high_price, low_price, close_price, volume)  # '1d' is the timeframe example
        except Exception as e:
            print(f"Failed to load stock data for {symbol}: {e}")

    def load_all_sample_data(self):
        tickers = self.get_samples()  # Eller MarketData.get_samples() om det är en statisk metod
        for symbol, _ in tickers:
            self.load_stock_data(symbol)

    def close(self):
        self.db.close()
