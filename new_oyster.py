#! /usr/bin/env python3
from __future__ import print_function

import argparse
import datetime
import os
import sys
import json
import uuid
import logging

def get_year():
    now = datetime.datetime.now()
    return now.year

def writable_directory(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(
            'not an existing directory: {}'.format(path))
    if not os.access(path, os.W_OK):
        raise argparse.ArgumentTypeError(
            'not a writable directory: {}'.format(path))
    return path

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create new cmd-oyster.')
    parser.add_argument('write_dir', type=writable_directory, help='Directory to write to.')
    parser.add_argument('invocation', help='Command invocation.')
    parser.add_argument(
        '-v',
        '--verbose',
        help='More verbose logging',
        dest="loglevel",
        default=logging.WARNING,
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        '-d',
        '--debug',
        help='Enable debugging logs',
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)

    new_uuid = str(uuid.uuid4())

    oyster = \
    {
        "component-commands": [
            "<FIXME>"
        ],
        "copying": {
            "authors": [
                "<FIXME>"
            ],
            "license-name": "MIT (Expat) License",
            "license-url": "http://opensource.org/licenses/MIT",
            "year": get_year()
        },
        "description": {
            "verbose-description": "<FIXME>"
        },
        "invocations": [
            {
                "invocation-string": args.invocation
            }
        ],
        "uuid": new_uuid
    }

    new_filename = new_uuid + '.json'
    new_filepath = os.path.join(args.write_dir, new_filename)
    with open(new_filepath, 'w') as new_file:
        json.dump(oyster, new_file, indent=4, separators=(',', ': '), sort_keys=True)
        print('Created new CmdOyster:\n{}'.format(new_filepath))
