import email
from email.policy import default
from flask import Flask
from flask import request
import json
import pprint
import requests
import subprocess
import tempfile
import urllib

app = Flask(__name__)

def s3_downloader(url, destination, version=None):
    p = urllib.parse.urlparse(url)
    assert p.scheme.lower() == 's3', 'Invalid scheme for s3 in URL "{}"'.format(url)
    args = ['aws', 's3api', 'get-object', '--bucket', p.netloc, '--key', p.path.lstrip('/')]
    if version:
        args.extend(['--version-id', version])
    args.append(destination)
    subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

@app.route("/pyatl", methods=['POST', 'GET'])
def pyatl():
    data = json.loads(request.data)
    if 'SubscribeURL' in data:
        url = data['SubscribeURL']
        print('Subscribing to topic at {}'.format(url))
        requests.get(url)
        return ''
    else:
        message = json.loads(data['Message'])
        bucket_name = message['receipt']['action']['bucketName']
        object_key = message['receipt']['action']['objectKey']
        sender = message['mail']['source']
        url = 's3://{}/{}'.format(bucket_name, object_key)
        print('new message from {} at {}'.format(sender, url))
        with tempfile.NamedTemporaryFile() as t:
            print('downloading message to {}'.format(t.name))
            s3_downloader(url, t.name)
            t.seek(0)
            m = email.message_from_binary_file(t, policy=default)
            for p in m.walk():
                print('found mime part {}'.format(p.get_filename()))
                payload = p.get_payload(decode=True)
                print(payload)
        return ''

