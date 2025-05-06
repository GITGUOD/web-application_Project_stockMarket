import mysql.connector

# Connect to MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tonny2002"  # Replace with your MySQL root password
)
cursor = conn.cursor()

# Create the database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS stockdb")
print("Database 'stockdb' ensured.")

# Step 3: Connect specifically to the 'stockdb' database
conn.database = 'stockdb'

# Step 4: Create a table for tickers
cursor.execute("""
CREATE TABLE IF NOT EXISTS tickers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100)
)
""")
print("Table 'tickers' ensured.")

# Cleanup
cursor.close()
conn.close()
