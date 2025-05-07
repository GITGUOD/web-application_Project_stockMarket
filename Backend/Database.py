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
            CREATE TABLE stock (
                ticketSymbol VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100),
                -- any other stock related metadata
            );
        """)

        # Create table for ticket
        self.cursor.execute("""
            CREATE TABLE ticket (
                ticketSymbol VARCHAR(10),
                timeframe VARCHAR(20),
                PRIMARY KEY (ticketSymbol, timeframe),
                FOREIGN KEY (ticketSymbol) REFERENCES stock(ticketSymbol)
            );

        """)

        # Create table for stock prices with timeframes, opening prices etc
        self.cursor.execute("""
            CREATE TABLE price (
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
        self.cursor.execute(
            "INSERT IGNORE INTO tickers (symbol, name) VALUES (%s, %s)",
            (symbol, name)
        )
        self.conn.commit()

    #Inserting multple stocks
    def insert_multiple_tickers(self, tickers):
        for symbol, name in tickers:
            self.insert_ticker(symbol, name)

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

    #Closing the connection
    def close(self):
        self.cursor.close()
        self.conn.close()