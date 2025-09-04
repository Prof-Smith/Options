
import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import norm
import plotly.graph_objects as go

# Black-Scholes formula
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

st.title("S&P 500 Derivative Strategy Simulator")

# Sidebar inputs
initial_index = st.sidebar.slider("Initial S&P 500 Index", 4000, 5000, 4500)
strike_call = st.sidebar.slider("Call Option Strike Price", 4400, 4700, 4550)
strike_put = st.sidebar.slider("Put Option Strike Price", 4300, 4600, 4450)
T = st.sidebar.slider("Time to Expiration (Years)", 0.1, 1.0, 0.25)
r = st.sidebar.slider("Risk-Free Rate (%)", 0.0, 0.1, 0.03)
sigma = st.sidebar.slider("Volatility (%)", 0.1, 0.5, 0.2)

# Convert rates
r = float(r)
sigma = float(sigma)

# Calculate option premiums
premium_call = black_scholes(initial_index, strike_call, T, r, sigma, 'call')
premium_put = black_scholes(initial_index, strike_put, T, r, sigma, 'put')

# Simulate index levels
np.random.seed(42)
days = 30
returns = np.random.normal(loc=0.0005, scale=sigma / np.sqrt(252), size=days)
index_levels = initial_index * np.cumprod(1 + returns)

# Strategy calculations
def covered_call(index):
    return np.minimum(index - initial_index, strike_call - initial_index) + premium_call

def protective_put(index):
    return np.maximum(index - initial_index, strike_put - index) - premium_put

def short_put_entry(index):
    return np.where(index >= strike_put, premium_put, premium_put - (strike_put - index))

# Create DataFrame
df = pd.DataFrame({
    "Day": np.arange(1, days + 1),
    "Index": index_levels,
    "Covered Call": covered_call(index_levels),
    "Protective Put": protective_put(index_levels),
    "Short Put Entry": short_put_entry(index_levels)
})

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Day"], y=df["Covered Call"], mode='lines', name='Covered Call'))
fig.add_trace(go.Scatter(x=df["Day"], y=df["Protective Put"], mode='lines', name='Protective Put'))
fig.add_trace(go.Scatter(x=df["Day"], y=df["Short Put Entry"], mode='lines', name='Short Put Entry'))
fig.update_layout(title="Strategy Payoffs Over Time", xaxis_title="Day", yaxis_title="Profit/Loss")

st.plotly_chart(fig)

st.subheader("Student Activity Prompts")
st.markdown("""
1. Which strategy provides the best downside protection?
2. At what index level does the covered call strategy cap its upside?
3. How does the short put entry strategy behave when the index falls below the strike price?
4. Compare the breakeven points for each strategy.
""")
