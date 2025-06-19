# Backend/MLModel/utils.py

import pandas as pd
import ta  # technical analysis library


def prepare_features(df):
    """
    Turns historical stock data into a format suitable for ML training.
    Example: Use past Open/High/Low/Close to predict next day's Close.
    """

    #df = dataframe
    # Checking if there is enough data in dataframe, len(df), especially for indicators
    if df is None or len(df) < 30:
        return None, None

    # Makes a copy of the dataframe
    df = df.copy()

    # Add Simple Moving Averages (SMA)
    df['SMA_10'] = ta.trend.sma_indicator(df['Close'], window=10)
    df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)

    # Add Relative Strength Index (RSI)
    df['RSI_14'] = ta.momentum.rsi(df['Close'], window=14)

    # Add MACD (Moving Average Convergence Divergence)
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    df['MACD_diff'] = macd.macd_diff()

    # Makes a new columne 'Target' which is the next day's closing price.
    df['Target'] = df['Close'].shift(-1)

    #Removes rows that have no values
    df.dropna(inplace=True)

    feature_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'SMA_10', 'SMA_20', 'RSI_14', 'MACD', 'MACD_signal', 'MACD_diff']
    #X are inputs which will be used to predict based on the data we have on feature cols
    X = df[feature_cols]
    # y is the model's prediction
    y = df['Target']

    return X, y
