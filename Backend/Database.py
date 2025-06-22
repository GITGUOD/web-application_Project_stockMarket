from decimal import Decimal
import time
import mysql.connector
import os

class Database:

    #Initiating db
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "stockdb")
        self.port = int(os.getenv("DB_PORT", 3306))

        for attempt in range(10):  # Försök 10 gånger med 3 sekunders mellanrum
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    port=self.port

                )
                print("✅ Database connection established.")
                break
            except mysql.connector.Error as err:
                print(f"⏳ Attempt {attempt + 1}/10: Database not ready, retrying in 3s...")
                time.sleep(3)
        else:
            raise Exception("❌ Could not connect to the database after 10 attempts.")

        #Variable for the db connection
        self.cursor = self.conn.cursor()

        # Create the database if it doesn't exist
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self.conn.database = self.database  # Connect to the database

        # Create the table "stock" which will be used to add stocks if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock (
                ticketSymbol VARCHAR(30) PRIMARY KEY,
                name VARCHAR(100)
            );
        """)

        # Creating table for users
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(255) UNIQUE,
                    password VARCHAR(255),
                    initial_cash DECIMAL(10, 2) DEFAULT 10000      
                );
                                
                                
                            """)
        
        # Creating table for users holding
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS holding (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                user_id INTEGER,
                symbol VARCHAR(255),
                quantity INTEGER,
                avg_price DECIMAL(10, 2),
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
                            
                            """)
        #Creating table for users trades
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTO_INCREMENT,
                user_id INTEGER,
                action VARCHAR(255), -- 'BUY' eller 'SELL'
                symbol VARCHAR(255),
                quantity INTEGER,
                price DECIMAL(10, 2),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
                            
                            """)

         # Create table for timeframes
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS timeframe (
                timeframe VARCHAR(20) PRIMARY KEY
            );

        """)

        # Create table for stock prices with timeframes, opening prices etc
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS price (
                ticketSymbol VARCHAR(30),
                timeframe VARCHAR(20),
                date DATETIME,
                open DECIMAL(10, 2),
                high DECIMAL(10, 2),
                low DECIMAL(10, 2),
                close DECIMAL(10, 2),
                volume BIGINT,
                PRIMARY KEY (ticketSymbol, timeframe, date),
                FOREIGN KEY (ticketSymbol) REFERENCES stock(ticketSymbol),
                FOREIGN KEY (timeframe) REFERENCES timeframe(timeframe)

            );

        """)


        # Insert allowed timeframes if not already there
        allowed_timeframes = [
            '1m', '2m', '5m', '15m', '30m', '60m', '90m',
            '1h', '1d', '5d', '1wk', '1mo', '3mo'
        ]

        for tf in allowed_timeframes:
            self.cursor.execute("""
                INSERT IGNORE INTO timeframe (timeframe) VALUES (%s)
            """, (tf,))
        self.conn.commit()

    #Creating user
    def create_user(self, username, hashed_password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Failed to create user: {e}")
            return False

    # Get user 
    def get_user_by_username(self, username):
        self.cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        row = self.cursor.fetchone()
        return {"id": row[0], "username": row[1], "password": row[2]} if row else None



    # Adding cash to the user
    def add_cash_to_user(self, user_id, amount):
        if amount <= 0:
            return {"error": "Amount must be positive"}

        # Check if user exists
        self.cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not self.cursor.fetchone():
            return {"error": "User not found"}

        self.cursor.execute("""
            UPDATE users SET initial_cash = initial_cash + %s
            WHERE id = %s
        """, (amount, user_id))

        self.conn.commit()
        return {"success": f"Added ${amount:.2f} to user {user_id}"}

    #Inserting stocks
    def insert_ticker(self, symbol, name):
        symbol = symbol.upper()
        self.cursor.execute(
            "INSERT IGNORE INTO stock (ticketSymbol, name) VALUES (%s, %s)",
            (symbol, name)
        )
        #self.cursor.execute(
        #    "INSERT IGNORE INTO ticket (ticketSymbol) VALUES (%s)",
        #    (symbol,)
        #)
        self.conn.commit()

    def buy_stock(self, user_id, symbol, quantity, price):
        # Convert quantity and price to Decimal
        quantity = Decimal(quantity)
        price = Decimal(str(price))  # Convert float to str first to avoid precision issues
        total_cost = quantity * price

        # Get user cash
        self.cursor.execute("SELECT initial_cash FROM users WHERE id = %s", (user_id,))
        row = self.cursor.fetchone()
        if not row:
            return {"error": "User not found"}
        
        current_cash = row[0]
        if current_cash < total_cost:
            return {"error": "Insufficient funds"}
        
        # Check if user already owns this stock
        self.cursor.execute("""
            SELECT quantity, avg_price FROM holding 
            WHERE user_id = %s AND symbol = %s
        """, (user_id, symbol))
        holding = self.cursor.fetchone()

        if holding:
            old_qty, old_avg_price = holding
            new_qty = old_qty + quantity
            new_avg_price = ((old_qty * old_avg_price) + (quantity * price)) / new_qty

            self.cursor.execute("""
                UPDATE holding 
                SET quantity = %s, avg_price = %s 
                WHERE user_id = %s AND symbol = %s
            """, (new_qty, new_avg_price, user_id, symbol))
        else:
            self.cursor.execute("""
                INSERT INTO holding (user_id, symbol, quantity, avg_price)
                VALUES (%s, %s, %s, %s)
            """, (user_id, symbol, quantity, price))

        # Deduct cash
        self.cursor.execute("""
            UPDATE users SET initial_cash = initial_cash - %s 
            WHERE id = %s
        """, (total_cost, user_id))

        # Log the trade
        self.cursor.execute("""
            INSERT INTO trades (user_id, action, symbol, quantity, price) 
            VALUES (%s, 'BUY', %s, %s, %s)
        """, (user_id, symbol, quantity, price))

        self.conn.commit()
        return {"success": f"Bought {quantity} of {symbol} at {price}"}
    

    # Sell stock
    def sell_stock(self, user_id, symbol, quantity, price):
        # Convert quantity and price to Decimal
        quantity = Decimal(quantity)
        price = Decimal(str(price))  # Convert float to str first to avoid precision issues
        
        total_value = quantity * price

        # Check if user has this stock
        self.cursor.execute("""
            SELECT quantity, avg_price FROM holding
            WHERE user_id = %s AND symbol = %s
        """, (user_id, symbol))
        holding = self.cursor.fetchone()

        if not holding:
            return {"error": f"You do not own any {symbol}"}

        current_quantity, avg_price = holding
        if quantity > current_quantity:
            return {"error": f"Not enough shares to sell. You have {current_quantity}"}

        # Update holdings or delete if selling all
        if quantity == current_quantity:
            self.cursor.execute("""
                DELETE FROM holding WHERE user_id = %s AND symbol = %s
            """, (user_id, symbol))
        else:
            new_quantity = current_quantity - quantity
            self.cursor.execute("""
                UPDATE holding SET quantity = %s WHERE user_id = %s AND symbol = %s
            """, (new_quantity, user_id, symbol))

        # Add cash to user's account
        self.cursor.execute("""
            UPDATE users SET initial_cash = initial_cash + %s
            WHERE id = %s
        """, (total_value, user_id))

        # Log the trade
        self.cursor.execute("""
            INSERT INTO trades (user_id, action, symbol, quantity, price)
            VALUES (%s, 'SELL', %s, %s, %s)
        """, (user_id, symbol, quantity, price))

        self.conn.commit()
        return {"success": f"Sold {quantity} of {symbol} at {price}"}


        

    #Inserting multple stocks
    def insert_multiple_tickers(self, tickers):
        for symbol, name in tickers:
            self.insert_ticker(symbol.upper(), name) #Symbol.upper() will make sure that simple the uppercase, ticketsymbol will be added. So instead of the whole Microsoft Inc etc only the four letters will be added

    #Inserting prices into the database
    def insert_price(self, ticketSymbol, timeframe, date, open_price, high_price, low_price, close_price, volume):
        """Inserts stock price data into the database."""
        try:
            self.cursor.execute("""
                INSERT INTO price (ticketSymbol, timeframe, date, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE open=%s, high=%s, low=%s, close=%s, volume=%s
            """, (ticketSymbol, timeframe, date, open_price, high_price, low_price, close_price, volume,
                  open_price, high_price, low_price, close_price, volume))
            self.conn.commit()
        except Exception as e:
            print(f"Failed to insert price data for {ticketSymbol} on {date}: {e}")

#Getting prices for the specific stock
    def get_prices_for_ticker(self, symbol, timeframe):
        self.cursor.execute("""
            SELECT date, open, high, low, close, volume 
            FROM price 
            WHERE ticketSymbol = %s AND timeframe = %s 
            ORDER BY date ASC
        """, (symbol, timeframe))
        return self.cursor.fetchall()
    
    #This is not used yet
    def get_stock_name(self, symbol):
        self.cursor.execute("SELECT name FROM stock WHERE ticketSymbol = %s", (symbol,))
        result = self.cursor.fetchone()
        return result[0] if result else "Unknown"



    #Closing the connection
    def close(self):
        self.cursor.close()
        self.conn.close()