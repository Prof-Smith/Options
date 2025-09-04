
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data
df = pd.read_csv("sp500_strategies_with_tooltips.csv")

st.title("S&P 500 Strategy Simulator with Tooltips")

# Day slider
selected_day = st.slider("Select Day", min_value=1, max_value=30, value=1)
selected_data = df[df['Day'] == selected_day].iloc[0]

# Summary with tooltips
st.subheader(f"Summary for Day {selected_day}")
st.write(f"Simulated Index Level: {selected_data['Index']:.2f}")
st.write(f"Covered Call Profit: {selected_data['Covered Call Profit']:.2f}")
st.caption(f"Tooltip: {selected_data['Covered Call Tooltip']}")
st.write(f"Protective Put Profit: {selected_data['Protective Put Profit']:.2f}")
st.caption(f"Tooltip: {selected_data['Protective Put Tooltip']}")
st.write(f"Short Put Entry Profit: {selected_data['Short Put Entry Profit']:.2f}")
st.caption(f"Tooltip: {selected_data['Short Put Entry Tooltip']}")

# Chart 1: Simulated Index
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['Day'], y=df['Index'], mode='lines+markers', name='Simulated Index'))
fig1.update_layout(title="Simulated S&P 500 Index", xaxis_title="Day", yaxis_title="Index Level")
st.plotly_chart(fig1)

# Chart 2: Strategy Payoffs
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df['Day'], y=df['Covered Call Profit'], mode='lines', name='Covered Call'))
fig2.add_trace(go.Scatter(x=df['Day'], y=df['Protective Put Profit'], mode='lines', name='Protective Put'))
fig2.add_trace(go.Scatter(x=df['Day'], y=df['Short Put Entry Profit'], mode='lines', name='Short Put Entry'))
fig2.update_layout(title="Strategy Payoffs Over Time", xaxis_title="Day", yaxis_title="Profit/Loss")
st.plotly_chart(fig2)
