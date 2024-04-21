# CLI arguments: SYMBOL DAY MONTH YEAR
# the arguments are for the start, program runs until present day
import markov.markov_helper as mh;
# import arima;
import fft_poly;
import datetime;
import sys
import math
import matplotlib.pyplot as plt

symbol = sys.argv[1]
window = int(sys.argv[2])
start_date = datetime.date(int(sys.argv[5]), int(sys.argv[4]), int(sys.argv[3]))
money = int(sys.argv[6])

stock_plot_data = []
fft_plot_data = []
markov_plot_data = []
# helper functions
def sell(stocks, data, index):
    return float(data['Close'][index]) * stocks

def buy(money, data, index):
    bought_stocks = math.floor(money / data['Close'][index])
    leftover = money - (bought_stocks * data['Close'][index])
    return int(bought_stocks), float(leftover)

# markov model with fft
def with_fft(money, plot, splot):
    plot_data = []
    data, timespan = mh.get_data_start_date(symbol, start_date)
    current_date = 1
    states = mh.markov_matrix(data, current_date, window)
    stocks = 0
    initialbuy = math.floor(money / data["Close"][1])
    for i in range(2, timespan):
        now = mh.get_categorised(data, current_date)
        diff = fft_poly.extrapolate_predict_next_day(data['Close'], i)
        if (now > 2 and diff >= 0):
            new, money = buy(money, data, i)
            stocks += new
        elif (diff < 0):
            newmon = sell(stocks, data, i)
            money += newmon
            stocks = 0
        current_date += 1
        plot.append(money + (stocks * data['Close'][i]))
        splot.append(initialbuy * data['Close'][i])
    return (money + (stocks * data['Close'][timespan - 1])) - (initialbuy *data['Close'][timespan - 1])

# markov model without fft
def without(money, plot):
    plot_data = []
    data, timespan = mh.get_data_start_date(symbol, start_date)
    current_date = 1
    states = mh.markov_matrix(data, current_date, window)
    stocks = 0
    initialbuy = math.floor(money / data["Close"][1])
    for i in range(1, timespan):
        now = mh.get_categorised(data, current_date)
        if (now > 2):
            new, money = buy(money, data, i)
            stocks += new
        else:
            newmon = sell(stocks, data, i)
            money += newmon
            stocks = 0
        current_date += 1
        plot.append(money + (stocks * data['Close'][i]))
    return (money + (stocks * data['Close'][timespan - 1])) - (initialbuy *data['Close'][timespan - 1])


money = without(money, plot=markov_plot_data)
print("profit made with pure markov: " + str(money))
money = with_fft(money, fft_plot_data, stock_plot_data)
print("profit made with fft: " + str(money))

stock_plot_data.plot()
fft_plot_data.plot()
markov_plot_data.plot()
plt.plot(stock_plot_data, color='r', label='market')
plt.plot(fft_plot_data, color='g', label='with fft')
plt.plot(markov_plot_data, color='b', label='markov')

plt.xlabel("Days Since Start") 
plt.ylabel("Total Money") 
plt.title("Market vs FFT/Markov vs Markov")
plt.legend() 
plt.show() 