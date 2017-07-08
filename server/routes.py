from authenticate import authenticate
from flask import Flask, request, abort
app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    password = request.get_json()['token']
    if authenticate(password):
        return 'Authentication successful'
    abort(401)
