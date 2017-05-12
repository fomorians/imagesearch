"""
Main training task.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os, json, random

from flask import Flask, render_template, jsonify, request, send_from_directory
from annoy import AnnoyIndex


### Util Functions
def get_json(filename):
    with open(filename) as json_data:
        data = json.load(json_data)
    return data

def get_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return -1

def validate_input(val):
    val = get_int(val)
    if val > -1 and val < limit:
        return val
    else:
        return random.randrange(limit)

def get_neighbors(image_id):
    results = []
    for item_id in ai.get_nns_by_item(image_id, 13):
        results.append({
            'id': item_id,
            'image': data['filenames'][item_id]
        })

    return results

### Setup & Data Inports
data = get_json('./data/metadata.json')
limit = len(data['filenames'])

ai = AnnoyIndex(data['features_length'])
ai.load('./data/index.ann')

### Start Flask App
app = Flask(__name__)

@app.route('/')
def index_route():
    initial_image_id = random.randint(1, 100)
    results = get_neighbors(initial_image_id)
    return render_template('index.html', results=results)

@app.route('/images/<path:path>')
def get_data_route(path):
    return send_from_directory('../', path)

@app.route('/nearest/<image_id>', methods=['GET'])
def get_nearest_html_route(image_id):
    image_id = validate_input(image_id)
    results = get_neighbors(image_id)
    return render_template('index.html', results=results)

@app.route('/api/nearest/<image_id>', methods=['GET'])
def get_nearest_api_route(image_id):
    image_id = validate_input(image_id)
    results = get_neighbors(image_id)
    return jsonify(results=results)

if __name__ == "__main__":
    app.run()
