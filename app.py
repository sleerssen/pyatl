from flask import Flask
from flask import request
import json
import pprint

app = Flask(__name__)

@app.route("/pyatl", methods=['POST', 'GET'])
def pyatl():
    print(request.args)
    print(request.data)
    pprint.pprint(json.loads(request.data))
    print(request.form)
    return "Hello World!"

