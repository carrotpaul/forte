from __future__ import unicode_literals
import youtube_dl
import os, hashlib

class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

def execute_dl(url):
    parent_path = os.environ.get('YOUTUBEDL_DOWNLOAD_PATH') or os.getcwd()
    filename = hashlib.sha1(url).hexdigest()
    file_path = parent_path + '/tmp/' + filename

    options = {
        'format': 'bestaudio/best',
        'logger' : MyLogger(),
        'outtmpl': file_path + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        # If everything is successful, _download_retcode returns 0
        if not ydl.download([url]):
            return file_path + '.mp3'
