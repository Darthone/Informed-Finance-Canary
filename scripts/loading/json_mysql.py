#!/usr/bin/python

import json
import os
import MySQLdb as mdb
from warnings import filterwarnings
filterwarnings('ignore', category = mdb.Warning)
import sys
from pprint import pprint
from shutil import move

def get_files(file_path):
    """ returns all files in a given file_path"""
    ret = []
    for root, dirs, files in os.walk(file_path):
        for f in files:
            ret.append(os.path.join(root, f))
    return ret

def insert_article_file(file_path, ingested_path):
	con = mdb.connect()
	with con:
		with open(file_path, 'r') as data_file:
			data = json.load(data_file)
			
		try:
			cur = con.cursor()
			web_source = "bloomberg"

			if 'authors' in data:
				authors = data['authors']
				authorQuery = 'INSERT IGNORE INTO author(author_id,name) VALUES (%s,%s)'
				authorArgs = [(authors.replace(" ", "_") + "_" + web_source,authors) for authors in data['authors']]
				cur.executemany(authorQuery,authorArgs)
			
			if 'tickers' in data:
				tickers = data['tickers']
				tickerArgs = [(tickers,tickers) for tickers in data['tickers']] 
				tickerQuery = 'INSERT IGNORE INTO stocks(stocks_id,ticker) VALUES (%s,%s)'
				cur.executemany(tickerQuery,tickerArgs)

			title = data["title"]
			date = data["date"]
			epoch = data["epoch"]
			text = data["text"]
			pk = date + "_" + title.replace(" ","_")
			articleArgs = (pk,title,date,text,web_source)
			articleQuery = 'INSERT IGNORE INTO articles(article_id,title,date,content,web_source) VALUES (%s,%s,%s,%s,%s)'
			cur.execute(articleQuery,articleArgs)
			
		finally:
			cur.close()
			if not os.path.exists(file_path):
				move(file_path,ingested_path)
			else:
				os.remove(file_path)
		

def main():
	# Directory to where articles are stored
	articles_path = u"/home/trey/bug-free-octo-parakeet/rss_grabber/handled/test"
	# Gets each filename
	files = get_files(articles_path)
	# Directory where ingested files will be moved to
	ingested_path = u"/home/trey/bug-free-octo-parakeet/rss_grabber/handled/testIngest"
	
	for f in files:
		insert_article_file(f,ingested_path)
		
if __name__== "__main__":
	main()
