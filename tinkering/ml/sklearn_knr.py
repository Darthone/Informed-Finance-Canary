#!/usr/bin/env python
import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, neighbors, svm, metrics
import peewee
from peewee import *
import ifc.ta as ta
import math

def addDailyReturn(dataset):
	"""
	Adding in daily return to create binary classifiers (Up or Down in relation to the previous day)
	"""

	#will normalize labels
	le = preprocessing.LabelEncoder()

	print "dataset['Adj_Close']\n", dataset['Adj_Close'][:5]
	
	print "dataset['Adj_Close'].shift(-1)\n", dataset['Adj_Close'].shift(1)[:5]

	dataset['UpDown'] = (dataset['Adj_Close']-dataset['Adj_Close'].shift(1))/dataset['Adj_Close'].shift(1)
	print dataset['UpDown'][240:]

	# will be denoted by 3 when transformed
	dataset.UpDown[dataset.UpDown > 0] = "sell"

	dataset.UpDown[dataset.UpDown == 0] = "hold"

	dataset.UpDown[dataset.UpDown < 0] = "buy"
	#print dataset['UpDown'][:10]
	dataset.UpDown = le.fit(dataset.UpDown).transform(dataset.UpDown)

	#print dataset['UpDown']

variances = []

def preProcessing(stock_name, start_date, end_date):
	"""
	Clean up data to allow for classifiers to predict
	"""
	x = ta.get_series(stock_name, start_date, end_date)
	x.run_calculations()                            
	x.trim_fat()                                    
	df = x.df
	#df = pd.read_csv(csv)
	addDailyReturn(df)
	
	#The columns left will be the ones that are being used to predict
	df.drop(['Date'], 1, inplace=True)
	df.drop(['Low'], 1, inplace=True)
	df.drop(['Volume'], 1, inplace=True)
	#df.drop(['Open'], 1, inplace=True)
	#df.drop(['Adj_Close'],1, inplace=True)
	df.drop(['Close'],1, inplace=True)
	df.drop(['High'],1, inplace=True)
	df.drop(['mavg_10'],1, inplace=True)
	df.drop(['mavg_30'],1, inplace=True)
	df.drop(['rsi_14'],1, inplace=True)
	
	return df

def trade(array):
	"""
	Once the algo has made its predictions we want to be able to trade
	"""	
	#converting array to list to compare algo indicator
	trade_list = array.tolist()
	stance = 'none'
	price_bought = 0
	price_sold = 0
	price_previous = 0
	total_profit = 0
	trade_count = 0
	starting_price = 0
 	
	try:
		for i in trade_list:
			current_price = i[0]
			current_updown = i[1]
			if stance == 'none':
				if current_updown < 1.5: #buy stock condition
					#check first if we have enough money
					print 'buy triggered'
					price_bought = current_price
					print 'bought stock for: ', price_bought
					stance = 'holding'
					if trade_count == 0:
						starting_price = price_bought
					trade_count += 1
			elif stance == 'holding':
				if current_updown > 2.5: #sell stock condition
					print 'sell triggered'
					price_sold = current_price
					print 'finished trade, sold for: ', price_sold
					stance = 'none'
					trade_profit = price_sold - price_bought
					total_profit += trade_profit
					print total_profit
					trade_count += 1
			price_previous = current_price

			print 'Gross Profit Per Stock: ', total_profit
			print '# of Trades: ', trade_count
			print'----------------------------------------'

			try:
				gross_percent_profit = (total_profit/starting_price) *100
				print 'Gross percent profit: ', gross_percent_profit
			except ZeroDivisionError:
				pass
	except IndexError:
		pass

for i in range(1):
	#calling in date ranges plus stock name to be pulled
	ticker = raw_input('Enter a stock ticker then press "Enter":\n')	

	train_df = preProcessing(ticker, "2015-04-17", "2016-04-17")
	test_df = preProcessing(ticker, "2016-04-17", "2017-04-17")

	print test_df[:5]	

	# separating the binary predictor into different arryays so the algo knows what to predict on
	X_train = np.array(train_df.drop(['UpDown'],1))
	y_train = np.array(train_df['UpDown'])
	X_test = np.array(test_df.drop(['UpDown'],1))
	y_test = np.array(test_df['UpDown'])

	trade_array = np.array(train_df.drop(['Open'],1))
	print '\nLSKJDF:L\n'
	print trade_array
	trade(trade_array)
	
	# performing the algorithm 
	clf = neighbors.KNeighborsRegressor()
	clf.fit(X_train,y_train)

	y_pred = clf.predict(X_test)
	print "\nSTART\n"
	print y_pred
	variance = abs(metrics.explained_variance_score(y_test, y_pred))

	# iterate and print average accuracy rate
	print "Variance:\n" + str(variance)
	variances.append(variance)	

	# test value
	test_set = np.array([[31,38],[100,101],[7,7],[34,31]])

	prediction = clf.predict(test_set)

	print prediction

#print sum(accuracies)/len(accuracies)
