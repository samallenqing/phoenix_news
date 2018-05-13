"""Test for AMQP"""
import json
from cloud_amqp_client import CloudAMQPClient

with open('../config.json') as config_data:
    cfg = json.load(config_data)

CLOUDAMQP_URL = cfg['amqp']['test']['url']
QUEUE_NAME = cfg['amqp']['test']['queue_name']


def test_basic():
    """Test function"""
    client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

    send_msg = {'test': 'test'}
    client.send_message(send_msg)

    receive_msg = client.get_message()

    assert send_msg == receive_msg

    print('test passed.')


if __name__ == "__main__":
    test_basic()
