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
            
def article_to_file(url, folder, main_url):
    j = {}
    try:
        a = Article(url)
        a.download()
        a.parse()
        j['url'] = url
        j['title'] = a.title.replace('/', '\\')
        j['text'] = a.text
        j['authors'] = a.authors
        j['error'] = None
        try:
            if "An Error has occured" in a.title:
                print "Bad article (no title): ", url
                return
            j['date'] = a.publish_date.strftime("%Y%m%d")
            j['epoch'] = a.publish_date.strftime("%s") # to epoch time
        except Exception as e:
            print "Bad article (Date): ", url
            j['date'] = '' 
            j['epoch'] = ''
        a.nlp()
        j['keywords'] = a.keywords
        filename = os.path.join(folder, "%s_%s" % (j['date'], j['title']))

        #print j['date'], a.title 
        
        with open(filename, 'w') as f:
            f.write(json.dumps(j))
            
    except Exception as e:
        print "Bad article: ", url

def url_to_articles(url):
    ret = []
    page = requests.get(url)
    tree = html.fromstring(page.content)
    ret = tree.xpath('//div[@class="headlineMed"]/a/@href')
    return ret

q = Queue()
folder = "articles"
num_worker_threads = 4

def dl_worker():
    while not q.empty():
        url = q.get()
        try:
            for u in url_to_articles(url):
                try:
                    article_to_file(u, folder, url)
                except Exception as e:
                    print e, u
        except Exception as e:
            print e, u

    q.task_done()


def main():
    urls = create_urls("articles.json")
    if not os.path.exists(folder) or not os.path.isdir(folder):
        os.mkdir(folder)

    urls.reverse()
    #for u in urls[1800:]:
    for u in urls[:]:
        q.put(u)

    for i in range(num_worker_threads):
        t = Thread(target=dl_worker)
        t.daemon = True
        t.start()

    q.join() # wait for threads

if __name__ == "__main__": 
    nltk.download('punkt')
    main()

