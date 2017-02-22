#!/usr/bin/python

import requests

from . import memoize

def is_valid_ticker(ticker_s):
    return dumb_valid_ticker(ticker_s) and valid_ticker(ticker_s)

def dumb_valid_ticker(ticker):
    return len(ticker) < 10 and len(ticker.split()) <= 4

@memoize
def valid_ticker(ticker):
    """ Reaches to reuters to validate a ticker symbol. 
        Cached to save bandwith/time. Possibly error prone """ #TODO testing
    sym = "symbol=" + ticker
    url_base = "http://www.reuters.com/finance/stocks/overview?" + sym
    return requests.get(url_base).url.endswith(sym)

