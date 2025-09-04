
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# Load or regenerate data
if os.path.exists("sp500_simulated_strategies.csv"):
    df = pd.read_csv("sp500_simulated_strategies.csv")
else:
    import numpy as np
    np.random.seed(42)
    initial_index = 4500
    days = 30
    volatility = 0.02
    returns = np.random.normal(loc=0.0005, scale=volatility, size=days)
    index_levels = initial_index * np.cumprod(1 + returns)
    strike_call = 4550
    strike_put = 4450
    premium_call = 50
    premium_put = 45
    def covered_call(index):
        return np.minimum(index - initial_index, strike_call - initial_index) + premium_call
    def protective_put(index):
        return np.maximum(index - initial_index, strike_put - index) - premium_put
    def short_put_entry(index):
        return np.where(index >= strike_put, premium_put, premium_put - (strike_put - index))
    df = pd.DataFrame({
        "Day": np.arange(1, days + 1),
        "Index": index_levels,
        "Covered Call": covered_call(index_levels),
        "Protective Put": protective_put(index_levels),
        "Short Put Entry": short_put_entry(index_levels)
    })

st.title("S&P 500 Strategy Simulator")
selected_day = st.slider("Select Day", min_value=1, max_value=30, value=1)
selected_data = df[df['Day'] == selected_day].iloc[0]

st.subheader(f"Summary for Day {selected_day}")
st.write(f"Simulated Index Level: {selected_data['Index']:.2f}")
st.write(f"Covered Call Value: {selected_data['Covered Call']:.2f}")
st.write(f"Protective Put Value: {selected_data['Protective Put']:.2f}")
st.write(f"Short Put Entry Value: {selected_data['Short Put Entry']:.2f}")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['Day'], y=df['Index'], mode='lines+markers', name='Simulated Index'))
fig1.update_layout(title="Simulated S&P 500 Index", xaxis_title="Day", yaxis_title="Index Level")
st.plotly_chart(fig1)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df['Day'], y=df['Covered Call'], mode='lines', name='Covered Call'))
fig2.add_trace(go.Scatter(x=df['Day'], y=df['Protective Put'], mode='lines', name='Protective Put'))
fig2.add_trace(go.Scatter(x=df['Day'], y=df['Short Put Entry'], mode='lines', name='Short Put Entry'))
fig2.update_layout(title="Strategy Payoffs Over Time", xaxis_title="Day", yaxis_title="Profit/Loss")
st.plotly_chart(fig2)
