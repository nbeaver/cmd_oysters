#! /usr/bin/env python2
from __future__ import print_function

import os.path
import sys
import json
import uuid

with open(os.path.join('templates', 'simple-template.json')) as template:
    oyster = json.load(template)

new_id = str(uuid.uuid4())
new_filepath = os.path.join('cmdoysters', new_id + '.json')
with open(new_filepath, 'w') as new_file:
    oyster['uuid'] = new_id
    json.dump(oyster, new_file, indent=4, separators=(',', ': '), sort_keys=True)
    print('Created new CmdOyster:\n{}'.format(new_filepath))
