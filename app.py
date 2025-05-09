from flask import Flask, jsonify, send_from_directory
from Backend.Database import Database
from Backend.API.MarketData import MarketData

def main():
    db = Database()
    market_data = MarketData(db)
    market_data.load_sample_tickers()
    # List of symbols to load historical stock data for
    symbols = ["MSFT", "AAPL", "GOOGL", "TSLA", "NVDA", "AMZN"]
    for symbol in symbols:
        market_data.load_stock_data(symbol)
    db.close()

app = Flask(__name__)
db = Database()

@app.route('/')
def home():
    return "Welcome to the Stock Market App!"

@app.route("/stock/<symbol>/prices")
def get_stock_prices(symbol):
    try:
        data = db.get_prices_for_ticker(symbol)
        if not data:
            return jsonify({"error": "No data found for symbol"}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    main()
    app.run(debug=True)
