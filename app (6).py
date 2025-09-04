
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="S&P 500 Strategy Simulator", layout="wide")

st.title("S&P 500 Strategy Simulator")

# Load data
df = pd.read_csv("corrected_sp500_strategies.csv")

selected_month = st.slider("Select Month", min_value=int(df['Day'].min()), max_value=int(df['Day'].max()), value=1)
selected_data = df[df['Day'] == selected_month].iloc[0]

st.subheader(f"Summary for Month {selected_month}")
st.write(f"Simulated Index Level: {selected_data['Index']:.2f}")
st.write(f"Covered Call Profit: {selected_data['Covered Call Profit']:.2f}")
st.write(f"Protective Put Profit: {selected_data['Protective Put Profit']:.2f}")
st.write(f"Short Put Entry Profit: {selected_data['Short Put Entry Profit']:.2f}")

# Monthly return chart
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Day'], y=df['S&P 500 Monthly %'], mode='lines+markers', name='S&P 500'))
fig.add_trace(go.Scatter(x=df['Day'], y=df['Covered Call Profit Monthly %'], mode='lines', name='Covered Call'))
fig.add_trace(go.Scatter(x=df['Day'], y=df['Protective Put Profit Monthly %'], mode='lines', name='Protective Put'))
fig.add_trace(go.Scatter(x=df['Day'], y=df['Short Put Entry Profit Monthly %'], mode='lines', name='Short Put Entry'))
fig.update_layout(title="Monthly Percentage Returns", xaxis_title="Month", yaxis_title="Return (%)")
st.plotly_chart(fig, use_container_width=True)
