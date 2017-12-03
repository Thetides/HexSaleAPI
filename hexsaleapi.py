import logging
import datetime
import json
from urllib.parse import urlencode
import requests


default_date = datetime.datetime.today().strftime('%Y-%m-%d')



def _url(path):
    """ API URL for hexsales.net
        
        Args:
            path - string - API path 
        Returns:
            A string that is the URL of  

    """
    return 'https://api.hexsales.net/v1' + path


def get_articles():
    """Gives you a list of all (known**) articles there are official AH sales for


        Returns:
            This function returns a dictionary object
    """
    try:
        response = requests.get(_url('/articles'))
        logging.info(response)
        data = response.content.decode("utf-8")
        articles = json.loads(data)
        return articles
    except Exception:
        raise Exception("An error has occurred while getting article")

def post_search(article, uuid, rarity, hex_type, hex_set, limit=25, offset=0, contains=False):
    """Let's you search for all articles with certain attribute values.

        Args:
            name - String - The name of the searched article.
            uuid - String - The official game uuid of the searched article.
            rarity - String - The rarity of the searched articles.
            type - String - The type of the searched articles.
            set - String - The set of the searched articles. Check /v1/sets for a list of all values.
            limit - Integer - Limits the quantity of returned results (default: 25).
            offset - Integer - Skips offset articles before returning (default: 0).
            contains - Boolean - If true, all articles with a name containing name will be searched (case insensitive), 
            instead of exact matches (case sensitive); defaults to true

        Returns:
             An array of information stored in a dict
    """
    try:
        response = requests.post(_url('/articles/search'), json={"name":article, 
                                                                 "uuid":uuid, 
                                                                 "rarity":rarity, 
                                                                 "type":hex_type,  
                                                                 "limit":limit, 
                                                                 "offset":offset, 
                                                                 "contains":contains
                                                                 }
                                                                 )
        logging.info(response)
        data = response.content.decode("utf-8")
        search_response = json.loads(data)
        return search_response
    except Exception:
        raise Exception("An error has occurred while searching for {}".format(article))

def get_articles_uuid(uuid):
    """ This function Gives you details for a specific article (currently it's name, game uuid, rarity,
         type (cards, equipment, packs, …) and set it belongs to)
    
        Args:
            uuid - String - The official game uuid of the searched article.
        
        Returns:
            Returns all data for the article with uuid. This is stored in a dict.
    
    """
    try:
        response = requests.get(_url('/articles/{}'.format(uuid)))
        logging.info(response)
        data = response.content.decode("utf-8")
        article = json.loads(data)
        return article
    except Exception:
        raise Exception("An error has occurred while looking up UUID:{}".format(uuid))

def get_articles_histories(uuid):
    """ Returns a JSON object with daily summary data for each currency for the article :uuid. 
    If the article :name does not exist, a 404 response is returned. 
    Note that all properties (average, median, etc are abbreviated, as opposed to the long form in summary data)
    
        Args:
            uuid - String - The official game uuid of the searched article.
        Returns:
            daily summary data for each currency  for articles uuid. This is stored in a dict.
    
    """
    try:
        response = requests.get(_url('/articles/{}/histories'.format(uuid)))
        logging.info(response)
        data = response.content.decode("utf-8")
        article_history = json.loads(data)
        return article_history
    except Exception:
        raise Exception("An error has occurred while getting history for UUID:{}".format(uuid))

def get_articles_summaries(uuid):
    """Contains a summarized sales for the specified article :uuid for a specified timespan for each currency.
        Note that all properties (average, median, etc are written out, as opposed to the short form in history data).
        Args:
            uuid - String - The official game uuid of the searched article.
        Returns:
            Returns a JSON object containing summarizing sales for the specified article :uuid for a specified timespan for each currency. This is stored in a dict.
    """
    try:
        response = requests.get(_url('/articles/{}/summaries'.format(uuid)))
        logging.info(response)
        data = response.content.decode("utf-8")
        article_summary = json.loads(data)
        return article_summary
    except Exception:
       raise Exception("An error has occurred while getting articel summary for UUID:{}".format(uuid)) 

# Histories

def get_histories(name, uuid, rarity, hex_type, hex_set, currency,start=default_date, end=default_date):
    """Allows you to find historical data for more than one article. 
        Args:
            start - String - Starting date of the timespan you want a history for (default: NOW() - 3 months)
            end - String - Ending date of the timespan you want a history for (default: NOW())
            name - String - The name of the searched article.
            uuid - String - The official game uuid of the searched article.
            rarity - String - The rarity of the searched articles.
            type - String - The type of the searched articles.
            set - String - The set of the searched articles. Check /v1/sets for a list of all values.
            currency - String - The currency to filter upon.
        Returns:
            This returns a history of all sales for the card searched. This data is stored in a dict.
            
    """
    payload = {"start":start,
               "end":end,
               "name":name,
               "uuid":uuid,
               "rarity":rarity,
               "type":hex_type,
               "set":hex_set,
               "currency":currency  
              }
    try:
        response = requests.get(_url('/histories'+ urlencode(payload)))
        logging.info(response)
        data = response.content.decode("utf-8")
        histories = json.loads(data)
        return histories
    except Exception:
        raise Exception("An error has occurred while getting history")

# Sets

def get_sets():
    """ Get the list of Hex: Shards of Fate sets.

        Returns:    
            Array of all set string values
    """
    try:
        response = requests.get(_url('/sets'))
        logging.info(response)
        data = response.content.decode("utf-8")
        hex_sets = data
        return hex_sets
    except Exception:
        raise Exception("An error has occurred while getting sets")

# Stats

def get_mostsold(start=default_date, 
                 end=default_date, 
                 limit=30):
    """Will return a dict of 'gold' and 'platinum' most sold items from the auction house 

        Args:
            start - String - The start of the timespan to aggregate on (default: today - days)
            end - String - The end of the timespan to aggregate on (default: today)
            limit - Integer - The number of articles with most sales to return (default: 30)
        Returns:
            A dict with an array or most sold articles
    
    """
    payload = {
        "start":start,
        "end":end,
        "limit":limit
    }
    try:
        response = requests.get(_url('/stats/mostsold' + urlencode(payload)))
        logging.info(response)
        data = response.content.decode("utf-8")
        mostsold = json.loads(data)
        return mostsold
    except Exception:
        raise Exception("An error has occurred while getting most sold")


def get_pricelist():
    """ Gets a collection of summary data for each article for each currency. 
    Basically it is like /v1/articles/:uuid/summaries but for all articles and for different timespans at once. Ideally you want to use this to calculate prices of decks/collections of articles.
    The current timespans are 1, 2, 3, 6, 7, 8, 13, 14, 15 and 30 days.

        Returns:
            A dict of summary data for each article for each currency
    """
    try:
        response = requests.get(_url('/stats/pricelist'))
        logging.info(response)
        data = response.content.decode("utf-8")
        pricelist = json.loads(data)
        return pricelist
    except Exception:
        raise  Exception("An error has occurred while getting a price list")

# Summaries

def get_summaries(name, uuid, rarity, hex_type, hex_set, currency, start=default_date, end=default_date):
    """ Lets you find summarizing data for more than one article.

        Args:
            start - String - Starting date of the timespan you want a history for (default: NOW() - 3 months)
            end - String - Ending date of the timespan you want a history for (default: NOW())
            name - String - The name of the searched article.
            uuid - String - The official game uuid of the searched article.
            rarity - String - The rarity of the searched articles.
            type - String - The type of the searched articles.
            set - String - The set of the searched articles. Check /v1/sets for a list of all values.
            currency - String - The currency to filter upon.
        Returns:
            A dict of summarized sales for defined search criteria
    """
    payload = {
        "start":start,
        "end":end,
        "name":name,
        "uuid":uuid,
        "rarity":rarity,
        "type":hex_type,
        "set":hex_set,
        "currency":currency
    }
    try:
        response = requests.get(_url('/summaries?' + urlencode(payload)))
        logging.info(response)
        data = response.content.decode("utf-8")
        summaries = json.loads(data)
        return summaries
    except Exception:
        raise Exception("An error has occurred while getting summaries.")