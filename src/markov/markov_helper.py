import yfinance as yf
import datetime
import math


# Gets data from start_date to current date 
def get_data(symbol):
    return yf.download(symbol, start=datetime.date.today() -  datetime.timedelta(years=5), end=datetime.date.today())

# Categorises the stock prices 
def categorise(x):
    x *= 100
    if x >= 0:
        if x < 0.5:
            return 3
        elif x <= 1:
            return 4
        else:
            return 5
    else:
        if x > -0.5:
            return 0
        elif x >= -1:
            return 1
        else:
            return 2

def get_categorised(data, index):
    return categorise((data['Close'][index] - data['Open'][index]) / data['Open'][index])

# Create the markov matrix
# Problem 1: markov matrix needs to be counting down not up
def markov_matrix(data, current, window):
    start = current - window
    states = [[0] * 6] * 6
    previous_day = get_categorised(data, start - 1)
    for j in range(start, window):
        day_change = get_categorised(data, i)
        states[previous_day][day_change] += 1
        previous_day = day_change
        i += 1
    for x in range(6):
        for y in range(6):
            states[x][y] /= window
    return states

# Find difference in date from start to end date
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
        
# Calculate statistics for Markov algorithm
def statcalc(stats):
    accuracy = (stats[0] + stats[2]) / (stats(0) + stats[1] + stats[2] + stats[3])
    precision = stats[0] / (stats[0] + stats[1])
    recall = stats[0] / (stats[0] + stats[3])
    return accuracy, precision, recall

def get_stat(states, previous, now):
    max = max(max(x) for x in states[previous])
    theoretical_now = 0
    for i in range(6):
        if max == states[previous][i]:
            theoretical_now = i
    # previous is index, now is up or down
    if now < 3 & theoretical_now < 3:
        return 2
    elif now > 2 & theoretical_now > 2:
        return 0
    elif now < 3 & theoretical_now > 2:
        return 1
    elif now > 2 & theoretical_now < 3:
        return 3