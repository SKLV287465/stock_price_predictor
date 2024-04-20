import yfinance as yf
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import sys
import scraper

symbol = "TSLA"
poly_degree = 3

# e.g. run 'python3 fft.py TSLA max 5'


data = scraper.get_all_data(symbol)

# Calculate the Fourier Transform
def calculate_fourier_transform(data):
    closeData = data[['Close']]
    fft = np.fft.fft(np.asarray(closeData['Close'].tolist()))

    transforms = []

    for n in [3, 6, 9]:
        fft_intermediete = np.copy(fft)
        fft_intermediete[n:-n] = 0
        transform = plt.plot(np.fft.ifft(fft_intermediete), label='Fourier transform with {} components'.format(n))
        # save the matplotlib object for later extrapolation
        transforms.append(transform[0])
    return transforms
def generate_polynomial_fit(data):
    return plt
def calculate_polynomial_fit(transforms, poly_degree):
    # Extrapolate predicted polynomials on the Fourier Transforms
    polynomials = []

    for transform in transforms:
        x_vals = transform.get_data()[0]
        y_vals = transform.get_data()[1]
        z = np.polyfit(x_vals, y_vals, poly_degree)
        f = np.poly1d(z)
        polynomials.append(f)
    return polynomials

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

def show():
    plt.style.use('ggplot')
    plt.xlabel('Days')
    plt.ylabel('USD')
    plt.ylim(0)
    plt.title(f'{symbol} (close) stock prices & Fourier transforms')
    plt.legend()
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

if __name__ == '__main__':
    testdata = scraper.test_extrapolationToday(symbol,200, 60)
    data = scraper.get_last(symbol, 365)
    plt.figure(figsize=(14, 7), dpi=100)
    plt.plot(np.asarray(testdata[1]['Close'].tolist()),  label='Real')
    transforms = calculate_fourier_transform(testdata[0])
    polynomials = calculate_polynomial_fit(transforms, poly_degree)
    plot_polynomial(polynomials, 0, len(data))


    show()