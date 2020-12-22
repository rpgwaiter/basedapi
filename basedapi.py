# Broadcasts info in json
import json
import os
from pymediainfo import MediaInfo
from flask import Response, Flask
from flask_cors import CORS
from flask_caching import Cache

apiver = '0.2'


class DirListing:
    def __init__(self, listing):  # 'listing' in this case is the full path to the dir
        self._listing = listing

        @property
        def listing(self):
            return self._listing

        @listing.setter
        def listing(self, currentdir):
            self._listing = {
                'dirs': [f for f in os.listdir(self.currentdir) if os.path.isdir(os.path.join(self.currentdir, f))],
                'files': [f for f in os.listdir(self.currentdir) if os.path.isfile(os.path.join(self.currentdir, f))]}


def build_media_object(req):
    fullname = '/mnt/' + req
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
    rootdir = "/mnt/"
    fullpath = rootdir + req
    if not os.path.exists(fullpath):
        return {}
    listing = DirListing(fullpath).listing

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
            'items': len(os.listdir(fullname)),
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
def mediastatus(req):
    return Response(build_media_object(req), mimetype='application/json')


@app.route('/', methods=['GET'])
@app.route('/<path:req>', methods=['GET'])
@cache.cached(timeout=30)
def getlisting(req=''):
    return Response(build_listing_object(req), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8836)
