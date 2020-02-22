#! /usr/bin/env python3

import os
import sys
import json
import uuid

if __name__ == '__main__':
    for filepath in sys.argv[1:]:
        oyster = json.load(open(filepath))
        if 'uuid' in oyster.keys():
            expected_filepath = os.path.join(os.path.dirname(filepath), oyster['uuid'] + '.json')
            if os.path.basename(filepath) != expected_filepath:
                os.rename(filepath, expected_filepath)
