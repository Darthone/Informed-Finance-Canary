from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ifc.db import StockArticle, Stock, Article, ArticleFeature, db

def db_insert(records):
    with db.atomic():
        for r in records:
            ArticleFeature.insert(r).execute()
            
def vader(article_id, lines):
    sid = SentimentIntensityAnalyzer()
    result = {
        'compound': 0.0,
        'negative': 0.0,
        'neutral': 0.0,
        'positive': 0.0,
        'article': article_id
    }
    for sentence in lines:
        ss = sid.polarity_scores(sentence)
        result['compound'] += ss['compound']
        result['negative'] += ss['neg']
        result['neutral'] += ss['neu']
        result['positive'] += ss['pos']
    return result

def get_articles():
    #TODO
    pass

def tfidf(corpus, corpusKeys):
    #TODO clean this up
    #discard any stop words - saves on processing
    stopset = list(stopwords.words('english'))
    stopset.append('000')
    stopset.extend([str(x) for x in range(9999)])
    vectorizer = TfidfVectorizer(stop_words=stopset, use_idf=True, ngram_range=(2,3))
    
    #matrix of input set
    X = (vectorizer.fit_transform(corpus)).toarray()
    size_matrix = X.shape[0] 
    lsa = TruncatedSVD(n_components=size_matrix, n_iter=100)
    terms = vectorizer.get_feature_names()
    records = []
    for i, comp in enumerate(X):
        termsInComp = zip(terms, comp)
        sortedTerms = sorted(termsInComp, key=lambda x: x[1], reverse=True) [:10]
        
        #List with all the terms gathered from the tfidf vectorizer
        termList = [term[0] + '.' for term in sortedTerms]
        
        # List with Article ID and list of tfidf terms
        records.append((vader(corpusKeys[i], termList), termList))
    return records

def main():
    qry = (StockArticle.select(Article.id, Article.title, Article.content, Article.date, Stock.id.alias('stock_id'), Stock.ticker, StockArticle).join(Stock, on=(StockArticle.stock_id == Stock.id)).join(Article, on=(StockArticle.article_id == Article.id)).where((Stock.ticker == 'GM') | (Stock.ticker == 'TGT'), Article.date > '2012-01-01').limit(10).naive())
    corpusDict = {article.article_id : article.content for article in qry }
    corpus = corpusDict.values()
    corpusKeys = corpusDict.keys()
    records = tfidf(corpus, corpusKeys)
    db_insert([r[0] for r in records])
    
if __name__== "__main__":
    main()

