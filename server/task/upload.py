from __future__ import print_function
from gmusicapi import Musicmanager
from oauth2client.client import OAuth2Credentials
from pprint import pprint
import os, json, ast

total_retries = 5
backoff = 1

class ClientLoginException(Exception):
    pass

class UploadException(Exception):
    def __init__(self, message):
        self.message = message

class GoogleMusicClient(object):
    def __init__(self):
        self.client = Musicmanager()
        if not self.login(self.client):
            raise ClientLoginException

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.client.logout():
            print ("WARNING: Could not logout of Musicmanager")

    def login(self, client):
        print ("Connecting to Google Music....", end='')

        json_credentials = ""
        with open('/run/secrets/google_oauth_credentials', 'r') as raw_cred:
            cred_dict = ast.literal_eval(raw_cred.read())
            json_credentials = json.dumps(cred_dict, ensure_ascii=False)

        oauth_credentials = OAuth2Credentials.from_json(json_credentials)
        results = client.login(oauth_credentials)

        print ("Success" if results else "Failure")
        return results

def set_tags(filename, tags):
    return True

def execute(manager, filename, tags={}):
    print ("Adding tags to file %s" % filename)
    set_tags(filename, tags)

    print ("Uploading %s....." % filename, end='')

    retries = 0
    while ( retries <= total_retries ):
        uploaded, _, rejected = manager.client.upload(filename)

        if rejected and retries == total_retries:
            print ("Upload failed. Number of retries exceeded", attempts, total_retries)
            raise UploadException(rejected[filename])
        elif rejected:
            retries += 1
            print ("Upload failed. Retrying %s / %s", attempts, total_retries)
            time.sleep(backoff)
        else:
            print ("Success")
            break

