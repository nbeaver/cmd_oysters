#! /usr/bin/env python3

import sys
import json
import uuid

for filepath in sys.argv[1:]:
    oyster = json.load(open(filepath))
    if 'uuid' not in oyster.keys():
        oyster['uuid'] = str(uuid.uuid4())
        with_uuid = open(filepath, 'w')
        json.dump(oyster, with_uuid, indent=4, separators=(',', ': '), sort_keys=True)
