import yfinance as yf # Quick start
dat = yf.Ticker("MSFT")
import matplotlib.pyplot as plt


#API Reference: https://ranaroussi.github.io/yfinance/reference/index.html

#Ticket Symbol for multiple ticker symbols:

tickers = yf.Tickers('MSFT AAPL GOOG')
tickers.tickers['MSFT'].info

#Saving ticket symbols into data variable
data = yf.download(['MSFT', 'AAPL', 'GOOG'], period='1mo', interval='1d')

print(data.head())

print(data.columns)


# Plot closing prices
data['Close'].plot(figsize=(10, 5))
plt.title("Stock Closing Prices - Last 1 Month")
plt.ylabel("Price (USD)")
plt.grid(True)
plt.show()



