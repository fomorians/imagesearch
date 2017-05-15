"""
Annoy Helper Class
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os
import json
import random

from annoy import AnnoyIndex

class AnnoyLookup(object):

    def __init__(self, metadata_path='./data/metadata.json', annoy_path='./data/index.ann'):
        with open(metadata_path) as f:
            self._data = json.load(f)

        self._limit = len(self._data['filenames'])
        self._index = AnnoyIndex(self._data['features_length'])
        self._index.load(annoy_path)

    def get_neighbors(self, image_id, max_neighbors=13):
        results = []

        if image_id < 0 or image_id >= self._limit:
            image_id = random.randrange(self._limit)

        for item_id in self._index.get_nns_by_item(image_id, max_neighbors):
            results.append({
                'id': item_id,
                'image': self._data['filenames'][item_id]
            })
        return results
