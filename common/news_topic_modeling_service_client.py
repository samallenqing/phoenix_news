"""News topic modeling RPC client"""
from jsonrpclib.jsonrpc import ServerProxy
from json import load

with open('../config.json') as config_data:
    cfg = load(config_data)
URL = cfg['jsonrpc']['news_modeling_service']['URL']
client = ServerProxy(URL)


def classify(text):
    """Classify topic"""
    topic = client.classify(text)
    print("Topic: %s" % str(topic))
    return topic
