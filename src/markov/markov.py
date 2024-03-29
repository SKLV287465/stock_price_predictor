import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import sys
import markov_helper as mh

# Markov chain stock return predition program

# inputs:
# 1: symbol
# 2: Window size
# 3: start date

# Take in CLI arguments
symbol = sys.argv[1]
window = sys.argv[2]
start_date = datetime.date(sys.argv[3])

    # ***DEPRECATED***
    # Initialise markov matrix 
    # states = [[0] * 6] * 6

#Intialise stats array
stats = [0] * 4
# 0: true positive
# 1: false positive
# 2: true negative
# 3: false negative
# Fetch data
data = mh.get_data(symbol)
start_index = mh.daterange(datetime.date.today() - datetime.timedelta(years=5), start_date)

states = mh.markov_matrix(data, start_index - 1, window)
for i in range(mh.daterange(start_date, datetime.date.today())):
    previous = mh.get_categorised(data, current_date - 1)
    now = mh.get_categorised(data, current_date)
    stats[mh.get_stat(states, previous, now)] += 1
    
    states = mh.markov_matrix(data, current_date, window) 
    current_date = start_index + i
    
accuracy, precision, recall = mh.statcalc(stats)
print('Accuracy: ' + accuracy)
print('Accuracy: ' + precision)
print('Accuracy: ' + recall)
