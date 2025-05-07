import yfinance as yf # Quick start
import Database

class MarketData:
    def __init__(self, db: Database):
        self.db = db



dat = yf.Ticker("MSFT")

#API Reference: https://ranaroussi.github.io/yfinance/reference/index.html

#Ticket Symbol for multiple ticker symbols:

tickers = yf.Tickers('MSFT AAPL GOOG')
tickers.tickers['MSFT'].info

#Saving ticket symbols into data variable
data = yf.download(['MSFT', 'AAPL', 'GOOG'], period='1mo', interval='1d')

print(data.head())

print(data.columns)

#We need a list of stocks:

tickers = [("MSFT", "Microsoft Corporation"),
           ("AAPL", "Apple Inc."),
           ("GOOGL", "Alphabet Inc."),
           ("TSLA", "Tesla Inc.")
           ]

for symbol, name in tickers:
    cursor.execute("INSERT IGNORE INTO tickers (symbol, name) VALUES (%s, %s)", (symbol, name))

conn.commit()



