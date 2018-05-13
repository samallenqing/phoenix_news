"""This is the backend server"""
import operations

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer


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


SERVER_HOST = 'localhost'
SERVER_PORT = 4040

RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))

RPC_SERVER.register_function(add, 'add')
RPC_SERVER.register_function(get_one_news, 'getOneNews')
RPC_SERVER.register_function(get_news_summaries_for_user, 'getNewsSummariesForUser')
RPC_SERVER.register_function(log_news_click_for_user, 'logNewsClickForUser')

print("Starting RPC server on %s: %d" % (SERVER_HOST, SERVER_PORT))

RPC_SERVER.serve_forever()
