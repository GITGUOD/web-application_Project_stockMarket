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
            CREATE TABLE IF NOT EXISTS tickers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                symbol VARCHAR(10) NOT NULL UNIQUE,
                name VARCHAR(100)
            )
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