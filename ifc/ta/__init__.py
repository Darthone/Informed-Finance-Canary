import bisect
from datetime import datetime

def dicts_to_series(list_of_dicts):
    """ convert data from yahoo finance """
    ret = []
    for day in list_of_dicts:
        ret.append(Day(day['Open'], day['High'], day['Low'], day['Close'], day['Adj_Close'],
                   datetime.strptime(day['Date'], "%Y-%m-%d"), day['Volume']))
    return Series(series=ret)

def db_to_series(symbol, start, end, db_con):
    """ read data from database """
    #TODO
    pass

class Day(object):
    """ used to store stock information by the day """
    def __init__(self, open, high, low, close, adj_close, date, volume):
        self.open = open
        self.high = high
        self.low = low
        self.volume = volume
        self.adj_close = adj_close
        self.close = close
        self.date = date

    def set_val(self, attr, value):
        """ used to set attribute values after the object has be initialized """
        setattr(self, attr, value)

    def __lt__(self, other):
        """ used to sort """
        return self.date < other.date

    def vectorize(self, features=None):
        """ return a vector of numbers to be used for machine learning """
        #TODO
        pass


class Series(object):
    """ used to represent a series of days """
    def __init__(self, series=None, config=None):
        self.series = []
        if self.series is not None:
            self.series.extend(series)
        self.sort()
        self.index = 0

    def insert(self, day):
        bisect.insort_left(self.series, day)

    def sort(self):
        self.series.sort()

    def run_calculations(self):
        self.calculate_mavg()

    def calculate_mavg(self):
        #TODO
        pass

    #TODO other calculations and signals

    def __iter__(self):
        """ allows for easy iteration ex: for day in series_obj: """
        for day in self.series:
            yield day

