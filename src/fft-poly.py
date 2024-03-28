import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys

symbol = sys.argv[1] # choose ticker symbol (e.g., TSLA, GOOG, AAPL)
timeframe = sys.argv[2] # choose timeframe (e.g., max, 5y, 6mo)
poly_degree = int(sys.argv[3]) # choose polynomial degree as basis for extrapolation (e.g., 3, 5, 10)

# e.g. run 'python3 fft.py TSLA max 5'

ticker = yf.Ticker(symbol)
dataset_ex_df = ticker.history(period=timeframe)
# dataset_ex_df['Close'].plot(title=f'{symbol} stock price ($)', figsize=(14,7))

# Calculate the Fourier Transform
data_FT = dataset_ex_df[['Close']]
close_fft = np.fft.fft(np.asarray(data_FT['Close'].tolist()))
fft_df = pd.DataFrame({'fft':close_fft})
fft_df['absolute'] = fft_df['fft'].apply(lambda x: np.abs(x))
fft_df['angle'] = fft_df['fft'].apply(lambda x: np.angle(x))

# Plot the Fourier Transforms
transforms = []
plt.figure(figsize=(14, 7), dpi=100)
plt.plot(np.asarray(data_FT['Close'].tolist()),  label='Real')
for num_ in [3, 6, 9]:
    fft_list_m10 = np.copy(close_fft)
    fft_list_m10[num_:-num_] = 0
    transform = plt.plot(np.fft.ifft(fft_list_m10), label='Fourier transform with {} components'.format(num_))
    # save the matplotlib object for later extrapolation
    transforms.append(transform[0])
plt.xlabel('Days')
plt.ylabel('USD')
plt.title(f'{symbol} (close) stock prices & Fourier transforms')
plt.legend()

colours = ['y', 'g', 'r']

# Extrapolate predicted polynomials on the Fourier Transforms
colour_index = 0
for transform in transforms:
    x_vals = transform.get_data()[0]
    y_vals = transform.get_data()[1]
    z = np.polyfit(x_vals, y_vals, poly_degree)
    f = np.poly1d(z)

    # plots points of the extrapolated polynomial
    # first arg is starting x-coordinate
    # second arg is ending x-coordinate
    # third arg is number of points
    # change these values according to the generated width of the original plot
    # e.g., if command line args are 'TSLA', 'max', and 5 then
    # 3000, 3600, 50 means show the extrapolated polynomial between 3000 and 3600
    # with 50 points (predicting next 100 days)
    for x1 in np.linspace(3000, 3600, 50):
        plt.plot(x1, f(x1), colours[colour_index] + '+')
    
    colour_index += 1

plt.show()

# notes:
# 
# - realistically not a feasible method of making accurate predictions
# - huge variation in results depending on chosen polynomial degree
# - the Fourier Transform model obtained from here <https://medium.com/shikhars-data-science-projects/predicting-stock-prices-using-arima-fourier-transformation-and-deep-learning-e5fb4f693c85>
#   might not actually be amenable to the kind of extrapolation that is done here <https://www.tradingview.com/script/ffvTzAlA-Fourier-Extrapolation-of-Variety-Moving-Averages-Loxx/>
#   or interpolation done here <https://www.math.utah.edu/~gustafso/s2018/2270/projects-2016/williamsBarrett/williamsBarrett-Fast-Fourier-Transform-Predicting-Financial-Securities-Prices.pdf>
#   essentially meaning the model from the first source (which is used here to generate the three fourier transforms)
#   is incompatible with what is being suggested in the other two sources
