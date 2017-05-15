"""
Model, loss, and optimization.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import tensorflow as tf

def encoder(inputs):
    "Progressivly reduces embedding space by downsampling."

    layer_1 = tf.layers.conv2d(
        inputs=inputs,
        kernel_size=3,
        strides=2,
        filters=16,
        padding='SAME',
        activation=tf.nn.relu) # 128
    layer_2 = tf.layers.conv2d(
        inputs=layer_1,
        kernel_size=3,
        strides=2,
        filters=32,
        padding='SAME',
        activation=tf.nn.relu) # 64
    layer_3 = tf.layers.conv2d(
        inputs=layer_2,
        kernel_size=3,
        strides=2,
        filters=64,
        padding='SAME',
        activation=tf.nn.relu) # 32
    layer_4 = tf.layers.conv2d(
        inputs=layer_3,
        kernel_size=3,
        strides=2,
        filters=128,
        padding='SAME',
        activation=tf.nn.relu) # 16
    layer_5 = tf.layers.conv2d(
        inputs=layer_4,
        kernel_size=3,
        strides=2,
        filters=256,
        padding='SAME',
        activation=tf.nn.relu) # 8
    layer_6 = tf.layers.conv2d(
        inputs=layer_5,
        kernel_size=3,
        strides=2,
        filters=512,
        padding='SAME',
        activation=tf.nn.relu) # 4
    return layer_6

def decoder(inputs):
    "Upsamples the embedding back to original size of the image."

    layer_1 = tf.layers.conv2d_transpose(
        inputs=inputs,
        kernel_size=3,
        strides=2,
        filters=512,
        padding='SAME',
        activation=tf.nn.relu) # 8
    layer_2 = tf.layers.conv2d_transpose(
        inputs=layer_1,
        kernel_size=3,
        strides=2,
        filters=256,
        padding='SAME',
        activation=tf.nn.relu) # 16
    layer_3 = tf.layers.conv2d_transpose(
        inputs=layer_2,
        kernel_size=3,
        strides=2,
        filters=128,
        padding='SAME',
        activation=tf.nn.relu) # 32
    layer_4 = tf.layers.conv2d_transpose(
        inputs=layer_3,
        kernel_size=3,
        strides=2,
        filters=64,
        padding='SAME',
        activation=tf.nn.relu) # 64
    layer_5 = tf.layers.conv2d_transpose(
        inputs=layer_4,
        kernel_size=3,
        strides=2,
        filters=32,
        padding='SAME',
        activation=tf.nn.relu) # 128
    layer_6 = tf.layers.conv2d_transpose(
        inputs=layer_5,
        kernel_size=3,
        strides=2,
        filters=3,
        padding='SAME',
        activation=tf.tanh) # 256
    return layer_6

def get_loss(decoded_image, labels, mode):
    "Return the loss function which will be used with an optimizer."

    loss = None
    if mode == tf.contrib.learn.ModeKeys.INFER:
        return loss

    loss = tf.losses.mean_squared_error(decoded_image, labels["image"])
    return loss

def get_train_op(loss, mode):
    "Return the trainining operation which will be used to train the model."

    train_op = None
    if mode != tf.contrib.learn.ModeKeys.TRAIN:
        return train_op

    global_step = tf.contrib.framework.get_or_create_global_step()

    train_op = tf.contrib.layers.optimize_loss(
        loss=loss,
        global_step=global_step,
        learning_rate=0.01,
        optimizer='Adam')

    return train_op

def model_fn(features, labels, mode):
    "Return ModelFnOps for use with Estimator."
    encoded_image = encoder(features["image"])
    decoded_image = decoder(encoded_image)

    loss = get_loss(decoded_image, labels, mode)
    train_op = get_train_op(loss, mode)

    predictions = {
        'encoded_image': encoded_image,
        'decoded_image': decoded_image,
    }

    if 'filename' in features:
        predictions['filename'] = features['filename']

    tf.summary.image('original', features['image'])
    tf.summary.image('decoded_image', decoded_image)

    return tf.contrib.learn.ModelFnOps(
        predictions=predictions,
        loss=loss,
        train_op=train_op,
        mode=mode)
