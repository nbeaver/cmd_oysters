#! /usr/bin/env python
from __future__ import print_function

import datetime
import os.path
import sys
import json
import uuid

if len(sys.argv) > 1:
    invocation = sys.argv[1]
else:
    invocation = "<FIXME>"

now = datetime.datetime.now()
year = now.year
new_uuid = str(uuid.uuid4())

oyster = \
{
    "component-commands": [
        "<FIXME>"
    ],
    "copying": {
        "authors": [
            "Firstname Lastname"
        ],
        "license-name": "MIT (Expat) License",
        "license-url": "http://opensource.org/licenses/MIT",
        "year": year
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
