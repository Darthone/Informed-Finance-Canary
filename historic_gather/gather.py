#!/usr/bin/env python
import json
import nltk
import os
import requests

from lxml import html
from newspaper import Article
from Queue import Queue
from threading import Thread

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

q = Queue()
folder = "articles"
num_worker_threads = 18

def dl_worker():
    url = q.get()
    if url is not None:
        for u in url_to_articles(url):
            article_to_file(u, folder)
        q.task_done()
        url = q.get()
    q.task_done()

def main():
    urls = create_urls("articles.json")
    if not os.path.exists(folder) or not os.path.isdir(folder):
        os.mkdir(folder)

    for i in range(num_worker_threads):
        t = Thread(target=dl_worker)
        t.daemon = True
        t.start()

    #urls.reverse()
    for u in urls:
        q.put(u)
     
    q.join()

if __name__ == "__main__": 
    nltk.download('punkt')
    main()

