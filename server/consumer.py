from kafka import KafkaConsumer
from kafka.errors import KafkaError
import os

class ForteConsumer(object):
    def __init__(self, servers, topic):
        self.consumer = KafkaConsumer(topic,
            group_id='forte',
            bootstrap_servers=servers)

    def consumer_events(self):
        print('Going to consume...')
        for message in self.consumer:
            print ("%s:%d:%d: key=%s value=%s" % (message.topic,
                message.partition,
                message.offset,
                message.key,
                message.value))

topic = os.environ.get('KAFKA_CONSUMER_TOPIC');
brokers = os.environ.get('KAFKA_CONSUMER_BROKERS');

consumer = ForteConsumer('localhost:9092', 'forte-download')
consumer.consumer_events();
