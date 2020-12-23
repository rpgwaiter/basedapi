# Broadcasts info in json
import json
import os
import random
from pymediainfo import MediaInfo
from flask import Response, Flask
from flask_cors import CORS
from flask_caching import Cache

apiver = '0.2'


class DirListing:
    def __init__(self, parent):  # 'listing' in this case is the full path to the dir
        self.dirs = [f for f in os.listdir(parent) if os.path.isdir(os.path.join(parent, f))]
        self.files = [f for f in os.listdir(parent) if os.path.isfile(os.path.join(parent, f))]



def build_media_object(req):
    fullname = os.getenv('FILEHOST_PATH') + req
    tracks = MediaInfo.parse(fullname).tracks
    ret = {
        'apiversion': apiver,
        'req': req
    }

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


def build_listing_object(req):
    fullpath = os.getenv('FILEHOST_PATH') + req
    if not os.path.exists(fullpath):
        return {}
    listing = DirListing(fullpath)

    ret = {
        'apiversion': apiver,
        'root': req,
        'dirs': {},
        'files': {}
    }

    for i, name in zip(range(len(listing.dirs)), sorted(listing.dirs)):
        fullname = fullpath + '/' + name
        ret['dirs'][i] = {
            'name': name,
            'items': len(os.listdir(fullname)), ## I think this slowed down results significantly
            'mtime': os.path.getmtime(fullname)
        }

    for i, name in zip(range(len(listing.files)), sorted(listing.files)):
        fullname = fullpath + '/' + name
        ret['files'][i] = {
            'name': name,
            'size': os.path.getsize(fullname),
            'mtime': os.path.getmtime(fullname)
        }

    return json.dumps(ret, indent=4)


def get_based_string():
    with open("./based.txt") as f:
        content = f.read().splitlines()

    return json.dumps({'message': random.choice(content)})


config = {
    "DEBUG": True,  # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 30
}

# Flask Stuff
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
CORS(app)


@app.route('/media/<path:req>', methods=['GET'])
@cache.cached(timeout=30)
def media_status(req):
    return Response(build_media_object(req), mimetype='application/json')


@app.route('/message', methods=['GET'])
def route_based_string():
    return Response(get_based_string(), mimetype='application/json')


@app.route('/', methods=['GET'])
@app.route('/<path:req>', methods=['GET'])
@cache.cached(timeout=30)
def get_listing(req=''):
    return Response(build_listing_object(req), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8836)
