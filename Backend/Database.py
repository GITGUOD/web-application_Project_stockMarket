import mysql.connector

class Database:

    #Initiating db
    def __init__(self, host="localhost", user="root", password="Tonny2002", database="stockdb"):
        self.conn =mysql.connector.connect(
            host=host,
            user=user,
            password=password  # MySQL password/code
        )

        #Variable for the db connection
        self.cursor = self.conn.cursor()

        # Create the database if it doesn't exist
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        self.conn.database = database  # Connect to the database

        # Create the table "stock" which will be used to add stocks if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock (
                ticketSymbol VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100)
            );
        """)

        # Create table for ticket
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ticket (
                ticketSymbol VARCHAR(10),
                timeframe VARCHAR(20),
                PRIMARY KEY (ticketSymbol, timeframe),
                FOREIGN KEY (ticketSymbol) REFERENCES stock(ticketSymbol)
            );

        """)

        # Create table for stock prices with timeframes, opening prices etc
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS price (
                ticketSymbol VARCHAR(10),
                timeframe VARCHAR(20),
                date DATE,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume BIGINT,
                PRIMARY KEY (ticketSymbol, timeframe, date),
                FOREIGN KEY (ticketSymbol, timeframe) REFERENCES ticket(ticketSymbol, timeframe)
            );

        """)

    #Inserting stocks into the table TICKERS
    def insert_ticker(self, symbol, name):
        symbol = symbol.upper()
        self.cursor.execute(
            "INSERT IGNORE INTO stock (ticketSymbol, name) VALUES (%s, %s)",
            (symbol, name)
        )
        self.cursor.execute(
            "INSERT IGNORE INTO ticket (ticketSymbol, timeframe) VALUES (%s, %s)",
            (symbol, "1d")
        )
        self.conn.commit()

        

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
    def get_prices_for_ticker(self, symbol, timeframe="1d"):
        self.cursor.execute("""
            SELECT date, open, high, low, close, volume 
            FROM price 
            WHERE ticketSymbol = %s AND timeframe = %s 
            ORDER BY date ASC
        """, (symbol, timeframe))
        return self.cursor.fetchall()


    #Closing the connection
    def close(self):
        self.cursor.close()
        self.conn.close()