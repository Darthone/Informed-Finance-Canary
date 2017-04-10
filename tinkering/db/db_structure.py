#!/usr/bin/python

import peewee
from peewee import *

database = MySQLDatabase("ifc", host="192.168.1.128", port=3306, user="", passwd="")

class author(peewee.Model):
	author_id = peewee.CharField(primary_key="true")
	name = peewee.CharField()
	
	class Meta:
		database = database
		
class stock(peewee.Model):
	stock_id = peewee.CharField(primary_key="true")
	ticker = peewee.CharField()
	name = peewee.CharField()
	
	class Meta:
		database = database

class stock_feature(peewee.Model):
	stock_id = peewee.CharField(primary_key="true")
	date = peewee.DateField()
	high = peewee.CharField()
	low = peewee.CharField()
	volume = peewee.CharField()
	opening = peewee.CharField()
	closing = peewee.CharField()
	rsi = peewee.CharField()
	macd = peewee.CharField()
	sma = peewee.CharField()
	ema = peewee.CharField()
	
	class Meta:
		database = database

class article_feature(peewee.Model):
	article_feature_id = peewee.IntegerField(primary_key="true")
	positive = peewee.CharField()
	negative = peewee.CharField()
	article_id = peewee.CharField()
	
	class Meta:
		database = database

class article_feature_stock_feature(peewee.Model):
	article_feature_id = peewee.IntegerField(primary_key="true")
	stock_id = peewee.CharField()
	date = peewee.DateField()
	
	class Meta:
		database = database

class article(peewee.Model):
	article_id = peewee.CharField(primary_key="true")
	stock_id = peewee.CharField()
	date = peewee.CharField()
	title = peewee.CharField()
	content = peewee.CharField()
	stock_prices = peewee.CharField()
	feature_set = peewee.CharField()
	web_source = peewee.CharField()
	author_id = peewee.CharField()
	
	class Meta:
		database = database

class stock_article(peewee.Model):
	stock_id = peewee.CharField(primary_key="true")
	article_id = peewee.CharField()
	
	class Meta:
		database = database

if __name__ == "__main__":
	try:
		author.create_table()
	except peewee.OperationalError:
			print "Author table already exists"
	try:
		stock.create_table()
	except peewee.OperationalError:
			print "Stock table already exists"
	try:
		stock_feature.create_table()
	except peewee.OperationalError:
			print "Stock_feature table already exists"
	try:
		article_feature.create_table()
	except peewee.OperationalError:
			print "Article_feature table already exists"
	try:
		article_feature_stock_feature.create_table()
	except peewee.OperationalError:
			print "Article_feature_stock_feature table already exists"
	try:
		article.create_table()
	except peewee.OperationalError:
			print "Article table already exists"
	try:
		stock_article.create_table()
	except peewee.OperationalError:
			print "Stock_article table already exists"
	
