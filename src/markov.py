import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import sys

def main():
    symbol = sys.argv[1]
    print(symbol)
    date = str(datetime.date.today())
    end_date = datetime.date.today()
    year, month, day = date.split('-')
    year = str(int(year) - 5)
    start_date = datetime.date(int(year), int(month), int(day))
    data = yf.download(symbol, start=start_date, end=date)
    
    day_change = []
    states = {
        "D1" : 0,
        "D2" : 0,
        "D3" : 0,
        "U1" : 0,
        "U2": 0,
        "U3" : 0
    }
    
    i = 0
    for delta in range((end_date - start_date).days + 1):
        result_date = start_date + datetime.timedelta(days=delta)
        day_change.append = (data['Close'][i]- data['Open'][i]) / data['Open'][i]
        i += 1
    
    # data['% change'].plot()
    # plt.title(symbol + " Stock Prices")
    # plt.show()
main()