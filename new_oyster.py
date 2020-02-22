#! /usr/bin/env python
from __future__ import print_function

import datetime
import os
import sys
import json
import uuid

def get_year():
    now = datetime.datetime.now()
    return now.year

if __name__ == '__main__':

    if len(sys.argv) > 1:
        invocation = sys.argv[1]
    else:
        sys.stderr.write("Usage: python "+sys.argv[0]+" 'command-invocation'"+'\n')
        sys.exit(1)

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
                "invocation-string": invocation
            }
        ],
        "uuid": new_uuid
    }

    root = sys.path[0]
    new_filename = new_uuid + '.json'
    new_filepath = os.path.join(root, 'cmdoysters', new_filename)
    with open(new_filepath, 'w') as new_file:
        json.dump(oyster, new_file, indent=4, separators=(',', ': '), sort_keys=True)
        print('Created new CmdOyster:\n{}'.format(new_filepath))
