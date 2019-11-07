from kafka import KafkaConsumer
from kafka.errors import KafkaError
from auth.authenticate import AuthenticationException, authenticate
from task import download, upload
from task.upload import ClientLoginException, UploadException
from pprint import pprint
import time, json, traceback, threading

class KafConsumer(object):
    def __init__(self, servers, topic, max_backoff = 10):
        backoff = 0.5

        print ('Starting the consumer....')

        while (backoff < max_backoff):
            try:
                self.consumer = KafkaConsumer(
                    topic,
                    group_id='forte-server',
                    bootstrap_servers=servers
                )

                print ("Established connection to Kafka with brokers %s" % servers)
                return
            except KafkaError as exception:
                backoff = backoff * 2

                plural_string = "second" if backoff == 1 else "seconds"
                print ("Kafka is not ready yet: %s. Retrying in %d %s..." %
                    (exception, backoff, plural_string))

                time.sleep(backoff)

        raise SystemExit("Could not connect to Kafka within timeout. Aborting.")

    def log_event(self, event, message):
        print (message)
        pprint (event)

    def task_execution(self, download_url, upload_manager):
        downloaded_file = download.execute(download_url)
        print("File %s downloaded successfully." % (downloaded_file))

        upload.execute(upload_manager, downloaded_file)

    def consume_events(self, upload_manager):
        print ("Polling for events....")
        for message in self.consumer:
            print ("[%s] Consuming event from partition:%s at offset:%s" % (
                message.topic, message.partition, message.offset))

            # Decrypt the JSON payload
            loaded_args = json.loads(message.value)

            try:
                # Authenticate the message.
                authenticate(loaded_args['auth_token'])
            except AuthenticationException:
                # We couldn't claim that this came from us. Drop the event.
                self.log_event(loaded_args, "Dropping unauthenticated event: ")

            # Now do the actual work in an Thread.
            # Note that (for now), we will treat the event as a fire and forget
            # task, so we won't be joining the thread.
            threading.Thread(
                target=task_execution,
                args=[loaded_args['url'], upload_manager]
            ).start()
