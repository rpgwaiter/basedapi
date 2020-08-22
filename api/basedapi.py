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
    files = [f for f in os.listdir(reqdir) if os.path.isfile(os.path.join(reqdir, f))]
    for i, name in zip(range(len(files)), sorted(files)):
        fullname = reqdir + '/' + name
        d[i] = {}
        d[i]['name'] = name
        d[i]['size'] = os.path.getsize(fullname)
        parse = MediaInfo.parse(fullname)

        for i2, track in zip(range(len(parse.tracks)), parse.tracks):
            if track.track_type == 'Video':
                d[i]['video'] = {}
                d[i]['video']['bitrate'] = track.bit_rate
                d[i]['video']['codec'] = track.codec_id
                d[i]['video']['duration'] = track.duration
                d[i]['video']['width'] = track.width
                d[i]['video']['height'] = track.height
                d[i]['video']['aspect_ratio'] = track.display_aspect_ratio
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
