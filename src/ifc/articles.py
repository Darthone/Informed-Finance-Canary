#!/usr/bin/env python
import os
import re
import ujson as json
import string

from lxml import html
from newspaper import Article
from shutil import copyfile
from common import create_dir, get_files, memoize, tickercheck

def get_prefound_files(path):
    """ opens a json file and reads a list from the root of the key files """
    with open(path, 'r') as f:
        return json.loads(f.read())['files']

def find_stock_tickers(text):
    """ finds valid ticker symbols in bodies of text that are closed within parenthesis. Ex (APPL.O) """
    ret = set()
    p = re.findall('\((.*?)\)', text)
    for i in p:
        t = i.strip()
        if tickercheck.is_valid_ticker(t):
            ret.add(t)
    return list(ret)

def handle_article_file(file_path, storage_config):
    """ Processed a file by extracting a ticker(s) and then moving it to an appropriate dir """
    base_name = os.path.basename(file_path)
    with open(file_path, 'rw') as f:
        j = json.loads(f.read())
        if "an error has occured" in j['title'].lower():
            copyfile(file_path, os.path.join(storage_config.bad_path, base_name))
            return
        j['tickers'] = find_stock_tickers(j['text'])
        path = storage_config.other_path if len(j['tickers']) == 0 else storage_config.stock_path
        with open(os.path.join(path, base_name), 'w') as fn:
            fn.write(json.dumps(j))
            
def article_to_file(url, folder):
    """ downloads an article into a file from a url
        throws execption for bad articles """
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
        filename = os.path.join(folder, "%s_%s" % (j['date'], j['title']))

        with open(filename, 'w') as f:
            f.write(json.dumps(j))

        return filename   
    except Exception as e:
        print "Bad article: ", url

def preprocess_article(text):
    """ Changes an articles text to lowercase, removes punctuation """
    return text.encode('ascii', 'ignore').lower().replace("\n", "").translate(None, string.punctuation)

