# Broadcasts info in json
import json
import os
from pymediainfo import MediaInfo
from flask import Response, Flask
from flask_cors import CORS
from flask_caching import Cache


def buildmediaobject(req):
    fullname = '/mnt/' + req
    tracks = MediaInfo.parse(fullname).tracks
    ret = {'req': fullname}

    for track in tracks:
        if track.track_type == 'Video':
            ret['video'] = {
                'bitrate': track.bit_rate,
                'codec': track.codec_id,
                'duration': track.duration,
                'width': track.width,
                'height': track.height,
                'aspect_ratio': track.display_aspect_ratio
                }
        # TODO: Add more media types here
    return json.dumps(ret, indent=4)


def buildlistingobject(path)   :
    rootdir = "/mnt/"
    reqdir = rootdir + path
    dirs = [f for f in os.listdir(reqdir) if os.path.isdir(os.path.join(reqdir, f))]
    files = [f for f in os.listdir(reqdir) if os.path.isfile(os.path.join(reqdir, f))]

    d = {
        'reqdir': reqdir,
        'dirs': {},
        'files': {}
         }

    for i, name in zip(range(len(dirs)), sorted(dirs)):
        fullname = reqdir + '/' + name
        d['dirs'][i] = {
            'name': name,
            'items': len(os.listdir(fullname))
        }

    for i, name in zip(range(len(files)), sorted(files)):
        fullname = reqdir + '/' + name
        d['files'][i] = {
            'name': name,
            'size': os.path.getsize(fullname),
        }

    return json.dumps(d, indent=4)


config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "simple", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 30
}

# Flask Stuff
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
CORS(app)


@app.route('/media/<path:req>', methods=['GET'])
@cache.cached(timeout=30)
def mediastatus(req):
    return Response(buildmediaobject(req), mimetype='application/json')


@app.route('/', methods=['GET'])
@app.route('/<path:req>', methods=['GET'])
@cache.cached(timeout=30)
def getlisting(req=''):
    return Response(buildlistingobject(req), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8836)