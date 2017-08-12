from kafka import KafkaConsumer
from kafka.errors import KafkaError
from task.download import execute_dl
# from task.upload import execute_up
from pprint import pprint
import os, json

class KafConsumer(object):
    def __init__(self, servers, topic):
        self.consumer = KafkaConsumer(topic,
            group_id='forte-server',
            bootstrap_servers=servers)

    def consume_events(self):
        print('Starting the consumer...')
        for message in self.consumer:
            print ("Consuming event from topic:%s at offset:%s" % (
                message.topic, message.offset))

            # Weird way of type checkking, but we use a try/except block here
            # because we want to make sure that the message contains URL in it.
            # If not, log the message and drop it. We don't want to block up
            # other messages in Kafka.
            try:
                loaded_args = json.loads(message.value)
                downloaded_file = execute_dl(loaded_args['url'])
                print ("File %s downloaded successfully." % (downloaded_file))
                # execute_up(downloaded_file)
            except TypeError:
                pprint (json.loads(message.value))
            except ValueError as exception:
                print ("Dropping malformed event: %s, reason: %s" %
                    (message.value, exception))
            except KeyError as exception:
                print ("Dropping illegal event: %s, reason: %s" %
                    (message.value, exception))


topic = os.environ.get('KAFKA_CONSUMER_TOPIC');
brokers = os.environ.get('KAFKA_CONSUMER_BROKERS');

consumer = KafConsumer(brokers, topic)
consumer.consume_events();
