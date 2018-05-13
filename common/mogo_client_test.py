"""Test case for mongodb"""
import mongodb_client as client


def test_basic():
    """Test function"""
    try:
        database = client.get_db('test')
        database.test.drop()
        assert database.test.count() == 0
        database.test.insert({"test": 1})
        assert database.test.count() == 1
        database.test.drop()
        assert database.test.count() == 0
        print('test_basic passed.')
    except AssertionError as err:
        print("test failed!\n")
        raise err


def test_basic2():
    """Test function"""
    try:
        database = client.get_db()
        print(database['news'].count())
        print('test_basic passed.')
    except AssertionError as err:
        print("test failed!\n")
        raise err


if __name__ == "__main__":
    test_basic()
    test_basic2()
