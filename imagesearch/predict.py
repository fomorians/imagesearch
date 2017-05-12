"""
Uses trained model for predictions and saves to file.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import argparse, os, json, time
import tensorflow as tf

from tqdm import tqdm
from annoy import AnnoyIndex
from imagesearch.inputs import generate_input_fn
from imagesearch.model import model_fn

def get_metadata(features_length, lookup_index):
    metadata = {
        'timestamp': time.time(),
        'features_length': features_length,
        'filenames': lookup_index
    }
    return metadata

def get_indicies(features_length, predictions_list):
    lookup_index = []
    annoy_index = AnnoyIndex(features_length)

    for i in tqdm(range(len(predictions_list))):
        prediction = predictions_list[i]
        flattened_image = prediction['encoded_image'].flatten()

        annoy_index.add_item(i, flattened_image)
        lookup_index.append(prediction['filename'].split("/")[-1])

    return lookup_index, annoy_index

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

    predictions_list = list(predictions_iter)
    features_length = len(predictions_list[0]['encoded_image'].flatten())

    print("Indexing {} images".format(len(predictions_list)))

    lookup_index, annoy_index = get_indicies(features_length, predictions_list)

    # build and save metadata
    metadata = get_metadata(features_length, lookup_index)
    with open('{}/metadata.json'.format(args.out_dir), 'w') as outfile:
        json.dump(metadata, outfile)

    print("Starting Annoy build process")
    # build and save annoy trees
    annoy_index.build(10) # 10 trees
    annoy_index.save('{}/index.ann'.format(args.out_dir))

    print("Successfully indexed {} images".format(len(lookup_index)))

if __name__ == '__main__':
    main()
