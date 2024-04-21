import yfinance as yf
import datetime


# Gets data from start_date to current date 
def get_data(symbol):
    data = yf.download(symbol, start=(datetime.date.today() -  datetime.timedelta(days=1826)), end=datetime.date.today())
    return data, len(data)

def get_data_start_date(symbol, start_date):
    data = yf.download(symbol, start=start_date, end=datetime.date.today())
    return data, len(data)
    
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
    for i in range(start, start + window):
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
    i = 0
    for n in range(int((end_date - start_date).days)):
        i += 1
    return i
        
# Calculate statistics for Markov algorithm
def statcalc(stats):
    accuracy = (stats[0] + stats[2]) / (stats[0] + stats[1] + stats[2] + stats[3])
    precision = stats[0] / (stats[0] + stats[1])
    recall = stats[0] / (stats[0] + stats[3])
    return accuracy, precision, recall

def get_stat(states, previous, now):
    up = 0
    down = 0
    prediction = 0
    for i in range(3):
        down += states[previous][i]
    for i in range(2, 5):
        up += states[previous][i]
    if up > down:
        prediction = 1
    else:
        prediction = 0
    # previous is index, now is up or down
    if now < 3 and prediction == 0:
        return 2
    elif now > 2 and prediction == 1:
        return 0
    elif now < 3 and prediction == 1:
        return 1
    elif now > 2 and prediction == 0:
        return 3
    return 0