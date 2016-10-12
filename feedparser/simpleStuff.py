#!/usr/bin/env python
import feedparser

def main():
	d = feedparser.parse("http://feedparser.org/docs/examples/atom10.xml")
	print(d)

if __name__ == '__main__':
	main()
