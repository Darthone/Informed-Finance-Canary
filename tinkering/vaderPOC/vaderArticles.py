#!/usr/bin/python

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize
import requests
import json
import os
import re
import codecs

sentences = []

file_path='/home/trey/bug-free-octo-parakeet/tinkering/testArticles/opinionArticle'
with codecs.open(file_path, mode='r', encoding='utf-8') as data_file:
	data = json.load(data_file)
content = data['text']
lines_list = tokenize.sent_tokenize(content)
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
	

	

	
	
	