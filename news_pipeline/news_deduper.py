"""News deduper"""
import datetime
import json
import os
import sys
from dateutil import parser
from sklearn.feature_extraction.text import TfidfVectorizer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client

from cloud_amqp_client import CloudAMQPClient

with open('../config.json') as config_data:
    cfg = json.load(config_data)

DEDUPE_NEWS_TASK_QUEUE_URL = cfg['amqp']['DEDUPE_NEWS_TASK_QUEUE']['url']
DEDUPE_NEWS_TASK_QUEUE_NAME = cfg['amqp']['DEDUPE_NEWS_TASK_QUEUE']['queue_name']

SLEEP_TIME_IN_SECONDS = 3

NEWS_TABLE_NAME = 'news'

SAME_NEWS_SIMILARITY_THRESHOLD = 0.9

CLOUD_AMQP_CLIENT = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
    """Handle message"""
    if msg is None or not isinstance(msg, dict):
        return
    task = msg
    text = task['text']
    if text is None:
        return

    published_at = parser.parse(task['publishedAt'])
    published_at_day_begin = datetime.datetime(published_at.year, published_at.month, published_at.day, 0, 0, 0, 0)
    published_at_day_end = published_at_day_begin + datetime.timedelta(days=1)

    database = mongodb_client.get_db()
    same_day_news_list = list(
        database[NEWS_TABLE_NAME].find({'publishedAt': {'$gte': published_at_day_begin, '$lt': published_at_day_end}}))

    if same_day_news_list is not None and len(same_day_news_list) > 0:
        documents = [news['text'] for news in same_day_news_list]
        documents.insert(0, text)

        tfidf = TfidfVectorizer().fit_transform(documents)
        pairwise_sim = tfidf * tfidf.T
        print(pairwise_sim)

        rows, _ = pairwise_sim.shape

        for row in range(1, rows):
            if pairwise_sim[row, 0] > SAME_NEWS_SIMILARITY_THRESHOLD:
                print("Duplicated news found. Ignore.")
                return

    task['publishedAt'] = parser.parse(task['publishedAt'])

    title = task['title']
    if title is not None:
        topic = news_topic_modeling_service_client.classify(title)
        task['class'] = topic

        database[NEWS_TABLE_NAME].replace_one({'digest': task['digest']}, task, upsert=True)


def run():
    """Start news deduper"""
    while True:
        if CLOUD_AMQP_CLIENT is not None:
            msg = CLOUD_AMQP_CLIENT.get_message()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass
        CLOUD_AMQP_CLIENT.sleep(SLEEP_TIME_IN_SECONDS)


if __name__ == '__main__':
    run()
