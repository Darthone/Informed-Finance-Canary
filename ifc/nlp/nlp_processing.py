import nltk
import math
from nltk.corpus import state_union, stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import pandas as pd

#State of the Union Addresses
train_text = state_union.raw("2005-GWBush.txt")
train_text2 = state_union.raw("2006-GWBush.txt")

#print train_text

#preprocessing
#tokenize by word - this is the Bag of Words
tokenized = word_tokenize(train_text)
tokenized2 = word_tokenize(train_text2)

corpus = [train_text, train_text2]

print corpus[0]

#discard any stop words - saves on processing
stopset = set(stopwords.words('english'))

vectorizer = TfidfVectorizer(stop_words=stopset, use_idf=True)

X = vectorizer.fit_transform(corpus)

print X[0]

size_matrix = X.shape[0] 

lsa = TruncatedSVD(n_components=size_matrix, n_iter=100)
lsa.fit(X)

print lsa.components_[0]

terms = vectorizer.get_feature_names()
for i, comp in enumerate(lsa.components_):
	termsInComp = zip(terms,comp)
	sortedTerms = sorted(termsInComp, key=lambda x: x[1], reverse=True) [:10]
	print "Concept %d:" % i
	for term in sortedTerms:
		print term[0]
	print "   "
