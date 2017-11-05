import logging
import requests
import json


def _url(path):
    return 'https://api.hexsales.net/v1' + path

def get_articles():
    return requests.get(_url('/articles/'))

def get_summaries():
    return requests.get(_url('/summaries'))

def get_histories():
    return requests.get(_url('/histories'))

def get_pricelist():
    return requests.get(_url('/stats/pricelist'))

def get_mostsold():
    return requests.get(_url('/stats/mostsold'))

def post_search(article):
    return requests.post(_url('/articles/search'), json={"name":article})


print(post_search('Runebind').content)