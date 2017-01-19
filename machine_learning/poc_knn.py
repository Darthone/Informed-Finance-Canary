import numpy as np
from math import sqrt
import warnings
from collections import Counter
import pandas as pd
import random
import urllib2

def k_nearest_neighbors(data, predict, k=3.0):
	if len(data) >= k:
		warnings.warn('K is a value less than total groups')

	distances = []
	for group in data:
		for features in data[group]:
			#calculating euclidian distance
			e_distance = np.linalg.norm(np.array(features)-np.array(predict))
			distances.append([e_distance, group])

	votes = [i[1] for i in sorted(distances)[:k]]
	#print(Counter(votes).most_common(1))
	vote_result = Counter(votes).most_common(1)[0][0]
	confidence = float(Counter(votes).most_common(1)[0][1]) / k
	
	#print(vote_result, confidence)

	#knnalgos
	return vote_result, confidence

accuracies = []

for i in range(5):
	df = pd.read_csv("breast_cancer_data.txt")
	df.replace('?',-99999, inplace=True)
	#df.drop(['id'], 1, inplace=True)
	full_data = df.astype(float).values.tolist()

	random.shuffle(full_data)

	test_size = 0.2
	train_set = {2:[],4:[]}
	test_set = {2:[],4:[]}
	train_data = full_data[:-int(test_size*len(full_data))]
	test_data = full_data[-int(test_size*len(full_data)):]

	for i in train_data:
		train_set[i[-1]].append(i[:-1])

	for i in test_data:
		test_set[i[-1]].append(i[:-1])

	correct = 0.0
	total = 0.0

	for group in test_set:
		for data in test_set[group]:
			vote,confidence = k_nearest_neighbors(train_set, data, k=5)
			if group == vote:
				correct +=1
			total +=1

	percent_correct = correct/total

	"""
	print correct
	print total 
	print percent_correct
	"""

	print 'Accuracy: ' + str(percent_correct)

	accuracies.append(percent_correct)

print(sum(accuracies)/len(accuracies))
