"""This is the backend server"""
import operations

from json import load
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

with open('../config.json') as config_data:
    cfg = load(config_data)

def get_one_news():
    """Get One News From Server"""
    return operations.get_one_news()


def add(num1, num2):
    """Simple add function"""
    return operations.add(num1, num2)


def get_news_summaries_for_user(user_id, page_num):
    """Paging of news"""
    print("get_news_summaries_for_user is called with %s and %s" % (user_id, page_num))
    return operations.get_news_summaries_for_user(user_id, page_num)


def log_news_click_for_user(user_id, news_id):
    """Log user news click"""
    print("log_news_click_for_user is called with %s and %s" % (user_id, news_id))
    operations.log_news_click_for_user(user_id, news_id)


SERVER_HOST = cfg['rpc_server']['backend_server']['host']
SERVER_PORT = cfg['rpc_server']['backend_server']['port']

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))

RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(get_one_news, 'getOneNews')
RPC_SERVER.register_function(get_news_summaries_for_user, 'getNewsSummariesForUser')
RPC_SERVER.register_function(log_news_click_for_user, 'logNewsClickForUser')

print("Starting RPC server on %s: %d" % (SERVER_HOST, SERVER_PORT))

RPC_SERVER.serve_forever()
