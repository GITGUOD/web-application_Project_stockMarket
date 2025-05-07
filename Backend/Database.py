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

        # Create the table "tickers" which will be used to add stocks if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE stock (
                ticketSymbol VARCHAR(10) PRIMARY KEY,
                name VARCHAR(100),
                -- any other stock related metadata
            );
        """)

        # Create table for time frames such as daily, weekly, monthly etc
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS timeframes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timeframe VARCHAR(20) not NULL UNIQUE
            )
        """)

        # Create table for stock prices with reference to timeframe
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

    #Closing the connection
    def close(self):
        self.cursor.close()
        self.conn.close()