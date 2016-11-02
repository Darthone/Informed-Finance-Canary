#!/usr/bin/env python

import feedparser
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader

def render_template(data, template, filter=None):
    env = Environment(loader=FileSystemLoader(''))

    if filter is not None:
        for key, value in filter.iteritems():
            env.filters[key] = value

    template = env.get_template(template)
    return template.render(feed=data).encode('utf-8')

def main():

    feed = feedparser.parse('http://feeds.reuters.com/reuters/technologyNews')
    json = render_template(feed.entries, 'json.tmpl')
    with open('news.json','a') as output:
        output.write(json)

if __name__== '__main__':
    main()
