import sys
import os
import time
import logging
import argparse
import ujson as json
from datetime import datetime

from ifc import common
from ifc.gather import rss
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from ifc import db
from ifc.articles import preprocess_article

def parse_args():
    parser = argparse.ArgumentParser(description='Loads articles in the database from a folder[s]')
    parser.add_argument('-c', "--config", help="Config file to load in via json. Default ./conf.json", default="./conf.json")
    args = parser.parse_args()
    if not os.path.exists(args.config) or not os.path.isfile(args.config):
        raise IOError("Config file missing or not a file: %s", args.config)
    return args

def load_article(path, handled_path, error_path):
    """ Loads an article into the db """
    base_name = os.path.basename(path)
    try:
        obj = {}
        with open(path, 'r') as f:
            obj = json.loads(f.read())

        text = preprocess_article(str(obj['text'].encode('ascii', 'ignore')))

        with db.db.atomic():
            (author, _) = db.Author.get_or_create(name=obj["authors"][0]) #TODO
            article = db.Article.create(author=author,
                                        date=datetime.strptime(obj['date'], "%Y%m%d").date(),
                                        title=obj['title'], content=text, source=obj['url'])
            for t in obj['tickers']: # maps relation of tickers to article
                (stock, _) = db.Stock.get_or_create(ticker=t, name=t)
                sa = db.StockArticle.create(stock=stock, article=article)

        # move to handled location
        os.rename(path, os.path.join(handled_path, base_name))

    except Exception as e:
        logging.error(e)
        os.rename(path, os.path.join(error_path, base_name))

class ArticleHandler(FileSystemEventHandler):
    """ File event handler which loads new articles into the DB """
    def __init__(self, handled_path, error_path):
        self.handled_path = handled_path
        self.error_path = error_path

    def on_created(self, event):
        if type(event) is FileCreatedEvent:
            load_article(event.src_path, self.handled_path, self.error_path)

def load_prexisting(path, handled_path, error_path):
    """ loads all articles in a given path since the observer only handles changes """
    for f in [_ for _ in os.listdir(path) if os.path.isfile(os.path.join(path, _))]:
        load_article(os.path.join(path, f), handled_path, error_path)

def main():
    args = parse_args()
    config = common.load_config_file(args.config)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    event_handler = ArticleHandler(config['done_prefix'], config['error'])
    common.create_dir(config["done_prefix"])
    common.create_dir(config["error"])

    observer = Observer()
    for path in config['watch']:
        load_prexisting(path, config['done_prefix'], config['error'])
        observer.schedule(event_handler, path)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
