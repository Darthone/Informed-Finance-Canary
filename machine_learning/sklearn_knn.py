import numpy as np
import pandas as pd
from sklearn import preprocessing, cross_validation, neighbors

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

	X = np.array(df.drop(['class'],1))
	y = np.array(df['class'])

	X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

	clf = neighbors.KNeighborsClassifier()
	clf.fit(X_train,y_train)

	accuracy = clf.score(X_test,y_test)

	"""
	print correct
	print total 
	print percent_correct
	"""

	accuracies.append(percent_correct)

print(sum(accuracies)/len(accuracies))
