"""This is setup for backend server"""
import json
import os
import pickle
import redis
import sys
from bson.json_util import dumps
from datetime import datetime

# pylint: disable=wrong-import-position
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
# pylint: disable=import-error
import mongodb_client
import recommendation_service_client

from cloud_amqp_client import CloudAMQPClient

with open('../config.json') as config_data:
    cfg = json.load(config_data)

LOG_CLICKS_TASK_QUEUE_URL = cfg['amqp']['LOG_CLICKS_TASK_QUEUE']['url']
LOG_CLICKS_TASK_QUEUE_NAME = cfg['amqp']['LOG_CLICKS_TASK_QUEUE']['queue_name']

REDIS_HOST = cfg['redis']['host']
REDIS_PORT = cfg['redis']['port']

NEWS_TABLE_NAME = "news"
NEWS_LIST_BATCH_SIZE = 10
NEWS_LIMIT = 200
USER_NEWS_TIME_OUT_IN_SECONDS = 60

CLOUD_AMQP_CLIENT = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT, db=0)


def get_one_news():
    """Get One News From Server"""
    print("getOneNews is called")
    database = mongodb_client.get_db('news')
    res = database['news'].find_one()
    return json.loads(dumps(res))


def add(num1, num2):
    """Simple add function"""
    print("function add is called with %d and %d" % (num1, num2))
    return num1 + num2


def get_news_summaries_for_user(user_id, page_num):
    """Get news summaries for user"""
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    sliced_news = []

    if redis_client.get(user_id) is not None:
        news_digests = pickle.loads(redis_client.get(user_id))
        sliced_news_digests = news_digests[begin_index:end_index]
        database = mongodb_client.get_db()
        sliced_news = list(database[NEWS_TABLE_NAME].find({'digest': {'$in': sliced_news_digests}}))
    else:
        database = mongodb_client.get_db()
        total_news = list(database[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIMIT))
        total_news_digest = [news['digest'] for news in total_news]

        redis_client.set(user_id, pickle.dumps(total_news_digest))
        redis_client.expire(user_id, USER_NEWS_TIME_OUT_IN_SECONDS)

        sliced_news = total_news[begin_index:end_index]

    preference = recommendation_service_client.get_preference_for_user(user_id)
    print("recommendation_service_client called!")
    top_preference = None

    if preference is not None and len(preference) > 0:
        top_preference = preference[0]

    for news in sliced_news:
        del news['text']
        if news['class'] == top_preference:
            news['reason'] = 'Recommend'
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'

    return json.loads(dumps(sliced_news))


def log_news_click_for_user(user_id, news_id):
    """Log user click news"""
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    CLOUD_AMQP_CLIENT.send_message(message)
