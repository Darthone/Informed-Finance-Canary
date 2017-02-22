#!/usr/bin/env python
from yahoo_finance import Share

def get_data_for_sym(ticker_sym, start, end):
    #TODO Error catching
    """ returns a list of dicts for stock data formatted as:
            {u'Volume': u'28720000', u'Symbol': u'YHOO', u'Adj_Close': u'35.83', u'High': u'35.89', u'Low': u'34.12', u'Date': u'2014-04-29', u'Close': u'35.83', u'Open': u'34.37'}
        Dates must be in format of YYYY-mm-dd """

    #TODO check if db has data
    # if not grab data and put it into the DB
    symbol = Share(ticker_sym)
    return symbol.get_historical(start, end)


