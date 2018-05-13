"""Basic test for news deduper"""
import news_deduper
import os

import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client as client

MESSAGE_1 = {'author': 'Katie Zezima, Katie Zezima',
           'title': 'Inside the NRA’s annual meeting: Guns, ammunition, family and politics',
           'description': 'Tens of thousands attend the meeting in Dallas, where enthusiasts flock to massive trade show.',
           'url': 'https://www.washingtonpost.com/national/inside-the-nras-annual-meeting-guns-ammunition-family-and-politics/2018/05/05/e3435b20-5069-11e8-84a0-458a1aa9ac0a_story.html',
           'urlToImage': 'https://www.washingtonpost.com/resizer/0kRKkb9KlDmmfKl64RwpjrK1EFE=/1484x0/arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/ISPW54CQRQI6RL2GWHLNYDM37Y.jpg',
           'publishedAt': '2018-05-06T08:25:00Z', 'source': 'the-washington-post',
           'digest': 'f6a28aa12f90242e9a03ad20f72fc8cf',
           'text': 'this is test'}

MESSAGE_2 = {'author': 'Katie Zezima, Katie Zezima',
           'title': 'Inside the NRA’s annual meeting: Guns, ammunition, family and politics',
           'description': 'Tens of thousands attend the meeting in Dallas, where enthusiasts flock to massive trade show.',
           'url': 'https://www.washingtonpost.com/national/inside-the-nras-annual-meeting-guns-ammunition-family-and-politics/2018/05/05/e3435b20-5069-11e8-84a0-458a1aa9ac0a_story.html',
           'urlToImage': 'https://www.washingtonpost.com/resizer/0kRKkb9KlDmmfKl64RwpjrK1EFE=/1484x0/arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/ISPW54CQRQI6RL2GWHLNYDM37Y.jpg',
           'publishedAt': '2018-05-06T08:25:00Z', 'source': 'the-washington-post',
           'digest': 'f6a28aa12f90242e9a03ad20f72fc8cf',
           'text': 'this is test'}

MESSAGE_3 = {'author': 'Katie Zezima, Katie Zezima',
           'title': 'Inside the NRA’s annual meeting: Guns, ammunition, family and politics',
           'description': 'Tens of thousands attend the meeting in Dallas, where enthusiasts flock to massive trade show.',
           'url': 'https://www.washingtonpost.com/national/inside-the-nras-annual-meeting-guns-ammunition-family-and-politics/2018/05/05/e3435b20-5069-11e8-84a0-458a1aa9ac0a_story.html',
           'urlToImage': 'https://www.washingtonpost.com/resizer/0kRKkb9KlDmmfKl64RwpjrK1EFE=/1484x0/arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/ISPW54CQRQI6RL2GWHLNYDM37Y.jpg',
           'publishedAt': '2018-05-06T08:25:00Z', 'source': 'the-washington-post',
           'digest': 'f6a28aa12f90242e9a03ad20f72fc8cf',
           'text': 'this is test'}


def basic_test():
    """Basic test"""
    database = client.get_db()
    database.news.drop()
    assert database.news.count() == 0
    news_deduper.handle_message(MESSAGE_1)
    assert database.news.count() == 1
    news_deduper.handle_message(MESSAGE_2)
    assert database.news.count() == 1
    news_deduper.handle_message(MESSAGE_3)
    assert database.news.count() == 1
    database.news.drop()
    assert database.news.count() == 0
    print('Basic test for deduper passed.')


if __name__ == '__main__':
    basic_test()
