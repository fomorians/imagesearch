"""
Uses trained model for predictions and saves to file.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import argparse, os, json, time
import tensorflow as tf
import numpy as np

from tqdm import tqdm
from annoy import AnnoyIndex
from imagesearch.inputs import generate_input_fn
from imagesearch.model import model_fn

def main():
    "Entrypoint for predictions."

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--model-dir',
        help='Location to read checkpoints, summaries and models',
        required=True)
    parser.add_argument(
        '--files',
        help='Prediction files globstring',
        default="data/validation/*.jpg")
    parser.add_argument(
        '--batch-size',
        help='Batch size for evaluation steps',
        type=int,
        default=32)
    parser.add_argument(
        '--out-dir',
        help='Location to save indexes',
        default=".")
    parser.add_argument(
        '--tree-count',
        help='Forest of (n) trees. More trees == higher query precision.',
        type=int,
        default=10)

    args = parser.parse_args()

    input_fn = generate_input_fn(
        file_pattern=args.files,
        batch_size=args.batch_size,
        num_epochs=1,
        shuffle=False)

    estimator = tf.contrib.learn.Estimator(
        model_dir=args.model_dir,
        model_fn=model_fn,
        config=None)

    predictions_iter = estimator.predict(
        input_fn=input_fn,
        as_iterable=True)

    # drop out of tensorflow into regular python/numpy
    predictions_list = list(predictions_iter)
    features_length = len(predictions_list[0]['encoded_image'].flatten())

    # flatten embeddings so they play nice with annoy
    embeddings = np.zeros(shape=(len(predictions_list),
                                 features_length),
                          dtype=np.float64)
                          
    for i in tqdm(range(len(predictions_list))):
        embeddings[i] = predictions_list[i]['encoded_image'].flatten()

    # get the normalized embeddings so our search is more accurate
    embeddings_norm = embeddings / embeddings.max()

    # build search and filename indexes
    filenames = []
    nn_search = AnnoyIndex(features_length)
    for i in tqdm(range(len(predictions_list))):
        nn_search.add_item(i, embeddings_norm[i])
        filenames.append(predictions_list[i]['filename'].split("/")[-1])

    # build and save filename metadata
    with open('{}/metadata.json'.format(args.out_dir), 'w') as outfile:
        json.dump({
            'timestamp': time.time(),
            'features_length': features_length,
            'filenames': filenames
        }, outfile)

    # build and save search trees
    nn_search.build(args.tree_count)
    nn_search.save('{}/index.ann'.format(args.out_dir))

    print("Successfully indexed {} images".format(len(filenames)))

if __name__ == '__main__':
    main()
