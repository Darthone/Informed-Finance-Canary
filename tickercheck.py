#!/usr/bin/python

# Validates if a ticker is ETF (Exchange Traded Fund)
# this is a change

import urllib2

def request(symbol, tag):
	url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol, tag)
	response = urllib2.urlopen(url)
	content = response.read().decode().strip().strip('"')
	return content

def get_name(symbol):
  return request(symbol, 'n')

def valid_ticker(ticker):
	ticker = ticker.upper()
	print get_name(ticker)
	return True if get_name(ticker) != 'N/A' else False

print valid_ticker('UA')
