#!/usr/bin/env python
from __future__ import division
# urllib2 opens http urls (authentication, redirections, cookies, etc.)
import urllib2
import os
# print timestamp that's recognizable
import datetime
import time
import sys
stocks = 'AAPL', 'FB', 'UAA' # AAPL, FB, UAA, JCP, TGT, DIS
stockRange = '1y' # 1y, 10d


def pullData(stock, stockRange):
	# none or hold for stance
	stance = 'none'
	priceBought = 0
	priceSold = 0
	pricePrevious = 0
	totalProfit = 0
	tradeCount = 0
	startingPrice = 0

	try:
		# values format -> date, close, high, low, open, volume
		urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=' + stockRange + '/csv'
		f = stock + '.txt'

		try:
			# if the file exists, open file and grab latest unix timestamp
			existingFile = open(f,'r').read()
			splitExisting = existingFile.split('\n')
			mostRecentLine = splitExisting[-2]
			lastUnix = mostRecentLine.split(',')[0]

		except Exception,e:
			print 'error in inner try:', str (e)
			lastUnix = 0

		# append new lines from site to existing file
		saveFile = open(f, 'a')
		openedSite = urllib2.urlopen(urlToVisit).read()
		splitSource = openedSite.split('\n')

		# grab valid lines after values section
		try:
			for l in splitSource:
				if l[0].isdigit():
					l_split = l.split(',')
					price =  float(l_split[1])
					currentDate = str(l_split[0])
					currentDateObj = datetime.datetime.strptime(currentDate, '%Y%m%d')
					print('Date: ' + currentDateObj.strftime('%m %d, %Y'))
					if 'values' not in l:
						splitLine = l.split(',')
						if len(splitLine) == 6:
							# most recent time? append to file
							if int(splitLine[0]) > int(lastUnix):
								lineToWrite = l + '\n'
								saveFile.write(lineToWrite)
					print 'Price: ', price

					# trading stances:
					# buy when not invested and stock price drops
					# sell when price is > .2% higher than bought
					if stance == 'none':
						if price < pricePrevious:
							print 'buy triggered'
							priceBought = price
							print 'bought stock for ', priceBought
							stance = 'holding'
							if tradeCount == 0:
								startingPrice = priceBought
							tradeCount += 1
					elif stance == 'holding':
						if price > (priceBought * .002 + priceBought):
							print 'sell triggered'
							priceSold = price
							print 'finished trade, sold for: ', priceSold
							stance = 'none'
							tradeProfit = priceSold - priceBought
							totalProfit += tradeProfit
							print totalProfit
							tradeCount += 1
					pricePrevious = price

				print 'Gross Profit Per Stock:', totalProfit
				print '# of Trades:', tradeCount
				print '------------------------------------'				

				try:
					grossPercentProfit = totalProfit/startingPrice * 100
					print 'Gross percent profit:', grossPercentProfit
				except ZeroDivisionError:
					pass
		except IndexError:
			pass

		saveFile.close()

		print 'Pulled', stock
		print str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%S'))

	except Exception, e:
		print 'error in main:', str(e)


stockToUse = raw_input('Stock to trade: ')
if not stockToUse:
	print "Please enter a valid stock ticker"
else:
	stockRange = raw_input('Enter period of trading: ')
	if not stockRange:
		print "Please enter a valid range for trading"
	else:
		pullData(stockToUse, stockRange)
