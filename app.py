
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data
df = pd.read_csv("sp500_simulated_strategies.csv")

st.title("S&P 500 Strategy Simulator")

# Day slider
selected_day = st.slider("Select Day", min_value=1, max_value=30, value=1)
selected_data = df[df['Day'] == selected_day].iloc[0]

# Summary
st.subheader(f"Summary for Day {selected_day}")
st.write(f"Simulated Index Level: {selected_data['Index']:.2f}")
st.write(f"Covered Call Value: {selected_data['Covered Call']:.2f}")
st.write(f"Protective Put Value: {selected_data['Protective Put']:.2f}")
st.write(f"Short Put Entry Value: {selected_data['Short Put Entry']:.2f}")

# Chart 1: Simulated Index
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['Day'], y=df['Index'], mode='lines+markers', name='Simulated Index'))
fig1.update_layout(title="Simulated S&P 500 Index", xaxis_title="Day", yaxis_title="Index Level")
st.plotly_chart(fig1)

# Chart 2: Strategy Payoffs
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df['Day'], y=df['Covered Call'], mode='lines', name='Covered Call'))
fig2.add_trace(go.Scatter(x=df['Day'], y=df['Protective Put'], mode='lines', name='Protective Put'))
fig2.add_trace(go.Scatter(x=df['Day'], y=df['Short Put Entry'], mode='lines', name='Short Put Entry'))
fig2.update_layout(title="Strategy Payoffs Over Time", xaxis_title="Day", yaxis_title="Profit/Loss")
st.plotly_chart(fig2)
