"""News API Client"""
from json import loads, load
import requests

with open('../config.json') as config_data:
    cfg = load(config_data)

NEWS_API_ENDPOINT = cfg['news_api']['NEWS_API_ENDPOINT']
NEWS_API_KEY = cfg['news_api']['NEWS_API_KEY']
ARTICILES_API = cfg['news_api']['ARTICILES_API']

CNN = 'cnn'
DEFAULT_SOURCE = [CNN]
SORT_BY_TOP = 'top'


# pylint: disable=invalid-name
def _buildUrl(endPoint=NEWS_API_ENDPOINT, apiName=ARTICILES_API):
    """Set up client connection"""
    return endPoint + apiName


# pylint: disable=invalid-name
def getNewsFromSource(sources=None, sortBy=SORT_BY_TOP):
    """Get news from source"""
    if sources is None:
        sources = DEFAULT_SOURCE

    articles = []

    for source in sources:
        payload = {
            'apikey': NEWS_API_KEY,
            'source': source,
            'sortBy': sortBy
        }
        response = requests.get(_buildUrl(), params=payload)
        res_json = loads(response.content.decode('utf-8'))

        if res_json is not None and res_json['status'] == 'ok' and res_json['source'] is not None:
            for news in res_json['articles']:
                news['source'] = res_json['source']
                articles.extend((res_json['articles']))
    return articles
