import logging
import requests
import json


def _url(path):
    return 'https://api.hexsales.net/v1' + path

def get_articles():
    response = requests.get(_url('/articles'))
    data = response.content.decode("utf-8")
    articles = json.loads(data)
    return articles

def get_summaries():
    response = requests.get(_url('/summaries'))
    data = response.content.decode("utf-8")
    summaries = json.loads(data)
    return summaries

def get_histories():
    response = requests.get(_url('/histories'))
    data = response.content.decode("utf-8")
    histories = json.loads(data)
    return histories

def get_pricelist():
    response = requests.get(_url('/stats/pricelist'))
    data = response.content.decode("utf-8")
    pricelist = json.loads(data)
    return pricelist

def get_mostsold():
    """Will return a dict of 'gold' and 'platinum' most sold items from the auction house """
    response = requests.get(_url('/stats/mostsold'))
    data = response.content.decode("utf-8")
    mostsold = json.loads(data)
    return mostsold

def post_search(article, limit=25,offset=0):
    response = requests.post(_url('/articles/search'), json={"name":article,"limit":limit, "offset":offset})

def get_articles_uuid(uuid):
    response = requests.get(_url('/articles/{}'.format(uuid)))
    data = response.content.decode("utf-8")
    article = json.loads(data)
    return article

def get_articles_histories(uuid):
    response = requests.get(_url('/articles/{}/histories'.format(uuid)))
    data = response.content.decode("utf-8")
    article_history = json.loads(data)
    return article_history

def get_articles_summaries(uuid):
    response = requests.get(_url('/articles/{}/summaries'.format(uuid)))
    data = response.content.decode("utf-8")
    article_summary = json.loads(data)
    return article_summary

def get_sets():
    return requests.get(_url('/sets'))

#print(post_search('Runebind').content)