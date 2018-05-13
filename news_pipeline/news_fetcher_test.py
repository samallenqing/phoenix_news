"""Basic test for news_fetcher"""
import news_fetcher

MESSAGE = {'author': 'Katie Zezima, Katie Zezima',
           'title': 'Inside the NRA’s annual meeting: Guns, ammunition, family and politics',
           'description': 'Tens of thousands attend the meeting in Dallas, where enthusiasts flock to massive trade show.',
           'url': 'https://www.washingtonpost.com/national/inside-the-nras-annual-meeting-guns-ammunition-family-and-politics/2018/05/05/e3435b20-5069-11e8-84a0-458a1aa9ac0a_story.html',
           'urlToImage': 'https://www.washingtonpost.com/resizer/0kRKkb9KlDmmfKl64RwpjrK1EFE=/1484x0/arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/ISPW54CQRQI6RL2GWHLNYDM37Y.jpg',
           'publishedAt': '2018-05-05T08:25:00Z', 'source': 'the-washington-post',
           'digest': 'f6a28aa12f90242e9a03ad20f72fc8cf'}


def news_fetcher_basic():
    """Basic Test"""
    response = 123
    while not response:
        response = news_fetcher.DEDUPE_NEWS_QUEUE_CLIENT.get_message()
    news_fetcher.handle_message(MESSAGE)
    response = news_fetcher.DEDUPE_NEWS_QUEUE_CLIENT.get_message()
    assert (response['source']) == 'the-washington-post'
    print('Test news_fetcher_basic passed!')


if __name__ == '__main__':
    news_fetcher_basic()
