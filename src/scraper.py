import yfinance as yf
import datetime
import math

class Model:
    def __init__(self, data, start, end):
        self.data = data
        self.start = start
        self.end = end
    def get_day_num(self, day):
        return (day - self.start).days

def get_all_data(symbol):
    ticker = yf.Ticker(symbol)
    return ticker.history(period='max')

def get_data(symbol, start, end):
    return yf.download(symbol, start=start, end=end)

def get_last(symbol, days):
    return yf.download(symbol, start=datetime.date.today() - datetime.timedelta(days=days), end=datetime.date.today())
def test_extrapolation(symbol, start, end, num_days):
    if (start > end - datetime.timedelta(num_days)):
        return 0;
    else:
        completeData = yf.download(symbol, start=start, end=end)
        reducedData = yf.download(symbol, start=start, end=end - datetime.timedelta(days=num_days))
        return reducedData, completeData

def test_extrapolationToday(symbol, num_days, num_days_ex):
    return test_extrapolation(symbol,datetime.date.today() - datetime.timedelta(days=num_days), datetime.date.today(), num_days_ex)
