from flask import Flask, jsonify
from Backend.Database import Database

app = Flask(__name__)
db = Database()

@app.route("/stock/<symbol>/prices")
def get_stock_prices(symbol):
    data = db.get_prices_for_ticker(symbol)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
