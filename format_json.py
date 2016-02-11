#! /usr/bin/env python

import sys
import json

for filepath in sys.argv[1:]:
    with open(filepath) as f:
        oyster = json.load(f)
    with open(filepath, 'w') as f:
        json.dump(oyster, f, indent=4, separators=(',', ': '), sort_keys=True)
