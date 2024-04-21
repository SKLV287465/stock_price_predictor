# CLI arguments: SYMBOL DAY MONTH YEAR
# the arguments are for the start, program runs until present day
import markov.markov_helper as mh;
# import arima;
# import fft;
import datetime;
import sys
import math

def sell(stocks, data, index):
    return float(data['Close'][index]) * stocks

def buy(money, data, index):
    bought_stocks = math.floor(money / data['Close'][index])
    leftover = money - (bought_stocks * data['Close'][index])
    return int(bought_stocks), float(leftover)

def with_fft():
    return
def without():
    return

def markov(symbol, date, money):
    symbol = sys.argv[1]
    window = int(sys.argv[2])
    start_date = datetime.date(int(sys.argv[5]), int(sys.argv[4]), int(sys.argv[3]))

        # ***DEPRECATED***
        # Initialise markov matrix 
        # states = [[0] * 6] * 6

    #Intialise stats array
    #stats = [0] * 4
    # 0: true positive
    # 1: false positive
    # 2: true negative
    # 3: false negative
    # Fetch data
    data, timespan = mh.get_data(symbol)

    current_date = 1
    states = mh.markov_matrix(data, current_date, window)
    stocks = 0
    initialbuy = math.floor(money / data["Close"][1])
    print(str(initialbuy))
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
    return (money + (stocks * data['Close'][timespan - 1])) - (initialbuy *data['Close'][timespan - 1] )

money = markov('MSFT', datetime.date(2020, 1, 1), 5000)
print("profit made with pure markov: " + str(money))