#!/usr/bin/env python
import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, neighbors, svm 
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

accuracies = []

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

	print test_df[:240]

		
	#X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.5)

	# performing the algorithm 
	clf = svm.SVR()
	clf.fit(X_train,y_train)

	accuracy = clf.score(X_test,y_test)

	# iterate and print average accuracy rate
	print accuracy
	accuracies.append(accuracy)	

	# test value
	test_set = np.array([[39,38],[100,101]])

	prediction = clf.predict(test_set)

	print prediction

#print sum(accuracies)/len(accuracies)
