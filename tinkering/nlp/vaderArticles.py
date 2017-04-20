#!/usr/bin/python

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize
import requests
import json
import os
import re
import codecs

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
	data_file = file.read()
	#data = [line.rstrip() for line in data_file]
	lines_list = tokenize.sent_tokenize(data_file)
	print lines_list
	sentences.extend(lines_list)
	result = {'compound':[], 'neg':[], 'neu':[], 'pos':[] }
	sid = SentimentIntensityAnalyzer()
	for sentence in sentences:
		print sentence.encode('utf-8')
		ss = sid.polarity_scores(sentence)
		for k in sorted(ss):
			print '{0}: {1}, '.format(k, ss[k]),
		print ""
		result['compound'].append(ss['compound'])
		result['neg'].append(ss['neg'])
		result['neu'].append(ss['neu'])
		result['pos'].append(ss['pos'])
		
	print 'sum:'
	for i in result.keys():
		print '\t',i,':', sum(result[i])
		
def main():
	articles_path = u"/home/trey/bug-free-octo-parakeet/tinkering/nlp/proccessed"
	
	files = get_files(articles_path)
	
	for f in files:
		vader(f)
		
if __name__== "__main__":
	main()
	

	

	
	
	