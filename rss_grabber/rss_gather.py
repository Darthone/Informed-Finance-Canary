#!/usr/bin/env python
import json
import os
import time
import logging

from threading import Thread

import requests
import nltk

from lxml import html
from newspaper import Article
from pull_ticker_from_article import create_dir, handle_article_file

#this is required so download it when ever the modula is called
nltk.download('punkt')

class ArticleStorageConfig():
    """ Stores information to pass to Threads """
    def __init__(self, stock_path, other_path, bad_path, error_path):
        self.stock_path = stock_path
        self.other_path = other_path
        self.bad_path = bad_path
        self.error_path = error_path


def create_urls(filename):
    json_data = {}
    ret = []
    with open(filename, 'r') as f:
        json_data = json.load(f)
    for s in json_data["sites"]:
        url_template = s['url']
        titles_key = "titles"
        if titles_key in s: # append each url
            for title in s['titles']:
                ret.append(url_template % (title))
        else: # there's no url template just a straight url
            ret.append(url_template)
    return ret
    
def article_to_file(url, folder):
    """ returns where the file is written to if successful, otherwise throws an error """
    j = {}
    try:
        a = Article(url)
        a.download()
        a.parse()
        j['title'] = a.title.replace('/', '\\')
        j['text'] = a.text
        j['authors'] = a.authors
        j['date'] = a.publish_date.strftime("%Y%m%d")
        j['epoch'] = a.publish_date.strftime("%s")
        formatTitle = j['title'].replace(" ","_").replace("'","\\'")
            
        a.nlp()
        j['keywords'] = a.keywords
        
        filename = os.path.join(folder, "%s_%s" % (j['date'], formatTitle))
        print j['date'], a.title
        
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                f.write(json.dumps(j))
        return filename
    except Exception as e:
        print e

def page_content_to_articles(page_content):
    ret = []
    tree = html.fromstring(page_content)
    ret = tree.xpath('//guid/text()')
    return ret

def dl_worker(url_to_watch, folder, storage_cfg):
    """ thread function, watches rss feeds and downloads the articles.
        exits if the url returns 404 """
    while (True):
        r = requests.get(url_to_watch)
        if r.status_code == 404:
            #log
            break
        for u in page_content_to_articles(r.content):
            try:
                f_path = article_to_file(u, folder)
                handle_article_file(f_path, storage_cfg.stock_path, 
                        storage_cfg.other_path, storage_cfg.bad_path)
            except Exception as e:
                logging.error(e)
                # log errros somewhere TODO
                pass
        time.sleep(120) # wait to reload the articles list
    
def main():
    #TODO Move these values to a config file which this program accepts as a command line arge
    rss_feeds_json = './rss_feeds_to_watch.json'
    articles_path = "articles"
    base_path = "/hostname/senior-design/handled"
    create_dir(base_path)

    #TODO set up logging
    FORMAT = '%(asctime)-15s %(filename)s %(thread)d %(funcName)s %(lineno)d %(message)s'
    logging.basicConfig(format=FORMAT)
    
    stock_path = os.path.join(base_path, "stock")
    other_path = os.path.join(base_path, "other")
    bad_path = os.path.join(base_path, "bad")
    error_path = os.path.join(base_path, "error")
    create_dir(error_path)
    create_dir(bad_path)
    create_dir(stock_path)
    create_dir(other_path)

    storage_cfg = ArticleStorageConfig(stock_path, other_path, bad_path, error_path)
    create_dir(articles_path)

    urls = create_urls(rss_feeds_json)
    t_handles = []
    for url in urls: # each thread gets a url to watch
        t = Thread(target=dl_worker, args=(url, articles_path, storage_cfg,))
        t.daemon = False
        t.start()
        t_handles.append(t)

    # wait for threads to never finish
    for t in t_handles:
        t.join()
    
if __name__ == "__main__":
    main()

