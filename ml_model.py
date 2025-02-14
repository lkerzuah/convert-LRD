import numpy as np
from sklearn.linear_model import LinearRegression

def generate_historical_rates(base_currency, target_currency):
    np.random.seed(42)
    return np.linspace(1.0, 2.0, num=30)

def predict_exchange_rate(base_currency, target_currency, base_inflation, target_inflation, days=7):
    rates = generate_historical_rates(base_currency, target_currency)

    if len(rates) < 5:
        return None

    X = np.arange(len(rates)).reshape(-1, 1)
    y = np.array(rates)

    model = LinearRegression()
    model.fit(X, y)

    future_X = np.arange(len(rates), len(rates) + days).reshape(-1, 1)
    predictions = model.predict(future_X)

    inflation_factor = (1 + (base_inflation - target_inflation) / 100) ** np.arange(1, days + 1)
    adjusted_predictions = predictions * inflation_factor

    return adjusted_predictions.tolist()
