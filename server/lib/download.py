from __future__ import unicode_literals
import youtube_dl
import hashlib

class MyLogger(object):
    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg) 

def execute_dl(url):
    filename = hashlib.sha1(url).hexdigest()
    parent_path = os.path.dirname(os.getcwd())

    options = {
        'format': 'bestaudio/best',
        'logger' : MyLogger(),
        'outtmpl': parent_path + '/tmp/' + filename + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([source])
