import streamlit as st
import pandas as pd
import datetime
import random
import plotly.express as px

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

def fetch_exchange_rates():
    import requests
    response = requests.get(API_URL)

    if response.status_code != 200:
        st.error("Error fetching exchange rates.")
        return None

    data = response.json()

    if "rates" in data:
        selected_currencies = {"USD": 1.0, "LRD": data["rates"].get("LRD", 0)}

        df = pd.DataFrame(list(selected_currencies.items()), columns=["Currency", "Rate"])

        df["Daily Inflation Rate"] = [random.uniform(0.05, 0.2) for _ in range(len(df))]

        return df

    return None



def predict_exchange_rate(base_currency, target_currency, base_inflation, target_inflation, days=7):
    rates_df = fetch_exchange_rates()

    if rates_df is None or rates_df.empty:
        return None

    try:
        base_rate = rates_df.loc[rates_df["Currency"] == base_currency, "Rate"].values[0]
        target_rate = rates_df.loc[rates_df["Currency"] == target_currency, "Rate"].values[0]


        predicted_rates = []
        for day in range(1, days + 1):
            base_rate *= (1 + base_inflation / 100)
            target_rate *= (1 + target_inflation / 100)
            predicted_rates.append(target_rate / base_rate)

        return predicted_rates

    except IndexError:
        return None



st.title("Convert & Predict LRD Rates")


selected_date = st.date_input("📅 Select a date to view the exchange rate", datetime.date.today())
selected_date_str = selected_date.strftime("%Y-%m-%d")

st.write(f"**Exchange rate for:** {selected_date_str}")
rates_df = fetch_exchange_rates()

if rates_df is not None and not rates_df.empty:
    st.dataframe(rates_df)

    rate_data = rates_df[rates_df["Currency"] == "LRD"]

    if not rate_data.empty:
        exchange_rate = rate_data["Rate"].values[0]
        st.write(f"💵 **Today's Rate {selected_date_str}:** **{exchange_rate} LRD/USD**")
    else:
        st.warning(f"⚠️ No exchange rate data available for {selected_date_str}")

    st.sidebar.header("🔄 Currency Conversion")
    base_currency = st.sidebar.selectbox("Base Currency", [" ", "USD", "LRD"])
    target_currency = st.sidebar.selectbox("Target Currency", [" ", "USD", "LRD"])
    amount = st.sidebar.number_input("Amount", min_value=1.0, value=1.0)

    try:
        base_rate = rates_df.loc[rates_df["Currency"] == base_currency, "Rate"].values[0]
        target_rate = rates_df.loc[rates_df["Currency"] == target_currency, "Rate"].values[0]

        converted_amount = amount * (target_rate / base_rate)
        st.sidebar.subheader("💲 Converted Amount:")
        st.sidebar.success(f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")

        if st.button("Predict Exchange Rate with Inflation"):
            if base_currency and target_currency:

                base_inflation = rates_df.loc[rates_df["Currency"] == base_currency, "Daily Inflation Rate"].values[0]
                target_inflation = rates_df.loc[rates_df["Currency"] == target_currency, "Daily Inflation Rate"].values[
                    0]

                predictions = predict_exchange_rate(base_currency, target_currency, base_inflation, target_inflation)

                if predictions is not None:
                    df_pred = pd.DataFrame({"Day": list(range(1, 8)), "Predicted Rate": predictions})
                    fig = px.bar(df_pred, x="Day", y="Predicted Rate",
                                 title=f" Predicted Exchange Rate ({base_currency} to {target_currency})",
                                 labels={"Day": "Day", "Predicted Rate": "Exchange Rate"},
                                 color="Predicted Rate",
                                 text_auto=True)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("⚠️ Prediction failed. Please check currency selection.")

    except IndexError:
        st.error("⚠️ Error retrieving exchange rate data. Please check currency selection.")

else:
    st.error("⚠️ Failed to fetch exchange rates.")
