"""
Data input pipeline definition.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import tensorflow as tf

def generate_input_fn(file_pattern, batch_size, num_epochs=None, shuffle=False):
    "Return _input_fn for use with Experiment."

    def _input_fn():
        height, width, channels = [256, 256, 3]

        filename_tensor = tf.train.match_filenames_once(file_pattern)
        filename_queue = tf.train.string_input_producer(
            filename_tensor,
            num_epochs=num_epochs,
            shuffle=shuffle)

        reader = tf.WholeFileReader()
        filename, contents = reader.read(filename_queue)

        image = tf.image.decode_jpeg(contents, channels=channels)
        image = tf.image.resize_image_with_crop_or_pad(image, height, width)
        image_batch, filname_batch = tf.train.batch(
            [image, filename],
            batch_size,
            num_threads=4,
            capacity=50000)

        # Converts image from uint8 to float32 and rescale from 0..255 => 0..1
        # Rescale from 0..1 => -1..1 so that the "center" of the image range is roughly 0.
        image_batch = tf.to_float(image_batch) / 255
        image_batch = (image_batch * 2) - 1

        features = {
            "image": image_batch,
            "filename": filname_batch
        }

        labels = {
            "image": image_batch
        }

        return features, labels
    return _input_fn
