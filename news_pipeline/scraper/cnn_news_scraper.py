"""CNN scraper"""
import os
import random
import requests
from lxml import html
# pylint: disable=trailing-whitespace
GET_CNN_NEWS_XPATH = """//p[contains(@class, 'zn-body__paragraph')]//text() | //div[contains(@class, 
'zn-body__paragraph')]//text() """

USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])

random.shuffle(USER_AGENTS)


def _get_header():
    """Get header of user agents"""
    user_agent = random.choice(USER_AGENTS)
    headers = {
        "User-Agent": user_agent
    }
    return headers


def extract_news(news_url):
    """Extract news info"""
    session_request = requests.session()
    response = session_request.get(news_url, headers=_get_header())
    news = {}

    try:
        tree = html.fromstring(response.content)
        news = tree.xpath(GET_CNN_NEWS_XPATH)
        news = ''.join(news)
    # pylint: disable=broad-except
    except Exception:
        return {}

    return news
