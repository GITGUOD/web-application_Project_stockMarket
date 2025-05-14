from flask import Flask, jsonify, render_template
from Backend.Database import Database
from Backend.API.MarketData import MarketData

def main():
    db = Database()
    market_data = MarketData(db)
    market_data.load_sample_tickers()
    market_data.load_all_sample_data()
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
        data = db.get_prices_for_ticker(symbol)

        if not data:
            return jsonify({"error": "No data found for symbol"}), 404


        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    main()
    app.run(debug=True)
