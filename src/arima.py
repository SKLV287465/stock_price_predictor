#!/usr/bin/env python3

import sys
import yfinance as yf
import pandas as pd
from pandas.plotting import autocorrelation_plot
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# Obtains the stock data for a particular ticker and time interval
def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data['Close']

ticker = sys.argv[1]
start_date = sys.argv[2]
end_date = sys.argv[3]
data = get_stock_data(ticker, start_date, end_date)

# Generate date index with frequency information
date_range = pd.date_range(start=data.index[0], periods=len(data), freq='D')

# Reindex the data with the generated date range for uniform indexing
data.index = date_range

# Plot stock data
plt.figure(figsize=(10, 6))
data.plot()
plt.title(f'{ticker} Stock Prices from {start_date} to {end_date}')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.show()

# Fit ARIMA model --> ARIMA(p, d, q)
model = ARIMA(data, order=(1, 1, 1))
model_fit = model.fit()

# Forecast the next {forecast_steps} days
forecast_steps = 30
forecast = model_fit.forecast(steps=forecast_steps)

# Plot the original data and forecasted values
plt.figure(figsize=(10, 6))
plt.plot(data, label='Original Data', color='blue')
plt.plot(forecast, label='Forecasted Data', color='red')
plt.title(f'ARIMA Forecast for {ticker} Stocks')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.show()

print("Forecasted values:")
print(forecast)