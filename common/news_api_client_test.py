"""Test news api client"""
import news_api_client as client


def test_basic():
    """Basic test"""
    news = client.getNewsFromSource()
    print(news)
    assert news is not None
    news = client.getNewsFromSource(sources=['cnn'], sortBy='top')
    assert news is not None
    print('Test passed!')


if __name__ == '__main__':
    test_basic()
