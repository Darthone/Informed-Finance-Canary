#!/usr/bin/env python
import os
import time
import logging

from threading import Thread

import requests
import ujson as json
from lxml import html

from ifc.common import create_dir
from ifc.articles import handle_article_file, article_to_file

class ArticleStorageConfig():
    """ Stores information to pass to Threads """
    def __init__(self, stock_path, other_path, bad_path, error_path):
        self.stock_path = stock_path
        self.other_path = other_path
        self.bad_path = bad_path
        self.error_path = error_path


class RssGatherer(Thread):
    """ Watches rss feeds and downloads the articles.
        exits if the url returns 404 """

    def __init__(self, url_to_watch, folder, storage_cfg, sleep_time=120):
        super(RssGatherer, self).__init__()
        self.daemon = True
        self.url_to_watch = url_to_watch
        self.folder = folder
        self.storage_cfg = storage_cfg
        self.sleep_time = sleep_time

    def run(self):
        while (True):
            req = requests.get(self.url_to_watch)
            if req.status_code == 404:
                #log
                break
            for url in self.page_content_to_articles(req.content):
                try:
                    f_path = article_to_file(url, self.folder)
                    handle_article_file(f_path, self.storage_cfg.stock_path,
                                        self.storage_cfg.other_path, self.storage_cfg.bad_path)
                except Exception as e:
                    logging.error(e)
                    # log errros somewhere TODO
                    pass
            time.sleep(self.sleep_time) # wait to reload the articles list

    def page_content_to_articles(self, page_content):
        tree = html.fromstring(page_content)
        return tree.xpath('//guid/text()')

