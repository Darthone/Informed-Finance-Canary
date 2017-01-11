# urllib2 opens http urls (authentication, redirections, cookies, etc.)
import urllib2
import os
# print timestamp that's recognizable
import time, datetime
import sys

stocks = 'AAPL', 'FB', 'UAA' # AAPL, FB, UAA, JCP, TGT, DIS
stockRange = '1y' # 1y, 10d


def pullData(stock):
	try:
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
		for l in splitSource:
			if 'values' not in l:
				splitLine = l.split(',')
				if len(splitLine) == 6:
					# most recent time? append to file
					if int(splitLine[0]) > int(lastUnix):
						lineToWrite = l + '\n'
						saveFile.write(lineToWrite)

		saveFile.close()

		print 'Pulled', stock
		print str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%S'))

	except Exception, e:
		print 'error in main:', str(e)
    


for stock in stocks:
	pullData(stock)