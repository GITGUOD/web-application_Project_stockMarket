from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
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
app.secret_key = "3f1cbe6d08b349a996fd5dcbdb876a78"
db = Database()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        success = db.create_user(username, password)
        if not success:
            return "User already exists", 400

        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.get_user_by_username(username)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        return "Invalid credentials", 401

    return render_template("login.html")

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect('/login')




@app.route('/')
def home():
    if 'user_id' not in session:
            return redirect('/login')
    return render_template("StockGrapth.html")

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
    
@app.route('/api/fibonacci')
def fibonacci():
    try:
        start = float(request.args.get('start'))
        end = float(request.args.get('end'))
        diff = end - start
        levels = {
            '0': end,
            '0.236': end - diff * 0.236,
            '0.382': end - diff * 0.382,
            '0.5': end - diff * 0.5,
            '0.618': end - diff * 0.618,
            '0.786': end - diff * 0.786,
            '1': start
        }
        return jsonify(levels)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    


if __name__ == "__main__":
    main()
    app.run(debug=True)
