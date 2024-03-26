import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import sys

def main():
    symbol = sys.argv[1]
    print(symbol)
    date = str(datetime.date.today())
    year, month, day = date.split('-')
    year = str(int(year) - 5)
    data = yf.download(symbol, start=year + '-' + month + '-' + day, end=date)
    data['Close'].plot()
    plt.title(symbol + " Stock Prices")
    plt.show()
    
main()