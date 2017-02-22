import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, neighbors 
from collections import Counter
#style.use('fivethirtyeight')
import warnings
import random

def k_nearest_neighbors(data, predict, k=3):
	if len(data) >= k:
		warnings.warn('K is a value less than total groups')

	#need to iterate through all the features in order to compare the closest points
	distances = []
	for group in data:
		for features in data[group]:
			#calculating euclidian distance
			e_distance = np.linalg.norm(np.array(features)-np.array(predict))
			#list of lists that define distance and grouping
			distances.append([e_distance, group])

	# get the k number of closest points and take their distance
	votes = [i[1] for i in sorted(distances)[:k]]
	#print(Counter(votes).most_common(1))
	vote_result = Counter(votes).most_common(1)[0][0]
	confidence = float(Counter(votes).most_common(1)[0][1]) / k
	
	#print(vote_result, confidence)

	#knnalgos
	return vote_result, confidence

accuracies = []

for i in range(5):
	df = pd.read_csv("AAPL.txt")
	#getting rid of columns we don't want
	df.drop(['date'], 1, inplace=True)
	df.drop(['low'], 1, inplace=True)
	df.drop(['volume'], 1, inplace=True)
	#data cleansing by converting to float for proper calculations
	full_data = df.astype(float).values.tolist()
	
	#shuffle data 
	random.shuffle(full_data)
	
	#initialize training and testing
	test_size = 0.2
	#populate distance and class dictionaries
	train_set = {}
	test_set = {}
	#partitioning the percent train and percent test
	train_data = full_data[:-int(test_size*len(full_data))]
	test_data = full_data[-int(test_size*len(full_data)):]

	for i in train_data:
		if not i[-1] in train_set:
			train_set[i[-1]] = [i[:-1]]
		else:
			train_set[i[-1]].append(i[:-1])

	for i in test_data:
		if not i[-1] in test_set:
			test_set[i[-1]] = [i[:-1]]
		else:
			test_set[i[-1]].append(i[:-1])

	correct = 0
	total = 0

	for group in test_set:
		for data in test_set[group]:
			vote = k_nearest_neighbors(train_set, data, k=5)
			if group == vote:
				correct += 1
			total += 1

	#print correct
	#print total
	percent_correct = correct/total 
	print percent_correct
	

#	accuracies.append(accuracy)

"""
print(sum(accuracies)/len(accuracies))

test_set = np.array([[104,106]])

test_set = test_set.reshape(len(test_set),-1)

prediction = clf.predict(test_set)

print prediction
"""
