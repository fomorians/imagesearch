"""
Basic Flask App
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from annoy_lookup import AnnoyLookup
from flask import Flask, render_template, jsonify, request, send_from_directory

lookup = AnnoyLookup()
app = Flask(__name__)

@app.route('/')
def index_route():
    results = lookup.get_multiple_neighbors(-1) # random starting image.
    return render_template('index.html', results=results)

@app.route('/nearest/<int:image_id>', methods=['GET'])
def get_nearest_html_route(image_id):
    results = lookup.get_multiple_neighbors(image_id)
    return render_template('index.html', results=results)

@app.route('/api/nearest/<int:image_id>', methods=['GET'])
def get_nearest_api_route(image_id):
    results = lookup.get_multiple_neighbors(image_id)
    return jsonify(results=results)

@app.route('/images/<path:path>')
def get_thumb_route(path):
    return send_from_directory('../data/validation/', path)

if __name__ == "__main__":
    app.run()
