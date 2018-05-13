"""News Monitor module"""
import datetime
import hashlib
import json
import sys
import os
import redis

# pylint: disable=wrong-import-position
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
# pylint: disable=import-error
import news_api_client
# pylint: disable=import-error
from cloud_amqp_client import CloudAMQPClient

with open('../config.json') as config_data:
    cfg = json.load(config_data)

SCRAPE_NEWS_TASK_QUEUE_URL = cfg['amqp']['SCRAPE_NEWS_TASK_QUEUE']['url']
SCRAPE_NEWS_TASK_QUEUE_NAME = cfg['amqp']['SCRAPE_NEWS_TASK_QUEUE']['queue_name']

SLEEP_TIME_IN_SECONDS = 10
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3

REDIS_HOST = cfg['redis']['host']
REDIS_PORT = cfg['redis']['port']

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

REDIS_CLIENT = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
CLOUD_AMQP_CLIENT = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


def run():
    """Start news monitor"""
    while True:
        news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)
        num_of_new_news = 0

        for news in news_list:
            news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()

            if REDIS_CLIENT.get(news_digest) is None:
                num_of_new_news = num_of_new_news + 1
                news['digest'] = news_digest

                if news['publishedAt'] is None:
                    news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

                REDIS_CLIENT.set(news_digest, 'True')
                REDIS_CLIENT.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

                CLOUD_AMQP_CLIENT.send_message(news)
        print("Fetched %d news." % num_of_new_news)

        CLOUD_AMQP_CLIENT.sleep(SLEEP_TIME_IN_SECONDS)


def run_with_test(news_list):
    """Start news monitor with test"""
    # news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)
    num_of_new_news = 0
    REDIS_CLIENT.flushall()
    for news in news_list:
        news_digest = hashlib.md5(news['title'].encode('utf-8')).hexdigest()

        if REDIS_CLIENT.get(news_digest) is None:
            num_of_new_news = num_of_new_news + 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            REDIS_CLIENT.set(news_digest, 'True')
            REDIS_CLIENT.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

    print("Fetched %d news." % num_of_new_news)
    return num_of_new_news


if __name__ == '__main__':
    run()
