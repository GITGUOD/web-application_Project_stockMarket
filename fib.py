import ccxt #for trading with crypto
import os # for environment variables

import yfinance as yf
import matplotlib.pyplot as plt

# Step 1: Define the stock symbol you want to fetch data for
stock_symbol = 'AAPL'  # Example: Apple Inc.

# Step 2: Fetch historical market data
# You can specify the period (e.g., '1y' for one year, '6mo' for six months)
data = yf.download(stock_symbol, period='1y', interval='1d')

# Step 3: Print the fetched data
print(data)

# Step 4: Plot the closing price
plt.figure(figsize=(12, 6))
plt.plot(data['Close'], label='Close Price', color='blue')
plt.title(f'{stock_symbol} Closing Prices Over the Last Year')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid()
plt.show()
