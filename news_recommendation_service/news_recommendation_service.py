"""NEWS recommendation server"""
import operator
import os
import sys

from json import load
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client

PREFERENCE_MODEL_TABLE_NAME = 'user_preference_model'

with open('../config.json') as config_data:
    cfg = load(config_data)

SERVER_HOST = cfg['rpc_server']['recommendation_server']['host']
SERVER_PORT = cfg['rpc_server']['recommendation_server']['port']



def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    """Determine two float is equal"""
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def get_preference_for_user(user_id):
    """Get user preference"""
    print("get_preference_for_user called")
    database = mongodb_client.get_db()
    model = database[PREFERENCE_MODEL_TABLE_NAME].find_one({'userId': user_id})

    if model is None:
        return []

    sorted_tuples = sorted(list(model['preference'].items()), key=operator.itemgetter(1), reverse=True)
    sorted_list = [x[0] for x in sorted_tuples]
    sorted_value_list = [x[1] for x in sorted_tuples]

    if is_close(float(sorted_value_list[0]), float(sorted_value_list[-1])):
        return []
    return sorted_list


RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(get_preference_for_user, 'get_preference_for_user')

print("Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT))

RPC_SERVER.serve_forever()
