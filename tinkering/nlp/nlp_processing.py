import nltk
import math
from nltk.corpus import state_union, stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import pandas as pd

#State of the Union Addresses
train_text = open("GM1.txt") 
train_text2 = open("GM2.txt")
train_text3 = open("GM3.txt") 
train_text4 = open("GM4.txt")


temp_train_text = train_text.readlines()
#print temp_train_text
str1 = ''.join(temp_train_text)
#print type(temp_train_text)
temp_train_text2 = train_text2.readlines()
str2 = ''.join(temp_train_text2)
temp_train_text3 = train_text3.readlines()
#print temp_train_text
str3 = ''.join(temp_train_text3)
#print type(temp_train_text)
temp_train_text4 = train_text4.readlines()
str4 = ''.join(temp_train_text4)

#preprocessing
#tokenize by word - this is the Bag of Words
#tokenized = word_tokenize(str1)
#tokenized2 = word_tokenize(str2)

corpus = [str1, str2, str3, str4]

print corpus[0]

#discard any stop words - saves on processing
stopset = list(stopwords.words('english'))

stopset.append('000')
for i in range(9999):
	stopset.append(str(i))

vectorizer = TfidfVectorizer(stop_words=stopset, use_idf=True, ngram_range=(2,3))

#matrix of input set
X = vectorizer.fit_transform(corpus)
#print '\n HERPING DERPING\n'
#print vectorizer.get_feature_names()
X = X.toarray()
print sorted(X[0], reverse=True)

print sorted(vectorizer.inverse_transform(X[0]), reverse=True)

size_matrix = X.shape[0] 

lsa = TruncatedSVD(n_components=size_matrix, n_iter=100)
lsa.fit(X)

#print lsa.components_[0]
#print type(lsa.components_)
terms = vectorizer.get_feature_names()
for i, comp in enumerate(X):
#for i, comp in enumerate(lsa.components_):
	termsInComp = zip(terms,comp)
	sortedTerms = sorted(termsInComp, key=lambda x: x[1], reverse=True) [:10]
	print "Article %d:" % i
	for term in sortedTerms:
		print term[0]
	print "   "
