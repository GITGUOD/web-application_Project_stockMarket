# Backend/MLModel/predictor.py

import joblib
import numpy as np
from Backend.MLModel.util import prepare_features


def load_model(model_path="models/stock_model.pkl"):
    return joblib.load(model_path)


def predict_next(df, model_path="models/stock_model.pkl"):

    # loads the data
    model = load_model(model_path)
    X, y = prepare_features(df)

    if len(X) == 0:
        raise ValueError("Insufficient data for prediction.")

    # Takes the last row of features (most recent stock day)
    # This will be used to predict tomorrow’s price
    latest_features = X.iloc[-1:].values
    # Runs prediction using .predict(...)
    # The [0] just takes the first result (since it's a 1-item array)
    predicted_price = model.predict(latest_features)[0]
    return predicted_price
