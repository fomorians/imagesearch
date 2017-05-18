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

        items, distances = self._index.get_nns_by_item(image_id,
                                                       max_neighbors,
                                                       include_distances=True)
        zipped = zip(items, distances)
        sorted_list = sorted(zipped, key=lambda (item_id, distance): distance)

        for item in sorted_list:
            item_id, distance = item
            results.append({
                'id': item_id,
                'image': self._data['filenames'][item_id]
            })

        return results

    def get_multiple_neighbors(self, image_id, set_count=3, offset=333, max_neighbors=36):
        results = []

        while set_count > 0:
            neighbors = self.get_neighbors(image_id, offset)
            image_id = neighbors[-1]['id']
            set_count = set_count - 1
            results.append(neighbors[:max_neighbors])

        return results
