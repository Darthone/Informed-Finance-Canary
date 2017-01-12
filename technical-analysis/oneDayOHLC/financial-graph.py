import time
import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as mplot
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
# custom matplotlib parameters
matplotlib.rcParams.update({'font.size': 9})

stocks = 'AAPL', 'FB', 'UAA'

def graphData(stock):
	try:
		s = stock + '.txt'

		# load values and format the date
		date, closePrice, highPrice, lowPrice, openPrice, volume = np.loadtxt(s, delimiter=',', unpack=True, converters={0: mdates.strpdate2num('%Y%m%d')})

		f = mplot.figure()
		# on a 4x4 figure, plot at (0,0)
		a = mplot.subplot2grid((5,4), (0,0), rowspan=4, colspan=4)
		
		# plot variables needed
		a.plot(date, openPrice)
		a.plot(date, highPrice)
		a.plot(date, lowPrice)
		a.plot(date, closePrice)
		mplot.ylabel('Stock Price ($)')
		a.grid(True)

		# bar chart for volume
		b = mplot.subplot2grid((5,4), (4,0), sharex=a, rowspan=1, colspan=4)
		b.bar(date, volume)
		# remove y-axis labeling for volume
		b.axes.yaxis.set_ticklabels([])
		mplot.ylabel('Volume')
		b.grid(True)

		# fit 10 dates into graph and formatt properly
		a.xaxis.set_major_locator(mticker.MaxNLocator(10))
		a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

		# rotating angles by 90 degrees to fit properly
		for label in a.xaxis.get_ticklabels():
			label.set_rotation(90)

		for label in b.xaxis.get_ticklabels():
			label.set_rotation(45)

		# subplot profile parameters
		mplot.subplots_adjust(left=.10, bottom=.19, right=.93, top=.95, wspace=.20, hspace=.07)

		# plot profiling
		mplot.xlabel('Date (YYY-MM-DD)')
		# mplot.ylabel('Stock Price ($)')
		mplot.suptitle(stock + ' Stock Price')
		
		# remove x axis from first graph, used at bottom already
		mplot.setp(a.get_xticklabels(), visible=False)

		# adjusting plots in a clean manner
		mplot.subplots_adjust(left=.09, bottom=.18, right=.94, top=.94, wspace=.20, hspace=0)

		mplot.show()

		f.savefig('financial_graph.png')		


	except Exception, e:
		print 'error in main:', str(e)


graphData('AAPL')