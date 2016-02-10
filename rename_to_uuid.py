#! /usr/bin/env python2

import os
import sys
import json
import uuid

for filepath in sys.argv[1:]:
    oyster = json.load(open(filepath))
    if 'uuid' in oyster.keys():
        expected_filepath = os.path.join(os.path.dirname(filepath), oyster['uuid'] + '.json')
        if os.path.basename(filepath) != expected_filepath:
            os.rename(filepath, expected_filepath)
