"""Create AMQP Client"""
import json
import pika


class CloudAMQPClient:
    """AMQP client generator"""

    def __init__(self, cloud_amqp_url, queue_name):
        """Initialization AMQP Client"""
        print('Run AMQP Remote.')
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def send_message(self, message):
        """Send Message"""
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        print('[x] sent message to %s:%s' % (self.queue_name, message))

    def get_message(self):
        """Get Message from AMQP"""
        # pylint: disable=unused-variable
        method_frame, headers, body = self.channel.basic_get(self.queue_name)
        if method_frame:
            print("[x] Received message from %s: %s" % (self.queue_name, body))
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body.decode("utf-8"))
        print("No message returned.")
        return None

    def sleep(self, seconds):
        """Make AMQP sleep"""
        self.connection.sleep(seconds)
