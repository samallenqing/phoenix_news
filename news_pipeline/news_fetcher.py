"""News fetcher: dedupe etc."""
import json
import os
import sys

from newspaper import Article

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

from cloud_amqp_client import CloudAMQPClient

with open('../config.json') as config_data:
    cfg = json.load(config_data)

DEDUPE_NEWS_TASK_QUEUE_URL = cfg['amqp']['DEDUPE_NEWS_TASK_QUEUE']['url']
DEDUPE_NEWS_TASK_QUEUE_NAME = cfg['amqp']['DEDUPE_NEWS_TASK_QUEUE']['queue_name']

SCRAPE_NEWS_TASK_QUEUE_URL = cfg['amqp']['SCRAPE_NEWS_TASK_QUEUE']['url']
SCRAPE_NEWS_TASK_QUEUE_NAME = cfg['amqp']['SCRAPE_NEWS_TASK_QUEUE']['queue_name']

SLEEP_TIME_IN_SECONDS = 5

DEDUPE_NEWS_QUEUE_CLIENT = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
SCRAPE_NEWS_QUEUE_CLIENT = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
    """Handle received message"""
    if msg is None or not isinstance(msg, dict):
        print('Message is broken.')
        return

    task = msg
    text = None
    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text
    DEDUPE_NEWS_QUEUE_CLIENT.send_message(task)


def run():
    """Run news fetcher"""
    while True:
        if SCRAPE_NEWS_QUEUE_CLIENT is not None:
            msg = SCRAPE_NEWS_QUEUE_CLIENT.get_message()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass
            SCRAPE_NEWS_QUEUE_CLIENT.sleep(SLEEP_TIME_IN_SECONDS)


if __name__ == '__main__':
    run()
