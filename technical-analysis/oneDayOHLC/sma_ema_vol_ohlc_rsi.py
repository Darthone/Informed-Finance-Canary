#!/usr/bin/env python
import matplotlib
# matplotlib.use('Agg')
import time
import datetime
import numpy as np
import matplotlib.pyplot as mplot
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ochl
# custom matplotlib parameters
matplotlib.rcParams.update({'font.size': 9})
import urllib2

stocks = 'AAPL', 'FB', 'UAA'

'''
compute the n period relative strength indicator
n=14 (periods) as a default developed by J. Welles Wilder
momentum oscillator that measures the speed and change of price movements
'''
def rsiFunction(prices, n=14):
	deltas = np.diff(prices)
	seed = deltas[:n+1]
	up = seed[seed >= 0].sum()/n
	down = -seed[seed < 0].sum()/n
	rs = up/down
	rsi = np.zeros_like(prices)
	rsi[:n] = 100. - 100./(1. + rs)

	for i in range(n, len(prices)):
		delta = deltas[i-1] # diff is 1 shorter

		if delta > 0:
			upval = delta
			downval = 0.
		else:
			upval = 0.
			downval = -delta

		up = (up * (n - 1) + upval)/n
		down = (down * (n - 1) + downval)/n

		rs = up/down
		rsi[i] = 100. - 100./(1. + rs)

	return rsi

def movingaverage(values, window):
	weights = np.repeat(1.0, window) / window
	# line smoothening
	smas = np.convolve(values, weights, 'valid')
	# list of values being returned as numpy array
	return smas

def ema(values, window):
	weights = np.exp(np.linspace(-1., 0., window))
	weights /= weights.sum()
	a = np.convolve(values, weights, mode='full')[:len(values)]
	a[:window] = a[window]
	return a

'''
macd line = 12ema - 26ema
signal line = 9ema of the macd line
histogram = macd line - signal line
12 - two trading weeks
26 - one trading month
9 - one and half trading week
http://www.forexabode.com/forex-school/technical-indicators/macd/
5-day trading week -> 10,22,7 or 10,22,8
'''
def computeMACD(x, slow=26, fast=12):
    slow = nslow
    fast= nfast
    emaslow = ema(x, slow)
    emafast= ema(x, fast)
    return emaslow, emafast, emafast-emaslow

def graphData(stock, MA1, MA2, dateRange):
	try:
		try:
			print 'pulling data on', stock
			urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=' + dateRange + '/csv'
			stockFile = []
			try:
				sourceCode = urllib2.urlopen(urlToVisit).read()
				splitSource = sourceCode.split('\n')
				for eachLine in splitSource:
					splitLine = eachLine.split(',')
					if len(splitLine) == 6:
						if 'values' not in eachLine:
							stockFile.append(eachLine)

			except Exception, e:
				print str(e), 'error in organization of pulled data'

		except Exception, e:
			print str(e), 'error in pulling price data'

		# load values and format the date
		date, closePrice, highPrice, lowPrice, openPrice, volume = np.loadtxt(stockFile, delimiter=',', unpack=True, converters={0: mdates.strpdate2num('%Y%m%d')})

		# add dates to data for candlestick to be plotted
		i = 0
		k = len(date)
		candles = []
		while i < k:
			newLine = date[i], openPrice[i], closePrice[i], highPrice[i], lowPrice[i], volume[i]
			candles.append(newLine)
			i = i + 1


		av1 = movingaverage(closePrice, MA1)
		av2 = movingaverage(closePrice, MA2)

		# starting point, plot exactly same amount of data
		SP = len(date[MA2-1:])

		label_1 = str(MA1) + ' SMA'
		label_2 = str(MA2) + ' SMA'

		f = mplot.figure()

		# on a 4x4 figure, plot at (0,0)
		a = mplot.subplot2grid((6,4), (1,0), rowspan=4, colspan=4)
		# using matplotlib's candlestick charting
		candlestick_ochl(a, candles[-SP:], width=0.5, colorup='g', colordown='r')
		# moving average applied to data
		a.plot(date[-SP:], av1[-SP:], label=label_1, linewidth=1.5)
		a.plot(date[-SP:], av2[-SP:], label=label_2, linewidth=1.5)
		mplot.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
		mplot.ylabel('Stock Price ($) and Volume')
		mplot.legend(loc=9, ncol=2, prop={'size':7}, fancybox=True)
		a.grid(True)


		minVolume = 0

		# rsi
		rsiCol = '#1a8782'
		posCol = '#386d13'
		negCol = '#8f2020'
		c = mplot.subplot2grid((6,4), (0,0), sharex=a, rowspan=1, colspan=4)
		rsi = rsiFunction(closePrice)
		c.plot(date[-SP:], rsi[-SP:], rsiCol, linewidth=1.5)
		c.axhline(70, color=negCol)
		c.axhline(30, color=posCol)
		c.fill_between(date[-SP:], rsi[-SP:], 70, where=(rsi[-SP:]>=70), facecolor=negCol, edgecolor=negCol)
		c.fill_between(date[-SP:], rsi[-SP:], 30, where=(rsi[-SP:]<=30), facecolor=posCol, edgecolor=posCol)
		# 70 --> red, overbought
		# 30 --> green, oversold
		c.text(0.015, 0.95, 'RSI (14)', va='top', transform=c.transAxes)
		c.tick_params(axis='x')
		c.tick_params(axis='y')
		c.set_yticks([30,70])
		# mplot.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='lower'))

		# fit 10 dates into graph and formatt properly
		a.xaxis.set_major_locator(mticker.MaxNLocator(10))
		a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

		avol = a.twinx()
		avol.fill_between(date[-SP:], minVolume, volume[-SP:], facecolor='b', alpha=.5)
		avol.axes.yaxis.set_ticklabels([])
		avol.grid(False)
		avol.set_ylim(0,2*volume.max())
		avol.tick_params(axis='x')
		avol.tick_params(axis='y')

		# macd
		d = mplot.subplot2grid((6,4), (5,0), sharex=a, rowspan=1, colspan=4)
		d.tick_params(axis='x')
		d.tick_params(axis='y')
		# nslow = 26
		# nfast = 12
		# nema = 9

		emaslow, emafast, macd = computeMACD(closePrice)
		ema9 = ema(macd, nema)

		d.plot(date[-SP:], macd[-SP:])
		d.plot(date[-SP:], ema9[-SP:])
		d.fill_between(date[-SP:], macd[-SP:]-ema9[-SP:], 0, alpha=0.5)
		d.text(0.015, 0.95, 'MACD ' + str(nfast) + ' ' + str(nslow) + ' ' + str(nema), va='top', transform=d.transAxes)
		d.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))

		# rotating angles by 90 degrees to fit properly
		for label in d.xaxis.get_ticklabels():
			label.set_rotation(45)

		# subplot profile parameters
		mplot.subplots_adjust(left=.10, bottom=.19, right=.93, top=.95, wspace=.20, hspace=.07)
		# plot profiling
		mplot.xlabel('Date (YYYY-MM-DD)')
		# mplot.ylabel('Stock Price ($)')
		mplot.suptitle(stock + ' Stock Price')
		# remove x axis from first graph, used at bottom already
		mplot.setp(c.get_xticklabels(), visible=False)
		mplot.setp(a.get_xticklabels(), visible=False)
		# adjusting plots in a clean manner
		mplot.subplots_adjust(left=.09, bottom=.18, right=.94, top=.94, wspace=.20, hspace=0)
		mplot.show()


		f.savefig('financial_graph.png')


	except Exception, e:
		print 'error in main:', str(e)

stockToUse = raw_input('Stock to chart: ')
# Simple Moving Averages (SMA) - 10, 30
sma1 = raw_input('SMA 1: ') or "10"
sma2 = raw_input('SMA 2: ') or "30"
# date range - 1y for 1 year, 10d for 10 days
dateRange = raw_input('Length of Process: ') or "1y"
# EMA Vars
nslow = raw_input('Slow EMA: ') or "26"
nfast = raw_input('Fast EMA: ') or "12"
nema = raw_input('EMA Signal: ') or "9"
nslow = int(nslow)
nfast = int(nfast)
nema = int(nema)
graphData(stockToUse, int(sma1), int(sma2), dateRange)
