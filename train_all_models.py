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
        for timeframe in timeframes:
            print(f"Training model for {symbol} timeframe {timeframe}...")
            df = get_price_history_from_db(db, symbol, timeframe)
            if df.empty:
                print(f"No data for {symbol} timeframe {timeframe}, skipping.")
                continue

            model_path = f"models/{symbol.lower()}_{timeframe}_model.pkl"
            try:
                train_model(df, model_path=model_path)
                print(f"Model trained and saved for {symbol} timeframe {timeframe}")
            except Exception as e:
                print(f"Failed to train model for {symbol} timeframe {timeframe}: {e}")

    db.close()

if __name__ == "__main__":
    main()
