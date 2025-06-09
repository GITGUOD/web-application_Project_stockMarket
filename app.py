from flask import Flask, jsonify, render_template, request
from Backend.Database import Database
from Backend.API.MarketData import MarketData

def main():
    db = Database()
    market_data = MarketData(db)
    VALID_INTERVALS = [
    ("10y", "1mo"),
    ("10y", "1wk"),
    ("5y", "1mo"),
    ("5y", "1wk"),
    ("1y", "1d"), # daily over 1 year
    ("3mo", "1d"),
    ("3mo", "1h"), 
    ("1mo", "1h"),
    ("5d", "30m"),    # 30min over 1 week etc
    ("5d", "15m")     # 15-minute data over 5 days
    ]

    market_data.load_sample_tickers()
    market_data.load_all_sample_data(VALID_INTERVALS) #Our timeframe data
    db.close()

#Hämtar html filen
app = Flask(__name__, template_folder='frontend')
db = Database()

@app.route('/')
def home():
    return render_template("StockGrapth.html")  # Visa din HTML-sida här


@app.route("/stock/<symbol>/prices")
def get_stock_prices(symbol):
    try:
        timeframe = request.args.get('timeframe', '1d')
        data = db.get_prices_for_ticker(symbol, timeframe)

        if not data:

            return jsonify({"error": "No data found for symbol"}), 404


        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


if __name__ == "__main__":
    main()
    app.run(debug=True)
