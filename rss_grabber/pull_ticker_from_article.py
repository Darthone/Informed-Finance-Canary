#!/usr/bin/env python

import json
import os
import re
import requests

from Queue import Queue
from threading import Thread
from shutil import copyfile

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_files(file_path):
    """ returns all files in a given file_path"""
    ret = []
    for root, dirs, files in os.walk(file_path):
        for f in files:
            ret.append(os.path.join(root, f))
    return ret

def get_prefound_files(path):
    """ opens a json file and reads a list from the root of the key files """
    with open(path, 'r') as f:
        return json.loads(f.read())['files']

def memoize(f):
    class memodict(dict):
        __slots__ = ()
        def __missing__(self, key):
            self[key] = ret = f(key)
            return ret
    return memodict().__getitem__

def is_valid_ticker(ticker_s):
    return dumb_valid_ticker(ticker_s) and valid_ticker(ticker_s)

def dumb_valid_ticker(ticker):
    if len(ticker) > 10 or len(ticker.split()) >= 4:
        return False
    return True

@memoize
def valid_ticker(ticker):
    """ reaches to reuters to validate a ticker symbol. Possibly error prone X """
    sym = "symbol=" + ticker
    url_base = "http://www.reuters.com/finance/stocks/overview?" + sym
    return requests.get(url_base).url.endswith(sym)

def find_stock_tickers(text):
    """ finds valid ticker symbols in bodies of text that are closed within parenthesis. Ex (APPL.O) """
    ret = set()
    p = re.findall('\((.*?)\)', text)
    for i in p:
        t = i.strip()
        if is_valid_ticker(t):
            ret.add(t)
    return list(ret)

def handle_article_file(file_path, stock_path, other_path, bad_path):
    """ Processed a file by extracting a ticker(s) and then moving it to an appropriate dir """
    base_name = os.path.basename(file_path)
    with open(file_path, 'rw') as f:
        j = json.loads(f.read())
        if "an error has occured" in j['title'].lower():
            copyfile(file_path, os.path.join(bad_path, base_name))
            return
        j['tickers'] = find_stock_tickers(j['text'])
        path = other_path if len(j['tickers']) == 0 else stock_path
        with open(os.path.join(path, base_name), 'w') as fn:
            fn.write(json.dumps(j))

#this is a library not a program
"""
q = Queue()
num_worker_threads = 6

def worker():
    base_path = "/home/trey/bug-free-octo-parakeet/rss_grabber/handled"
    create_dir(base_path)

    stock_path = os.path.join(base_path, "stock")
    other_path = os.path.join(base_path, "other")
    bad_path = os.path.join(base_path, "bad")
    error_path = os.path.join(base_path, "error")
    create_dir(error_path)
    create_dir(bad_path)
    create_dir(stock_path)
    create_dir(other_path)

    while not q.empty():
        article_file = q.get()
        try:
            handle_article_file(article_file, stock_path, other_path, bad_path)
        except Exception as e: # Move articles that cause an error to another folder for follow up
            base_name = os.path.basename(article_file)
            copyfile(article_file, os.path.join(error_path, base_name))
    q.task_done()

def main():
    articles_path = u"/home/trey/bug-free-octo-parakeet/rss_grabber/articles"
    files = get_files(articles_path)
    #files = get_prefound_files("articles_paths.json")
    
    print len(files)
    #jroot = {}
    #jroot["files"] = files
    #with open("articles_paths.json", 'w') as f:
    #    f.write(json.dumps(jroot))
    for f in files:
        q.put(f)

    for i in range(num_worker_threads):
        t = Thread(target=worker)
        t.daemon = True
        t.start()
    
    q.join() # wait for threads
	
	

if __name__ == "__main__":
    main()
	
"""
