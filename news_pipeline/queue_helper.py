"""Queue helper, clean queue data"""
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
# pylint: disable=wrong-import-position
# pylint: disable=import-error
from cloud_amqp_client import CloudAMQPClient

with open('../config.json') as config_data:
    cfg = json.load(config_data)

DEDUPE_NEWS_TASK_QUEUE_URL = cfg['amqp']['DEDUPE_NEWS_TASK_QUEUE']['url']
DEDUPE_NEWS_TASK_QUEUE_NAME = cfg['amqp']['DEDUPE_NEWS_TASK_QUEUE']['queue_name']

SCRAPE_NEWS_TASK_QUEUE_URL = cfg['amqp']['SCRAPE_NEWS_TASK_QUEUE']['url']
SCRAPE_NEWS_TASK_QUEUE_NAME = cfg['amqp']['SCRAPE_NEWS_TASK_QUEUE']['queue_name']


# pylint: disable=invalid-name
def clearQueue(quque_url, queue_name):
    """Clear message queues"""
    scrape_news_queue_client = CloudAMQPClient(quque_url, queue_name)

    num_of_messages = 0

    while True:
        if scrape_news_queue_client is not None:
            msg = scrape_news_queue_client.get_message()
            if msg is None:
                print("Cleared %d messages." % num_of_messages)
                return
            num_of_messages += 1


if __name__ == '__main__':
    clearQueue(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
    clearQueue(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
