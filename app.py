from decimal import Decimal
import decimal
from flask import Flask, flash, jsonify, render_template, request, session, redirect, url_for
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
    
@app.route('/buy', methods=['POST'])
def buy():
    data = request.get_json()
    user_id = data.get('user_id')
    symbol = data.get('symbol')
    quantity = data.get('quantity')

    # Validate inputs
    if not (user_id and symbol and quantity):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Get latest price for the stock symbol
    db.cursor.execute("""
        SELECT close 
        FROM price
        WHERE ticketSymbol = %s
        ORDER BY date DESC
        LIMIT 1
    """, (symbol,))
    price_row = db.cursor.fetchone()

    if not price_row:
        return jsonify({"error": "Price data not found for symbol"}), 400
    
    price = float(price_row[0])

    # Call buy_stock with price
    result = db.buy_stock(user_id, symbol, quantity, price)

    if "error" in result:
        return jsonify(result), 400
    else:
        return jsonify(result), 200
    

@app.route('/sell', methods=['POST'])
def sell():
    data = request.get_json()
    user_id = data.get('user_id')
    symbol = data.get('symbol')
    quantity = data.get('quantity')

    # Validate inputs
    if not (user_id and symbol and quantity):
        return jsonify({"error": "Missing required fields"}), 400

    # Get latest price for the stock symbol
    db.cursor.execute("""
        SELECT close 
        FROM price
        WHERE ticketSymbol = %s
        ORDER BY date DESC
        LIMIT 1
    """, (symbol,))
    price_row = db.cursor.fetchone()

    if not price_row:
        return jsonify({"error": "Price data not found for symbol"}), 400
    
    price = float(price_row[0])

    # Call your sell_stock method (implement this similarly to buy_stock)
    result = db.sell_stock(user_id, symbol, quantity, price)

    if "error" in result:
        return jsonify(result), 400
    else:
        return jsonify(result), 200
    
@app.route('/api/session')
def get_session():
    user_id = session.get('user_id')
    return jsonify({'user_id': user_id})

@app.route('/portfolio')
def portfolio():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')  # Or handle appropriately
    
    # Fetch cash balance
    db.cursor.execute("SELECT initial_cash FROM users WHERE id = %s", (user_id,))
    cash_row = db.cursor.fetchone()
    cash_balance = cash_row[0] if cash_row else 0

    db.cursor.execute("""
        SELECT h.symbol, h.quantity, h.avg_price, p.close
        FROM holding h
        JOIN (
            SELECT ticketSymbol, MAX(date) as max_date
            FROM price
            GROUP BY ticketSymbol
        ) latest ON h.symbol = latest.ticketSymbol
        JOIN price p ON p.ticketSymbol = latest.ticketSymbol AND p.date = latest.max_date
        WHERE h.user_id = %s
    """, (user_id,))
    
    rows = db.cursor.fetchall()
    portfolio = []
    total_stock_value = Decimal('0.0')
    total_pnl = Decimal('0.0')

    for symbol, quantity, avg_price, current_price in rows:
    
        avg_price = Decimal(avg_price)
        current_price = Decimal(str(current_price))
        quantity = Decimal(quantity)


        pnl = (Decimal(str(current_price)) - avg_price) * quantity
        total_pnl += pnl


        try:
            pnl_percent = ((Decimal(str(current_price)) - avg_price) / avg_price) * 100
        except (decimal.DivisionByZero, ZeroDivisionError):
            pnl_percent = Decimal('0.0')

        total_stock_value += current_price * quantity

            
        portfolio.append({
            'symbol': symbol,
            'quantity': quantity,
            'avg_price': avg_price,
            'current_price': current_price,
            'pnl': pnl,
            'pnl_percent': pnl_percent

        })

    total_portfolio_value = cash_balance + total_stock_value


    return render_template('portfolio.html', portfolio=portfolio, cash_balance=cash_balance, total_portfolio_value=total_portfolio_value, total_pnl=total_pnl)


@app.route('/add_cash', methods=['POST'])
def add_cash():
    user_id = session.get('user_id')
    if not user_id:
        flash("Du måste vara inloggad för att lägga till cash.", "error")
        return redirect(url_for('portfolio'))

    amount_str = request.form.get('amount')
    if not amount_str:
        flash("Ingen summa angavs.", "error")
        return redirect(url_for('portfolio'))
    
    try:
        amount = float(amount_str)
    except ValueError:
        flash("Felaktig summa angavs.", "error")
        return redirect(url_for('portfolio'))

    if amount <= 0:
        flash("Summan måste vara positiv.", "error")
        return redirect(url_for('portfolio'))

    result = db.add_cash_to_user(user_id, amount)
    if "error" in result:
        flash(result["error"], "error")
    else:
        flash(result["success"], "success")

    return redirect(url_for('portfolio'))

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    user_id = session.get('user_id')
    if not user_id:
        flash("You must be logged in to delete your account.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        password = request.form.get('password')

        # Get user's hashed password from DB
        db.cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        row = db.cursor.fetchone()
        if not row:
            flash("User not found.", "error")
            return redirect(url_for('portfolio'))

        stored_password_hash = row[0]

        # Check password
        if not check_password_hash(stored_password_hash, password):
            flash("Incorrect password. Account deletion cancelled.", "error")
            return redirect(url_for('delete_account'))

        # Delete user data
        db.cursor.execute("DELETE FROM holding WHERE user_id = %s", (user_id,))
        db.cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db.conn.commit()

        # Clear session
        session.clear()

        flash("Your account has been deleted successfully.", "success")
        return redirect(url_for('home'))

    # GET request - show confirmation form
    return render_template('confirm_delete.html')


if __name__ == "__main__":
    main()
    app.run(debug=True)
