import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, neighbors 

def addDailyReturn(dataset):
	"""
	Adding in daily return to create binary classifiers (Up or Down in relation to the previous day)
	"""

	#will normalize labels
	le = preprocessing.LabelEncoder()

	dataset['UpDown'] = (dataset['close']-dataset['close'].shift(-1))/dataset['close'].shift(-1)
	dataset.UpDown[dataset.UpDown >= 0] = 'Up'
	dataset.UpDown[dataset.UpDown < 0] = 'Down'
	dataset.UpDown = le.fit(dataset.UpDown).transform(dataset.UpDown)

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

df = pd.read_csv("GM.csv")
#using open, high, close to determine UpDown
df.drop(['date'], 1, inplace=True)
df.drop(['low'], 1, inplace=True)
df.drop(['volume'], 1, inplace=True)
df.drop(['open'], 1, inplace=True)
df.drop(['adj_close'],1, inplace=True)

addDailyReturn(df)

X = np.array(df.drop(['UpDown'],1))
y = np.array(df['UpDown'])
print y

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = neighbors.KNeighborsClassifier() 
clf.fit(X_train,y_train)

accuracy = clf.score(X_test,y_test)

print accuracy

test_set = np.array([[104,106]])

prediction = clf.predict(test_set)

print prediction
