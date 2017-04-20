#!/usr/bin/env python
import argparse
import logging
import os
import sys

import ujson as json

from ifc import common
from ifc.gather import rss

def create_urls(config):
    ret = []
    for s in config["sites"]:
        url_template = s['url']
        titles_key = "titles"
        if titles_key in s: # append each url
            for title in s['titles']:
                ret.append(url_template % (title))
        else: # there's no url template just a straight url
            ret.append(url_template)
    return ret

def parse_args():
    parser = argparse.ArgumentParser(description='Downloads all article from Reuters archives between two dates')
    parser.add_argument('-c', "--config", help="Config file to load in via json. Default ./conf.json", default="./conf.json")
    args = parser.parse_args()
    if not os.path.exists(args.config) or not os.path.isfile(args.config):
        raise IOError("Config file missing or not a file: %s", args.config)
    return args

def main():
    args = parse_args()
    config = common.load_config_file(args.config)

    #TODO set up logging
    FORMAT = '%(asctime)-15s %(filename)s %(thread)d %(funcName)s %(lineno)d %(message)s'
    logging.basicConfig(format=FORMAT)

    articles_path = config["articlesPath"]
    base_path = config["basePath"]
    common.create_dir(articles_path)
    common.create_dir(base_path)

    stock_path = os.path.join(base_path, "stock")
    other_path = os.path.join(base_path, "other")
    bad_path = os.path.join(base_path, "bad")
    error_path = os.path.join(base_path, "error")
    common.create_dir(error_path)
    common.create_dir(bad_path)
    common.create_dir(stock_path)
    common.create_dir(other_path)

    storage_cfg = rss.ArticleStorageConfig(stock_path, other_path, bad_path, error_path)

    t_handles = []
    for url in create_urls(config): # each thread gets a url to watch
        t = rss.RssGatherer(url, articles_path, storage_cfg)
        t.start()
        t_handles.append(t)

    # wait for threads to never finish
    for t in t_handles:
        t.join()

if __name__ == "__main__":
    main()

