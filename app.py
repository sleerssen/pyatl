from flask import Flask
from flask import request
app = Flask(__name__)

@app.route("/pyatl", methods=['POST', 'GET'])
def pyatl():
    print(request.args)
    print(request.data)
    print(request.form)
    return "Hello World!"

