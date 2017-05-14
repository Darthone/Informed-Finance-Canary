#!/usr/bin/env python
from common import memoize
#from DateTime import date, timedelta
#from ifc.db import StockFeature, database

import logging
#import peewee
import yahoo_finance

def get_data_for_sym_from_yahoo(ticker_sym, start, end):
    """ returns a list of dicts for stock data formatted as:
            {u'Volume': u'28720000', u'Symbol': u'YHOO', u'Adj_Close': u'35.83', u'High': u'35.89', u'Low': u'34.12', u'Date': u'2014-04-29', u'Close': u'35.83', u'Open': u'34.37'}
        Dates must be in format of YYYY-mm-dd """
    try:
        return yahoo_finance.Share(ticker_sym).get_historical(start, end)
    except yahoo_finance.YQLResponseMalformedError:
        logging.error("Malformed Url")
        return []

#@memoize
def get_data_for_sym(ticker_sym, start, end):
    return list(reversed(get_data_for_sym_from_yahoo(ticker_sym, start, end)))
	#res = StockFeature.select().where(Relationship.from_user == self))

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
