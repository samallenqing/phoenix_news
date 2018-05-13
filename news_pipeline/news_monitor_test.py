"""Basic test for news monitor"""
from unittest.mock import MagicMock
import news_monitor

MESSAGE_LIST = [{'author': 'Katie Zezima, Katie Zezima',
                 'title': 'Inns, ammunition, family and politics',
                 'description': 'Tens of thousands attend the meehow.',
                 'url': 'https://www.washingtonpost.com/national/inside-the-nras-anl',
                 'urlToImage': 'https://www.washingtonpost.com/resiW54CQRQI6RL2GWHLNYDM37Y.jpg',
                 'publishedAt': '2018-05-05T08:25:00Z', 'source': 'the-washington-post',
                 'digest': 'fasdfsadf8cf'},
                {'author': 'Katie Zezima, Katie Zezima',
                 'title': 'Inside the NRA’s annus, ammunition, family and politics',
                 'description': 'Tens of enthusiasts flock to massive trade show.',
                 'url': 'https://www.washind-politics/2018/story.html',
                 'urlToImage': 'https://www.wasd-was2GWHLNYDM37Y.jpg',
                 'publishedAt': '2018-05-05T08:25:00Z', 'source': 'the-washington-post',
                 'digest': 'f6aasdfpokpf72fc8cf'},
                {'author': 'Katie Zezima, Katie Zezima',
                 'title': 'Inside asdf ammunition, family and politics',
                 'description': 'Tens of tsive trade show.',
                 'url': 'hnras-annual-meeting-guns-ammuna9ac0a_story.html',
                 'urlToImage': 'https://www.wapjrRQI6RL2GWHLNYDM37Y.jpg',
                 'publishedAt': '2018-05-05T08:25:00Z', 'source': 'the-washington-post',
                 'digest': 'f6a223123oj3ad20f72fc8cf'}]


def basic_test():
    """Basic test for news monitor"""
    news_list_1 = MagicMock(return_value=[])
    res = news_monitor.run_with_test(news_list_1())
    assert res == 0
    news_list_2 = MagicMock(return_value=MESSAGE_LIST)
    res = news_monitor.run_with_test(news_list_2())
    assert res == 3
    print("Test Passed!")


if __name__ == '__main__':
    basic_test()
