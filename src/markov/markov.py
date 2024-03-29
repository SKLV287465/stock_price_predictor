import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import sys
import markov_helper as mh

# Markov chain stock return predition program

# inputs:
# 1: symbol
# 2: Window size
# 3: start day, month, year

# Take in CLI arguments
symbol = sys.argv[1]
window = int(sys.argv[2])
start_date = datetime.date(int(sys.argv[5]), int(sys.argv[4]), int(sys.argv[3]))

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
data, timespan = mh.get_data(symbol)

current_date = 1
states = mh.markov_matrix(data, current_date, window)

for i in range(1, timespan):
    previous = mh.get_categorised(data, current_date - 1)
    now = mh.get_categorised(data, current_date)
    stats[mh.get_stat(states, previous, now)] += 1
    
    states = mh.markov_matrix(data, current_date, window) 
    current_date += 1
    
accuracy, precision, recall = mh.statcalc(stats)
print('Accuracy: ' + str(accuracy))
print('Precision: ' + str(precision))
print('Recall: ' + str(recall))
