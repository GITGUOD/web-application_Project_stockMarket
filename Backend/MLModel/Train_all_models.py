from Backend.Database import Database
from Backend.API.MarketData import MarketData
from Backend.MLModel.Trainer import train_model
from Backend.MLModel.util import prepare_features
from Backend.MLModel.helpers import get_price_history_from_db
import os

def main():
    db = Database()
    market_data = MarketData(db)

    # Load your sample tickers (e.g., MSFT, AAPL)
    tickers = market_data.get_samples()
    timeframes = ["1d", "1wk", "1mo", "1h"]  # Add more is possible if needed

    os.makedirs("models", exist_ok=True)

    for symbol, _ in tickers:
        print(f"Training model for {symbol}...")

        df = get_price_history_from_db(db, symbol, timeframes)
        if df.empty or len(df) < 40:
            print(f"Skipping {symbol} — not enough data.")
            continue

        try:
            train_model(df, model_path=f"models/{symbol.lower()}_model.pkl")
        except Exception as e:
            print(f"Error training {symbol}: {e}")

    db.close()

if __name__ == "__main__":
    main()
