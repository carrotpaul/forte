from flask import Flask, request, abort
from authenticate import authenticate
from worker import download_from_source

_servlet = Flask(__name__)

@_servlet.route('/download', methods=['POST'])
def download():
    json_data = request.get_json()
    if authenticate(json_data['token']):
        download_from_source.delay(json_data['url'])
        return 'Authentication successful\n'
    abort(401)
