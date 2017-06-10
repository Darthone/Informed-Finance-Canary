#!/usr/bin/env python
"""
    Backend rest server for IFC

    How to use:
        - source the top level virtual environment and run
"""
import ujson as json

import pandas as pd
import random # for spoofing

from datetime import datetime
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict


from ifc.ta import get_series
from ifc.db import *
from ifc.nlp import tfidf

app = Flask(__name__)
CORS(app)
api = Api(app)

stock_date_range_parser = reqparse.RequestParser()
stock_date_range_parser.add_argument('symbol')
stock_date_range_parser.add_argument('start')
stock_date_range_parser.add_argument('end')


class Articles(Resource):
    """ returns related articles"""
    def get(self):
        args = stock_date_range_parser.parse_args()
        sym = Stock.get(ticker=args['symbol'])
        articles = StockArticle.select().join(Article).where(StockArticle.stock == sym, 
                           Article.date > datetime.strptime(args['start'], "%Y-%m-%d").date(), 
                           Article.date < datetime.strptime(args['end'], "%Y-%m-%d").date()).order_by(Article.date)
        corpusDict = {article.article_id : article.article.content for article in articles }
        corpus = corpusDict.values()
        corpusKeys = corpusDict.keys()
        tfidf_records = tfidf(corpus, corpusKeys, True)

        ret = {'data':[]}
        tmp = []
        dup = {}
        for a in articles:
            if not dup.has_key(a.article.title): # this is a hack, dupes should not exist in the first place
                #f = [x for x in ArticleFeature.select().join(Article).where(Article.title == a.article.title)]
                item = {
                    "author": a.article.author.name,
                    "date": a.article.date.strftime("%Y-%m-%d"),
                    "title": a.article.title,
                    "content": a.article.content,
                    "source": a.article.source,
                    "keywords": tfidf_records[a.article_id][1],
                }
                item["sentiment"] = {
                    "pos": tfidf_records[a.article_id][0]['positive'] * 10,
                    "net":  tfidf_records[a.article_id][0]['neutral']* 10,
                    "neg":  tfidf_records[a.article_id][0]['negative']* 10,
                    "comp": tfidf_records[a.article_id][0]['compound'] * 10
                    }
                tmp.append(item)
                dup[a.article.title] = ""
        ret['data'] = list(reversed(tmp))
        return ret

def get_summary(start, end, sym):
    ret = {}
    return ret

def get_backtesting(start, end, data):
	#TODO 
    ret = {
        "price": data.df['Adj_Close'][len(data.df) - 1],
        "indicator": random.randint(1,5),
        "gross": 0.0,
        "numTrades": 1,
        "grossPercent": 5.8,
        }
    return ret

class StockData(Resource):
    """ returns stock data and calculations"""
    def get(self):
        stock_date_range_parser.add_argument('params')
        args = stock_date_range_parser.parse_args()
        calcs = json.loads(args['params'])

        x = get_series(args['symbol'], args['start'], args['end'])
        #x.run_calculations()
        cc = []
        for calc in calcs:
            t = calc['type']
            p = calc['param']
            if t == 'mavg':
                cc.append(x.calculate_mavg(p['window']))
            elif t == 'rsi':
                cc.append(x.calculate_rsi(p['window']))
            elif t == 'macd':
                cc.append('signal_' + str(p['signal']))
                cc.append(x.calculate_macd(**p))
            elif t == '':
                pass
                #TODO
                #x.calculate_mom()
                #x.calculate_rocr()
                #x.calculate_atr()
                #x.calculate_mfi()
                #x.calculate_obv()
                #x.calculate_cci()
                #x.calculate_trix()
                #x.calculate_adx()
        x.df = x.df.where((pd.notnull(x.df)), None) # cast Nan to Null
        jret = {
            'ohlc' : list(zip(x.df.epoch, x.df['Open'], x.df['High'], x.df['Low'], x.df['Adj_Close'])),
            'volume': list(zip(x.df.epoch, x.df['Volume'])),
            'columns': cc,
            'backtesting': get_backtesting(args['start'], args['end'], x)
        }
        for c in cc:
            jret[c] = list(zip(x.df.epoch, x.df[c]))
        return jret 

#
# Actually setup the Api resource routing here
#
api.add_resource(Articles, '/articles')
api.add_resource(StockData, '/stock')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
