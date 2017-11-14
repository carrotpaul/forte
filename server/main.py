from consumer import KafConsumer
from task.upload import GoogleMusicClient
import os

topic = os.environ.get('KAFKA_CONSUMER_TOPIC');
brokers = os.environ.get('KAFKA_CONSUMER_BROKERS');

with GoogleMusicClient() as music_manager:
    consumer = KafConsumer(brokers, topic)
    consumer.consume_events(music_manager);
