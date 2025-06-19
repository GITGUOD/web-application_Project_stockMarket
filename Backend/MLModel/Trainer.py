# Backend/MLModel/trainer.py

import joblib
from sklearn.linear_model import LinearRegression #Simple ML model which fits/draws best line
from sklearn.model_selection import train_test_split #Splits the data into training and testing parts
from Backend.MLModel.util import prepare_features #import our data in util

#df = dataframe
def train_model(df, model_path="models/stock_model.pkl"):
    """
    Trains a simple linear regression model to predict next-day price.
    """

    # function to get input and output data.
    X, y = prepare_features(df)

    # Check if there's data
    if X is None or y is None or len(X) == 0:
        raise ValueError("Not enough data to train model.")

    #Splits the data:

    # - 80% will be used to train
    # - 20% will be used to test
    # - shuffle=False means we keep the time order, which is important for stock data, in other words, not suffling data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    # Creates a Linear Regression model.
    # .fit(...) means the model learns by looking at inputs (X_train) and expected outputs (y_train).
    model = LinearRegression()
    model.fit(X_train, y_train)

    #This shows how well the model performs on test data.
    #The score (called R²) is between:
        #1.0 = perfect prediction
        #0.0 = not good
        #Negative = worse than guessing
    score = model.score(X_test, y_test)
    print(f"Model R^2 score: {score:.4f}")

    # Saves the model to a file (stock_model.pkl) so you don’t need to train it again every time.
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

    return model
