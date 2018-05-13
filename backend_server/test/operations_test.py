"""Test operations"""
import sys

import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import operations


def test_get_one_news_basic():
    """Test method getOneNews"""
    news = operations.get_one_news()
    print(news)
    assert news is not None
    print("Test passed!")


def test_get_news_summaries_for_user_basic():
    """Test test_get_news_summaries_for_user"""
    news_1 = operations.get_news_summaries_for_user('test', 1)
    assert news_1 is not None
    print('test_get_news_summaries_for_user_basic Passed!')


def test_get_news_summaries_for_user_pagination():
    """Test test_get_news_summaries_for_user pagination"""
    news_page_1 = operations.get_news_summaries_for_user('test', 1)
    news_page_2 = operations.get_news_summaries_for_user('test', 2)

    digests_page_1_set = set([news['digest'] for news in news_page_1])
    digests_page_2_set = set([news['digest'] for news in news_page_2])

    assert len(digests_page_1_set.intersection(digests_page_2_set)) == 0
    print('test_get_news_summaries_for_user_pagination passed!')


if __name__ == "__main__":
    test_get_one_news_basic()
    test_get_news_summaries_for_user_basic()
    test_get_news_summaries_for_user_pagination()
