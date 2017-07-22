from __future__ import unicode_literals
from celery import Celery
import os, hashlib
import youtube_dl

_worker = Celery(__name__, broker=os.environ.get('CELERY_BROKER_URL'))

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

@_worker.task
def download_from_source(source):
    filename = hashlib.sha1(request_url).hexdigest()

    options = {
		'format': 'bestaudio/best',
        'logger' : MyLogger(),
		'outtmpl': 'downloads/' + filename + '.%(ext)s',
		'postprocessors': [{
	        'key': 'FFmpegExtractAudio',
	        'preferredcodec': 'mp3',
	        'preferredquality': '192',
	    }],
	}

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([source])
