#!/usr/bin/python

from stockData import get_data_for_sym
from pprint import pprint
from db import StockFeature, database
from datetime import date, timedelta
import peewee
import yahoo_finance

#List of stocks that will be queried
Stocks = ['TGT','UAA','GM']
StartDate = '2017-04-12'
Yesterday = date.today() - timedelta(1)
#EndDate = '2017-04-15'
EndDate = Yesterday.strftime("%Y-%m-%d")
	
# For loop that queries Yahoo Finance and maps output to StockFeature table fields. Inserts mapped fields into StockFeature table
for stock in Stocks:
	try:
		Data = get_data_for_sym(stock,StartDate,EndDate)
		db_data = ({'stock_id': li["Symbol"], 'date': li["Date"], 'high': li["High"], 'low': li["Low"], 'volume': li["Volume"], 'opening': li["Open"], 'closing': li["Close"]} for li in Data)
		
		try:
			with database.atomic():
				StockFeature.insert_many(db_data).execute()
		except peewee.IntegrityError:
			print('Skipping Duplicate')

	except yahoo_finance.YQLResponseMalformedError:
		print "Query error: %s not available for query" % (StartDate)