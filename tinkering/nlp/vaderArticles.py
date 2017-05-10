#!/usr/bin/python

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize
import requests
import json
import os
import re
import codecs
from ifc.db import ArticleFeature, db
import peewee
import logging

def get_files(file_path):
    """ returns all files in a given file_path"""
    ret = []
    for root, dirs, files in os.walk(file_path):
        for f in files:
            ret.append(os.path.join(root, f))
    return ret
	
def vader(file_path):
	sentences = []
	
	file = open(file_path, 'r')
	base = os.path.basename(file_path)
	articleID =  os.path.splitext(base)[0]
	data_file = file.read()
	#data = [line.rstrip() for line in data_file]
	lines_list = tokenize.sent_tokenize(data_file)
	#print lines_list
	sentences.extend(lines_list)
	result = {'compound':[], 'neg':[], 'neu':[], 'pos':[] }
	sid = SentimentIntensityAnalyzer()
	for sentence in sentences:
		#print sentence.encode('utf-8')
		ss = sid.polarity_scores(sentence)
		#for k in sorted(ss):
		#	print '{0}: {1}, '.format(k, ss[k]),
		#print ""
		result['compound'].append(ss['compound'])
		result['neg'].append(ss['neg'])
		result['neu'].append(ss['neu'])
		result['pos'].append(ss['pos'])
	vaderList = [sum(result[i]) for i in result.keys()]
	list = [articleID,vaderList]
	print list
	#print list[0], list[1][0]
	#print vaderList
	resultsKeys = result.keys()	
	#print 'sum:'
	db_data = ({'article': list[0], 'negative': list[1][0], 'neutral': list[1][1], 'positive': list[1][2], 'compound': list[1][3]})
	#db_data = ({'article': list[0], 'negative': list[1][0], 'neutral': list[1][1], 'positive': list[1][2], 'compound': list[1][3]} for li in list)
	print db_data
	#db_data = ({'article': articleID, 'negative': sum(result[i]), 'neutral': sum(result[i]), 'positive': sum(result[i]), 'compound': sum(result[i])} for i in result.keys())
	with db.atomic():
		ArticleFeature.insert(db_data).execute()
		print "1"
	#		logging.info('Skipping Duplicate')
	#for i in result.keys():
	#	print '\t',i,':', sum(result[i]).append(vaderList)
	
	#for i in result:
		#print result
		#print resultsKeys[i], sum(i)
		#for i in resultsKeys:
			#print summation[i]
		#my_dict = {articleID : (sum(result[i])), (sum(result[i]), (sum(result[i])}
		#print my_dict
		#print articleID, i, sum(result[i])
		#print sum(result[i])
		#db_data = [articleID,sum(result[i])]
		#print '\t',i,':', sum(result[i])
	#print db_data

def main():
	articles_path = u"/home/trey/bug-free-octo-parakeet/tinkering/nlp/processed"
	
	files = get_files(articles_path)
	
	for f in files:
		vader(f)
		
if __name__== "__main__":
	main()
	

	

	
	
	