#!/usr/bin/env python
import logging
from datetime import datetime, timedelta

from Queue import Queue
from threading import Thread

import ujson as json

from ifc.articles import article_to_file, handle_article_file

def create_urls(url_template, subs=[]):
    """ creates a list of urls given a template and the subsitutions """
    if len(subs) == 0:
        return [url_template]
    else:
        return [url_template % (s) for s in subs]

def daterangeGenerator(start_date, end_date, str_format="%Y%m%d"):
    if start_date == end_date:
        yield str_to_date(end_date, str_format)
    for n in range(int((str_to_date(end_date, str_format) - str_to_date(start_date, str_format)).days)):
        yield str_to_date(start_date) + timedelta(n)

def daterange(start_date, end_date, str_format="%Y%m%d"):

    return [d.strftime(str_format) for d in daterangeGenerator(start_date, end_date, str_format="%Y%m%d")]
    
def str_to_date(date_str, str_format="%Y%m%d"):
	return datetime.strptime(date_str, str_format)

class Gatherer(Thread):
    def __init__(self, startDate, endDate, storage_config, config=None, dlPath="./articles", numThreads=8):
        super(Gatherer, self).__init__()
        self.daemon = True
        self.startDate = startDate
        self.endDate = endDate
        self.queue = Queue()
        self.dlPath = dlPath
        self.numThreads = numThreads
        self.storage_config = storage_config

    def find_all_articles(self):
        """ place all article in the queue """
        pass

    def run(self):
        self.find_all_articles()
        while not self.queue.empty():
            url = self.queue.get()
            try:
                logging.debug("downloading url %s", url)
                path = article_to_file(url, self.dlPath)
                handle_article_file(path, self.storage_config)
            except Exception as e:
                logging.error("failed to download article %s: %s", url, e)
            self.queue.task_done()
        self.queue.join() # wait for threads


