#!/usr/bin/env python
import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, neighbors, svm 
import peewee
from peewee import *
import ifc.ta as ta

def addDailyReturn(dataset):
	"""
	Adding in daily return to create binary classifiers (Up or Down in relation to the previous day)
	"""

	#will normalize labels
	le = preprocessing.LabelEncoder()

	dataset['UpDown'] = (-(dataset['Adj_Close']-dataset['Adj_Close'].shift(-1))/dataset['Adj_Close'].shift(-1))
	#dataset['UpDown'] = '%.4f'%(daily_return)
	print dataset['UpDown'][:5]
	dataset.UpDown = le.fit(dataset.UpDown).transform(dataset.UpDown)
	print dataset['UpDown'][:5]

accuracies = []

def preProcessing(stock_name, start_date, end_date):
	"""
	Clean up data to allow for classifiers to prict
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
	df.drop(['Adj_Close'],1, inplace=True)
	#df.drop(['Close'],1, inplace=True)
	df.drop(['High'],1, inplace=True)
	df.drop(['mavg_10'],1, inplace=True)
	df.drop(['mavg_30'],1, inplace=True)
	df.drop(['rsi_14'],1, inplace=True)
	
	return df

for i in range(3):
	#calling in date ranges plus stock name to be pulled
	train_df = preProcessing("TGT", "2015-04-17", "2016-04-17")
	test_df = preProcessing("TGT", "2016-04-17", "2017-04-17")

	# separating the binary predictor into different arryays so the algo knows what to predict on
	X_train = np.array(train_df.drop(['UpDown'],1))
	y_train = np.array(train_df['UpDown'])
	X_test = np.array(test_df.drop(['UpDown'],1))
	y_test = np.array(test_df['UpDown'])
	
	#X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.5)

	# performing the classifier
	clf = neighbors.KNeighborsRegressor() 
	clf.fit(X_train,y_train)

	accuracy = clf.score(X_test,y_test)

	# iterate and print average accuracy rate
	print accuracy
	accuracies.append(accuracy)	

	# test value
	test_set = np.array([[104,106]])

	prediction = clf.predict(test_set)

	print prediction

print sum(accuracies)/len(accuracies)
