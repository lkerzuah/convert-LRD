import requests
import pandas as pd
import random

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"


def fetch_exchange_rates():
    response = requests.get(API_URL)

    if response.status_code != 200:
        print("Error fetching exchange rates.")
        return None

    data = response.json()

    if "rates" in data:
        # Keep only USD and LRD
        selected_currencies = {"USD": 1.0, "LRD": data["rates"].get("LRD", 0)}

        df = pd.DataFrame(list(selected_currencies.items()), columns=["Currency", "Rate"])

        # Simulate daily inflation rates (random between 0.05% and 0.2%)
        df["Daily Inflation Rate"] = [random.uniform(0.05, 0.2) for _ in range(len(df))]

        # Predict exchange rates for the next 7 days using inflation rate
        predictions = []
        for _, row in df.iterrows():
            rates = [row["Rate"] * (1 + row["Daily Inflation Rate"] / 100) ** i for i in range(1, 8)]
            predictions.append(rates)

        # Add predictions to DataFrame
        for i in range(7):
            df[f"Day {i + 1} Prediction"] = [pred[i] for pred in predictions]

        return df

    return None
