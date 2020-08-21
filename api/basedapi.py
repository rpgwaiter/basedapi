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

            parse = MediaInfo.parse(reqdir + '/' + name)
            print("Tracks: " + str(len(parse.tracks)))
            for track in parse.tracks:
                if track.track_type == 'Video':
                    d[i]['bitrate'] = track.bit_rate
                    d[i]['codec'] = track.codec

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
    api.run(debug=True, host="0.0.0.0", port=9001)
