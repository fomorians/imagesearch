"""
Trains and evaluates model
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import tensorflow as tf

from imagesearch.inputs import generate_input_fn
from imagesearch.model import model_fn

def generate_experiment_fn(train_files, eval_files, batch_size, num_epochs):

    "Define and return `_experiment_fn` for use with `learn_runner.run`."
    def _experiment_fn(output_dir):

        train_input_fn = generate_input_fn(
            file_pattern=train_files,
            batch_size=batch_size,
            num_epochs=num_epochs,
            shuffle=True)

        eval_input_fn = generate_input_fn(
            file_pattern=eval_files,
            batch_size=batch_size,
            num_epochs=1,
            shuffle=False)

        run_config = tf.contrib.learn.RunConfig(
            save_summary_steps=1000,
            save_checkpoints_steps=1000,
            save_checkpoints_secs=None,
            gpu_memory_fraction=0.8)

        estimator = tf.contrib.learn.Estimator(
            model_dir=output_dir,
            model_fn=model_fn,
            config=run_config)

        eval_metrics = {
            'rmse': tf.contrib.learn.MetricSpec(
                metric_fn=tf.metrics.root_mean_squared_error,
                prediction_key='decoded_image',
                label_key='image')
        }

        experiment = tf.contrib.learn.Experiment(
            estimator=estimator,
            train_input_fn=train_input_fn,
            eval_input_fn=eval_input_fn,
            export_strategies=None,
            train_steps=None,
            eval_steps=None,
            eval_metrics=eval_metrics)
        return experiment

    return _experiment_fn
