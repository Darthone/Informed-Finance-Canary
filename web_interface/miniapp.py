#!/usr/bin/env python
from __future__ import division
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import urllib2
import os
import time
import datetime
import sys
from decimal import Decimal
stockRange = '1y'

# app config
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
	tickerName = TextField('Ticker Name:', validators=[validators.required()])
	sma1 = TextField('Simple Moving Average 1 (SMA) (eg 10):', validators=[validators.required()])
	sma2 = TextField('Simple Moving Average 2 (SMA) (eg 30):', validators=[validators.required()])
	dateRange = TextField('Length of Process: ', validators=[validators.required()])
	nslow = TextField('Slow EMA (eg 26): ', validators=[validators.required()])
	nfast = TextField('Fast EMA (eg 12): ', validators=[validators.required()])
	nema = TextField('EMA Signal Line (eg 9): ', validators=[validators.required()])

@app.route("/", methods=['GET', 'POST'])
def hello():
	form = ReusableForm(request.form)

	print form.errors
	if request.method == 'POST':
		tickerName = request.form['tickerName']
		sma1 = request.form['sma1']
		sma2 = request.form['sma2']
		dateRange = request.form['dateRange']
		nslow = request.form['nslow']
		nfast = request.form['nfast']
		nema = request.form['nema']
		print tickerName, sma1, sma2, dateRange, nslow, nfast, nema
		
		if form.validate():
			flash('Ticker Name: ' + tickerName)
			flash('Simple Moving Average 1 (SMA) (eg 10): ' + sma1)
			flash('Simple Moving Average 2 (SMA) (eg 30): ' + sma2)
			flash('Length of Process: ' + dateRange)
			flash('Slow EMA (eg 26): ' + nslow)
			flash('Fast EMA (eg 12): ' + nfast)
			flash('EMA Signal Line (eg 9): ' + nema)
			pullData(tickerName, dateRange)
		else:
			flash('Error: All the form fields are required. ')

	return render_template('index.html', form=form)

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
			existingFile = open(stock + '.txt','r').read()
			splitExisting = existingFile.split('\n')
			mostRecentLine = splitExisting[-2]
			lastUnix = mostRecentLine.split(',')[0]

		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print(exc_type, fname, exc_tb.tb_lineno)
			print('error in inner try:' + str(e))
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
					flash('Date: ' + currentDateObj.strftime('%m %d, %Y'))
					if 'values' not in l:
						splitLine = l.split(',')
						if len(splitLine) == 6:
							# most recent time? append to file
							if int(splitLine[0]) > int(lastUnix):
								lineToWrite = l + '\n'
								saveFile.write(lineToWrite)
					flash('Price: ', price)

					# trading stances:
					# buy when not invested and stock price drops
					# sell when price is > .2% higher than bought
					if stance == 'none':
						if price < pricePrevious:
							flash('buy triggered')
							priceBought = price
							flash('bought stock for ', priceBought)
							stance = 'holding'
							if tradeCount == 0:
								startingPrice = priceBought
							tradeCount += 1
					elif stance == 'holding':
						if price > (priceBought * .002 + priceBought):
							flash('sell triggered')
							priceSold = price
							flash('finished trade, sold for: ', priceSold)
							stance = 'none'
							tradeProfit = priceSold - priceBought
							totalProfit += tradeProfit
							flash(totalProfit)
							tradeCount += 1
					pricePrevious = price

				flash('Gross Profit Per Stock:', totalProfit)
				flash('# of Trades:', tradeCount)
				flash('------------------------------------')				

				try:
					grossPercentProfit = totalProfit/startingPrice * 100
					flash('Gross percent profit:', grossPercentProfit)
				except ZeroDivisionError:
					pass
		except IndexError:
			pass

		saveFile.close()

		flash('Pulled', stock)
		flash(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%S')))

	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print(exc_type, fname, exc_tb.tb_lineno)
		print 'error in main:', str(e)
		flash('error in main:', str(e))


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000)
