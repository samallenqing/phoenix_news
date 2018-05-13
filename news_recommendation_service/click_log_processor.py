"""Click log processor"""
import json
import os
import sys

import news_classes

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
from cloud_amqp_client import CloudAMQPClient

with open('../config.json') as config_data:
    cfg = json.load(config_data)

LOG_CLICKS_TASK_QUEUE_URL = cfg['amqp']['LOG_CLICKS_TASK_QUEUE']['url']
LOG_CLICKS_TASK_QUEUE_NAME = cfg['amqp']['LOG_CLICKS_TASK_QUEUE']['queue_name']

NUM_OF_CLASSES = 8
INITIAL_P = 1.0 / NUM_OF_CLASSES
ALPHA = 0.2

PREFERENCE_MODEL_TABLE_NAME = "user_preference_model"
NEWS_TABLE_NAME = "news"

SLEEP_TIME_IN_SECONDS = 1

CLOUD_AMQP_CLIENT = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)


def handle_message(message):
    """Process message"""
    if message is None or not isinstance(message, dict):
        print('message is broken')
        return

    if 'userId' not in message or 'newsId' not in message or 'timestamp' not in message:
        return

    userId = message['userId']
    newsId = message['newsId']

    database = mongodb_client.get_db()
    model = database[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': userId})

    if model is None:
        print("Creating preference model for new user: %s" % userId)
        new_model = {'userId': userId}
        preference = {}
        for i in news_classes.classes:
            preference[i] = float(INITIAL_P)
        new_model['preference'] = preference
        model = new_model

    news = database[NEWS_TABLE_NAME].find_one({'digest': newsId})

    if news is None or 'class' not in news or news['class'] not in news_classes.classes:
        print('Skipping processing...')
        return

    click_class = news['class']

    old_p = model['preference'][click_class]
    model['preference'][click_class] = float((1 - ALPHA) * old_p + ALPHA)

    for i, prob in model['preference'].items():
        if not i == click_class:
            model['preference'][i] = float((1 - ALPHA) * model['preference'][i])

    database[PREFERENCE_MODEL_TABLE_NAME].replace_one({'userId': userId}, model, upsert=True)


def run():
    while True:
        if CLOUD_AMQP_CLIENT is not None:
            message = CLOUD_AMQP_CLIENT.get_message()
            if message is not None:
                # Parse and process the task
                try:
                    handle_message(message)
                except Exception as e:
                    print(e)
                    pass
            CLOUD_AMQP_CLIENT.sleep(SLEEP_TIME_IN_SECONDS)


if __name__ == "__main__":
    run()
