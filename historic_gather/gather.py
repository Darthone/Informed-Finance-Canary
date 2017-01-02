#!/usr/bin/env python
import json
import nltk
from newspaper import Article
import os
import requests
from lxml import html

def create_urls(filename):
    json_data = {}
    ret = []
    with open(filename, 'r') as f:
        json_data = json.load(f)
    url_template = json_data['url']
    for date in json_data['dates']:
        ret.append(url_template % (date))
    return ret

def article_to_file(url, folder):
    j = {}
    try:
        a = Article(url)
        a.download()
        a.parse()
        j['title'] = a.title.replace('/', '\\')
        j['text'] = a.text
        j['authors'] = a.authors
        j['date'] = a.publish_date.strftime("%Y%m%d")
        j['epoch'] = a.publish_date.strftime("%s") # to epoch time
        a.nlp()
        j['keywords'] = a.keywords
        filename = os.path.join(folder, "%s_%s" % (j['date'], j['title']))

        print j['date'], a.title 
        with open(filename, 'w') as f:
            f.write(json.dumps(j))
    except Exception as e:
        print e

def url_to_articles(url):
    ret = []
    page = requests.get(url)
    tree = html.fromstring(page.content)
    ret = tree.xpath('//div[@class="headlineMed"]/a/@href')
    return ret

def main():
    urls = create_urls("articles.json")
    #url ='http://www.reuters.com/article/aids-day-china-idUSL4N1DO19B'
    folder = "articles"
    if not os.path.exists(folder) or not os.path.isdir(folder):
        os.mkdir(folder)

    #urls.reverse()
    print len(urls)
    i = 0 # starting point
    for url in urls[i:]:
        print i
        for u in url_to_articles(url):
            article_to_file(u, folder)
        i+=1


if __name__ == "__main__": 
    nltk.download('punkt')
    main()

