#! /usr/bin/env python2
from __future__ import print_function

import os.path
import sys
import json
import uuid

root = sys.path[0]
print('root =', root)
template_path = os.path.join(root, 'templates', 'simple.json')
with open(template_path) as template:
    oyster = json.load(template)

new_id = str(uuid.uuid4())
new_filename = new_id + '.json'
new_filepath = os.path.join(root, 'cmdoysters', new_filename)
with open(new_filepath, 'w') as new_file:
    oyster['uuid'] = new_id
    json.dump(oyster, new_file, indent=4, separators=(',', ': '), sort_keys=True)
    print('Created new CmdOyster:\n{}'.format(new_filepath))
