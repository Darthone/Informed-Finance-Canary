#!/usr/bin/env python
import feedparser

def getHeadlines(rss_url):
	headlines = []

	# fetch the rss feed and return the parsed RSS
	feed = feedparser.parse(rss_url)

	for newsitem in feed['items']:
		headlines.append(newsitem['title'])

	return headlines

# list to hold all headlines
allHeadlines = []

# list of RSS feeds that we will fetch and combine
newsurls = {
	'apnews': 'http://hosted2.ap.org/atom/APDEFAULT/3d281c11a76b4ad082fe88aa0db04909',
	'googlenews': 'http://news.google.com/?output=rss',
	'yahoonews': 'http://news.yahoo.com/rss/'
}

# iterate over the feed urls
for key,url in newsurls.items():
	# call getHeadlines() and combine the returned headlines with allHeadlines
	allHeadlines.extend(getHeadlines(url))

# iterate over the allheadlines list and print each headline
for h1 in allHeadlines:
	print(h1)
