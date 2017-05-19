#!/usr/bin/env python
from datetime import datetime
#from ifc.db import StockFeature, database

import logging
import io
import requests
import pandas as pd

from ifc.common import memoize

def get_data_from_google(ticker_sym, start, end):
    """ Returns a data frame of data for a given stock between two dates """
    url = "https://www.google.com/finance/historical?q=%s&startdate=%s&enddate=%s&output=csv" % (ticker_sym, start, end)
    s = requests.get(url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    df['Date'] = pd.to_datetime(df['Date'])
    df['epoch'] = (df['Date'] - datetime(1970,1,1)).dt.total_seconds() * 1000
    df.set_index('Date')
    df['Adj_Close'] = df['Close'] # google's api doens't provide so just assume it's the same
    cols = ['High', 'Low', 'Volume', 'Open', 'Close', 'Adj_Close']
    for c in cols: # cast columns to numeric
        df[c] = pd.to_numeric(df[c])
    return df.iloc[::-1] # reverse the dataframe so index 0 is the earliest date

#@memoize
#def get_data_for_sym(ticker_sym, start, end):
#    return list(reversed(get_data_for_sym_from_yahoo(ticker_sym, start, end)))
#	#res = StockFeature.select().where(Relationship.from_user == self))

"""
def fill_db_with_data(ticker_sym, days_back=3650):
    start = date.today()
    end = date.today() - timedelta(days_back)
    EndDate = Yesterday.strftime("%Y-%m-%d")
	data = get_data_for_sym(ticker_sym, star.tstrftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
	db_data = ({'stock_id': li["Symbol"], 'date': li["Date"], 'high': li["High"], 'low': li["Low"], 'volume': li["Volume"], 'opening': li["Open"], 'closing': li["Close"]} for li in data)
	try:
		with database.atomic():1
			StockFeature.insert_many(db_data).execute()
 	except peewee.IntegrityError:
		logging.info('Skipping Duplicate')
        """
