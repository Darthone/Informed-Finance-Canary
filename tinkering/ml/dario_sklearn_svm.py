#!/usr/bin/env python
import numpy as np
import pandas as pd

from sklearn import preprocessing, cross_validation, svm


def main():

    df = pd.read_csv("AAPL.txt")
    #df.replace('?',-99999, inplace=True)
    #df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df.drop(['low'], 1, inplace=True)
    df.drop(['volume'], 1, inplace=True)
    #df['sma'] = pd.rolling_mean(df['open'], 5)
    df.drop(['date'], 1, inplace=True)
    #df = df[5:]
    print df

    for i in range(1):
        X = np.array(df.drop(['open'], 1))
        y = np.array(df['open'])

        print "training Data", X
        print "labels", y[:-1]
        
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=.5)
        clf = svm.SVR()
        clf.fit(X_train, y_train)

        #clf = svm.SVC()
        #clf.fit(X, y) 

    test_set = np.array([[118.99, 117.94]]) #, 116.46]])
    #test_set = test_set.reshape(len(test_set), -1)
    prediction = clf.predict(test_set)
    print prediction

if __name__ == "__main__":
    main()
