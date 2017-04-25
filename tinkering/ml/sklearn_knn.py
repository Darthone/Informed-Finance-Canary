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

	dataset['UpDown'] = -(dataset['Adj_Close']-dataset['Adj_Close'].shift(-1))/dataset['Adj_Close'].shift(-1)
	#print dataset['UpDown']
	dataset.UpDown[dataset.UpDown >= 0] = 'Up' 
	dataset.UpDown[dataset.UpDown < 0] = 'Down'
	dataset.UpDown = le.fit(dataset.UpDown).transform(dataset.UpDown)
	#print dataset['UpDown']

accuracies = []

def preProcessing(start_date, end_date):
	x = ta.get_series("TGT", start_date, end_date)
	x.run_calculations()                            
	x.trim_fat()                                    
	df = x.df
	#df = pd.read_csv(csv)
	addDailyReturn(df)
	
	df.drop(['Date'], 1, inplace=True)
	df.drop(['Low'], 1, inplace=True)
	df.drop(['Volume'], 1, inplace=True)
	#df.drop(['open'], 1, inplace=True)
	df.drop(['Adj_Close'],1, inplace=True)
	#df.drop(['close'],1, inplace=True)
	df.drop(['High'],1, inplace=True)
	df.drop(['mavg_10'],1, inplace=True)
	df.drop(['mavg_30'],1, inplace=True)
	df.drop(['rsi_14'],1, inplace=True)
	
	return df

for i in range(3):
	train_df = preProcessing("2015-04-17", "2016-04-17")
	test_df = preProcessing("2016-04-17", "2017-04-17")

	X_train = np.array(train_df.drop(['UpDown'],1))
	y_train = np.array(train_df['UpDown'])
	X_test = np.array(test_df.drop(['UpDown'],1))
	y_test = np.array(test_df['UpDown'])
	
	#X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.5)

	clf = neighbors.KNeighborsClassifier() 
	clf.fit(X_train,y_train)

	accuracy = clf.score(X_test,y_test)

	print accuracy
	accuracies.append(accuracy)	

	test_set = np.array([[104,106]])

	prediction = clf.predict(test_set)

	print prediction

print sum(accuracies)/len(accuracies)
