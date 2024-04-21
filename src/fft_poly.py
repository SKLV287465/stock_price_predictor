import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
import scraper


symbol = "TSLA"
poly_degree = 3

# Calculate the Fourier Transform
def calculate_fourier_transform(data, num_components):
    fft = np.fft.fft(np.asarray(data))

    fft_intermediete = np.copy(fft)
    fft_intermediete[num_components:-num_components] = 0
    return np.fft.ifft(fft_intermediete)

def calculate_polynomial_fit(data, poly_degree):
    # Extrapolate predicted polynomials on the Fourier Transforms

    x_vals = np.arange(0, data.size)

    y_vals = data
    z = np.polyfit(x_vals, y_vals, poly_degree)
    return  np.poly1d(z)

        # plots points of the extrapolated polynomial
        # first arg is starting x-coordinate
        # second arg is ending x-coordinate
        # third arg is number of points
        # change these values according to the generated width of the original plot
        # e.g., if command line args are 'TSLA', 'max', and 5 then
        # 3000, 3600, 50 means show the extrapolated polynomial between 3000 and 3600
        # with 50 points (predicting next 100 days)
def plot_polynomial(polynomials, start, extrapolation):
    colour_index = 0
    colours = ['y', 'g', 'r']
    for f in polynomials:
        for x1 in np.linspace(start, start + extrapolation, 100):
            plt.plot(x1, f(x1), colours[colour_index] + '+')

        colour_index += 1

def polynomial_predict(f, day):
    return f(day) - f(day - 1)

def predict_next_day(data, num_days):
    data = data[0:num_days]
    transforms = calculate_fourier_transform(data)
    polynomials = calculate_polynomial_fit(transforms, poly_degree)
    return polynomials[0](num_days + 1) - polynomials[0](num_days)


def show():
    plt.style.use('ggplot')
    plt.xlabel('Days')
    plt.ylabel('USD')
    plt.ylim(0)
    plt.title(f'{symbol} (close) stock prices & Fourier transforms')
    plt.legend()
    plt.show()

def extrapolate(data, num_days, degree = 1, num_components = 0):
    n = data.size
    size =  n + num_days
    trend_polynomial = calculate_polynomial_fit(data, degree)
    detrended_data = np.zeros(n)
    for i in range(n):
        detrended_data[i] = data[i] - trend_polynomial(i)
    if num_components > 0:
        detrended_data = calculate_fourier_transform(detrended_data, num_components)
    new_data = np.zeros(size)

    # Calculate new data
    for i in range(size):
        new_data[i] = detrended_data[i % n] + trend_polynomial(i)
    return new_data

def extrapolate_predict(data,degree, num_day, look_ahead, num_components = 0):
    data = data[0:num_day]
    extrapolation = extrapolate(data, look_ahead, degree, num_components)
    return extrapolation[num_day + look_ahead - 1] - extrapolation[num_day-1]

def extrapolate_predict_next_day(data, num_day,degree = 1, num_components = 0):
    return extrapolate_predict(data, num_day,degree, 1, num_components)
# notes:
# 
# - realistically not a feasible method of making accurate predictions
# - huge variation in results depending on chosen polynomial degree
# - the Fourier Transform model obtained from here <https://medium.com/shikhars-data-science-projects/predicting-stock-prices-using-arima-fourier-transformation-and-deep-learning-e5fb4f693c85>
#   might not actually be amenable to the kind of extrapolation that is done here <https://www.tradingview.com/script/ffvTzAlA-Fourier-Extrapolation-of-Variety-Moving-Averages-Loxx/>
#   or interpolation done here <https://www.math.utah.edu/~gustafso/s2018/2270/projects-2016/williamsBarrett/williamsBarrett-Fast-Fourier-Transform-Predicting-Financial-Securities-Prices.pdf>
#   essentially meaning the model from the first source (which is used here to generate the three fourier transforms)
#   is incompatible with what is being suggested in the other two sources

if __name__ == '__main__':
    reduced, actual = scraper.test_extrapolationToday(symbol,300, 40)
    plt.figure(figsize=(14, 7), dpi=100)
    plt.plot(np.asarray(actual['Close'].tolist()),  label='Real')
    # Account for weekend non trading days
    data = reduced['Close']
    extrapolation = extrapolate(data, len(actual) - len(reduced), 1)
    plt.plot(np.arange(0, extrapolation.size), extrapolation, 'r', label='Projection', linewidth=1)
    transform = calculate_fourier_transform(reduced['Close'], 3)
    polynomials = calculate_polynomial_fit(transform, poly_degree)
    # plot_polynomial(polynomials, 0, len(testdata[1]))


    show()