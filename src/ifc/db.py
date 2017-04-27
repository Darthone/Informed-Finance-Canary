#!/usr/bin/python

from peewee import *

db = MySQLDatabase("ifc", host="127.0.0.1", port=3306, user="dario", passwd="SecurePassword08!")

class BaseModel(Model):
    """ Base Model which is extended in each model """
    class Meta:
        database = db


class Author(BaseModel):
    """ Author information """
    name = CharField(unique=True)
    
        
class Stock(BaseModel):
    """ Stock name and ticker symbol """
    ticker = CharField(unique=True)
    name = CharField(unique=True)
    

class StockFeature(BaseModel):
    """ Model storing info about stock prices """
    id = IntegerField()
    stock = ForeignKeyField(Stock, related_name='stock_name')
    date = DateField()
    high = DecimalField()
    low = DecimalField()
    volume = DecimalField()
    opening = DecimalField()
    closing = DecimalField()
    rsi = DecimalField()
    macd = DecimalField()
    sma = DecimalField()
    ema = DecimalField()
    
    class Meta:
        primary_key = CompositeKey('id', 'stock', 'date')

    
""" I'm not sure if we need this, I think it's just a join and filter
class ArticleFeatureStockFeature(BaseModel):
    article = 
    stock =
    date = DateField()

    class Meta:
        primary_key = CompositeKey(
   """ 

class Article(BaseModel):
    """ Contains content from an article """
    author = ForeignKeyField(Author, related_name='author')
    date = DateField()
    title = CharField(unique=True)
    content = TextField()
    source = CharField()


class ArticleFeature(BaseModel):
    """ Relationship for showing which article relates to the extracted feasture """
    article = ForeignKeyField(Article, related_name="article", primary_key=True)
    positive = DecimalField()
    negative = DecimalField()
    other = TextField()


class StockArticle(BaseModel):
    """ many-to-many relationship showing which stocks were found in an article """
    stock = ForeignKeyField(Stock)
    article = ForeignKeyField(Article)
    

if __name__ == "__main__":
    try:
        Author.create_table()
    except OperationalError:
        print "Author table already exists"
    try:
        Stock.create_table()
    except OperationalError:
        print "Stock table already exists"
    try:
        StockFeature.create_table()
    except OperationalError:
        print "Stock_feature table already exists"
    try:
        Article.create_table()
    except OperationalError:
        print "Article table already exists"
    try:
        StockArticle.create_table()
    except OperationalError:
        print "Stock_article table already exists"
    try:
        ArticleFeature.create_table()
    except OperationalError:
        print "Article_feature table already exists"
    #try:
    #    ArticleFeatureStockFeature.create_table()
    #except OperationalError:
    #    print "Article_feature_stock_feature table already exists"
    
