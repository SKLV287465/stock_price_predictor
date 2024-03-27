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
    

    # states = {
    #     "D1" : [0, 0, 0, 0, 0, 0],
    #     "D2" : [0, 0, 0, 0, 0, 0],
    #     "D3" : [0, 0, 0, 0, 0, 0],
    #     "U1" : [0, 0, 0, 0, 0, 0],
    #     "U2" : [0, 0, 0, 0, 0, 0],
    #     "U3" : [0, 0, 0, 0, 0, 0]
    # }
    
    # State matrix (divide all of the indexes by window size).
    states = [[0] * 6] * 6
    
    i = 0
    for delta in range((end_date - start_date).days + 1):
        result_date = start_date + datetime.timedelta(days=delta)
        day_change = ((data['Close'][i]- data['Open'][i]) * 100 / data['Open'][i])
        if i == 0:
            
        if (day_change >= 0):
            if (day_change < 0.5):
                
            elif (day_change < 1):
            else:
        else:
            if (day_change > -0.5):
            elif (day_change > -1):
            else:
            
            
        i += 1
    
    # data['% change'].plot()
    # plt.title(symbol + " Stock Prices")
    # plt.show()
main()