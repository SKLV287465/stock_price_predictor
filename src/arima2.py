#!/usr/bin/env python3

import sys
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import r2_score
from pmdarima.arima import auto_arima
from pmdarima.arima import ADFTest

# Obtains the stock data for a particular ticker and time interval
def get_stock_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    return df['Close']

ticker = sys.argv[1]
start_date = sys.argv[2]
end_date = sys.argv[3]
df = get_stock_data(ticker, start_date, end_date)


# Perform Augmented Dickey-Fuller Test to check stationarity of data
# If p-val from test is < 0.05, then null hypothesis is rejected, indicating data
# is stationary. If > 0.05, data is non-stationary (need to make stationary to
# fit ARIMA model)
adf_test = ADFTest(alpha=0.05)
result = adf_test.should_diff(df)
print(result[0])

differencing = 0
while result[0] > 0.05:
    differencing += 1

    if differencing == 2:
        break

    # Differencing the data
    df_diff = df.diff().dropna()
    # Redo ADF test on the differenced data
    result = adf_test.should_diff(df_diff)
    print(result[0])

actual_data_size = int(0.8 * len(df))
# actual - selects the bottom 80% of the data using slicing.
# test - selects the last 20% of the data using slicing.
actual = df[:actual_data_size]
test = df[actual_data_size:]
plt.plot(actual)
plt.plot(test)
plt.show()

actual.index = pd.date_range(start=start_date, periods=len(actual))
test.index = pd.date_range(start=actual.index[-1] + pd.Timedelta(days=1), periods=len(test))

# Fit the data to the ARIMA model, using the differencing parameter determined
model=auto_arima(actual, start_p = 0, d = differencing, start_q = 0,
          max_p = 5, max_d = differencing, max_q = 5, start_P = 0,
          D = 1, start_Q = 0, max_P = 5, max_D = 5,
          max_Q = 5, m = 12, seasonal = True, trace = True,
          supress_warnings = True, stepwise = True)

prediction = pd.DataFrame(model.predict(n_periods=len(test)), index=test.index, columns=['Predicted'])

plt.plot(actual, label = "Actual")
plt.plot(test, label = "Test")
plt.plot(prediction, label = "Predicted")
plt.legend(loc = 'upper left')
plt.show()

# Calcuate the r-sqared value of the test data compared to the predicted data
r2 = r2_score(test, prediction)
print(r2)