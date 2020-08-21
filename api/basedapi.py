# Broadcasts info in json
import json
import os
from itertools import islice
import time
import urllib.request

from pymediainfo import MediaInfo

from flask import Response, Flask
from flask_cors import CORS

#def getMediaInfo(file):


def generatejson(path="/Movies"):
    rootdir = "/mnt/public"
    reqdir = rootdir + path
    d = {'reqdir': reqdir}
    for (root, dir, files) in os.walk(reqdir):
        for i, name in zip(range(0, len(files)), sorted(files)):
            d[i] = {}
            d[i]['name'] = name
            print(MediaInfo.parse(reqdir + '/' + name))
        break
    return d


def spitjson():
    # Get json data
    d = generatejson()
    return json.dumps(d, indent=4)


# Flask Stuff
api = Flask(__name__)
CORS(api)


@api.route('/', methods=['GET'])
def getstatus():
    return Response(spitjson(), mimetype='application/json')


if __name__ == '__main__':
    api.run(debug=True, host="localhost", port=9001)
