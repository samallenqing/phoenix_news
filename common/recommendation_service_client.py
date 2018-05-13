"""Recommendation service client"""
from jsonrpclib.jsonrpc import ServerProxy
from json import load

with open('../config.json') as config_data:
    cfg = load(config_data)

URL = cfg['rpc_client']['recommendation_service']['url']
client = ServerProxy(URL)


def get_preference_for_user(user_id):
    """Get user preference"""
    preference = client.get_preference_for_user(user_id)
    print("Preference list:%s" % str(preference))
    return preference
