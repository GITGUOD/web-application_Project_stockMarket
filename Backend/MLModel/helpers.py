import pandas as pd
from Backend.Database import Database as db

def get_price_history_from_db(db, symbol, timeframe):
    rows = db.get_prices_for_ticker(symbol, timeframe)
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)
    return df
