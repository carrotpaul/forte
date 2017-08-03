from celery import Celery
from lib.download import execute_dl
import os

_worker = Celery(__name__, broker=os.environ.get('CELERY_BROKER_URL'))

@_worker.task
def download_from_source(source):
    execute_dl(source)
