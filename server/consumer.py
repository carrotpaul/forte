from kafka import KafkaConsumer
from kafka.errors import KafkaError
from auth.authenticate import AuthenticationException, authenticate
from task.download import execute_dl
# from task.upload import execute_up
from pprint import pprint
import os, time, json

class KafConsumer(object):
    def __init__(self, servers, topic, max_backoff = 10):
        backoff = 0.5

        while (backoff < max_backoff):
            try:
                self.consumer = KafkaConsumer(topic,
                    group_id='forte-server',
                    bootstrap_servers=servers)

                print ("Established connection to Kafka with brokers %s" % servers)
                return
            except KafkaError as exception:
                backoff = backoff * 2

                plural_string = "second" if backoff == 1 else "seconds"
                print ("Kafka is not ready yet: %s. Retrying in %d %s..." %
                    (exception, backoff, plural_string))

                time.sleep(backoff)

        raise SystemExit("Could not connect to Kafka within timeout. Aborting.")

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
                authenticate(loaded_args['auth_token'])
                downloaded_file = execute_dl(loaded_args['url'])
                print ("File %s downloaded successfully." % (downloaded_file))
                # execute_up(downloaded_file)
            except AuthenticationException:
                print ("Dropping unauthenticated event: %s" % message.value)
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
