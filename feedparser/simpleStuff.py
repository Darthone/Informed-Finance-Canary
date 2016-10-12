#!/usr/bin/env python
import feedparser

def main():
	# feed data is a dictionary
	d = feedparser.parse("http://reddit.com/r/python/.rss")
	# print(d['feed']['title'])
	
	# relative links
	# print d['feed']['link']

	# parse escaped HTML
	# print d.feed.subtitle
	
	# see # of entries
	print len(d['entries'])
	print('\n')

	# each entry in the feed is a dictionary. Use [0] to print the first
	# entry
	print d['entries'][0]['title']

	# feedparser tutorial
if __name__ == '__main__':
	main()
