import yfinance as yf # YFinance API, importing data
import Database
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




dat = yf.Ticker("MSFT")

#API Reference: https://ranaroussi.github.io/yfinance/reference/index.html

#Ticket Symbol for multiple ticker symbols:

tickers = yf.Tickers('MSFT AAPL GOOG')
tickers.tickers['MSFT'].info

#Saving ticket symbols into data variable
data = yf.download(['MSFT', 'AAPL', 'GOOG'], period='1mo', interval='1d')

print(data.head())

print(data.columns)

#A list of stocks:

tickers = [("MSFT", "Microsoft Corporation"),
           ("AAPL", "Apple Inc."),
           ("GOOGL", "Alphabet Inc."),
           ("TSLA", "Tesla Inc."),
           ("NVDA", "Nvidia Corporation."),
           ("AMZN", "Amazon.com Inc.")
           ]

for symbol, name in tickers:
    cursor.execute("INSERT IGNORE INTO tickers (symbol, name) VALUES (%s, %s)", (symbol, name))

conn.commit()



