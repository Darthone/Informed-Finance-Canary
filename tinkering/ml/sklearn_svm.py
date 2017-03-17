import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, neighbors, svm 

def addDailyReturn(dataset):
	"""
	Adding in daily return to create binary classifiers (Up or Down in relation to the previous day)
	"""

	#will normalize labels
	le = preprocessing.LabelEncoder()

	dataset['UpDown'] = -(dataset['adj_close']-dataset['adj_close'].shift(-1))/dataset['adj_close'].shift(-1)
	print dataset['UpDown']
	dataset.UpDown[dataset.UpDown >= 0] = 'Up' 
	dataset.UpDown[dataset.UpDown < 0] = 'Down'
	dataset.UpDown = le.fit(dataset.UpDown).transform(dataset.UpDown)
	#print dataset['UpDown']
"""
	features = dataset.columns[1:-1]
	X = dataset[features]    
	y = dataset.UpDown    

	X_train = X[X.index < start_test]
	y_train = y[y.index < start_test]              

	X_test = X[X.index >= start_test]    
	y_test = y[y.index >= start_test]

	return X_train, y_train, X_test, y_test   
"""
accuracies = []

def preProcessing(csv):
	df = pd.read_csv(csv)
	addDailyReturn(df)
	
	df.drop(['date'], 1, inplace=True)
	df.drop(['low'], 1, inplace=True)
	df.drop(['volume'], 1, inplace=True)
	#df.drop(['open'], 1, inplace=True)
	df.drop(['adj_close'],1, inplace=True)
	#df.drop(['close'],1, inplace=True)
	df.drop(['high'],1, inplace=True)
	
	return df

for i in range(100):
	train_df = preProcessing('GM_14_15.csv')
	test_df = preProcessing('GM_16_17.csv')

	X_train = np.array(train_df.drop(['UpDown'],1))
	y_train = np.array(train_df['UpDown'])
	X_test = np.array(test_df.drop(['UpDown'],1))
	y_test = np.array(test_df['UpDown'])
	
	#X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.5)

	clf = svm.SVC() 
	clf.fit(X_train,y_train)

	accuracy = clf.score(X_test,y_test)

	print accuracy
	accuracies.append(accuracy)	

	test_set = np.array([[104,106]])

	prediction = clf.predict(test_set)

	print prediction

print sum(accuracies)/len(accuracies)
