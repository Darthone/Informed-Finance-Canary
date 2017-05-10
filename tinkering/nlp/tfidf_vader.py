import math
from nltk.corpus import state_union, stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import pandas as pd
import shutil
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ifc.db import StockArticle, Stock, Article, Author, ArticleFeature, db
import peewee

def tfidf():
	qry = (StockArticle.select(Article.id, Article.title, Article.content, Article.date, Stock.id.alias('stock_id'), Stock.ticker, StockArticle).join(Stock, on=(StockArticle.stock_id == Stock.id)).join(Article, on=(StockArticle.article_id == Article.id)).where((Stock.ticker == 'GM.N') | (Stock.ticker == 'TGT.N') | (Stock.ticker == 'UAA') | (Stock.ticker == 'UAA.N'), Article.date > '2015-01-01').naive())
	corpusDict = {article.article_id : article.content for article in qry }
	corpus = corpusDict.values()
	corpusKeys = corpusDict.keys()

	#discard any stop words - saves on processing
	stopset = list(stopwords.words('english'))
	stopset.append('000')
	for i in range(9999):
		stopset.append(str(i))
	vectorizer = TfidfVectorizer(stop_words=stopset, use_idf=True, ngram_range=(2,3))
	
	#matrix of input set
	X = vectorizer.fit_transform(corpus)
	X = X.toarray()
	size_matrix = X.shape[0] 
	lsa = TruncatedSVD(n_components=size_matrix, n_iter=100)
	#lsa.fit(X)
	terms = vectorizer.get_feature_names()
	tfidfList = []
	for i, comp in enumerate(X):
		termsInComp = zip(terms,comp)
		sortedTerms = sorted(termsInComp, key=lambda x: x[1], reverse=True) [:10]
		
		#List with all the terms gathered from the tfidf vectorizer
		termList = [term[0] + '.' for term in sortedTerms]
		
		# List with Article ID and list of tfidf terms
		tfidfList = [corpusKeys[i],termList]
		
		vader(tfidfList)
		
def vader(term):
	data = term[1]
	result = {'compound':[], 'neg':[], 'neu':[], 'pos':[] }
	sid = SentimentIntensityAnalyzer()
	for sentence in data:
		ss = sid.polarity_scores(sentence)
		result['compound'].append(ss['compound'])
		result['neg'].append(ss['neg'])
		result['neu'].append(ss['neu'])
		result['pos'].append(ss['pos'])
	vaderList = [sum(result[i]) for i in result.keys()]
	list = [term[0],vaderList]
	resultsKeys = result.keys()	
	db_data = ({'article': list[0], 'negative': list[1][0], 'neutral': list[1][1], 'positive': list[1][2], 'compound': list[1][3]})
	try:
		with db.atomic():
				ArticleFeature.insert(db_data).execute()
	except peewee.IntegrityError:
		print term[0]
		#print 'Skipping Duplicate'
			
def main():

	tfidf()
	
if __name__== "__main__":
	main()