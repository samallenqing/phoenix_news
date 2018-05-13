"""Create mongoDB client"""
import json
from pymongo import MongoClient

with open('../config.json') as json_data_file:
    cfg = json.load(json_data_file)

DB_NAME = cfg['mongoDB']['database']

try:
    CLIENT = MongoClient("%s:%d" % (cfg['mongoDB']['host'], cfg['mongoDB']['port']))
except Exception as e:
    print(e)


def get_db(database=DB_NAME):
    """Connect mongoDB database"""
    database = CLIENT[database]
    return database
