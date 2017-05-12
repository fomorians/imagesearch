"""
Helper script to perform data preprocessing.
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from fnmatch import fnmatch

import argparse, os
import shutil

def main():
    "Entrypoint for data preprocessing."

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input-dir',
        help='Input file directory',
        required=True)
    parser.add_argument(
        '--output-dir',
        help='Output file directory',
        required=True)
    parser.add_argument(
        '--input-ext',
        help='Input file extension')
    parser.add_argument(
        '--output-ext',
        help='Output file extension')
    parser.add_argument(
        '--limit',
        help='Limits number of files copied',
        default=-1,
        type=int)

    args = parser.parse_args()
    limit = args.limit

    for path, subdirs, files in os.walk(args.input_dir):
        for idx, input_name in enumerate(files):
            if not args.input_ext or fnmatch(input_name, '*.{}'.format(args.input_ext)):
                output_name = input_name
                if args.output_ext:
                    base_name = output_name.split('.')[0]
                    output_name = '{}.{}'.format(base_name, args.output_ext)

                input_path = os.path.join(path, input_name)
                output_path = os.path.join(args.output_dir, output_name)

                shutil.copyfile(input_path, output_path)
                print("idx: {}, old: {}, new: {}".format(idx, input_path, output_path))

            if idx >= limit - 1: break
        if idx >= limit - 1: break

if __name__ == '__main__':
    main()
