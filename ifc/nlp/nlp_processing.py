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

print train_text

#preprocessing
#tokenize by word - this is the Bag of Words
tokenized = word_tokenize(train_text)
tokenized2 = word_tokenize(train_text2)

#discard any stop words - saves on processing
stopset = set(stopwords.words('english'))

vectorizer = TfidfVectorizer(stop_words=stopset, use_idf=True, ngram_range=(1,3))

X = vectorizer.fit_transform(tokenized)

print X


