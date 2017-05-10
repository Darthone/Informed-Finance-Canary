#!/usr/bin/python

from ifc.db import StockArticle, Stock, Article, Author
import peewee

query = (StockArticle.select(Article.id.alias('article_id'), Article.title, Article.content, Stock.id.alias('stock_id'), Stock.ticker, StockArticle).join(Stock, on=(StockArticle.stock_id == Stock.id)).join(Article, on=(StockArticle.article_id == Article.id)).where(Stock.ticker == 'GM.N').naive())

articleList = {}

#for article in qry:
articleList = {article.article_id : article.content for article in query }
	#articleList.append(article.id,article.content)

print len(articleList)
